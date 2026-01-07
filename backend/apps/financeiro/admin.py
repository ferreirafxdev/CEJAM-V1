from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum

from .models import (
    Despesa,
    PagamentoAluno,
    PagamentoAlunoHistorico,
    PagamentoProfessor,
    PlanoEducacional,
)


@admin.register(PlanoEducacional)
class PlanoEducacionalAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "valor_mensalidade",
        "modelo_pagamento",
        "dia_vencimento",
        "duracao_meses",
        "ativo",
    )
    search_fields = ("nome",)
    list_filter = ("modelo_pagamento", "dia_vencimento", "duracao_meses", "ativo")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Plano",
            {
                "fields": (
                    "nome",
                    "valor_mensalidade",
                    "modelo_pagamento",
                    "dia_vencimento",
                    "duracao_meses",
                    "forma_pagamento_padrao",
                    "ativo",
                )
            },
        ),
        (
            "Descontos e bolsas",
            {"fields": ("desconto_percent", "bolsa_tipo", "bolsa_percent")},
        ),
        (
            "Encargos",
            {"fields": ("taxa_matricula", "multa_percent", "juros_percent", "juros_diario_percent")},
        ),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(PagamentoAluno)
class PagamentoAlunoAdmin(admin.ModelAdmin):
    change_list_template = "admin/financeiro/pagamentoaluno/change_list.html"
    list_display = (
        "aluno",
        "competencia",
        "valor",
        "valor_pago",
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
    readonly_fields = (
        "pagamento_registrado_em",
        "nf_numero",
        "nf_pdf",
        "nf_emitida_em",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Pagamento",
            {
                "fields": (
                    "aluno",
                    "plano",
                    "competencia",
                    "valor",
                    "valor_pago",
                    "desconto",
                    "multa",
                    "juros",
                    "dias_atraso",
                )
            },
        ),
        (
            "Datas",
            {"fields": ("data_vencimento", "data_pagamento", "forma_pagamento", "status")},
        ),
        ("Observacoes", {"fields": ("observacoes",)}),
        ("Nota fiscal", {"fields": ("nf_numero", "nf_pdf", "nf_emitida_em")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            queryset = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        totals = queryset.filter(status=PagamentoAluno.Status.PAGO).aggregate(
            total_recebido=Sum("valor_pago"),
            total_multa=Sum("multa"),
        )
        response.context_data["total_recebido"] = totals["total_recebido"] or Decimal("0.00")
        response.context_data["total_multa"] = totals["total_multa"] or Decimal("0.00")
        return response


@admin.register(PagamentoAlunoHistorico)
class PagamentoAlunoHistoricoAdmin(admin.ModelAdmin):
    list_display = ("pagamento", "acao", "status_anterior", "status_novo", "created_at")
    list_filter = ("acao", "status_novo")
    search_fields = ("pagamento__aluno__nome_completo", "pagamento__aluno__cpf")
    readonly_fields = ("created_at",)


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
