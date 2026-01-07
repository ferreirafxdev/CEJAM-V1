import { useCallback, useEffect, useState } from "react";

import { listResource } from "../lib/api";
import type { ResourceOptionSource, SelectOption } from "../data/resources";

const optionsCache = new Map<string, SelectOption[]>();

type OptionsState = {
  options: SelectOption[];
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
};

export function useResourceOptions(resource?: ResourceOptionSource): OptionsState {
  const [options, setOptions] = useState<SelectOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const cacheKey = resource
    ? `${resource.endpoint}|${resource.labelKey}|${resource.valueKey ?? "id"}`
    : "";

  const fetchOptions = useCallback(async () => {
    if (!resource) {
      setOptions([]);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await listResource<Record<string, unknown>>(resource.endpoint);
      const labelKey = resource.labelKey;
      const valueKey = resource.valueKey ?? "id";
      const mapped = response.results
        .map((item) => ({
          value: item[valueKey] as string | number,
          label: String(item[labelKey] ?? item[valueKey] ?? ""),
        }))
        .filter((item) => item.label !== "")
        .sort((a, b) => a.label.localeCompare(b.label, "pt-BR"));

      optionsCache.set(cacheKey, mapped);
      setOptions(mapped);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Erro ao carregar opcoes";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [cacheKey, resource]);

  useEffect(() => {
    if (!resource) {
      return;
    }
    const cached = optionsCache.get(cacheKey);
    if (cached) {
      setOptions(cached);
      setLoading(false);
      return;
    }
    fetchOptions();
  }, [cacheKey, fetchOptions, resource]);

  return { options, loading, error, refresh: fetchOptions };
}
