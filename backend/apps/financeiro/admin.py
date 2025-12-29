from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum

from .models import Despesa, PagamentoAluno, PagamentoProfessor, PlanoEducacional


@admin.register(PlanoEducacional)
class PlanoEducacionalAdmin(admin.ModelAdmin):
    list_display = ("nome", "valor_mensalidade", "dia_vencimento", "duracao_meses")
    search_fields = ("nome",)
    list_filter = ("dia_vencimento", "duracao_meses")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Plano", {"fields": ("nome", "valor_mensalidade", "dia_vencimento", "duracao_meses")}),
        ("Encargos", {"fields": ("taxa_matricula", "multa_percent", "juros_percent")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(PagamentoAluno)
class PagamentoAlunoAdmin(admin.ModelAdmin):
    change_list_template = "admin/financeiro/pagamentoaluno/change_list.html"
    list_display = (
        "aluno",
        "competencia",
        "valor",
        "data_vencimento",
        "data_pagamento",
        "forma_pagamento",
        "status",
    )
    list_filter = (
        "status",
        "forma_pagamento",
        ("competencia", admin.DateFieldListFilter),
        "aluno__turma",
    )
    date_hierarchy = "competencia"
    search_fields = ("aluno__nome_completo", "aluno__cpf")
    list_select_related = ("aluno", "aluno__turma")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Pagamento", {"fields": ("aluno", "competencia", "valor", "multa")}),
        (
            "Datas",
            {"fields": ("data_vencimento", "data_pagamento", "forma_pagamento", "status")},
        ),
        ("Observacoes", {"fields": ("observacoes",)}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            queryset = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        totals = queryset.filter(status=PagamentoAluno.Status.PAGO).aggregate(
            total_recebido=Sum("valor"),
            total_multa=Sum("multa"),
        )
        response.context_data["total_recebido"] = totals["total_recebido"] or Decimal("0.00")
        response.context_data["total_multa"] = totals["total_multa"] or Decimal("0.00")
        return response


@admin.register(PagamentoProfessor)
class PagamentoProfessorAdmin(admin.ModelAdmin):
    change_list_template = "admin/financeiro/pagamentoprofessor/change_list.html"
    list_display = (
        "professor",
        "competencia",
        "valor_bruto",
        "descontos",
        "valor_liquido",
        "data_pagamento",
        "status",
    )
    list_filter = ("status", ("competencia", admin.DateFieldListFilter))
    date_hierarchy = "competencia"
    search_fields = ("professor__nome_completo", "professor__cpf")
    list_select_related = ("professor",)
    readonly_fields = ("valor_liquido", "created_at", "updated_at")
    fieldsets = (
        (
            "Pagamento",
            {"fields": ("professor", "competencia", "valor_bruto", "descontos", "valor_liquido")},
        ),
        ("Status", {"fields": ("data_pagamento", "status")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            queryset = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        totals = queryset.filter(status=PagamentoProfessor.Status.PAGO).aggregate(
            total_pago=Sum("valor_liquido")
        )
        response.context_data["total_pago"] = totals["total_pago"] or Decimal("0.00")
        return response


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "categoria", "valor", "data", "tipo")
    list_filter = ("categoria", "tipo", "data")
    search_fields = ("descricao",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Despesa", {"fields": ("descricao", "categoria", "valor", "data", "tipo")}),
        ("Observacoes", {"fields": ("observacoes",)}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )
