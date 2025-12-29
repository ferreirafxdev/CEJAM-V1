from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Professor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome_completo", models.CharField(max_length=200)),
                (
                    "cpf",
                    models.CharField(
                        max_length=11,
                        unique=True,
                        validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
                    ),
                ),
                ("especialidade", models.CharField(max_length=120)),
                ("telefone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                (
                    "tipo_vinculo",
                    models.CharField(
                        choices=[("CLT", "CLT"), ("HORISTA", "Horista"), ("PJ", "PJ")],
                        max_length=10,
                    ),
                ),
                (
                    "valor_hora",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "salario_fixo",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ATIVO", "Ativo"), ("INATIVO", "Inativo")],
                        default="ATIVO",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nome_completo"],
            },
        ),
    ]
