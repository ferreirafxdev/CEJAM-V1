from django.contrib.auth.models import Group, Permission, User
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.alunos.models import Aluno
from apps.cadastros.models import Escola, Responsavel
from apps.contratos.models import Assinatura, Contrato, TemplateContrato
from apps.contratos.services import gerar_pdf_contrato
from apps.financeiro.models import Despesa, PagamentoAluno, PagamentoProfessor, PlanoEducacional
from apps.professores.models import Professor
from apps.turmas.models import Turma

from .serializers import (
    AlunoSerializer,
    AssinaturaSerializer,
    ContratoSerializer,
    DespesaSerializer,
    EscolaSerializer,
    GroupSerializer,
    PagamentoAlunoSerializer,
    PagamentoProfessorSerializer,
    PermissionSerializer,
    PlanoEducacionalSerializer,
    ProfessorSerializer,
    ResponsavelSerializer,
    TemplateContratoSerializer,
    TurmaSerializer,
    UserSerializer,
)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.select_related("content_type").all()
    serializer_class = PermissionSerializer
    search_fields = ("name", "codename", "content_type__app_label")
    ordering_fields = ("name", "codename")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.prefetch_related("permissions").all()
    serializer_class = GroupSerializer
    search_fields = ("name",)
    ordering_fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("groups", "user_permissions").all()
    serializer_class = UserSerializer
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("username", "email")


class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer
    search_fields = ("razao_social", "nome_fantasia", "cnpj")
    ordering_fields = ("nome_fantasia", "cidade")


class ResponsavelViewSet(viewsets.ModelViewSet):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    search_fields = ("nome_completo", "cpf", "email")
    ordering_fields = ("nome_completo",)


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.select_related("turma", "responsavel").all()
    serializer_class = AlunoSerializer
    search_fields = ("nome_completo", "cpf", "numero_matricula", "nome_responsavel")
    ordering_fields = ("nome_completo", "data_matricula")


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    search_fields = ("nome_completo", "cpf", "especialidade")
    ordering_fields = ("nome_completo",)


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.select_related("professor_responsavel").all()
    serializer_class = TurmaSerializer
    search_fields = ("nome", "serie_ano")
    ordering_fields = ("nome", "serie_ano")


class PlanoEducacionalViewSet(viewsets.ModelViewSet):
    queryset = PlanoEducacional.objects.all()
    serializer_class = PlanoEducacionalSerializer
    search_fields = ("nome",)
    ordering_fields = ("nome", "valor_mensalidade")


class PagamentoAlunoViewSet(viewsets.ModelViewSet):
    queryset = PagamentoAluno.objects.select_related("aluno", "aluno__turma").all()
    serializer_class = PagamentoAlunoSerializer
    search_fields = ("aluno__nome_completo", "aluno__cpf")
    ordering_fields = ("competencia", "data_vencimento", "valor")


class PagamentoProfessorViewSet(viewsets.ModelViewSet):
    queryset = PagamentoProfessor.objects.select_related("professor").all()
    serializer_class = PagamentoProfessorSerializer
    search_fields = ("professor__nome_completo", "professor__cpf")
    ordering_fields = ("competencia", "valor_bruto")


class DespesaViewSet(viewsets.ModelViewSet):
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer
    search_fields = ("descricao", "categoria")
    ordering_fields = ("data", "valor")


class TemplateContratoViewSet(viewsets.ModelViewSet):
    queryset = TemplateContrato.objects.all()
    serializer_class = TemplateContratoSerializer
    search_fields = ("nome", "versao")
    ordering_fields = ("nome", "updated_at")


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related(
        "escola",
        "aluno",
        "responsavel",
        "turma",
        "plano",
        "template",
        "gerado_por",
    ).all()
    serializer_class = ContratoSerializer
    search_fields = ("numero", "aluno__nome_completo", "responsavel__nome_completo")
    ordering_fields = ("data_emissao", "numero")

    def update(self, request, *args, **kwargs):
        contrato = self.get_object()
        if contrato.status != Contrato.Status.RASCUNHO:
            return Response(
                {"detail": "Contrato emitido ou cancelado nao pode ser alterado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def gerar_pdf(self, request, pk=None):
        contrato = self.get_object()
        try:
            gerar_pdf_contrato(contrato, request.user)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(contrato)
        return Response(serializer.data)


class AssinaturaViewSet(viewsets.ModelViewSet):
    queryset = Assinatura.objects.select_related("contrato").all()
    serializer_class = AssinaturaSerializer
    search_fields = ("contrato__numero", "nome", "cpf")
    ordering_fields = ("data_assinatura", "tipo")


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "groups": list(user.groups.values_list("name", flat=True)),
        }
        return Response(data)
