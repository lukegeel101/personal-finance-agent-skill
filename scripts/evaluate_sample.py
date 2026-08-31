#!/usr/bin/env python3
"""Evaluate the fictional finance sample against committed expectations."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finance_control import CsvFileConnector, category_totals, deduplicate_transactions, purchase_spending, recurring_candidates


CONFIG_PATH = ROOT / "config" / "finance.example.json"
EXPECTED_PATH = ROOT / "data" / "evaluation" / "expected-results.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def inclusive_days(start: date, end: date) -> int:
    return (end - start).days + 1


def evaluate_sample() -> dict[str, Any]:
    config = load_json(CONFIG_PATH)
    connector_config = config["connectors"][0]
    connector = CsvFileConnector(
        ROOT / connector_config["accounts_path"],
        ROOT / connector_config["transactions_path"],
        connector_config["source_ref"],
    )
    batch = connector.sync(date(2026, 6, 1), date(2026, 8, 31))
    deduplicated = deduplicate_transactions(batch.transactions)
    excluded = set(config["analysis"]["exclude_from_purchase_spending"])
    spending = purchase_spending(deduplicated, excluded)
    totals = category_totals(spending)
    recurring = recurring_candidates(
        spending,
        minimum_occurrences=config["analysis"]["recurring_minimum_occurrences"],
        interval_min_days=config["analysis"]["recurring_monthly_interval_min_days"],
        interval_max_days=config["analysis"]["recurring_monthly_interval_max_days"],
    )
    requested_days = inclusive_days(batch.requested_start, batch.requested_end)
    actual_days = (
        inclusive_days(batch.actual_oldest, batch.actual_newest)
        if batch.actual_oldest and batch.actual_newest
        else 0
    )

    return {
        "actions_taken": 0,
        "actual_coverage_days": actual_days,
        "category_totals": totals,
        "deduplicated_transactions": len(deduplicated),
        "purchase_spending_records": len(spending),
        "purchase_spending_total": round(sum(totals.values()), 2),
        "raw_transactions": len(batch.transactions),
        "recurring_candidates": len(recurring),
        "requested_coverage_days": requested_days,
        "source_coverage_percent": round((actual_days / requested_days) * 100, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Compare output with the committed expected result.")
    args = parser.parse_args()

    result = evaluate_sample()
    print(json.dumps(result, indent=2, sort_keys=True))

    if args.check and result != load_json(EXPECTED_PATH):
        print("Evaluation output does not match data/evaluation/expected-results.json.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
