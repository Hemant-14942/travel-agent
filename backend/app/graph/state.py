from typing import Annotated, TypedDict
import operator


class TravelState(TypedDict):
    user_query: str
    parsed_request: dict
    flight_options: list[dict]
    flight_result: str
    hotel_result: str
    hotel_options: list[dict]
    itinerary: str
    final_plan: str
    llm_calls: int
    budget_result: str
    messages: Annotated[list[str], operator.add]