import { Bell, LogIn, LogOut, Menu, Search } from "lucide-react";
import { Link } from "react-router-dom";

import type { MeResponse } from "../lib/api";
import { clearAuthTokens } from "../lib/api";
import type { MeStatus } from "../hooks/useMe";

type HeaderProps = {
  user: MeResponse | null;
  status: MeStatus;
  onOpenSidebar: () => void;
};

export function Header({ user, status, onOpenSidebar }: HeaderProps) {
  const name =
    user?.first_name || user?.last_name
      ? `${user.first_name} ${user.last_name}`.trim()
      : user?.username || "admin";
  const role = user?.is_superuser
    ? "Administrador"
    : user?.groups?.[0] || "Usuario";

  const statusLabel =
    status === "ready"
      ? "API online"
      : status === "loading"
        ? "Conectando..."
        : "Sem autenticacao";
  const statusClass =
    status === "ready"
      ? "bg-emerald-100 text-emerald-700"
      : status === "loading"
        ? "bg-amber-100 text-amber-700"
        : "bg-rose-100 text-rose-700";

  const handleLogout = () => {
    clearAuthTokens();
    window.location.href = "/login";
  };

  return (
    <header className="sticky top-0 z-20 border-b border-white/40 bg-white/70 backdrop-blur-xl">
      <div className="flex items-center justify-between gap-4 px-6 py-4 sm:px-8">
        <div className="flex flex-1 items-center gap-3">
          <button
            type="button"
            className="rounded-xl border border-slate-200 bg-white/90 p-2 text-slate-600 shadow-sm transition hover:border-brand-200 hover:text-brand-800 lg:hidden"
            onClick={onOpenSidebar}
            aria-label="Abrir menu"
          >
            <Menu className="h-4 w-4" />
          </button>
          <div className="relative hidden w-full max-w-md lg:block">
            <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="search"
              placeholder="Buscar alunos, turmas, contratos..."
              className="w-full rounded-full border border-white bg-white/80 py-2.5 pl-11 pr-4 text-sm text-slate-600 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-200"
            />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span
            className={`hidden items-center rounded-full px-3 py-1 text-xs font-semibold sm:inline-flex ${statusClass}`}
          >
            {statusLabel}
          </span>
          <button
            type="button"
            className="relative rounded-full border border-white bg-white/80 p-2 text-slate-600 shadow-sm transition hover:text-brand-800"
            aria-label="Notificacoes"
          >
            <Bell className="h-5 w-5" />
            <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-brand-600" />
          </button>
          {status === "ready" ? (
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white/80 px-3 py-2 text-xs font-semibold text-slate-600 shadow-sm transition hover:border-brand-200 hover:text-brand-800"
              onClick={handleLogout}
            >
              <LogOut className="h-4 w-4" />
              Sair
            </button>
          ) : (
            <Link
              to="/login"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white/80 px-3 py-2 text-xs font-semibold text-slate-600 shadow-sm transition hover:border-brand-200 hover:text-brand-800"
            >
              <LogIn className="h-4 w-4" />
              Entrar
            </Link>
          )}
          <div className="flex items-center gap-3 rounded-full border border-white bg-white/80 px-2 py-1.5 shadow-sm">
            <div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-brand-600 to-accent-500 text-sm font-semibold text-white">
              {name.slice(0, 1).toUpperCase()}
            </div>
            <div className="hidden text-left leading-tight sm:block">
              <p className="text-sm font-semibold text-slate-700">{name}</p>
              <p className="text-xs text-slate-500">{role}</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
