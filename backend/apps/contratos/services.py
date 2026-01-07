import hashlib
import os
import shutil
from types import SimpleNamespace

from django.conf import settings
from django.core.files.base import ContentFile
from django.template import Context, Template, loader
from django.utils import timezone
from django.utils.safestring import mark_safe

from .defaults import DEFAULT_TEMPLATE_CSS
from .models import Contrato


MESES_PT = [
    "janeiro",
    "fevereiro",
    "marco",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]


def _resolve_wkhtmltopdf_path():
    explicit = os.environ.get("WKHTMLTOPDF_PATH")
    if explicit and os.path.isfile(explicit):
        return explicit
    candidates = [
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
        r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return shutil.which("wkhtmltopdf")


def _render_pdf_with_weasyprint(html, base_url=None):
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise RuntimeError(
            "weasyprint nao instalado. Instale com: pip install weasyprint"
        ) from exc
    return HTML(string=html, base_url=base_url).write_pdf()


def _render_pdf_with_wkhtmltopdf(html):
    try:
        import pdfkit
    except ImportError as exc:
        raise RuntimeError("pdfkit nao instalado. Instale com: pip install pdfkit") from exc
    wkhtmltopdf = _resolve_wkhtmltopdf_path()
    if not wkhtmltopdf:
        raise RuntimeError(
            "wkhtmltopdf nao encontrado. Instale o aplicativo ou defina WKHTMLTOPDF_PATH."
        )
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
    options = {
        "page-size": "A4",
        "encoding": "UTF-8",
        "enable-local-file-access": "",
        "quiet": "",
    }
    return pdfkit.from_string(html, False, options=options, configuration=config)


def _render_pdf(html, base_url=None):
    engine = os.getenv("PDF_ENGINE", "weasyprint").strip().lower()
    if engine == "weasyprint":
        return _render_pdf_with_weasyprint(html, base_url=base_url)
    if engine in {"wkhtmltopdf", "pdfkit"}:
        return _render_pdf_with_wkhtmltopdf(html)
    if engine == "auto":
        try:
            return _render_pdf_with_weasyprint(html, base_url=base_url)
        except Exception:
            return _render_pdf_with_wkhtmltopdf(html)
    raise RuntimeError("PDF_ENGINE invalido. Use weasyprint, wkhtmltopdf ou auto.")


def _format_currency(value):
    if value is None:
        return "0,00"
    valor = f"{value:,.2f}"
    return valor.replace(",", "X").replace(".", ",").replace("X", ".")


def _format_percent(value):
    if value is None:
        return "0,00"
    valor = f"{value:,.2f}"
    return valor.replace(",", "X").replace(".", ",").replace("X", ".")


def _data_extenso(data):
    if not data:
        return ""
    mes = MESES_PT[data.month - 1]
    return f"{data.day} de {mes} de {data.year}"


def _fallback_responsavel(contrato):
    aluno = contrato.aluno
    return SimpleNamespace(
        nome_completo=aluno.nome_responsavel or "",
        cpf="",
        rg="",
        endereco=aluno.endereco or "",
        telefone=aluno.telefone_responsavel or "",
        email=aluno.email_responsavel or "",
    )


def build_contract_context(contrato):
    responsavel = contrato.responsavel or _fallback_responsavel(contrato)
    plano = contrato.plano
    data_emissao = contrato.data_emissao or timezone.localdate()
    return {
        "contrato": contrato,
        "escola": contrato.escola,
        "aluno": contrato.aluno,
        "responsavel": responsavel,
        "turma": contrato.turma,
        "plano": plano,
        "data_emissao_extenso": _data_extenso(data_emissao),
        "plano_valor_mensalidade": _format_currency(plano.valor_mensalidade),
        "plano_taxa_matricula": _format_currency(plano.taxa_matricula),
        "plano_multa_percent": _format_percent(plano.multa_percent),
        "plano_juros_percent": _format_percent(plano.juros_percent),
    }


def build_snapshot(contrato, responsavel):
    return {
        "contrato": {
            "numero": contrato.numero,
            "data_emissao": contrato.data_emissao.isoformat() if contrato.data_emissao else None,
            "cidade_assinatura": contrato.cidade_assinatura,
            "status": contrato.status,
        },
        "template": {
            "id": contrato.template_id,
            "nome": contrato.template.nome,
            "versao": contrato.template.versao,
        },
        "escola": {
            "id": contrato.escola_id,
            "razao_social": contrato.escola.razao_social,
            "nome_fantasia": contrato.escola.nome_fantasia,
            "cnpj": contrato.escola.cnpj,
            "endereco_completo": contrato.escola.endereco_completo,
            "cidade": contrato.escola.cidade,
            "uf": contrato.escola.uf,
            "telefone": contrato.escola.telefone,
            "email": contrato.escola.email,
            "responsavel": contrato.escola.responsavel,
        },
        "responsavel": {
            "id": getattr(responsavel, "id", None),
            "nome_completo": responsavel.nome_completo,
            "cpf": responsavel.cpf,
            "rg": responsavel.rg,
            "endereco": responsavel.endereco,
            "telefone": responsavel.telefone,
            "email": responsavel.email,
        },
        "aluno": {
            "id": contrato.aluno_id,
            "nome_completo": contrato.aluno.nome_completo,
            "cpf": contrato.aluno.cpf,
            "data_nascimento": contrato.aluno.data_nascimento.isoformat(),
            "endereco": contrato.aluno.endereco,
            "numero_matricula": contrato.aluno.numero_matricula,
            "status": contrato.aluno.status,
        },
        "turma": {
            "id": contrato.turma_id,
            "nome": contrato.turma.nome,
            "serie_ano": contrato.turma.serie_ano,
            "turno": contrato.turma.turno,
            "valor_mensalidade": str(contrato.turma.valor_mensalidade),
        },
        "plano": {
            "id": contrato.plano_id,
            "nome": contrato.plano.nome,
            "valor_mensalidade": str(contrato.plano.valor_mensalidade),
            "dia_vencimento": contrato.plano.dia_vencimento,
            "duracao_meses": contrato.plano.duracao_meses,
            "taxa_matricula": str(contrato.plano.taxa_matricula),
            "multa_percent": str(contrato.plano.multa_percent),
            "juros_percent": str(contrato.plano.juros_percent),
        },
    }


def gerar_pdf_contrato(contrato, user=None):
    if contrato.status != Contrato.Status.RASCUNHO:
        raise ValueError("Contrato ja emitido ou cancelado.")

    if not contrato.numero:
        contrato.save()

    context = build_contract_context(contrato)
    responsavel = context["responsavel"]

    corpo = Template(contrato.template.corpo_html).render(Context(context))
    css_text = contrato.template.css or DEFAULT_TEMPLATE_CSS
    css_text = Template(css_text).render(Context(context))

    html = loader.render_to_string(
        "contratos/pdf_base.html",
        {"content": mark_safe(corpo), "css": css_text, "contrato": contrato},
    )

    pdf_bytes = _render_pdf(html, base_url=str(settings.BASE_DIR))
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

    filename = f"{contrato.numero}.pdf"
    contrato.pdf_gerado.save(filename, ContentFile(pdf_bytes), save=False)
    contrato.pdf_hash = pdf_hash
    contrato.snapshot = build_snapshot(contrato, responsavel)
    contrato.gerado_em = timezone.now()
    contrato.gerado_por = user if user and user.is_authenticated else None
    contrato.status = Contrato.Status.EMITIDO
    contrato.save(
        update_fields=[
            "pdf_gerado",
            "pdf_hash",
            "snapshot",
            "gerado_em",
            "gerado_por",
            "status",
            "updated_at",
        ]
    )
