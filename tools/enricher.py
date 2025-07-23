
import json
import random
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..llm import get_llm
from ..schemas import schema_as_string, ALL_TABLE_NAMES
from ..threat_intel_types import ThreatIntelState


class UserQueryEnricher:
    """Enriches a user query and picks four tables."""

    PROMPT = ChatPromptTemplate.from_messages([
        ("system", """
You are an expert threat intelligence analyst. Your task is to enrich a natural language user query into a precise threat hunting request.
Identify potential Indicators of Compromise (IoCs) like IP addresses, domains, hashes, or email addresses from the user query.
Based on the identified IoCs and the nature of the request, shortlist exactly 4 relevant security log tables from the following available tables.
For each shortlisted table, explain why it's relevant.

Available Security Log Tables and their schemas:
{table_schemas}

Your output MUST be a JSON object with two keys:
1. "enriched_query": A detailed threat hunting request based on the user's query, specifying the IoCs and the type of activity to look for.
2. "shortlisted_tables": A JSON array of the 4 selected table names.

Example Input: "Find activities related to malicious IP address 192.168.1.1"
Example Output:
{{
    "enriched_query": "Identify network connections and associated processes linked to the malicious IP address 192.168.1.1.",
    "shortlisted_tables": ["InboundBrowsing", "OutBoundBrowsing", "ProcessEvents", "AuthenticationEvents"]
}}
        """),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    def __call__(self, state: ThreatIntelState) -> ThreatIntelState:
        # Real implementation (if not already present, add logic here)
        # This is a placeholder; actual enrichment logic should be implemented.
        return state
