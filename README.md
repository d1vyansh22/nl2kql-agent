# NL2KQL Agent

A modular threat intelligence system that converts natural language queries into Kusto Query Language (KQL) for security analytics. Built with [LangGraph](https://github.com/langchain-ai/langgraph), this project demonstrates a multi-step workflow for query enrichment, KQL generation, and validation.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture & File Structure](#architecture--file-structure)
- [How the Workflow Connects](#how-the-workflow-connects)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Extending the System](#extending-the-system)
- [License](#license)

---

## Project Overview

**NL2KQL Agent** is designed to:
- Take a user's natural language security query
- Enrich it with context and indicators of compromise (IoCs)
- Generate a valid KQL query for Microsoft Sentinel or similar platforms
- Validate and, if needed, auto-correct the generated KQL

The system is modular, with each step as a node in a LangGraph workflow.

---

## Architecture & File Structure

```
.
├── app.py                  # Demo runner for the workflow
├── config.py               # Loads environment variables (API keys, etc.)
├── export_graphs.py        # Exports the workflow graph as JSON
├── graph.py                # Defines the LangGraph workflow
├── langgraph.json          # Exported graph structure (for visualization)
├── llm.py                  # LLM (Gemini) client setup
├── requirements.txt        # Python dependencies
├── schemas.py              # Security log table schemas
├── threat_intel_types.py   # TypedDict for workflow state
├── tools/
│   ├── enricher.py         # Node: Enriches user queries
│   ├── kql_generator.py    # Node: Generates KQL from enriched queries
│   └── validator.py        # Node: Validates and fixes KQL
└── .env                    # (Not committed) API keys and secrets
```

### File Connections & Responsibilities

- **app.py**: Entry point for running demo scenarios. Imports `build_graph` from `graph.py` and executes the workflow with sample queries.
- **config.py**: Loads environment variables (e.g., `GOOGLE_API_KEY`) using `python-dotenv`. Required for LLM access.
- **export_graphs.py**: Uses `build_graph` to export the workflow's nodes and edges to `langgraph.json` for visualization.
- **graph.py**: Central file that wires together all workflow nodes (`enricher`, `kql_generator`, `kql_validator`) using LangGraph's `StateGraph`. Each node is a class from the `tools/` directory.
- **langgraph.json**: Output of `export_graphs.py`, visualizes the workflow structure (nodes and edges).
- **llm.py**: Singleton Gemini LLM client, used by all nodes that require language model inference.
- **schemas.py**: Contains the schemas for all security log tables, used for context in enrichment and KQL generation.
- **threat_intel_types.py**: Defines `ThreatIntelState`, a `TypedDict` that represents the state passed between nodes.
- **tools/enricher.py**: Implements the `UserQueryEnricher` node. Enriches the user's query, identifies IoCs, and selects relevant tables.
- **tools/kql_generator.py**: Implements the `NL2KQLGenerator` node. Converts enriched queries and table schemas into KQL using the LLM.
- **tools/validator.py**: Implements the `QueryValidator` node. Simulates KQL validation and uses the LLM to auto-correct invalid queries.

---

## How the Workflow Connects

1. **User Input**: A natural language query is provided (via `app.py` or API).
2. **Enricher Node** (`tools/enricher.py`):
   - Enriches the query, extracts IoCs, and selects 4 relevant tables.
   - Output: `enriched_query`, `shortlisted_tables`.
3. **KQL Generator Node** (`tools/kql_generator.py`):
   - Uses the enriched query and table schemas to generate a KQL query.
   - Output: `kql_query`.
4. **Validator Node** (`tools/validator.py`):
   - Simulates KQL validation. If invalid, uses the LLM to suggest a fix.
   - Retries up to 2 times if needed.
   - Output: `validation_status`, `validation_error` (if any).
5. **Graph Structure** (`graph.py`):
   - Nodes are connected in sequence: `enricher` → `kql_generator` → `kql_validator`.
   - Conditional edge: If validation fails and a retry is needed, loops back to `kql_generator`.
   - Success edge: If validation passes, ends the workflow.

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd nl2kql-agent
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Environment Variables (.env)
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 5. Verify Installation
```sh
python app.py
```
You should see demo scenarios run through the workflow, with step-by-step output.

---

## Running & Visualizing the Workflow

- **Run Demo**: `python app.py`
- **Export Graph**: `python export_graphs.py` (generates `langgraph.json`)
- **Visualize**: Use any graph visualization tool that supports JSON (e.g., [Graphviz](https://graphviz.gitlab.io/), [Mermaid](https://mermaid-js.github.io/)).

---

## Extending the System

- **Add New Nodes**: Implement a new class in `tools/`, update `graph.py` to add it to the workflow.
- **Change Table Schemas**: Edit `schemas.py` to add/remove fields or tables.
- **Swap LLMs**: Update `llm.py` and `.env` to use a different provider or model.
- **Integrate with APIs**: Replace the simulated validation in `validator.py` with real KQL validation APIs.

---

## License

MIT License. See `LICENSE` file for details.
