import { useCallback, useEffect, useMemo, useState } from "react";

import { createResource, deleteResource, listResource, updateResource } from "../lib/api";
import type { ApiListResponse } from "../lib/api";
import type { ResourceConfig } from "../data/resources";

const DEFAULT_PAGE_SIZE = 50;

type ResourceState<T> = {
  items: T[];
  count: number;
  page: number;
  totalPages: number;
  search: string;
  setSearch: (value: string) => void;
  setPage: (value: number) => void;
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
  createItem: (payload: Record<string, unknown>) => Promise<void>;
  updateItem: (id: string | number, payload: Record<string, unknown>) => Promise<void>;
  deleteItem: (id: string | number) => Promise<void>;
};

function resolveErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message;
  }
  return "Erro ao carregar dados";
}

export function useResourceData<T extends Record<string, unknown>>(
  config: ResourceConfig
): ResourceState<T> {
  const [items, setItems] = useState<T[]>([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response: ApiListResponse<T> = await listResource<T>(config.endpoint, {
        page,
        search: config.searchable === false ? undefined : search,
      });
      setItems(response.results ?? []);
      setCount(response.count ?? 0);
    } catch (err) {
      setError(resolveErrorMessage(err));
      setItems([]);
      setCount(0);
    } finally {
      setLoading(false);
    }
  }, [config.endpoint, config.searchable, page, search]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    setPage(1);
  }, [search, config.key]);

  const totalPages = useMemo(() => {
    const total = Math.ceil(count / DEFAULT_PAGE_SIZE);
    return total > 0 ? total : 1;
  }, [count]);

  const createItem = useCallback(
    async (payload: Record<string, unknown>) => {
      await createResource(config.endpoint, payload);
      await fetchData();
    },
    [config.endpoint, fetchData]
  );

  const updateItem = useCallback(
    async (id: string | number, payload: Record<string, unknown>) => {
      await updateResource(config.endpoint, id, payload);
      await fetchData();
    },
    [config.endpoint, fetchData]
  );

  const deleteItem = useCallback(
    async (id: string | number) => {
      await deleteResource(config.endpoint, id);
      await fetchData();
    },
    [config.endpoint, fetchData]
  );

  return {
    items,
    count,
    page,
    totalPages,
    search,
    setSearch,
    setPage,
    loading,
    error,
    refresh: fetchData,
    createItem,
    updateItem,
    deleteItem,
  };
}
