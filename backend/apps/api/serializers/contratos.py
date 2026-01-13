from rest_framework import serializers

from apps.contratos.models import Assinatura, Contrato, TemplateContrato


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
