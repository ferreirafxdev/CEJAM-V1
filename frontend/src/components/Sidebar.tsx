import { NavLink } from "react-router-dom";
import { ChevronLeft, ChevronRight, X } from "lucide-react";

import { navigationSections } from "../data/navigation";

type SidebarProps = {
  collapsed: boolean;
  onToggleCollapse: () => void;
  mobileOpen: boolean;
  onCloseMobile: () => void;
};

export function Sidebar({
  collapsed,
  onToggleCollapse,
  mobileOpen,
  onCloseMobile,
}: SidebarProps) {
  const widthClass = collapsed ? "lg:w-20" : "lg:w-64";
  const translateClass = mobileOpen ? "translate-x-0" : "-translate-x-full";

  return (
    <>
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-slate-900/40 backdrop-blur-sm lg:hidden"
          onClick={onCloseMobile}
        />
      )}
      <aside
        className={`fixed left-0 top-0 z-40 h-screen w-64 border-r border-white/50 bg-white/85 shadow-soft backdrop-blur-xl transition-all lg:translate-x-0 ${widthClass} ${translateClass}`}
      >
        <div className="flex items-center justify-between px-4 py-5">
          <div className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-600 text-lg font-bold text-white">
              C
            </div>
            {!collapsed && (
              <div className="leading-tight">
                <p className="text-sm font-semibold text-brand-900">
                  CEJAM - Painel Escolar
                </p>
                <p className="text-xs text-slate-500">Gestao Educacional</p>
              </div>
            )}
          </div>
          <button
            type="button"
            className="rounded-full p-2 text-slate-500 transition hover:bg-brand-50 hover:text-brand-800 lg:hidden"
            onClick={onCloseMobile}
            aria-label="Fechar menu"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <nav className="flex h-[calc(100%-140px)] flex-col gap-6 overflow-y-auto px-3 pb-6">
          {navigationSections.map((section) => (
            <div key={section.label} className="space-y-2">
              {!collapsed && (
                <p className="px-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">
                  {section.label}
                </p>
              )}
              <div className="space-y-1">
                {section.items.map((item) => (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    title={collapsed ? item.label : undefined}
                    className={({ isActive }) =>
                      `group flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition ${
                        collapsed ? "justify-center" : ""
                      } ${
                        isActive
                          ? "bg-brand-600 text-white shadow-soft"
                          : "text-slate-600 hover:bg-brand-50 hover:text-brand-800"
                      }`
                    }
                  >
                    {({ isActive }) => (
                      <>
                        <item.icon
                          className={`h-5 w-5 transition ${
                            isActive
                              ? "text-white"
                              : "text-brand-600 group-hover:text-brand-800"
                          }`}
                        />
                        {!collapsed && <span>{item.label}</span>}
                      </>
                    )}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="px-3 pb-6">
          <button
            type="button"
            onClick={onToggleCollapse}
            className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/80 px-3 py-2 text-sm font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800"
          >
            {collapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
            {!collapsed && <span>Recolher menu</span>}
          </button>
        </div>
      </aside>
    </>
  );
}
