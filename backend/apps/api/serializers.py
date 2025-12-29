from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers

from apps.alunos.models import Aluno
from apps.cadastros.models import Escola, Responsavel
from apps.contratos.models import Assinatura, Contrato, TemplateContrato
from apps.financeiro.models import Despesa, PagamentoAluno, PagamentoProfessor, PlanoEducacional
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

    class Meta:
        model = Aluno
        fields = "__all__"


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

    class Meta:
        model = PagamentoAluno
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
