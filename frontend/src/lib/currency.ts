// Primary: Frankfurter API — free, no key required.
// Fallback: hardcoded approximate rates (updated periodically).
// This means currency conversion ALWAYS works, even offline.
const API = "https://api.frankfurter.app/latest";

export const CURRENCIES = [
  { code: "INR", symbol: "₹",   label: "Indian Rupee" },
  { code: "USD", symbol: "$",   label: "US Dollar" },
  { code: "EUR", symbol: "€",   label: "Euro" },
  { code: "GBP", symbol: "£",   label: "British Pound" },
  { code: "JPY", symbol: "¥",   label: "Japanese Yen" },
  { code: "AED", symbol: "AED", label: "UAE Dirham" },
  { code: "SGD", symbol: "S$",  label: "Singapore Dollar" },
  { code: "THB", symbol: "฿",   label: "Thai Baht" },
] as const;

export type CurrencyCode = (typeof CURRENCIES)[number]["code"];

export interface Rates {
  base: "INR";
  rates: Partial<Record<CurrencyCode, number>>;
  fetchedAt: number;
  source: "live" | "fallback";
}

// Approximate mid-market rates as of June 2026 (1 INR = X foreign currency).
// Used when the live API is unreachable.
const FALLBACK_RATES: Partial<Record<CurrencyCode, number>> = {
  INR: 1,
  USD: 0.012,
  EUR: 0.011,
  GBP: 0.0095,
  JPY: 1.87,
  AED: 0.044,
  SGD: 0.016,
  THB: 0.43,
};

export const FALLBACK: Rates = {
  base: "INR",
  rates: FALLBACK_RATES,
  fetchedAt: 0,
  source: "fallback",
};

let _cache: Rates | null = null;

export async function fetchRates(): Promise<Rates> {
  // Return cached live rates if fresh (30 min).
  if (_cache && _cache.source === "live" && Date.now() - _cache.fetchedAt < 30 * 60 * 1000) {
    return _cache;
  }

  const targets = CURRENCIES.filter((c) => c.code !== "INR")
    .map((c) => c.code)
    .join(",");

  try {
    const res = await fetch(`${API}?from=INR&to=${targets}`, { signal: AbortSignal.timeout(6000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    _cache = {
      base: "INR",
      rates: { INR: 1, ...json.rates },
      fetchedAt: Date.now(),
      source: "live",
    };
    return _cache;
  } catch {
    // Live fetch failed — return hardcoded fallback so UI always works.
    return FALLBACK;
  }
}

export function convert(amountINR: number, rates: Rates, to: CurrencyCode): number {
  if (to === "INR") return amountINR;
  const rate = rates.rates[to] ?? FALLBACK_RATES[to] ?? 1;
  return amountINR * rate;
}

export function formatAmount(amount: number, code: CurrencyCode): string {
  const currency = CURRENCIES.find((c) => c.code === code);
  const sym = currency?.symbol ?? code;

  if (code === "JPY") {
    return `${sym}${Math.round(amount).toLocaleString()}`;
  }
  if (code === "INR") {
    return `₹${Math.round(amount).toLocaleString("en-IN")}`;
  }
  return `${sym}${amount.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}
