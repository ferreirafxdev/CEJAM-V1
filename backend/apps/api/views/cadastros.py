from rest_framework import viewsets

from apps.cadastros.models import Escola, Responsavel

from ..serializers import EscolaSerializer, ResponsavelSerializer


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
