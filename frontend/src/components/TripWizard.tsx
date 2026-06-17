"use client";

import { useState } from "react";
import { Arrow, Plane, Calendar, Wallet, Flag, Loader, Sparkles, MapPin } from "./Icons";

/* ── Types ───────────────────────────────────────────────────────────────── */
interface WizardState {
  origin: string;
  destination: string;
  days: number;
  budgetLakhs: number;
  style: string;
  interests: string[];
}

interface TripWizardProps {
  onSubmit: (query: string) => void;
  isRunning: boolean;
}

/* ── Static data ─────────────────────────────────────────────────────────── */
const POPULAR_ORIGINS = [
  "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai",
  "Kolkata", "Pune", "Ahmedabad",
];

const POPULAR_DESTINATIONS = [
  "Bali", "Japan", "Thailand", "Singapore", "Dubai",
  "Europe", "Goa", "Maldives", "Sri Lanka", "Paris",
  "London", "New York", "Istanbul", "Vietnam", "Nepal",
];

const TRAVEL_STYLES = [
  { id: "adventure", label: "🏔️ Adventure" },
  { id: "beach",     label: "🏖️ Beach" },
  { id: "cultural",  label: "🏛️ Cultural" },
  { id: "luxury",    label: "💎 Luxury" },
  { id: "budget",    label: "💰 Budget" },
  { id: "honeymoon", label: "💑 Honeymoon" },
  { id: "family",    label: "👨‍👩‍👧 Family" },
  { id: "solo",      label: "🎒 Solo" },
];

const INTERESTS = [
  "Food & Cuisine", "History", "Nightlife", "Nature",
  "Shopping", "Photography", "Wellness & Spa", "Hiking",
  "Art & Museums", "Local Culture", "Water Sports", "Wildlife",
];

const BUDGET_PRESETS = [
  { label: "Under 50k", value: 0.5 },
  { label: "1 Lakh",    value: 1 },
  { label: "1.5 Lakhs", value: 1.5 },
  { label: "2 Lakhs",   value: 2 },
  { label: "3 Lakhs",   value: 3 },
  { label: "5 Lakhs",   value: 5 },
];

const STEPS = ["Destination", "Duration & Style", "Budget & Interests", "Review"];

/* ── Component ───────────────────────────────────────────────────────────── */
export function TripWizard({ onSubmit, isRunning }: TripWizardProps) {
  const [step, setStep] = useState(0);
  const [state, setState] = useState<WizardState>({
    origin: "",
    destination: "",
    days: 7,
    budgetLakhs: 1.5,
    style: "",
    interests: [],
  });

  const set = <K extends keyof WizardState>(k: K, v: WizardState[K]) =>
    setState((s) => ({ ...s, [k]: v }));

  const toggleInterest = (i: string) =>
    setState((s) => ({
      ...s,
      interests: s.interests.includes(i)
        ? s.interests.filter((x) => x !== i)
        : [...s.interests, i],
    }));

  /* ── Validation per step ── */
  const canNext = [
    state.origin.trim().length > 1 && state.destination.trim().length > 1,
    state.days >= 1 && state.style !== "",
    state.budgetLakhs > 0,
    true,
  ][step];

  /* ── Build query string ── */
  const buildQuery = (): string => {
    const budget =
      state.budgetLakhs < 1
        ? `under ₹${Math.round(state.budgetLakhs * 100000)}`
        : `under ${state.budgetLakhs} lakh${state.budgetLakhs !== 1 ? "s" : ""}`;
    const interests =
      state.interests.length > 0
        ? ` Interests: ${state.interests.join(", ")}.`
        : "";
    return (
      `Plan a ${state.days}-day ${state.style} trip from ${state.origin} ` +
      `to ${state.destination} ${budget}.${interests}`
    );
  };

  const handleSubmit = () => {
    if (isRunning) return;
    onSubmit(buildQuery());
  };

  /* ── Step renders ── */
  const stepContent = [
    /* Step 0 — Destination */
    <div key="s0" className="wz-step">
      <div className="wz-step-icon"><Plane /></div>
      <h3 className="wz-step-title">Where are you travelling?</h3>
      <div className="wz-field-row">
        <div className="wz-field">
          <label>Flying from</label>
          <input
            className="wz-input"
            placeholder="e.g. Delhi"
            value={state.origin}
            onChange={(e) => set("origin", e.target.value)}
          />
          <div className="wz-presets">
            {POPULAR_ORIGINS.map((o) => (
              <button key={o} className={`wz-preset${state.origin === o ? " active" : ""}`}
                onClick={() => set("origin", o)}>{o}</button>
            ))}
          </div>
        </div>
        <div className="wz-arrow"><Arrow /></div>
        <div className="wz-field">
          <label>Destination</label>
          <input
            className="wz-input"
            placeholder="e.g. Bali, Japan, Paris"
            value={state.destination}
            onChange={(e) => set("destination", e.target.value)}
          />
          <div className="wz-presets">
            {POPULAR_DESTINATIONS.map((d) => (
              <button key={d} className={`wz-preset${state.destination === d ? " active" : ""}`}
                onClick={() => set("destination", d)}>{d}</button>
            ))}
          </div>
        </div>
      </div>
    </div>,

    /* Step 1 — Duration & Style */
    <div key="s1" className="wz-step">
      <div className="wz-step-icon"><Calendar /></div>
      <h3 className="wz-step-title">How long & what style?</h3>

      <div className="wz-field" style={{ maxWidth: 400 }}>
        <label>Duration — <strong>{state.days} days</strong></label>
        <input
          type="range" min={1} max={30} step={1}
          value={state.days}
          onChange={(e) => set("days", Number(e.target.value))}
          className="wz-range"
        />
        <div className="wz-range-labels"><span>1 day</span><span>30 days</span></div>
      </div>

      <div className="wz-field" style={{ marginTop: 28 }}>
        <label>Travel style</label>
        <div className="wz-grid">
          {TRAVEL_STYLES.map((s) => (
            <button key={s.id}
              className={`wz-style-chip${state.style === s.id ? " active" : ""}`}
              onClick={() => set("style", s.id)}>
              {s.label}
            </button>
          ))}
        </div>
      </div>
    </div>,

    /* Step 2 — Budget & Interests */
    <div key="s2" className="wz-step">
      <div className="wz-step-icon"><Wallet /></div>
      <h3 className="wz-step-title">Budget & interests</h3>

      <div className="wz-field" style={{ maxWidth: 500 }}>
        <label>Total budget per person</label>
        <div className="wz-budget-grid">
          {BUDGET_PRESETS.map((b) => (
            <button key={b.label}
              className={`wz-budget-btn${state.budgetLakhs === b.value ? " active" : ""}`}
              onClick={() => set("budgetLakhs", b.value)}>
              {b.label}
            </button>
          ))}
        </div>
        <p className="wz-budget-val">
          Selected: <strong>₹{Math.round(state.budgetLakhs * 100000).toLocaleString()}</strong>
        </p>
      </div>

      <div className="wz-field" style={{ marginTop: 24 }}>
        <label>Interests <span className="wz-optional">(optional)</span></label>
        <div className="wz-interests-grid">
          {INTERESTS.map((i) => (
            <button key={i}
              className={`wz-interest-chip${state.interests.includes(i) ? " active" : ""}`}
              onClick={() => toggleInterest(i)}>
              {i}
            </button>
          ))}
        </div>
      </div>
    </div>,

    /* Step 3 — Review */
    <div key="s3" className="wz-step">
      <div className="wz-step-icon"><Flag /></div>
      <h3 className="wz-step-title">Review your trip</h3>
      <div className="wz-review">
        <div className="wz-review-row">
          <MapPin /><div><span className="wz-rv-label">Route</span><span className="wz-rv-val">{state.origin} → {state.destination}</span></div>
        </div>
        <div className="wz-review-row">
          <Calendar /><div><span className="wz-rv-label">Duration</span><span className="wz-rv-val">{state.days} days</span></div>
        </div>
        <div className="wz-review-row">
          <Sparkles /><div><span className="wz-rv-label">Style</span><span className="wz-rv-val capitalize">{state.style || "—"}</span></div>
        </div>
        <div className="wz-review-row">
          <Wallet /><div><span className="wz-rv-label">Budget</span><span className="wz-rv-val">₹{Math.round(state.budgetLakhs * 100000).toLocaleString()}</span></div>
        </div>
        {state.interests.length > 0 && (
          <div className="wz-review-row">
            <Flag /><div><span className="wz-rv-label">Interests</span><span className="wz-rv-val">{state.interests.join(", ")}</span></div>
          </div>
        )}
      </div>

      <div className="wz-query-preview">
        <span className="wz-query-label">Query that will be sent:</span>
        <code className="wz-query-text">{buildQuery()}</code>
      </div>
    </div>,
  ];

  return (
    <div className="wizard">
      {/* Progress bar */}
      <div className="wz-progress">
        {STEPS.map((label, i) => (
          <div key={label} className={`wz-progress-step${i <= step ? " passed" : ""}${i === step ? " current" : ""}`}>
            <div className="wz-progress-dot">{i < step ? "✓" : i + 1}</div>
            <span className="wz-progress-label">{label}</span>
          </div>
        ))}
        <div className="wz-progress-line">
          <div className="wz-progress-fill" style={{ width: `${(step / (STEPS.length - 1)) * 100}%` }} />
        </div>
      </div>

      {/* Step content */}
      <div className="wz-body">{stepContent[step]}</div>

      {/* Navigation */}
      <div className="wz-nav">
        {step > 0 ? (
          <button className="btn btn-ghost" onClick={() => setStep(step - 1)} disabled={isRunning}>
            ← Back
          </button>
        ) : <span />}

        {step < STEPS.length - 1 ? (
          <button className="btn" onClick={() => setStep(step + 1)} disabled={!canNext}>
            Continue <Arrow />
          </button>
        ) : (
          <button className="btn" onClick={handleSubmit} disabled={isRunning || !canNext}>
            {isRunning ? <><Loader className="spin" /> Planning…</> : <><Sparkles /> Plan my trip</>}
          </button>
        )}
      </div>
    </div>
  );
}
