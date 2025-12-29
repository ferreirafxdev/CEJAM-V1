from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Assinatura, Contrato, TemplateContrato
from .services import gerar_pdf_contrato


@admin.register(TemplateContrato)
class TemplateContratoAdmin(admin.ModelAdmin):
    list_display = ("nome", "versao", "ativo", "updated_at")
    list_filter = ("ativo",)
    search_fields = ("nome", "versao")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Template", {"fields": ("nome", "versao", "ativo")}),
        ("Conteudo", {"fields": ("corpo_html", "css")}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    change_form_template = "admin/contratos/contrato/change_form.html"
    list_display = ("numero", "aluno", "responsavel", "turma", "plano", "status", "data_emissao")
    list_filter = ("status", ("data_emissao", admin.DateFieldListFilter), "escola")
    search_fields = ("numero", "aluno__nome_completo", "aluno__cpf", "responsavel__nome_completo", "responsavel__cpf")
    list_select_related = ("aluno", "responsavel", "turma", "plano", "escola")
    date_hierarchy = "data_emissao"
    readonly_fields = (
        "numero",
        "pdf_hash",
        "pdf_visualizar",
        "qr_payload",
        "gerado_em",
        "gerado_por",
        "snapshot",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        ("Identificacao", {"fields": ("numero", "status", "data_emissao", "cidade_assinatura")}),
        ("Relacionamentos", {"fields": ("escola", "aluno", "responsavel", "turma", "plano", "template")}),
        ("PDF", {"fields": ("pdf_visualizar", "pdf_hash", "qr_payload", "snapshot")}),
        ("Auditoria", {"fields": ("gerado_por", "gerado_em", "created_at", "updated_at")}),
    )
    actions = ["gerar_pdf_em_lote"]

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.status != Contrato.Status.RASCUNHO:
            model_fields = [field.name for field in self.model._meta.fields]
            return sorted(set(readonly + model_fields + ["pdf_visualizar"]))
        return readonly

    @admin.display(description="PDF gerado")
    def pdf_visualizar(self, obj):
        if not obj or not obj.pdf_gerado:
            return "-"
        return format_html('<a href="{}" target="_blank">Baixar PDF</a>', obj.pdf_gerado.url)

    @admin.display(description="Payload QR")
    def qr_payload(self, obj):
        if not obj:
            return "-"
        return obj.qr_payload() or "-"

    @admin.action(description="Gerar PDF dos contratos selecionados")
    def gerar_pdf_em_lote(self, request, queryset):
        total = 0
        for contrato in queryset:
            if contrato.status != Contrato.Status.RASCUNHO:
                continue
            gerar_pdf_contrato(contrato, request.user)
            total += 1
        if total:
            self.message_user(request, f"{total} contrato(s) emitido(s) com sucesso.", messages.SUCCESS)
        else:
            self.message_user(request, "Nenhum contrato em rascunho para emitir.", messages.WARNING)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/gerar-pdf/",
                self.admin_site.admin_view(self.gerar_pdf_view),
                name="contratos_contrato_gerar_pdf",
            )
        ]
        return custom_urls + urls

    def gerar_pdf_view(self, request, object_id):
        contrato = self.get_object(request, object_id)
        if not contrato:
            self.message_user(request, "Contrato nao encontrado.", messages.ERROR)
            return redirect("..")
        if contrato.status != Contrato.Status.RASCUNHO:
            self.message_user(request, "Contrato ja emitido ou cancelado.", messages.WARNING)
            return redirect(reverse("admin:contratos_contrato_change", args=[contrato.pk]))
        try:
            gerar_pdf_contrato(contrato, request.user)
        except Exception as exc:
            self.message_user(request, f"Erro ao gerar PDF: {exc}", messages.ERROR)
        else:
            self.message_user(request, "PDF gerado com sucesso.", messages.SUCCESS)
        return redirect(reverse("admin:contratos_contrato_change", args=[contrato.pk]))


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ("contrato", "tipo", "nome", "cpf", "data_assinatura")
    list_filter = ("tipo", ("data_assinatura", admin.DateFieldListFilter))
    search_fields = ("contrato__numero", "nome", "cpf")
    list_select_related = ("contrato",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Assinatura", {"fields": ("contrato", "tipo", "nome", "cpf", "data_assinatura")}),
        ("Auditoria", {"fields": ("created_at",)}),
    )
