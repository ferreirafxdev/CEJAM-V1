export function formatNumber(value?: number | string) {
  if (value === undefined || value === null || value === "") {
    return "--";
  }
  const numberValue = typeof value === "string" ? Number(value) : value;
  if (Number.isNaN(numberValue)) {
    return "--";
  }
  return new Intl.NumberFormat("pt-BR").format(numberValue);
}

export function formatDate(value?: string) {
  if (!value) {
    return "--";
  }
  const dateOnlyMatch = value.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (dateOnlyMatch) {
    const [, year, month, day] = dateOnlyMatch;
    return `${day}/${month}/${year}`;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleDateString("pt-BR");
}

export function formatDateTime(value?: string) {
  if (!value) {
    return "--";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}

export function formatPercent(value?: number | string) {
  if (value === undefined || value === null || value === "") {
    return "--";
  }
  const numberValue = typeof value === "string" ? Number(value) : value;
  if (Number.isNaN(numberValue)) {
    return "--";
  }
  return `${new Intl.NumberFormat("pt-BR", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numberValue)}%`;
}

export function formatBoolean(value?: boolean) {
  if (value === undefined || value === null) {
    return "--";
  }
  return value ? "Sim" : "Nao";
}
