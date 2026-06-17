export interface ParsedRequest {
  origin?: string;
  destination?: string;
  destination_city?: string;
  trip_days?: number;
  budget_in_inr?: number | null;
  parser_source?: string;
  [key: string]: unknown;
}

export interface FlightOption {
  airline?: string;
  flight_number?: string;
  origin?: string;
  destination?: string;
  departure_airport?: string;
  arrival_airport?: string;
  departure_time?: string;
  arrival_time?: string;
  status?: string;
  price?: number | null;
  price_source?: string;
  source?: string;
  url?: string;
  snippet?: string;
  [key: string]: unknown;
}

export interface HotelOption {
  name?: string;
  city?: string;
  category?: string;
  price_per_night?: number | null;
  price_source?: string;
  source?: string;
  url?: string;
  snippet?: string;
  [key: string]: unknown;
}

export interface TravelPlanState {
  user_query: string;
  parsed_request: ParsedRequest;
  flight_options: FlightOption[];
  flight_result: string;
  hotel_options: HotelOption[];
  hotel_result: string;
  budget_result: string;
  itinerary: string;
  final_plan: string;
  llm_calls: number;
  messages: string[];
}

export interface PipelineNodeMeta {
  id: string;
  label: string;
  description: string;
}

export type StreamEvent =
  | { type: "start"; user_query: string; pipeline: PipelineNodeMeta[] }
  | { type: "step"; node: string; label: string; message: string; llm_calls: number }
  | { type: "complete"; state: TravelPlanState }
  | { type: "error"; detail: string };

export type NodeStatus = "pending" | "active" | "done" | "failed";
