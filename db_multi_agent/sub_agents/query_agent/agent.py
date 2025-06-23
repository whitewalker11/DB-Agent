"""
Query Agent

This agent handles data-focused query tasks such as:
- Running SELECT queries
- Performing search/filter in tables
- Getting row counts and summaries
- Time series and correlation analysis
- Fetching latest entries

Used as a sub-agent in a multi-agent ADK database assistant.
"""

from google.adk import Agent
from .prompt import instruction
from .tools.query_tools import (
    run_query,
    run_custom_sql,
    search_in_table,
    count_rows,
    top_k_column_values,
    numeric_column_stats,
    time_series_summary,
    compute_correlation,
    get_latest_entries_from_table,
)

query_agent = Agent(
    name="query_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[
        run_query,
        run_custom_sql,
        search_in_table,
        count_rows,
        top_k_column_values,
        numeric_column_stats,
        time_series_summary,
        compute_correlation,
        get_latest_entries_from_table
    ],
)
