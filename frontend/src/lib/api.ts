export type DashboardStats = {
  total_alunos: number;
  turmas_ativas: number;
  turnos_ativos: number;
  contratos_emitidos: number;
  receita_mes: string;
};

export type DashboardActivity = {
  type: string;
  message: string;
  timestamp: string;
};

export type DashboardResponse = {
  stats: DashboardStats;
  recent_activity: DashboardActivity[];
};

export type MeResponse = {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_superuser: boolean;
  groups: string[];
  can_access_financeiro: boolean;
};

export type AuthTokens = {
  access: string;
  refresh: string;
};

const ACCESS_TOKEN_KEY = "cejam.accessToken";
const REFRESH_TOKEN_KEY = "cejam.refreshToken";

const baseUrl = (import.meta.env.VITE_API_URL ?? "").trim();
const apiPrefix = (import.meta.env.VITE_API_PREFIX ?? "/api").trim();

function buildUrl(path: string) {
  const normalizedBase = baseUrl.replace(/\/$/, "");
  const normalizedPrefix = apiPrefix.startsWith("/") ? apiPrefix : `/${apiPrefix}`;
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${normalizedBase}${normalizedPrefix}${normalizedPath}`;
}

function getAccessToken() {
  return (
    localStorage.getItem(ACCESS_TOKEN_KEY) ||
    (import.meta.env.VITE_ACCESS_TOKEN ?? "")
  ).trim();
}

export function getStoredAccessToken() {
  return getAccessToken();
}

function normalizeEndpoint(endpoint: string) {
  const withSlash = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  return withSlash.endsWith("/") ? withSlash : `${withSlash}/`;
}

function buildQuery(params?: Record<string, string | number | boolean | null | undefined>) {
  if (!params) {
    return "";
  }
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") {
      return;
    }
    searchParams.set(key, String(value));
  });
  const query = searchParams.toString();
  return query ? `?${query}` : "";
}

export type ApiListResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export function setAuthTokens(access: string, refresh?: string) {
  if (access) {
    localStorage.setItem(ACCESS_TOKEN_KEY, access);
  }
  if (refresh) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  }
}

export function clearAuthTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

async function parseError(response: Response) {
  try {
    const data = await response.json();
    if (typeof data === "string") {
      return data;
    }
    if (data?.detail) {
      return data.detail as string;
    }
    return JSON.stringify(data);
  } catch {
    return `Request failed (${response.status})`;
  }
}

type ApiOptions = Omit<RequestInit, "body"> & { body?: unknown };

async function apiFetch<T>(path: string, options: ApiOptions = {}) {
  const headers = new Headers(options.headers ?? {});
  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let body = options.body;
  if (body && typeof body === "object" && !(body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
    body = JSON.stringify(body);
  }

  const response = await fetch(buildUrl(path), {
    ...options,
    headers,
    body: body as BodyInit | null | undefined,
  });

  if (!response.ok) {
    const message = await parseError(response);
    throw new Error(message);
  }

  if (response.status === 204) {
    return null as T;
  }

  return (await response.json()) as T;
}

export function getDashboard() {
  return apiFetch<DashboardResponse>("/dashboard/");
}

export function getMe() {
  return apiFetch<MeResponse>("/auth/me/");
}

export async function login(username: string, password: string) {
  const tokens = await apiFetch<AuthTokens>("/auth/token/", {
    method: "POST",
    body: { username, password },
  });
  setAuthTokens(tokens.access, tokens.refresh);
  return tokens;
}

export function listResource<T>(
  endpoint: string,
  params?: Record<string, string | number | boolean | null | undefined>
) {
  const normalized = normalizeEndpoint(endpoint);
  return apiFetch<ApiListResponse<T>>(`${normalized}${buildQuery(params)}`);
}

export function createResource<T>(endpoint: string, payload: unknown) {
  const normalized = normalizeEndpoint(endpoint);
  return apiFetch<T>(normalized, { method: "POST", body: payload });
}

export function updateResource<T>(
  endpoint: string,
  id: string | number,
  payload: unknown
) {
  const normalized = normalizeEndpoint(endpoint);
  return apiFetch<T>(`${normalized}${id}/`, { method: "PATCH", body: payload });
}

export function deleteResource(endpoint: string, id: string | number) {
  const normalized = normalizeEndpoint(endpoint);
  return apiFetch<void>(`${normalized}${id}/`, { method: "DELETE" });
}
