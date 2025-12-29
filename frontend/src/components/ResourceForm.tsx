import { useEffect, useMemo, useState } from "react";

import { useResourceOptions } from "../lib/options";
import { FieldConfig, FieldSection, Option, ResourceConfig } from "../resources";

type ResourceFormProps = {
  resource: ResourceConfig;
  item: Record<string, any> | null;
  open: boolean;
  locked: boolean;
  onClose: () => void;
  onSubmit: (payload: Record<string, any>) => void;
  onDelete: (item: Record<string, any>) => void;
  onAction: (actionKey: string) => void;
  submitting: boolean;
  actionLoading: boolean;
};

const DEFAULT_SECTION: FieldSection = {
  title: "Dados gerais",
  fields: [],
};

function SelectField({
  field,
  value,
  disabled,
  onChange,
  optionsOverride,
}: {
  field: FieldConfig;
  value: any;
  disabled: boolean;
  onChange: (value: any) => void;
  optionsOverride?: Option[];
}) {
  const resourceOptions = useResourceOptions(field.resource);
  const options = optionsOverride || resourceOptions.data || [];
  const isNumeric =
    options.length > 0 ? typeof options[0].value === "number" : Boolean(field.resource);

  return (
    <label>
      {field.label}
      <select
        value={value ?? ""}
        onChange={(event) => {
          if (!event.target.value) {
            onChange("");
            return;
          }
          onChange(isNumeric ? Number(event.target.value) : event.target.value);
        }}
        disabled={disabled}
      >
        <option value="">Selecione</option>
        {options.map((option) => (
          <option key={String(option.value)} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function MultiSelectField({
  field,
  value,
  disabled,
  onChange,
  optionsOverride,
}: {
  field: FieldConfig;
  value: any[];
  disabled: boolean;
  onChange: (value: any[]) => void;
  optionsOverride?: Option[];
}) {
  const resourceOptions = useResourceOptions(field.resource);
  const options = optionsOverride || resourceOptions.data || [];
  const isNumeric =
    options.length > 0 ? typeof options[0].value === "number" : Boolean(field.resource);

  return (
    <label>
      {field.label}
      <div className="multiselect">
        {options.map((option) => {
          const selected = Array.isArray(value) ? value.includes(option.value) : false;
          return (
            <label key={String(option.value)} className="multiselect__item">
              <input
                type="checkbox"
                checked={selected}
                onChange={(event) => {
                  const next = new Set(value || []);
                  if (event.target.checked) {
                    next.add(isNumeric ? Number(option.value) : option.value);
                  } else {
                    next.delete(isNumeric ? Number(option.value) : option.value);
                  }
                  onChange(Array.from(next));
                }}
                disabled={disabled}
              />
              <span>{option.label}</span>
            </label>
          );
        })}
        {resourceOptions.isLoading && <small>Carregando opcoes...</small>}
      </div>
    </label>
  );
}

function normalizeValue(field: FieldConfig, value: any) {
  if (value === "" || value === undefined) {
    return field.type === "multiselect" ? [] : null;
  }
  if (field.type === "number") {
    const parsed = Number(value);
    return Number.isNaN(parsed) ? null : parsed;
  }
  if (field.type === "boolean") {
    return Boolean(value);
  }
  if (field.type === "multiselect") {
    return Array.isArray(value) ? value : [];
  }
  return value;
}

function buildInitialData(resource: ResourceConfig, item: Record<string, any> | null) {
  const data: Record<string, any> = {};
  resource.fields.forEach((field) => {
    if (item && item[field.name] !== undefined && item[field.name] !== null) {
      data[field.name] = item[field.name];
      return;
    }
    if (field.type === "boolean") {
      data[field.name] = false;
      return;
    }
    if (field.type === "multiselect") {
      data[field.name] = [];
      return;
    }
    data[field.name] = "";
  });
  return data;
}

export default function ResourceForm({
  resource,
  item,
  open,
  locked,
  onClose,
  onSubmit,
  onDelete,
  onAction,
  submitting,
  actionLoading,
}: ResourceFormProps) {
  const [formData, setFormData] = useState<Record<string, any>>(() =>
    buildInitialData(resource, item)
  );

  useEffect(() => {
    setFormData(buildInitialData(resource, item));
  }, [resource, item]);

  const resolvedOptions = useMemo(() => {
    const map = new Map<string, Option[]>();
    resource.fields.forEach((field) => {
      if (field.type !== "select" && field.type !== "multiselect") return;
      if (field.options) {
        map.set(field.name, field.options);
      }
    });
    return map;
  }, [resource]);

  const fieldMap = useMemo(
    () => new Map(resource.fields.map((field) => [field.name, field])),
    [resource]
  );

  const sections = useMemo(() => {
    if (resource.sections && resource.sections.length > 0) {
      return resource.sections;
    }
    return [
      {
        ...DEFAULT_SECTION,
        fields: resource.fields.map((field) => field.name),
      },
    ];
  }, [resource]);

  const handleChange = (field: FieldConfig, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [field.name]: value,
    }));
  };

  if (!open) return null;

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const payload: Record<string, any> = {};
    resource.fields.forEach((field) => {
      if (field.readOnly) return;
      payload[field.name] = normalizeValue(field, formData[field.name]);
    });
    onSubmit(payload);
  };

  const renderField = (field: FieldConfig) => {
    const disabled = locked || field.readOnly || resource.readOnly;
    const fieldValue = formData[field.name];
    const options = resolvedOptions.get(field.name);

    if (field.type === "textarea") {
      return (
        <label key={field.name} className={field.monospace ? "mono" : ""}>
          {field.label}
          <textarea
            rows={field.rows || 4}
            value={fieldValue ?? ""}
            onChange={(event) => handleChange(field, event.target.value)}
            disabled={disabled}
          />
        </label>
      );
    }

    if (field.type === "select") {
      return (
        <SelectField
          key={field.name}
          field={field}
          value={fieldValue}
          disabled={disabled}
          onChange={(value) => handleChange(field, value)}
          optionsOverride={options}
        />
      );
    }

    if (field.type === "multiselect") {
      return (
        <MultiSelectField
          key={field.name}
          field={field}
          value={Array.isArray(fieldValue) ? fieldValue : []}
          disabled={disabled}
          onChange={(value) => handleChange(field, value)}
          optionsOverride={options}
        />
      );
    }

    if (field.type === "boolean") {
      return (
        <label key={field.name} className="checkbox">
          <input
            type="checkbox"
            checked={Boolean(fieldValue)}
            onChange={(event) => handleChange(field, event.target.checked)}
            disabled={disabled}
          />
          <span>{field.label}</span>
        </label>
      );
    }

    if (field.type === "link") {
      return (
        <label key={field.name}>
          {field.label}
          {fieldValue ? (
            <a className="link" href={fieldValue} target="_blank" rel="noreferrer">
              Abrir PDF
            </a>
          ) : (
            <div className="muted">Nao gerado</div>
          )}
        </label>
      );
    }

    if (field.type === "json") {
      return (
        <label key={field.name}>
          {field.label}
          <pre className="code-block">
            {fieldValue ? JSON.stringify(fieldValue, null, 2) : "-"}
          </pre>
        </label>
      );
    }

    return (
      <label key={field.name}>
        {field.label}
        <input
          type={field.type === "date" ? "date" : "text"}
          value={field.type === "date" ? fieldValue || "" : fieldValue ?? ""}
          onChange={(event) => handleChange(field, event.target.value)}
          disabled={disabled}
        />
      </label>
    );
  };

  return (
    <div className="drawer">
      <div className="drawer__panel">
        <div className="drawer__header">
          <div>
            <h3>{item ? "Editar registro" : "Novo registro"}</h3>
            <p>{resource.label}</p>
          </div>
          <button className="btn btn-ghost" onClick={onClose}>
            Fechar
          </button>
        </div>
        {item && resource.actions && resource.actions.length > 0 && (
          <div className="drawer__tools">
            {resource.actions.map((action) => {
              const enabled = action.enabledWhen ? action.enabledWhen(item) : true;
              return (
                <button
                  key={action.key}
                  className={`btn btn-${action.variant || "ghost"}`}
                  onClick={() => onAction(action.key)}
                  disabled={!enabled || actionLoading}
                  type="button"
                >
                  {actionLoading ? "Processando..." : action.label}
                </button>
              );
            })}
          </div>
        )}
        <form className="drawer__form" onSubmit={handleSubmit}>
          {(() => {
            const usedFields = new Set<string>();
            return (
              <>
                {sections.map((section) => (
                  <fieldset key={section.title} className="form-section">
                    <legend>{section.title}</legend>
                    <div className="form-section__grid">
                      {section.fields.map((fieldName) => {
                        const field = fieldMap.get(fieldName);
                        if (!field) return null;
                        usedFields.add(fieldName);
                        return renderField(field);
                      })}
                    </div>
                  </fieldset>
                ))}
                {resource.fields.some((field) => !usedFields.has(field.name)) && (
                  <fieldset className="form-section">
                    <legend>Outros</legend>
                    <div className="form-section__grid">
                      {resource.fields
                        .filter((field) => !usedFields.has(field.name))
                        .map((field) => renderField(field))}
                    </div>
                  </fieldset>
                )}
              </>
            );
          })()}
          <div className="drawer__actions">
            {!resource.readOnly && (
              <button className="btn btn-primary" type="submit" disabled={submitting || locked}>
                {submitting ? "Salvando..." : "Salvar"}
              </button>
            )}
            {item && !resource.readOnly && (
              <button className="btn btn-danger" type="button" onClick={() => onDelete(item)}>
                Excluir
              </button>
            )}
          </div>
          {locked && (
            <div className="alert alert-warning">
              Este registro esta bloqueado para edicao.
            </div>
          )}
        </form>
      </div>
      <div className="drawer__overlay" onClick={onClose} />
    </div>
  );
}
