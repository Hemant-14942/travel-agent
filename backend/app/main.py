from app.services.travel_planner import build_initial_state, generate_travel_plan


GRAPH_FLOW = [
    "START",
    "Request Parser",
    "Flight Agent",
    "Hotel Agent",
    "Budget Agent",
    "Itinerary Agent",
    "Final Agent",
    "END",
]


def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_graph_flow():
    print_section("LANGGRAPH EXECUTION FLOW")
    print(" -> ".join(GRAPH_FLOW))


def print_agent_trace(messages: list[str]):
    print_section("AGENT EXECUTION TRACE")

    for index, message in enumerate(messages, start=1):
        print(f"{index}. {message}")


def print_options(title: str, options: list[dict]):
    print_section(title)

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")


initial_state = build_initial_state(
    "Plan a 7-day Japan trip from Delhi under 2 lakhs"
)

print_graph_flow()

print_section("INPUT STATE")
print(f"User query: {initial_state['user_query']}")
print("Initial LLM calls:", initial_state["llm_calls"])

result = generate_travel_plan(initial_state["user_query"])

print_agent_trace(result["messages"])

print_section("PARSED REQUEST")
print(result["parsed_request"])

print_options("STRUCTURED FLIGHT OPTIONS", result["flight_options"])
print_options("STRUCTURED HOTEL OPTIONS", result["hotel_options"])

print_section("FORMATTED FLIGHT RESULT")
print(result["flight_result"])

print_section("FORMATTED HOTEL RESULT")
print(result["hotel_result"])

print_section("BUDGET RESULT")
print(result["budget_result"])

print_section("LLM CALL COUNT")
print(result["llm_calls"])

print_section("FINAL PLAN")
print(result["final_plan"])