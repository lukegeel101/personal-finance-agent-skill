#!/usr/bin/env python3
"""Validate public finance examples, permissions, and adapter behavior."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finance_control.adapters import CsvFileConnector, EVIDENCE_STATUSES


CONFIG_PATH = ROOT / "config" / "finance.example.json"
CONTROL_CENTER_PATH = ROOT / "data" / "sample" / "control-center.json"
ACCOUNTS_PATH = ROOT / "data" / "sample" / "accounts.json"

SENSITIVE_KEYS = {
    "account_number",
    "api_key",
    "card_number",
    "cookie",
    "credential",
    "email",
    "full_account_number",
    "password",
    "phone",
    "refresh_token",
    "routing_number",
    "security_answer",
    "session_token",
    "social_security_number",
    "street_address",
    "token",
    "username",
}

SECRET_VALUE_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{12,}\b", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]

PROHIBITED_AUTHORITIES = {
    "connect_account",
    "grant_scope",
    "submit_payment",
    "transfer_money",
    "cancel_subscription",
    "apply_for_credit",
    "trade_asset",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_iso8601(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    return True


def find_sensitive_content(value: Any, prefix: str = "root") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = key.lower().replace("-", "_").replace(" ", "_")
            if normalized in SENSITIVE_KEYS:
                errors.append(f"{prefix}.{key}: sensitive key is not allowed in public examples")
            errors.extend(find_sensitive_content(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(find_sensitive_content(child, f"{prefix}[{index}]"))
    elif isinstance(value, str):
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                errors.append(f"{prefix}: value resembles a secret")
    return errors


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("schema_version") != 1:
        errors.append("config.schema_version must be 1")
    connectors = config.get("connectors")
    if not isinstance(connectors, list) or not connectors:
        errors.append("config.connectors must be a non-empty array")
    else:
        for index, connector in enumerate(connectors):
            if connector.get("type") != "csv_file":
                errors.append(f"config.connectors[{index}].type must be csv_file in the public example")
            if connector.get("read_only") is not True:
                errors.append(f"config.connectors[{index}].read_only must be true")
    authority = config.get("authority", {})
    for action in PROHIBITED_AUTHORITIES:
        if authority.get(action) is not False:
            errors.append(f"config.authority.{action} must be false")
    excluded = config.get("analysis", {}).get("exclude_from_purchase_spending", [])
    for required in ("internal_transfer", "credit_card_payment", "refund", "cashback"):
        if required not in excluded:
            errors.append(f"config.analysis.exclude_from_purchase_spending must include {required}")
    errors.extend(find_sensitive_content(config, "config"))
    return errors


def validate_control_center(control_center: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if control_center.get("schema_version") != 1:
        errors.append("control_center.schema_version must be 1")
    if control_center.get("sample") is not True:
        errors.append("control_center.sample must be true in the public repository")
    if not parse_iso8601(control_center.get("updated_at", "")):
        errors.append("control_center.updated_at must be an ISO 8601 timestamp")
    labels = set(control_center.get("status_labels", []))
    if labels != EVIDENCE_STATUSES:
        errors.append("control_center.status_labels must contain the complete evidence-status set")
    fact_ids: set[str] = set()
    for index, fact in enumerate(control_center.get("facts", [])):
        path = f"control_center.facts[{index}]"
        fact_id = fact.get("id")
        if not isinstance(fact_id, str) or not fact_id:
            errors.append(f"{path}.id must be a non-empty string")
        elif fact_id in fact_ids:
            errors.append(f"{path}.id duplicates {fact_id}")
        else:
            fact_ids.add(fact_id)
        if fact.get("status") not in EVIDENCE_STATUSES:
            errors.append(f"{path}.status is invalid")
        if not parse_iso8601(fact.get("observed_at", "")):
            errors.append(f"{path}.observed_at must be an ISO 8601 timestamp")
        for required in ("domain", "statement", "source_ref", "assumptions", "remaining_uncertainty"):
            if not isinstance(fact.get(required), str):
                errors.append(f"{path}.{required} must be a string")
    for index, coverage in enumerate(control_center.get("source_coverage", [])):
        path = f"control_center.source_coverage[{index}]"
        for field in ("requested_start", "requested_end", "actual_oldest", "actual_newest"):
            try:
                date.fromisoformat(coverage.get(field, ""))
            except (TypeError, ValueError):
                errors.append(f"{path}.{field} must be an ISO date")
        if not parse_iso8601(coverage.get("observed_at", "")):
            errors.append(f"{path}.observed_at must be an ISO 8601 timestamp")
        if not coverage.get("freshness_note"):
            errors.append(f"{path}.freshness_note is required")
    for index, change in enumerate(control_center.get("change_log", [])):
        path = f"control_center.change_log[{index}]"
        if not parse_iso8601(change.get("changed_at", "")):
            errors.append(f"{path}.changed_at must be an ISO 8601 timestamp")
        for required in ("task", "source_ref", "old_state", "new_state", "remaining_uncertainty"):
            if not isinstance(change.get(required), str):
                errors.append(f"{path}.{required} must be a string")
    errors.extend(find_sensitive_content(control_center, "control_center"))
    return errors


def validate_accounts(accounts_payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if accounts_payload.get("sample") is not True:
        errors.append("accounts.sample must be true in the public repository")
    account_refs: set[str] = set()
    for index, account in enumerate(accounts_payload.get("accounts", [])):
        path = f"accounts.accounts[{index}]"
        account_ref = account.get("account_ref")
        if not isinstance(account_ref, str) or not account_ref.startswith("acct-"):
            errors.append(f"{path}.account_ref must be an opaque sample reference")
        elif account_ref in account_refs:
            errors.append(f"{path}.account_ref duplicates {account_ref}")
        else:
            account_refs.add(account_ref)
        if account.get("currency") != "USD":
            errors.append(f"{path}.currency must be USD in the public example")
    errors.extend(find_sensitive_content(accounts_payload, "accounts"))
    return errors


def validate_adapter(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    connector_config = config["connectors"][0]
    connector = CsvFileConnector(
        ROOT / connector_config["accounts_path"],
        ROOT / connector_config["transactions_path"],
        connector_config["source_ref"],
    )
    if not connector.read_only:
        errors.append("CSV connector must be read-only")
    try:
        batch = connector.sync(date(2026, 6, 1), date(2026, 8, 31))
    except (KeyError, TypeError, ValueError) as error:
        return [f"CSV connector validation failed: {error}"]
    account_refs = {account.account_ref for account in batch.accounts}
    if not account_refs:
        errors.append("CSV connector returned no accounts")
    if not batch.transactions:
        errors.append("CSV connector returned no sample transactions")
    for transaction in batch.transactions:
        if transaction.account_ref not in account_refs:
            errors.append(f"Transaction {transaction.transaction_ref} references an unknown account")
        if transaction.evidence_status not in EVIDENCE_STATUSES:
            errors.append(f"Transaction {transaction.transaction_ref} has an invalid status")
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(transaction.description):
                errors.append(f"Transaction {transaction.transaction_ref} description resembles a secret")
    if batch.actual_oldest != date(2026, 6, 1):
        errors.append("CSV connector actual_oldest is unexpected")
    if batch.actual_newest != date(2026, 8, 15):
        errors.append("CSV connector actual_newest is unexpected")
    return errors


def validate_workspace() -> list[str]:
    config = load_json(CONFIG_PATH)
    control_center = load_json(CONTROL_CENTER_PATH)
    accounts = load_json(ACCOUNTS_PATH)
    errors = validate_config(config)
    errors.extend(validate_control_center(control_center))
    errors.extend(validate_accounts(accounts))
    if not errors:
        errors.extend(validate_adapter(config))
    return errors


def main() -> int:
    errors = validate_workspace()
    if errors:
        print("Finance workspace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Finance workspace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

