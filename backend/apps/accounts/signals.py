from django.apps import apps
from django.contrib.auth.models import Group, Permission


def _permission_codenames(actions, model_labels):
    codenames = []
    for model_label in model_labels:
        app_label, model_name = model_label.split(".")
        model = apps.get_model(app_label, model_name)
        for action in actions:
            codenames.append(f"{action}_{model._meta.model_name}")
    return codenames


def create_default_groups(sender, **kwargs):
    auth_models = [
        "auth.User",
        "auth.Group",
        "auth.Permission",
    ]
    domain_models = [
        "cadastros.Escola",
        "cadastros.Responsavel",
        "alunos.Aluno",
        "turmas.Turma",
        "professores.Professor",
        "financeiro.PlanoEducacional",
        "financeiro.PagamentoAluno",
        "financeiro.PagamentoProfessor",
        "financeiro.Despesa",
        "contratos.TemplateContrato",
        "contratos.Contrato",
        "contratos.Assinatura",
    ]
    all_models = auth_models + domain_models

    # Default groups and permissions for Django Admin access control.
    group_definitions = {
        "Administrador": {"models": all_models, "actions": ["add", "change", "delete", "view"]},
        "Diretor": {"models": domain_models, "actions": ["add", "change", "view"]},
        "Coordenacao": {
            "models": [
                "alunos.Aluno",
                "turmas.Turma",
                "professores.Professor",
                "contratos.Contrato",
            ],
            "actions": ["add", "change", "view"],
        },
        "Professor": {"models": ["alunos.Aluno", "turmas.Turma"], "actions": ["view"]},
        "Secretaria": {
            "models": [
                "cadastros.Escola",
                "cadastros.Responsavel",
                "alunos.Aluno",
                "turmas.Turma",
                "financeiro.PlanoEducacional",
                "financeiro.PagamentoAluno",
                "financeiro.Despesa",
                "contratos.Contrato",
            ],
            "actions": ["add", "change", "view"],
        },
    }

    for group_name, config in group_definitions.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        codenames = _permission_codenames(config["actions"], config["models"])
        permissions = Permission.objects.filter(codename__in=codenames)
        group.permissions.set(permissions)
