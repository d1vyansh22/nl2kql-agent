"""
NL2KQL Agent - A threat intelligence system that converts natural language queries to KQL.

This package provides a modular threat intelligence system built with LangGraph that:
1. Enriches user queries to identify IoCs and context
2. Generates KQL queries from enriched natural language
3. Validates and fixes KQL queries through reflection

Usage:
    from nl2kql_agent.graph import build_graph
    
    app = build_graph()
    result = app.invoke({"user_query": "Find malicious IP 192.168.1.1", "chat_history": [], "retries": 0})
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .graph import build_graph

__all__ = ["build_graph"]
