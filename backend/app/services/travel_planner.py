from collections.abc import Iterator

from app.graph.builder import travel_graph
from app.logger import get_logger

log = get_logger(__name__)


PIPELINE_NODES = [
    {
        "id": "request_parser",
        "label": "Understanding request",
        "description": "Extracting destination, dates and budget",
    },
    {
        "id": "flight_agent",
        "label": "Searching flights",
        "description": "AviationStack schedules + Tavily fare estimates",
    },
    {
        "id": "hotel_agent",
        "label": "Finding hotels",
        "description": "Live hotel search via Tavily",
    },
    {
        "id": "budget_agent",
        "label": "Calculating budget",
        "description": "Deterministic cost breakdown",
    },
    {
        "id": "itinerary_agent",
        "label": "Designing itinerary",
        "description": "Day-by-day plan with the LLM",
    },
    {
        "id": "final_agent",
        "label": "Finalizing plan",
        "description": "Polished travel plan and tips",
    },
]

NODE_LABELS = {node["id"]: node["label"] for node in PIPELINE_NODES}


def build_initial_state(user_query: str) -> dict:
    return {
        "user_query": user_query,
        "parsed_request": {},
        "flight_result": "",
        "flight_options": [],
        "hotel_result": "",
        "hotel_options": [],
        "itinerary": "",
        "final_plan": "",
        "budget_result": "",
        "llm_calls": 0,
        "messages": [],
    }


def generate_travel_plan(user_query: str) -> dict:
    log.info(f"Starting full plan (invoke mode) — '{user_query[:80]}'")
    initial_state = build_initial_state(user_query)
    result = travel_graph.invoke(initial_state)
    log.info(f"Plan complete — {result['llm_calls']} LLM calls, {len(result['messages'])} agent messages")
    return result


def _merge_update(state: dict, update: dict) -> dict:
    for key, value in update.items():
        if key == "messages":
            state["messages"] = state["messages"] + value
        else:
            state[key] = value

    return state


def stream_travel_plan_events(user_query: str) -> Iterator[dict]:
    """Yield real-time pipeline events as the LangGraph workflow runs."""
    log.info(f"Starting streaming plan — '{user_query[:80]}'")
    state = build_initial_state(user_query)

    yield {
        "type": "start",
        "user_query": user_query,
        "pipeline": PIPELINE_NODES,
    }

    for update in travel_graph.stream(state, stream_mode="updates"):
        for node_name, node_update in update.items():
            state = _merge_update(state, node_update)
            latest_message = state["messages"][-1] if state["messages"] else ""
            log.info(f"  Node '{node_name}' done — {latest_message}")

            yield {
                "type": "step",
                "node": node_name,
                "label": NODE_LABELS.get(node_name, node_name),
                "message": latest_message,
                "llm_calls": state["llm_calls"],
            }

    log.info(f"Streaming complete — {state['llm_calls']} LLM calls")
    yield {"type": "complete", "state": state}
