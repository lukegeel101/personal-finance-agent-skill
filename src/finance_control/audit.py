"""Deterministic audit helpers for normalized transactions."""

from __future__ import annotations

import re
from collections import defaultdict
from statistics import mean
from typing import Iterable

from .adapters import Transaction


STATUS_RANK = {
    "PENDING_VERIFICATION": 0,
    "ESTIMATE": 1,
    "PLAN": 1,
    "USER_REPORTED": 2,
    "CONNECTED_SNAPSHOT": 3,
    "CONFIRMED": 4,
}


def normalize_descriptor(description: str) -> str:
    normalized = description.upper().strip()
    normalized = re.sub(r"\b\d{2,}\b", "", normalized)
    normalized = re.sub(r"[^A-Z0-9]+", " ", normalized)
    return " ".join(normalized.split())


def transaction_deduplication_key(transaction: Transaction) -> tuple[str, str, int, str]:
    return (
        transaction.account_ref,
        transaction.posted_at.isoformat(),
        round(transaction.amount * 100),
        normalize_descriptor(transaction.description),
    )


def deduplicate_transactions(transactions: Iterable[Transaction]) -> list[Transaction]:
    selected: dict[tuple[str, str, int, str], Transaction] = {}
    for transaction in transactions:
        key = transaction_deduplication_key(transaction)
        current = selected.get(key)
        if current is None or STATUS_RANK.get(transaction.evidence_status, -1) > STATUS_RANK.get(current.evidence_status, -1):
            selected[key] = transaction
    return sorted(selected.values(), key=lambda transaction: (transaction.posted_at, transaction.transaction_ref))


def purchase_spending(
    transactions: Iterable[Transaction], excluded_categories: set[str]
) -> list[Transaction]:
    return [
        transaction
        for transaction in transactions
        if transaction.amount < 0 and transaction.category not in excluded_categories
    ]


def category_totals(transactions: Iterable[Transaction]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for transaction in transactions:
        if transaction.amount < 0:
            totals[transaction.category] += abs(transaction.amount)
    return {category: round(amount, 2) for category, amount in sorted(totals.items())}


def recurring_candidates(
    transactions: Iterable[Transaction],
    minimum_occurrences: int = 3,
    interval_min_days: int = 25,
    interval_max_days: int = 35,
) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[Transaction]] = defaultdict(list)
    for transaction in transactions:
        if transaction.amount < 0:
            groups[(normalize_descriptor(transaction.description), transaction.category)].append(transaction)

    candidates: list[dict[str, object]] = []
    for (descriptor, category), records in sorted(groups.items()):
        records.sort(key=lambda transaction: transaction.posted_at)
        if len(records) < minimum_occurrences:
            continue
        intervals = [
            (current.posted_at - previous.posted_at).days
            for previous, current in zip(records, records[1:])
        ]
        amounts = [abs(transaction.amount) for transaction in records]
        average_amount = mean(amounts)
        amount_range = max(amounts) - min(amounts)
        amount_stable = amount_range <= max(1.0, average_amount * 0.10)
        interval_stable = all(interval_min_days <= interval <= interval_max_days for interval in intervals)
        if amount_stable and interval_stable:
            candidates.append(
                {
                    "descriptor": descriptor,
                    "category": category,
                    "occurrences": len(records),
                    "average_amount": round(average_amount, 2),
                    "average_interval_days": round(mean(intervals), 1),
                    "first_seen": records[0].posted_at.isoformat(),
                    "last_seen": records[-1].posted_at.isoformat(),
                }
            )
    return candidates

