import { useEffect, useMemo, useState } from "react";
import { Search } from "lucide-react";

import { getStoredAccessToken, listResource, updateResource } from "../lib/api";
import { formatDate, formatDateTime, formatNumber, formatPercent } from "../lib/format";
import { useToast } from "../components/Toast";

type AlunoItem = {
  id: number;
  nome_completo: string;
  cpf?: string | null;
  turma_nome?: string | null;
  plano_financeiro_nome?: string | null;
  status?: string | null;
};

type PagamentoAlunoItem = {
  id: number;
  aluno: number;
  aluno_nome?: string;
  turma_nome?: string;
  plano_nome?: string | null;
  competencia?: string | null;
  valor?: number | string | null;
  valor_pago?: number | string | null;
  valor_total?: number | string | null;
  desconto?: number | string | null;
  multa?: number | string | null;
  juros?: number | string | null;
  dias_atraso?: number | null;
  data_vencimento?: string | null;
  data_pagamento?: string | null;
  forma_pagamento?: string | null;
  status?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  pagamento_registrado_em?: string | null;
  nf_numero?: string | null;
  nf_pdf_url?: string;
};

const alunoStatusLabels: Record<string, string> = {
  ATIVO: "Ativo",
  INATIVO: "Inativo",
  TRANCADO: "Trancado",
};

const statusLabels: Record<string, string> = {
  PAGO: "Feito",
  EM_ABERTO: "Em aberto",
  ATRASADO: "Atrasado",
  ISENTO: "Isento",
  PENDENTE: "Em aberto",
};

const statusStyles: Record<string, string> = {
  PAGO: "bg-emerald-100 text-emerald-700",
  EM_ABERTO: "bg-amber-100 text-amber-700",
  ATRASADO: "bg-rose-100 text-rose-700",
  ISENTO: "bg-slate-100 text-slate-600",
  PENDENTE: "bg-amber-100 text-amber-700",
  ATIVO: "bg-emerald-100 text-emerald-700",
  INATIVO: "bg-rose-100 text-rose-700",
  TRANCADO: "bg-slate-200 text-slate-700",
};

const formaPagamentoLabels: Record<string, string> = {
  DINHEIRO: "Dinheiro",
  PIX: "Pix",
  BOLETO: "Boleto",
  CARTAO: "Cartao",
};

const statusOptions = [
  { value: "EM_ABERTO", label: "Em aberto" },
  { value: "PAGO", label: "Feito" },
  { value: "ATRASADO", label: "Atrasado" },
  { value: "ISENTO", label: "Isento" },
];

const formaPagamentoOptions = [
  { value: "DINHEIRO", label: "Dinheiro" },
  { value: "PIX", label: "Pix" },
  { value: "BOLETO", label: "Boleto" },
  { value: "CARTAO", label: "Cartao" },
];

async function fetchAllPages<T>(
  endpoint: string,
  params?: Record<string, string | number | boolean | null | undefined>
) {
  const results: T[] = [];
  let page = 1;
  let hasNext = true;

  while (hasNext) {
    const response = await listResource<T>(endpoint, { ...params, page });
    results.push(...(response.results ?? []));
    hasNext = Boolean(response.next);
    page += 1;
  }

  return results;
}

function formatMoney(value?: number | string | null) {
  const formatted = formatNumber(value ?? undefined);
  if (formatted === "--") {
    return formatted;
  }
  return `R$ ${formatted}`;
}

function formatAlunoStatus(value?: string | null) {
  if (!value) {
    return "--";
  }
  return alunoStatusLabels[value] ?? value;
}

function formatPaymentStatus(value?: string | null) {
  if (!value) {
    return "--";
  }
  return statusLabels[value] ?? value;
}

function getStatusClass(value?: string | null) {
  if (!value) {
    return "bg-slate-100 text-slate-600";
  }
  return statusStyles[value] ?? "bg-slate-100 text-slate-600";
}

function formatFormaPagamento(value?: string | null) {
  if (!value) {
    return "--";
  }
  return formaPagamentoLabels[value] ?? value;
}

function getRegistroTimestamp(payment: PagamentoAlunoItem) {
  return formatDateTime(
    payment.pagamento_registrado_em ?? payment.updated_at ?? payment.created_at ?? undefined
  );
}

function getJurosPercent(payment: PagamentoAlunoItem) {
  const valor = Number(payment.valor ?? 0);
  const desconto = Number(payment.desconto ?? 0);
  const juros = Number(payment.juros ?? 0);
  const base = valor - desconto;
  if (!Number.isFinite(base) || !Number.isFinite(juros) || base <= 0) {
    return "--";
  }
  return formatPercent((juros / base) * 100);
}

export function PagamentoAlunosPage() {
  const [students, setStudents] = useState<AlunoItem[]>([]);
  const [payments, setPayments] = useState<PagamentoAlunoItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [editingPaymentId, setEditingPaymentId] = useState<number | null>(null);
  const [paymentForm, setPaymentForm] = useState({
    status: "EM_ABERTO",
    forma_pagamento: "DINHEIRO",
    data_pagamento: "",
  });
  const [savingPayment, setSavingPayment] = useState(false);
  const [search, setSearch] = useState("");
  const [loadingStudents, setLoadingStudents] = useState(true);
  const [loadingPayments, setLoadingPayments] = useState(false);
  const { pushToast } = useToast();

  const hasToken = Boolean(getStoredAccessToken());

  useEffect(() => {
    let active = true;

    if (!hasToken) {
      setStudents([]);
      setLoadingStudents(false);
      return () => {
        active = false;
      };
    }

    const loadStudents = async () => {
      setLoadingStudents(true);
      try {
        const data = await fetchAllPages<AlunoItem>("/alunos");
        if (!active) {
          return;
        }
        setStudents(data);
        if (data.length > 0) {
          setSelectedId((current) => current ?? data[0].id);
        }
      } catch (err) {
        if (!active) {
          return;
        }
        pushToast({
          title: "Erro ao carregar alunos",
          description: err instanceof Error ? err.message : "Erro ao carregar alunos",
          variant: "error",
        });
        setStudents([]);
      } finally {
        if (active) {
          setLoadingStudents(false);
        }
      }
    };

    loadStudents();

    return () => {
      active = false;
    };
  }, [hasToken, pushToast]);

  useEffect(() => {
    let active = true;

    if (!hasToken || selectedId === null) {
      setPayments([]);
      return () => {
        active = false;
      };
    }

    const loadPayments = async () => {
      setLoadingPayments(true);
      try {
        const data = await fetchAllPages<PagamentoAlunoItem>(
          "/pagamentos-alunos",
          { aluno: selectedId }
        );
        if (!active) {
          return;
        }
        setPayments(data);
      } catch (err) {
        if (!active) {
          return;
        }
        pushToast({
          title: "Erro ao carregar pagamentos",
          description: err instanceof Error ? err.message : "Erro ao carregar pagamentos",
          variant: "error",
        });
        setPayments([]);
      } finally {
        if (active) {
          setLoadingPayments(false);
        }
      }
    };

    loadPayments();

    return () => {
      active = false;
    };
  }, [hasToken, pushToast, selectedId]);

  useEffect(() => {
    setEditingPaymentId(null);
  }, [selectedId]);

  const filteredStudents = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) {
      return students;
    }
    return students.filter((student) => {
      const name = student.nome_completo?.toLowerCase() ?? "";
      const cpf = student.cpf?.toLowerCase() ?? "";
      const turma = student.turma_nome?.toLowerCase() ?? "";
      return name.includes(term) || cpf.includes(term) || turma.includes(term);
    });
  }, [search, students]);

  const selectedStudent = useMemo(
    () => students.find((student) => student.id === selectedId) ?? null,
    [students, selectedId]
  );

  const editingPayment = useMemo(
    () => payments.find((payment) => payment.id === editingPaymentId) ?? null,
    [payments, editingPaymentId]
  );

  useEffect(() => {
    if (!editingPayment) {
      return;
    }
    setPaymentForm({
      status: editingPayment.status ?? "EM_ABERTO",
      forma_pagamento: editingPayment.forma_pagamento ?? "DINHEIRO",
      data_pagamento: editingPayment.data_pagamento ?? "",
    });
  }, [editingPayment]);

  const summary = useMemo(() => {
    const total = payments.length;
    const paid = payments.filter((payment) => payment.status === "PAGO").length;
    const open = payments.filter(
      (payment) => payment.status === "EM_ABERTO" || payment.status === "PENDENTE"
    ).length;
    const overdue = payments.filter((payment) => payment.status === "ATRASADO").length;
    const exempt = payments.filter((payment) => payment.status === "ISENTO").length;
    return { total, paid, open, overdue, exempt };
  }, [payments]);

  const handleSavePayment = async () => {
    if (!editingPayment) {
      return;
    }
    setSavingPayment(true);
    try {
      const payload = {
        status: paymentForm.status,
        forma_pagamento: paymentForm.forma_pagamento,
        data_pagamento: paymentForm.data_pagamento || null,
      };
      const updated = await updateResource<PagamentoAlunoItem>(
        "/pagamentos-alunos",
        editingPayment.id,
        payload
      );
      setPayments((prev) =>
        prev.map((item) => (item.id === updated.id ? updated : item))
      );
      setEditingPaymentId(updated.id);
      pushToast({ title: "Pagamento atualizado", variant: "success" });
    } catch (err) {
      pushToast({
        title: "Erro ao atualizar pagamento",
        description: err instanceof Error ? err.message : "Erro ao atualizar pagamento",
        variant: "error",
      });
    } finally {
      setSavingPayment(false);
    }
  };

  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold text-brand-900">Pagamentos de alunos</h1>
        <p className="text-sm text-slate-500">
          Selecione um aluno para ver juros, status e forma de pagamento.
        </p>
      </header>

      {!hasToken && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          Autenticacao necessaria para acessar os dados. Clique em "Entrar".
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-[1fr_2fr]">
        <aside className="rounded-3xl border border-white/70 bg-white/90 p-4 shadow-soft">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="search"
              placeholder="Buscar aluno, CPF ou turma..."
              className="w-full rounded-full border border-white bg-white/80 py-2.5 pl-11 pr-4 text-sm text-slate-600 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-200"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <div className="mt-4 space-y-2">
            {loadingStudents && (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-white/70 px-4 py-3 text-sm text-slate-500">
                Carregando alunos...
              </div>
            )}
            {!loadingStudents && filteredStudents.length === 0 && (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-white/70 px-4 py-3 text-sm text-slate-500">
                Nenhum aluno encontrado.
              </div>
            )}
            {!loadingStudents &&
              filteredStudents.map((student) => {
                const active = student.id === selectedId;
                return (
                  <button
                    key={student.id}
                    type="button"
                    onClick={() => setSelectedId(student.id)}
                    className={`flex w-full items-center justify-between gap-3 rounded-2xl border px-4 py-3 text-left text-sm transition ${
                      active
                        ? "border-brand-500 bg-brand-600 text-white shadow-soft"
                        : "border-white/70 bg-white/80 text-slate-700 hover:border-brand-100"
                    }`}
                  >
                    <div>
                      <p className="text-sm font-semibold">{student.nome_completo}</p>
                      <p className={`text-xs ${active ? "text-white/70" : "text-slate-400"}`}>
                        {student.turma_nome ? `Turma: ${student.turma_nome}` : "Turma nao informada"}
                      </p>
                    </div>
                    <span
                      className={`rounded-full px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] ${
                        active ? "bg-white/20 text-white" : "bg-slate-100 text-slate-500"
                      }`}
                    >
                      {formatAlunoStatus(student.status)}
                    </span>
                  </button>
                );
              })}
          </div>
        </aside>

        <div className="rounded-3xl border border-white/70 bg-white/90 p-6 shadow-soft">
          {!selectedStudent && (
            <div className="rounded-2xl border border-dashed border-slate-200 bg-white/70 px-4 py-10 text-center text-sm text-slate-500">
              Selecione um aluno para ver os detalhes de pagamento.
            </div>
          )}

          {selectedStudent && (
            <div className="space-y-6">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold text-brand-900">
                    {selectedStudent.nome_completo}
                  </h2>
                  <p className="text-sm text-slate-500">
                    {selectedStudent.cpf ? `CPF: ${selectedStudent.cpf}` : "CPF nao informado"}
                    {selectedStudent.turma_nome ? ` | Turma: ${selectedStudent.turma_nome}` : ""}
                    {selectedStudent.plano_financeiro_nome
                      ? ` | Plano: ${selectedStudent.plano_financeiro_nome}`
                      : ""}
                  </p>
                </div>
                <span className={`rounded-full px-3 py-1 text-xs font-semibold ${getStatusClass(selectedStudent.status)}`}>
                  {formatAlunoStatus(selectedStudent.status)}
                </span>
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
                {[
                  { label: "Pagamentos", value: summary.total },
                  { label: "Em aberto", value: summary.open },
                  { label: "Feitos", value: summary.paid },
                  { label: "Atrasados", value: summary.overdue },
                  { label: "Isentos", value: summary.exempt },
                ].map((item) => (
                  <div
                    key={item.label}
                    className="rounded-2xl border border-white/70 bg-white/80 p-4 shadow-sm"
                  >
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                      {item.label}
                    </p>
                    <p className="mt-2 text-2xl font-semibold text-brand-900">
                      {formatNumber(item.value)}
                    </p>
                    <p className="text-xs text-slate-400">Resumo do aluno</p>
                  </div>
                ))}
              </div>

              {editingPayment && (
                <div className="rounded-2xl border border-white/70 bg-white/80 p-4">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <h3 className="text-sm font-semibold text-brand-900">
                        Editar pagamento
                      </h3>
                      <p className="text-xs text-slate-500">
                        Competencia {formatDate(editingPayment.competencia ?? undefined)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      {editingPayment.nf_pdf_url && (
                        <a
                          href={editingPayment.nf_pdf_url}
                          target="_blank"
                          rel="noreferrer"
                          className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 transition hover:border-emerald-300"
                        >
                          Baixar NF
                        </a>
                      )}
                      <button
                        type="button"
                        className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800"
                        onClick={() => setEditingPaymentId(null)}
                      >
                        Fechar
                      </button>
                    </div>
                  </div>

                  <div className="mt-4 grid gap-4 sm:grid-cols-3">
                    <label className="block">
                      <span className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                        Status
                      </span>
                      <select
                        className="w-full rounded-xl border border-slate-200 bg-white/80 px-3 py-2 text-sm text-slate-700 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-100"
                        value={paymentForm.status}
                        onChange={(event) =>
                          setPaymentForm((prev) => ({ ...prev, status: event.target.value }))
                        }
                      >
                        {statusOptions.map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    </label>

                    <label className="block">
                      <span className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                        Forma de pagamento
                      </span>
                      <select
                        className="w-full rounded-xl border border-slate-200 bg-white/80 px-3 py-2 text-sm text-slate-700 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-100"
                        value={paymentForm.forma_pagamento}
                        onChange={(event) =>
                          setPaymentForm((prev) => ({
                            ...prev,
                            forma_pagamento: event.target.value,
                          }))
                        }
                      >
                        {formaPagamentoOptions.map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                      </select>
                    </label>

                    <label className="block">
                      <span className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                        Data pagamento
                      </span>
                      <input
                        type="date"
                        className="w-full rounded-xl border border-slate-200 bg-white/80 px-3 py-2 text-sm text-slate-700 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-100"
                        value={paymentForm.data_pagamento}
                        onChange={(event) =>
                          setPaymentForm((prev) => ({
                            ...prev,
                            data_pagamento: event.target.value,
                          }))
                        }
                      />
                    </label>
                  </div>

                  <div className="mt-4 grid gap-4 sm:grid-cols-3 xl:grid-cols-6">
                    {[
                      { label: "Valor", value: formatMoney(editingPayment.valor) },
                      { label: "Desconto", value: formatMoney(editingPayment.desconto) },
                      { label: "Multa", value: formatMoney(editingPayment.multa) },
                      { label: "Juros", value: formatMoney(editingPayment.juros) },
                      { label: "Total", value: formatMoney(editingPayment.valor_total) },
                      { label: "Pago", value: formatMoney(editingPayment.valor_pago) },
                    ].map((item) => (
                      <div
                        key={item.label}
                        className="rounded-2xl border border-white/70 bg-white/70 p-3"
                      >
                        <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-400">
                          {item.label}
                        </p>
                        <p className="mt-1 text-sm font-semibold text-brand-900">
                          {item.value}
                        </p>
                      </div>
                    ))}
                  </div>

                  <div className="mt-4 flex flex-wrap justify-end gap-2">
                    <button
                      type="button"
                      className="rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800"
                      onClick={() => setEditingPaymentId(null)}
                      disabled={savingPayment}
                    >
                      Cancelar
                    </button>
                    <button
                      type="button"
                      className="rounded-full bg-brand-600 px-4 py-2 text-xs font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-70"
                      onClick={handleSavePayment}
                      disabled={savingPayment}
                    >
                      {savingPayment ? "Salvando..." : "Salvar"}
                    </button>
                  </div>
                </div>
              )}

              <div className="rounded-2xl border border-white/70 bg-white/80 p-4">
                <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
                  <h3 className="text-sm font-semibold text-brand-900">Historico de pagamentos</h3>
                  <span className="text-xs text-slate-400">
                    {payments.length} registro{payments.length === 1 ? "" : "s"}
                  </span>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full border-separate border-spacing-y-2 text-left text-sm">
                    <thead>
                      <tr className="text-xs uppercase tracking-[0.18em] text-slate-400">
                        <th className="px-3 py-2">Competencia</th>
                        <th className="px-3 py-2">Valor</th>
                        <th className="px-3 py-2">Desconto</th>
                        <th className="px-3 py-2">Juros (%)</th>
                        <th className="px-3 py-2">Total</th>
                        <th className="px-3 py-2">Status</th>
                        <th className="px-3 py-2">Forma</th>
                        <th className="px-3 py-2">Vencimento</th>
                        <th className="px-3 py-2">Pago em</th>
                        <th className="px-3 py-2">Registro</th>
                        <th className="px-3 py-2">Acoes</th>
                      </tr>
                    </thead>
                    <tbody>
                      {loadingPayments && (
                        <tr>
                          <td
                            className="px-3 py-4 text-center text-sm text-slate-500"
                            colSpan={11}
                          >
                            Carregando pagamentos...
                          </td>
                        </tr>
                      )}
                      {!loadingPayments && payments.length === 0 && (
                        <tr>
                          <td
                            className="px-3 py-4 text-center text-sm text-slate-500"
                            colSpan={11}
                          >
                            Nenhum pagamento registrado.
                          </td>
                        </tr>
                      )}
                      {!loadingPayments &&
                        payments.map((payment) => (
                          <tr
                            key={payment.id}
                            className="rounded-2xl bg-white shadow-sm"
                          >
                            <td className="px-3 py-3 text-slate-600">
                              {formatDate(payment.competencia ?? undefined)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {formatMoney(payment.valor)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {formatMoney(payment.desconto)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {getJurosPercent(payment)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {formatMoney(payment.valor_total)}
                            </td>
                            <td className="px-3 py-3">
                              <span
                                className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${getStatusClass(
                                  payment.status
                                )}`}
                              >
                                {formatPaymentStatus(payment.status)}
                              </span>
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {formatFormaPagamento(payment.forma_pagamento)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {formatDate(payment.data_vencimento ?? undefined)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {formatDate(payment.data_pagamento ?? undefined)}
                            </td>
                            <td className="px-3 py-3 text-slate-600">
                              {getRegistroTimestamp(payment)}
                            </td>
                            <td className="px-3 py-3">
                              <div className="flex items-center gap-2">
                                <button
                                  type="button"
                                  className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800"
                                  onClick={() => setEditingPaymentId(payment.id)}
                                >
                                  Editar
                                </button>
                                {payment.nf_pdf_url && (
                                  <a
                                    href={payment.nf_pdf_url}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 transition hover:border-emerald-300"
                                  >
                                    NF
                                  </a>
                                )}
                              </div>
                            </td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
