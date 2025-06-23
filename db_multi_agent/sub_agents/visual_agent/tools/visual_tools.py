import psycopg2
import matplotlib.pyplot as plt
from db_config import DB_CONFIG

def plot_histogram(table: str, column: str, bins: int = 10):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {column} FROM {table};")
            data = [row[0] for row in cur.fetchall()]
            plt.hist(data, bins=bins)
            plt.title(f"{column} Distribution")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.savefig("histogram.png")
            return "Histogram saved as histogram.png"

def plot_time_series(table: str, date_column: str, value_column: str):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT {date_column}, {value_column} 
                FROM {table} 
                ORDER BY {date_column} ASC;
            """)
            rows = cur.fetchall()
            dates, values = zip(*rows)
            plt.plot(dates, values)
            plt.title(f"{value_column} over Time")
            plt.xlabel("Date")
            plt.ylabel(value_column)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig("time_series.png")
            return "Time series saved as time_series.png"
