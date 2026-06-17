export interface ItineraryActivity {
  time?: string;
  text: string;
}

export interface ItineraryDay {
  day: number;
  title: string;
  activities: ItineraryActivity[];
  highlight?: string;   // first activity or bold phrase used as day summary
}

const DAY_HEADER_RE = /^#+\s*day\s*(\d+)[:\s–-]*(.*)$/i;
const TIME_PREFIX_RE = /^(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s*[–:-]\s*/i;

function extractTime(text: string): { time?: string; clean: string } {
  const m = text.match(TIME_PREFIX_RE);
  if (m) return { time: m[1], clean: text.slice(m[0].length).trim() };
  return { clean: text };
}

function parseBullet(raw: string): ItineraryActivity {
  const stripped = raw.replace(/^[-*•]\s*/, "").replace(/\*\*/g, "").trim();
  const { time, clean } = extractTime(stripped);
  return { time, text: clean };
}

export function parseItinerary(markdown: string): ItineraryDay[] {
  const lines = markdown.split("\n").map((l) => l.trimEnd());
  const days: ItineraryDay[] = [];
  let current: ItineraryDay | null = null;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    const dayMatch = trimmed.match(DAY_HEADER_RE);
    if (dayMatch) {
      current = {
        day: parseInt(dayMatch[1], 10),
        title: dayMatch[2].replace(/\*\*/g, "").trim() || `Day ${dayMatch[1]}`,
        activities: [],
      };
      days.push(current);
      continue;
    }

    if (!current) continue;

    const isBullet = /^[-*•]/.test(trimmed);
    const isNumbered = /^\d+[.)]\s/.test(trimmed);

    if (isBullet || isNumbered) {
      const raw = isBullet ? trimmed : trimmed.replace(/^\d+[.)]\s*/, "");
      const activity = parseBullet(raw);
      if (activity.text) {
        current.activities.push(activity);
        if (!current.highlight) current.highlight = activity.text;
      }
    } else if (!trimmed.startsWith("#")) {
      // plain paragraph under a day heading — treat as a note
      const clean = trimmed.replace(/\*\*/g, "").trim();
      if (clean) current.activities.push({ text: clean });
    }
  }

  return days;
}
