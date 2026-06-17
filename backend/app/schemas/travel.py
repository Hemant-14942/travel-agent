from typing import Any

from pydantic import BaseModel, Field


class TravelPlanRequest(BaseModel):
    user_query: str = Field(
        ...,
        min_length=10,
        description="Natural language travel planning request.",
        examples=["Plan a 7-day Japan trip from Delhi under 2 lakhs"],
    )


class TravelPlanResponse(BaseModel):
    user_query: str
    parsed_request: dict[str, Any]
    flight_options: list[dict[str, Any]]
    flight_result: str
    hotel_options: list[dict[str, Any]]
    hotel_result: str
    budget_result: str
    itinerary: str
    final_plan: str
    llm_calls: int
    messages: list[str]
