"use client";

import { useCallback, useRef, useState } from "react";
import { streamTravelPlan } from "@/lib/api";
import type {
  NodeStatus,
  PipelineNodeMeta,
  StreamEvent,
  TravelPlanState,
} from "@/lib/types";
import { FALLBACK, type CurrencyCode, type Rates } from "@/lib/currency";

import { TripWizard } from "@/components/TripWizard";
import { AgentPipeline } from "@/components/AgentPipeline";
import { TripOverview } from "@/components/TripOverview";
import { BudgetCard } from "@/components/BudgetCard";
import { FlightList, HotelList } from "@/components/Options";
import { FinalPlan } from "@/components/FinalPlan";
import { DestinationHero } from "@/components/DestinationHero";
import { ItineraryTimeline } from "@/components/ItineraryTimeline";
import { CurrencyWidget } from "@/components/CurrencyWidget";
import { PdfExport } from "@/components/PdfExport";
import {
  Compass,
  Sparkles,
  Plane,
  Bed,
  Wallet,
  Flag,
  MapPin,
  Alert,
  Route,
  Calendar,
} from "@/components/Icons";

type Phase = "idle" | "running" | "done" | "error";

export default function Home() {
  const [phase, setPhase]               = useState<Phase>("idle");
  const [pipeline, setPipeline]         = useState<PipelineNodeMeta[]>([]);
  const [statuses, setStatuses]         = useState<Record<string, NodeStatus>>({});
  const [activeLabel, setActiveLabel]   = useState("");
  const [latestMessage, setLatestMessage] = useState("");
  const [llmCalls, setLlmCalls]         = useState(0);
  const [result, setResult]             = useState<TravelPlanState | null>(null);
  const [error, setError]               = useState("");
  const [currency, setCurrency]         = useState<CurrencyCode>("INR");
  const [rates, setRates]               = useState<Rates>(FALLBACK);

  const pipelineRef = useRef<PipelineNodeMeta[]>([]);

  /* ── Stream event handler ─────────────────────────────────────────────── */
  const handleEvent = useCallback((event: StreamEvent) => {
    if (event.type === "start") {
      pipelineRef.current = event.pipeline;
      setPipeline(event.pipeline);
      const initial: Record<string, NodeStatus> = {};
      event.pipeline.forEach((node, idx) => {
        initial[node.id] = idx === 0 ? "active" : "pending";
      });
      setStatuses(initial);
      setActiveLabel(event.pipeline[0]?.label ?? "");
      setLatestMessage("");
    } else if (event.type === "step") {
      setLlmCalls(event.llm_calls);
      setLatestMessage(event.message);
      setStatuses((prev) => {
        const next = { ...prev };
        next[event.node] = "done";
        const order = pipelineRef.current;
        const idx = order.findIndex((n) => n.id === event.node);
        const upcoming = order[idx + 1];
        if (upcoming) {
          if (next[upcoming.id] !== "done") next[upcoming.id] = "active";
          setActiveLabel(upcoming.label);
        }
        return next;
      });
    } else if (event.type === "complete") {
      const done: Record<string, NodeStatus> = {};
      pipelineRef.current.forEach((node) => { done[node.id] = "done"; });
      setStatuses(done);
      setLlmCalls(event.state.llm_calls);
      setResult(event.state);
      setPhase("done");
    } else if (event.type === "error") {
      setError(event.detail);
      setPhase("error");
      setStatuses((prev) => {
        const next = { ...prev };
        for (const id of Object.keys(next)) {
          if (next[id] === "active") next[id] = "failed";
        }
        return next;
      });
    }
  }, []);

  const markActiveFailed = useCallback(() => {
    setStatuses((prev) => {
      const next = { ...prev };
      for (const id of Object.keys(next)) {
        if (next[id] === "active") next[id] = "failed";
      }
      return next;
    });
  }, []);

  /* ── Start a plan run ─────────────────────────────────────────────────── */
  const runPlan = useCallback(
    async (query: string) => {
      setPhase("running");
      setResult(null);
      setError("");
      setLlmCalls(0);
      setLatestMessage("");
      setActiveLabel("");
      setPipeline([]);
      setStatuses({});
      try {
        await streamTravelPlan(query, { onEvent: handleEvent });
        setPhase((current) => (current === "error" ? current : "done"));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Something went wrong.");
        setPhase("error");
        markActiveFailed();
      }
    },
    [handleEvent, markActiveFailed],
  );

  /* ── Derived values ───────────────────────────────────────────────────── */
  const isRunning    = phase === "running";
  const showPipeline = phase !== "idle" && pipeline.length > 0;

  // Display name: what the user actually typed (e.g. "Maldives", "Japan").
  const dest = result?.parsed_request?.destination
    ?? result?.parsed_request?.destination_city
    ?? "";
  // City used for Unsplash photo search — more specific gives better photos.
  const destCity = result?.parsed_request?.destination_city
    ?? result?.parsed_request?.destination
    ?? "";
  const origin   = result?.parsed_request?.origin ?? "";
  const tripDays = result?.parsed_request?.trip_days;

  const handleRatesChange = useCallback((r: Rates, c: CurrencyCode) => {
    setRates(r);
    setCurrency(c);
  }, []);

  return (
    <main className="shell" id="print-root">
      {/* ── Topbar ── */}
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark"><Compass /></span>
          <span>Wander<span className="accent">lust</span></span>
        </div>
        <div className="topbar-meta">
          {result && dest ? (
            <PdfExport destination={dest || destCity} />
          ) : null}
        </div>
      </header>

      {/* ── Hero + Wizard ── */}
      {phase === "idle" || phase === "running" ? (
        <section className="hero">
          <span className="eyebrow">
            <Sparkles /> Powered by a 6-agent AI pipeline
          </span>
          <h1>
            Plan your perfect trip with a<br />
            <span className="grad">team of AI travel agents</span>
          </h1>
          <p>
            Fill in the form below — watch specialized agents search flights,
            find hotels, crunch the budget, and craft a day-by-day itinerary live.
          </p>
          <TripWizard onSubmit={runPlan} isRunning={isRunning} />
        </section>
      ) : null}

      {/* ── Error banner ── */}
      {error ? (
        <div className="error-banner reveal">
          <Alert />
          <span>{error}</span>
          <button
            className="btn btn-ghost"
            style={{ marginLeft: "auto", padding: "7px 14px", fontSize: 13 }}
            onClick={() => { setPhase("idle"); setError(""); }}
          >
            Try again
          </button>
        </div>
      ) : null}

      {/* ── Live pipeline ── */}
      {showPipeline ? (
        <section className="section">
          <AgentPipeline
            nodes={pipeline}
            statuses={statuses}
            activeLabel={activeLabel}
            latestMessage={latestMessage}
            isRunning={isRunning}
            errored={phase === "error"}
            llmCalls={llmCalls}
          />
        </section>
      ) : null}

      {/* ── Results ── */}
      {result ? (
        <>
          {/* Destination photo hero */}
          {dest ? (
            <section className="section">
              <DestinationHero
                displayName={dest}
                photoQuery={destCity}
                origin={origin}
                days={tripDays}
              />
            </section>
          ) : null}

          {/* Currency converter — controls all price displays */}
          <section className="section">
            <CurrencyWidget onRatesChange={handleRatesChange} />
          </section>

          {/* Trip overview */}
          {Object.keys(result.parsed_request).length > 0 ? (
            <section className="section">
              <div className="section-head">
                <span className="ico"><MapPin /></span>
                <div>
                  <h2>Trip overview</h2>
                  <div className="sub">What we understood from your request</div>
                </div>
              </div>
              <TripOverview parsed={result.parsed_request} />
            </section>
          ) : null}

          {/* Budget breakdown */}
          {result.budget_result ? (
            <section className="section">
              <div className="section-head">
                <span className="ico"><Wallet /></span>
                <div>
                  <h2>Budget breakdown</h2>
                  <div className="sub">Estimated, deterministic cost split</div>
                </div>
              </div>
              <BudgetCard
                budgetResult={result.budget_result}
                rates={rates}
                currency={currency}
              />
            </section>
          ) : null}

          {/* Flights */}
          {result.flight_options?.length ? (
            <section className="section">
              <div className="section-head">
                <span className="ico"><Plane /></span>
                <div>
                  <h2>Flight options</h2>
                  <div className="sub">{result.flight_options.length} options found</div>
                </div>
              </div>
              <FlightList flights={result.flight_options} />
            </section>
          ) : null}

          {/* Hotels */}
          {result.hotel_options?.length ? (
            <section className="section">
              <div className="section-head">
                <span className="ico"><Bed /></span>
                <div>
                  <h2>Where to stay</h2>
                  <div className="sub">{result.hotel_options.length} stays found</div>
                </div>
              </div>
              <HotelList hotels={result.hotel_options} />
            </section>
          ) : null}

          {/* Day-by-day timeline */}
          {result.itinerary ? (
            <section className="section">
              <div className="section-head">
                <span className="ico"><Calendar /></span>
                <div>
                  <h2>Day-by-day itinerary</h2>
                  <div className="sub">Expandable timeline view</div>
                </div>
              </div>
              <ItineraryTimeline markdown={result.itinerary} />
            </section>
          ) : null}

          {/* Full final plan (markdown) */}
          {result.final_plan ? (
            <section className="section">
              <div className="section-head">
                <span className="ico"><Flag /></span>
                <div>
                  <h2>Full travel plan</h2>
                  <div className="sub">Crafted by the final agent</div>
                </div>
              </div>
              <FinalPlan content={result.final_plan} />
            </section>
          ) : null}

          {/* New trip CTA */}
          <section className="section" style={{ textAlign: "center", marginTop: 20 }}>
            <button
              className="btn"
              onClick={() => { setPhase("idle"); setResult(null); setError(""); }}
            >
              <Route /> Plan another trip
            </button>
          </section>
        </>
      ) : null}

      {/* ── Empty state ── */}
      {phase === "idle" && !result ? (
        <div className="empty-hint">
          <div className="ring"><Compass /></div>
          <p>Fill in the wizard above to start planning your trip.</p>
        </div>
      ) : null}

      <footer className="foot">
        Built with Next.js · FastAPI · LangGraph — all prices are estimates,
        verify before booking.
      </footer>
    </main>
  );
}
