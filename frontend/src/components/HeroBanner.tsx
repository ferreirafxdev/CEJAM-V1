import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

type HeroBannerProps = {
  title: string;
  subtitle: string;
  ctaLabel: string;
  ctaHref: string;
};

export function HeroBanner({ title, subtitle, ctaLabel, ctaHref }: HeroBannerProps) {
  return (
    <div className="relative overflow-hidden rounded-[28px] bg-gradient-to-r from-brand-900 via-brand-600 to-accent-200 p-8 text-white shadow-soft">
      <div className="absolute -right-16 -top-24 h-48 w-48 rounded-full bg-white/15 blur-2xl" />
      <div className="absolute -bottom-20 -left-10 h-56 w-56 rounded-full bg-white/10 blur-3xl" />

      <div className="relative z-10 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="max-w-2xl space-y-2">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-white/70">
            Calendario Academico
          </p>
          <h2 className="text-2xl font-semibold sm:text-3xl lg:text-4xl">
            {title}
          </h2>
          <p className="text-sm text-white/85 sm:text-base">{subtitle}</p>
        </div>
        <Link
          to={ctaHref}
          className="inline-flex w-fit items-center gap-2 rounded-full bg-white/90 px-5 py-2.5 text-sm font-semibold text-brand-900 shadow-sm transition hover:translate-y-[-1px] hover:bg-white"
        >
          {ctaLabel}
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}
