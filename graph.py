from langgraph.graph import StateGraph, END
from .tools.enricher import UserQueryEnricher
from .tools.kql_generator import NL2KQLGenerator
from .tools.validator import QueryValidator
from .threat_intel_types import ThreatIntelState

def build_graph():
    g = StateGraph(ThreatIntelState)
    g.add_node("enricher", UserQueryEnricher())
    g.add_node("kql_generator", NL2KQLGenerator())
    g.add_node("kql_validator", QueryValidator())

    g.set_entry_point("enricher")
    g.add_edge("enricher", "kql_generator")
    g.add_edge("kql_generator", "kql_validator")
    g.add_conditional_edges(
        "kql_validator",
        lambda s: "kql_generator" if s["validation_status"] == "retrying" else END,
    )
    return g.compile()
