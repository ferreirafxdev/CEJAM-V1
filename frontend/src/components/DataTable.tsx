import { formatBoolean, formatCurrency, formatDate, prettyLabel } from "../lib/format";

type DataTableProps = {
  columns: string[];
  items: Record<string, any>[];
  onSelect: (item: Record<string, any>) => void;
};

function renderValue(key: string, value: any) {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "boolean") return formatBoolean(value);
  if (key.includes("data") || key.includes("competencia")) return formatDate(value);
  if (key.includes("valor") || key.includes("multa") || key.includes("juros")) {
    return formatCurrency(value);
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

export default function DataTable({ columns, items, onSelect }: DataTableProps) {
  return (
    <div className="table">
      <div className="table__head">
        {columns.map((key) => (
          <div key={key} className="table__cell table__cell--head">
            {prettyLabel(key)}
          </div>
        ))}
        <div className="table__cell table__cell--head">Acoes</div>
      </div>
      <div className="table__body">
        {items.map((item) => (
          <div key={item.id} className="table__row">
            {columns.map((key) => (
              <div key={key} className="table__cell">
                {renderValue(key, item[key])}
              </div>
            ))}
            <div className="table__cell">
              <button className="btn btn-ghost" onClick={() => onSelect(item)}>
                Ver / Editar
              </button>
            </div>
          </div>
        ))}
        {items.length === 0 && (
          <div className="table__empty">Nenhum registro encontrado.</div>
        )}
      </div>
    </div>
  );
}
