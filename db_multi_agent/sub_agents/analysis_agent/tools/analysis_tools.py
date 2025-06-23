import psycopg2
from db_config import DB_CONFIG

def compute_statistics(table: str, column: str):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT 
                    AVG({column}), 
                    MIN({column}), 
                    MAX({column}), 
                    STDDEV({column})
                FROM {table};
            """)
            avg, min_, max_, stddev = cur.fetchone()
            return {
                "mean": avg,
                "min": min_,
                "max": max_,
                "stddev": stddev
            }

def compute_correlation(table: str, col1: str, col2: str):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT CORR({col1}, {col2}) FROM {table};
            """)
            return {"correlation": cur.fetchone()[0]}
