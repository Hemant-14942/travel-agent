"use client";

import { useState } from "react";
import { parseItinerary, type ItineraryDay } from "@/lib/parseItinerary";
import { Calendar, MapPin, Clock, Flag } from "./Icons";

const DAY_ICONS = ["🌅", "🗺️", "🍜", "🏛️", "🌊", "🎭", "🛍️", "🌄", "🎨", "🏔️"];

function DayCard({ day, isLast }: { day: ItineraryDay; isLast: boolean }) {
  const [open, setOpen] = useState(true);
  const icon = DAY_ICONS[(day.day - 1) % DAY_ICONS.length];

  return (
    <div className="tl-item">
      {/* Spine dot */}
      <div className="tl-spine">
        <div className="tl-dot">{isLast ? <Flag /> : <span>{day.day}</span>}</div>
        {!isLast && <div className="tl-line" />}
      </div>

      {/* Card */}
      <div className="tl-card">
        <button className="tl-card-head" onClick={() => setOpen((o) => !o)}>
          <span className="tl-day-icon">{icon}</span>
          <div className="tl-day-info">
            <span className="tl-day-num">Day {day.day}</span>
            <span className="tl-day-title">{day.title}</span>
          </div>
          <span className="tl-toggle">{open ? "▲" : "▼"}</span>
        </button>

        {open && day.activities.length > 0 && (
          <ul className="tl-activities">
            {day.activities.map((act, idx) => (
              <li key={idx} className="tl-activity">
                {act.time ? (
                  <span className="tl-act-time">
                    <Clock />
                    {act.time}
                  </span>
                ) : (
                  <span className="tl-act-bullet">
                    <MapPin />
                  </span>
                )}
                <span className="tl-act-text">{act.text}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

interface ItineraryTimelineProps {
  markdown: string;
}

export function ItineraryTimeline({ markdown }: ItineraryTimelineProps) {
  const days = parseItinerary(markdown);

  if (days.length === 0) return null;

  return (
    <div className="timeline">
      <div className="tl-controls">
        <span className="tl-meta">
          <Calendar /> {days.length} days
        </span>
      </div>
      <div className="tl-track">
        {days.map((day, idx) => (
          <DayCard key={day.day} day={day} isLast={idx === days.length - 1} />
        ))}
      </div>
    </div>
  );
}
