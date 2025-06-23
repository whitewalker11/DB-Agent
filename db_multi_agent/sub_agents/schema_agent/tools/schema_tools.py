# schema_tools.py

"""
This module provides tools for exploring database schema
including listing tables, describing columns, foreign keys,
primary keys, and table size. Intended for schema_agent in a
multi-agent ADK-based database assistant.
"""

import psycopg2
import json
from db_config import DB_CONFIG


def _get_db_connection():
    """Establish and return a PostgreSQL database connection."""
    return psycopg2.connect(**DB_CONFIG)


def list_tables() -> str:
    """Returns all tables in the public schema as a newline-separated string."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
        return "\n".join([t[0] for t in tables]) or "No tables found."
    except Exception as e:
        return f"Database error: {str(e)}"


def describe_table(table_name: str) -> str:
    """Returns column name, type, and nullability for a given table."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                rows = cursor.fetchall()
        if not rows:
            return f"Table '{table_name}' not found."
        output = ["Column | Type | Nullable", "-------|------|---------"]
        output += [f"{col} | {dtype} | {nullable}" for col, dtype, nullable in rows]
        return "\n".join(output)
    except Exception as e:
        return f"Database error: {str(e)}"


def get_table_schema_json(table_name: str) -> str:
    """Returns table schema as a formatted JSON string."""
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
                    {"column": col, "type": dtype, "nullable": nullable == 'YES'}
                    for col, dtype, nullable in cursor.fetchall()
                ]
        return json.dumps(schema, indent=2) if schema else f"No schema found for {table_name}."
    except Exception as e:
        return f"Database error: {str(e)}"


def get_foreign_keys(table_name: str) -> str:
    """Returns all foreign key constraints from a table."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        tc.constraint_name,
                        kcu.column_name,
                        ccu.table_name AS foreign_table,
                        ccu.column_name AS foreign_column
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                      AND tc.table_name = %s;
                """, (table_name,))
                rows = cursor.fetchall()
        if not rows:
            return f"No foreign keys found in {table_name}."
        output = ["Constraint | Column | References", "-----------|--------|-----------"]
        output += [f"{c} | {col} | {ref_tbl}.{ref_col}" for c, col, ref_tbl, ref_col in rows]
        return "\n".join(output)
    except Exception as e:
        return f"Database error: {str(e)}"


def get_primary_keys_for_table(table_name: str) -> str:
    """Returns primary key columns of a given table."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_name = %s;
                """, (table_name,))
                pk_columns = [col[0] for col in cursor.fetchall()]
        if not pk_columns:
            return f"No primary key found for {table_name}."
        return f"Primary key(s): {', '.join(pk_columns)}"
    except Exception as e:
        return f"Database error: {str(e)}"


def get_table_size(table_name: str) -> str:
    """Returns the size of a given table in human-readable format."""
    try:
        with _get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT pg_size_pretty(pg_total_relation_size(%s::regclass));
                """, (table_name,))
                size = cursor.fetchone()[0]
        return f"Table '{table_name}' size: {size}"
    except Exception as e:
        return f"Database error: {str(e)}"


