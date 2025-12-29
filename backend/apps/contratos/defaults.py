DEFAULT_TEMPLATE_HTML = """
<h1>Contrato de Prestacao de Servicos Educacionais</h1>
<p><strong>Contrato:</strong> {{ contrato.numero }}</p>

<div class="quadro-resumo">
  <h2>Quadro Resumo</h2>
  <table>
    <tbody>
      <tr>
        <th>Escola</th>
        <td>{{ escola.nome_fantasia }} ({{ escola.razao_social }})</td>
      </tr>
      <tr>
        <th>CNPJ</th>
        <td>{{ escola.cnpj }}</td>
      </tr>
      <tr>
        <th>Aluno</th>
        <td>{{ aluno.nome_completo }}{% if aluno.numero_matricula %} - Matricula {{ aluno.numero_matricula }}{% endif %}</td>
      </tr>
      <tr>
        <th>Responsavel</th>
        <td>{{ responsavel.nome_completo }} - CPF {{ responsavel.cpf }}</td>
      </tr>
      <tr>
        <th>Turma</th>
        <td>{{ turma.nome }} - {{ turma.serie_ano }} - {{ turma.get_turno_display }}</td>
      </tr>
      <tr>
        <th>Plano</th>
        <td>{{ plano.nome }} - R$ {{ plano_valor_mensalidade }}</td>
      </tr>
      <tr>
        <th>Emissao</th>
        <td>{{ contrato.data_emissao|date:"d/m/Y" }}</td>
      </tr>
    </tbody>
  </table>
</div>

<p>
Pelo presente instrumento particular, de um lado <strong>{{ escola.razao_social }}</strong>,
inscrita no CNPJ sob o numero <strong>{{ escola.cnpj }}</strong>, com sede em
{{ escola.endereco_completo }}, {{ escola.cidade }} - {{ escola.uf }}, doravante denominada
<strong>CONTRATADA</strong>, e de outro lado <strong>{{ responsavel.nome_completo }}</strong>,
CPF {{ responsavel.cpf }}, residente e domiciliado em {{ responsavel.endereco }},
doravante denominado <strong>CONTRATANTE</strong>, neste ato representando o aluno
<strong>{{ aluno.nome_completo }}</strong>, resolvem firmar o presente contrato de prestacao de
servicos educacionais, que se regera pelas clausulas e condicoes seguintes.
</p>

<h2>Clausula Primeira - Do Objeto</h2>
<p>
O presente contrato tem por objeto a prestacao de servicos educacionais pela CONTRATADA ao aluno
identificado, referente ao ano letivo e atividades curriculares da turma {{ turma.nome }},
{{ turma.serie_ano }}, turno {{ turma.get_turno_display }}.
</p>

<h2>Clausula Segunda - Da Matricula e Vigencia</h2>
<p>
A matricula do aluno e formalizada pela assinatura deste contrato e pelo pagamento da taxa de matricula,
quando aplicavel. O presente contrato tera vigencia de {{ plano.duracao_meses }} meses, iniciando-se
na data de emissao e se encerrando ao final do periodo contratado, salvo rescisao antecipada.
</p>

<h2>Clausula Terceira - Dos Valores e Condicoes de Pagamento</h2>
<p>
Pelos servicos prestados, o CONTRATANTE pagara a mensalidade de R$ {{ plano_valor_mensalidade }},
com vencimento todo dia {{ plano.dia_vencimento }}. A taxa de matricula, quando existente, e de
R$ {{ plano_taxa_matricula }}.
</p>
<p>
Em caso de atraso, incidira multa de {{ plano_multa_percent }}% e juros de {{ plano_juros_percent }}%
ao mes, calculados pro rata die, alem de correcao monetaria nos termos da legislacao vigente.
</p>

<h2>Clausula Quarta - Das Obrigacoes da Contratada</h2>
<p>
A CONTRATADA compromete-se a prestar os servicos educacionais com observancia das normas legais e
pedagogicas, garantindo corpo docente habilitado, carga horaria adequada e acompanhamento escolar.
</p>

<h2>Clausula Quinta - Das Obrigacoes do Contratante</h2>
<p>
O CONTRATANTE compromete-se a efetuar os pagamentos nos prazos estipulados, acompanhar o desempenho
do aluno, zelar pela disciplina e cumprir as normas internas da instituicao.
</p>

<h2>Clausula Sexta - Da Rescisao</h2>
<p>
O presente contrato podera ser rescindido por qualquer das partes mediante comunicacao por escrito,
respeitando-se os valores proporcionais aos servicos efetivamente prestados, bem como eventuais encargos.
</p>

<h2>Clausula Setima - Da Confidencialidade e Protecao de Dados</h2>
<p>
As partes se comprometem a manter sigilo sobre informacoes pessoais e academicas, observando a
Lei Geral de Protecao de Dados (LGPD - Lei 13.709/2018), utilizando-as exclusivamente para fins
educacionais e administrativos.
</p>

<h2>Clausula Oitava - Disposicoes Gerais</h2>
<p>
Este contrato constitui o acordo integral entre as partes, substituindo entendimentos anteriores.
Qualquer alteracao devera ser feita por escrito e assinada por ambas as partes.
</p>

<h2>Clausula Nona - Do Foro</h2>
<p>
Fica eleito o foro da comarca de {{ contrato.cidade_assinatura }} para dirimir quaisquer duvidas
oriundas do presente instrumento, renunciando as partes a qualquer outro, por mais privilegiado que seja.
</p>

<p class="assinatura-local">
{{ contrato.cidade_assinatura }}, {{ data_emissao_extenso }}.
</p>

<div class="assinaturas">
  <div class="linha-assinatura">
    <span>______________________________________________</span>
    <strong>{{ responsavel.nome_completo }}</strong>
    <span>CONTRATANTE</span>
  </div>
  <div class="linha-assinatura">
    <span>______________________________________________</span>
    <strong>{{ escola.responsavel }}</strong>
    <span>CONTRATADA - {{ escola.nome_fantasia }}</span>
  </div>
  <div class="linha-assinatura">
    <span>______________________________________________</span>
    <strong>Testemunha 1</strong>
    <span>CPF:</span>
  </div>
  <div class="linha-assinatura">
    <span>______________________________________________</span>
    <strong>Testemunha 2</strong>
    <span>CPF:</span>
  </div>
</div>
"""


DEFAULT_TEMPLATE_CSS = """
@page {
  size: A4;
  margin: 3cm 2cm 2cm 3cm;
  @top-center {
    content: "Contrato {{ contrato.numero }}";
    font-size: 10pt;
  }
  @bottom-center {
    content: "Contrato {{ contrato.numero }}";
    font-size: 10pt;
  }
  @bottom-right {
    content: "Pagina " counter(page) " de " counter(pages);
    font-size: 10pt;
  }
}

* {
  box-sizing: border-box;
}

body {
  font-family: "Times New Roman", "Liberation Serif", "Nimbus Roman", serif;
  font-size: 12pt;
  line-height: 1.5;
  text-align: justify;
  color: #111;
}

h1 {
  text-align: center;
  font-size: 14pt;
  text-transform: uppercase;
  margin: 0 0 16pt 0;
}

h2 {
  font-size: 12pt;
  text-transform: uppercase;
  margin: 18pt 0 6pt 0;
}

p {
  text-indent: 1.25cm;
  margin: 0 0 10pt 0;
}

.quadro-resumo {
  border: 1px solid #222;
  padding: 10pt;
  margin-bottom: 16pt;
}

.quadro-resumo h2 {
  margin-top: 0;
  text-align: center;
  font-size: 12pt;
}

.quadro-resumo table {
  width: 100%;
  border-collapse: collapse;
}

.quadro-resumo th,
.quadro-resumo td {
  text-align: left;
  padding: 4pt 0;
  vertical-align: top;
}

.assinatura-local {
  text-indent: 0;
  text-align: right;
  margin-top: 18pt;
}

.assinaturas {
  margin-top: 28pt;
}

.linha-assinatura {
  margin-bottom: 22pt;
  text-align: center;
}

.linha-assinatura span {
  display: block;
  text-indent: 0;
}

.linha-assinatura strong {
  display: block;
  margin-top: 6pt;
  font-weight: bold;
}
"""
