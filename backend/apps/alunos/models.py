from django.core.validators import RegexValidator
from django.db import models


class Aluno(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMININO = "F", "Feminino"
        OUTRO = "O", "Outro"

    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        INATIVO = "INATIVO", "Inativo"

    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
    )
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    responsavel = models.ForeignKey(
        "cadastros.Responsavel",
        on_delete=models.PROTECT,
        related_name="alunos",
        null=True,
        blank=True,
    )
    nome_responsavel = models.CharField(max_length=200, blank=True)
    telefone_responsavel = models.CharField(max_length=20, blank=True)
    email_responsavel = models.EmailField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVO)
    data_matricula = models.DateField()
    numero_matricula = models.CharField(max_length=30, unique=True, null=True, blank=True)
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.PROTECT,
        related_name="alunos",
    )
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    historico_escolar = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self):
        return self.nome_completo
