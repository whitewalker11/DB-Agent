
# 🤖 Multi-Agent DB Assistant

This project demonstrates an intelligent and modular PostgreSQL assistant powered by Google's Agent Development Kit (ADK) and Gemini. This system enables natural language interaction with your database using specialized sub-agents, each with dedicated tools and responsibilities for a more robust and scalable architecture.

---

## 🧠 Architecture Overview

The architecture is divided into a root agent that orchestrates tasks and several sub-agents that handle specialized functions:

### RootAgent:
- The entry point for all user requests.
- Interprets the user's intent and delegates the task to the most appropriate sub-agent.

### Sub-Agents:
- **QueryAgent**: Converts natural language to SQL and runs safe database queries.
- **SchemaAgent**: Explores and describes the database schema (tables, columns, keys, etc.).
- **AnalysisAgent**: Performs data analysis, calculates statistics, and extracts insights.
- **VisualAgent**: Generates visualizations like bar plots, time series charts, and more based on the data.

Each sub-agent uses its own dedicated suite of tools (e.g., `DbqueryTools`, `SchemaTools`) to perform its role effectively.

---

## 🗂️ Project Structure

```
db_multi_agent/
├── agent.py                 # Root agent definition
├── config.py                # Database and API key configuration
├── __init__.py
├── prompt.py                # Prompts for the root agent
└── sub_agents/
    ├── query_agent/
    │   ├── agent.py
    │   ├── prompt.py
    │   └── tools/
    │       ├── db_tools.py
    │       └── nl2sql_tool.py
    ├── schema_agent/
    │   ├── agent.py
    │   ├── prompt.py
    │   └── tools/
    │       └── schema_tools.py
    ├── analysis_agent/
    │   ├── agent.py
    │   ├── prompt.py
    │   └── tools/
    │       └── analysis_tools.py
    └── visual_agent/
        ├── agent.py
        ├── prompt.py
        └── tools/
            └── visual_tools.py
```

---

## ⚙️ Setup Instructions

### Configuration

Update your `config.py` with PostgreSQL connection details and your OpenAI API key if you plan to use the natural language to SQL tool.

```python
# config.py

# PostgreSQL Database Configuration
DB_CONFIG = {
    "host": "your-db-host",
    "database": "your-db-name",
    "user": "your-db-user",
    "password": "your-db-password",
    "port": 5432
}

# OpenAI API Key for the nl2sql_tool
OPENAI_KEY = "your-openai-key"
```

**Security Note**: For production, always use environment variables or a dedicated secret management service.

### Installation

```bash
pip install google-adk psycopg2-binary openai
```

### Run the Agent

You can run the agent from your terminal or launch the web interface.

**Terminal Mode:**

```bash
cd db_multi_agent/
adk run db_multi_agent
```

**Web Mode:**

```bash
adk web db_multi_agent
# Visit http://localhost:8080 in your browser
```

---

## 🔍 Example Interactions

The RootAgent will automatically delegate these requests to the correct sub-agent:

- **User**: "List all tables in the database."  
  **Action**: RootAgent → SchemaAgent → `list_tables()`

- **User**: "Describe the users table."  
  **Action**: RootAgent → SchemaAgent → `describe_table("users")`

- **User**: "Tell me who are the top 5 customers by sales."  
  **Action**: RootAgent → QueryAgent → `convert_to_sql()` → `run_query()`

- **User**: "Find the correlation between age and income in the customers table."  
  **Action**: RootAgent → AnalysisAgent → `compute_correlation("customers", "age", "income")`

- **User**: "Show me total sales over time as a line chart."  
  **Action**: RootAgent → VisualAgent → `visualize_time_series(...)`

---

## 📈 Ideal Use Cases

This multi-agent architecture is particularly well-suited for:

- **Advanced Business Intelligence**: Complex, multi-step queries requiring analysis and visualization.
- **Automated Data Insights**: Systems that proactively analyze and surface insights.
- **Data Exploration for Non-Technical Users**: A safe, intuitive interface to query data.
- **Automated Reporting and Visual Dashboards**: Generate visual reports and charts via conversation.

Feel free to expand the agents or add new tools to fit your specific project needs!
