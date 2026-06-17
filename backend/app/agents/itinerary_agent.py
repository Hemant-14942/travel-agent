from app.llm.model import get_llm
from app.llm.prompts import ITINERARY_PROMPT
from app.logger import get_logger

log = get_logger(__name__)


def run_itinerary_agent(
    user_query: str,
    flight_result: str,
    hotel_result: str,
    budget_result: str,
) -> str:
    log.info("Calling LLM to generate day-wise itinerary")
    llm    = get_llm()
    prompt = ITINERARY_PROMPT.format(
        user_query=user_query,
        flight_result=flight_result,
        hotel_result=hotel_result,
        budget_result=budget_result,
    )
    response = llm.invoke(prompt)
    log.info(f"Itinerary LLM call complete — {len(response.content)} chars returned")
    return response.content
