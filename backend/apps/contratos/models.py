from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.utils import timezone


def contrato_pdf_path(instance, filename):
    numero = instance.numero or "rascunho"
    return f"contratos/{numero}/{filename}"


class TemplateContrato(models.Model):
    nome = models.CharField(max_length=120)
    versao = models.CharField(max_length=20)
    corpo_html = models.TextField()
    css = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "nome"]

    def __str__(self):
        return f"{self.nome} v{self.versao}"


class Contrato(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = "RASCUNHO", "Rascunho"
        EMITIDO = "EMITIDO", "Emitido"
        CANCELADO = "CANCELADO", "Cancelado"

    numero = models.CharField(max_length=20, unique=True, blank=True)
    escola = models.ForeignKey(
        "cadastros.Escola",
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    aluno = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    responsavel = models.ForeignKey(
        "cadastros.Responsavel",
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    plano = models.ForeignKey(
        "financeiro.PlanoEducacional",
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    template = models.ForeignKey(
        TemplateContrato,
        on_delete=models.PROTECT,
        related_name="contratos",
    )
    data_emissao = models.DateField(default=timezone.localdate)
    cidade_assinatura = models.CharField(max_length=120)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RASCUNHO)
    pdf_gerado = models.FileField(upload_to=contrato_pdf_path, blank=True, null=True)
    pdf_hash = models.CharField(max_length=64, blank=True)
    snapshot = models.JSONField(blank=True, null=True)
    gerado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contratos_gerados",
    )
    gerado_em = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data_emissao", "-created_at"]

    def __str__(self):
        return self.numero or "Contrato (rascunho)"

    def qr_payload(self):
        if not self.numero or not self.pdf_hash:
            return ""
        return f"{self.numero}|{self.pdf_hash}"

    def _gerar_numero(self):
        ano = (self.data_emissao or timezone.localdate()).year
        prefix = f"CEJAM-{ano}-"
        ultimo = (
            Contrato.objects.select_for_update()
            .filter(numero__startswith=prefix)
            .order_by("-numero")
            .first()
        )
        ultimo_seq = 0
        if ultimo and ultimo.numero:
            try:
                ultimo_seq = int(ultimo.numero.split("-")[-1])
            except (ValueError, IndexError):
                ultimo_seq = 0
        return f"{prefix}{ultimo_seq + 1:06d}"

    def save(self, *args, **kwargs):
        if not self.numero:
            with transaction.atomic():
                if not self.data_emissao:
                    self.data_emissao = timezone.localdate()
                self.numero = self._gerar_numero()
        super().save(*args, **kwargs)


class Assinatura(models.Model):
    class Tipo(models.TextChoices):
        RESPONSAVEL = "RESPONSAVEL", "Responsavel"
        ESCOLA = "ESCOLA", "Escola"
        TESTEMUNHA_1 = "TESTEMUNHA_1", "Testemunha 1"
        TESTEMUNHA_2 = "TESTEMUNHA_2", "Testemunha 2"

    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name="assinaturas",
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(
        max_length=11,
        validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
    )
    data_assinatura = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tipo", "nome"]

    def __str__(self):
        return f"{self.contrato} - {self.get_tipo_display()}"
