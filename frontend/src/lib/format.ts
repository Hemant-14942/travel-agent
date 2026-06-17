export function formatINR(value?: number | null): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "—";
  }
  return `₹${Math.round(value).toLocaleString("en-IN")}`;
}

export interface BudgetItem {
  label: string;
  detail: string;
  amount: number | null;
  isTotal: boolean;
}

export interface ParsedBudget {
  items: BudgetItem[];
  total: number | null;
  intro: string;
}

/**
 * The budget agent returns a human-readable multi-line string. We lightly
 * parse it into structured rows so the UI can render a clean breakdown.
 */
export function parseBudget(text: string): ParsedBudget {
  const lines = text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const items: BudgetItem[] = [];
  let total: number | null = null;
  let intro = "";

  for (const line of lines) {
    const isBullet = /^[-*•]/.test(line);
    if (!isBullet) {
      if (!intro && !/breakdown|estimat/i.test(line)) intro = line;
      continue;
    }

    const content = line.replace(/^[-*•]\s*/, "");
    const isTotal = /total/i.test(content);

    const amounts = content.match(/₹\s?[\d,]+/g);
    let amount: number | null = null;
    if (amounts && amounts.length > 0) {
      const last = amounts[amounts.length - 1];
      amount = Number(last.replace(/[₹,\s]/g, ""));
    }

    const colonIdx = content.indexOf(":");
    const label = colonIdx >= 0 ? content.slice(0, colonIdx).trim() : content.trim();
    const detail = colonIdx >= 0 ? content.slice(colonIdx + 1).trim() : "";

    if (isTotal) total = amount;
    items.push({ label, detail, amount, isTotal });
  }

  return { items, total, intro };
}

export function titleCase(value?: string): string {
  if (!value) return "";
  return value
    .split(/\s+/)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}
