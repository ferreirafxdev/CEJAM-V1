import { useQuery } from "@tanstack/react-query";

import { apiRequest } from "./api";
import { Option, resourceMap } from "../resources";

function inferOptionLabel(item: Record<string, any>) {
  return (
    item.nome_fantasia ||
    item.nome_completo ||
    item.nome ||
    item.username ||
    item.razao_social ||
    item.id
  );
}

export function useResourceOptions(resourceKey?: string) {
  return useQuery({
    queryKey: ["options", resourceKey],
    enabled: !!resourceKey,
    queryFn: async () => {
      if (!resourceKey) return [] as Option[];
      const resource = resourceMap.get(resourceKey);
      if (!resource) return [] as Option[];
      const data = await apiRequest<any>(`${resource.endpoint}?page_size=500`);
      const items = Array.isArray(data) ? data : data.results || [];
      return items.map((item: Record<string, any>) => ({
        value: item.id,
        label: item[resource.optionLabel || "name"] || inferOptionLabel(item),
      }));
    },
  });
}
