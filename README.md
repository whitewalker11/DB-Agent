# 🤖 **DB Agent - Conversational PostgreSQL Assistant**

Welcome to the **DB Agent**, a powerful conversational AI interface that allows you to interact with your **PostgreSQL database** using **natural language queries**. Built using **Google's Agent Development Kit (ADK)**, this agent bridges the gap between human language and database operations.

---
## 🔧 What is ADK?

The **Agent Development Kit (ADK)** by **Google** is a powerful open-source framework that enables developers to build **modular, intelligent agents** using **Large Language Models (LLMs)** like **Gemini**. ADK abstracts away the complexity of tool orchestration, prompt engineering, and reasoning, making it easier to deploy LLM-powered systems into production.

---

## 🧠 What is the DB Agent?

One of the most practical applications of ADK is the **Database Agent (DB Agent)** — a conversational assistant that allows users to interact with a **PostgreSQL database** using **natural language**.

### ✨ What DB Agent Can Do:
- Understand questions like “How many users signed up last week?”
- Automatically generate and execute **read-only SQL queries**
- Return human-friendly summaries of the result
- Ensure safety by limiting query types and access

---

## ✅ Key Advantages of ADK

| Feature                  | Description |
|--------------------------|-------------|
| 🔍 Abstracts LLM Logic   | No manual prompting or chaining — just tools and intent |
| 🛠️ Modular Tooling       | Tools are simple, clean Python functions |
| 🧠 Intelligent Reasoning  | The LLM chooses the right tool at the right time |
| 🚀 Deployment-Ready       | Built-in support for production use cases |

---

## 🔄 How It Works

1. **User Input**:  
   > _“List all active users from last month”_

2. **LLM Agent**:  
   - Parses the natural language query  
   - Selects the appropriate tool

3. **Tool Execution**:  
   - Constructs SQL using `psycopg2`  
   - Executes read-only query securely

4. **Response**:  
   - Parses the result  
   - Returns a friendly response to the user

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

- `run_query(query: str)` - Run **safe** SELECT queries
- `run_custom_sql(query: str)` - Run EXPLAIN/SHOW (non-destructive only)

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


### 🧠 Natural Language to SQL (via OpenAI GPT-4)

You can enable natural language to SQL conversion by integrating the `nl2sql_tool.py` module using OpenAI's GPT-4.

#### 🛠 Tool: `convert_to_sql(nl_query: str, table_context: Optional[str])`

This tool translates natural language queries into executable **PostgreSQL SELECT** queries using an OpenAI LLM.

#### 🔍 How It Works

1. The user types a question like:
   > “Show total sales grouped by product category from last year.”
2. The tool invokes GPT-4 and provides optional **table schema context**.
3. GPT-4 responds with a SQL SELECT query.
4. The query is sanitized, validated, and returned for execution.

#### ✅ Features

- Supports only **safe SELECT queries**
- Automatically strips formatting (e.g., markdown blocks)
- Useful for non-technical users or rapid prototyping
---

## 🎓 Sample Agent Definition (in `__init__.py`)

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



### 📂 `config.py` Example

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "your_db",
    "user": "postgres",
    "password": "your_pass",
    "port": "5432"
}
```

> ⚠️ **Note**: Use environment variables or secret managers in production!

### ➔ Installation

```bash
pip install google-adk psycopg2-binary
gcloud auth application-default login  # if needed for LLM access
```

---

## 🌐 Running the Agent

### 💾 Terminal Mode

```bash
cd db_agent/
adk run db_agent
```

### 🎨 Web Interface (Optional)

```bash
adk web db_agent
# Then visit http://localhost:8080
```

---

## 🌍 Use Cases

- Business analytics with no SQL knowledge
- Internal database monitoring bots
- Quick schema introspection
- Data-driven dashboards and assistants

---


### 💬 Sample Interactions (Try These!)

Once your agent is live, interact with it via natural language prompts:

#### 📋 List all tables

**User:** What tables are in the database?\
**Agent:** `employees, products, orders`\
➡️ *(Uses **`list_tables`** tool)*

---

#### 🧾 Describe a table

**User:** Describe the `employees` table.\
**Agent:**

```
Column    | Type    | Nullable
----------|---------|---------
id        | integer | NO
name      | text    | NO
```

➡️ *(Uses **`describe_table`** tool)*

---

#### 🔢 Count rows in a table

**User:** How many rows are in the `products` table?\
**Agent:** `Table 'products' contains 150 rows.`\
➡️ *(Uses **`count_rows`** tool)*

---

#### 🔍 Run a SELECT query

**User:** Show me the first 5 entries from the `orders` table.\
**Agent:** *(Returns formatted result of **`SELECT * FROM orders LIMIT 5;`**)*\
➡️ *(Uses **`run_query`** tool)*

---

#### 🔎 Search for a value

**User:** Find all employees named 'John' in the `employees` table under the `name` column.\
**Agent:** *(Returns matching rows)*\
➡️ *(Uses **`search_in_table`** tool)*

---

#### 🧬 Get table schema in JSON

**User:** Give me the schema for the `products` table as JSON.\
**Agent:**

```json
[
  {"column": "id", "type": "integer", "nullable": false},
  {"column": "product_name", "type": "text", "nullable": false}
]
```

➡️ *(Uses **`get_table_schema_json`** tool)*

---

#### 📦 Check table size

**User:** What's the size of the `orders` table?\
**Agent:** `Table 'orders' size: 1.5 MB`\
➡️ *(Uses **`get_table_size`** tool)*

---

#### 🔗 Find foreign keys

**User:** Are there any foreign keys in the `orders` table?\
**Agent:**

```
Constraint                | Column      | References
--------------------------|-------------|-----------------
orders_customer_id_fkey   | customer_id | customers.id
```

➡️ *(Uses **`get_foreign_keys`** tool)*

---

#### 🏷️ Top values in a column

**User:** What are the most common product categories in the `products` table?\
**Agent:**

```
Electronics: 50
Books: 30
Clothing: 20
```

➡️ *(Uses **`top_k_column_values`** tool)*

---

#### 📊 Numeric column stats

**User:** What are the statistics for the `price` column in the `products` table?\
**Agent:**

```
Mean: 125.75
Median: 100.00
Std Dev: 50.22
Min: 10.00
Max: 500.00
```

➡️ *(Uses **`numeric_column_stats`** tool)*

---

#### 🆕 Latest entry

**User:** Show me the latest order from the `orders` table.\
**Agent:** *(Returns the latest row from **`orders`**)*\
➡️ *(Uses **`get_latest_entries_from_table`** tool)*

---

#### 🔑 Get primary keys

**User:** What are the primary keys for the `employees` table?\
**Agent:** `Primary key columns for 'employees': id`\
➡️ *(Uses **`get_primary_keys_for_table`** tool)*

---




## 🎉 Summary

The **DB Agent** turns your database into an intelligent assistant. With ADK, modular tools, and Gemini power, it makes exploring data as easy as chatting. Perfect for analysts, engineers, or anyone who wants smart access to data.

---

Feel free to customize and expand this setup for your organization!
