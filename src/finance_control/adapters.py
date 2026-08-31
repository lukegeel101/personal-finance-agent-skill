"""Provider-neutral adapter contracts and a read-only CSV implementation."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Protocol, runtime_checkable


EVIDENCE_STATUSES = {
    "CONFIRMED",
    "CONNECTED_SNAPSHOT",
    "USER_REPORTED",
    "ESTIMATE",
    "PLAN",
    "PENDING_VERIFICATION",
}


@dataclass(frozen=True)
class Account:
    account_ref: str
    kind: str
    currency: str
    display_name: str
    source_ref: str


@dataclass(frozen=True)
class Transaction:
    transaction_ref: str
    account_ref: str
    posted_at: date
    amount: float
    currency: str
    description: str
    category: str
    source_ref: str
    evidence_status: str


@dataclass(frozen=True)
class Balance:
    account_ref: str
    amount: float
    currency: str
    observed_at: datetime
    source_ref: str
    freshness_note: str


@dataclass(frozen=True)
class Holding:
    account_ref: str
    asset_ref: str
    description: str
    quantity: float
    market_value: float
    currency: str
    observed_at: datetime
    source_ref: str
    tax_treatment: str | None = None


@dataclass(frozen=True)
class SyncBatch:
    source_ref: str
    requested_start: date
    requested_end: date
    observed_at: datetime
    accounts: tuple[Account, ...] = field(default_factory=tuple)
    transactions: tuple[Transaction, ...] = field(default_factory=tuple)
    balances: tuple[Balance, ...] = field(default_factory=tuple)
    holdings: tuple[Holding, ...] = field(default_factory=tuple)
    actual_oldest: date | None = None
    actual_newest: date | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)


@runtime_checkable
class FinancialConnector(Protocol):
    """Read-only normalized connector contract.

    Authentication, token storage, and provider-specific behavior belong outside
    this public core.
    """

    @property
    def source_ref(self) -> str:
        ...

    @property
    def read_only(self) -> bool:
        ...

    def sync(self, start: date, end: date) -> SyncBatch:
        ...


class CsvFileConnector:
    """Read accounts and transactions from local normalized sample files."""

    REQUIRED_TRANSACTION_COLUMNS = {
        "transaction_ref",
        "account_ref",
        "posted_at",
        "amount",
        "currency",
        "description",
        "category",
        "source_ref",
        "evidence_status",
    }

    def __init__(
        self,
        accounts_path: Path,
        transactions_path: Path,
        source_ref: str,
    ) -> None:
        self.accounts_path = Path(accounts_path)
        self.transactions_path = Path(transactions_path)
        self._source_ref = source_ref

    @property
    def source_ref(self) -> str:
        return self._source_ref

    @property
    def read_only(self) -> bool:
        return True

    def _load_accounts(self) -> tuple[Account, ...]:
        with self.accounts_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        accounts: list[Account] = []
        for row in payload.get("accounts", []):
            account = Account(
                account_ref=row["account_ref"],
                kind=row["kind"],
                currency=row["currency"],
                display_name=row["display_name"],
                source_ref=row["source_ref"],
            )
            if account.source_ref != self.source_ref:
                raise ValueError(f"Account {account.account_ref} has an unexpected source_ref")
            accounts.append(account)
        return tuple(accounts)

    def _load_transactions(self) -> tuple[Transaction, ...]:
        with self.transactions_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = set(reader.fieldnames or [])
            missing = self.REQUIRED_TRANSACTION_COLUMNS - columns
            if missing:
                raise ValueError(f"Transaction CSV is missing columns: {sorted(missing)}")
            transactions: list[Transaction] = []
            for row in reader:
                status = row["evidence_status"]
                if status not in EVIDENCE_STATUSES:
                    raise ValueError(f"Invalid evidence status: {status}")
                transaction = Transaction(
                    transaction_ref=row["transaction_ref"],
                    account_ref=row["account_ref"],
                    posted_at=date.fromisoformat(row["posted_at"]),
                    amount=float(row["amount"]),
                    currency=row["currency"],
                    description=row["description"],
                    category=row["category"],
                    source_ref=row["source_ref"],
                    evidence_status=status,
                )
                if transaction.source_ref != self.source_ref:
                    raise ValueError(f"Transaction {transaction.transaction_ref} has an unexpected source_ref")
                transactions.append(transaction)
        return tuple(transactions)

    def sync(self, start: date, end: date) -> SyncBatch:
        if end < start:
            raise ValueError("end must be on or after start")
        accounts = self._load_accounts()
        all_transactions = self._load_transactions()
        transactions = tuple(
            transaction
            for transaction in all_transactions
            if start <= transaction.posted_at <= end
        )
        dates = [transaction.posted_at for transaction in transactions]
        warnings: list[str] = [
            "Static file import. Observation time does not imply real-time data."
        ]
        if not transactions:
            warnings.append("No transactions were returned for the requested window.")
        return SyncBatch(
            source_ref=self.source_ref,
            requested_start=start,
            requested_end=end,
            observed_at=datetime.now().astimezone(),
            accounts=accounts,
            transactions=transactions,
            actual_oldest=min(dates) if dates else None,
            actual_newest=max(dates) if dates else None,
            warnings=tuple(warnings),
        )

