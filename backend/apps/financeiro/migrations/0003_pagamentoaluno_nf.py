from django.db import migrations, models

import apps.financeiro.models


class Migration(migrations.Migration):
    dependencies = [
        ("financeiro", "0002_planoeducacional"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pagamentoaluno",
            name="forma_pagamento",
            field=models.CharField(
                choices=[
                    ("DINHEIRO", "Dinheiro"),
                    ("PIX", "Pix"),
                    ("BOLETO", "Boleto"),
                    ("CARTAO", "Cartao"),
                ],
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="pagamento_registrado_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="nf_numero",
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="nf_pdf",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=apps.financeiro.models.nota_fiscal_pdf_path,
            ),
        ),
        migrations.AddField(
            model_name="pagamentoaluno",
            name="nf_emitida_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
