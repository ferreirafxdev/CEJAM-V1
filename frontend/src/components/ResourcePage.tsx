import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import { apiRequest } from "../lib/api";
import { ResourceConfig } from "../resources";
import DataTable from "./DataTable";
import FilterPanel from "./FilterPanel";
import ResourceForm from "./ResourceForm";

type ResourcePageProps = {
  resource: ResourceConfig;
};

export default function ResourcePage({ resource }: ResourcePageProps) {
  const [selected, setSelected] = useState<Record<string, any> | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [filterText, setFilterText] = useState("");
  const [filters, setFilters] = useState<Record<string, string>>({});

  useEffect(() => {
    const next: Record<string, string> = {};
    resource.filters?.forEach((fieldName) => {
      next[fieldName] = "";
    });
    setFilters(next);
  }, [resource]);

  const listQuery = useQuery({
    queryKey: ["resource", resource.key],
    queryFn: async () => {
      const data = await apiRequest<any>(`${resource.endpoint}?page_size=200`);
      return Array.isArray(data) ? data : data.results || [];
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload: Record<string, any>) =>
      apiRequest(resource.endpoint, {
        method: "POST",
        body: JSON.stringify(payload),
      }),
    onSuccess: () => {
      listQuery.refetch();
      setDrawerOpen(false);
      setSelected(null);
    },
  });

  const updateMutation = useMutation({
    mutationFn: (payload: Record<string, any>) => {
      if (!selected) throw new Error("Sem registro selecionado.");
      return apiRequest(`${resource.endpoint}${selected.id}/`, {
        method: "PATCH",
        body: JSON.stringify(payload),
      });
    },
    onSuccess: () => {
      listQuery.refetch();
      setDrawerOpen(false);
      setSelected(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (item: Record<string, any>) =>
      apiRequest(`${resource.endpoint}${item.id}/`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      listQuery.refetch();
      setDrawerOpen(false);
      setSelected(null);
    },
  });

  const actionMutation = useMutation({
    mutationFn: async (actionKey: string) => {
      if (!selected) throw new Error("Sem registro selecionado.");
      if (resource.key === "contratos" && actionKey === "gerar_pdf") {
        return apiRequest(`${resource.endpoint}${selected.id}/gerar_pdf/`, {
          method: "POST",
        });
      }
      throw new Error("Acao nao suportada.");
    },
    onSuccess: () => {
      listQuery.refetch();
    },
  });

  const items = listQuery.data || [];
  const filtered = useMemo(() => {
    let data = items;
    if (filterText) {
      const term = filterText.toLowerCase();
      data = data.filter((item: Record<string, any>) =>
        resource.columns.some((key) => String(item[key] || "").toLowerCase().includes(term))
      );
    }
    if (resource.filters && resource.filters.length > 0) {
      data = data.filter((item: Record<string, any>) =>
        resource.filters!.every((fieldName) => {
          const filterValue = filters[fieldName];
          if (!filterValue) return true;
          const itemValue = item[fieldName];
          if (itemValue === null || itemValue === undefined) return false;
          if (Array.isArray(itemValue)) {
            return itemValue.map(String).includes(filterValue);
          }
          return String(itemValue) === filterValue;
        })
      );
    }
    return data;
  }, [filterText, filters, items, resource.columns, resource.filters]);

  const isLocked = selected ? resource.lockWhen?.(selected) ?? false : false;

  const handleOpenCreate = () => {
    setSelected(null);
    setDrawerOpen(true);
  };

  const handleSelect = (item: Record<string, any>) => {
    setSelected(item);
    setDrawerOpen(true);
  };

  const handleSubmit = (payload: Record<string, any>) => {
    if (selected) {
      updateMutation.mutate(payload);
    } else {
      createMutation.mutate(payload);
    }
  };

  return (
    <section className="resource fade-in">
      <div className="resource__header">
        <div>
          <h3>{resource.label}</h3>
          <p>{resource.description}</p>
        </div>
      </div>

      <div className="resource__actions">
        <input
          className="input-search"
          placeholder="Buscar..."
          value={filterText}
          onChange={(event) => setFilterText(event.target.value)}
        />
        {!resource.readOnly && (
          <button className="btn btn-primary" onClick={handleOpenCreate}>
            Adicionar
          </button>
        )}
      </div>

      {actionMutation.error instanceof Error && (
        <div className="alert alert-error">{actionMutation.error.message}</div>
      )}

      <div className="changelist">
        <div className="changelist__main">
          {listQuery.isLoading ? (
            <div className="card">Carregando...</div>
          ) : listQuery.error instanceof Error ? (
            <div className="alert alert-error">{listQuery.error.message}</div>
          ) : (
            <DataTable columns={resource.columns} items={filtered} onSelect={handleSelect} />
          )}
        </div>
        <FilterPanel resource={resource} filters={filters} onChange={setFilters} />
      </div>

      <ResourceForm
        resource={resource}
        item={selected}
        open={drawerOpen}
        locked={isLocked}
        onClose={() => setDrawerOpen(false)}
        onSubmit={handleSubmit}
        onDelete={(item) => deleteMutation.mutate(item)}
        onAction={(actionKey) => actionMutation.mutate(actionKey)}
        submitting={createMutation.isPending || updateMutation.isPending}
        actionLoading={actionMutation.isPending}
      />
    </section>
  );
}
