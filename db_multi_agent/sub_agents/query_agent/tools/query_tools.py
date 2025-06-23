# query_tools.py

"""
This module provides query utilities to execute and analyze SQL queries
on a PostgreSQL database. Includes search, correlation, statistics,
time series, and safe custom query execution.
"""

from db_config import DB_CONFIG
import psycopg2


def _get_db_connection():
    """Establish and return a connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)


def run_query(query: str) -> str:
    """Executes a SELECT-only SQL query and returns formatted results."""
    if not query.strip().lower().startswith("select"):
        return "Only SELECT queries are allowed."
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
        if not rows:
            return "Query returned no results."
        output = [" | ".join(column_names), "-|-".join(["-" * len(c) for c in column_names])]
        output += [" | ".join(map(str, row)) for row in rows]
        return "\n".join(output)
    except Exception as e:
        return f"Database error: {str(e)}"


def run_custom_sql(query: str) -> str:
    """
    Executes a safe custom SQL query (e.g., EXPLAIN or SHOW) after filtering
    out dangerous keywords. Returns formatted results.
    """
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    if any(word in query.lower() for word in forbidden):
        return "Destructive queries are not allowed."
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
        output = [" | ".join(column_names), "-|-".join(["-" * len(c) for c in column_names])]
        output += [" | ".join(map(str, row)) for row in rows]
        return "\n".join(output)
    except Exception as e:
        return f"Database error: {str(e)}"


def search_in_table(table: str, column: str, value: str) -> str:
    """Searches for a value in a specific column of a table (ILIKE match)."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {table} WHERE {column}::text ILIKE %s LIMIT 10;"
                cursor.execute(query, (f"%{value}%",))
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
        if not rows:
            return f"No matches found for {value} in {table}.{column}"
        output = [" | ".join(column_names), "-|-".join(["-" * len(c) for c in column_names])]
        output += [" | ".join(map(str, row)) for row in rows]
        return "\n".join(output)
    except Exception as e:
        return f"Database error: {str(e)}"


def count_rows(table: str) -> str:
    """Counts and returns the total number of rows in a given table."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
        return f"{table} contains {count} rows."
    except Exception as e:
        return f"Database error: {str(e)}"


def top_k_column_values(table: str, column: str, k: int = 5) -> str:
    """Returns the top-k most frequent values in a column."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT {column}::text, COUNT(*) as freq
                    FROM {table}
                    WHERE {column} IS NOT NULL
                    GROUP BY {column}
                    ORDER BY freq DESC
                    LIMIT %s;
                """, (k,))
                rows = cursor.fetchall()
        return "\n".join([f"{val}: {freq}" for val, freq in rows]) or "No data found."
    except Exception as e:
        return f"Database error: {str(e)}"


def numeric_column_stats(table: str, column: str) -> str:
    """
    Calculates and returns basic statistics (mean, median, stddev, min, max)
    for a numeric column in a given table.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT
                        AVG({column}),
                        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {column}),
                        STDDEV({column}),
                        MIN({column}),
                        MAX({column})
                    FROM {table}
                    WHERE {column} IS NOT NULL;
                """)
                stats = cursor.fetchone()
        return (
            f"Mean: {stats[0]:.2f}\nMedian: {stats[1]:.2f}\n"
            f"StdDev: {stats[2]:.2f}\nMin: {stats[3]}\nMax: {stats[4]}"
        )
    except Exception as e:
        return f"Database error: {str(e)}"


def time_series_summary(table: str, date_col: str, agg_col: str) -> str:
    """
    Groups by month (based on date_col) and computes average of agg_col,
    returning a time series summary.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT DATE_TRUNC('month', {date_col})::date, AVG({agg_col})
                    FROM {table}
                    WHERE {date_col} IS NOT NULL AND {agg_col} IS NOT NULL
                    GROUP BY 1 ORDER BY 1;
                """)
                rows = cursor.fetchall()
        return "\n".join([f"{date} : {avg:.2f}" for date, avg in rows])
    except Exception as e:
        return f"Database error: {str(e)}"


def compute_correlation(table: str, col1: str, col2: str) -> str:
    """
    Computes Pearson correlation between two numeric columns in a table.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT CORR({col1}, {col2})
                    FROM {table}
                    WHERE {col1} IS NOT NULL AND {col2} IS NOT NULL;
                """)
                result = cursor.fetchone()[0]
        return f"Correlation: {result:.4f}" if result is not None else "Not enough data to compute correlation."
    except Exception as e:
        return f"Database error: {str(e)}"


def get_latest_entries_from_table(table: str) -> str:
    """
    Attempts to retrieve the most recent row from a table using common
    ordering columns like created_at, updated_at, or id.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT * FROM {table}
                    ORDER BY COALESCE(
                        (SELECT column_name FROM information_schema.columns
                         WHERE table_name = %s AND column_name IN ('created_at', 'updated_at', 'id')
                         ORDER BY ordinal_position LIMIT 1), 'id') DESC
                    LIMIT 1;
                """, (table,))
                row = cursor.fetchone()
                column_names = [desc[0] for desc in cursor.description]
        output = [" | ".join(column_names), "-|-".join(["-" * len(c) for c in column_names])]
        output.append(" | ".join(map(str, row)))
        return "\n".join(output)
    except Exception as e:
        return f"Database error: {str(e)}"


__all__ = [
    "run_query",
    "run_custom_sql",
    "search_in_table",
    "count_rows",
    "top_k_column_values",
    "numeric_column_stats",
    "time_series_summary",
    "compute_correlation",
    "get_latest_entries_from_table",
]
