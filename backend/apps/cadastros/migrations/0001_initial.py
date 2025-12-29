from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Escola",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("razao_social", models.CharField(max_length=200)),
                ("nome_fantasia", models.CharField(max_length=200)),
                (
                    "cnpj",
                    models.CharField(
                        max_length=14,
                        unique=True,
                        validators=[RegexValidator(r"^\d{14}$", "CNPJ deve conter 14 digitos.")],
                    ),
                ),
                ("endereco_completo", models.TextField()),
                ("cidade", models.CharField(max_length=120)),
                ("uf", models.CharField(max_length=2)),
                ("telefone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("responsavel", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nome_fantasia", "razao_social"],
            },
        ),
        migrations.CreateModel(
            name="Responsavel",
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
                ("rg", models.CharField(blank=True, max_length=20)),
                ("endereco", models.TextField()),
                ("telefone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nome_completo"],
            },
        ),
    ]
