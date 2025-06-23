"""
Schema Agent

This agent is responsible for database schema exploration tasks such as:
- Listing tables
- Describing table columns
- Viewing schema in JSON format
- Fetching primary and foreign keys
- Checking table size

Used as a sub-agent in a multi-agent ADK database assistant.
"""

from google.adk import Agent
from .prompt import instruction
from .tools.schema_tools import (
    list_tables,
    describe_table,
    get_table_schema_json,
    get_foreign_keys,
    get_primary_keys_for_table,
    get_table_size,
)

schema_agent = Agent(
    name="schema_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[
        list_tables,
        describe_table,
        get_table_schema_json,
        get_foreign_keys,
        get_primary_keys_for_table,
        get_table_size
    ],
)
