import { useResourceOptions } from "../lib/options";
import { FieldConfig, ResourceConfig } from "../resources";

type FilterPanelProps = {
  resource: ResourceConfig;
  filters: Record<string, string>;
  onChange: (filters: Record<string, string>) => void;
};

function FilterSelect({
  field,
  value,
  onChange,
}: {
  field: FieldConfig;
  value: string;
  onChange: (value: string) => void;
}) {
  const resourceOptions = useResourceOptions(field.resource);
  const options = field.options || resourceOptions.data || [];

  const mappedOptions =
    field.type === "boolean"
      ? [
          { value: "true", label: "Sim" },
          { value: "false", label: "Nao" },
        ]
      : options.map((option) => ({
          value: String(option.value),
          label: option.label,
        }));

  return (
    <label className="filter-field">
      <span>{field.label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">Todos</option>
        {mappedOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function FilterPanel({ resource, filters, onChange }: FilterPanelProps) {
  if (!resource.filters || resource.filters.length === 0) {
    return null;
  }

  const fieldMap = new Map(resource.fields.map((field) => [field.name, field]));

  const handleClear = () => {
    const next: Record<string, string> = {};
    resource.filters?.forEach((fieldName) => {
      next[fieldName] = "";
    });
    onChange(next);
  };

  return (
    <aside className="filters">
      <div className="filters__header">
        <h4>Filtros</h4>
        <button className="btn btn-ghost" type="button" onClick={handleClear}>
          Limpar
        </button>
      </div>
      <div className="filters__fields">
        {resource.filters.map((fieldName) => {
          const field = fieldMap.get(fieldName);
          if (!field) return null;
          return (
            <FilterSelect
              key={fieldName}
              field={field}
              value={filters[fieldName] || ""}
              onChange={(value) => onChange({ ...filters, [fieldName]: value })}
            />
          );
        })}
      </div>
    </aside>
  );
}
