export type Option = {
  value: string | number | boolean;
  label: string;
};

export type FieldType =
  | "text"
  | "email"
  | "number"
  | "date"
  | "textarea"
  | "select"
  | "multiselect"
  | "boolean"
  | "link"
  | "json";

export type FieldConfig = {
  name: string;
  label: string;
  type: FieldType;
  required?: boolean;
  options?: Option[];
  resource?: string;
  readOnly?: boolean;
  monospace?: boolean;
  rows?: number;
};

export type FieldSection = {
  title: string;
  fields: string[];
};

export type ResourceAction = {
  key: string;
  label: string;
  variant?: "primary" | "ghost" | "danger";
  enabledWhen?: (item: Record<string, any>) => boolean;
};

export type ResourceConfig = {
  key: string;
  label: string;
  path: string;
  endpoint: string;
  description: string;
  optionLabel?: string;
  columns: string[];
  fields: FieldConfig[];
  sections?: FieldSection[];
  filters?: string[];
  actions?: ResourceAction[];
  lockWhen?: (item: Record<string, any>) => boolean;
  readOnly?: boolean;
};

const statusAluno: Option[] = [
  { value: "ATIVO", label: "Ativo" },
  { value: "INATIVO", label: "Inativo" },
];

const statusProfessor: Option[] = [
  { value: "ATIVO", label: "Ativo" },
  { value: "INATIVO", label: "Inativo" },
];

const statusTurma: Option[] = [
  { value: "ATIVA", label: "Ativa" },
  { value: "ENCERRADA", label: "Encerrada" },
];

const turnoOptions: Option[] = [
  { value: "MANHA", label: "Manha" },
  { value: "TARDE", label: "Tarde" },
  { value: "NOITE", label: "Noite" },
];

const sexoOptions: Option[] = [
  { value: "M", label: "Masculino" },
  { value: "F", label: "Feminino" },
  { value: "O", label: "Outro" },
];

const formaPagamento: Option[] = [
  { value: "DINHEIRO", label: "Dinheiro" },
  { value: "PIX", label: "Pix" },
  { value: "BOLETO", label: "Boleto" },
];

const statusPagamentoAluno: Option[] = [
  { value: "PAGO", label: "Pago" },
  { value: "PENDENTE", label: "Pendente" },
  { value: "ATRASADO", label: "Atrasado" },
];

const statusPagamentoProfessor: Option[] = [
  { value: "PAGO", label: "Pago" },
  { value: "PENDENTE", label: "Pendente" },
];

const tipoVinculo: Option[] = [
  { value: "CLT", label: "CLT" },
  { value: "HORISTA", label: "Horista" },
  { value: "PJ", label: "PJ" },
];

const categoriaDespesa: Option[] = [
  { value: "AGUA", label: "Agua" },
  { value: "LUZ", label: "Luz" },
  { value: "ALUGUEL", label: "Aluguel" },
  { value: "INTERNET", label: "Internet" },
  { value: "MATERIAL", label: "Material" },
  { value: "OUTROS", label: "Outros" },
];

const tipoDespesa: Option[] = [
  { value: "FIXA", label: "Fixa" },
  { value: "VARIAVEL", label: "Variavel" },
];

const contratoStatus: Option[] = [
  { value: "RASCUNHO", label: "Rascunho" },
  { value: "EMITIDO", label: "Emitido" },
  { value: "CANCELADO", label: "Cancelado" },
];

const assinaturaTipo: Option[] = [
  { value: "RESPONSAVEL", label: "Responsavel" },
  { value: "ESCOLA", label: "Escola" },
  { value: "TESTEMUNHA_1", label: "Testemunha 1" },
  { value: "TESTEMUNHA_2", label: "Testemunha 2" },
];

export const resources: ResourceConfig[] = [
  {
    key: "escolas",
    label: "Escolas",
    path: "/cadastros/escolas",
    endpoint: "/escolas/",
    description: "Dados institucionais e responsaveis legais da escola.",
    optionLabel: "nome_fantasia",
    filters: ["uf"],
    columns: ["nome_fantasia", "cnpj", "cidade", "uf", "telefone"],
    fields: [
      { name: "razao_social", label: "Razao social", type: "text", required: true },
      { name: "nome_fantasia", label: "Nome fantasia", type: "text", required: true },
      { name: "cnpj", label: "CNPJ", type: "text", required: true },
      { name: "endereco_completo", label: "Endereco completo", type: "textarea", required: true },
      { name: "cidade", label: "Cidade", type: "text", required: true },
      { name: "uf", label: "UF", type: "text", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "email", label: "Email", type: "email", required: true },
      { name: "responsavel", label: "Responsavel", type: "text", required: true },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Identificacao", fields: ["razao_social", "nome_fantasia", "cnpj"] },
      { title: "Endereco", fields: ["endereco_completo", "cidade", "uf"] },
      { title: "Contato", fields: ["telefone", "email", "responsavel"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "responsaveis",
    label: "Responsaveis",
    path: "/cadastros/responsaveis",
    endpoint: "/responsaveis/",
    description: "Responsaveis financeiros e legais vinculados aos alunos.",
    optionLabel: "nome_completo",
    columns: ["nome_completo", "cpf", "telefone", "email"],
    fields: [
      { name: "nome_completo", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text", required: true },
      { name: "rg", label: "RG", type: "text" },
      { name: "endereco", label: "Endereco", type: "textarea", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "email", label: "Email", type: "email", required: true },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Identificacao", fields: ["nome_completo", "cpf", "rg"] },
      { title: "Contato", fields: ["endereco", "telefone", "email"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "alunos",
    label: "Alunos",
    path: "/cadastros/alunos",
    endpoint: "/alunos/",
    description: "Cadastro completo de alunos, matriculas e contatos.",
    optionLabel: "nome_completo",
    filters: ["status", "turma", "sexo"],
    columns: ["nome_completo", "cpf", "numero_matricula", "turma_nome", "status"],
    fields: [
      { name: "nome_completo", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text" },
      { name: "data_nascimento", label: "Data de nascimento", type: "date", required: true },
      { name: "sexo", label: "Sexo", type: "select", options: sexoOptions, required: true },
      { name: "endereco", label: "Endereco", type: "textarea", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "responsavel", label: "Responsavel", type: "select", resource: "responsaveis" },
      { name: "nome_responsavel", label: "Responsavel (legado)", type: "text" },
      { name: "telefone_responsavel", label: "Telefone responsavel", type: "text" },
      { name: "email_responsavel", label: "Email responsavel", type: "email" },
      { name: "status", label: "Status", type: "select", options: statusAluno, required: true },
      { name: "data_matricula", label: "Data de matricula", type: "date", required: true },
      { name: "numero_matricula", label: "Numero de matricula", type: "text" },
      { name: "turma", label: "Turma", type: "select", resource: "turmas", required: true },
      { name: "valor_mensalidade", label: "Valor mensalidade", type: "number", required: true },
      { name: "observacoes", label: "Observacoes", type: "textarea" },
      { name: "historico_escolar", label: "Historico escolar", type: "textarea" },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Dados do aluno", fields: ["nome_completo", "cpf", "data_nascimento", "sexo"] },
      { title: "Contato", fields: ["endereco", "telefone"] },
      {
        title: "Responsavel",
        fields: ["responsavel", "nome_responsavel", "telefone_responsavel", "email_responsavel"],
      },
      {
        title: "Matricula",
        fields: ["status", "data_matricula", "numero_matricula", "turma", "valor_mensalidade"],
      },
      { title: "Historico", fields: ["observacoes", "historico_escolar"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "professores",
    label: "Professores",
    path: "/cadastros/professores",
    endpoint: "/professores/",
    description: "Cadastro docente com regime e valores.",
    optionLabel: "nome_completo",
    filters: ["status", "tipo_vinculo"],
    columns: ["nome_completo", "cpf", "especialidade", "tipo_vinculo", "status"],
    fields: [
      { name: "nome_completo", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text", required: true },
      { name: "especialidade", label: "Disciplina", type: "text", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "email", label: "Email", type: "email", required: true },
      { name: "tipo_vinculo", label: "Tipo de vinculo", type: "select", options: tipoVinculo, required: true },
      { name: "valor_hora", label: "Valor hora", type: "number" },
      { name: "salario_fixo", label: "Salario fixo", type: "number" },
      { name: "status", label: "Status", type: "select", options: statusProfessor, required: true },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Dados principais", fields: ["nome_completo", "cpf", "especialidade"] },
      { title: "Contato", fields: ["telefone", "email"] },
      { title: "Vinculo", fields: ["tipo_vinculo", "valor_hora", "salario_fixo", "status"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "turmas",
    label: "Turmas",
    path: "/cadastros/turmas",
    endpoint: "/turmas/",
    description: "Configuracao de turmas, turnos e professores responsaveis.",
    optionLabel: "nome",
    filters: ["status", "turno"],
    columns: ["nome", "serie_ano", "turno", "professor_nome", "status"],
    fields: [
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "serie_ano", label: "Serie/Ano", type: "text", required: true },
      { name: "turno", label: "Turno", type: "select", options: turnoOptions, required: true },
      {
        name: "professor_responsavel",
        label: "Professor responsavel",
        type: "select",
        resource: "professores",
        required: true,
      },
      { name: "valor_mensalidade", label: "Valor mensalidade", type: "number", required: true },
      { name: "capacidade_maxima", label: "Capacidade maxima", type: "number", required: true },
      { name: "status", label: "Status", type: "select", options: statusTurma, required: true },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Identificacao", fields: ["nome", "serie_ano", "turno"] },
      {
        title: "Equipe",
        fields: ["professor_responsavel", "capacidade_maxima", "status"],
      },
      { title: "Financeiro", fields: ["valor_mensalidade"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "planos",
    label: "Planos educacionais",
    path: "/financeiro/planos",
    endpoint: "/planos/",
    description: "Planos e condicoes financeiras de contrato.",
    optionLabel: "nome",
    columns: ["nome", "valor_mensalidade", "dia_vencimento", "duracao_meses"],
    fields: [
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "valor_mensalidade", label: "Valor mensalidade", type: "number", required: true },
      { name: "dia_vencimento", label: "Dia de vencimento", type: "number", required: true },
      { name: "duracao_meses", label: "Duracao em meses", type: "number", required: true },
      { name: "taxa_matricula", label: "Taxa matricula", type: "number" },
      { name: "multa_percent", label: "Multa (%)", type: "number" },
      { name: "juros_percent", label: "Juros (%) ao mes", type: "number" },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      {
        title: "Plano",
        fields: ["nome", "valor_mensalidade", "dia_vencimento", "duracao_meses"],
      },
      { title: "Encargos", fields: ["taxa_matricula", "multa_percent", "juros_percent"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "pagamentos-alunos",
    label: "Pagamentos de alunos",
    path: "/financeiro/pagamentos-alunos",
    endpoint: "/pagamentos-alunos/",
    description: "Controle de mensalidades e pagamentos de alunos.",
    filters: ["status", "forma_pagamento"],
    columns: ["aluno_nome", "competencia", "valor", "data_vencimento", "status"],
    fields: [
      { name: "aluno", label: "Aluno", type: "select", resource: "alunos", required: true },
      { name: "competencia", label: "Competencia", type: "date", required: true },
      { name: "valor", label: "Valor", type: "number", required: true },
      { name: "data_vencimento", label: "Data vencimento", type: "date", required: true },
      { name: "data_pagamento", label: "Data pagamento", type: "date" },
      { name: "forma_pagamento", label: "Forma pagamento", type: "select", options: formaPagamento, required: true },
      { name: "status", label: "Status", type: "select", options: statusPagamentoAluno, required: true },
      { name: "multa", label: "Multa", type: "number" },
      { name: "observacoes", label: "Observacoes", type: "textarea" },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Pagamento", fields: ["aluno", "competencia", "valor", "multa"] },
      {
        title: "Datas",
        fields: ["data_vencimento", "data_pagamento", "forma_pagamento", "status"],
      },
      { title: "Observacoes", fields: ["observacoes"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "pagamentos-professores",
    label: "Pagamentos de professores",
    path: "/financeiro/pagamentos-professores",
    endpoint: "/pagamentos-professores/",
    description: "Pagamentos de professores e valores liquidos.",
    filters: ["status"],
    columns: ["professor_nome", "competencia", "valor_bruto", "valor_liquido", "status"],
    fields: [
      { name: "professor", label: "Professor", type: "select", resource: "professores", required: true },
      { name: "competencia", label: "Competencia", type: "date", required: true },
      { name: "valor_bruto", label: "Valor bruto", type: "number", required: true },
      { name: "descontos", label: "Descontos", type: "number" },
      { name: "valor_liquido", label: "Valor liquido", type: "number", readOnly: true },
      { name: "data_pagamento", label: "Data pagamento", type: "date" },
      { name: "status", label: "Status", type: "select", options: statusPagamentoProfessor, required: true },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      {
        title: "Pagamento",
        fields: ["professor", "competencia", "valor_bruto", "descontos", "valor_liquido"],
      },
      { title: "Status", fields: ["data_pagamento", "status"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "despesas",
    label: "Despesas",
    path: "/financeiro/despesas",
    endpoint: "/despesas/",
    description: "Despesas administrativas e operacionais.",
    filters: ["categoria", "tipo"],
    columns: ["descricao", "categoria", "valor", "data", "tipo"],
    fields: [
      { name: "descricao", label: "Descricao", type: "text", required: true },
      { name: "categoria", label: "Categoria", type: "select", options: categoriaDespesa, required: true },
      { name: "valor", label: "Valor", type: "number", required: true },
      { name: "data", label: "Data", type: "date", required: true },
      { name: "tipo", label: "Tipo", type: "select", options: tipoDespesa, required: true },
      { name: "observacoes", label: "Observacoes", type: "textarea" },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Despesa", fields: ["descricao", "categoria", "valor", "data", "tipo"] },
      { title: "Observacoes", fields: ["observacoes"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "templates-contrato",
    label: "Templates de contrato",
    path: "/contratos/templates",
    endpoint: "/templates-contrato/",
    description: "Modelos juridicos com corpo em HTML e CSS ABNT.",
    optionLabel: "nome",
    filters: ["ativo"],
    columns: ["nome", "versao", "ativo"],
    fields: [
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "versao", label: "Versao", type: "text", required: true },
      { name: "ativo", label: "Ativo", type: "boolean" },
      { name: "corpo_html", label: "Corpo HTML", type: "textarea", required: true, monospace: true, rows: 12 },
      { name: "css", label: "CSS juridico", type: "textarea", monospace: true, rows: 12 },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Template", fields: ["nome", "versao", "ativo"] },
      { title: "Conteudo", fields: ["corpo_html", "css"] },
      { title: "Auditoria", fields: ["created_at", "updated_at"] },
    ],
  },
  {
    key: "contratos",
    label: "Contratos",
    path: "/contratos/contratos",
    endpoint: "/contratos/",
    description: "Geracao, emissao e armazenamento de contratos em PDF.",
    optionLabel: "numero",
    filters: ["status", "escola"],
    columns: ["numero", "aluno_nome", "responsavel_nome", "turma_nome", "status", "data_emissao"],
    lockWhen: (item) => item.status && item.status !== "RASCUNHO",
    actions: [
      {
        key: "gerar_pdf",
        label: "Gerar PDF",
        variant: "primary",
        enabledWhen: (item) => item.status === "RASCUNHO",
      },
    ],
    fields: [
      { name: "numero", label: "Numero", type: "text", readOnly: true },
      { name: "status", label: "Status", type: "select", options: contratoStatus, required: true },
      { name: "data_emissao", label: "Data emissao", type: "date", required: true },
      { name: "cidade_assinatura", label: "Cidade assinatura", type: "text", required: true },
      { name: "escola", label: "Escola", type: "select", resource: "escolas", required: true },
      { name: "aluno", label: "Aluno", type: "select", resource: "alunos", required: true },
      { name: "responsavel", label: "Responsavel", type: "select", resource: "responsaveis", required: true },
      { name: "turma", label: "Turma", type: "select", resource: "turmas", required: true },
      { name: "plano", label: "Plano", type: "select", resource: "planos", required: true },
      { name: "template", label: "Template", type: "select", resource: "templates-contrato", required: true },
      { name: "pdf_url", label: "PDF", type: "link", readOnly: true },
      { name: "pdf_hash", label: "Hash PDF", type: "text", readOnly: true },
      { name: "qr_payload", label: "Payload QR", type: "text", readOnly: true },
      { name: "gerado_em", label: "Gerado em", type: "text", readOnly: true },
      { name: "gerado_por_username", label: "Gerado por", type: "text", readOnly: true },
      { name: "snapshot", label: "Snapshot", type: "json", readOnly: true },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
      { name: "updated_at", label: "Atualizado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Identificacao", fields: ["numero", "status", "data_emissao", "cidade_assinatura"] },
      {
        title: "Relacionamentos",
        fields: ["escola", "aluno", "responsavel", "turma", "plano", "template"],
      },
      { title: "PDF", fields: ["pdf_url", "pdf_hash", "qr_payload", "snapshot"] },
      { title: "Auditoria", fields: ["gerado_por_username", "gerado_em", "created_at", "updated_at"] },
    ],
  },
  {
    key: "assinaturas",
    label: "Assinaturas",
    path: "/contratos/assinaturas",
    endpoint: "/assinaturas/",
    description: "Controle de assinaturas vinculadas aos contratos.",
    filters: ["tipo"],
    columns: ["contrato_numero", "tipo", "nome", "cpf", "data_assinatura"],
    fields: [
      { name: "contrato", label: "Contrato", type: "select", resource: "contratos", required: true },
      { name: "tipo", label: "Tipo", type: "select", options: assinaturaTipo, required: true },
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text", required: true },
      { name: "data_assinatura", label: "Data assinatura", type: "date" },
      { name: "created_at", label: "Criado em", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Assinatura", fields: ["contrato", "tipo", "nome", "cpf", "data_assinatura"] },
      { title: "Auditoria", fields: ["created_at"] },
    ],
  },
  {
    key: "usuarios",
    label: "Usuarios",
    path: "/seguranca/usuarios",
    endpoint: "/usuarios/",
    description: "Usuarios de acesso ao sistema e grupos vinculados.",
    optionLabel: "username",
    filters: ["is_active", "is_staff", "is_superuser"],
    columns: ["username", "email", "is_active", "is_staff", "is_superuser"],
    fields: [
      { name: "username", label: "Usuario", type: "text", required: true },
      { name: "first_name", label: "Nome", type: "text" },
      { name: "last_name", label: "Sobrenome", type: "text" },
      { name: "email", label: "Email", type: "email" },
      { name: "is_active", label: "Ativo", type: "boolean" },
      { name: "is_staff", label: "Equipe", type: "boolean" },
      { name: "is_superuser", label: "Superusuario", type: "boolean" },
      { name: "password", label: "Senha", type: "text" },
      { name: "groups", label: "Grupos", type: "multiselect", resource: "grupos" },
      { name: "user_permissions", label: "Permissoes", type: "multiselect", resource: "permissoes" },
    ],
    sections: [
      { title: "Credenciais", fields: ["username", "password"] },
      { title: "Dados pessoais", fields: ["first_name", "last_name", "email"] },
      { title: "Acesso", fields: ["is_active", "is_staff", "is_superuser"] },
      { title: "Permissoes", fields: ["groups", "user_permissions"] },
    ],
  },
  {
    key: "grupos",
    label: "Grupos e permissoes",
    path: "/seguranca/grupos",
    endpoint: "/grupos/",
    description: "Perfis de acesso e permissoes detalhadas.",
    optionLabel: "name",
    columns: ["name"],
    fields: [
      { name: "name", label: "Nome", type: "text", required: true },
      { name: "permissions", label: "Permissoes", type: "multiselect", resource: "permissoes" },
    ],
    sections: [
      { title: "Grupo", fields: ["name"] },
      { title: "Permissoes", fields: ["permissions"] },
    ],
  },
  {
    key: "permissoes",
    label: "Permissoes",
    path: "/seguranca/permissoes",
    endpoint: "/permissoes/",
    description: "Lista somente leitura de permissoes do Django.",
    optionLabel: "name",
    readOnly: true,
    columns: ["name", "codename", "content_type_label"],
    fields: [
      { name: "name", label: "Nome", type: "text", readOnly: true },
      { name: "codename", label: "Codename", type: "text", readOnly: true },
      { name: "content_type_label", label: "Content type", type: "text", readOnly: true },
    ],
    sections: [
      { title: "Permissao", fields: ["name", "codename", "content_type_label"] },
    ],
  },
];

export const resourceGroups = [
  {
    label: "Cadastros",
    items: ["escolas", "responsaveis", "alunos", "professores", "turmas"],
  },
  {
    label: "Financeiro",
    items: ["planos", "pagamentos-alunos", "pagamentos-professores", "despesas"],
  },
  {
    label: "Contratos",
    items: ["templates-contrato", "contratos", "assinaturas"],
  },
  {
    label: "Seguranca",
    items: ["usuarios", "grupos", "permissoes"],
  },
];

export const resourceMap = new Map(resources.map((resource) => [resource.key, resource]));
