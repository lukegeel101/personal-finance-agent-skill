import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "evaluate_sample.py"
SPEC = importlib.util.spec_from_file_location("finance_evaluate_sample", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SampleEvaluationTests(unittest.TestCase):
    def test_evaluation_matches_expected_results(self) -> None:
        self.assertEqual(MODULE.evaluate_sample(), MODULE.load_json(MODULE.EXPECTED_PATH))

    def test_evaluation_never_takes_external_action(self) -> None:
        self.assertEqual(MODULE.evaluate_sample()["actions_taken"], 0)


if __name__ == "__main__":
    unittest.main()
