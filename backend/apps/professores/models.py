from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Professor(models.Model):
    class TipoVinculo(models.TextChoices):
        CLT = "CLT", "CLT"
        HORISTA = "HORISTA", "Horista"
        PJ = "PJ", "PJ"

    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        INATIVO = "INATIVO", "Inativo"

    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
    )
    especialidade = models.CharField(max_length=120)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    tipo_vinculo = models.CharField(max_length=10, choices=TipoVinculo.choices)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salario_fixo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def clean(self):
        if self.tipo_vinculo == self.TipoVinculo.CLT and not self.salario_fixo:
            raise ValidationError({"salario_fixo": "Informe o salario fixo para CLT."})
        if self.tipo_vinculo == self.TipoVinculo.HORISTA and not self.valor_hora:
            raise ValidationError({"valor_hora": "Informe o valor por hora para Horista."})

    def __str__(self):
        return self.nome_completo
