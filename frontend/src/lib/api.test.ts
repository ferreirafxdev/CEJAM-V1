import { beforeEach, describe, expect, it, vi } from "vitest";

import { clearAuthTokens, getDashboard, setAuthTokens } from "./api";

describe("api", () => {
  beforeEach(() => {
    clearAuthTokens();
    vi.restoreAllMocks();
  });

  it("adds Authorization header when token is set", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        stats: {
          total_alunos: 1,
          turmas_ativas: 1,
          turnos_ativos: 1,
          contratos_emitidos: 1,
          receita_mes: "0.00",
        },
        recent_activity: [],
      }),
    });

    vi.stubGlobal("fetch", fetchMock as unknown as typeof fetch);
    setAuthTokens("token-value", "refresh-value");

    await getDashboard();

    const [, options] = fetchMock.mock.calls[0];
    const headers = new Headers(options?.headers);
    expect(headers.get("Authorization")).toBe("Bearer token-value");
  });
});
