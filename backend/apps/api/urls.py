from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AlunoViewSet,
    AssinaturaViewSet,
    ContratoViewSet,
    DespesaViewSet,
    EscolaViewSet,
    GroupViewSet,
    MeView,
    PagamentoAlunoViewSet,
    PagamentoProfessorViewSet,
    PermissionViewSet,
    PlanoEducacionalViewSet,
    ProfessorViewSet,
    ResponsavelViewSet,
    TemplateContratoViewSet,
    TurmaViewSet,
    UserViewSet,
)


router = DefaultRouter()
router.register(r"permissoes", PermissionViewSet, basename="permissoes")
router.register(r"grupos", GroupViewSet, basename="grupos")
router.register(r"usuarios", UserViewSet, basename="usuarios")
router.register(r"escolas", EscolaViewSet, basename="escolas")
router.register(r"responsaveis", ResponsavelViewSet, basename="responsaveis")
router.register(r"alunos", AlunoViewSet, basename="alunos")
router.register(r"professores", ProfessorViewSet, basename="professores")
router.register(r"turmas", TurmaViewSet, basename="turmas")
router.register(r"planos", PlanoEducacionalViewSet, basename="planos")
router.register(r"pagamentos-alunos", PagamentoAlunoViewSet, basename="pagamentos-alunos")
router.register(r"pagamentos-professores", PagamentoProfessorViewSet, basename="pagamentos-professores")
router.register(r"despesas", DespesaViewSet, basename="despesas")
router.register(r"templates-contrato", TemplateContratoViewSet, basename="templates-contrato")
router.register(r"contratos", ContratoViewSet, basename="contratos")
router.register(r"assinaturas", AssinaturaViewSet, basename="assinaturas")

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="auth_me"),
    path("", include(router.urls)),
]
