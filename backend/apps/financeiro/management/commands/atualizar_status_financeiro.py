from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.financeiro.models import PagamentoAluno, PagamentoAlunoHistorico


def _snapshot(instance):
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


def _diff(before, instance):
    changes = {}
    for field, old_value in before.items():
        new_value = getattr(instance, field)
        if old_value != new_value:
            changes[field] = {
                "de": str(old_value) if old_value is not None else None,
                "para": str(new_value) if new_value is not None else None,
            }
    return changes


class Command(BaseCommand):
    help = "Atualiza multas, juros e status dos pagamentos em aberto."

    def handle(self, *args, **options):
        updated = 0
        historico = 0
        queryset = PagamentoAluno.objects.exclude(status=PagamentoAluno.Status.PAGO)
        for pagamento in queryset:
            before = _snapshot(pagamento)
            pagamento.aplicar_regras()
            changes = _diff(before, pagamento)
            if not changes:
                continue
            pagamento.save()
            updated += 1
            acao = (
                PagamentoAlunoHistorico.Acao.STATUS
                if "status" in changes
                else PagamentoAlunoHistorico.Acao.ATUALIZADO
            )
            PagamentoAlunoHistorico.objects.create(
                pagamento=pagamento,
                acao=acao,
                status_anterior=before.get("status"),
                status_novo=pagamento.status,
                valor_devido=pagamento.valor_total,
                valor_pago=pagamento.valor_pago or Decimal("0.00"),
                detalhes=changes,
            )
            historico += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Atualizados: {updated}. Historicos: {historico}."
            )
        )
