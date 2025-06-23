# db_agent/__init__.py

from google.adk import Agent
from .agent_config import global_instruction, instruction

from .tools.db_tools import ( # Assuming db_tools.py is directly in the tools directory
    run_query,
    list_tables,
    describe_table,
    search_in_table,
    count_rows,
    get_table_schema_json,
    get_foreign_keys,
    get_table_size,
    run_custom_sql,
    top_k_column_values,
    numeric_column_stats,
    time_series_summary,
    compute_correlation,
    get_latest_entries_from_table,
    get_primary_keys_for_table,
)

from .tools.nl2sql_tool import convert_to_sql

root_agent = Agent(
    name="db_agent",
    model="gemini-2.0-flash",
    global_instruction=global_instruction,
    instruction=instruction,
    tools=[
        run_query,
        list_tables,
        describe_table,
        search_in_table,
        count_rows,
        get_table_schema_json,
        get_foreign_keys,
        get_table_size,
        run_custom_sql,
        top_k_column_values,
        numeric_column_stats,
        time_series_summary,
        get_latest_entries_from_table,
        compute_correlation,
        get_primary_keys_for_table,
        convert_to_sql,
    ]
)

# If you prefer to have a function to get the agent instance:
def create_agent():
    return root_agent