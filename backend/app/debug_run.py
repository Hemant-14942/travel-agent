from app.graph.builder import travel_graph
from app.services.travel_planner import build_initial_state


def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_state_summary(state: dict):
    print(f"user_query: {state['user_query']}")
    print(f"parsed request: {state['parsed_request']}")
    print(f"flight options count: {len(state['flight_options'])}")
    print(f"hotel options count: {len(state['hotel_options'])}")
    print(f"has budget result: {bool(state['budget_result'])}")
    print(f"has itinerary: {bool(state['itinerary'])}")
    print(f"has final plan: {bool(state['final_plan'])}")
    print(f"llm calls: {state['llm_calls']}")
    print(f"messages count: {len(state['messages'])}")

    if state["messages"]:
        print(f"latest message: {state['messages'][-1]}")


initial_state = build_initial_state(
    "Plan a 7-day Japan trip from Delhi under 2 lakhs"
)


print_section("LANGGRAPH STREAM DEBUG")
print("This run shows the full state after each graph step.")

for step_number, state_snapshot in enumerate(
    travel_graph.stream(initial_state, stream_mode="values"),
    start=1,
):
    print_section(f"STATE SNAPSHOT #{step_number}")
    print_state_summary(state_snapshot)