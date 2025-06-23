"""
Schema Tools Package

This package provides utilities to introspect PostgreSQL database schema,
including table lists, column metadata, foreign keys, and table size.
"""

from .schema_tools import (
    list_tables,
    describe_table,
    get_table_schema_json,
    get_foreign_keys,
    get_primary_keys_for_table,
    get_table_size
)

__all__ = [
    "list_tables",
    "describe_table",
    "get_table_schema_json",
    "get_foreign_keys",
    "get_primary_keys_for_table",
    "get_table_size"
]
