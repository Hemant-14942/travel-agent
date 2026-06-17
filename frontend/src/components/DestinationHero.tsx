"use client";

import { useEffect, useState } from "react";
import { fetchDestinationPhoto, type UnsplashPhoto } from "@/lib/unsplash";
import { MapPin } from "./Icons";

interface DestinationHeroProps {
  /** What to show as the big title — the user's original input (e.g. "Maldives", "Japan"). */
  displayName: string;
  /** What to search Unsplash with — the resolved city (e.g. "Male", "Tokyo"). */
  photoQuery: string;
  origin: string;
  days?: number;
}

export function DestinationHero({ displayName, photoQuery, origin, days }: DestinationHeroProps) {
  const [photo, setPhoto] = useState<UnsplashPhoto | null>(null);

  useEffect(() => {
    const primary  = photoQuery || displayName;
    const fallback = displayName !== primary ? displayName : undefined;
    if (!primary) return;
    fetchDestinationPhoto(primary, fallback).then(setPhoto);
  }, [photoQuery, displayName]);

  return (
    <div className="dest-hero reveal">
      <div
        className="dest-hero-img"
        style={photo ? { backgroundImage: `url(${photo.regular})` } : undefined}
      />
      <div className="dest-hero-overlay" />

      <div className="dest-hero-content">
        <div className="dest-hero-eyebrow">
          <MapPin />
          <span>{origin} → {displayName}</span>
        </div>
        <h2 className="dest-hero-title">{displayName}</h2>
        {days ? <p className="dest-hero-sub">{days}-day trip</p> : null}
      </div>

      {photo ? (
        <a
          className="dest-hero-credit"
          href={photo.creditLink}
          target="_blank"
          rel="noreferrer"
        >
          Photo by {photo.credit} on Unsplash
        </a>
      ) : null}
    </div>
  );
}
