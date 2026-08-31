from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_workspace.py"
SPEC = importlib.util.spec_from_file_location("finance_validator", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class FinanceWorkspaceValidationTests(unittest.TestCase):
    def test_public_workspace_is_valid(self) -> None:
        self.assertEqual([], VALIDATOR.validate_workspace())

    def test_sensitive_key_is_rejected(self) -> None:
        errors = VALIDATOR.find_sensitive_content({"connector": {"refresh_token": "not-real"}})
        self.assertTrue(any("refresh_token" in error for error in errors))

    def test_external_authority_must_remain_disabled(self) -> None:
        config = VALIDATOR.load_json(VALIDATOR.CONFIG_PATH)
        config["authority"]["submit_payment"] = True
        errors = VALIDATOR.validate_config(config)
        self.assertTrue(any("submit_payment" in error for error in errors))

    def test_invalid_fact_status_is_rejected(self) -> None:
        control_center = VALIDATOR.load_json(VALIDATOR.CONTROL_CENTER_PATH)
        control_center["facts"][0]["status"] = "GUESSED"
        errors = VALIDATOR.validate_control_center(control_center)
        self.assertTrue(any("status is invalid" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

