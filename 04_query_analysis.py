"""Run basic MySQL checks for the Apple SEC facts table."""

from __future__ import annotations

import os
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine

TABLE_NAME = "aapl_financial_facts"


def make_engine():
    user = quote_plus(os.getenv("MYSQL_USER", "root"))
    password = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DB", "sec_analysis")
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")


def show_query(title: str, sql: str, engine) -> None:
    print(f"\n## {title}")
    print(pd.read_sql(sql, engine).to_string(index=False))


def main() -> None:
    engine = make_engine()
    show_query("row count", f"SELECT COUNT(*) AS total_rows FROM {TABLE_NAME};", engine)
    show_query(
        "filing forms",
        f"""
        SELECT form, COUNT(*) AS row_count
        FROM {TABLE_NAME}
        GROUP BY form
        ORDER BY row_count DESC
        LIMIT 10;
        """,
        engine,
    )
    show_query(
        "recent USD revenue observations",
        f"""
        SELECT concept, fy, fp, end, unit, value, filed
        FROM {TABLE_NAME}
        WHERE concept IN ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax')
          AND unit = 'USD'
        ORDER BY end DESC, filed DESC
        LIMIT 10;
        """,
        engine,
    )


if __name__ == "__main__":
    main()
