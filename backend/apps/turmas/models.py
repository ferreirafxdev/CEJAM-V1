from django.db import models


class Turma(models.Model):
    class Turno(models.TextChoices):
        MANHA = "MANHA", "Manha"
        TARDE = "TARDE", "Tarde"
        NOITE = "NOITE", "Noite"

    class Status(models.TextChoices):
        ATIVA = "ATIVA", "Ativa"
        ENCERRADA = "ENCERRADA", "Encerrada"

    nome = models.CharField(max_length=120)
    serie_ano = models.CharField(max_length=50)
    turno = models.CharField(max_length=10, choices=Turno.choices)
    professor_responsavel = models.ForeignKey(
        "professores.Professor",
        on_delete=models.PROTECT,
        related_name="turmas",
    )
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    capacidade_maxima = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVA)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.serie_ano})"
