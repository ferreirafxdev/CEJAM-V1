import type { LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";

type QuickAccessCardProps = {
  title: string;
  description: string;
  href: string;
  icon: LucideIcon;
};

export function QuickAccessCard({
  title,
  description,
  href,
  icon: Icon,
}: QuickAccessCardProps) {
  return (
    <Link
      to={href}
      className="group flex h-full flex-col gap-4 rounded-2xl border border-white/70 bg-white/90 p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-brand-100 hover:shadow-soft"
    >
      <div className="flex items-center justify-between">
        <div className="rounded-xl bg-brand-50 p-2 text-brand-600 transition group-hover:bg-brand-600 group-hover:text-white">
          <Icon className="h-5 w-5" />
        </div>
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          Acesso rapido
        </span>
      </div>
      <div className="space-y-1">
        <p className="text-lg font-semibold text-brand-900">{title}</p>
        <p className="text-sm text-slate-500">{description}</p>
      </div>
    </Link>
  );
}
