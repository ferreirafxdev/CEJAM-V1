import calendar
from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, Value
from django.db.models.functions import Coalesce


def can_access_financeiro(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return any(perm.startswith("financeiro.") for perm in user.get_all_permissions())


def shift_month(date_value, months):
    month_index = (date_value.month - 1) + months
    year = date_value.year + (month_index // 12)
    month = (month_index % 12) + 1
    day = min(date_value.day, calendar.monthrange(year, month)[1])
    return date_value.replace(year=year, month=month, day=day)


def financeiro_expressions():
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


def decimal_str(value):
    return str(value or Decimal("0.00"))
