import type { DashboardActivity } from "../lib/api";

type ActivityListProps = {
  items: DashboardActivity[];
  loading?: boolean;
};

const typeStyles: Record<string, string> = {
  aluno: "bg-blue-100 text-blue-700",
  pagamento: "bg-emerald-100 text-emerald-700",
  contrato: "bg-amber-100 text-amber-700",
  turma: "bg-indigo-100 text-indigo-700",
};

function formatTimestamp(timestamp: string) {
  const date = new Date(timestamp);
  const datePart = date.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
  const timePart = date.toLocaleTimeString("pt-BR", {
    hour: "2-digit",
    minute: "2-digit",
  });
  return `${datePart} ${timePart}`;
}

export function ActivityList({ items, loading }: ActivityListProps) {
  if (loading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 3 }).map((_, index) => (
          <div
            key={`skeleton-${index}`}
            className="h-12 animate-pulse rounded-xl bg-slate-100"
          />
        ))}
      </div>
    );
  }

  if (!items.length) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-200 bg-white/80 p-6 text-center text-sm text-slate-500">
        Nenhuma atividade recente.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((activity, index) => (
        <div
          key={`${activity.type}-${index}`}
          className="flex items-center justify-between gap-4 rounded-2xl border border-white/70 bg-white/90 px-4 py-3 shadow-sm"
        >
          <div className="space-y-1">
            <span
              className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                typeStyles[activity.type] || "bg-slate-100 text-slate-600"
              }`}
            >
              {activity.type.toUpperCase()}
            </span>
            <p className="text-sm font-medium text-slate-700">
              {activity.message}
            </p>
          </div>
          <span className="text-xs text-slate-400">
            {formatTimestamp(activity.timestamp)}
          </span>
        </div>
      ))}
    </div>
  );
}
