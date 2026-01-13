from rest_framework import serializers

from apps.alunos.models import Aluno
from apps.cadastros.models import Responsavel
from apps.financeiro.models import PlanoEducacional
from apps.professores.models import Professor
from apps.turmas.models import Turma


class AlunoSerializer(serializers.ModelSerializer):
    responsavel_nome = serializers.CharField(source="responsavel.nome_completo", read_only=True)
    turma_nome = serializers.CharField(source="turma.nome", read_only=True)
    plano_financeiro_nome = serializers.CharField(
        source="plano_financeiro.nome",
        read_only=True,
    )
    responsavel = serializers.PrimaryKeyRelatedField(
        queryset=Responsavel.objects.all(),
        required=False,
        allow_null=True,
    )
    turma = serializers.PrimaryKeyRelatedField(queryset=Turma.objects.all())
    plano_financeiro = serializers.PrimaryKeyRelatedField(
        queryset=PlanoEducacional.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Aluno
        fields = (
            "id",
            "nome_completo",
            "cpf",
            "data_nascimento",
            "sexo",
            "endereco",
            "telefone",
            "responsavel",
            "nome_responsavel",
            "telefone_responsavel",
            "email_responsavel",
            "status",
            "data_matricula",
            "numero_matricula",
            "turma",
            "plano_financeiro",
            "valor_mensalidade",
            "observacoes",
            "historico_escolar",
            "created_at",
            "updated_at",
            "responsavel_nome",
            "turma_nome",
            "plano_financeiro_nome",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "responsavel_nome",
            "turma_nome",
            "plano_financeiro_nome",
        )
        extra_kwargs = {
            "nome_completo": {
                "required": True,
                "allow_blank": False,
                "error_messages": {"required": "Informe o nome completo."},
            },
            "cpf": {"required": False, "allow_blank": True, "allow_null": True},
            "data_nascimento": {
                "required": True,
                "error_messages": {"required": "Informe a data de nascimento."},
            },
            "sexo": {"required": True, "error_messages": {"required": "Informe o sexo."}},
            "endereco": {
                "required": True,
                "allow_blank": False,
                "error_messages": {"required": "Informe o endereco."},
            },
            "telefone": {
                "required": True,
                "allow_blank": False,
                "error_messages": {"required": "Informe o telefone."},
            },
            "responsavel": {"required": False, "allow_null": True},
            "nome_responsavel": {"required": False, "allow_blank": True},
            "telefone_responsavel": {"required": False, "allow_blank": True},
            "email_responsavel": {"required": False, "allow_blank": True},
            "status": {"required": False, "default": Aluno.Status.ATIVO},
            "data_matricula": {
                "required": True,
                "error_messages": {"required": "Informe a data de matricula."},
            },
            "numero_matricula": {"required": False, "allow_blank": True, "allow_null": True},
            "turma": {"required": True, "error_messages": {"required": "Informe a turma."}},
            "plano_financeiro": {"required": False, "allow_null": True},
            "valor_mensalidade": {
                "required": True,
                "error_messages": {"required": "Informe o valor da mensalidade."},
            },
            "observacoes": {"required": False, "allow_blank": True},
            "historico_escolar": {"required": False, "allow_blank": True},
        }

    def validate_cpf(self, value):
        if value in {"", None}:
            return None
        return value

    def validate_numero_matricula(self, value):
        if value in {"", None}:
            return None
        return value


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = "__all__"


class TurmaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.CharField(
        source="professor_responsavel.nome_completo",
        read_only=True,
    )

    class Meta:
        model = Turma
        fields = "__all__"
