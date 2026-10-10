"""Preview Apple SEC financial facts and company profile files."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
FACTS_PATH = ROOT / "financial_facts.csv"
PROFILE_PATH = ROOT / "company_profile.json"


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")


def main() -> None:
    require_file(FACTS_PATH)
    require_file(PROFILE_PATH)

    facts = pd.read_csv(FACTS_PATH)
    print("SEC financial facts rows:", len(facts))
    print("Columns:", facts.columns.tolist())
    print("\nPreview:")
    print(facts.head(3))

    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        profile = json.load(file)

    print("\nApple company profile")
    print(f"Company name: {profile.get('entityName', 'N/A')}")
    print(f"Ticker: {profile.get('ticker', 'N/A')}")
    print(f"SIC: {profile.get('sic', 'N/A')} | {profile.get('sicDescription', 'N/A')}")


if __name__ == "__main__":
    main()
