import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

import { apiRequest, clearTokens, getTokens, setTokens } from "../lib/api";

type User = {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_superuser: boolean;
  groups: string[];
};

type AuthContextValue = {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

async function fetchMe() {
  return apiRequest<User>("/auth/me/");
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const tokens = getTokens();
    if (!tokens) {
      setLoading(false);
      return;
    }
    fetchMe()
      .then((data) => setUser(data))
      .catch(() => {
        clearTokens();
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (username: string, password: string) => {
    const tokens = await apiRequest<{ access: string; refresh: string }>("/auth/token/", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    setTokens(tokens);
    const me = await fetchMe();
    setUser(me);
  };

  const logout = () => {
    clearTokens();
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      loading,
      login,
      logout,
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return ctx;
}
