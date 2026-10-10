"""Import cleaned Apple SEC facts into MySQL."""

from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent
CLEAN_PATH = ROOT / "aapl_filings_clean.csv"
TABLE_NAME = "aapl_financial_facts"


def mysql_config() -> dict[str, str]:
    return {
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": os.getenv("MYSQL_PORT", "3306"),
        "database": os.getenv("MYSQL_DB", "sec_analysis"),
    }


def validate_identifier(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", name):
        raise ValueError(f"Unsafe MySQL identifier: {name!r}")
    return name


def make_url(config: dict[str, str], include_db: bool = True) -> str:
    user = quote_plus(config["user"])
    password = quote_plus(config["password"])
    host = config["host"]
    port = config["port"]
    db_part = f"/{config['database']}" if include_db else ""
    return f"mysql+pymysql://{user}:{password}@{host}:{port}{db_part}?charset=utf8mb4"


def main() -> None:
    if not CLEAN_PATH.exists():
        raise FileNotFoundError("Run 02_data_clean.py before importing into MySQL.")

    config = mysql_config()
    database = validate_identifier(config["database"])

    root_engine = create_engine(make_url(config, include_db=False))
    with root_engine.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{database}` DEFAULT CHARACTER SET utf8mb4"))
    print(f"Database ready: {database}")

    engine = create_engine(make_url(config, include_db=True))
    facts = pd.read_csv(CLEAN_PATH, parse_dates=["filed", "start", "end"])
    facts.to_sql(name=TABLE_NAME, con=engine, if_exists="replace", index=False, chunksize=1000)

    print(f"Imported {len(facts)} rows into {database}.{TABLE_NAME}")


if __name__ == "__main__":
    main()
