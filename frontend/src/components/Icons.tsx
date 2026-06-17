import type { ReactElement, SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement>;

const base = {
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  viewBox: "0 0 24 24",
};

export const Compass = (p: IconProps) => (
  <svg {...base} {...p}>
    <circle cx="12" cy="12" r="9" />
    <path d="m14.5 9.5-2 5-5 2 2-5 5-2Z" />
  </svg>
);

export const Sparkles = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M12 3v4M12 17v4M3 12h4M17 12h4" />
    <path d="m6.5 6.5 2 2M15.5 15.5l2 2M17.5 6.5l-2 2M8.5 15.5l-2 2" />
    <circle cx="12" cy="12" r="2.4" />
  </svg>
);

export const Search = (p: IconProps) => (
  <svg {...base} {...p}>
    <circle cx="11" cy="11" r="7" />
    <path d="m20 20-3.2-3.2" />
  </svg>
);

export const Plane = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2a1 1 0 0 0-.9 1.7l5.2 3-2.3 3.3-2.4-.3a.8.8 0 0 0-.7 1.3l2 2.4 2.4 2a.8.8 0 0 0 1.3-.7l-.3-2.4 3.3-2.3 3 5.2a1 1 0 0 0 1.7-.9Z" />
  </svg>
);

export const Bed = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M3 7v12M3 13h18v6M21 19v-5a3 3 0 0 0-3-3H8" />
    <circle cx="6.5" cy="10.5" r="1.6" />
  </svg>
);

export const Wallet = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M3 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v0H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9" />
    <path d="M16 13h3" />
  </svg>
);

export const Route = (p: IconProps) => (
  <svg {...base} {...p}>
    <circle cx="6" cy="19" r="2.5" />
    <circle cx="18" cy="5" r="2.5" />
    <path d="M8.5 19H14a3 3 0 0 0 0-6H10a3 3 0 0 1 0-6h5.5" />
  </svg>
);

export const Flag = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M5 21V4M5 4h11l-1.5 3L16 10H5" />
  </svg>
);

export const Check = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="m4 12.5 5 5L20 6.5" />
  </svg>
);

export const Loader = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M12 3a9 9 0 1 0 9 9" />
  </svg>
);

export const MapPin = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z" />
    <circle cx="12" cy="10" r="2.5" />
  </svg>
);

export const Calendar = (p: IconProps) => (
  <svg {...base} {...p}>
    <rect x="3.5" y="5" width="17" height="16" rx="2.5" />
    <path d="M3.5 9.5h17M8 3v4M16 3v4" />
  </svg>
);

export const Globe = (p: IconProps) => (
  <svg {...base} {...p}>
    <circle cx="12" cy="12" r="9" />
    <path d="M3 12h18M12 3c2.5 2.5 2.5 15 0 18M12 3c-2.5 2.5-2.5 15 0 18" />
  </svg>
);

export const Coins = (p: IconProps) => (
  <svg {...base} {...p}>
    <ellipse cx="9" cy="7" rx="6" ry="3" />
    <path d="M3 7v5c0 1.7 2.7 3 6 3M3 12v5c0 1.7 2.7 3 6 3" />
    <ellipse cx="16" cy="14" rx="5" ry="2.6" />
    <path d="M11 14v5c0 1.4 2.2 2.6 5 2.6s5-1.2 5-2.6v-5" />
  </svg>
);

export const Arrow = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M5 12h14M13 6l6 6-6 6" />
  </svg>
);

export const PlaneTakeoff = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M2 21h20" />
    <path d="M3.5 14.5 6 15l3 1 9.5-3.2a2 2 0 0 0-1.2-3.8l-2.3.7-4-4.7-2 .6 2.2 4.7-3.3 1-1.8-1.6-1.8.5Z" />
  </svg>
);

export const Link = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7L11.5 6" />
    <path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7L12.5 18" />
  </svg>
);

export const Alert = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M12 3 2 20h20L12 3Z" />
    <path d="M12 10v4M12 17.5v.5" />
  </svg>
);

export const X = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M6 6l12 12M18 6 6 18" />
  </svg>
);

export const Clock = (p: IconProps) => (
  <svg {...base} {...p}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v5l3 2" />
  </svg>
);

export const Tag = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M3 12V5a2 2 0 0 1 2-2h7l9 9-9 9-9-9Z" />
    <circle cx="8" cy="8" r="1.4" />
  </svg>
);

export const Camera = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M14.5 4h-5l-2 2.5H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8.5a2 2 0 0 0-2-2h-3.5L14.5 4Z" />
    <circle cx="12" cy="13" r="3" />
  </svg>
);

export const Star = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="m12 2 3.1 6.3L22 9.3l-5 4.9 1.2 6.9L12 18l-6.2 3.1L7 14.2 2 9.3l6.9-1L12 2Z" />
  </svg>
);

export const ChevronDown = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="m6 9 6 6 6-6" />
  </svg>
);

export const Download = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M12 3v12M8 11l4 4 4-4" />
    <path d="M4 17v1a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-1" />
  </svg>
);

export const Users = (p: IconProps) => (
  <svg {...base} {...p}>
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
    <circle cx="9" cy="7" r="4" />
    <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
  </svg>
);

export const Sliders = (p: IconProps) => (
  <svg {...base} {...p}>
    <line x1="4" y1="21" x2="4" y2="14" />
    <line x1="4" y1="10" x2="4" y2="3" />
    <line x1="12" y1="21" x2="12" y2="12" />
    <line x1="12" y1="8" x2="12" y2="3" />
    <line x1="20" y1="21" x2="20" y2="16" />
    <line x1="20" y1="12" x2="20" y2="3" />
    <line x1="1" y1="14" x2="7" y2="14" />
    <line x1="9" y1="8" x2="15" y2="8" />
    <line x1="17" y1="16" x2="23" y2="16" />
  </svg>
);

export const iconForNode: Record<string, (p: IconProps) => ReactElement> = {
  request_parser: Sparkles,
  flight_agent: Plane,
  hotel_agent: Bed,
  budget_agent: Wallet,
  itinerary_agent: Route,
  final_agent: Flag,
};
