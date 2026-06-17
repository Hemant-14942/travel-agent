from app.logger import get_logger

log = get_logger(__name__)


def run_budget_agent(
    flight_options: list[dict],
    hotel_options: list[dict],
    nights: int = 6,
) -> str:
    priced_flights = [f for f in flight_options if f.get("price") is not None]
    priced_hotels  = [h for h in hotel_options  if h.get("price_per_night") is not None]

    food_transport_cost = 35000
    activities_cost     = 25000

    # ── Flights ──────────────────────────────────────────────────────────────
    if priced_flights:
        cheapest_flight = min(priced_flights, key=lambda f: f["price"])
        flight_cost     = cheapest_flight["price"]
        price_label     = "estimated fare" if cheapest_flight.get("source") == "Tavily" else "fare"
        log.info(f"Cheapest flight: {cheapest_flight['airline']} — ₹{flight_cost:,} ({price_label})")
        flight_budget_text = (
            f"- Recommended flight: {cheapest_flight['airline']} "
            f"with {price_label} ₹{flight_cost} (verify on aggregator before booking)\n"
        )
    elif flight_options:
        flight_cost = 0
        log.warning("Flights found but no fare prices available (AviationStack limitation)")
        flight_budget_text = (
            "- Recommended flight: Real flight results were found, but "
            "AviationStack does not provide fare prices. Check airline or booking "
            "sites before booking.\n"
        )
    else:
        flight_cost = 0
        log.warning("No flight results found for this route")
        flight_budget_text = (
            "- Recommended flight: No live flight results found for this route.\n"
        )

    # ── Hotels ───────────────────────────────────────────────────────────────
    if priced_hotels:
        cheapest_hotel = min(priced_hotels, key=lambda h: h["price_per_night"])
        hotel_cost     = cheapest_hotel["price_per_night"] * nights
        price_label    = (
            "estimated nightly price"
            if "estimate" in cheapest_hotel.get("price_source", "").lower()
            else "nightly price"
        )
        log.info(
            f"Cheapest hotel: {cheapest_hotel['name']} — "
            f"₹{cheapest_hotel['price_per_night']:,}/night × {nights} nights = ₹{hotel_cost:,}"
        )
        hotel_budget_text = (
            f"- Recommended hotel: {cheapest_hotel['name']} "
            f"with {price_label} ₹{cheapest_hotel['price_per_night']} "
            f"for {nights} nights "
            f"= ₹{hotel_cost}\n"
        )
    else:
        hotel_cost = 0
        log.warning("No hotel results with parseable prices found")
        hotel_budget_text = (
            "- Recommended hotel: Real hotel search results did not include "
            "a parseable nightly price. Check source links before booking.\n"
        )

    total_cost = flight_cost + hotel_cost + food_transport_cost + activities_cost
    log.info(
        f"Budget total — flight ₹{flight_cost:,} + hotel ₹{hotel_cost:,} + "
        f"food/transport ₹{food_transport_cost:,} + activities ₹{activities_cost:,} "
        f"= ₹{total_cost:,}"
    )

    return (
        "Estimated Budget Breakdown\n"
        f"{flight_budget_text}"
        f"{hotel_budget_text}"
        f"- Food and local transport: ₹{food_transport_cost}\n"
        f"- Activities and sightseeing: ₹{activities_cost}\n"
        f"- Estimated total: ₹{total_cost}"
    )
