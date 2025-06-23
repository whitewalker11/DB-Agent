
# 🤖 DB Agent - Conversational PostgreSQL Assistant

Welcome to the **DB Agent**, a powerful conversational AI interface that allows you to interact with your **PostgreSQL database** using **natural language queries**. Built using **Google's Agent Development Kit (ADK)**, this agent bridges the gap between human language and database operations.

---

## 🔧 What is the Agent Development Kit (ADK)?

The **Agent Development Kit (ADK)** by Google is a framework to build smart, modular AI agents powered by **LLMs** (like Gemini). It simplifies the agent-building process, making tools easier to create, invoke, and manage.

---

## 🧠 Architecture Overview

The agent architecture supports both single-agent and multi-agent setups, where sub-agents may handle specialized responsibilities:

- **RootAgent**: Orchestrates communication and delegates tasks to sub-agents (in multi-agent setups).
- **Sub Agents** (optional):
  - Query, Schema, Analysis, or Visual sub-agents
- **Tools**: Encapsulated Python functions that interact with the database and return results to the user.

---

## 🗂 Project Structure (Generic)

```
db_agent/
├── agent.py                 # Root agent definition
├── config.py                # DB configuration
├── __init__.py
├── prompt.py
├── tools/
│   ├── db_tools.py
│   ├── nl2sql_tool.py
│   ├── schema_tools.py
│   ├── analysis_tools.py
│   └── visual_tools.py
```

---

## ⚙️ Setup Instructions

### 🔐 Configuration

Update your `config.py` with PostgreSQL connection details:

```python
DB_CONFIG = {
    "host": "your-db-host",
    "database": "your-db-name",
    "user": "your-db-user",
    "password": "your-db-password",
    "port": 5432
}
```

---

### 📦 Installation

```bash
pip install google-adk psycopg2-binary openai
```

---

## 🚀 Run Agent

```bash
adk run db_agent
# or
adk web db_agent
```

---

## 🔍 Example Interactions

- "List all tables" → `list_tables()`
- "Describe the users table" → `describe_table("users")`
- "Find correlation between age and income" → `compute_correlation("users", "age", "income")`
- "Show total sales over time" → Visualization tools

---

## 🚀 Tools Available

### 🔢 Basic Querying

- `run_query(query: str)`
- `run_custom_sql(query: str)`

### 📄 Schema Introspection

- `list_tables()`
- `describe_table(table_name)`
- `get_foreign_keys(table_name)`
- `get_primary_keys_for_table(table_name)`
- `get_table_schema_json(table_name)`

### 📊 Data Exploration

- `count_rows(table)`
- `search_in_table(table, column, value)`
- `top_k_column_values(table, column)`
- `numeric_column_stats(table, column)`
- `time_series_summary(table, date_column, agg_column)`
- `compute_correlation(table, col1, col2)`

### 📦 Monitoring

- `get_table_size(table)`
- `get_latest_entries_from_table(table)`

### 🧠 NL → SQL Tool (OpenAI)

- `convert_to_sql(nl_query: str, table_context: Optional[str])`

---

## 🌍 Use Cases

- SQL-less business intelligence
- Conversational database bots
- Data exploration by non-technical users
- Automated reports and dashboards

---

## 🎉 Summary

The **DB Agent** transforms your database into a smart assistant. Whether you're building a single-agent or multi-agent system, it provides modular tools and natural language understanding using LLMs, ideal for modern data workflows.
