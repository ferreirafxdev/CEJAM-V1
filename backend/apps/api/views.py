import calendar
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.core.cache import cache
from django.db.models import (
    Case,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Q,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.alunos.models import Aluno
from apps.cadastros.models import Escola, Responsavel
from apps.contratos.models import Assinatura, Contrato, TemplateContrato
from apps.contratos.services import gerar_pdf_contrato
from apps.financeiro.models import (
    Despesa,
    PagamentoAluno,
    PagamentoAlunoHistorico,
    PagamentoProfessor,
    PlanoEducacional,
)
from apps.professores.models import Professor
from apps.turmas.models import Turma

from .serializers import (
    AlunoSerializer,
    AssinaturaSerializer,
    ContratoSerializer,
    DespesaSerializer,
    EscolaSerializer,
    GroupSerializer,
    PagamentoAlunoSerializer,
    PagamentoAlunoHistoricoSerializer,
    PagamentoProfessorSerializer,
    PermissionSerializer,
    PlanoEducacionalSerializer,
    ProfessorSerializer,
    ResponsavelSerializer,
    TemplateContratoSerializer,
    TurmaSerializer,
    UserSerializer,
)

def _can_access_financeiro(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return any(
        perm.startswith("financeiro.") for perm in user.get_all_permissions()
    )


def _shift_month(date_value, months):
    month_index = (date_value.month - 1) + months
    year = date_value.year + (month_index // 12)
    month = (month_index % 12) + 1
    day = min(date_value.day, calendar.monthrange(year, month)[1])
    return date_value.replace(year=year, month=month, day=day)


def _financeiro_expressions():
    zero = Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))
    valor = Coalesce(F("valor"), zero)
    desconto = Coalesce(F("desconto"), zero)
    multa = Coalesce(F("multa"), zero)
    juros = Coalesce(F("juros"), zero)
    valor_total = ExpressionWrapper(
        valor - desconto + multa + juros,
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )
    valor_recebido = Coalesce(
        F("valor_pago"),
        valor_total,
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )
    return zero, valor_total, valor_recebido


def _decimal_str(value):
    return str(value or Decimal("0.00"))


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.select_related("content_type").all()
    serializer_class = PermissionSerializer
    search_fields = ("name", "codename", "content_type__app_label")
    ordering_fields = ("name", "codename")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.prefetch_related("permissions").all()
    serializer_class = GroupSerializer
    search_fields = ("name",)
    ordering_fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("groups", "user_permissions").all()
    serializer_class = UserSerializer
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("username", "email")


class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer
    search_fields = ("razao_social", "nome_fantasia", "cnpj")
    ordering_fields = ("nome_fantasia", "cidade")


class ResponsavelViewSet(viewsets.ModelViewSet):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    search_fields = ("nome_completo", "cpf", "email")
    ordering_fields = ("nome_completo",)


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.select_related("turma", "responsavel").all()
    serializer_class = AlunoSerializer
    search_fields = ("nome_completo", "cpf", "numero_matricula", "nome_responsavel")
    ordering_fields = ("nome_completo", "data_matricula")


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    search_fields = ("nome_completo", "cpf", "especialidade")
    ordering_fields = ("nome_completo",)


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.select_related("professor_responsavel").all()
    serializer_class = TurmaSerializer
    search_fields = ("nome", "serie_ano")
    ordering_fields = ("nome", "serie_ano")


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


class TemplateContratoViewSet(viewsets.ModelViewSet):
    queryset = TemplateContrato.objects.all()
    serializer_class = TemplateContratoSerializer
    search_fields = ("nome", "versao")
    ordering_fields = ("nome", "updated_at")


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related(
        "escola",
        "aluno",
        "responsavel",
        "turma",
        "plano",
        "template",
        "gerado_por",
    ).all()
    serializer_class = ContratoSerializer
    search_fields = ("numero", "aluno__nome_completo", "responsavel__nome_completo")
    ordering_fields = ("data_emissao", "numero")

    def update(self, request, *args, **kwargs):
        contrato = self.get_object()
        if contrato.status != Contrato.Status.RASCUNHO:
            return Response(
                {"detail": "Contrato emitido ou cancelado nao pode ser alterado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def gerar_pdf(self, request, pk=None):
        contrato = self.get_object()
        try:
            gerar_pdf_contrato(contrato, request.user)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(contrato)
        return Response(serializer.data)


class AssinaturaViewSet(viewsets.ModelViewSet):
    queryset = Assinatura.objects.select_related("contrato").all()
    serializer_class = AssinaturaSerializer
    search_fields = ("contrato__numero", "nome", "cpf")
    ordering_fields = ("data_assinatura", "tipo")


class FinanceiroDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not _can_access_financeiro(request.user):
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
        start = _shift_month(today.replace(day=1), -(months - 1))

        zero, valor_total_expr, valor_recebido_expr = _financeiro_expressions()
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
                    "total": _decimal_str(item["total"]),
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
                    "total": _decimal_str(item["total"]),
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
                    "total": _decimal_str(item["total"]),
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
                    "valor": _decimal_str(item["valor"]),
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
                    "previsto": _decimal_str(item["previsto"]),
                    "realizado": _decimal_str(item["realizado"]),
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
                "receita_mes": _decimal_str(receita_mes),
                "receita_periodo": _decimal_str(receita_periodo),
                "taxa_inadimplencia": f"{taxa_inadimplencia:.2f}",
                "alunos_adimplentes": adimplentes_alunos,
                "alunos_inadimplentes": inadimplentes_alunos,
                "ticket_medio": _decimal_str(ticket_medio),
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
        if not _can_access_financeiro(request.user):
            return Response(
                {"detail": "Acesso financeiro nao autorizado."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.localdate()
        _, valor_total_expr, valor_recebido_expr = _financeiro_expressions()

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
                    "valor_devido": _decimal_str(item["valor_devido"]),
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
                "total": _decimal_str(turma_top["total"]),
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
        proj_start = _shift_month(today.replace(day=1), 1)
        proj_end = _shift_month(proj_start, proj_months - 1)
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
                    "total": _decimal_str(item["total"]),
                }
            )

        payload = {
            "inadimplentes_mais_30_dias": inadimplentes[:200],
            "turma_maior_receita": turma_maior_receita,
            "plano_maior_inadimplencia": plano_maior_inadimplencia,
            "projecao_receita": projecao,
        }
        return Response(payload)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        can_access_financeiro = _can_access_financeiro(request.user)
        cache_key = f"dashboard:{request.user.pk or 'anon'}:{'fin' if can_access_financeiro else 'basic'}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        receita_mes = Decimal("0.00")

        if can_access_financeiro:
            _, _, valor_recebido_expr = _financeiro_expressions()
            receita_mes = (
                PagamentoAluno.objects.filter(
                    competencia__year=today.year,
                    competencia__month=today.month,
                    status=PagamentoAluno.Status.PAGO,
                ).aggregate(total=Sum(valor_recebido_expr))
            ).get("total") or Decimal("0.00")

        stats = {
            "total_alunos": Aluno.objects.count(),
            "turmas_ativas": Turma.objects.filter(status=Turma.Status.ATIVA).count(),
            "turnos_ativos": (
                Turma.objects.filter(status=Turma.Status.ATIVA)
                .values("turno")
                .distinct()
                .count()
            ),
            "contratos_emitidos": Contrato.objects.filter(status=Contrato.Status.EMITIDO).count(),
            "receita_mes": str(receita_mes),
        }

        atividades = []

        def adicionar_atividade(tipo, mensagem, timestamp):
            if not timestamp:
                return
            atividades.append(
                {"type": tipo, "message": mensagem, "timestamp": timestamp}
            )

        ultimo_aluno = Aluno.objects.order_by("-created_at").first()
        if ultimo_aluno:
            adicionar_atividade(
                "aluno",
                f"Nova matricula: {ultimo_aluno.nome_completo}",
                ultimo_aluno.created_at,
            )

        ultimo_pagamento = (
            PagamentoAluno.objects.select_related("aluno")
            .filter(status=PagamentoAluno.Status.PAGO)
            .order_by("-created_at")
            .first()
        )
        if can_access_financeiro and ultimo_pagamento:
            adicionar_atividade(
                "pagamento",
                f"Pagamento recebido: {ultimo_pagamento.aluno.nome_completo}",
                ultimo_pagamento.created_at,
            )

        ultimo_contrato = (
            Contrato.objects.filter(status=Contrato.Status.EMITIDO)
            .order_by("-created_at")
            .first()
        )
        if ultimo_contrato:
            adicionar_atividade(
                "contrato",
                f"Contrato emitido: {ultimo_contrato.numero}",
                ultimo_contrato.created_at,
            )

        ultima_turma = Turma.objects.order_by("-updated_at").first()
        if ultima_turma:
            adicionar_atividade(
                "turma",
                f"Turma {ultima_turma.nome} atualizada",
                ultima_turma.updated_at,
            )

        atividades.sort(key=lambda item: item["timestamp"], reverse=True)
        for atividade in atividades:
            atividade["timestamp"] = atividade["timestamp"].isoformat()

        payload = {"stats": stats, "recent_activity": atividades[:4]}
        cache.set(cache_key, payload, timeout=getattr(settings, "DASHBOARD_CACHE_TTL", 30))
        return Response(payload)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "groups": list(user.groups.values_list("name", flat=True)),
            "can_access_financeiro": _can_access_financeiro(user),
        }
        return Response(data)
