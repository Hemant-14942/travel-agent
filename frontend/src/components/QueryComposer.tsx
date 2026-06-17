"use client";

import { useState } from "react";
import { Search, Arrow, Loader } from "./Icons";

const EXAMPLES = [
  "Plan a 7-day Japan trip from Delhi under 2 lakhs",
  "5-day Bali honeymoon from Mumbai under 1.5 lakhs",
  "Weekend Goa getaway from Bangalore under 40k",
  "10-day Europe backpacking from Delhi under 3 lakhs",
];

interface QueryComposerProps {
  onSubmit: (query: string) => void;
  isRunning: boolean;
}

export function QueryComposer({ onSubmit, isRunning }: QueryComposerProps) {
  const [value, setValue] = useState("");

  const submit = () => {
    const query = value.trim();
    if (query.length < 10 || isRunning) return;
    onSubmit(query);
  };

  return (
    <div className="composer">
      <div className="composer-box">
        <Search className="lead" />
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") submit();
          }}
          placeholder="Where to? e.g. Plan a 7-day Japan trip from Delhi under 2 lakhs"
          disabled={isRunning}
        />
        <button className="btn" onClick={submit} disabled={isRunning || value.trim().length < 10}>
          {isRunning ? (
            <>
              <Loader className="spin" /> Planning…
            </>
          ) : (
            <>
              Plan my trip <Arrow />
            </>
          )}
        </button>
      </div>

      <div className="chips">
        {EXAMPLES.map((example) => (
          <button
            key={example}
            className="chip"
            onClick={() => {
              setValue(example);
              if (!isRunning) onSubmit(example);
            }}
            disabled={isRunning}
          >
            {example}
          </button>
        ))}
      </div>
    </div>
  );
}
