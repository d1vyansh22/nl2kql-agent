from typing import TypedDict, List, Any
from langchain_core.messages import BaseMessage

class ThreatIntelState(TypedDict, total=False):
    """
    Represents the state of our threat intelligence system.

    Attributes:
        user_query (str): The original natural language query from the user.
        enriched_query (str): The enriched query with identified IoCs.
        shortlisted_tables (List[str]): Names of tables selected by the enricher.
        kql_query (str): The generated KQL query.
        validation_status (str): Status of KQL validation (e.g., "valid", "invalid", "retrying").
        validation_error (str): Error message if KQL validation fails.
        retries (int): Number of times a query has been retried after validation failure.
        chat_history (List[BaseMessage]): History of messages for conversational context.
    """
    user_query: str
    enriched_query: str
    shortlisted_tables: List[str]
    kql_query: str
    validation_status: str
    validation_error: str
    retries: int
    chat_history: List[BaseMessage]
