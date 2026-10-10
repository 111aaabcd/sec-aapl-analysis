"""Clean Apple SEC companyfacts observations for analysis."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "financial_facts.csv"
OUTPUT_PATH = ROOT / "aapl_filings_clean.csv"

KEEP_COLUMNS = [
    "taxonomy",
    "concept",
    "label",
    "unit",
    "value",
    "accn",
    "form",
    "filed",
    "fy",
    "fp",
    "start",
    "end",
    "frame",
]
REQUIRED_COLUMNS = {"concept", "unit", "value", "accn", "form", "filed"}
DATE_COLUMNS = ["filed", "start", "end"]


def clean_facts(raw_path: Path = RAW_PATH) -> pd.DataFrame:
    if not raw_path.exists():
        raise FileNotFoundError(f"Required file not found: {raw_path}")

    df = pd.read_csv(raw_path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"financial_facts.csv missing columns: {', '.join(sorted(missing))}")

    available_columns = [column for column in KEEP_COLUMNS if column in df.columns]
    clean = df[available_columns].copy()

    for column in DATE_COLUMNS:
        if column in clean.columns:
            clean[column] = pd.to_datetime(clean[column], errors="coerce")

    clean["value"] = pd.to_numeric(clean["value"], errors="coerce")
    if "fy" in clean.columns:
        clean["fy"] = pd.to_numeric(clean["fy"], errors="coerce").astype("Int64")

    clean = clean.dropna(subset=["concept", "unit", "value", "accn", "form", "filed"])
    clean = clean.drop_duplicates()
    sort_columns = [column for column in ["filed", "concept", "end", "accn"] if column in clean.columns]
    clean = clean.sort_values(sort_columns, na_position="last").reset_index(drop=True)
    return clean


def main() -> None:
    clean = clean_facts()
    clean.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Raw rows: {len(pd.read_csv(RAW_PATH))}")
    print(f"Clean rows: {len(clean)}")
    print(f"Output: {OUTPUT_PATH.name}")
    print("Columns:", clean.columns.tolist())
    print("\nPreview:")
    print(clean.head(3))


if __name__ == "__main__":
    main()
