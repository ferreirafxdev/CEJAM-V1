from django.conf import settings
from django.template import loader
from django.utils import timezone

from apps.contratos.services import _render_pdf


def _format_currency(value):
    if value is None:
        return "0,00"
    valor = f"{value:,.2f}"
    return valor.replace(",", "X").replace(".", ",").replace("X", ".")


def _format_percent(value):
    if value is None:
        return "0,00"
    valor = f"{value:,.2f}"
    return valor.replace(",", "X").replace(".", ",").replace("X", ".")


def _format_date(value):
    if not value:
        return "--"
    return value.strftime("%d/%m/%Y")


def _format_datetime(value):
    if not value:
        return "--"
    local = timezone.localtime(value) if timezone.is_aware(value) else value
    return local.strftime("%d/%m/%Y %H:%M")


def build_nota_fiscal_context(pagamento):
    aluno = pagamento.aluno
    turma = getattr(aluno, "turma", None)
    valor = pagamento.valor or 0
    desconto = pagamento.desconto or 0
    multa = pagamento.multa or 0
    juros = pagamento.juros or 0
    base = valor - desconto
    base = base if base > 0 else 0
    juros_percent = (juros / base * 100) if base else 0
    registro = pagamento.pagamento_registrado_em or pagamento.updated_at
    total = pagamento.valor_total
    valor_pago = pagamento.valor_pago or 0

    emitida = pagamento.nf_emitida_em or timezone.now()
    status_label = pagamento.get_status_display() if pagamento.status else "--"
    forma_label = (
        pagamento.get_forma_pagamento_display()
        if pagamento.forma_pagamento
        else "--"
    )
    return {
        "pagamento": pagamento,
        "aluno": aluno,
        "turma": turma,
        "nf_numero": pagamento.nf_numero,
        "nf_emitida_em": emitida,
        "nf_emitida_em_formatada": _format_datetime(emitida),
        "competencia_formatada": _format_date(pagamento.competencia),
        "vencimento_formatado": _format_date(pagamento.data_vencimento),
        "pagamento_formatado": _format_date(pagamento.data_pagamento),
        "registro_formatado": _format_datetime(registro),
        "valor_formatado": _format_currency(valor),
        "desconto_formatado": _format_currency(desconto),
        "multa_formatada": _format_currency(multa),
        "juros_formatado": _format_currency(juros),
        "juros_percent_formatado": _format_percent(juros_percent),
        "total_formatado": _format_currency(total),
        "valor_pago_formatado": _format_currency(valor_pago),
        "status_label": status_label,
        "forma_pagamento_label": forma_label,
        "media_url": settings.MEDIA_URL,
    }


def gerar_pdf_nota_fiscal(pagamento):
    context = build_nota_fiscal_context(pagamento)
    html = loader.render_to_string("financeiro/nota_fiscal.html", context)
    return _render_pdf(html, base_url=str(settings.BASE_DIR))
