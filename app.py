from .graph import build_graph
from .threat_intel_types import ThreatIntelState


def run_demo():
    """Run demonstration scenarios for the threat intelligence system."""
    app = build_graph()

    scenarios = [
        "Find activities related to malicious IP address 192.168.1.1",
        "Investigate phishing email from attacker@evil.com",
        "Analyze activities related to suspicious file hash abcdef123456",
    ]

    print("--- Threat Intelligence System Demo ---")
    
    for i, query in enumerate(scenarios, 1):
        print(f"\n=== Example {i}: {query} ===")
        
        initial_state: ThreatIntelState = {
            "user_query": query,
            "enriched_query": "",
            "shortlisted_tables": [],
            "kql_query": "",
            "validation_status": "",
            "validation_error": "",
            "retries": 0,
            "chat_history": []
        }
        
        try:
            result = app.invoke(initial_state)
            
            print("\n--- Final Results ---")
            print(f"User Query: {result['user_query']}")
            print(f"Enriched Query: {result['enriched_query']}")
            print(f"Shortlisted Tables: {result['shortlisted_tables']}")
            print(f"Final KQL Query: {result['kql_query']}")
            print(f"Validation Status: {result['validation_status']}")
            if result.get('validation_error'):
                print(f"Validation Error: {result['validation_error']}")
            print(f"Retries: {result.get('retries', 0)}")
            
        except Exception as e:
            print(f"Error processing query: {e}")
        
        print("-" * 80)


if __name__ == "__main__":
    run_demo()
