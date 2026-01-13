from .academico import AlunoViewSet, ProfessorViewSet, TurmaViewSet
from .auth import GroupViewSet, MeView, PermissionViewSet, UserViewSet
from .cadastros import EscolaViewSet, ResponsavelViewSet
from .contratos import AssinaturaViewSet, ContratoViewSet, TemplateContratoViewSet
from .dashboard import DashboardView
from .financeiro import (
    DespesaViewSet,
    FinanceiroDashboardView,
    FinanceiroRelatoriosView,
    PagamentoAlunoHistoricoViewSet,
    PagamentoAlunoViewSet,
    PagamentoProfessorViewSet,
    PlanoEducacionalViewSet,
)

__all__ = [
    "AlunoViewSet",
    "ProfessorViewSet",
    "TurmaViewSet",
    "GroupViewSet",
    "MeView",
    "PermissionViewSet",
    "UserViewSet",
    "EscolaViewSet",
    "ResponsavelViewSet",
    "AssinaturaViewSet",
    "ContratoViewSet",
    "TemplateContratoViewSet",
    "DashboardView",
    "DespesaViewSet",
    "FinanceiroDashboardView",
    "FinanceiroRelatoriosView",
    "PagamentoAlunoHistoricoViewSet",
    "PagamentoAlunoViewSet",
    "PagamentoProfessorViewSet",
    "PlanoEducacionalViewSet",
]
