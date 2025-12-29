import decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("turmas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="turma",
            name="valor_mensalidade",
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=10),
            preserve_default=False,
        ),
    ]
