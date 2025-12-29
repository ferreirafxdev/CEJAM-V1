from django.core.validators import RegexValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("alunos", "0001_initial"),
        ("cadastros", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="responsavel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="alunos",
                to="cadastros.responsavel",
            ),
        ),
        migrations.AddField(
            model_name="aluno",
            name="numero_matricula",
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="aluno",
            name="cpf",
            field=models.CharField(
                blank=True,
                max_length=11,
                null=True,
                unique=True,
                validators=[RegexValidator(r"^\d{11}$", "CPF deve conter 11 digitos.")],
            ),
        ),
        migrations.AlterField(
            model_name="aluno",
            name="nome_responsavel",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="aluno",
            name="telefone_responsavel",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="aluno",
            name="email_responsavel",
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
