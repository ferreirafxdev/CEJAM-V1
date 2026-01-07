# Modulo Financeiro Escolar - referencia tecnica

## Modelagem (resumo)

- alunos_aluno
  - nome_completo, numero_matricula, turma_id, status
  - plano_financeiro_id (FK -> financeiro_planoeducacional)

- financeiro_planoeducacional
  - modelo_pagamento (MENSAL/TRIMESTRAL/SEMESTRAL/ANUAL)
  - valor_mensalidade, desconto_percent, bolsa_tipo, bolsa_percent
  - multa_percent, juros_percent, juros_diario_percent
  - forma_pagamento_padrao, ativo

- financeiro_pagamentoaluno
  - aluno_id (FK), plano_id (FK opcional)
  - competencia, data_vencimento, data_pagamento
  - valor, desconto, multa, juros, valor_pago, dias_atraso
  - status (PAGO/EM_ABERTO/ATRASADO/ISENTO)
  - pagamento_registrado_em, nf_numero, nf_pdf, nf_emitida_em

- financeiro_pagamentoalunohistorico
  - pagamento_id (FK), acao, status_anterior, status_novo
  - valor_devido, valor_pago, alterado_por, detalhes, created_at

## Endpoints REST principais

- GET /api/planos/
- GET /api/alunos/
- GET /api/pagamentos-alunos/
- POST /api/pagamentos-alunos/
- PATCH /api/pagamentos-alunos/{id}/
- POST /api/pagamentos-alunos/recalcular/
- GET /api/pagamentos-alunos-historico/?pagamento={id}
- GET /api/financeiro/dashboard/
- GET /api/financeiro/relatorios/

## Regras de negocio (core)

- Plano calcula desconto/bolsa e define multas/juros de atraso.
- Pagamento aluno recalcula:
  - desconto, multa, juros, dias_atraso
  - status automatico (EM_ABERTO/ATRASADO) quando nao PAGO
- Status PAGO gera NF em PDF e registra pagamento_registrado_em.
- Historico registra criacao, atualizacao, mudanca de status e NF.

## Consultas SQL analiticas (PostgreSQL)

-- Inadimplentes ha mais de 30 dias
SELECT
  a.id,
  a.nome_completo,
  t.nome AS turma,
  MAX(p.data_vencimento) AS ultimo_vencimento,
  SUM(p.valor - p.desconto + p.multa + p.juros) AS valor_devido
FROM financeiro_pagamentoaluno p
JOIN alunos_aluno a ON p.aluno_id = a.id
LEFT JOIN turmas_turma t ON a.turma_id = t.id
WHERE p.status IN ('EM_ABERTO', 'ATRASADO')
  AND p.data_vencimento < CURRENT_DATE - INTERVAL '30 days'
GROUP BY a.id, a.nome_completo, t.nome
ORDER BY valor_devido DESC;

-- Receita por turma (pagamentos pagos)
SELECT
  t.nome AS turma,
  SUM(COALESCE(p.valor_pago, p.valor - p.desconto + p.multa + p.juros)) AS receita
FROM financeiro_pagamentoaluno p
JOIN alunos_aluno a ON p.aluno_id = a.id
JOIN turmas_turma t ON a.turma_id = t.id
WHERE p.status = 'PAGO'
GROUP BY t.nome
ORDER BY receita DESC;

-- Taxa de inadimplencia por plano
SELECT
  COALESCE(pl.nome, 'Sem plano') AS plano,
  COUNT(*) AS total,
  SUM(CASE WHEN p.status IN ('EM_ABERTO', 'ATRASADO') THEN 1 ELSE 0 END) AS inadimplentes,
  ROUND(
    100.0 * SUM(CASE WHEN p.status IN ('EM_ABERTO', 'ATRASADO') THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
    2
  ) AS taxa_inadimplencia
FROM financeiro_pagamentoaluno p
LEFT JOIN financeiro_planoeducacional pl ON p.plano_id = pl.id
GROUP BY pl.nome
ORDER BY taxa_inadimplencia DESC;

-- Projecao de receita para os proximos meses
SELECT
  DATE_TRUNC('month', p.competencia) AS mes,
  SUM(p.valor - p.desconto + p.multa + p.juros) AS previsto
FROM financeiro_pagamentoaluno p
WHERE p.competencia >= DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
  AND p.status <> 'ISENTO'
GROUP BY mes
ORDER BY mes;

## Estrutura de dashboards

- KPIs
  - receita_mes
  - receita_periodo
  - taxa_inadimplencia
  - alunos_adimplentes vs inadimplentes
  - ticket_medio

- Graficos
  - Linha: receita mensal (competencia)
  - Barras: pagamentos por turma (quantidade)
  - Pizza: status de pagamento
  - Heatmap: inadimplencia por mes (data_vencimento)
  - Comparativo: previsto vs realizado

## Sugestoes de metricas estrategicas

- Ticket medio por aluno (receita / alunos pagantes)
- Receita por plano e por turma (mix de produtos)
- Taxa de inadimplencia por faixa de atraso
- Evolucao de receita (mensal e trimestral)
- Receita prevista x realizada (gap de previsibilidade)

## Rotina automatica

- Agende: python manage.py atualizar_status_financeiro
- Opcional: POST /api/pagamentos-alunos/recalcular/
