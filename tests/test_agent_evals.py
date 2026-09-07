"""Regression checks for the model-first S1 eval integration."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_agent_evals as runner


class ModelFirstEvalTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / "config/workflow-policy.json").read_text())
        self.cases = runner.load_cases(ROOT / "evals/cases")

    def test_current_cases_match_native_and_activated_routes(self):
        runner.validate_cases(self.cases, self.policy)
        self.assertEqual({c["expected"]["tier"] for c in self.cases}, {"native", "compact", "full"})

    def test_changed_tier_module_gate_or_contract_is_rejected(self):
        source = next(c for c in self.cases if c["id"] == "full-security-signal")
        for field, value in [("tier", "native"), ("modules", []),
                             ("humanGate", False), ("writesBeforeContract", True)]:
            with self.subTest(field=field):
                changed = copy.deepcopy(source)
                changed["expected"][field] = value
                self.assertTrue(runner.validate_case(changed, self.policy))

    def test_policy_and_case_cannot_agree_on_a_deleted_module(self):
        source = copy.deepcopy(next(c for c in self.cases if c["expected"]["tier"] == "compact"))
        obsolete = ["agents/workflows/inline.md"]
        self.policy["agentEvals"]["requiredModulesByTier"]["compact"] = obsolete
        source["expected"]["modules"] = obsolete
        errors = runner.validate_case(source, self.policy)
        self.assertTrue(any("module does not exist" in error for error in errors), errors)

    def test_external_scorer_rejects_wrong_model_first_outcome(self):
        results = [{"caseId": c["id"], **c["expected"]} for c in self.cases]
        self.assertEqual(runner.score_results(self.cases, results), (len(self.cases), 0))
        results[0]["tier"] = "inline"
        with self.assertRaises(runner.EvalError):
            runner.score_results(self.cases, results)

    def test_invalid_fact_types_return_diagnostics_instead_of_type_errors(self):
        source = next(c for c in self.cases if c["id"] == "full-security-signal")
        for field, value in [("signals", 1), ("risks", "security"), ("files", "6"),
                             ("multipleDeliverableGoals", "yes")]:
            with self.subTest(field=field):
                changed = copy.deepcopy(source)
                changed["facts"][field] = value
                errors = runner.validate_case(changed, self.policy)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_invalid_case_and_expected_types_return_diagnostics(self):
        source = next(c for c in self.cases if c["id"] == "full-security-signal")
        changes = [
            (("id",), 12, "id"),
            (("expected", "tier"), 12, "tier"),
            (("expected", "tier"), "inline", "tier"),
            (("expected", "modules"), "agents/workflows/full.md", "modules"),
            (("expected", "modules"), [12], "modules"),
            (("expected", "humanGate"), 1, "humanGate"),
            (("expected", "writesBeforeContract"), 0, "writesBeforeContract"),
            (("expected", "capabilityStatus"), "maybe", "capabilityStatus"),
            (("expected", "promotion"), 1, "promotion"),
            (("expected", "promotion"), "", "promotion"),
        ]
        for path, value, marker in changes:
            with self.subTest(path=path, value=value):
                changed = copy.deepcopy(source)
                target = changed
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                errors = runner.validate_case(changed, self.policy)
                self.assertTrue(any(marker in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
