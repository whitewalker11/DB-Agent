
# 🤖 DB Agent (Single-Agent) - Conversational PostgreSQL Assistant

Welcome to the Single-Agent DB Agent, a powerful conversational AI that allows you to interact with your PostgreSQL database using natural language. Built with Google's Agent Development Kit (ADK) and powered by Gemini, this agent makes data exploration as simple as having a conversation.

---

## 🔧 What is the Agent Development Kit (ADK)?

The Agent Development Kit (ADK) by Google is a framework to build smart, modular AI agents powered by LLMs. It simplifies the agent-building process, making tools easier to create, invoke, and manage.

### Key Advantages:
✅ Abstracts LLM Logic: No need to manage complex LLM orchestration.  
📊 Modular Tooling: Tools are clean, reusable Python functions.  
🤖 Intelligent Reasoning: The LLM decides when to invoke which tool.  
🌎 Deployment-Ready: Easily plug into production.

---

## 🔍 How It Works

1. User asks a question (e.g., "How many users signed up last month?").
2. The LLM interprets the request and routes it to the correct tool.
3. The tool queries the database using psycopg2.
4. The output is returned, parsed, and sent back to the user in a readable format.

---

## 🔹 Project Structure

```
DBAgent/
├── db_agent/
│   ├── config.py               # DB configuration (host, user, etc.)
│   ├── __init__.py             # Root agent definition
│   ├── agent.py                # (Optional) Duplicate of __init__.py
│   ├── test_conn.py            # Connection testing script
│   └── tools/
│       ├── __init__.py
│       ├── db_tools.py         # Core tool functions
│       └── nl2sql_tool.py      # Natural language to SQL tool (optional)
```

---

## 🚀 Tools Available to the Agent

### 🔢 Basic Querying
- `run_query(query: str)`
- `run_custom_sql(query: str)`

### 📄 Schema Introspection
- `list_tables()`
- `describe_table(table_name: str)`
- `get_table_schema_json(table_name: str)`
- `get_primary_keys_for_table(table_name: str)`
- `get_foreign_keys(table_name: str)`

### 📊 Data Exploration
- `count_rows(table: str)`
- `search_in_table(table, column, value)`
- `top_k_column_values(table, column, k=5)`
- `numeric_column_stats(table, column)`
- `time_series_summary(table, date_column, agg_column)`
- `compute_correlation(table, col1, col2)`

### 🔍 Monitoring
- `get_table_size(table: str)`
- `get_latest_entries_from_table(table: str)`

### 🧠 Natural Language to SQL (Optional, via OpenAI GPT-4)
Tool: `convert_to_sql(nl_query: str, table_context: Optional[str])`

---

## 🎓 Sample Agent Definition (`__init__.py`)

```python
from google.adk import Agent
from .tools.db_tools import *

root_agent = Agent(
    name="db_agent",
    model="gemini-2.0-flash",
    global_instruction="You are a helpful database assistant.",
    instruction="Use tools only when necessary. Respond concisely.",
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
        compute_correlation,
        get_latest_entries_from_table,
        get_primary_keys_for_table,
    ]
)
```

---

## 🚪 Setup Instructions

### Configure Database Connection
Update `config.py` with your PostgreSQL credentials.

```python
# config.py
DB_CONFIG = {
    "host": "localhost",
    "database": "your_db",
    "user": "postgres",
    "password": "your_pass",
    "port": "5432"
}
```

⚠️ **Note**: Use environment variables or a secret manager in production!

---

### Installation

```bash
pip install google-adk psycopg2-binary openai
gcloud auth application-default login  # if needed for LLM access
```

---

### Running the Agent

**Terminal Mode:**
```bash
cd db_agent/
adk run db_agent
```

**Web Interface (Optional):**
```bash
adk web db_agent
# Then visit http://localhost:8080
```

---

## 💬 Sample Interactions (Try These!)

- "What tables are in the database?"
- "Describe the employees table."
- "How many rows are in the products table?"
- "Show me the first 5 entries from the orders table."
- "Find all employees named 'John' in the employees table under the name column."
- "Give me the schema for the products table as JSON."
- "What's the size of the orders table?"
- "Are there any foreign keys in the orders table?"
- "What are the most common product categories?"
- "What are the statistics for the price column in the products table?"
- "Show me the latest order."
- "What are the primary keys for the employees table?"

---

## 🎉 Summary

The Single-Agent DB Agent turns your database into an intelligent assistant. With ADK, modular tools, and the power of Gemini, it makes exploring data as easy as chatting. Perfect for analysts, engineers, or anyone who wants smart, immediate access to data.
