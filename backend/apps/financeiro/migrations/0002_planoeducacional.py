import decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("financeiro", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlanoEducacional",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("valor_mensalidade", models.DecimalField(decimal_places=2, max_digits=10)),
                ("dia_vencimento", models.PositiveSmallIntegerField()),
                ("duracao_meses", models.PositiveSmallIntegerField()),
                (
                    "taxa_matricula",
                    models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=10),
                ),
                (
                    "multa_percent",
                    models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=5),
                ),
                (
                    "juros_percent",
                    models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=5),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
    ]
