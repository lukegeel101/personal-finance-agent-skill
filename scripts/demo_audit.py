#!/usr/bin/env python3
"""Run a small read-only audit against the fictional sample data."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finance_control import CsvFileConnector, category_totals, deduplicate_transactions, purchase_spending, recurring_candidates


def main() -> int:
    config = json.loads((ROOT / "config" / "finance.example.json").read_text(encoding="utf-8"))
    connector_config = config["connectors"][0]
    connector = CsvFileConnector(
        ROOT / connector_config["accounts_path"],
        ROOT / connector_config["transactions_path"],
        connector_config["source_ref"],
    )
    batch = connector.sync(date(2026, 6, 1), date(2026, 8, 31))
    transactions = deduplicate_transactions(batch.transactions)
    excluded = set(config["analysis"]["exclude_from_purchase_spending"])
    spending = purchase_spending(transactions, excluded)
    output = {
        "sample": True,
        "source_ref": batch.source_ref,
        "requested_window": [batch.requested_start.isoformat(), batch.requested_end.isoformat()],
        "actual_window": [
            batch.actual_oldest.isoformat() if batch.actual_oldest else None,
            batch.actual_newest.isoformat() if batch.actual_newest else None,
        ],
        "transaction_count": len(transactions),
        "purchase_spending_by_category": category_totals(spending),
        "recurring_candidates": recurring_candidates(
            spending,
            minimum_occurrences=config["analysis"]["recurring_minimum_occurrences"],
            interval_min_days=config["analysis"]["recurring_monthly_interval_min_days"],
            interval_max_days=config["analysis"]["recurring_monthly_interval_max_days"],
        ),
        "warnings": list(batch.warnings),
        "actions_not_taken": [
            "No account connected.",
            "No payment or transfer submitted.",
            "No subscription canceled.",
            "No trade or application submitted."
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

