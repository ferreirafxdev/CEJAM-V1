import { useCallback, useEffect, useState } from "react";

import { getMe } from "../lib/api";
import type { MeResponse } from "../lib/api";

export type MeStatus = "loading" | "ready" | "error";

export function useMe() {
  const [user, setUser] = useState<MeResponse | null>(null);
  const [status, setStatus] = useState<MeStatus>("loading");

  const fetchMe = useCallback(async () => {
    setStatus("loading");
    try {
      const response = await getMe();
      setUser(response);
      setStatus("ready");
    } catch {
      setUser(null);
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    fetchMe();
  }, [fetchMe]);

  return { user, status, refresh: fetchMe };
}
