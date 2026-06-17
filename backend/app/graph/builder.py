from langgraph.graph import StateGraph, START, END

from app.graph.state import TravelState
from app.graph.nodes import (
    request_parser_node,
    flight_agent_node,
    hotel_agent_node,
    itinerary_agent_node,
    final_agent_node,
    budget_agent_node,
)


def build_graph():
    graph_builder = StateGraph(TravelState)

    graph_builder.add_node("request_parser", request_parser_node)
    graph_builder.add_node("flight_agent", flight_agent_node)
    graph_builder.add_node("hotel_agent", hotel_agent_node)
    graph_builder.add_node("budget_agent", budget_agent_node)
    graph_builder.add_node("itinerary_agent", itinerary_agent_node)
    graph_builder.add_node("final_agent", final_agent_node)

    graph_builder.add_edge(START, "request_parser")
    graph_builder.add_edge("request_parser", "flight_agent")
    graph_builder.add_edge("flight_agent", "hotel_agent")
    graph_builder.add_edge("hotel_agent", "budget_agent")
    graph_builder.add_edge("budget_agent", "itinerary_agent")
    graph_builder.add_edge("itinerary_agent", "final_agent")
    graph_builder.add_edge("final_agent", END)

    return graph_builder.compile()


travel_graph = build_graph()