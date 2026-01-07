import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { KeyRound, User } from "lucide-react";

import { login } from "../lib/api";
import { useToast } from "../components/Toast";

export function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { pushToast } = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    try {
      await login(username, password);
      pushToast({
        title: "Autenticacao concluida",
        description: "Acesso liberado ao painel.",
        variant: "success",
      });
      navigate("/");
    } catch (err) {
      pushToast({
        title: "Falha no login",
        description: err instanceof Error ? err.message : "Erro ao autenticar",
        variant: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-50 via-white to-brand-50">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-6 py-10">
        <div className="grid w-full max-w-4xl gap-10 lg:grid-cols-[1.1fr_1fr]">
          <div className="hidden flex-col justify-between rounded-3xl bg-brand-900 p-8 text-white shadow-soft lg:flex">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-white/60">
                CEJAM
              </p>
              <h1 className="mt-3 text-3xl font-semibold">
                Painel Escolar integrado
              </h1>
              <p className="mt-4 text-sm text-white/70">
                Centralize matriculas, contratos e seguranca em um unico lugar.
              </p>
            </div>
            <div className="space-y-2 text-sm text-white/70">
              <p>API: `VITE_API_URL`</p>
              <p>Autenticacao: JWT via /api/auth/token/</p>
            </div>
          </div>

          <div className="rounded-3xl border border-white/70 bg-white/90 p-8 shadow-soft">
            <div className="space-y-2">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-brand-600">
                Acesso
              </p>
              <h2 className="text-2xl font-semibold text-brand-900">
                Entrar no painel
              </h2>
              <p className="text-sm text-slate-500">
                Use seu usuario administrativo para continuar.
              </p>
            </div>

            <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
              <label className="block">
                <span className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Usuario
                </span>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                  <input
                    type="text"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    className="w-full rounded-xl border border-slate-200 bg-white/80 py-2.5 pl-10 pr-3 text-sm text-slate-700 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-100"
                    placeholder="Digite seu usuario"
                    required
                  />
                </div>
              </label>

              <label className="block">
                <span className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Senha
                </span>
                <div className="relative">
                  <KeyRound className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                  <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    className="w-full rounded-xl border border-slate-200 bg-white/80 py-2.5 pl-10 pr-3 text-sm text-slate-700 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-100"
                    placeholder="Sua senha"
                    required
                  />
                </div>
              </label>

              <button
                type="submit"
                className="w-full rounded-full bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-70"
                disabled={loading}
              >
                {loading ? "Autenticando..." : "Entrar"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
