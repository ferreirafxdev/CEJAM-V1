from decimal import Decimal

from django.core.files.base import ContentFile
from django.db import models, transaction
from django.utils import timezone


def nota_fiscal_pdf_path(instance, filename):
    numero = instance.nf_numero or f"pagamento-{instance.id or 'novo'}"
    return f"notas-fiscais/{numero}/{filename}"


class PlanoEducacional(models.Model):
    class ModeloPagamento(models.TextChoices):
        MENSAL = "MENSAL", "Mensal"
        TRIMESTRAL = "TRIMESTRAL", "Trimestral"
        SEMESTRAL = "SEMESTRAL", "Semestral"
        ANUAL = "ANUAL", "Anual"

    class BolsaTipo(models.TextChoices):
        NENHUMA = "NENHUMA", "Nenhuma"
        PARCIAL = "PARCIAL", "Parcial"
        INTEGRAL = "INTEGRAL", "Integral"
        CONVENIO = "CONVENIO", "Convenio"

    class FormaPagamentoPadrao(models.TextChoices):
        DINHEIRO = "DINHEIRO", "Dinheiro"
        PIX = "PIX", "Pix"
        BOLETO = "BOLETO", "Boleto"
        CARTAO = "CARTAO", "Cartao"

    nome = models.CharField(max_length=120)
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2)
    modelo_pagamento = models.CharField(
        max_length=12,
        choices=ModeloPagamento.choices,
        default=ModeloPagamento.MENSAL,
    )
    desconto_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    bolsa_tipo = models.CharField(
        max_length=12,
        choices=BolsaTipo.choices,
        default=BolsaTipo.NENHUMA,
    )
    bolsa_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    dia_vencimento = models.PositiveSmallIntegerField()
    duracao_meses = models.PositiveSmallIntegerField()
    taxa_matricula = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    multa_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    juros_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    juros_diario_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    forma_pagamento_padrao = models.CharField(
        max_length=10,
        choices=FormaPagamentoPadrao.choices,
        null=True,
        blank=True,
    )
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def calcular_valor_liquido(self, valor_base=None):
        base = Decimal(valor_base) if valor_base is not None else self.valor_mensalidade
        desconto = (base * self.desconto_percent) / Decimal("100")
        bolsa = Decimal("0.00")
        if self.bolsa_tipo == self.BolsaTipo.INTEGRAL:
            bolsa = base
        elif self.bolsa_tipo in {self.BolsaTipo.PARCIAL, self.BolsaTipo.CONVENIO}:
            bolsa = (base * self.bolsa_percent) / Decimal("100")
        valor = base - desconto - bolsa
        return valor if valor > 0 else Decimal("0.00")


class PagamentoAluno(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = "DINHEIRO", "Dinheiro"
        PIX = "PIX", "Pix"
        BOLETO = "BOLETO", "Boleto"
        CARTAO = "CARTAO", "Cartao"

    class Status(models.TextChoices):
        PAGO = "PAGO", "Pago"
        EM_ABERTO = "EM_ABERTO", "Em aberto"
        ATRASADO = "ATRASADO", "Atrasado"
        ISENTO = "ISENTO", "Isento"

    aluno = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.PROTECT,
        related_name="pagamentos",
    )
    plano = models.ForeignKey(
        "financeiro.PlanoEducacional",
        on_delete=models.SET_NULL,
        related_name="pagamentos_alunos",
        null=True,
        blank=True,
    )
    competencia = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    desconto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=10, choices=FormaPagamento.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.EM_ABERTO)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    juros = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    dias_atraso = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True)
    pagamento_registrado_em = models.DateTimeField(null=True, blank=True)
    nf_numero = models.CharField(max_length=30, unique=True, blank=True, null=True)
    nf_pdf = models.FileField(upload_to=nota_fiscal_pdf_path, blank=True, null=True)
    nf_emitida_em = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-competencia", "aluno__nome_completo"]

    def __str__(self):
        return f"{self.aluno} - {self.competencia:%m/%Y}"

    @property
    def valor_total(self):
        base = (self.valor or Decimal("0.00")) - (self.desconto or Decimal("0.00"))
        total = base + (self.multa or Decimal("0.00")) + (self.juros or Decimal("0.00"))
        return total if total > 0 else Decimal("0.00")

    def aplicar_regras(self, referencia=None):
        referencia = referencia or self.data_pagamento or timezone.localdate()
        plano = self.plano or getattr(self.aluno, "plano_financeiro", None)
        if plano and not self.plano:
            self.plano = plano

        valor = self.valor or Decimal("0.00")
        self.desconto = Decimal("0.00")
        if plano:
            valor_liquido = plano.calcular_valor_liquido(valor)
            self.desconto = max(valor - valor_liquido, Decimal("0.00"))

        if self.status == self.Status.ISENTO:
            self.desconto = valor
            self.multa = Decimal("0.00")
            self.juros = Decimal("0.00")
            self.dias_atraso = 0
            self.valor_pago = Decimal("0.00")
            return

        self.multa = Decimal("0.00")
        self.juros = Decimal("0.00")
        dias_atraso = 0
        if self.data_vencimento and referencia:
            dias_atraso = max((referencia - self.data_vencimento).days, 0)
        self.dias_atraso = dias_atraso
        if plano and dias_atraso > 0:
            base = valor - (self.desconto or Decimal("0.00"))
            base = base if base > 0 else Decimal("0.00")
            self.multa = (base * plano.multa_percent) / Decimal("100")
            juros_fixo = (base * plano.juros_percent) / Decimal("100")
            juros_diario = ((base * plano.juros_diario_percent) / Decimal("100")) * Decimal(
                dias_atraso
            )
            self.juros = juros_fixo + juros_diario

        if self.status != self.Status.PAGO:
            if dias_atraso > 0:
                self.status = self.Status.ATRASADO
            else:
                self.status = self.Status.EM_ABERTO

        if self.status == self.Status.PAGO:
            if not self.data_pagamento:
                self.data_pagamento = timezone.localdate()
            if self.valor_pago is None:
                self.valor_pago = self.valor_total

    def _gerar_nf_numero(self):
        ano = (self.data_pagamento or timezone.localdate()).year
        prefix = f"NF-{ano}-"
        ultimo = (
            PagamentoAluno.objects.select_for_update()
            .filter(nf_numero__startswith=prefix)
            .order_by("-nf_numero")
            .first()
        )
        ultimo_seq = 0
        if ultimo and ultimo.nf_numero:
            try:
                ultimo_seq = int(ultimo.nf_numero.split("-")[-1])
            except (ValueError, IndexError):
                ultimo_seq = 0
        return f"{prefix}{ultimo_seq + 1:06d}"

    def emitir_nf(self, user=None):
        if self.status != self.Status.PAGO:
            return
        if not self.id:
            self.save()

        from .services import gerar_pdf_nota_fiscal

        with transaction.atomic():
            if not self.pagamento_registrado_em:
                self.pagamento_registrado_em = timezone.now()
            if self.nf_pdf:
                self.save(update_fields=["pagamento_registrado_em", "updated_at"])
                return
            if not self.nf_numero:
                self.nf_numero = self._gerar_nf_numero()

            pdf_bytes = gerar_pdf_nota_fiscal(self)
            filename = f"{self.nf_numero}.pdf"
            self.nf_pdf.save(filename, ContentFile(pdf_bytes), save=False)
            self.nf_emitida_em = timezone.now()

            self.save(
                update_fields=[
                    "nf_numero",
                    "nf_pdf",
                    "nf_emitida_em",
                    "pagamento_registrado_em",
                    "updated_at",
                ]
            )


class PagamentoAlunoHistorico(models.Model):
    class Acao(models.TextChoices):
        CRIADO = "CRIADO", "Criado"
        ATUALIZADO = "ATUALIZADO", "Atualizado"
        STATUS = "STATUS", "Status"
        NF = "NF", "Nota fiscal"

    pagamento = models.ForeignKey(
        PagamentoAluno,
        on_delete=models.CASCADE,
        related_name="historico",
    )
    acao = models.CharField(max_length=12, choices=Acao.choices)
    status_anterior = models.CharField(max_length=10, blank=True, null=True)
    status_novo = models.CharField(max_length=10, blank=True, null=True)
    valor_devido = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    alterado_por = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pagamentos_alunos_historico",
    )
    detalhes = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pagamento_id} - {self.acao}"


class PagamentoProfessor(models.Model):
    class Status(models.TextChoices):
        PAGO = "PAGO", "Pago"
        PENDENTE = "PENDENTE", "Pendente"

    professor = models.ForeignKey(
        "professores.Professor",
        on_delete=models.PROTECT,
        related_name="pagamentos",
    )
    competencia = models.DateField()
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    descontos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-competencia", "professor__nome_completo"]

    def save(self, *args, **kwargs):
        if self.valor_liquido is None:
            # Auto-calc net value when not provided.
            self.valor_liquido = (self.valor_bruto or Decimal("0.00")) - (
                self.descontos or Decimal("0.00")
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.professor} - {self.competencia:%m/%Y}"


class Despesa(models.Model):
    class Categoria(models.TextChoices):
        AGUA = "AGUA", "Agua"
        LUZ = "LUZ", "Luz"
        ALUGUEL = "ALUGUEL", "Aluguel"
        INTERNET = "INTERNET", "Internet"
        MATERIAL = "MATERIAL", "Material"
        OUTROS = "OUTROS", "Outros"

    class Tipo(models.TextChoices):
        FIXA = "FIXA", "Fixa"
        VARIAVEL = "VARIAVEL", "Variavel"

    descricao = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data", "descricao"]

    def __str__(self):
        return self.descricao
