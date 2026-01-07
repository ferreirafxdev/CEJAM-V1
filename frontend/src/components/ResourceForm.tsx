import { useEffect, useMemo, useState, type FormEvent } from "react";
import { X } from "lucide-react";

import type { ResourceField } from "../data/resources";
import { useResourceOptions } from "../hooks/useResourceOptions";

type ResourceFormProps = {
  title: string;
  description?: string;
  fields: ResourceField[];
  initialValues: Record<string, unknown>;
  submitting?: boolean;
  onSubmit: (payload: Record<string, unknown>) => void;
  onCancel: () => void;
};

const baseInputClass =
  "w-full rounded-xl border border-slate-200 bg-white/80 px-3 py-2 text-sm text-slate-700 shadow-sm outline-none transition focus:border-brand-200 focus:ring-2 focus:ring-brand-100";

function normalizePayload(
  fields: ResourceField[],
  values: Record<string, unknown>
): Record<string, unknown> {
  const payload: Record<string, unknown> = {};

  fields.forEach((field) => {
    if (field.readOnly) {
      return;
    }
    const rawValue = values[field.name];

    if (field.type === "password") {
      if (!rawValue) {
        return;
      }
      payload[field.name] = rawValue;
      return;
    }

    if (field.type === "boolean") {
      payload[field.name] = Boolean(rawValue);
      return;
    }

    if (field.type === "number" || field.type === "currency") {
      if (rawValue === "" || rawValue === null || rawValue === undefined) {
        payload[field.name] = null;
        return;
      }
      const parsed = Number(rawValue);
      payload[field.name] = Number.isNaN(parsed) ? null : parsed;
      return;
    }

    if (field.type === "date") {
      payload[field.name] = rawValue === "" ? null : rawValue;
      return;
    }

    if (field.type === "select" && field.multiple) {
      const arrayValue = Array.isArray(rawValue) ? rawValue : [];
      payload[field.name] =
        field.valueType === "number"
          ? arrayValue.map((value) => Number(value))
          : arrayValue;
      return;
    }

    if (field.type === "select") {
      if (rawValue === "" || rawValue === null || rawValue === undefined) {
        payload[field.name] = null;
        return;
      }
      payload[field.name] =
        field.valueType === "number" ? Number(rawValue) : rawValue;
      return;
    }

    payload[field.name] = rawValue ?? "";
  });

  return payload;
}

export function ResourceForm({
  title,
  description,
  fields,
  initialValues,
  submitting,
  onSubmit,
  onCancel,
}: ResourceFormProps) {
  const [values, setValues] = useState<Record<string, unknown>>(initialValues);

  useEffect(() => {
    setValues(initialValues);
  }, [initialValues]);

  const submitPayload = useMemo(
    () => normalizePayload(fields, values),
    [fields, values]
  );

  const handleChange = (field: ResourceField, value: unknown) => {
    setValues((prev) => ({ ...prev, [field.name]: value }));
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(submitPayload);
  };

  return (
    <div className="fixed inset-0 z-40 flex">
      <button
        type="button"
        className="fixed inset-0 cursor-default bg-slate-900/40 backdrop-blur-sm"
        onClick={onCancel}
        aria-label="Fechar formulario"
      />
      <div className="relative ml-auto flex h-full w-full max-w-2xl flex-col overflow-y-auto border-l border-white/60 bg-white/95 p-6 shadow-soft">
        <div className="flex items-start justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <h2 className="text-xl font-semibold text-brand-900">{title}</h2>
            {description && (
              <p className="text-sm text-slate-500">{description}</p>
            )}
          </div>
          <button
            type="button"
            className="rounded-full border border-slate-200 bg-white/80 p-2 text-slate-500 transition hover:text-brand-800"
            onClick={onCancel}
            aria-label="Fechar formulario"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <div className="grid gap-4 sm:grid-cols-2">
            {fields.map((field) => (
              <FieldInput
                key={field.name}
                field={field}
                value={values[field.name]}
                onChange={handleChange}
                disabled={Boolean(submitting) || Boolean(field.readOnly)}
              />
            ))}
          </div>

          <div className="flex flex-wrap items-center justify-end gap-3 border-t border-slate-100 pt-4">
            <button
              type="button"
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:border-brand-200 hover:text-brand-800"
              onClick={onCancel}
              disabled={submitting}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="rounded-full bg-brand-600 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-70"
              disabled={submitting}
            >
              {submitting ? "Salvando..." : "Salvar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

type FieldInputProps = {
  field: ResourceField;
  value: unknown;
  disabled?: boolean;
  onChange: (field: ResourceField, value: unknown) => void;
};

function FieldInput({ field, value, disabled, onChange }: FieldInputProps) {
  const { options, loading } = useResourceOptions(field.resource);
  const mergedOptions = field.options ?? options;

  const inputValue =
    field.type === "boolean"
      ? Boolean(value)
      : field.type === "select" && field.multiple
        ? (value as string[]) ?? []
        : (value as string | number | undefined) ?? "";

  const commonProps = {
    id: field.name,
    name: field.name,
    disabled,
    required: field.required,
    className: baseInputClass,
  };

  return (
    <div className={field.type === "textarea" ? "sm:col-span-2" : ""}>
      <label
        htmlFor={field.name}
        className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500"
      >
        {field.label}
        {field.required ? " *" : ""}
      </label>

      {field.type === "textarea" && (
        <textarea
          {...commonProps}
          rows={4}
          value={inputValue as string}
          onChange={(event) => onChange(field, event.target.value)}
        />
      )}

      {field.type === "text" && (
        <input
          {...commonProps}
          type="text"
          value={inputValue as string}
          placeholder={field.placeholder}
          onChange={(event) => onChange(field, event.target.value)}
        />
      )}

      {field.type === "email" && (
        <input
          {...commonProps}
          type="email"
          value={inputValue as string}
          placeholder={field.placeholder}
          onChange={(event) => onChange(field, event.target.value)}
        />
      )}

      {field.type === "password" && (
        <input
          {...commonProps}
          type="password"
          value={inputValue as string}
          placeholder={field.placeholder}
          onChange={(event) => onChange(field, event.target.value)}
        />
      )}

      {(field.type === "number" || field.type === "currency") && (
        <input
          {...commonProps}
          type="number"
          step={field.type === "currency" ? "0.01" : "1"}
          value={inputValue as string | number}
          placeholder={field.placeholder}
          onChange={(event) => onChange(field, event.target.value)}
        />
      )}

      {field.type === "date" && (
        <input
          {...commonProps}
          type="date"
          value={inputValue as string}
          onChange={(event) => onChange(field, event.target.value)}
        />
      )}

      {field.type === "select" && (
        <select
          {...commonProps}
          multiple={field.multiple}
          value={inputValue as string | string[]}
          onChange={(event) => {
            if (field.multiple) {
              const values = Array.from(event.target.selectedOptions).map(
                (option) => option.value
              );
              onChange(field, values);
              return;
            }
            onChange(field, event.target.value);
          }}
        >
          {!field.multiple && (
            <option value="">
              {loading ? "Carregando..." : "Selecione"}
            </option>
          )}
          {mergedOptions.map((option) => (
            <option key={`${field.name}-${option.value}`} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )}

      {field.type === "boolean" && (
        <label className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white/80 px-3 py-2 text-sm text-slate-600">
          <input
            type="checkbox"
            checked={Boolean(inputValue)}
            onChange={(event) => onChange(field, event.target.checked)}
            disabled={disabled}
          />
          <span>{inputValue ? "Sim" : "Nao"}</span>
        </label>
      )}

      {field.helper && (
        <p className="mt-1 text-xs text-slate-400">{field.helper}</p>
      )}
    </div>
  );
}
