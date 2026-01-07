import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Pencil, Plus, RefreshCcw, Search, Trash2 } from "lucide-react";

import type { ResourceConfig, ResourceField } from "../data/resources";
import { useResourceData } from "../hooks/useResourceData";
import { formatBoolean, formatDate, formatNumber } from "../lib/format";
import { getStoredAccessToken } from "../lib/api";
import { ResourceForm } from "../components/ResourceForm";
import { useToast } from "../components/Toast";

type ResourcePageProps = {
  config: ResourceConfig;
};

function formatCell(value: unknown) {
  if (value === null || value === undefined || value === "") {
    return "--";
  }
  if (typeof value === "boolean") {
    return formatBoolean(value);
  }
  if (typeof value === "number") {
    return formatNumber(value);
  }
  if (typeof value === "string") {
    if (/^\d{4}-\d{2}-\d{2}/.test(value)) {
      return formatDate(value);
    }
    return value;
  }
  return String(value);
}

function buildInitialValues(
  fields: ResourceField[],
  item?: Record<string, unknown>
) {
  const values: Record<string, unknown> = {};
  fields.forEach((field) => {
    if (field.type === "password") {
      values[field.name] = "";
      return;
    }
    if (field.type === "boolean") {
      values[field.name] =
        item?.[field.name] ?? field.defaultValue ?? false;
      return;
    }
    if (field.type === "select" && field.multiple) {
      values[field.name] = Array.isArray(item?.[field.name])
        ? item?.[field.name]
        : (field.defaultValue as string[] | undefined) ?? [];
      return;
    }
    values[field.name] = item?.[field.name] ?? field.defaultValue ?? "";
  });
  return values;
}

export function ResourcePage({ config }: ResourcePageProps) {
  const {
    items,
    count,
    page,
    totalPages,
    search,
    setSearch,
    setPage,
    loading,
    error,
    refresh,
    createItem,
    updateItem,
    deleteItem,
  } = useResourceData(config);
  const { pushToast } = useToast();

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [editing, setEditing] = useState<Record<string, unknown> | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [searchInput, setSearchInput] = useState(search);

  useEffect(() => {
    setSearchInput(search);
  }, [search, config.key]);

  useEffect(() => {
    if (error) {
      pushToast({
        title: `Erro ao carregar ${config.title.toLowerCase()}`,
        description: error,
        variant: "error",
      });
    }
  }, [error, config.title, pushToast]);

  useEffect(() => {
    const handler = window.setTimeout(() => {
      setSearch(searchInput);
    }, 350);
    return () => window.clearTimeout(handler);
  }, [searchInput, setSearch]);

  const allowCreate = config.allowCreate !== false;
  const allowEdit = config.allowEdit !== false;
  const allowDelete = config.allowDelete !== false;
  const showActions = allowEdit || allowDelete;
  const hasToken = Boolean(getStoredAccessToken());

  const initialValues = useMemo(
    () => buildInitialValues(config.fields, editing ?? undefined),
    [config.fields, editing]
  );

  const handleOpenCreate = () => {
    setEditing(null);
    setDrawerOpen(true);
  };

  const handleEdit = (item: Record<string, unknown>) => {
    setEditing(item);
    setDrawerOpen(true);
  };

  const handleDelete = async (item: Record<string, unknown>) => {
    if (!allowDelete) {
      return;
    }
    const id = item.id as string | number | undefined;
    if (!id) {
      return;
    }
    const confirmed = window.confirm("Tem certeza que deseja remover este registro?");
    if (!confirmed) {
      return;
    }
    try {
      await deleteItem(id);
      pushToast({
        title: "Registro removido",
        variant: "success",
      });
    } catch (err) {
      pushToast({
        title: "Erro ao remover",
        description: err instanceof Error ? err.message : "Erro ao remover",
        variant: "error",
      });
    }
  };

  const handleSubmit = async (payload: Record<string, unknown>) => {
    setSubmitting(true);
    try {
      if (editing?.id) {
        await updateItem(editing.id as string | number, payload);
        pushToast({
          title: "Registro atualizado",
          variant: "success",
        });
      } else {
        await createItem(payload);
        pushToast({
          title: "Registro criado",
          variant: "success",
        });
      }
      setDrawerOpen(false);
    } catch (err) {
      pushToast({
        title: "Erro ao salvar",
        description: err instanceof Error ? err.message : "Erro ao salvar",
        variant: "error",
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="space-y-6">
      <header className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-brand-900">
              {config.title}
            </h1>
            <p className="text-sm text-slate-500">{config.description}</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 shadow-sm transition hover:border-brand-200 hover:text-brand-800"
              onClick={refresh}
            >
              <RefreshCcw className="h-4 w-4" />
              Atualizar
            </button>
            {allowCreate && (
              <button
                type="button"
                className="inline-flex items-center gap-2 rounded-full bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
                onClick={handleOpenCreate}
              >
                <Plus className="h-4 w-4" />
                Novo {config.singular}
              </button>
            )}
          </div>
        </div>

        {!hasToken && (
          <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
            Autenticacao necessaria para acessar os dados. Clique em{" "}
            <Link className="font-semibold underline" to="/login">
              Entrar
            </Link>
            .
          </div>
        )}

        {config.searchable !== false && (
          <div className="relative max-w-md">
            <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="search"
              placeholder="Buscar por nome, codigo ou detalhes..."
              className="w-full rounded-full border border-white bg-white/80 py-2.5 pl-11 pr-4 text-sm text-slate-600 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-200"
              value={searchInput}
              onChange={(event) => setSearchInput(event.target.value)}
            />
          </div>
        )}
      </header>

      <div className="rounded-3xl border border-white/70 bg-white/90 p-4 shadow-soft">
        <div className="overflow-x-auto">
          <table className="min-w-full border-separate border-spacing-y-3 text-left text-sm">
            <thead>
              <tr className="text-xs uppercase tracking-[0.18em] text-slate-400">
                {config.columns.map((column) => (
                  <th key={column.key} className="px-4 py-2">
                    {column.label}
                  </th>
                ))}
                {showActions && <th className="px-4 py-2">Acoes</th>}
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr>
                  <td
                    className="px-4 py-6 text-center text-sm text-slate-500"
                    colSpan={config.columns.length + (showActions ? 1 : 0)}
                  >
                    Carregando registros...
                  </td>
                </tr>
              )}
              {!loading && items.length === 0 && (
                <tr>
                  <td
                    className="px-4 py-6 text-center text-sm text-slate-500"
                    colSpan={config.columns.length + (showActions ? 1 : 0)}
                  >
                    Nenhum registro encontrado.
                  </td>
                </tr>
              )}
              {!loading &&
                items.map((item) => (
                  <tr
                    key={String(item.id ?? JSON.stringify(item))}
                    className="rounded-2xl bg-white shadow-sm"
                  >
                    {config.columns.map((column) => (
                      <td key={column.key} className="px-4 py-3 text-slate-600">
                        {formatCell(
                          column.value ? column.value(item) : item[column.key]
                        )}
                      </td>
                    ))}
                    {showActions && (
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          {allowEdit && (
                            <button
                              type="button"
                              className="inline-flex items-center gap-1 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800"
                              onClick={() => handleEdit(item)}
                            >
                              <Pencil className="h-3.5 w-3.5" />
                              Editar
                            </button>
                          )}
                          {allowDelete && (
                            <button
                              type="button"
                              className="inline-flex items-center gap-1 rounded-full border border-rose-200 bg-rose-50 px-3 py-1.5 text-xs font-semibold text-rose-600 transition hover:border-rose-300"
                              onClick={() => handleDelete(item)}
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                              Excluir
                            </button>
                          )}
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
            </tbody>
          </table>
        </div>

        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-sm text-slate-500">
          <span>
            {count} registro{count === 1 ? "" : "s"}
          </span>
          <div className="flex items-center gap-2">
            <button
              type="button"
              className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800 disabled:cursor-not-allowed disabled:opacity-60"
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page <= 1}
            >
              Anterior
            </button>
            <span>
              Pagina {page} de {totalPages}
            </span>
            <button
              type="button"
              className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800 disabled:cursor-not-allowed disabled:opacity-60"
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page >= totalPages}
            >
              Proxima
            </button>
          </div>
        </div>
      </div>

      {drawerOpen && (
        <ResourceForm
          title={editing ? `Editar ${config.singular}` : `Novo ${config.singular}`}
          description={
            editing
              ? "Atualize os dados e salve as alteracoes."
              : "Preencha os campos para criar um novo registro."
          }
          fields={config.fields}
          initialValues={initialValues}
          submitting={submitting}
          onSubmit={handleSubmit}
          onCancel={() => setDrawerOpen(false)}
        />
      )}
    </section>
  );
}

