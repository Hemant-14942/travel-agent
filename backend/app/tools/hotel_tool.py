import re

import requests

from app.config import get_required_env
from app.logger import get_logger

log = get_logger(__name__)

TAVILY_SEARCH_URL = "https://api.tavily.com/search"
USD_TO_INR_ESTIMATE = 83

# Realistic hotel price bounds in INR per night.
# Anything outside this range is almost certainly a scraped artefact
# (review count, star rating, tax percentage, teaser "from ₹51" bait price).
MIN_PRICE_INR = 400        # cheapest budget dorm/hostel in India
MAX_PRICE_INR = 150_000    # ultra-luxury ceiling


def _to_int(value: str) -> int:
    cleaned = value.replace(",", "").strip()
    if not cleaned:
        raise ValueError(f"Empty numeric string after cleaning: {value!r}")
    return int(cleaned)


def _is_realistic(price_inr: int) -> bool:
    return MIN_PRICE_INR <= price_inr <= MAX_PRICE_INR


def _all_prices(pattern: str, content: str, multiplier: int = 1) -> list[int]:
    """Return all prices matching `pattern`, converted to INR, sanity-filtered."""
    matches = re.findall(pattern, content, re.IGNORECASE)
    return [
        _to_int(m) * multiplier
        for m in matches
        if _is_realistic(_to_int(m) * multiplier)
    ]


def _extract_price_per_night(content: str) -> int | None:
    """
    Extract a realistic nightly hotel price (INR) from a Tavily snippet.

    Priority order:
    1. INR amounts next to /night or per night keywords — most reliable
    2. Bare INR amounts (₹ / Rs / INR) — filtered to realistic range
    3. USD nightly price → converted to INR
    4. Bare USD price → converted, last resort
    """

    # 1. INR explicitly tied to a nightly context
    inr_nightly = _all_prices(
        r"(?:₹|Rs\.?|INR)\s?(\d[\d,]*)\s*(?:/night|per night|per\s+night|night)",
        content,
    )
    if inr_nightly:
        return min(inr_nightly)

    # 2. Bare INR amount — still sanity-checked
    inr_bare = _all_prices(r"(?:₹|Rs\.?|INR)\s?(\d[\d,]*)", content)
    if inr_bare:
        return min(inr_bare)

    # 3. USD nightly price
    usd_nightly = _all_prices(
        r"\$\s?(\d[\d,]*)\s*(?:/night|per night|per\s+night|night)",
        content,
        multiplier=USD_TO_INR_ESTIMATE,
    )
    if usd_nightly:
        return min(usd_nightly)

    # 4. Bare USD — last resort
    usd_bare = _all_prices(r"\$\s?(\d[\d,]*)", content, multiplier=USD_TO_INR_ESTIMATE)
    if usd_bare:
        return min(usd_bare)

    return None


def search_hotels(user_query: str, flight_result: str, parsed_request: dict) -> list[dict]:
    api_key   = get_required_env("TAVILY_API_KEY")
    city      = parsed_request["destination_city"]
    trip_days = parsed_request["trip_days"]
    budget    = parsed_request["budget_in_inr"]

    # Per-night budget ceiling: rough estimate so Tavily returns relevant results.
    per_night_budget = max(budget // max(trip_days - 1, 1), 2000)

    query = (
        f"hotel price per night in {city} under INR {per_night_budget} per night. "
        f"Budget hotels {city} price per night INR booking."
    )
    log.info(f"Tavily hotel search in {city} — per-night ceiling ₹{per_night_budget:,}")
    log.debug(f"Hotel search query: '{query}'")

    response = requests.post(
        TAVILY_SEARCH_URL,
        json={
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 7,
        },
        timeout=20,
    )
    response.raise_for_status()

    results = response.json().get("results", [])
    log.info(f"Tavily returned {len(results)} hotel result(s) for {city}")

    hotels = []
    for result in results:
        content = result.get("content", "")
        price   = _extract_price_per_night(content)

        if price is None:
            log.debug(f"No realistic price found in snippet for: {result.get('title', '?')[:60]}")
        else:
            log.debug(f"Extracted price ₹{price:,}/night from: {result.get('title', '?')[:60]}")

        hotels.append({
            "name":           result.get("title", "Unknown hotel"),
            "city":           city,
            "category":       "real_search_result",
            "price_per_night": price,
            "price_source":   "Tavily estimate",
            "url":            result.get("url", ""),
            "snippet":        content,
        })

    priced = [h for h in hotels if h["price_per_night"] is not None]
    log.info(f"Hotels with valid price: {len(priced)}/{len(hotels)}")
    if priced:
        prices = [h["price_per_night"] for h in priced]
        log.info(f"Hotel price range: ₹{min(prices):,} – ₹{max(prices):,} per night")

    return hotels
