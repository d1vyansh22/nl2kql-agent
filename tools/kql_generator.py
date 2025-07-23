
## 8. nl2kql_agent/tools/kql_generator.py
from typing import List
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..llm import get_llm
from ..schemas import schema_as_string
from ..threat_intel_types import ThreatIntelState



class NL2KQLGenerator:
    """Generates KQL queries from enriched natural language queries."""
    # Removed duplicate __call__ method to resolve method name conflict.

    PROMPT = ChatPromptTemplate.from_messages([
        ("system", """
You are an expert in Kusto Query Language (KQL) and a security analyst.
Your task is to generate a semantically correct KQL query based on the provided enriched threat hunting request and the schemas of the shortlisted tables.
Focus on extracting the relevant information from the tables using appropriate KQL operators (e.g., `where`, `contains`, `has`, `startswith`, `endswith`, `project`, `join`).
Ensure the query uses the exact table and field names as provided in the schema.
If multiple tables are shortlisted, consider if a `union` or `join` operation is appropriate, or if separate queries are needed. For simplicity, prioritize single table queries first, then consider `union` if the request clearly spans multiple tables for the same type of data.

Shortlisted Tables and their Schemas:
{shortlisted_table_schemas}

Enriched Threat Hunting Request:
{enriched_query}

Your output MUST be ONLY the KQL query string, without any additional text, explanations, or markdown formatting (e.g., no ```kql).
        """),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    def __init__(self):
        self.llm = get_llm(temperature=0.2)

    def __call__(self, state: ThreatIntelState) -> ThreatIntelState:
        print("\n[KQL Generator]")
        # Use .get() for all optional keys to avoid KeyError
        enriched_query = state.get("enriched_query", "")
        shortlisted_tables = state.get("shortlisted_tables", [])
        chat_history = state.get("chat_history", [])

        shortlisted_schemas_str = schema_as_string(shortlisted_tables)

        try:
            msg = self.PROMPT.format_messages(
                shortlisted_table_schemas=shortlisted_schemas_str,
                enriched_query=enriched_query,
                chat_history=chat_history
            )
            llm_response = self.llm.invoke(msg)
            kql_query = ""
            if isinstance(llm_response.content, str):
                kql_query = llm_response.content.strip()
            else:
                print(f"Warning: LLM response content for KQL generation is not a string, received type: {type(llm_response.content)}")
                if isinstance(llm_response.content, list):
                    kql_query = "".join([part for part in llm_response.content if isinstance(part, str)]).strip()
                if not kql_query:
                    raise ValueError("LLM response content is not a parsable string for KQL.")

            print(f"Generated KQL Query: {kql_query}")

            state["kql_query"] = kql_query
            state["validation_status"] = "pending"
            if "chat_history" not in state or state["chat_history"] is None:
                state["chat_history"] = []
            state["chat_history"].append(AIMessage(content=f"Generated KQL: {kql_query}"))
            return state
        except Exception as e:
            print(f"An unexpected error occurred during KQL generation: {e}")
            state["kql_query"] = f"Error generating KQL: {e}"
            state["validation_status"] = "failed"
            state["validation_error"] = str(e)
            if "chat_history" not in state or state["chat_history"] is None:
                state["chat_history"] = []
            state["chat_history"].append(AIMessage(content=f"Error generating KQL: {e}"))
            return state
