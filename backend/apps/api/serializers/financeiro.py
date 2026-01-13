from rest_framework import serializers

from apps.financeiro.models import (
    Despesa,
    PagamentoAluno,
    PagamentoAlunoHistorico,
    PagamentoProfessor,
    PlanoEducacional,
)


class PlanoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoEducacional
        fields = "__all__"


class PagamentoAlunoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source="aluno.nome_completo", read_only=True)
    turma_nome = serializers.CharField(source="aluno.turma.nome", read_only=True)
    plano_nome = serializers.SerializerMethodField()
    nf_pdf_url = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()

    class Meta:
        model = PagamentoAluno
        fields = "__all__"
        read_only_fields = (
            "desconto",
            "multa",
            "juros",
            "dias_atraso",
            "valor_total",
            "nf_numero",
            "nf_pdf",
            "nf_emitida_em",
            "pagamento_registrado_em",
        )

    def get_nf_pdf_url(self, obj):
        request = self.context.get("request")
        if obj.nf_pdf and request:
            return request.build_absolute_uri(obj.nf_pdf.url)
        if obj.nf_pdf:
            return obj.nf_pdf.url
        return ""

    def get_plano_nome(self, obj):
        if obj.plano:
            return obj.plano.nome
        aluno_plano = getattr(obj.aluno, "plano_financeiro", None)
        if aluno_plano:
            return aluno_plano.nome
        return ""

    def get_valor_total(self, obj):
        return str(obj.valor_total)


class PagamentoAlunoHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagamentoAlunoHistorico
        fields = "__all__"


class PagamentoProfessorSerializer(serializers.ModelSerializer):
    professor_nome = serializers.CharField(source="professor.nome_completo", read_only=True)

    class Meta:
        model = PagamentoProfessor
        fields = "__all__"


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = "__all__"
