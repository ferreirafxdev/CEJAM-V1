from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AlunoViewSet,
    AssinaturaViewSet,
    ContratoViewSet,
    DespesaViewSet,
    EscolaViewSet,
    FinanceiroDashboardView,
    FinanceiroRelatoriosView,
    GroupViewSet,
    DashboardView,
    MeView,
    PagamentoAlunoViewSet,
    PagamentoAlunoHistoricoViewSet,
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
router.register(
    r"pagamentos-alunos-historico",
    PagamentoAlunoHistoricoViewSet,
    basename="pagamentos-alunos-historico",
)
router.register(r"pagamentos-professores", PagamentoProfessorViewSet, basename="pagamentos-professores")
router.register(r"despesas", DespesaViewSet, basename="despesas")
router.register(r"templates-contrato", TemplateContratoViewSet, basename="templates-contrato")
router.register(r"contratos", ContratoViewSet, basename="contratos")
router.register(r"assinaturas", AssinaturaViewSet, basename="assinaturas")

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="auth_me"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("financeiro/dashboard/", FinanceiroDashboardView.as_view(), name="financeiro_dashboard"),
    path("financeiro/relatorios/", FinanceiroRelatoriosView.as_view(), name="financeiro_relatorios"),
    path("", include(router.urls)),
]
