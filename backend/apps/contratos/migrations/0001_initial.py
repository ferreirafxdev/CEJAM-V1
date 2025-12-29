from django.conf import settings
from django.core.validators import RegexValidator
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

import apps.contratos.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cadastros", "0001_initial"),
        ("alunos", "0002_aluno_responsavel_matricula"),
        ("turmas", "0002_turma_valor_mensalidade"),
        ("financeiro", "0002_planoeducacional"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TemplateContrato",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("versao", models.CharField(max_length=20)),
                ("corpo_html", models.TextField()),
                ("css", models.TextField(blank=True)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-updated_at", "nome"],
            },
        ),
        migrations.CreateModel(
            name="Contrato",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero", models.CharField(blank=True, max_length=20, unique=True)),
                ("data_emissao", models.DateField(default=django.utils.timezone.localdate)),
                ("cidade_assinatura", models.CharField(max_length=120)),
                (
                    "status",
                    models.CharField(
                        choices=[("RASCUNHO", "Rascunho"), ("EMITIDO", "Emitido"), ("CANCELADO", "Cancelado")],
                        default="RASCUNHO",
                        max_length=10,
                    ),
                ),
                ("pdf_gerado", models.FileField(blank=True, null=True, upload_to=apps.contratos.models.contrato_pdf_path)),
                ("pdf_hash", models.CharField(blank=True, max_length=64)),
                ("snapshot", models.JSONField(blank=True, null=True)),
                ("gerado_em", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contratos",
                        to="alunos.aluno",
                    ),
                ),
                (
                    "escola",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contratos",
                        to="cadastros.escola",
                    ),
                ),
                (
                    "gerado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="contratos_gerados",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "plano",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contratos",
                        to="financeiro.planoeducacional",
                    ),
                ),
                (
                    "responsavel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contratos",
                        to="cadastros.responsavel",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contratos",
                        to="contratos.templatecontrato",
                    ),
                ),
                (
                    "turma",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contratos",
                        to="turmas.turma",
                    ),
                ),
            ],
            options={
                "ordering": ["-data_emissao", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Assinatura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("RESPONSAVEL", "Responsavel"),
                            ("ESCOLA", "Escola"),
                            ("TESTEMUNHA_1", "Testemunha 1"),
                            ("TESTEMUNHA_2", "Testemunha 2"),
                        ],
                        max_length=20,
                    ),
                ),
                ("nome", models.CharField(max_length=200)),
                (
                    "cpf",
                    models.CharField(
                        max_length=11,
                        validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
                    ),
                ),
                ("data_assinatura", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "contrato",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assinaturas",
                        to="contratos.contrato",
                    ),
                ),
            ],
            options={
                "ordering": ["tipo", "nome"],
            },
        ),
    ]
