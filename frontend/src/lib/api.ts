import type { StreamEvent, TravelPlanState } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

/**
 * Non-streaming call — returns the full plan in one response.
 */
export async function generateTravelPlan(
  userQuery: string,
): Promise<TravelPlanState> {
  const response = await fetch(`${API_BASE_URL}/api/travel-plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_query: userQuery }),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Failed to generate travel plan: ${errorBody}`);
  }

  return response.json();
}

interface StreamCallbacks {
  onEvent: (event: StreamEvent) => void;
  signal?: AbortSignal;
}

/**
 * Streaming call — consumes the Server-Sent Events stream from the backend
 * and forwards each parsed event to `onEvent` so the UI can render the
 * agent pipeline in real time.
 */
export async function streamTravelPlan(
  userQuery: string,
  { onEvent, signal }: StreamCallbacks,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/travel-plan/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_query: userQuery }),
    signal,
  });

  if (!response.ok || !response.body) {
    const errorBody = await response.text().catch(() => "");
    throw new Error(
      `Failed to start travel plan stream: ${response.status} ${errorBody}`,
    );
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // SSE frames are separated by a blank line.
    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      const line = frame.trim();
      if (!line.startsWith("data:")) continue;

      const payload = line.slice(5).trim();
      if (!payload) continue;

      try {
        onEvent(JSON.parse(payload) as StreamEvent);
      } catch {
        // Ignore malformed partial frames.
      }
    }
  }
}
