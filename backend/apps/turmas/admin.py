from django.contrib import admin

from .models import Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "serie_ano",
        "turno",
        "professor_responsavel",
        "valor_mensalidade",
        "capacidade_maxima",
        "status",
        "total_alunos",
    )
    list_filter = ("status", "turno", "serie_ano")
    search_fields = ("nome", "serie_ano", "professor_responsavel__nome_completo")
    list_select_related = ("professor_responsavel",)
    readonly_fields = ("created_at", "updated_at", "total_alunos")
    fieldsets = (
        ("Identificacao", {"fields": ("nome", "serie_ano", "turno")}),
        (
            "Equipe",
            {"fields": ("professor_responsavel", "capacidade_maxima", "status")},
        ),
        ("Financeiro", {"fields": ("valor_mensalidade",)}),
        ("Indicadores", {"fields": ("total_alunos",)}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Total alunos")
    def total_alunos(self, obj):
        return obj.alunos.count()
