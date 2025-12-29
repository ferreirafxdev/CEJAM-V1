const STORAGE_KEY = "cejamsys.auth";

export type Tokens = {
  access: string;
  refresh: string;
};

export const API_BASE_URL =
  import.meta.env.VITE_API_URL?.replace(/\/$/, "") || "http://localhost:8000/api";

export function getTokens(): Tokens | null {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as Tokens;
  } catch {
    return null;
  }
}

export function setTokens(tokens: Tokens) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens));
}

export function clearTokens() {
  localStorage.removeItem(STORAGE_KEY);
}

async function refreshAccessToken(refresh: string): Promise<string | null> {
  const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });
  if (!response.ok) return null;
  const data = (await response.json()) as { access: string };
  return data.access;
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
  retry = true
): Promise<Response> {
  const tokens = getTokens();
  const headers = new Headers(options.headers || {});

  if (!headers.has("Content-Type") && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  if (tokens?.access) {
    headers.set("Authorization", `Bearer ${tokens.access}`);
  }

  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers,
    });
  } catch (error) {
    throw new Error(
      `Nao foi possivel conectar ao backend em ${API_BASE_URL}. Verifique se o servidor esta ativo.`
    );
  }

  if (response.status === 401 && retry && tokens?.refresh) {
    const newAccess = await refreshAccessToken(tokens.refresh);
    if (newAccess) {
      setTokens({ access: newAccess, refresh: tokens.refresh });
      return apiFetch(path, options, false);
    }
    clearTokens();
  }

  return response;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await apiFetch(path, options);
  if (response.status === 204) {
    return {} as T;
  }
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    const message =
      data?.detail ||
      data?.error ||
      `Erro ${response.status} ao acessar ${path}`;
    throw new Error(message);
  }
  return data as T;
}
