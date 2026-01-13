from decimal import Decimal

from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.alunos.models import Aluno
from apps.contratos.models import Contrato
from apps.financeiro.models import PagamentoAluno
from apps.turmas.models import Turma

from ..utils import can_access_financeiro, financeiro_expressions


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        can_access_financeiro = can_access_financeiro(request.user)
        cache_key = f"dashboard:{request.user.pk or 'anon'}:{'fin' if can_access_financeiro else 'basic'}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        receita_mes = Decimal("0.00")

        if can_access_financeiro:
            _, _, valor_recebido_expr = financeiro_expressions()
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
