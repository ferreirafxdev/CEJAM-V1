from django.contrib import admin

from .models import Professor


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "cpf", "especialidade", "tipo_vinculo", "status")
    list_filter = ("status", "tipo_vinculo")
    search_fields = ("nome_completo", "cpf", "especialidade")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Dados principais", {"fields": ("nome_completo", "cpf", "especialidade")}),
        ("Contato", {"fields": ("telefone", "email")}),
        (
            "Vinculo",
            {"fields": ("tipo_vinculo", "valor_hora", "salario_fixo", "status")},
        ),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )
