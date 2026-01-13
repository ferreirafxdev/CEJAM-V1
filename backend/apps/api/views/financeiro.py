import calendar
from datetime import timedelta
from decimal import Decimal

from django.db.models import Case, Count, DecimalField, Q, Sum, Value, When
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.alunos.models import Aluno
from apps.financeiro.models import (
    Despesa,
    PagamentoAluno,
    PagamentoAlunoHistorico,
    PagamentoProfessor,
    PlanoEducacional,
)
from apps.turmas.models import Turma

from ..serializers import (
    DespesaSerializer,
    PagamentoAlunoHistoricoSerializer,
    PagamentoAlunoSerializer,
    PagamentoProfessorSerializer,
    PlanoEducacionalSerializer,
)
from ..utils import can_access_financeiro, decimal_str, financeiro_expressions, shift_month


class PlanoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = PlanoEducacional.objects.all()
    serializer_class = PlanoEducacionalSerializer
    search_fields = ("nome",)
    ordering_fields = ("nome", "valor_mensalidade")


class PagamentoAlunoViewSet(viewsets.ModelViewSet):
    queryset = PagamentoAluno.objects.select_related(
        "aluno",
        "aluno__turma",
        "plano",
        "aluno__plano_financeiro",
    ).all()
    serializer_class = PagamentoAlunoSerializer
    search_fields = ("aluno__nome_completo", "aluno__cpf")
    ordering_fields = ("competencia", "data_vencimento", "valor")

    def get_queryset(self):
        queryset = super().get_queryset()
        aluno_id = self.request.query_params.get("aluno")
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.aplicar_regras()
        instance.save()
        self._registrar_historico(
            instance,
            PagamentoAlunoHistorico.Acao.CRIADO,
            status_novo=instance.status,
            detalhes={"origem": "api"},
        )
        self._emitir_nf_se_pago(instance)

    def perform_update(self, serializer):
        before = self._snapshot(serializer.instance)
        instance = serializer.save()
        instance.aplicar_regras()
        instance.save()
        changes = self._diff(before, instance)
        if changes:
            acao = (
                PagamentoAlunoHistorico.Acao.STATUS
                if "status" in changes
                else PagamentoAlunoHistorico.Acao.ATUALIZADO
            )
            self._registrar_historico(
                instance,
                acao,
                status_anterior=before.get("status"),
                status_novo=instance.status,
                detalhes=changes,
            )
        self._emitir_nf_se_pago(instance)

    def _snapshot(self, instance):
        fields = [
            "status",
            "forma_pagamento",
            "data_pagamento",
            "data_vencimento",
            "valor",
            "valor_pago",
            "desconto",
            "multa",
            "juros",
            "dias_atraso",
            "plano_id",
        ]
        return {field: getattr(instance, field) for field in fields}

    def _diff(self, before, instance):
        changes = {}
        for field, old_value in before.items():
            new_value = getattr(instance, field)
            if old_value != new_value:
                changes[field] = {
                    "de": str(old_value) if old_value is not None else None,
                    "para": str(new_value) if new_value is not None else None,
                }
        return changes

    def _registrar_historico(
        self,
        instance,
        acao,
        status_anterior=None,
        status_novo=None,
        detalhes=None,
    ):
        PagamentoAlunoHistorico.objects.create(
            pagamento=instance,
            acao=acao,
            status_anterior=status_anterior,
            status_novo=status_novo,
            valor_devido=instance.valor_total,
            valor_pago=instance.valor_pago or Decimal("0.00"),
            alterado_por=(
                self.request.user if self.request.user and self.request.user.is_authenticated else None
            ),
            detalhes=detalhes,
        )

    def _emitir_nf_se_pago(self, instance):
        if instance.status != PagamentoAluno.Status.PAGO:
            return
        had_nf = bool(instance.nf_pdf)
        update_fields = []
        if not instance.data_pagamento:
            instance.data_pagamento = timezone.localdate()
            update_fields.append("data_pagamento")
        if update_fields:
            instance.save(update_fields=update_fields + ["updated_at"])
        try:
            instance.emitir_nf(user=self.request.user)
        except Exception as exc:
            raise serializers.ValidationError({"detail": str(exc)}) from exc
        if not had_nf and instance.nf_pdf:
            self._registrar_historico(
                instance,
                PagamentoAlunoHistorico.Acao.NF,
                status_novo=instance.status,
                detalhes={"nf_numero": instance.nf_numero},
            )

    @action(detail=False, methods=["post"])
    def recalcular(self, request):
        queryset = self.filter_queryset(self.get_queryset()).exclude(
            status=PagamentoAluno.Status.PAGO
        )
        updated = 0
        historico = 0
        for pagamento in queryset:
            before = self._snapshot(pagamento)
            pagamento.aplicar_regras()
            changes = self._diff(before, pagamento)
            if not changes:
                continue
            pagamento.save()
            updated += 1
            acao = (
                PagamentoAlunoHistorico.Acao.STATUS
                if "status" in changes
                else PagamentoAlunoHistorico.Acao.ATUALIZADO
            )
            self._registrar_historico(
                pagamento,
                acao,
                status_anterior=before.get("status"),
                status_novo=pagamento.status,
                detalhes=changes,
            )
            historico += 1

        return Response({"updated": updated, "historico": historico})


class PagamentoAlunoHistoricoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PagamentoAlunoHistorico.objects.select_related(
        "pagamento",
        "pagamento__aluno",
        "alterado_por",
    ).all()
    serializer_class = PagamentoAlunoHistoricoSerializer
    search_fields = (
        "pagamento__aluno__nome_completo",
        "pagamento__aluno__cpf",
        "alterado_por__username",
    )
    ordering_fields = ("created_at", "acao")

    def get_queryset(self):
        queryset = super().get_queryset()
        pagamento_id = self.request.query_params.get("pagamento")
        if pagamento_id:
            queryset = queryset.filter(pagamento_id=pagamento_id)
        aluno_id = self.request.query_params.get("aluno")
        if aluno_id:
            queryset = queryset.filter(pagamento__aluno_id=aluno_id)
        return queryset


class PagamentoProfessorViewSet(viewsets.ModelViewSet):
    queryset = PagamentoProfessor.objects.select_related("professor").all()
    serializer_class = PagamentoProfessorSerializer
    search_fields = ("professor__nome_completo", "professor__cpf")
    ordering_fields = ("competencia", "valor_bruto")


class DespesaViewSet(viewsets.ModelViewSet):
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer
    search_fields = ("descricao", "categoria")
    ordering_fields = ("data", "valor")


class FinanceiroDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not can_access_financeiro(request.user):
            return Response(
                {"detail": "Acesso financeiro nao autorizado."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.localdate()
        months = request.query_params.get("months")
        try:
            months = int(months) if months else 12
        except ValueError:
            months = 12
        months = min(max(months, 1), 36)
        start = shift_month(today.replace(day=1), -(months - 1))

        zero, valor_total_expr, valor_recebido_expr = financeiro_expressions()
        base_qs = PagamentoAluno.objects.select_related(
            "aluno",
            "aluno__turma",
            "plano",
            "aluno__plano_financeiro",
        )
        period_qs = base_qs.filter(competencia__gte=start, competencia__lte=today)
        paid_qs = period_qs.filter(status=PagamentoAluno.Status.PAGO)

        receita_mes = (
            paid_qs.filter(
                competencia__year=today.year,
                competencia__month=today.month,
            ).aggregate(total=Sum(valor_recebido_expr))
        ).get("total") or Decimal("0.00")

        receita_periodo = (
            paid_qs.aggregate(total=Sum(valor_recebido_expr))
        ).get("total") or Decimal("0.00")

        mes_qs = period_qs.filter(
            competencia__year=today.year,
            competencia__month=today.month,
        )
        total_mes = mes_qs.exclude(status=PagamentoAluno.Status.ISENTO).count()
        inadimplentes_mes = mes_qs.filter(
            status__in=[PagamentoAluno.Status.EM_ABERTO, PagamentoAluno.Status.ATRASADO]
        ).count()
        taxa_inadimplencia = (
            (inadimplentes_mes / total_mes) * 100 if total_mes else 0
        )

        inadimplentes_alunos = (
            PagamentoAluno.objects.filter(
                status__in=[PagamentoAluno.Status.EM_ABERTO, PagamentoAluno.Status.ATRASADO],
                data_vencimento__lt=today,
            )
            .values("aluno_id")
            .distinct()
            .count()
        )
        total_alunos = Aluno.objects.count()
        adimplentes_alunos = max(total_alunos - inadimplentes_alunos, 0)

        receita_por_turma = []
        for item in (
            paid_qs.values("aluno__turma__id", "aluno__turma__nome")
            .annotate(total=Sum(valor_recebido_expr))
            .order_by("-total")
        ):
            receita_por_turma.append(
                {
                    "turma_id": item["aluno__turma__id"],
                    "turma": item["aluno__turma__nome"] or "Sem turma",
                    "total": decimal_str(item["total"]),
                }
            )

        receita_por_plano = []
        for item in (
            paid_qs.annotate(
                plano_nome=Coalesce(
                    "plano__nome",
                    "aluno__plano_financeiro__nome",
                    Value("Sem plano"),
                )
            )
            .values("plano_nome")
            .annotate(total=Sum(valor_recebido_expr))
            .order_by("-total")
        ):
            receita_por_plano.append(
                {
                    "plano": item["plano_nome"],
                    "total": decimal_str(item["total"]),
                }
            )

        status_labels = dict(PagamentoAluno.Status.choices)
        status_pagamentos = []
        for item in (
            period_qs.values("status")
            .annotate(total=Count("id"))
            .order_by("-total")
        ):
            status_value = item["status"]
            status_pagamentos.append(
                {
                    "status": status_value,
                    "label": status_labels.get(status_value, status_value),
                    "total": item["total"],
                }
            )

        evolucao_receita = []
        for item in (
            paid_qs.annotate(mes=TruncMonth("competencia"))
            .values("mes")
            .annotate(total=Sum(valor_recebido_expr))
            .order_by("mes")
        ):
            mes = item["mes"]
            evolucao_receita.append(
                {
                    "mes": mes.strftime("%Y-%m") if mes else "",
                    "total": decimal_str(item["total"]),
                }
            )

        pagamentos_por_turma = []
        for item in (
            period_qs.values("aluno__turma__id", "aluno__turma__nome")
            .annotate(total=Count("id"))
            .order_by("-total")
        ):
            pagamentos_por_turma.append(
                {
                    "turma_id": item["aluno__turma__id"],
                    "turma": item["aluno__turma__nome"] or "Sem turma",
                    "total": item["total"],
                }
            )

        inadimplencia_heatmap = []
        for item in (
            period_qs.filter(
                status__in=[PagamentoAluno.Status.EM_ABERTO, PagamentoAluno.Status.ATRASADO]
            )
            .exclude(data_vencimento__isnull=True)
            .annotate(mes=TruncMonth("data_vencimento"))
            .values("mes")
            .annotate(
                total=Count("id"),
                valor=Sum(valor_total_expr),
            )
            .order_by("mes")
        ):
            mes = item["mes"]
            inadimplencia_heatmap.append(
                {
                    "mes": mes.strftime("%Y-%m") if mes else "",
                    "inadimplentes": item["total"],
                    "valor": decimal_str(item["valor"]),
                }
            )

        previsto_realizado = []
        for item in (
            period_qs.annotate(mes=TruncMonth("competencia"))
            .values("mes")
            .annotate(
                previsto=Sum(
                    Case(
                        When(status=PagamentoAluno.Status.ISENTO, then=zero),
                        default=valor_total_expr,
                        output_field=DecimalField(max_digits=12, decimal_places=2),
                    )
                ),
                realizado=Sum(
                    Case(
                        When(status=PagamentoAluno.Status.PAGO, then=valor_recebido_expr),
                        default=zero,
                        output_field=DecimalField(max_digits=12, decimal_places=2),
                    )
                ),
            )
            .order_by("mes")
        ):
            mes = item["mes"]
            previsto_realizado.append(
                {
                    "mes": mes.strftime("%Y-%m") if mes else "",
                    "previsto": decimal_str(item["previsto"]),
                    "realizado": decimal_str(item["realizado"]),
                }
            )

        receita_media = (
            paid_qs.aggregate(
                total=Sum(valor_recebido_expr),
                alunos=Count("aluno", distinct=True),
            )
        )
        total_receita = receita_media.get("total") or Decimal("0.00")
        alunos_receita = receita_media.get("alunos") or 0
        ticket_medio = total_receita / alunos_receita if alunos_receita else Decimal("0.00")

        payload = {
            "periodo": {
                "inicio": start.isoformat(),
                "fim": today.isoformat(),
                "meses": months,
            },
            "kpis": {
                "receita_mes": decimal_str(receita_mes),
                "receita_periodo": decimal_str(receita_periodo),
                "taxa_inadimplencia": f"{taxa_inadimplencia:.2f}",
                "alunos_adimplentes": adimplentes_alunos,
                "alunos_inadimplentes": inadimplentes_alunos,
                "ticket_medio": decimal_str(ticket_medio),
            },
            "charts": {
                "receita_mensal": evolucao_receita,
                "pagamentos_por_turma": pagamentos_por_turma,
                "status_pagamentos": status_pagamentos,
                "inadimplencia_heatmap": inadimplencia_heatmap,
                "previsto_vs_realizado": previsto_realizado,
                "receita_por_turma": receita_por_turma,
                "receita_por_plano": receita_por_plano,
            },
        }
        return Response(payload)


class FinanceiroRelatoriosView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not can_access_financeiro(request.user):
            return Response(
                {"detail": "Acesso financeiro nao autorizado."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.localdate()
        _, valor_total_expr, valor_recebido_expr = financeiro_expressions()

        limite = today - timedelta(days=30)
        inadimplentes_qs = PagamentoAluno.objects.select_related("aluno", "aluno__turma").filter(
            status__in=[PagamentoAluno.Status.EM_ABERTO, PagamentoAluno.Status.ATRASADO],
            data_vencimento__lt=limite,
        )
        inadimplentes_map = {}
        for pagamento in inadimplentes_qs:
            if not pagamento.data_vencimento:
                continue
            dias_atraso = (today - pagamento.data_vencimento).days
            item = inadimplentes_map.get(pagamento.aluno_id)
            if not item:
                item = {
                    "aluno_id": pagamento.aluno_id,
                    "aluno": pagamento.aluno.nome_completo,
                    "turma": getattr(pagamento.aluno.turma, "nome", ""),
                    "dias_atraso": dias_atraso,
                    "valor_devido": Decimal("0.00"),
                    "ultimo_vencimento": pagamento.data_vencimento,
                }
            item["valor_devido"] += pagamento.valor_total
            if dias_atraso > item["dias_atraso"]:
                item["dias_atraso"] = dias_atraso
                item["ultimo_vencimento"] = pagamento.data_vencimento
            inadimplentes_map[pagamento.aluno_id] = item

        inadimplentes = []
        for item in inadimplentes_map.values():
            inadimplentes.append(
                {
                    "aluno_id": item["aluno_id"],
                    "aluno": item["aluno"],
                    "turma": item["turma"],
                    "dias_atraso": item["dias_atraso"],
                    "valor_devido": decimal_str(item["valor_devido"]),
                    "ultimo_vencimento": (
                        item["ultimo_vencimento"].isoformat()
                        if item["ultimo_vencimento"]
                        else ""
                    ),
                }
            )
        inadimplentes.sort(key=lambda x: x["dias_atraso"], reverse=True)

        turma_top = (
            PagamentoAluno.objects.select_related("aluno", "aluno__turma")
            .filter(status=PagamentoAluno.Status.PAGO)
            .values("aluno__turma__id", "aluno__turma__nome")
            .annotate(total=Sum(valor_recebido_expr))
            .order_by("-total")
            .first()
        )
        turma_maior_receita = None
        if turma_top:
            turma_maior_receita = {
                "turma_id": turma_top["aluno__turma__id"],
                "turma": turma_top["aluno__turma__nome"] or "Sem turma",
                "total": decimal_str(turma_top["total"]),
            }

        plano_stats = []
        for item in (
            PagamentoAluno.objects.annotate(
                plano_nome=Coalesce(
                    "plano__nome",
                    "aluno__plano_financeiro__nome",
                    Value("Sem plano"),
                )
            )
            .values("plano_nome")
            .annotate(
                total=Count("id"),
                inadimplentes=Count(
                    "id",
                    filter=Q(
                        status__in=[
                            PagamentoAluno.Status.EM_ABERTO,
                            PagamentoAluno.Status.ATRASADO,
                        ]
                    ),
                ),
            )
        ):
            total = item["total"] or 0
            inadimplentes_count = item["inadimplentes"] or 0
            taxa = (inadimplentes_count / total) * 100 if total else 0
            plano_stats.append(
                {
                    "plano": item["plano_nome"],
                    "total": total,
                    "inadimplentes": inadimplentes_count,
                    "taxa_inadimplencia": taxa,
                }
            )
        plano_stats.sort(key=lambda x: x["taxa_inadimplencia"], reverse=True)
        plano_maior_inadimplencia = plano_stats[0] if plano_stats else None
        if plano_maior_inadimplencia:
            plano_maior_inadimplencia = {
                "plano": plano_maior_inadimplencia["plano"],
                "total": plano_maior_inadimplencia["total"],
                "inadimplentes": plano_maior_inadimplencia["inadimplentes"],
                "taxa_inadimplencia": f"{plano_maior_inadimplencia['taxa_inadimplencia']:.2f}",
            }

        proj_months = request.query_params.get("projecao")
        try:
            proj_months = int(proj_months) if proj_months else 6
        except ValueError:
            proj_months = 6
        proj_months = min(max(proj_months, 1), 24)
        proj_start = shift_month(today.replace(day=1), 1)
        proj_end = shift_month(proj_start, proj_months - 1)
        proj_end = proj_end.replace(day=calendar.monthrange(proj_end.year, proj_end.month)[1])

        projecao = []
        for item in (
            PagamentoAluno.objects.filter(
                competencia__gte=proj_start,
                competencia__lte=proj_end,
            )
            .exclude(status=PagamentoAluno.Status.ISENTO)
            .annotate(mes=TruncMonth("competencia"))
            .values("mes")
            .annotate(total=Sum(valor_total_expr))
            .order_by("mes")
        ):
            mes = item["mes"]
            projecao.append(
                {
                    "mes": mes.strftime("%Y-%m") if mes else "",
                    "total": decimal_str(item["total"]),
                }
            )

        payload = {
            "inadimplentes_mais_30_dias": inadimplentes[:200],
            "turma_maior_receita": turma_maior_receita,
            "plano_maior_inadimplencia": plano_maior_inadimplencia,
            "projecao_receita": projecao,
        }
        return Response(payload)
