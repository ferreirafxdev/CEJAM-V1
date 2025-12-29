from django.contrib import admin

from .models import Escola, Responsavel


@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ("nome_fantasia", "cnpj", "cidade", "uf", "telefone", "email")
    search_fields = ("razao_social", "nome_fantasia", "cnpj")
    list_filter = ("uf",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Identificacao", {"fields": ("razao_social", "nome_fantasia", "cnpj")}),
        ("Endereco", {"fields": ("endereco_completo", "cidade", "uf")}),
        ("Contato", {"fields": ("telefone", "email", "responsavel")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "cpf", "telefone", "email")
    search_fields = ("nome_completo", "cpf")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Identificacao", {"fields": ("nome_completo", "cpf", "rg")}),
        ("Contato", {"fields": ("endereco", "telefone", "email")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )
