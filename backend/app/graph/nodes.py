from app.graph.state import TravelState
from app.agents.request_parser_agent import run_request_parser_agent
from app.agents.flight_agent import run_flight_agent
from app.agents.hotel_agent import run_hotel_agent
from app.agents.itinerary_agent import run_itinerary_agent
from app.agents.final_agent import run_final_agent
from app.agents.budget_agent import run_budget_agent
from app.logger import get_logger

log = get_logger(__name__)


def request_parser_node(state: TravelState):
    log.info("── Node: request_parser  Parsing user query with LLM")
    parsed_request = run_request_parser_agent(state["user_query"])
    log.info(
        f"   Parsed — origin={parsed_request.get('origin')}  "
        f"destination={parsed_request.get('destination_city')}  "
        f"days={parsed_request.get('trip_days')}  "
        f"budget=₹{parsed_request.get('budget_in_inr'):,}  "
        f"source={parsed_request.get('parser_source')}"
    )
    return {
        "parsed_request": parsed_request,
        "llm_calls": state["llm_calls"] + 1,
        "messages": ["Request Parser Agent extracted trip details with LLM"],
    }


def flight_agent_node(state: TravelState):
    origin = state["parsed_request"].get("origin", "?")
    dest   = state["parsed_request"].get("destination_city", "?")
    log.info(f"── Node: flight_agent  Searching flights {origin} → {dest}")
    flight_options, flight_result = run_flight_agent(
        state["user_query"],
        state["parsed_request"],
    )
    log.info(f"   Found {len(flight_options)} flight option(s)")
    return {
        "flight_options": flight_options,
        "flight_result": flight_result,
        "messages": ["Flight Agent searched AviationStack and Tavily fare estimates"],
    }


def hotel_agent_node(state: TravelState):
    dest = state["parsed_request"].get("destination_city", "?")
    log.info(f"── Node: hotel_agent  Searching hotels in {dest}")
    hotel_options, hotel_result = run_hotel_agent(
        state["user_query"],
        state["flight_result"],
        state["parsed_request"],
    )
    log.info(f"   Found {len(hotel_options)} hotel option(s)")
    return {
        "hotel_options": hotel_options,
        "hotel_result": hotel_result,
        "messages": ["Hotel Agent searched real hotel results with Tavily"],
    }


def budget_agent_node(state: TravelState):
    trip_days = state["parsed_request"]["trip_days"]
    nights    = max(trip_days - 1, 1)
    log.info(f"── Node: budget_agent  Calculating budget for {nights} nights")
    budget_result = run_budget_agent(
        state["flight_options"],
        state["hotel_options"],
        nights=nights,
    )
    log.info("   Budget breakdown ready")
    return {
        "budget_result": budget_result,
        "messages": ["Budget Agent calculated estimated trip cost"],
    }


def itinerary_agent_node(state: TravelState):
    days = state["parsed_request"].get("trip_days", "?")
    dest = state["parsed_request"].get("destination_city", "?")
    log.info(f"── Node: itinerary_agent  Generating {days}-day itinerary for {dest} with LLM")
    itinerary = run_itinerary_agent(
        state["user_query"],
        state["flight_result"],
        state["hotel_result"],
        state["budget_result"],
    )
    log.info(f"   Itinerary generated ({len(itinerary)} chars)")
    return {
        "itinerary": itinerary,
        "llm_calls": state["llm_calls"] + 1,
        "messages": ["Itinerary Agent created a draft day-wise plan"],
    }


def final_agent_node(state: TravelState):
    log.info("── Node: final_agent  Composing final travel plan with LLM")
    final_plan = run_final_agent(
        state["user_query"],
        state["flight_result"],
        state["hotel_result"],
        state["itinerary"],
        state["budget_result"],
    )
    log.info(f"   Final plan ready ({len(final_plan)} chars) — total LLM calls: {state['llm_calls'] + 1}")
    return {
        "final_plan": final_plan,
        "llm_calls": state["llm_calls"] + 1,
        "messages": ["Final Agent combined all results into final plan"],
    }
