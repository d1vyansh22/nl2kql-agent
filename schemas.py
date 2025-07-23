from typing import List, Tuple, Dict

# Define the schemas for the security log tables
TABLE_SCHEMAS: Dict[str, List[Tuple[str, str]]] = {
    "PassiveDNS": [("ip", "string"), ("domain", "string")],
    "InboundBrowsing": [
        ("timestamp", "string"), ("timestamp_1", "datetime"), ("method", "string"), 
        ("src_ip", "string"), ("user_agent", "string"), ("url", "string")
    ],
    "ProcessEvents": [
        ("timestamp", "string"), ("timestamp_1", "datetime"), ("parent_process_name", "string"), 
        ("parent_process_hash", "string"), ("process_commandline", "string"), ("process_name", "string"), 
        ("process_hash", "string"), ("hostname", "string")
    ],
    "Email": [
        ("sender", "string"), ("event_time", "string"), ("event_time_1", "datetime"), 
        ("reply_to", "string"), ("recipient", "string"), ("subject", "string"), 
        ("accepted", "bool"), ("accepted_1", "string"), ("link", "guid"), 
        ("link", "string"), ("recipient", "string")
    ],
    "OutBoundBrowsing": [
        ("timestamp", "string"), ("timestamp_1", "datetime"), ("method", "string"), 
        ("src_ip", "string"), ("user_agent", "string"), ("url", "string")
    ],
    "FileCreationEvents": [
        ("timestamp", "string"), ("timestamp_1", "datetime"), ("hostname", "string"), 
        ("sha256", "string"), ("path", "string"), ("filename", "string"), 
        ("size", "int"), ("size_1", "real")
    ],
    "Employees": [
        ("name", "string"), ("timestamp", "datetime"), ("user_agent", "string"), 
        ("ip_addr", "string"), ("email_addr", "string"), ("company_domain", "string"), 
        ("username", "string"), ("role", "string"), ("hostname", "string")
    ],
    "IAM": [
        ("Action", "string"), ("HostName", "string"), ("Source_IP", "string"), 
        ("SourceIP_Location", "string"), ("TargetResource", "string"), ("Timestamp", "string"), 
        ("UserName", "string"), ("UserAgent", "string")
    ],
    "AuthenticationEvents": [
        ("hostname", "string"), ("password_hash", "guid"), ("result", "string"), 
        ("src_ip", "string"), ("timestamp", "string"), ("timestamp_1", "datetime"), 
        ("user_agent", "string"), ("username", "string")
    ]
}

ALL_TABLE_NAMES = list(TABLE_SCHEMAS.keys())


def schema_as_string(table_names: List[str]) -> str:
    """
    Generates a string representation of the schema for given tables.
    """
    schema_str = ""
    for table_name in table_names:
        if table_name in TABLE_SCHEMAS:
            schema_str += f"\nTable: {table_name}\nFields:\n"
            for field, f_type in TABLE_SCHEMAS[table_name]:
                schema_str += f"- {field} ({f_type})\n"
        else:
            schema_str += f"\nWarning: Schema for table '{table_name}' not found.\n"
    return schema_str
