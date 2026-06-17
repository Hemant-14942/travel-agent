from app.tools.hotel_tool import search_hotels
from app.logger import get_logger

log = get_logger(__name__)


def format_hotel_options(hotel_options: list[dict]) -> str:
    lines = ["Hotel options:"]
    for hotel in hotel_options:
        price        = hotel.get("price_per_night")
        price_source = hotel.get("price_source", "search result")
        price_text   = (
            f"₹{price}/night ({price_source})"
            if price
            else "price not found in search result"
        )
        lines.append(
            f"- {hotel['name']}: {hotel['city']}, "
            f"{hotel['category']}, {price_text}"
        )
        if hotel.get("url"):
            lines.append(f"  Source: {hotel['url']}")
        if hotel.get("snippet"):
            lines.append(f"  Details: {hotel['snippet']}")
    return "\n".join(lines)


def run_hotel_agent(
    user_query: str,
    flight_result: str,
    parsed_request: dict,
) -> tuple[list[dict], str]:
    city = parsed_request.get("destination_city", "?")
    log.info(f"Searching hotels in {city} via Tavily")

    hotel_options = search_hotels(user_query, flight_result, parsed_request)

    priced = [h for h in hotel_options if h.get("price_per_night") is not None]
    log.info(f"Hotel search done — {len(hotel_options)} results, {len(priced)} with price")

    hotel_result = format_hotel_options(hotel_options)
    return hotel_options, hotel_result
