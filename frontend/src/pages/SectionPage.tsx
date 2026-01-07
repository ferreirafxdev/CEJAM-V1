import { Link } from "react-router-dom";

import type { SectionConfig } from "../data/resources";

type SectionPageProps = {
  config: SectionConfig;
};

export function SectionPage({ config }: SectionPageProps) {
  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold text-brand-900">
          {config.title}
        </h1>
        <p className="text-sm text-slate-500">{config.description}</p>
      </header>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {config.items.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className="group flex flex-col gap-3 rounded-2xl border border-white/70 bg-white/90 p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-brand-100 hover:shadow-soft"
          >
            <div className="flex items-center justify-between">
              <div className="rounded-xl bg-brand-50 p-2 text-brand-600 transition group-hover:bg-brand-600 group-hover:text-white">
                <item.icon className="h-5 w-5" />
              </div>
              <span className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                Acesso
              </span>
            </div>
            <div>
              <p className="text-lg font-semibold text-brand-900">{item.label}</p>
              <p className="text-sm text-slate-500">{item.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
