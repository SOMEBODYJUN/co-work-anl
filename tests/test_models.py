import copy
import json
from pathlib import Path
import tempfile
import unittest

from cncrisis.models import bank_stress, early_warning, _split_panel

ROOT = Path(__file__).resolve().parents[1]


class BankStressTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "tests/fixtures/models/bank.json").read_text())

    def test_allowances_cash_and_liquidity_support_have_distinct_effects(self):
        rows = bank_stress(self.data)["results"]
        self.assertEqual(rows[0]["gross_credit_loss"], 8)
        self.assertEqual(rows[0]["opening_allowance_used"], 3)
        self.assertEqual(rows[0]["ending_capital"], 6)
        self.assertEqual(rows[2]["ending_capital"], 6)
        self.assertAlmostEqual(rows[1]["liquid_assets_sold_book"], 14 / .9)
        self.assertAlmostEqual(rows[1]["ending_capital"], 6 - 14 / 9)

    def test_unfunded_runoff_is_not_automatic_borrowing(self):
        self.data["scenarios"][0]["deposit_runoff_fraction"] = 1
        row = bank_stress(self.data)["results"][0]
        self.assertAlmostEqual(row["unmet_funding_need"], 71)
        self.assertEqual(row["cash_available_after_requested_outflows"], 0)

    def test_bad_balance_sheet_is_detected(self):
        self.data["banks"][0]["cash"] += 1
        with self.assertRaisesRegex(ValueError, "does not reconcile"):
            bank_stress(self.data)

    def test_existing_negative_equity_remains_visible(self):
        self.data["banks"][0].update(capital=-5, other_liabilities=35)
        self.assertEqual(bank_stress(self.data)["results"][0]["ending_capital"], -9)


class WarningTests(unittest.TestCase):
    def setUp(self):
        import pandas as pd
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.csv = Path(self.tmp.name) / "data.csv"
        rows = []
        for c in ("A", "B", "C"):
            for y in list(range(1950, 1981)) + list(range(1985, 1995)) + list(range(2000, 2011)):
                event = int(y % 4 == 0)
                rows.append({"country": c, "as_of": f"{y}-12-31", "horizon_end": f"{y + 1}-12-31",
                    "available_at": f"{y}-06-01", "event": event,
                    "event_id": f"{c}-{y + 1}" if event else "", "event_date": f"{y + 1}-12-31" if event else "",
                    "x": y % 7, "z": y % 3})
        self.frame = pd.DataFrame(rows)
        self.frame.to_csv(self.csv, index=False)
        self.spec = {"input_kind": "synthetic_test", "csv": str(self.csv), "features": ["x", "z"],
            "target_definition": "synthetic future event", "information_mode": "verified_release_vintages",
            "label_observed_through": "2012-12-31", "models": ["logit"], "threads": 1,
            "split": {"train_end": "1984-12-31", "calibration_start": "1985-01-01", "calibration_end": "1994-12-31", "test_start": "2000-01-01", "test_end": "2010-12-31"},
            "alarm_rule": {"calibration_false_alarm_budget": .1, "decision_rationale": "fixture"}}

    def test_future_target_changes_do_not_change_predictions_or_threshold(self):
        old = early_warning(self.spec)
        mask = self.frame.as_of == "2000-12-31"
        self.frame.loc[mask, "event"] = 0
        self.frame.loc[mask, ["event_id", "event_date"]] = ""
        self.frame.to_csv(self.csv, index=False)
        new = early_warning(self.spec)
        self.assertEqual([r["score"] for r in old["test_predictions"]], [r["score"] for r in new["test_predictions"]])
        self.assertEqual(old["models"]["logit"]["alarm_threshold"], new["models"]["logit"]["alarm_threshold"])

    def test_future_release_is_detected(self):
        self.frame.loc[0, "available_at"] = "2020-01-01"
        with self.assertRaisesRegex(ValueError, "Feature release"):
            _split_panel(self.frame, self.spec)

    def test_country_holdout_never_enters_train_or_calibration(self):
        self.spec["heldout_countries"] = ["C"]
        parts = _split_panel(self.frame, self.spec)
        self.assertNotIn("C", parts["train"].country.unique())
        self.assertNotIn("C", parts["calibration"].country.unique())
        self.assertEqual(set(parts["test"].country), {"C"})

    def test_unmatured_labels_are_purged(self):
        self.frame.loc[self.frame.as_of == "1980-12-31", "horizon_end"] = "1985-01-01"
        parts = _split_panel(self.frame, self.spec)
        self.assertFalse((parts["train"].as_of.dt.year == 1980).any())
