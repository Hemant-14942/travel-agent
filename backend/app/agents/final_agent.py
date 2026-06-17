from app.llm.model import get_llm
from app.llm.prompts import FINAL_PLAN_PROMPT
from app.logger import get_logger

log = get_logger(__name__)


def run_final_agent(
    user_query: str,
    flight_result: str,
    hotel_result: str,
    itinerary: str,
    budget_result: str,
) -> str:
    log.info("Calling LLM to compose final polished travel plan")
    llm    = get_llm()
    prompt = FINAL_PLAN_PROMPT.format(
        user_query=user_query,
        flight_result=flight_result,
        hotel_result=hotel_result,
        itinerary=itinerary,
        budget_result=budget_result,
    )
    response = llm.invoke(prompt)
    log.info(f"Final plan LLM call complete — {len(response.content)} chars returned")
    return response.content
