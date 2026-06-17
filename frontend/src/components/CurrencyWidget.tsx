"use client";

import { useEffect, useState } from "react";
import {
  CURRENCIES,
  FALLBACK,
  fetchRates,
  type CurrencyCode,
  type Rates,
} from "@/lib/currency";

interface CurrencyWidgetProps {
  onRatesChange: (rates: Rates, currency: CurrencyCode) => void;
}

export function CurrencyWidget({ onRatesChange }: CurrencyWidgetProps) {
  const [rates, setRates]       = useState<Rates>(FALLBACK);   // always has a value
  const [selected, setSelected] = useState<CurrencyCode>("INR");
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    fetchRates()
      .then((r) => setRates(r))
      .finally(() => setLoading(false));
  }, []);

  // Notify parent whenever rates or selected currency changes.
  useEffect(() => {
    onRatesChange(rates, selected);
  }, [rates, selected, onRatesChange]);

  const isLive      = rates.source === "live";
  const statusLabel = loading
    ? "Loading live rates…"
    : isLive
      ? "Live exchange rates"
      : "Approx. rates (live fetch failed)";
  const statusColor = loading ? "var(--muted)" : isLive ? "var(--mint)" : "var(--gold)";

  return (
    <div className="currency-widget">
      <div className="currency-meta">
        <span className="currency-label">Show prices in</span>
        <span className="currency-status" style={{ color: statusColor }}>
          {loading ? (
            <span className="spin-small">⟳</span>
          ) : isLive ? "●" : "~"}{" "}
          {statusLabel}
        </span>
      </div>
      <div className="currency-tabs">
        {CURRENCIES.map((c) => (
          <button
            key={c.code}
            className={`currency-tab${selected === c.code ? " active" : ""}`}
            onClick={() => setSelected(c.code)}
            title={c.label}
          >
            {c.symbol} {c.code}
          </button>
        ))}
      </div>
    </div>
  );
}
