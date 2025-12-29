from django.contrib import admin

from .models import Aluno


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "cpf", "numero_matricula", "turma", "status", "data_matricula")
    list_filter = ("status", "turma", "sexo")
    search_fields = ("nome_completo", "cpf", "numero_matricula", "responsavel__nome_completo", "nome_responsavel")
    list_select_related = ("turma", "responsavel")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Dados do aluno", {"fields": ("nome_completo", "cpf", "data_nascimento", "sexo")}),
        ("Contato", {"fields": ("endereco", "telefone")}),
        ("Responsavel", {"fields": ("responsavel",)}),
        (
            "Responsavel (legado)",
            {"fields": ("nome_responsavel", "telefone_responsavel", "email_responsavel")},
        ),
        (
            "Matricula",
            {"fields": ("status", "data_matricula", "numero_matricula", "turma", "valor_mensalidade")},
        ),
        ("Historico", {"fields": ("observacoes", "historico_escolar")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )
