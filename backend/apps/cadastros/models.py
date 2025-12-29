from django.core.validators import RegexValidator
from django.db import models


class Escola(models.Model):
    razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200)
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^\d{14}$", "CNPJ deve conter 14 digitos.")],
    )
    endereco_completo = models.TextField()
    cidade = models.CharField(max_length=120)
    uf = models.CharField(max_length=2)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    responsavel = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_fantasia", "razao_social"]

    def __str__(self):
        return self.nome_fantasia or self.razao_social


class Responsavel(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
    )
    rg = models.CharField(max_length=20, blank=True)
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo
