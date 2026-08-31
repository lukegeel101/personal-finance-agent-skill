from __future__ import annotations

import sys
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finance_control import CsvFileConnector, FinancialConnector, category_totals, deduplicate_transactions, purchase_spending, recurring_candidates


class AdapterAndAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.connector = CsvFileConnector(
            ROOT / "data" / "sample" / "accounts.json",
            ROOT / "data" / "sample" / "transactions.csv",
            "mock-csv-source",
        )
        cls.batch = cls.connector.sync(date(2026, 6, 1), date(2026, 8, 31))

    def test_connector_satisfies_protocol_and_is_read_only(self) -> None:
        self.assertIsInstance(self.connector, FinancialConnector)
        self.assertTrue(self.connector.read_only)

    def test_connector_records_actual_coverage(self) -> None:
        self.assertEqual(date(2026, 6, 1), self.batch.actual_oldest)
        self.assertEqual(date(2026, 8, 15), self.batch.actual_newest)
        self.assertEqual(16, len(self.batch.transactions))

    def test_deduplication_prefers_stronger_evidence(self) -> None:
        original = self.batch.transactions[0]
        stronger = replace(
            original,
            transaction_ref="statement-copy",
            source_ref="mock-statement-source",
            evidence_status="CONFIRMED",
        )
        result = deduplicate_transactions([original, stronger])
        self.assertEqual(1, len(result))
        self.assertEqual("CONFIRMED", result[0].evidence_status)

    def test_purchase_spending_excludes_reconciliation_categories(self) -> None:
        excluded = {
            "internal_transfer",
            "credit_card_payment",
            "refund",
            "cashback",
            "cash_withdrawal",
        }
        spending = purchase_spending(self.batch.transactions, excluded)
        categories = {transaction.category for transaction in spending}
        self.assertNotIn("credit_card_payment", categories)
        self.assertNotIn("refund", categories)
        self.assertNotIn("cashback", categories)
        self.assertEqual(265.75, category_totals(spending)["groceries"])

    def test_monthly_recurring_candidates_are_detected(self) -> None:
        candidates = recurring_candidates(self.batch.transactions)
        descriptors = {candidate["descriptor"] for candidate in candidates}
        self.assertIn("STREAMFLIX EXAMPLE", descriptors)
        self.assertIn("EXAMPLE RENTAL HOUSING", descriptors)


if __name__ == "__main__":
    unittest.main()

