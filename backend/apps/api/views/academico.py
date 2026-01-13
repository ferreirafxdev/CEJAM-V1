from rest_framework import viewsets

from apps.alunos.models import Aluno
from apps.professores.models import Professor
from apps.turmas.models import Turma

from ..serializers import AlunoSerializer, ProfessorSerializer, TurmaSerializer


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
