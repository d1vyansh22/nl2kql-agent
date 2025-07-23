import random
from typing import List
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..llm import get_llm
from ..schemas import schema_as_string
from ..threat_intel_types import ThreatIntelState



class QueryValidator:
    """Validates KQL syntax and semantics, with reflection for fixing."""
    # Removed duplicate __call__ method to resolve method override conflict.

    MAX_RETRIES = 2

    REFLECTION_PROMPT = ChatPromptTemplate.from_messages([
        ("system", """
You are an expert KQL query debugger. A KQL query has failed validation.
Your task is to analyze the provided KQL query, the validation error, and the relevant table schemas.
Based on this information, propose a corrected KQL query.
Ensure the corrected query adheres to KQL syntax and uses correct table and field names from the schema.
Your output MUST be ONLY the corrected KQL query string, without any additional text, explanations, or markdown formatting (e.g., no ```kql).

Original KQL Query:
{original_kql_query}

Validation Error:
{validation_error}

Shortlisted Tables and their Schemas (for context):
{shortlisted_table_schemas}

Enriched Threat Hunting Request (for original intent):
{enriched_query}
        """),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    def __init__(self):
        self.llm = get_llm(temperature=0.5)

    def _simulate_kql_validation(self, kql_query: str, shortlisted_tables: List[str]) -> dict:
        """
        Simulates KQL syntax and semantic validation.
        In a real system, this would call a KQLAnalyzer REST API.
        """
        print(f"\n[Simulating KQL Validation for: {kql_query}]")
        
        # Simulate common errors for demonstration
        if "invalid_field" in kql_query:
            return {"is_valid": False, "error": "Semantic error: 'invalid_field' is not a recognized column."}
        if "missing_pipe" in kql_query:
            return {"is_valid": False, "error": "Syntax error: Missing pipe operator '|' before 'where'."}
        if "non_existent_table" in kql_query:
             return {"is_valid": False, "error": "Semantic error: Table 'non_existent_table' does not exist."}
        
        # Check if the query actually references any of the shortlisted tables
        references_shortlisted_table = False
        for table in shortlisted_tables:
            if table in kql_query:
                references_shortlisted_table = True
                break
        
        if not references_shortlisted_table:
            return {"is_valid": False, "error": "Semantic error: Query does not reference any of the shortlisted tables."}

        # Simulate random success/failure for general queries
        if random.random() < 0.8:  # 80% chance of success
            return {"is_valid": True, "error": None}
        else:
            return {"is_valid": False, "error": "Generic KQL syntax or semantic error (simulated)."}

    def __call__(self, state: ThreatIntelState) -> ThreatIntelState:
        print("\n[Query Validator]")
        
        kql_query = state.get("kql_query", "")
        shortlisted_tables = state.get("shortlisted_tables", [])
        enriched_query = state.get("enriched_query", "")
        retries = state.get("retries", 0)
        chat_history = state.get("chat_history", [])

        validation_result = self._simulate_kql_validation(kql_query, shortlisted_tables)

        if validation_result["is_valid"]:
            print("KQL Query Validated Successfully.")
            state["validation_status"] = "valid"
            state["validation_error"] = ""
            state["retries"] = 0
            if "chat_history" not in state or state["chat_history"] is None:
                state["chat_history"] = []
            state["chat_history"].append(AIMessage(content=f"KQL Validated: {kql_query}"))
            return state
        else:
            print(f"KQL Query Validation Failed: {validation_result['error']}")
            if retries < self.MAX_RETRIES:
                print(f"Attempting to fix query (Retry {retries + 1}/{self.MAX_RETRIES})...")
                
                shortlisted_schemas_str = schema_as_string(shortlisted_tables)
                
                try:
                    msg = self.REFLECTION_PROMPT.format_messages(
                        original_kql_query=kql_query,
                        validation_error=validation_result["error"],
                        shortlisted_table_schemas=shortlisted_schemas_str,
                        enriched_query=enriched_query,
                        chat_history=chat_history
                    )
                    
                    llm_response = self.llm.invoke(msg)
                    
                    fixed_kql_query = ""
                    if isinstance(llm_response.content, str):
                        fixed_kql_query = llm_response.content.strip()
                    else:
                        print(f"Warning: LLM response content for KQL fix is not a string, received type: {type(llm_response.content)}")
                        if isinstance(llm_response.content, list):
                            fixed_kql_query = "".join([part for part in llm_response.content if isinstance(part, str)]).strip()
                        if not fixed_kql_query:
                            raise ValueError("LLM response content is not a parsable string for KQL fix.")

                    print(f"Proposed Fixed KQL Query: {fixed_kql_query}")

                    state["kql_query"] = fixed_kql_query
                    state["validation_status"] = "retrying"
                    state["validation_error"] = validation_result["error"]
                    state["retries"] = retries + 1
                    chat_history = state.get("chat_history", [])
                    chat_history.append(AIMessage(content=f"KQL Fix Attempted: {fixed_kql_query} (Error: {validation_result['error']})"))
                    state["chat_history"] = chat_history
                    
                    return state
                    
                except Exception as e:
                    print(f"An unexpected error occurred during KQL fixing: {e}")
                    state["validation_status"] = "failed"
                    state["validation_error"] = f"Error during KQL fix attempt: {e}"
                    if "chat_history" not in state or state["chat_history"] is None:
                        state["chat_history"] = []
                    state["chat_history"].append(AIMessage(content=f"Error during KQL fix attempt: {e}"))
                    return state
            else:
                print(f"Max retries reached ({self.MAX_RETRIES}). Query remains invalid.")
                state["validation_status"] = "failed"
                state["validation_error"] = validation_result["error"]
                if "chat_history" not in state or state["chat_history"] is None:
                    state["chat_history"] = []
                state["chat_history"].append(AIMessage(content=f"KQL Validation Failed after retries: {kql_query} (Error: {validation_result['error']})"))
                return state
