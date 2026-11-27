import copy
import json
from pathlib import Path
import unittest

from cncrisis import methods


class MethodTests(unittest.TestCase):
    def test_loan_matches_vendored_reference_and_identity(self):
        for principal, annual, months in [(1000, 0, 10), (1000, .12, 1), (1000000, .03, 240)]:
            result = methods.loan({"principal": principal, "annual_rate": annual, "months": months})
            self.assertLess(result["reference_error"], 1e-6)
            self.assertAlmostEqual(sum(x["principal"] for x in result["schedule"]), principal, places=6)
            self.assertAlmostEqual(result["schedule"][-1]["balance"], 0, places=6)
            self.assertTrue(all(x["balance"] >= 0 for x in result["schedule"]))
            npf = methods._financial()
            for row in result["schedule"]:
                self.assertAlmostEqual(row["interest"], float(-npf.ipmt(annual/12, row["month"], months, principal)), places=6)
                self.assertAlmostEqual(row["principal"], float(-npf.ppmt(annual/12, row["month"], months, principal)), places=6)

    def test_stock_flow_refinancing_does_not_erase_debt(self):
        data = {"opening_debt": 100, "new_financing": 20, "principal_repaid": 20, "writeoff": 0, "revaluation": 0, "opening_cash": 1, "cash_receipts": 1, "cash_payments": 3}
        result = methods.stock_flow(data)
        self.assertEqual(result["ending_debt"], 100)
        self.assertEqual(result["cash_shortfall"], 1)
        self.assertEqual(result["cash_usable"], 0)
        self.assertEqual(result["debt_identity_residual"], 0)
        with self.assertRaises(ValueError):
            methods.stock_flow(dict(data, principal_repaid=500))

    def test_bridge_future_training_does_not_leak(self):
        data = json.loads((methods.FIXTURES/"synthetic_panel.json").read_text())
        original = methods.bridge(data)
        changed = copy.deepcopy(data)
        changed["quarterly_gdp"][-1] = 1000000
        rerun = methods.bridge(changed)
        self.assertEqual(original["predictions"][0], rerun["predictions"][0])
        self.assertEqual(original["predictions"][-1]["bridge"], rerun["predictions"][-1]["bridge"])
        self.assertEqual(original["n_test"], 20)

    def test_nowcast_news_reconciles_two_vintages(self):
        result = methods.nowcast(None)
        self.assertTrue(result["converged"])
        self.assertEqual(result["n_new_observations"], 2)
        self.assertLess(result["news_reconciliation_error"], 1e-7)
        self.assertAlmostEqual(result["updated_estimate"]-result["previous_estimate"], result["news_impact"], places=7)

    def test_observed_data_replay_matches_saved_fetch(self):
        receipt = json.loads((methods.FIXTURES/"akshare_live_receipt.json").read_text())
        result = methods.akshare(None)
        self.assertEqual(result["rows"], receipt["rows"])
        self.assertEqual(result["sha256"], receipt["input_sha256"])
        self.assertEqual(result["input_kind"], "observed_vendor_series")

    def test_vendored_sources_integrity(self):
        self.assertEqual(methods.doctor()["vendor_integrity"], "pass")


if __name__ == "__main__":
    unittest.main()
