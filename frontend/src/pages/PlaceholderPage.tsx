import { FileText } from "lucide-react";

type PlaceholderPageProps = {
  title: string;
};

export function PlaceholderPage({ title }: PlaceholderPageProps) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="max-w-lg space-y-4 rounded-3xl border border-white/70 bg-white/90 p-8 text-center shadow-soft">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-600">
          <FileText className="h-6 w-6" />
        </div>
        <h1 className="text-2xl font-semibold text-brand-900">{title}</h1>
        <p className="text-sm text-slate-500">
          Esta area esta pronta para integrar com a API. Use este espaco para
          listagens, filtros e acoes do modulo.
        </p>
      </div>
    </div>
  );
}
