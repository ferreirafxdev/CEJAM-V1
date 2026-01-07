from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers

from apps.alunos.models import Aluno
from apps.cadastros.models import Escola, Responsavel
from apps.contratos.models import Assinatura, Contrato, TemplateContrato
from apps.financeiro.models import (
    Despesa,
    PagamentoAluno,
    PagamentoAlunoHistorico,
    PagamentoProfessor,
    PlanoEducacional,
)
from apps.professores.models import Professor
from apps.turmas.models import Turma


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "name", "codename", "content_type")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "permissions")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "password",
        )

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        permissions = validated_data.pop("user_permissions", [])
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        if groups:
            user.groups.set(groups)
        if permissions:
            user.user_permissions.set(permissions)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop("groups", None)
        permissions = validated_data.pop("user_permissions", None)
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        if permissions is not None:
            instance.user_permissions.set(permissions)
        return instance


class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = "__all__"


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = "__all__"


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


class PlanoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoEducacional
        fields = "__all__"


class PagamentoAlunoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source="aluno.nome_completo", read_only=True)
    turma_nome = serializers.CharField(source="aluno.turma.nome", read_only=True)
    plano_nome = serializers.SerializerMethodField()
    nf_pdf_url = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()

    class Meta:
        model = PagamentoAluno
        fields = "__all__"
        read_only_fields = (
            "desconto",
            "multa",
            "juros",
            "dias_atraso",
            "valor_total",
            "nf_numero",
            "nf_pdf",
            "nf_emitida_em",
            "pagamento_registrado_em",
        )

    def get_nf_pdf_url(self, obj):
        request = self.context.get("request")
        if obj.nf_pdf and request:
            return request.build_absolute_uri(obj.nf_pdf.url)
        if obj.nf_pdf:
            return obj.nf_pdf.url
        return ""

    def get_plano_nome(self, obj):
        if obj.plano:
            return obj.plano.nome
        aluno_plano = getattr(obj.aluno, "plano_financeiro", None)
        if aluno_plano:
            return aluno_plano.nome
        return ""

    def get_valor_total(self, obj):
        return str(obj.valor_total)


class PagamentoAlunoHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagamentoAlunoHistorico
        fields = "__all__"


class PagamentoProfessorSerializer(serializers.ModelSerializer):
    professor_nome = serializers.CharField(source="professor.nome_completo", read_only=True)

    class Meta:
        model = PagamentoProfessor
        fields = "__all__"


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = "__all__"


class TemplateContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateContrato
        fields = "__all__"


class ContratoSerializer(serializers.ModelSerializer):
    escola_nome = serializers.CharField(source="escola.nome_fantasia", read_only=True)
    aluno_nome = serializers.CharField(source="aluno.nome_completo", read_only=True)
    responsavel_nome = serializers.CharField(source="responsavel.nome_completo", read_only=True)
    turma_nome = serializers.CharField(source="turma.nome", read_only=True)
    plano_nome = serializers.CharField(source="plano.nome", read_only=True)
    template_nome = serializers.CharField(source="template.nome", read_only=True)
    gerado_por_username = serializers.CharField(source="gerado_por.username", read_only=True)
    pdf_url = serializers.SerializerMethodField()
    qr_payload = serializers.SerializerMethodField()

    class Meta:
        model = Contrato
        fields = "__all__"

    def get_pdf_url(self, obj):
        request = self.context.get("request")
        if obj.pdf_gerado and request:
            return request.build_absolute_uri(obj.pdf_gerado.url)
        if obj.pdf_gerado:
            return obj.pdf_gerado.url
        return ""

    def get_qr_payload(self, obj):
        return obj.qr_payload()


class AssinaturaSerializer(serializers.ModelSerializer):
    contrato_numero = serializers.CharField(source="contrato.numero", read_only=True)

    class Meta:
        model = Assinatura
        fields = "__all__"
