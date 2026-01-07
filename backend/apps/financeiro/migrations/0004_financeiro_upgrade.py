import decimal

from django.db import migrations, models
import django.db.models.deletion


def migrar_status_pagamento(apps, schema_editor):
    PagamentoAluno = apps.get_model("financeiro", "PagamentoAluno")
    PagamentoAluno.objects.filter(status="PENDENTE").update(status="EM_ABERTO")


class Migration(migrations.Migration):
    dependencies = [
        ("financeiro", "0003_pagamentoaluno_nf"),
    ]

    operations = [
        migrations.AddField(
            model_name="planoeducacional",
            name="modelo_pagamento",
            field=models.CharField(
                choices=[
                    ("MENSAL", "Mensal"),
                    ("TRIMESTRAL", "Trimestral"),
                    ("SEMESTRAL", "Semestral"),
                    ("ANUAL", "Anual"),
                ],
                default="MENSAL",
                max_length=12,
            ),
        ),
        migrations.AddField(
            model_name="planoeducacional",
            name="desconto_percent",
            field=models.DecimalField(
                decimal_places=2,
                default=decimal.Decimal("0.00"),
                max_digits=5,
            ),
        ),
        migrations.AddField(
            model_name="planoeducacional",
            name="bolsa_tipo",
            field=models.CharField(
                choices=[
                    ("NENHUMA", "Nenhuma"),
                    ("PARCIAL", "Parcial"),
                    ("INTEGRAL", "Integral"),
                    ("CONVENIO", "Convenio"),
                ],
                default="NENHUMA",
                max_length=12,
            ),
        ),
        migrations.AddField(
            model_name="planoeducacional",
            name="bolsa_percent",
            field=models.DecimalField(
                decimal_places=2,
                default=decimal.Decimal("0.00"),
                max_digits=5,
            ),
        ),
        migrations.AddField(
            model_name="planoeducacional",
            name="juros_diario_percent",
            field=models.DecimalField(
                decimal_places=2,
                default=decimal.Decimal("0.00"),
                max_digits=5,
            ),
        ),
        migrations.AddField(
            model_name="planoeducacional",
            name="forma_pagamento_padrao",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DINHEIRO", "Dinheiro"),
                    ("PIX", "Pix"),
                    ("BOLETO", "Boleto"),
                    ("CARTAO", "Cartao"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="planoeducacional",
            name="ativo",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="plano",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pagamentos_alunos",
                to="financeiro.planoeducacional",
            ),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="valor_pago",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="desconto",
            field=models.DecimalField(
                decimal_places=2,
                default=decimal.Decimal("0.00"),
                max_digits=10,
            ),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="juros",
            field=models.DecimalField(
                decimal_places=2,
                default=decimal.Decimal("0.00"),
                max_digits=10,
            ),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="dias_atraso",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="pagamentoaluno",
            name="status",
            field=models.CharField(
                choices=[
                    ("PAGO", "Pago"),
                    ("EM_ABERTO", "Em aberto"),
                    ("ATRASADO", "Atrasado"),
                    ("ISENTO", "Isento"),
                ],
                default="EM_ABERTO",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="PagamentoAlunoHistorico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "acao",
                    models.CharField(
                        choices=[
                            ("CRIADO", "Criado"),
                            ("ATUALIZADO", "Atualizado"),
                            ("STATUS", "Status"),
                            ("NF", "Nota fiscal"),
                        ],
                        max_length=12,
                    ),
                ),
                ("status_anterior", models.CharField(blank=True, max_length=10, null=True)),
                ("status_novo", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "valor_devido",
                    models.DecimalField(
                        decimal_places=2,
                        default=decimal.Decimal("0.00"),
                        max_digits=10,
                    ),
                ),
                (
                    "valor_pago",
                    models.DecimalField(
                        decimal_places=2,
                        default=decimal.Decimal("0.00"),
                        max_digits=10,
                    ),
                ),
                ("detalhes", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "alterado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pagamentos_alunos_historico",
                        to="auth.user",
                    ),
                ),
                (
                    "pagamento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="historico",
                        to="financeiro.pagamentoaluno",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.RunPython(migrar_status_pagamento, migrations.RunPython.noop),
    ]
