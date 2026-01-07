import { useCallback, useEffect, useState } from "react";

import { getDashboard } from "../lib/api";
import type { DashboardResponse } from "../lib/api";

export function useDashboardData() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getDashboard();
      setData(response);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Erro desconhecido";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return {
    data,
    error,
    loading,
    refresh: fetchDashboard,
  };
}
