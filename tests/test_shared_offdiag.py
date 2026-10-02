"""Shared global optimum, balanced normal form, and overlap boundary checks."""

import copy
import json
import random
import unittest
from fractions import Fraction as Q
from pathlib import Path
from unittest.mock import patch

from facility_spe.exact import bounded_overlap as full
from facility_spe.exact import shared_offdiag as new


def complete_ne(instance, record):
    """Check conditional costs directly, independently of both solvers."""
    weights = list(map(Q, instance["weights"]))
    sites = list(map(set, instance["locations"]))
    s, t = record["layout"]
    common = sorted(sites[s] & sites[t])
    assert record["shared"] == common
    probabilities = list(map(Q, record["prob_first"]))
    assert len(probabilities) == len(common)
    x = sum((weights[i] for i in sites[s] - sites[t]), Q(0))
    y = sum((weights[i] for i in sites[t] - sites[s]), Q(0))
    x += sum((weights[i] * p for i, p in zip(common, probabilities)), Q(0))
    y += sum((weights[i] * (1 - p) for i, p in zip(common, probabilities)), Q(0))
    assert record["loads"] == [x, y]
    for i, p in zip(common, probabilities):
        assert 0 <= p <= 1
        cost1 = x + weights[i] * (1 - p)
        cost2 = y + weights[i] * p
        assert p == 0 or cost1 <= cost2
        assert p == 1 or cost2 <= cost1


class SharedOffdiagonalTests(unittest.TestCase):
    def compare(self, instance):
        out = new.solve(instance)
        normalized = dict(instance)
        if "U1" not in instance:
            normalized["U1"] = normalized["U2"] = list(range(len(instance["locations"])))
        reference = full.solve(normalized)
        self.assertEqual(out["alpha"], reference["alpha"])
        new.verify(instance, out)
        full.verify(normalized, out)
        serialized = json.loads(json.dumps(full.serial(out)))
        new.verify(instance, serialized)
        catalog = normalized["U1"]
        for s in catalog:
            for t in catalog:
                record = new.continuation(instance, out, s, t)
                complete_ne(instance, record)
                if s == t:
                    self.assertTrue(all(p == Q(1, 2) for p in record["prob_first"]))
        return out

    def test_boundary_and_random_reference_comparisons(self):
        cases = [
            {"weights": [], "locations": [[], [], []]},
            {"weights": [7], "locations": [[0]]},
            {"weights": [5], "locations": [[0], [0], []]},
            {"weights": [8, 40, 23], "locations": [[0, 1], [2], [1]]},
            {"weights": [1, 1, 1, 1], "locations": [[0, 1, 2, 3], [0, 1, 2, 3], [0, 2]]},
            {"weights": ["2/3", "7/5", "1/11"], "locations": [[0, 1], [], [1, 2]],
             "U1": [2, 0, 2], "U2": [0, 2]},
        ]
        rng = random.Random(2026100207)
        for _ in range(90):
            n, size = rng.randrange(7), rng.randrange(1, 5)
            cases.append({
                "weights": [str(Q(rng.randrange(1, 30), rng.randrange(1, 9))) for _ in range(n)],
                "locations": [[i for i in range(n) if rng.randrange(2)] for _ in range(size)],
            })
        for case in cases:
            with self.subTest(case=case):
                self.compare(case)

    def test_known_positive_gap_and_non_diagonal_optimum(self):
        simple = {"weights": [8, 40, 23], "locations": [[0, 1], [2], [1]]}
        self.assertEqual(self.compare(simple)["alpha"], Q(23, 20))
        lower = json.loads(Path("examples/shared/sharp_lower_rational.json").read_text())
        out = self.compare(lower)
        self.assertEqual(out["alpha"], Q(499750, 309017))
        self.assertEqual(out["on_path"]["layout"], [0, 4])
        diagonals = [rec["witness"] for rec in out["deviations"]
                     if len(set(rec["witness"]["layout"])) == 1]
        self.assertEqual(len(diagonals), 2)
        self.assertTrue(all(all(p == Q(1, 2) for p in rec["prob_first"])
                            for rec in diagonals))

    def test_small_sparse_catalog_threshold_witnesses(self):
        three = {"weights": [7071, 2929, 5000],
                 "locations": [[0, 1], [0], [2]]}
        self.assertEqual(self.compare(three)["alpha"], Q(7071, 5000))

        four = json.loads(Path("examples/shared/sparse_four_rational.json").read_text())
        self.assertEqual(self.compare(four)["alpha"], Q(6327, 4000))

        five = json.loads(Path("examples/shared/sharp_lower_rational.json").read_text())
        five["U1"] = five["U2"] = list(range(5))
        self.assertEqual(self.compare(five)["alpha"], Q(499750, 309017))

    def test_diagonal_tie_avoids_unsafe_balanced_punishment(self):
        instance = {"weights": [1] * 4, "locations": [list(range(4))] * 2}
        # This is an exact off-diagonal NE satisfying the relaxed H quotas at
        # factor one, but its first facility cannot withstand balanced (2, 2)
        # after moving to its opponent's site. A balanced diagonal has the same
        # optimal factor and must be selected instead of this relaxed witness.
        unsafe = {"layout": [0, 1], "shared": list(range(4)),
                  "prob_first": [Q(1), Q(1, 4), Q(1, 4), Q(1, 4)],
                  "loads": [Q(7, 4), Q(9, 4)]}
        complete_ne(instance, unsafe)
        self.assertGreater(Q(2), unsafe["loads"][0])
        out = self.compare(instance)
        self.assertEqual(out["alpha"], 1)
        self.assertEqual(out["on_path"]["layout"][0], out["on_path"]["layout"][1])

    def test_huge_diagonal_overlap_never_enumerated(self):
        size = 200
        instance = {
            "weights": [40] + [str(Q(8, size))] * size + [str(Q(23, size))] * size,
            "locations": [[0] + list(range(1, size + 1)),
                          list(range(size + 1, 2 * size + 1)), [0]],
        }
        calls = []

        def distinct_local(weights, sites, s, t):
            self.assertNotEqual(s, t)
            self.assertLessEqual(len(sites[s] & sites[t]), 1)
            calls.append((s, t))
            return full.local(weights, sites, s, t)

        with patch.object(new, "local", side_effect=distinct_local):
            out = new.solve(instance)
        self.assertEqual(len(calls), 3)
        self.assertEqual(out["local_calls"], 3)
        self.assertEqual(out["distinct_overlap"], 1)
        self.assertEqual(out["alpha"], Q(23, 20))
        new.verify(instance, out)
        for s in range(3):
            for t in range(3):
                complete_ne(instance, new.continuation(instance, out, s, t))
        singleton = {"weights": [1] * size, "locations": [list(range(size))]}
        with patch.object(new, "local", side_effect=AssertionError("diagonal enumeration")):
            out = new.solve(singleton)
        self.assertEqual(out["alpha"], 1)
        self.assertEqual(out["distinct_overlap"], 0)
        new.verify(singleton, out)

    def test_heterogeneous_and_damaged_certificates_rejected(self):
        with self.assertRaises(ValueError):
            new.solve({"weights": [1], "locations": [[0], []], "U1": [0], "U2": [1]})
        with self.assertRaises(ValueError):
            new.solve({"weights": [1], "locations": [[0]], "U1": [0]})
        with self.assertRaises(ValueError):
            new.solve({"weights": [1.0], "locations": [[0]]})
        instance = {"weights": [8, 40, 23], "locations": [[0, 1], [2], [1]]}
        out = new.solve(instance)
        damaged = copy.deepcopy(out)
        damaged["alpha"] = Q(1)
        with self.assertRaises(ValueError):
            new.verify(instance, damaged)
        damaged = copy.deepcopy(out)
        damaged["deviations"].pop()
        with self.assertRaises(ValueError):
            new.verify(instance, damaged)


if __name__ == "__main__":
    unittest.main()
