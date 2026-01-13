from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.contratos.models import Assinatura, Contrato, TemplateContrato
from apps.contratos.services import gerar_pdf_contrato

from ..serializers import AssinaturaSerializer, ContratoSerializer, TemplateContratoSerializer


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
