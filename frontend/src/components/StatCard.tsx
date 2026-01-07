import type { LucideIcon } from "lucide-react";

type StatCardProps = {
  title: string;
  value: string | number;
  icon: LucideIcon;
  delta?: string;
  loading?: boolean;
};

export function StatCard({ title, value, icon: Icon, delta, loading }: StatCardProps) {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-white/70 bg-white/90 p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-soft">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{title}</p>
        <div className="rounded-xl bg-brand-50 p-2 text-brand-600">
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div className="flex items-baseline gap-3">
        {loading ? (
          <div className="h-8 w-20 animate-pulse rounded-lg bg-slate-200" />
        ) : (
          <p className="text-2xl font-semibold text-brand-900 sm:text-3xl">
            {value}
          </p>
        )}
        {delta && !loading && (
          <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-700">
            {delta}
          </span>
        )}
      </div>
    </div>
  );
}
