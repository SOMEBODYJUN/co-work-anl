import argparse
import json
from pathlib import Path
import tempfile
import unittest

from cncrisis import compute


class ComputeTests(unittest.TestCase):
    def test_completed_job_is_reused_and_changed_input_is_recomputed(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            spec = base / "input.json"
            spec.write_text(json.dumps({"input_kind": "synthetic_test", "opening_debt": 100,
                "new_financing": 0, "principal_repaid": 1, "writeoff": 0, "revaluation": 0,
                "opening_cash": 2, "cash_receipts": 0, "cash_payments": 1}))
            plan = base / "plan.json"
            plan.write_text(json.dumps({"budget_period": "fixture", "allocated_cores": 2,
                "plan_core_hour_budget": 1, "jobs": [{"id": "account", "method": "stock-flow", "input": str(spec)}]}))
            args = argparse.Namespace(file=plan, workspace=base / "work", compute_command="run", session_seconds=30)
            compute.execute(args)
            compute.execute(args)
            ledger = json.loads((args.workspace / "compute/ledger.json").read_text())
            self.assertEqual(len(ledger["runs"]), 1)
            data = json.loads(spec.read_text()); data["opening_debt"] = 90
            spec.write_text(json.dumps(data))
            compute.execute(args)
            ledger = json.loads((args.workspace / "compute/ledger.json").read_text())
            self.assertEqual(len(ledger["runs"]), 2)
            self.assertNotEqual(ledger["runs"][0]["fingerprint"], ledger["runs"][1]["fingerprint"])

    def test_exhausted_plan_starts_no_new_job(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d); workspace = base / "work"; (workspace / "compute").mkdir(parents=True)
            plan = base / "plan.json"
            plan.write_text(json.dumps({"budget_period": "fixture", "allocated_cores": 2,
                "plan_core_hour_budget": 1, "jobs": [{"id": "not-started", "method": "stock-flow", "input": "nonexistent.json"}]}))
            (workspace / "compute/ledger.json").write_text(json.dumps({"schema": "cncrisis-compute-ledger.v1", "budget_period": "fixture",
                "sessions": [{"estimated_core_hours": 1, "status": "finished"}], "runs": []}))
            result = compute.execute(argparse.Namespace(file=plan, workspace=workspace, compute_command="run", session_seconds=30))
            self.assertEqual(result["session"]["status"], "budget_or_session_limit")
            self.assertEqual(result["runs"], [])
