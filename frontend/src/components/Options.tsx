import type { FlightOption, HotelOption } from "@/lib/types";
import { formatINR } from "@/lib/format";
import { PlaneTakeoff, Bed, Link, Tag, Clock, MapPin, Alert } from "./Icons";

function isAggregatorEstimate(flight: FlightOption): boolean {
  const src = (flight.price_source ?? flight.source ?? "").toLowerCase();
  return /tavily|estimat|aggregator|web|search/i.test(src);
}

function isHotelEstimate(hotel: HotelOption): boolean {
  return !!hotel.price_source && /tavily|estimat|web|search/i.test(hotel.price_source);
}

function hostOf(url?: string): string {
  if (!url) return "source";
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "source";
  }
}

/** One-line disclaimer shown on every flight fare card. */
function FlightDisclaimer() {
  return (
    <div className="fare-disclaimer">
      <Alert />
      Fare from aggregator — actual checkout price may vary. Always verify before booking.
    </div>
  );
}

export function FlightCard({ flight }: { flight: FlightOption }) {
  const origin      = flight.departure_airport || flight.origin || "DEP";
  const destination = flight.arrival_airport   || flight.destination || "ARR";
  const estimate    = isAggregatorEstimate(flight);

  return (
    <div className="opt-card reveal">
      <div className="opt-head">
        <div>
          <div className="opt-title">{flight.airline || "Flight option"}</div>
          {flight.flight_number && flight.flight_number !== "fare estimate" ? (
            <div className="opt-sub">Flight {flight.flight_number}</div>
          ) : flight.status ? (
            <div className="opt-sub">{flight.status}</div>
          ) : null}
        </div>
        <div className="opt-price">
          <div className="num">{formatINR(flight.price ?? null)}</div>
          <div className="per">{flight.price == null ? "see source" : "approx"}</div>
        </div>
      </div>

      <div className="route">
        <div className="leg">
          <span className="code">{String(origin).slice(0, 4).toUpperCase()}</span>
          {flight.departure_time && flight.departure_time !== "check booking site" ? (
            <span className="time">{flight.departure_time}</span>
          ) : null}
        </div>
        <div className="path">
          <PlaneTakeoff />
        </div>
        <div className="leg" style={{ textAlign: "right" }}>
          <span className="code">{String(destination).slice(0, 4).toUpperCase()}</span>
          {flight.arrival_time && flight.arrival_time !== "check booking site" ? (
            <span className="time">{flight.arrival_time}</span>
          ) : null}
        </div>
      </div>

      {flight.snippet ? <p className="opt-snippet">{flight.snippet}</p> : null}

      <div className="opt-foot">
        <span className={`badge ${estimate ? "est" : ""}`}>
          {estimate ? <Tag /> : <Clock />}
          {estimate ? "Aggregator estimate" : flight.status || "Scheduled"}
        </span>
        {flight.url ? (
          <a className="src-link" href={flight.url} target="_blank" rel="noreferrer">
            {hostOf(flight.url)}
            <Link />
          </a>
        ) : null}
      </div>

      {/* Always show disclaimer for any fare we show — even AviationStack
          doesn't provide final checkout prices */}
      <FlightDisclaimer />
    </div>
  );
}

export function HotelCard({ hotel }: { hotel: HotelOption }) {
  const estimate = isHotelEstimate(hotel);
  return (
    <div className="opt-card reveal">
      <div className="opt-head">
        <div>
          <div className="opt-title">{hotel.name || "Hotel option"}</div>
          <div className="opt-sub">
            {[hotel.category, hotel.city].filter(Boolean).join(" · ") || "Stay"}
          </div>
        </div>
        <div className="opt-price">
          <div className="num">{formatINR(hotel.price_per_night ?? null)}</div>
          <div className="per">per night</div>
        </div>
      </div>

      {hotel.snippet ? <p className="opt-snippet">{hotel.snippet}</p> : null}

      <div className="opt-foot">
        <span className={`badge ${estimate ? "est" : ""}`}>
          <MapPin />
          {estimate ? "Web estimate" : hotel.city || "Verified"}
        </span>
        {hotel.url ? (
          <a className="src-link" href={hotel.url} target="_blank" rel="noreferrer">
            {hostOf(hotel.url)}
            <Link />
          </a>
        ) : null}
      </div>
    </div>
  );
}

export function FlightList({ flights }: { flights: FlightOption[] }) {
  if (!flights.length) return null;
  return (
    <>
      {/* Section-level notice so users understand what these numbers mean */}
      <div className="section-notice">
        <Alert />
        Prices are aggregator estimates (MakeMyTrip, Skyscanner, Ixigo, etc.).
        Airline direct sites are excluded — they show teaser fares that are
        higher at checkout. Always confirm the final price on the booking platform.
      </div>
      <div className="opt-grid">
        {flights.slice(0, 6).map((flight, idx) => (
          <FlightCard key={idx} flight={flight} />
        ))}
      </div>
    </>
  );
}

export function HotelList({ hotels }: { hotels: HotelOption[] }) {
  if (!hotels.length) return null;
  return (
    <div className="opt-grid">
      {hotels.slice(0, 6).map((hotel, idx) => (
        <HotelCard key={idx} hotel={hotel} />
      ))}
    </div>
  );
}

export { PlaneTakeoff, Bed };
