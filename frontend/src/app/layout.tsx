import type { ReactNode } from "react";
import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Wanderlust — AI Travel Planner",
  description:
    "A LangGraph multi-agent system that plans flights, hotels, budget and a day-by-day itinerary in real time.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  themeColor: "#0e0c0a",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="bg-ambient" aria-hidden />
        <div className="bg-grain" aria-hidden />
        {children}
      </body>
    </html>
  );
}
