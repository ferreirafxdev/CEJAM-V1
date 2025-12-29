from django.db import migrations

from apps.contratos.defaults import DEFAULT_TEMPLATE_CSS, DEFAULT_TEMPLATE_HTML


def create_default_template(apps, schema_editor):
    TemplateContrato = apps.get_model("contratos", "TemplateContrato")
    if TemplateContrato.objects.filter(nome="CEJAM - Modelo Padrao", versao="1.0").exists():
        return
    TemplateContrato.objects.create(
        nome="CEJAM - Modelo Padrao",
        versao="1.0",
        corpo_html=DEFAULT_TEMPLATE_HTML,
        css=DEFAULT_TEMPLATE_CSS,
        ativo=True,
    )


def remove_default_template(apps, schema_editor):
    TemplateContrato = apps.get_model("contratos", "TemplateContrato")
    TemplateContrato.objects.filter(nome="CEJAM - Modelo Padrao", versao="1.0").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contratos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_template, remove_default_template),
    ]
