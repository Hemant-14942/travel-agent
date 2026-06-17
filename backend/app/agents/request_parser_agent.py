import json
import re

from app.llm.model import get_llm
from app.llm.prompts import REQUEST_PARSER_PROMPT
from app.logger import get_logger

log = get_logger(__name__)


def _extract_trip_days(user_query: str) -> int:
    match = re.search(r"(\d+)\s*[- ]?day", user_query, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 7


def _extract_budget_in_inr(user_query: str) -> int:
    lower_query = user_query.lower()
    match = re.search(r"under\s+(\d+(?:\.\d+)?)\s*(lakh|lakhs|lac|lacs)", lower_query)
    if match:
        return int(float(match.group(1)) * 100000)
    return 200000


def _extract_origin(user_query: str) -> str:
    match = re.search(r"from\s+([a-zA-Z ]+?)(?:\s+under|\s+to|\s+for|$)", user_query, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Delhi"


def _extract_destination(user_query: str) -> str:
    match = re.search(r"(?:to|trip to|visit)\s+([a-zA-Z ]+?)(?:\s+from|\s+under|\s+for|$)", user_query, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    if "japan" in user_query.lower():
        return "Japan"
    return "Tokyo"


def _fallback_parse_request(user_query: str) -> dict:
    destination = _extract_destination(user_query)
    return {
        "origin": _extract_origin(user_query),
        "destination": destination,
        "destination_city": "Tokyo" if destination.lower() == "japan" else destination,
        "trip_days": _extract_trip_days(user_query),
        "budget_in_inr": _extract_budget_in_inr(user_query),
    }


def _extract_json(text: str) -> dict:
    cleaned_text = text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(r"^```(?:json)?", "", cleaned_text)
        cleaned_text = re.sub(r"```$", "", cleaned_text).strip()
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _normalize_parsed_request(parsed_request: dict, user_query: str) -> dict:
    fallback = _fallback_parse_request(user_query)
    origin         = parsed_request.get("origin")         or fallback["origin"]
    destination    = parsed_request.get("destination")    or fallback["destination"]
    destination_city = (
        parsed_request.get("destination_city") or fallback["destination_city"]
    )
    trip_days      = parsed_request.get("trip_days")      or fallback["trip_days"]
    budget_in_inr  = parsed_request.get("budget_in_inr")  or fallback["budget_in_inr"]
    return {
        "origin":           str(origin).strip(),
        "destination":      str(destination).strip(),
        "destination_city": str(destination_city).strip(),
        "trip_days":        int(trip_days),
        "budget_in_inr":    int(budget_in_inr),
        "parser_source":    "llm",
    }


def run_request_parser_agent(user_query: str) -> dict:
    log.info("Calling LLM to parse user query")
    llm    = get_llm()
    prompt = REQUEST_PARSER_PROMPT.format(user_query=user_query)

    try:
        response       = llm.invoke(prompt)
        parsed_request = _extract_json(response.content)
        result         = _normalize_parsed_request(parsed_request, user_query)
        log.debug(f"LLM parsed: {result}")
        return result
    except Exception as exc:
        log.warning(f"LLM parse failed ({exc}) — falling back to regex parser")
        fallback = _fallback_parse_request(user_query)
        fallback["parser_source"] = "regex_fallback"
        log.debug(f"Regex fallback result: {fallback}")
        return fallback
