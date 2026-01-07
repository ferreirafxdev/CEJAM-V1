import {
  Banknote,
  BookOpen,
  CheckCircle,
  ClipboardList,
  FileCheck,
  GraduationCap,
  Receipt,
  School,
  Shield,
  UserCheck,
  UserCog,
  Users,
  UsersRound,
  Wallet,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export type SelectOption = {
  value: string | number;
  label: string;
};

export type ResourceOptionSource = {
  endpoint: string;
  labelKey: string;
  valueKey?: string;
};

export type ResourceField = {
  name: string;
  label: string;
  type:
    | "text"
    | "email"
    | "number"
    | "currency"
    | "date"
    | "textarea"
    | "select"
    | "boolean"
    | "password";
  required?: boolean;
  readOnly?: boolean;
  options?: SelectOption[];
  resource?: ResourceOptionSource;
  multiple?: boolean;
  valueType?: "string" | "number";
  placeholder?: string;
  helper?: string;
  defaultValue?: string | number | boolean | string[];
};

export type ResourceColumn<T> = {
  key: string;
  label: string;
  value?: (item: T) => string | number | boolean | null;
};

export type ResourceConfig<T = Record<string, unknown>> = {
  key: string;
  path: string;
  title: string;
  singular: string;
  description: string;
  endpoint: string;
  fields: ResourceField[];
  columns: ResourceColumn<T>[];
  allowCreate?: boolean;
  allowEdit?: boolean;
  allowDelete?: boolean;
  searchable?: boolean;
};

export type SectionItem = {
  label: string;
  description: string;
  path: string;
  icon: LucideIcon;
};

export type SectionConfig = {
  title: string;
  description: string;
  items: SectionItem[];
};

const sexoOptions: SelectOption[] = [
  { value: "M", label: "Masculino" },
  { value: "F", label: "Feminino" },
  { value: "O", label: "Outro" },
];

const statusAlunoOptions: SelectOption[] = [
  { value: "ATIVO", label: "Ativo" },
  { value: "INATIVO", label: "Inativo" },
  { value: "TRANCADO", label: "Trancado" },
];

const statusProfessorOptions: SelectOption[] = [
  { value: "ATIVO", label: "Ativo" },
  { value: "INATIVO", label: "Inativo" },
];

const tipoVinculoOptions: SelectOption[] = [
  { value: "CLT", label: "CLT" },
  { value: "HORISTA", label: "Horista" },
  { value: "PJ", label: "PJ" },
];

const turnoOptions: SelectOption[] = [
  { value: "MANHA", label: "Manha" },
  { value: "TARDE", label: "Tarde" },
  { value: "NOITE", label: "Noite" },
];

const statusTurmaOptions: SelectOption[] = [
  { value: "ATIVA", label: "Ativa" },
  { value: "ENCERRADA", label: "Encerrada" },
];

const contratoStatusOptions: SelectOption[] = [
  { value: "RASCUNHO", label: "Rascunho" },
  { value: "EMITIDO", label: "Emitido" },
  { value: "CANCELADO", label: "Cancelado" },
];

const assinaturaTipoOptions: SelectOption[] = [
  { value: "RESPONSAVEL", label: "Responsavel" },
  { value: "ESCOLA", label: "Escola" },
  { value: "TESTEMUNHA_1", label: "Testemunha 1" },
  { value: "TESTEMUNHA_2", label: "Testemunha 2" },
];

const formaPagamentoOptions: SelectOption[] = [
  { value: "DINHEIRO", label: "Dinheiro" },
  { value: "PIX", label: "Pix" },
  { value: "BOLETO", label: "Boleto" },
  { value: "CARTAO", label: "Cartao" },
];

const modeloPagamentoOptions: SelectOption[] = [
  { value: "MENSAL", label: "Mensal" },
  { value: "TRIMESTRAL", label: "Trimestral" },
  { value: "SEMESTRAL", label: "Semestral" },
  { value: "ANUAL", label: "Anual" },
];

const bolsaTipoOptions: SelectOption[] = [
  { value: "NENHUMA", label: "Nenhuma" },
  { value: "PARCIAL", label: "Parcial" },
  { value: "INTEGRAL", label: "Integral" },
  { value: "CONVENIO", label: "Convenio" },
];

const statusPagamentoAlunoOptions: SelectOption[] = [
  { value: "PAGO", label: "Pago" },
  { value: "EM_ABERTO", label: "Em aberto" },
  { value: "ATRASADO", label: "Atrasado" },
  { value: "ISENTO", label: "Isento" },
];

const statusPagamentoProfessorOptions: SelectOption[] = [
  { value: "PAGO", label: "Pago" },
  { value: "PENDENTE", label: "Pendente" },
];

const despesaCategoriaOptions: SelectOption[] = [
  { value: "AGUA", label: "Agua" },
  { value: "LUZ", label: "Luz" },
  { value: "ALUGUEL", label: "Aluguel" },
  { value: "INTERNET", label: "Internet" },
  { value: "MATERIAL", label: "Material" },
  { value: "OUTROS", label: "Outros" },
];

const despesaTipoOptions: SelectOption[] = [
  { value: "FIXA", label: "Fixa" },
  { value: "VARIAVEL", label: "Variavel" },
];

export const resourceConfigs: ResourceConfig[] = [
  {
    key: "escolas",
    path: "/escolas",
    title: "Escolas",
    singular: "Escola",
    description: "Cadastre e acompanhe as unidades escolares.",
    endpoint: "/escolas",
    searchable: true,
    fields: [
      { name: "razao_social", label: "Razao social", type: "text", required: true },
      { name: "nome_fantasia", label: "Nome fantasia", type: "text", required: true },
      { name: "cnpj", label: "CNPJ", type: "text", required: true },
      {
        name: "endereco_completo",
        label: "Endereco completo",
        type: "textarea",
        required: true,
      },
      { name: "cidade", label: "Cidade", type: "text", required: true },
      { name: "uf", label: "UF", type: "text", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "email", label: "Email", type: "email", required: true },
      { name: "responsavel", label: "Responsavel", type: "text", required: true },
    ],
    columns: [
      { key: "nome_fantasia", label: "Nome fantasia" },
      { key: "cnpj", label: "CNPJ" },
      { key: "cidade", label: "Cidade" },
      { key: "telefone", label: "Telefone" },
    ],
  },
  {
    key: "responsaveis",
    path: "/responsaveis",
    title: "Responsaveis",
    singular: "Responsavel",
    description: "Gerencie os responsaveis financeiros e legais.",
    endpoint: "/responsaveis",
    searchable: true,
    fields: [
      { name: "nome_completo", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text", required: true },
      { name: "rg", label: "RG", type: "text" },
      { name: "endereco", label: "Endereco", type: "textarea", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "email", label: "Email", type: "email", required: true },
    ],
    columns: [
      { key: "nome_completo", label: "Nome" },
      { key: "cpf", label: "CPF" },
      { key: "telefone", label: "Telefone" },
      { key: "email", label: "Email" },
    ],
  },
  {
    key: "alunos",
    path: "/alunos",
    title: "Alunos",
    singular: "Aluno",
    description: "Mantenha matriculas, documentos e status atualizados.",
    endpoint: "/alunos",
    searchable: true,
    fields: [
      { name: "nome_completo", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text" },
      { name: "data_nascimento", label: "Data de nascimento", type: "date", required: true },
      { name: "sexo", label: "Sexo", type: "select", options: sexoOptions, required: true },
      { name: "endereco", label: "Endereco", type: "textarea", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      {
        name: "responsavel",
        label: "Responsavel",
        type: "select",
        resource: { endpoint: "/responsaveis", labelKey: "nome_completo" },
        valueType: "number",
      },
      { name: "nome_responsavel", label: "Nome responsavel", type: "text" },
      { name: "telefone_responsavel", label: "Telefone responsavel", type: "text" },
      { name: "email_responsavel", label: "Email responsavel", type: "email" },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: statusAlunoOptions,
        defaultValue: "ATIVO",
      },
      { name: "data_matricula", label: "Data de matricula", type: "date", required: true },
      { name: "numero_matricula", label: "Numero matricula", type: "text" },
      {
        name: "turma",
        label: "Turma",
        type: "select",
        resource: { endpoint: "/turmas", labelKey: "nome" },
        valueType: "number",
        required: true,
      },
      {
        name: "plano_financeiro",
        label: "Plano financeiro",
        type: "select",
        resource: { endpoint: "/planos", labelKey: "nome" },
        valueType: "number",
      },
      {
        name: "valor_mensalidade",
        label: "Valor mensalidade",
        type: "currency",
        required: true,
      },
      { name: "observacoes", label: "Observacoes", type: "textarea" },
      { name: "historico_escolar", label: "Historico escolar", type: "textarea" },
    ],
    columns: [
      { key: "nome_completo", label: "Aluno" },
      { key: "turma_nome", label: "Turma" },
      { key: "plano_financeiro_nome", label: "Plano" },
      { key: "status", label: "Status" },
      { key: "data_matricula", label: "Matricula" },
    ],
  },
  {
    key: "professores",
    path: "/professores",
    title: "Professores",
    singular: "Professor",
    description: "Gestao completa da equipe docente.",
    endpoint: "/professores",
    searchable: true,
    fields: [
      { name: "nome_completo", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text", required: true },
      { name: "especialidade", label: "Especialidade", type: "text", required: true },
      { name: "telefone", label: "Telefone", type: "text", required: true },
      { name: "email", label: "Email", type: "email", required: true },
      {
        name: "tipo_vinculo",
        label: "Tipo vinculo",
        type: "select",
        options: tipoVinculoOptions,
        required: true,
      },
      { name: "valor_hora", label: "Valor hora", type: "currency" },
      { name: "salario_fixo", label: "Salario fixo", type: "currency" },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: statusProfessorOptions,
        defaultValue: "ATIVO",
      },
    ],
    columns: [
      { key: "nome_completo", label: "Professor" },
      { key: "especialidade", label: "Especialidade" },
      { key: "tipo_vinculo", label: "Vinculo" },
      { key: "status", label: "Status" },
    ],
  },
  {
    key: "turmas",
    path: "/turmas",
    title: "Turmas",
    singular: "Turma",
    description: "Organize classes, horarios e professores responsaveis.",
    endpoint: "/turmas",
    searchable: true,
    fields: [
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "serie_ano", label: "Serie/ano", type: "text", required: true },
      { name: "turno", label: "Turno", type: "select", options: turnoOptions, required: true },
      {
        name: "professor_responsavel",
        label: "Professor responsavel",
        type: "select",
        resource: { endpoint: "/professores", labelKey: "nome_completo" },
        valueType: "number",
        required: true,
      },
      {
        name: "valor_mensalidade",
        label: "Valor mensalidade",
        type: "currency",
        required: true,
      },
      { name: "capacidade_maxima", label: "Capacidade maxima", type: "number", required: true },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: statusTurmaOptions,
        defaultValue: "ATIVA",
      },
    ],
    columns: [
      { key: "nome", label: "Turma" },
      { key: "serie_ano", label: "Serie/ano" },
      { key: "turno", label: "Turno" },
      { key: "professor_nome", label: "Professor" },
      { key: "status", label: "Status" },
    ],
  },
  {
    key: "planos",
    path: "/planos",
    title: "Planos educacionais",
    singular: "Plano",
    description: "Defina valores, duracao e regras financeiras.",
    endpoint: "/planos",
    searchable: true,
    fields: [
      { name: "nome", label: "Nome", type: "text", required: true },
      {
        name: "valor_mensalidade",
        label: "Valor mensalidade",
        type: "currency",
        required: true,
      },
      {
        name: "modelo_pagamento",
        label: "Modelo pagamento",
        type: "select",
        options: modeloPagamentoOptions,
        required: true,
        defaultValue: "MENSAL",
      },
      {
        name: "dia_vencimento",
        label: "Dia vencimento",
        type: "number",
        required: true,
      },
      {
        name: "duracao_meses",
        label: "Duracao (meses)",
        type: "number",
        required: true,
      },
      {
        name: "forma_pagamento_padrao",
        label: "Forma pagamento padrao",
        type: "select",
        options: formaPagamentoOptions,
      },
      {
        name: "taxa_matricula",
        label: "Taxa matricula",
        type: "currency",
        required: true,
        defaultValue: 0,
      },
      {
        name: "desconto_percent",
        label: "Desconto (%)",
        type: "currency",
        defaultValue: 0,
      },
      {
        name: "bolsa_tipo",
        label: "Bolsa",
        type: "select",
        options: bolsaTipoOptions,
        defaultValue: "NENHUMA",
      },
      {
        name: "bolsa_percent",
        label: "Bolsa (%)",
        type: "currency",
        defaultValue: 0,
      },
      {
        name: "multa_percent",
        label: "Multa (%)",
        type: "currency",
        required: true,
        defaultValue: 0,
      },
      {
        name: "juros_percent",
        label: "Juros fixo (%)",
        type: "currency",
        required: true,
        defaultValue: 0,
      },
      {
        name: "juros_diario_percent",
        label: "Juros diario (%)",
        type: "currency",
        defaultValue: 0,
      },
      {
        name: "ativo",
        label: "Ativo",
        type: "boolean",
        defaultValue: true,
      },
    ],
    columns: [
      { key: "nome", label: "Plano" },
      { key: "modelo_pagamento", label: "Modelo" },
      { key: "valor_mensalidade", label: "Mensalidade" },
      { key: "dia_vencimento", label: "Vencimento" },
      { key: "ativo", label: "Ativo" },
    ],
  },
  {
    key: "pagamentos-alunos",
    path: "/pagamentos-alunos",
    title: "Pagamentos de alunos",
    singular: "Pagamento aluno",
    description: "Controle mensalidades, vencimentos e recebimentos.",
    endpoint: "/pagamentos-alunos",
    searchable: true,
    fields: [
      {
        name: "aluno",
        label: "Aluno",
        type: "select",
        resource: { endpoint: "/alunos", labelKey: "nome_completo" },
        valueType: "number",
        required: true,
      },
      {
        name: "plano",
        label: "Plano",
        type: "select",
        resource: { endpoint: "/planos", labelKey: "nome" },
        valueType: "number",
      },
      {
        name: "competencia",
        label: "Competencia",
        type: "date",
        required: true,
      },
      { name: "valor", label: "Valor", type: "currency", required: true },
      {
        name: "valor_pago",
        label: "Valor pago",
        type: "currency",
        helper: "Preencha quando o pagamento for concluido.",
      },
      {
        name: "desconto",
        label: "Desconto",
        type: "currency",
        readOnly: true,
      },
      {
        name: "multa",
        label: "Multa",
        type: "currency",
        readOnly: true,
      },
      {
        name: "juros",
        label: "Juros",
        type: "currency",
        readOnly: true,
      },
      {
        name: "dias_atraso",
        label: "Dias atraso",
        type: "number",
        readOnly: true,
      },
      {
        name: "valor_total",
        label: "Total devido",
        type: "currency",
        readOnly: true,
      },
      {
        name: "data_vencimento",
        label: "Data vencimento",
        type: "date",
        required: true,
      },
      { name: "data_pagamento", label: "Data pagamento", type: "date" },
      {
        name: "forma_pagamento",
        label: "Forma pagamento",
        type: "select",
        options: formaPagamentoOptions,
        required: true,
      },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: statusPagamentoAlunoOptions,
        defaultValue: "EM_ABERTO",
      },
      { name: "observacoes", label: "Observacoes", type: "textarea" },
    ],
    columns: [
      { key: "aluno_nome", label: "Aluno" },
      { key: "turma_nome", label: "Turma" },
      { key: "competencia", label: "Competencia" },
      { key: "valor_total", label: "Total" },
      { key: "status", label: "Status" },
    ],
  },
  {
    key: "pagamentos-professores",
    path: "/pagamentos-professores",
    title: "Pagamentos de professores",
    singular: "Pagamento professor",
    description: "Registre competencias e valores da equipe docente.",
    endpoint: "/pagamentos-professores",
    searchable: true,
    fields: [
      {
        name: "professor",
        label: "Professor",
        type: "select",
        resource: { endpoint: "/professores", labelKey: "nome_completo" },
        valueType: "number",
        required: true,
      },
      {
        name: "competencia",
        label: "Competencia",
        type: "date",
        required: true,
      },
      {
        name: "valor_bruto",
        label: "Valor bruto",
        type: "currency",
        required: true,
      },
      {
        name: "descontos",
        label: "Descontos",
        type: "currency",
        required: true,
        defaultValue: 0,
      },
      {
        name: "valor_liquido",
        label: "Valor liquido",
        type: "currency",
        readOnly: true,
        helper: "Calculado automaticamente quando vazio.",
      },
      { name: "data_pagamento", label: "Data pagamento", type: "date" },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: statusPagamentoProfessorOptions,
        defaultValue: "PENDENTE",
      },
    ],
    columns: [
      { key: "professor_nome", label: "Professor" },
      { key: "competencia", label: "Competencia" },
      { key: "valor_bruto", label: "Valor bruto" },
      { key: "valor_liquido", label: "Valor liquido" },
      { key: "status", label: "Status" },
    ],
  },
  {
    key: "despesas",
    path: "/despesas",
    title: "Despesas",
    singular: "Despesa",
    description: "Acompanhe custos fixos e variaveis.",
    endpoint: "/despesas",
    searchable: true,
    fields: [
      { name: "descricao", label: "Descricao", type: "text", required: true },
      {
        name: "categoria",
        label: "Categoria",
        type: "select",
        options: despesaCategoriaOptions,
        required: true,
      },
      { name: "valor", label: "Valor", type: "currency", required: true },
      { name: "data", label: "Data", type: "date", required: true },
      {
        name: "tipo",
        label: "Tipo",
        type: "select",
        options: despesaTipoOptions,
        required: true,
      },
      { name: "observacoes", label: "Observacoes", type: "textarea" },
    ],
    columns: [
      { key: "descricao", label: "Descricao" },
      { key: "categoria", label: "Categoria" },
      { key: "valor", label: "Valor" },
      { key: "data", label: "Data" },
      { key: "tipo", label: "Tipo" },
    ],
  },
  {
    key: "templates",
    path: "/templates-contrato",
    title: "Templates de contrato",
    singular: "Template de contrato",
    description: "Padronize textos e estilos para contratos escolares.",
    endpoint: "/templates-contrato",
    searchable: true,
    fields: [
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "versao", label: "Versao", type: "text", required: true },
      { name: "corpo_html", label: "Corpo HTML", type: "textarea", required: true },
      { name: "css", label: "CSS", type: "textarea" },
      {
        name: "ativo",
        label: "Ativo",
        type: "boolean",
        defaultValue: true,
      },
    ],
    columns: [
      { key: "nome", label: "Template" },
      { key: "versao", label: "Versao" },
      { key: "ativo", label: "Ativo" },
      { key: "updated_at", label: "Atualizado" },
    ],
  },
  {
    key: "contratos",
    path: "/contratos",
    title: "Contratos",
    singular: "Contrato",
    description: "Emissao e acompanhamento de contratos escolares.",
    endpoint: "/contratos",
    searchable: true,
    fields: [
      {
        name: "numero",
        label: "Numero",
        type: "text",
        readOnly: true,
      },
      {
        name: "escola",
        label: "Escola",
        type: "select",
        resource: { endpoint: "/escolas", labelKey: "nome_fantasia" },
        valueType: "number",
        required: true,
      },
      {
        name: "aluno",
        label: "Aluno",
        type: "select",
        resource: { endpoint: "/alunos", labelKey: "nome_completo" },
        valueType: "number",
        required: true,
      },
      {
        name: "responsavel",
        label: "Responsavel",
        type: "select",
        resource: { endpoint: "/responsaveis", labelKey: "nome_completo" },
        valueType: "number",
        required: true,
      },
      {
        name: "turma",
        label: "Turma",
        type: "select",
        resource: { endpoint: "/turmas", labelKey: "nome" },
        valueType: "number",
        required: true,
      },
      {
        name: "plano",
        label: "Plano educacional",
        type: "select",
        resource: { endpoint: "/planos", labelKey: "nome" },
        valueType: "number",
        required: true,
      },
      {
        name: "template",
        label: "Template",
        type: "select",
        resource: { endpoint: "/templates-contrato", labelKey: "nome" },
        valueType: "number",
        required: true,
      },
      {
        name: "data_emissao",
        label: "Data emissao",
        type: "date",
        required: true,
      },
      {
        name: "cidade_assinatura",
        label: "Cidade assinatura",
        type: "text",
        required: true,
      },
      {
        name: "status",
        label: "Status",
        type: "select",
        options: contratoStatusOptions,
        defaultValue: "RASCUNHO",
      },
    ],
    columns: [
      { key: "numero", label: "Contrato" },
      { key: "aluno_nome", label: "Aluno" },
      { key: "escola_nome", label: "Escola" },
      { key: "status", label: "Status" },
      { key: "data_emissao", label: "Emissao" },
    ],
  },
  {
    key: "assinaturas",
    path: "/assinaturas",
    title: "Assinaturas",
    singular: "Assinatura",
    description: "Registre assinaturas e aceite digital.",
    endpoint: "/assinaturas",
    searchable: true,
    fields: [
      {
        name: "contrato",
        label: "Contrato",
        type: "select",
        resource: { endpoint: "/contratos", labelKey: "numero" },
        valueType: "number",
        required: true,
      },
      {
        name: "tipo",
        label: "Tipo",
        type: "select",
        options: assinaturaTipoOptions,
        required: true,
      },
      { name: "nome", label: "Nome", type: "text", required: true },
      { name: "cpf", label: "CPF", type: "text", required: true },
      { name: "data_assinatura", label: "Data assinatura", type: "date" },
    ],
    columns: [
      { key: "contrato_numero", label: "Contrato" },
      { key: "tipo", label: "Tipo" },
      { key: "nome", label: "Nome" },
      { key: "data_assinatura", label: "Data" },
    ],
  },
  {
    key: "permissoes",
    path: "/permissoes",
    title: "Permissoes",
    singular: "Permissao",
    description: "Visualize permissoes cadastradas no sistema.",
    endpoint: "/permissoes",
    searchable: true,
    allowCreate: false,
    allowEdit: false,
    allowDelete: false,
    fields: [
      { name: "name", label: "Nome", type: "text", readOnly: true },
      { name: "codename", label: "Codename", type: "text", readOnly: true },
      { name: "content_type", label: "Content type", type: "number", readOnly: true },
    ],
    columns: [
      { key: "name", label: "Permissao" },
      { key: "codename", label: "Codigo" },
      { key: "content_type", label: "Content type" },
    ],
  },
  {
    key: "grupos",
    path: "/grupos",
    title: "Grupos",
    singular: "Grupo",
    description: "Organize grupos e niveis de acesso.",
    endpoint: "/grupos",
    searchable: true,
    fields: [
      { name: "name", label: "Nome", type: "text", required: true },
      {
        name: "permissions",
        label: "Permissoes",
        type: "select",
        multiple: true,
        resource: { endpoint: "/permissoes", labelKey: "name" },
        valueType: "number",
      },
    ],
    columns: [
      { key: "name", label: "Grupo" },
      {
        key: "permissions",
        label: "Permissoes",
        value: (item) => {
          const permissions = (item as { permissions?: unknown[] }).permissions;
          return permissions ? permissions.length : 0;
        },
      },
    ],
  },
  {
    key: "usuarios",
    path: "/usuarios",
    title: "Usuarios",
    singular: "Usuario",
    description: "Controle acessos e perfis administrativos.",
    endpoint: "/usuarios",
    searchable: true,
    fields: [
      { name: "username", label: "Usuario", type: "text", required: true },
      { name: "first_name", label: "Nome", type: "text" },
      { name: "last_name", label: "Sobrenome", type: "text" },
      { name: "email", label: "Email", type: "email" },
      { name: "is_active", label: "Ativo", type: "boolean", defaultValue: true },
      { name: "is_staff", label: "Staff", type: "boolean" },
      { name: "is_superuser", label: "Superuser", type: "boolean" },
      {
        name: "groups",
        label: "Grupos",
        type: "select",
        multiple: true,
        resource: { endpoint: "/grupos", labelKey: "name" },
        valueType: "number",
      },
      {
        name: "user_permissions",
        label: "Permissoes diretas",
        type: "select",
        multiple: true,
        resource: { endpoint: "/permissoes", labelKey: "name" },
        valueType: "number",
      },
      {
        name: "password",
        label: "Senha",
        type: "password",
        helper: "Preencha apenas para criar ou atualizar senha.",
      },
    ],
    columns: [
      { key: "username", label: "Usuario" },
      { key: "email", label: "Email" },
      { key: "is_active", label: "Ativo" },
      { key: "is_staff", label: "Staff" },
      { key: "is_superuser", label: "Superuser" },
    ],
  },
];

export const resourceByPath = resourceConfigs.reduce<Record<string, ResourceConfig>>(
  (acc, config) => {
    acc[config.path] = config;
    return acc;
  },
  {}
);

export const sectionByPath: Record<string, SectionConfig> = {
  "/cadastros": {
    title: "Cadastros",
    description: "Centralize cadastros essenciais do painel escolar.",
    items: [
      {
        label: "Escolas",
        description: "Unidades e dados institucionais.",
        path: "/escolas",
        icon: School,
      },
      {
        label: "Responsaveis",
        description: "Responsaveis legais e financeiros.",
        path: "/responsaveis",
        icon: UserCheck,
      },
      {
        label: "Alunos",
        description: "Matriculas e perfis dos alunos.",
        path: "/alunos",
        icon: GraduationCap,
      },
      {
        label: "Professores",
        description: "Equipe docente e especialidades.",
        path: "/professores",
        icon: Users,
      },
      {
        label: "Turmas",
        description: "Organizacao das turmas.",
        path: "/turmas",
        icon: UsersRound,
      },
    ],
  },
  "/financeiro": {
    title: "Financeiro",
    description: "Fluxo de pagamentos, planos e despesas.",
    items: [
      {
        label: "Planos educacionais",
        description: "Valores e condicoes dos planos.",
        path: "/planos",
        icon: ClipboardList,
      },
      {
        label: "Pagamentos alunos",
        description: "Mensalidades e recebimentos.",
        path: "/pagamentos-alunos",
        icon: Banknote,
      },
      {
        label: "Pagamentos professores",
        description: "Competencias e repasses docentes.",
        path: "/pagamentos-professores",
        icon: Wallet,
      },
      {
        label: "Despesas",
        description: "Custos fixos e variaveis.",
        path: "/despesas",
        icon: Receipt,
      },
    ],
  },
  "/documentos": {
    title: "Documentos",
    description: "Modelos, contratos e assinaturas digitais.",
    items: [
      {
        label: "Templates de Contrato",
        description: "Gerencie layouts de contratos.",
        path: "/templates-contrato",
        icon: BookOpen,
      },
      {
        label: "Contratos",
        description: "Emissao e historico de contratos.",
        path: "/contratos",
        icon: FileCheck,
      },
      {
        label: "Assinaturas",
        description: "Controle de assinaturas e aceite.",
        path: "/assinaturas",
        icon: CheckCircle,
      },
    ],
  },
  "/seguranca": {
    title: "Seguranca",
    description: "Controle de acesso e politicas administrativas.",
    items: [
      {
        label: "Permissoes",
        description: "Permissoes do sistema.",
        path: "/permissoes",
        icon: Shield,
      },
      {
        label: "Grupos",
        description: "Perfis e grupos de acesso.",
        path: "/grupos",
        icon: Users,
      },
      {
        label: "Usuarios",
        description: "Administradores e equipes internas.",
        path: "/usuarios",
        icon: UserCog,
      },
    ],
  },
};
