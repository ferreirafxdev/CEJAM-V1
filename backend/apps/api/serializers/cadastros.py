from rest_framework import serializers

from apps.cadastros.models import Escola, Responsavel


class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = "__all__"


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = "__all__"
