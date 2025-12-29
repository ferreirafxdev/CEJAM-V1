from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("professores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Turma",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("serie_ano", models.CharField(max_length=50)),
                (
                    "turno",
                    models.CharField(
                        choices=[("MANHA", "Manha"), ("TARDE", "Tarde"), ("NOITE", "Noite")],
                        max_length=10,
                    ),
                ),
                ("capacidade_maxima", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("ATIVA", "Ativa"), ("ENCERRADA", "Encerrada")],
                        default="ATIVA",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "professor_responsavel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="turmas",
                        to="professores.professor",
                    ),
                ),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
    ]
