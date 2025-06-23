from typing import Optional
from openai import OpenAI
from .. import config



# Initialize OpenAI client with API key from config
client = OpenAI()

def convert_to_sql(nl_query: str, table_context: Optional[str] = "") -> str:
    """
    Tool Name: convert_to_sql

    Description:
        Converts a natural language prompt into a SQL SELECT query using OpenAI's GPT-4.

    Parameters:
        nl_query (str): A user query in natural language.
        table_context (Optional[str]): Info about the DB schema.

    Returns:
        A SQL query as a string or an error message.
    """
    prompt = f"""You are an expert SQL generator. Convert the user's query into a valid PostgreSQL SELECT statement.

Tables and schema:
{table_context}

Natural Language Query: "{nl_query}"

Only return the SQL query, nothing else.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        sql = response.choices[0].message.content.strip()
        if sql.startswith("```sql") or sql.startswith("```"):
            sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql
    except Exception as e:
        return f"Error generating SQL: {str(e)}"
