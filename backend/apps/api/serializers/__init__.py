from .academico import AlunoSerializer, ProfessorSerializer, TurmaSerializer
from .auth import GroupSerializer, PermissionSerializer, UserSerializer
from .cadastros import EscolaSerializer, ResponsavelSerializer
from .contratos import AssinaturaSerializer, ContratoSerializer, TemplateContratoSerializer
from .financeiro import (
    DespesaSerializer,
    PagamentoAlunoHistoricoSerializer,
    PagamentoAlunoSerializer,
    PagamentoProfessorSerializer,
    PlanoEducacionalSerializer,
)

__all__ = [
    "AlunoSerializer",
    "ProfessorSerializer",
    "TurmaSerializer",
    "GroupSerializer",
    "PermissionSerializer",
    "UserSerializer",
    "EscolaSerializer",
    "ResponsavelSerializer",
    "AssinaturaSerializer",
    "ContratoSerializer",
    "TemplateContratoSerializer",
    "DespesaSerializer",
    "PagamentoAlunoHistoricoSerializer",
    "PagamentoAlunoSerializer",
    "PagamentoProfessorSerializer",
    "PlanoEducacionalSerializer",
]
