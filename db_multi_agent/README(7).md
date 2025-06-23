
# 🤖 Multi-Agent DB Assistant

An intelligent and modular PostgreSQL assistant powered by **Google's Agent Development Kit (ADK)** and **Gemini**. This system enables natural language interaction with your database using specialized **sub-agents**, each with dedicated tools and responsibilities.

![System Diagram](./Flowcharts%20(1).png)

---

## 🧠 Architecture Overview

The architecture is divided into a root agent and several sub-agents:

- **RootAgent**: Orchestrates communication and delegates tasks to sub-agents.
- **Sub Agents**:
  - `Query Agent`: Converts natural language to SQL and runs queries.
  - `Schema Agent`: Explores and describes the database schema.
  - `Analysis Agent`: Performs data insights, summarization, and stats.
  - `Visual Agent`: Generates visualizations like bar plots, time series, etc.

Each sub-agent uses its respective **Tool Suite** (e.g., `DbqueryTools`, `SchemaTools`) to interact with the database.

---

## 🗂 Project Structure

```
db_multi_agent/
├── agent.py                 # Root agent definition
├── config.py                # Database config
├── __init__.py
├── prompt.py
├── sub_agents/
│   ├── query_agent/
│   │   ├── agent.py
│   │   ├── prompt.py
│   │   └── tools/
│   │       ├── db_tools.py
│   │       └── nl2sql_tool.py
│   ├── schema_agent/
│   │   ├── agent.py
│   │   ├── prompt.py
│   │   └── tools/
│   │       └── schema_tools.py
│   ├── analysis_agent/
│   │   └── tools/
│   │       └── analysis_tools.py
│   └── visual_agent/
│       └── tools/
│           └── visual_tools.py
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

Set OpenAI key (if using `nl2sql_tool.py`):

```python
OPENAI_KEY = "your-openai-key"
```

---

### 📦 Installation

```bash
pip install google-adk psycopg2-binary openai
```

---

## 🚀 Run Agent

### Terminal Mode

```bash
cd db_multi_agent/
adk run db_multi_agent
```

### Web Mode

```bash
adk web db_multi_agent
# Visit http://localhost:8080
```

---

## 🔍 Example Interactions

- *User:* "List all tables" → Uses `list_tables()`
- *User:* "Describe the users table" → Uses `describe_table("users")`
- *User:* "Find correlation between age and income" → Uses `compute_correlation("users", "age", "income")`
- *User:* "Show total sales over time" → Uses `visualize_time_series(...)`

---

## 📈 Ideal Use Cases

- SQL-less business intelligence
- Auto-insights from large datasets
- Data exploration by non-technical users
- Automated reporting and visual dashboards

> Feel free to expand the agents or tools as per your project needs!
