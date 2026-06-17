import { formatINR, parseBudget } from "@/lib/format";
import { FALLBACK, convert, formatAmount, type CurrencyCode, type Rates } from "@/lib/currency";

const SWATCHES = ["#f4622a", "#4ba8d4", "#44d7a8", "#f4c25a", "#ff8a3d", "#6fd0e0"];

interface BudgetCardProps {
  budgetResult: string;
  rates?: Rates | null;
  currency?: CurrencyCode;
}

function fmt(amountINR: number | null, rates?: Rates | null, currency?: CurrencyCode): string {
  if (amountINR === null) return "—";
  if (!currency || currency === "INR") return formatINR(amountINR);
  const r = rates ?? FALLBACK;
  return formatAmount(convert(amountINR, r, currency), currency);
}

export function BudgetCard({ budgetResult, rates, currency = "INR" }: BudgetCardProps) {
  const { items, total } = parseBudget(budgetResult);
  const rows = items.filter((item) => !item.isTotal);
  const totalRow = items.find((item) => item.isTotal);

  if (items.length === 0) {
    return (
      <div className="card final-wrap reveal">
        <div className="final-inner">
          <pre style={{ whiteSpace: "pre-wrap", color: "var(--text-soft)", fontFamily: "var(--font-body)" }}>
            {budgetResult}
          </pre>
        </div>
      </div>
    );
  }

  return (
    <div className="card budget reveal">
      <div className="budget-total">
        <div className="label">Estimated total trip cost</div>
        <div className="amount">{fmt(total, rates, currency)}</div>
        {currency !== "INR" && total ? (
          <div className="amount-inr-sub">≈ {formatINR(total)} INR</div>
        ) : null}
        <div className="note">
          Calculated deterministically from the cheapest flight and hotel found,
          plus typical food, transport and activity estimates.
        </div>
        <div className="bar">
          <div style={{
            height: "100%", width: "100%",
            background: "linear-gradient(90deg, var(--ember), var(--ember-2), var(--gold))",
          }} />
        </div>
      </div>

      <div className="budget-items">
        {rows.map((item, idx) => (
          <div key={`${item.label}-${idx}`} className="budget-row">
            <span className="swatch" style={{ background: SWATCHES[idx % SWATCHES.length] }} />
            <div className="b-label">
              {item.label}
              {item.detail ? <div className="b-detail">{item.detail}</div> : null}
            </div>
            <span className="b-amount">{fmt(item.amount, rates, currency)}</span>
          </div>
        ))}
        {totalRow ? (
          <div className="budget-row total">
            <span className="swatch" style={{ background: "var(--ember)" }} />
            <div className="b-label">{totalRow.label || "Estimated total"}</div>
            <span className="b-amount">{fmt(totalRow.amount ?? total, rates, currency)}</span>
          </div>
        ) : null}
      </div>
    </div>
  );
}
