import decimal

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("alunos", "0001_initial"),
        ("professores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PagamentoAluno",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("competencia", models.DateField()),
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
                ("data_vencimento", models.DateField()),
                ("data_pagamento", models.DateField(blank=True, null=True)),
                (
                    "forma_pagamento",
                    models.CharField(
                        choices=[
                            ("DINHEIRO", "Dinheiro"),
                            ("PIX", "Pix"),
                            ("BOLETO", "Boleto"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PAGO", "Pago"),
                            ("PENDENTE", "Pendente"),
                            ("ATRASADO", "Atrasado"),
                        ],
                        default="PENDENTE",
                        max_length=10,
                    ),
                ),
                (
                    "multa",
                    models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=10),
                ),
                ("observacoes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pagamentos",
                        to="alunos.aluno",
                    ),
                ),
            ],
            options={
                "ordering": ["-competencia", "aluno__nome_completo"],
            },
        ),
        migrations.CreateModel(
            name="PagamentoProfessor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("competencia", models.DateField()),
                ("valor_bruto", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "descontos",
                    models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=10),
                ),
                (
                    "valor_liquido",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
                ),
                ("data_pagamento", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("PAGO", "Pago"), ("PENDENTE", "Pendente")],
                        default="PENDENTE",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "professor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pagamentos",
                        to="professores.professor",
                    ),
                ),
            ],
            options={
                "ordering": ["-competencia", "professor__nome_completo"],
            },
        ),
        migrations.CreateModel(
            name="Despesa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("descricao", models.CharField(max_length=200)),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("AGUA", "Agua"),
                            ("LUZ", "Luz"),
                            ("ALUGUEL", "Aluguel"),
                            ("INTERNET", "Internet"),
                            ("MATERIAL", "Material"),
                            ("OUTROS", "Outros"),
                        ],
                        max_length=20,
                    ),
                ),
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
                ("data", models.DateField()),
                (
                    "tipo",
                    models.CharField(
                        choices=[("FIXA", "Fixa"), ("VARIAVEL", "Variavel")],
                        max_length=10,
                    ),
                ),
                ("observacoes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-data", "descricao"],
            },
        ),
    ]
