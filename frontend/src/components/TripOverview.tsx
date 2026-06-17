import type { ParsedRequest } from "@/lib/types";
import { formatINR, titleCase } from "@/lib/format";
import { Globe, MapPin, Calendar, Coins } from "./Icons";

export function TripOverview({ parsed }: { parsed: ParsedRequest }) {
  // Prefer what the user typed (e.g. "Maldives") over the resolved city
  // ("Male") so the display is always user-friendly.
  const destination =
    parsed.destination || parsed.destination_city || "Destination";

  const stats = [
    {
      icon: <Globe />,
      label: "From",
      value: titleCase(parsed.origin) || "—",
    },
    {
      icon: <MapPin />,
      label: "Destination",
      value: titleCase(destination),
    },
    {
      icon: <Calendar />,
      label: "Duration",
      value: parsed.trip_days ? `${parsed.trip_days} days` : "—",
    },
    {
      icon: <Coins />,
      label: "Budget",
      value: formatINR(parsed.budget_in_inr ?? null),
    },
  ];

  return (
    <div className="stat-grid">
      {stats.map((s) => (
        <div key={s.label} className="stat reveal">
          <div className="stat-ico">{s.icon}</div>
          <div className="stat-label">{s.label}</div>
          <div className="stat-value">{s.value}</div>
        </div>
      ))}
    </div>
  );
}
