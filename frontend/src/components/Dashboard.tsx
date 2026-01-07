import { Clock, FileCheck, GraduationCap, Users, UsersRound } from "lucide-react";
import { useEffect, useMemo, useRef } from "react";

import { useDashboardData } from "../hooks/useDashboardData";
import { useMe } from "../hooks/useMe";
import { formatNumber } from "../lib/format";
import { ActivityList } from "./ActivityList";
import { HeroBanner } from "./HeroBanner";
import { QuickAccessCard } from "./QuickAccessCard";
import { StatCard } from "./StatCard";
import { useToast } from "./Toast";

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Bom dia";
  if (hour < 18) return "Boa tarde";
  return "Boa noite";
}

export function Dashboard() {
  const { data, loading, error } = useDashboardData();
  const { user } = useMe();
  const { pushToast } = useToast();
  const lastError = useRef<string | null>(null);

  useEffect(() => {
    if (error && error !== lastError.current) {
      pushToast({
        title: "Erro ao carregar dashboard",
        description: error,
        variant: "error",
      });
      lastError.current = error;
    }
  }, [error, pushToast]);

  const stats = data?.stats;
  const name =
    user && (user.first_name || user.last_name)
      ? `${user.first_name} ${user.last_name}`.trim()
      : user?.username || "admin";

  const kpis = useMemo(
    () => [
      {
        title: "Total de Alunos",
        value: formatNumber(stats?.total_alunos),
        delta: "+2%",
        icon: Users,
      },
      {
        title: "Turmas Ativas",
        value: formatNumber(stats?.turmas_ativas),
        delta: "+1%",
        icon: UsersRound,
      },
      {
        title: "Turnos",
        value: formatNumber(stats?.turnos_ativos),
        delta: "+0%",
        icon: Clock,
      },
      {
        title: "Contratos Emitidos",
        value: formatNumber(stats?.contratos_emitidos),
        delta: "+3%",
        icon: FileCheck,
      },
    ],
    [stats]
  );

  const quickAccess = [
    {
      title: "Alunos",
      description: "Gerenciar matriculas e cadastros",
      href: "/alunos",
      icon: GraduationCap,
    },
    {
      title: "Turmas",
      description: "Visualizar e organizar turmas",
      href: "/turmas",
      icon: UsersRound,
    },
    {
      title: "Contratos",
      description: "Emitir e gerenciar contratos",
      href: "/contratos",
      icon: FileCheck,
    },
  ];

  return (
    <section className="space-y-8">
      <div className="space-y-2">
        <p className="text-sm font-semibold uppercase tracking-[0.22em] text-brand-600">
          {getGreeting()}, {name || "admin"}!
        </p>
        <h1 className="text-2xl font-semibold text-brand-900 sm:text-3xl">
          Aqui esta um resumo do seu painel escolar
        </h1>
      </div>

      <HeroBanner
        title="Bem-vindo ao novo ciclo letivo"
        subtitle="Organize matriculas, acompanhe desempenho e mantenha contratos em dia com uma visao completa do seu ecossistema escolar."
        ctaLabel="Ver matriculas"
        ctaHref="/alunos"
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {kpis.map((stat, index) => (
          <div key={stat.title} style={{ animationDelay: `${index * 80}ms` }}>
            <StatCard
              title={stat.title}
              value={stat.value}
              delta={stat.delta}
              icon={stat.icon}
              loading={loading}
            />
          </div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.3fr_1fr]">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-brand-900">
              Acesso rapido
            </h2>
            <p className="text-sm text-slate-500">Atalhos do dia a dia</p>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            {quickAccess.map((item) => (
              <QuickAccessCard key={item.title} {...item} />
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-brand-900">
              Atividade recente
            </h2>
            <p className="text-sm text-slate-500">Ultimas atualizacoes</p>
          </div>
          <ActivityList items={data?.recent_activity ?? []} loading={loading} />
        </div>
      </div>
    </section>
  );
}
