from django.core.validators import RegexValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("turmas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Aluno",
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
                ("data_nascimento", models.DateField()),
                (
                    "sexo",
                    models.CharField(
                        choices=[("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")],
                        max_length=1,
                    ),
                ),
                ("endereco", models.TextField()),
                ("telefone", models.CharField(max_length=20)),
                ("nome_responsavel", models.CharField(max_length=200)),
                ("telefone_responsavel", models.CharField(max_length=20)),
                ("email_responsavel", models.EmailField(max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[("ATIVO", "Ativo"), ("INATIVO", "Inativo")],
                        default="ATIVO",
                        max_length=10,
                    ),
                ),
                ("data_matricula", models.DateField()),
                ("valor_mensalidade", models.DecimalField(decimal_places=2, max_digits=10)),
                ("observacoes", models.TextField(blank=True)),
                ("historico_escolar", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "turma",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="alunos",
                        to="turmas.turma",
                    ),
                ),
            ],
            options={
                "ordering": ["nome_completo"],
            },
        ),
    ]
