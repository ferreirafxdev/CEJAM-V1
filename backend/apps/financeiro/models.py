from decimal import Decimal

from django.db import models


class PlanoEducacional(models.Model):
    nome = models.CharField(max_length=120)
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField()
    duracao_meses = models.PositiveSmallIntegerField()
    taxa_matricula = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    multa_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    juros_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class PagamentoAluno(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = "DINHEIRO", "Dinheiro"
        PIX = "PIX", "Pix"
        BOLETO = "BOLETO", "Boleto"

    class Status(models.TextChoices):
        PAGO = "PAGO", "Pago"
        PENDENTE = "PENDENTE", "Pendente"
        ATRASADO = "ATRASADO", "Atrasado"

    aluno = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.PROTECT,
        related_name="pagamentos",
    )
    competencia = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=10, choices=FormaPagamento.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-competencia", "aluno__nome_completo"]

    def __str__(self):
        return f"{self.aluno} - {self.competencia:%m/%Y}"


class PagamentoProfessor(models.Model):
    class Status(models.TextChoices):
        PAGO = "PAGO", "Pago"
        PENDENTE = "PENDENTE", "Pendente"

    professor = models.ForeignKey(
        "professores.Professor",
        on_delete=models.PROTECT,
        related_name="pagamentos",
    )
    competencia = models.DateField()
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    descontos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-competencia", "professor__nome_completo"]

    def save(self, *args, **kwargs):
        if self.valor_liquido is None:
            # Auto-calc net value when not provided.
            self.valor_liquido = (self.valor_bruto or Decimal("0.00")) - (
                self.descontos or Decimal("0.00")
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.professor} - {self.competencia:%m/%Y}"


class Despesa(models.Model):
    class Categoria(models.TextChoices):
        AGUA = "AGUA", "Agua"
        LUZ = "LUZ", "Luz"
        ALUGUEL = "ALUGUEL", "Aluguel"
        INTERNET = "INTERNET", "Internet"
        MATERIAL = "MATERIAL", "Material"
        OUTROS = "OUTROS", "Outros"

    class Tipo(models.TextChoices):
        FIXA = "FIXA", "Fixa"
        VARIAVEL = "VARIAVEL", "Variavel"

    descricao = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data", "descricao"]

    def __str__(self):
        return self.descricao
