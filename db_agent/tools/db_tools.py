# import psycopg2
# from .. import config


# def run_query(query: str):
#     """
#     Executes a SQL SELECT query.
#     """
#     if not query.strip().lower().startswith("select"):
#         return "Only SELECT queries are allowed for safety."

#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         column_names = [desc[0] for desc in cursor.description]
#         conn.close()

#         if not rows:
#             return "Query executed successfully. No results returned."

#         formatted = " | ".join(column_names) + "\n"
#         formatted += "-|-".join(["-" * len(col) for col in column_names]) + "\n"
#         for row in rows:
#             formatted += " | ".join(str(item) for item in row) + "\n"
#         return formatted

#     except Exception as e:
#         return f"Database error: {str(e)}"


# def list_tables():
#     """
#     Returns a list of all tables in the public schema.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT table_name FROM information_schema.tables
#             WHERE table_schema = 'public';
#         """)
#         tables = cursor.fetchall()
#         conn.close()
#         return "\n".join([table[0] for table in tables]) or "No tables found."
#     except Exception as e:
#         return f"Database error: {str(e)}"


# def describe_table(table_name: str):
#     """
#     Describes the columns of a table: name, data type, nullable.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(f"""
#             SELECT column_name, data_type, is_nullable
#             FROM information_schema.columns
#             WHERE table_name = %s;
#         """, (table_name,))
#         rows = cursor.fetchall()
#         conn.close()

#         if not rows:
#             return f"No such table: {table_name}"

#         formatted = "Column | Type | Nullable\n"
#         formatted += "-------|------|---------\n"
#         for col, dtype, nullable in rows:
#             formatted += f"{col} | {dtype} | {nullable}\n"
#         return formatted

#     except Exception as e:
#         return f"Database error: {str(e)}"


# def search_in_table(table_name: str, column: str, value: str):
#     """
#     Searches for a value in a specific column of a table.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         query = f"SELECT * FROM {table_name} WHERE {column}::text ILIKE %s LIMIT 10;"
#         cursor.execute(query, (f"%{value}%",))
#         rows = cursor.fetchall()
#         column_names = [desc[0] for desc in cursor.description]
#         conn.close()

#         if not rows:
#             return f"No results found for '{value}' in {table_name}.{column}"

#         formatted = " | ".join(column_names) + "\n"
#         formatted += "-|-".join(["-" * len(col) for col in column_names]) + "\n"
#         for row in rows:
#             formatted += " | ".join(str(item) for item in row) + "\n"
#         return formatted

#     except Exception as e:
#         return f"Database error: {str(e)}"


# def count_rows(table_name: str):
#     """
#     Returns the number of rows in a table.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
#         count = cursor.fetchone()[0]
#         conn.close()
#         return f"Table '{table_name}' contains {count} rows."
#     except Exception as e:
#         return f"Database error: {str(e)}"



# def get_table_schema_json(table_name: str):
#     """
#     Returns the schema of a table as a JSON object.
#     """
#     import json
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT column_name, data_type, is_nullable
#             FROM information_schema.columns
#             WHERE table_name = %s;
#         """, (table_name,))
#         schema = [
#             {"column": col, "type": dtype, "nullable": nullable}
#             for col, dtype, nullable in cursor.fetchall()
#         ]
#         conn.close()

#         if not schema:
#             return f"No such table: {table_name}"
#         return json.dumps(schema, indent=2)

#     except Exception as e:
#         return f"Database error: {str(e)}"



# def get_foreign_keys(table_name: str):
#     """
#     Lists foreign key constraints in the specified table.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT
#                 tc.constraint_name, kcu.column_name, 
#                 ccu.table_name AS foreign_table_name,
#                 ccu.column_name AS foreign_column_name
#             FROM 
#                 information_schema.table_constraints AS tc
#                 JOIN information_schema.key_column_usage AS kcu
#                   ON tc.constraint_name = kcu.constraint_name
#                 JOIN information_schema.constraint_column_usage AS ccu
#                   ON ccu.constraint_name = tc.constraint_name
#             WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s;
#         """, (table_name,))
#         results = cursor.fetchall()
#         conn.close()

#         if not results:
#             return f"No foreign keys found in table: {table_name}"

#         formatted = "Constraint | Column | References\n"
#         formatted += "-----------|--------|----------\n"
#         for constraint, col, ref_table, ref_col in results:
#             formatted += f"{constraint} | {col} | {ref_table}.{ref_col}\n"
#         return formatted

#     except Exception as e:
#         return f"Database error: {str(e)}"



# def get_table_size(table_name: str):
#     """
#     Returns the size of the table in MB.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT pg_size_pretty(pg_total_relation_size(%s));
#         """, (table_name,))
#         size = cursor.fetchone()[0]
#         conn.close()
#         return f"Table '{table_name}' size: {size}"

#     except Exception as e:
#         return f"Database error: {str(e)}"



# def run_custom_sql(query: str):
#     """
#     Runs a custom SQL query (non-modifying) like EXPLAIN or SHOW statements.
#     """
#     try:
#         forbidden = any(word in query.lower() for word in ["insert", "update", "delete", "drop", "alter"])
#         if forbidden:
#             return "Destructive queries are not allowed for safety."

#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         column_names = [desc[0] for desc in cursor.description]
#         conn.close()

#         if not rows:
#             return "Query executed successfully. No results returned."

#         formatted = " | ".join(column_names) + "\n"
#         formatted += "-|-".join(["-" * len(col) for col in column_names]) + "\n"
#         for row in rows:
#             formatted += " | ".join(str(item) for item in row) + "\n"
#         return formatted

#     except Exception as e:
#         return f"Database error: {str(e)}"



# def top_k_column_values(table: str, column: str, k: int = 5):
#     """
#     Returns the top-K most frequent values in a column.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(f"""
#             SELECT {column}, COUNT(*) as freq
#             FROM {table}
#             GROUP BY {column}
#             ORDER BY freq DESC
#             LIMIT %s;
#         """, (k,))
#         rows = cursor.fetchall()
#         conn.close()

#         if not rows:
#             return f"No data found in {table}.{column}"

#         return "\n".join([f"{val}: {count}" for val, count in rows])

#     except Exception as e:
#         return f"Database error: {str(e)}"


# def numeric_column_stats(table: str, column: str):
#     """
#     Returns basic statistics for a numeric column.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(f"""
#             SELECT 
#                 AVG({column}) AS mean,
#                 PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {column}) AS median,
#                 STDDEV({column}) AS stddev,
#                 MIN({column}) AS min,
#                 MAX({column}) AS max
#             FROM {table};
#         """)
#         stats = cursor.fetchone()
#         conn.close()

#         return (
#             f"Mean: {stats[0]:.2f}\n"
#             f"Median: {stats[1]:.2f}\n"
#             f"Std Dev: {stats[2]:.2f}\n"
#             f"Min: {stats[3]:.2f}\n"
#             f"Max: {stats[4]:.2f}"
#         )
#     except Exception as e:
#         return f"Database error: {str(e)}"


# def time_series_summary(table: str, date_column: str, agg_column: str):
#     """
#     Aggregates a numeric column by month/year using a date column.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(f"""
#             SELECT DATE_TRUNC('month', {date_column}) AS month,
#                    AVG({agg_column}) AS average
#             FROM {table}
#             GROUP BY month
#             ORDER BY month;
#         """)
#         rows = cursor.fetchall()
#         conn.close()

#         return "\n".join([f"{month.date()} : {avg:.2f}" for month, avg in rows])
#     except Exception as e:
#         return f"Database error: {str(e)}"


# def compute_correlation(table: str, col1: str, col2: str):
#     """
#     Computes the correlation between two numeric columns.
#     """
#     try:
#         conn = psycopg2.connect(**config.DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute(f"""
#             SELECT CORR({col1}, {col2}) FROM {table};
#         """)
#         corr = cursor.fetchone()[0]
#         conn.close()

#         return f"Correlation between {col1} and {col2}: {corr:.4f}" if corr is not None else "Correlation could not be computed."

#     except Exception as e:
#         return f"Database error: {str(e)}"

import psycopg2
import json
from .. import config # Assuming config.py holds DB_CONFIG dictionary

# --- Helper for Connection Management ---
def _get_db_connection():
    """Establishes and returns a database connection."""
    return psycopg2.connect(**config.DB_CONFIG)

# --- Core Database Interaction Functions ---

def run_query(query: str) -> str:
    """
    Executes a SQL SELECT query and returns formatted results.
    Only SELECT queries are allowed for safety.
    """
    if not query.strip().lower().startswith("select"):
        return "Only SELECT queries are allowed for safety."

    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not cursor.description: # Handle queries that return no data, like 'SELECT 1;'
                    return "Query executed successfully. No results returned or no columns."

                column_names = [desc[0] for desc in cursor.description]

        if not rows:
            return "Query executed successfully. No results returned."

        # Format results
        formatted_output = []
        header = " | ".join(column_names)
        formatted_output.append(header)
        formatted_output.append("-|-".join(["-" * len(col) for col in column_names]))
        for row in rows:
            formatted_output.append(" | ".join(str(item) for item in row))
        return "\n".join(formatted_output)

    except Exception as e:
        # In a real application, you'd want to log the full traceback here
        return f"Database error: {str(e)}"


def list_tables() -> str:
    """
    Returns a list of all tables in the public schema, formatted as a string.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
        return "\n".join([table[0] for table in tables]) or "No tables found in public schema."
    except Exception as e:
        return f"Database error: {str(e)}"


def describe_table(table_name: str) -> str:
    """
    Describes the columns of a table: name, data type, nullable.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Parameterize table_name to prevent SQL injection, even though it's in WHERE clause
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                rows = cursor.fetchall()

        if not rows:
            return f"No such table or no columns found for: {table_name}"

        formatted_output = []
        formatted_output.append("Column | Type | Nullable")
        formatted_output.append("-------|------|---------")
        for col, dtype, nullable in rows:
            formatted_output.append(f"{col} | {dtype} | {nullable}")
        return "\n".join(formatted_output)

    except Exception as e:
        return f"Database error: {str(e)}"


def search_in_table(table_name: str, column: str, value: str) -> str:
    """
    Searches for a value in a specific column of a table.
    Limits results to 10. Columns are cast to text for ILIKE comparison.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # IMPORTANT: Dynamically adding table/column names directly into f-strings
                # can be an SQL injection risk if inputs are not trusted/sanitized.
                # For this specific tool, assuming table_name and column are validated
                # or come from internal introspection. Value is safely parameterized.
                query = f"SELECT * FROM {table_name} WHERE {column}::text ILIKE %s LIMIT 10;"
                cursor.execute(query, (f"%{value}%",))
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]

        if not rows:
            return f"No results found for '{value}' in {table_name}.{column}"

        formatted_output = []
        header = " | ".join(column_names)
        formatted_output.append(header)
        formatted_output.append("-|-".join(["-" * len(col) for col in column_names]))
        for row in rows:
            formatted_output.append(" | ".join(str(item) for item in row))
        return "\n".join(formatted_output)

    except psycopg2.errors.UndefinedColumn:
        return f"Error: Column '{column}' does not exist in table '{table_name}'."
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table_name}' does not exist."
    except Exception as e:
        return f"Database error: {str(e)}"


def count_rows(table_name: str) -> str:
    """
    Returns the number of rows in a table.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Safer to use execute for table_name if from untrusted source
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
        return f"Table '{table_name}' contains {count} rows."
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table_name}' does not exist."
    except Exception as e:
        return f"Database error: {str(e)}"


def get_table_schema_json(table_name: str) -> str:
    """
    Returns the schema of a table as a JSON object string.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                schema = [
                    {"column": col, "type": dtype, "nullable": nullable == 'YES'} # Convert 'YES'/'NO' to boolean
                    for col, dtype, nullable in cursor.fetchall()
                ]

        if not schema:
            return f"No such table or no columns found for: {table_name}"
        return json.dumps(schema, indent=2)

    except Exception as e:
        return f"Database error: {str(e)}"


def get_foreign_keys(table_name: str) -> str:
    """
    Lists foreign key constraints in the specified table.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        tc.constraint_name,
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM
                        information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s
                    ORDER BY tc.constraint_name, kcu.ordinal_position;
                """, (table_name,))
                results = cursor.fetchall()

        if not results:
            return f"No foreign keys found in table: {table_name}"

        formatted_output = []
        formatted_output.append("Constraint | Column | References")
        formatted_output.append("-----------|--------|----------")
        for constraint, col, ref_table, ref_col in results:
            formatted_output.append(f"{constraint} | {col} | {ref_table}.{ref_col}")
        return "\n".join(formatted_output)

    except Exception as e:
        return f"Database error: {str(e)}"


def get_table_size(table_name: str) -> str:
    """
    Returns the size of the table in a human-readable format (e.g., MB).
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Use %s for table_name, then pass it as a parameter
                # pg_total_relation_size needs a regclass, which can take a quoted string
                cursor.execute("""
                    SELECT pg_size_pretty(pg_total_relation_size(%s::regclass));
                """, (table_name,))
                size = cursor.fetchone()[0]
        return f"Table '{table_name}' size: {size}"
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table_name}' does not exist or insufficient permissions."
    except Exception as e:
        return f"Database error: {str(e)}"


def run_custom_sql(query: str) -> str:
    """
    Runs a custom SQL query (non-modifying) like EXPLAIN or SHOW statements.
    """
    try:
        # Check for forbidden keywords (case-insensitive)
        forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
        if any(word in query.lower() for word in forbidden_keywords):
            return "Destructive or schema-modifying queries are not allowed for safety."

        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not cursor.description: # Handle queries that return no data, like 'EXPLAIN ANALYZE SELECT 1;'
                    return "Query executed successfully. No results returned or no columns."

                column_names = [desc[0] for desc in cursor.description]

        if not rows:
            return "Query executed successfully. No results returned."

        formatted_output = []
        header = " | ".join(column_names)
        formatted_output.append(header)
        formatted_output.append("-|-".join(["-" * len(col) for col in column_names]))
        for row in rows:
            formatted_output.append(" | ".join(str(item) for item in row))
        return "\n".join(formatted_output)

    except Exception as e:
        return f"Database error: {str(e)}"


def top_k_column_values(table: str, column: str, k: int = 5) -> str:
    """
    Returns the top-K most frequent values in a column.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Again, for column and table, assume validated or internal source.
                query = f"""
                    SELECT {column}::text, COUNT(*) as freq
                    FROM {table}
                    WHERE {column} IS NOT NULL -- Exclude NULLs from frequency count
                    GROUP BY {column}
                    ORDER BY freq DESC
                    LIMIT %s;
                """
                cursor.execute(query, (k,))
                rows = cursor.fetchall()

        if not rows:
            return f"No data or distinct values found in {table}.{column}"

        return "\n".join([f"{val}: {count}" for val, count in rows])

    except psycopg2.errors.UndefinedColumn:
        return f"Error: Column '{column}' does not exist in table '{table}'."
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table}' does not exist."
    except Exception as e:
        return f"Database error: {str(e)}"


def numeric_column_stats(table: str, column: str) -> str:
    """
    Returns basic statistics for a numeric column.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Validate column is numeric type before executing if possible,
                # or rely on DB error. Assume table/column safe from injection.
                query = f"""
                    SELECT
                        AVG({column}) AS mean,
                        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {column}) AS median,
                        STDDEV({column}) AS stddev,
                        MIN({column}) AS min,
                        MAX({column}) AS max
                    FROM {table}
                    WHERE {column} IS NOT NULL; -- Exclude NULLs from calculations
                """
                cursor.execute(query)
                stats = cursor.fetchone()

        # Check if any stats are None (e.g., if table is empty or column has only NULLs)
        if all(s is None for s in stats):
             return f"No numeric data found in {table}.{column} to compute statistics."

        return (
            f"Mean: {stats[0]:.2f}\n"
            f"Median: {stats[1]:.2f}\n"
            f"Std Dev: {stats[2]:.2f}\n"
            f"Min: {stats[3]:.2f}\n"
            f"Max: {stats[4]:.2f}"
        )
    except psycopg2.errors.UndefinedColumn:
        return f"Error: Column '{column}' does not exist in table '{table}'."
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table}' does not exist."
    except psycopg2.errors.DatatypeMismatch: # Or similar error for non-numeric column
        return f"Error: Column '{column}' in table '{table}' is not a numeric type."
    except Exception as e:
        return f"Database error: {str(e)}"


def time_series_summary(table: str, date_column: str, agg_column: str) -> str:
    """
    Aggregates a numeric column by month/year using a date column.
    Returns the average of the aggregation column per month.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Ensure date_column and agg_column are valid and not injectable.
                # Assume they come from internal validation or trusted source.
                query = f"""
                    SELECT DATE_TRUNC('month', {date_column})::date AS month_start,
                           AVG({agg_column}) AS average
                    FROM {table}
                    WHERE {date_column} IS NOT NULL AND {agg_column} IS NOT NULL
                    GROUP BY month_start
                    ORDER BY month_start;
                """
                cursor.execute(query)
                rows = cursor.fetchall()

        if not rows:
            return f"No time series data found in {table} for columns {date_column} and {agg_column}."

        return "\n".join([f"{month_start} : {avg:.2f}" for month_start, avg in rows])
    except psycopg2.errors.UndefinedColumn:
        return f"Error: One of the columns ('{date_column}', '{agg_column}') does not exist in table '{table}'."
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table}' does not exist."
    except psycopg2.errors.InvalidDatetimeFormat: # Or similar if date_column isn't a date
         return f"Error: Column '{date_column}' in table '{table}' is not a valid date/time type."
    except psycopg2.errors.DatatypeMismatch: # If agg_column isn't numeric
        return f"Error: Column '{agg_column}' in table '{table}' is not a numeric type."
    except Exception as e:
        return f"Database error: {str(e)}"


def compute_correlation(table: str, col1: str, col2: str) -> str:
    """
    Computes the Pearson correlation between two numeric columns.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Assume table, col1, col2 are safe/validated.
                query = f"SELECT CORR({col1}, {col2}) FROM {table} WHERE {col1} IS NOT NULL AND {col2} IS NOT NULL;"
                cursor.execute(query)
                corr = cursor.fetchone()[0]

        if corr is None:
            return f"Correlation could not be computed for {col1} and {col2} in {table}. Check if there is enough non-null data."
        return f"Correlation between {col1} and {col2}: {corr:.4f}"
    except psycopg2.errors.UndefinedColumn:
        return f"Error: One of the columns ('{col1}', '{col2}') does not exist in table '{table}'."
    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table}' does not exist."
    except psycopg2.errors.DatatypeMismatch: # If columns aren't numeric
        return f"Error: One or both columns ('{col1}', '{col2}') in table '{table}' are not numeric types."
    except Exception as e:
        return f"Database error: {str(e)}"
    
    
# Add this new function to your db_agent/tools/db_tools.py file

def get_latest_entries_from_table(table_name: str) -> str:
    """
    Attempts to retrieve the latest single entry from a specified table.
    It prioritizes columns like 'created_at', 'updated_at', 'timestamp', 'date', or 'id'
    to determine the 'latest' entry.
    Returns the full row of the latest entry.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                # First, get column names and types to infer a suitable ordering column
                cursor.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                columns_info = cursor.fetchall()

                if not columns_info:
                    return f"No such table: {table_name}"

                # Prioritize columns for 'latest'
                order_column = None
                # Check for timestamp/date columns first
                for col_name, data_type in columns_info:
                    if col_name.lower() in ('created_at', 'updated_at', 'timestamp', 'date') and 'timestamp' in data_type:
                        order_column = col_name
                        break
                # If no clear timestamp, try 'id' (assuming it's an auto-incrementing primary key)
                if not order_column:
                    for col_name, data_type in columns_info:
                        if col_name.lower() == 'id':
                            order_column = col_name
                            break

                if not order_column:
                    return f"Could not determine a suitable 'latest' column (like 'created_at', 'updated_at', 'id') for table: {table_name}. Please specify a column if you want to order."

                # Execute the query to get the latest entry
                query = f"SELECT * FROM {table_name} ORDER BY {order_column} DESC LIMIT 1;"
                cursor.execute(query)
                row = cursor.fetchone()
                column_names = [desc[0] for desc in cursor.description]

        if not row:
            return f"Table '{table_name}' is empty."

        formatted_output = []
        header = " | ".join(column_names)
        formatted_output.append(header)
        formatted_output.append("-|-".join(["-" * len(col) for col in column_names]))
        formatted_output.append(" | ".join(str(item) for item in row))
        return "\n".join(formatted_output)

    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table_name}' does not exist."
    except psycopg2.errors.UndefinedColumn as e:
        # This might catch if our inferred column doesn't actually exist, though we try to check
        return f"Database error: Could not find order column '{order_column}' in table '{table_name}'. Detail: {str(e)}"
    except Exception as e:
        return f"Database error: {str(e)}"
    

# Add this new function to your db_agent/tools/db_tools.py file

def get_primary_keys_for_table(table_name: str) -> str:
    """
    Returns the primary key columns for a specified table.
    """
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_name = %s
                    ORDER BY kcu.ordinal_position;
                """, (table_name,))
                pk_columns = cursor.fetchall()

        if not pk_columns:
            return f"No primary key found for table: {table_name}"

        # Extract column names from the fetched rows
        pk_column_names = [col[0] for col in pk_columns]

        if len(pk_column_names) == 1:
            return f"The primary key for '{table_name}' is: {pk_column_names[0]}"
        else:
            return f"The primary key for '{table_name}' consists of columns: {', '.join(pk_column_names)}"

    except psycopg2.errors.UndefinedTable:
        return f"Error: Table '{table_name}' does not exist."
    except Exception as e:
        return f"Database error: {str(e)}"