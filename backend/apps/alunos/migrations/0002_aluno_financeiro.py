from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("financeiro", "0004_financeiro_upgrade"),
        ("alunos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="plano_financeiro",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="alunos",
                to="financeiro.planoeducacional",
            ),
        ),
        migrations.AlterField(
            model_name="aluno",
            name="status",
            field=models.CharField(
                choices=[("ATIVO", "Ativo"), ("INATIVO", "Inativo"), ("TRANCADO", "Trancado")],
                default="ATIVO",
                max_length=10,
            ),
        ),
    ]
