from app.tools.flight_tool import search_flights
from app.logger import get_logger

log = get_logger(__name__)


def format_flight_options(flight_options: list[dict]) -> str:
    lines = ["Flight options:"]

    if not flight_options:
        return "Flight options:\n- No live flight results found for this route."

    for flight in flight_options:
        price      = flight.get("price")
        price_text = f"₹{price}" if price else "fare not available from AviationStack"
        lines.append(
            f"- {flight['airline']} ({flight['flight_number']}): "
            f"{flight['route']} [{flight['searched_route']}], "
            f"departs {flight['departure_time']}, "
            f"arrives {flight['arrival_time']}, status: {flight['status']}, "
            f"{price_text}"
        )
        if flight.get("url"):
            lines.append(f"  Source: {flight['url']}")
        if flight.get("snippet"):
            lines.append(f"  Details: {flight['snippet']}")

    return "\n".join(lines)


def run_flight_agent(user_query: str, parsed_request: dict) -> tuple[list[dict], str]:
    origin = parsed_request.get("origin", "?")
    dest   = parsed_request.get("destination_city", "?")
    log.info(f"Searching flights: {origin} → {dest}")

    flight_options = search_flights(user_query, parsed_request)

    priced = [f for f in flight_options if f.get("price") is not None]
    log.info(f"Flight search done — {len(flight_options)} results, {len(priced)} with price")

    flight_result = format_flight_options(flight_options)
    return flight_options, flight_result
