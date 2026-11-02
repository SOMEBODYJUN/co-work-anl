"""Audit saved concrete inputs; never run/overwrite the original search main.

The old 36-case review has no customer weights. The explicitly saved new
mixed-prefix inputs below are new tests, not a reproduction of that old run.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "frozen_satellite", BASE / "original/symmetric_core_satellite.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SymmetricSolver = module.SymmetricSolver
ExactSPESolver = module.ExactSPESolver


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def portfolio(instance, q, price, z):
    assert all(0 <= v <= 1 for v in z)
    value = sum((customer.multiplicity * min(
        F(1), sum((z[a] for a in customer.topics), F()))
        for customer in instance.customers), F()) - price * sum(z, F())
    return value / instance.welfare(q)


def main():
    fingerprints = []
    for entry in json.loads((BASE / "source-manifest.json").read_text()):
        path = BASE / "original" / Path(entry["path"]).name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == entry["sha256"]
        fingerprints.append({"id": entry["id"], "sha256": digest})

    # This is precisely the original function's 288 seeded comparisons.
    basic = module.self_test()
    assert basic["comparisons"] == 288

    # New fully materialized test inputs, using a separate explicitly named seed.
    rng = random.Random(2026110207)
    mixed = []
    for m, k, ell in [(6, 1, 3), (6, 2, 3), (7, 2, 4)]:
        for trial in range(4):
            sw = [rng.randrange(7) for _ in range(1 << k)]
            cw = [0] + [rng.randrange(7) for _ in range(1, 1 << k)]
            symmetry = SymmetricSolver(m, k, ell, sw, cw)
            ordinary = ExactSPESolver(symmetry.instance())
            prefixes = [(0,) * k + (0,) * (ell - 2) + (1, 2),
                        (0,) * k + (0,) * (ell - 2) + (2, 2),
                        (1,) + (0,) * (k - 1) + (0,) * (ell - 2) + (1, 2)]
            for prefix in prefixes:
                expected = {symmetry.canonical(prefix, q)
                            for q in ordinary.outcomes(prefix)}
                observed = symmetry.solve(prefix)
                assert set(observed) == expected
                mixed.append({"m": m, "k": k, "ell": ell, "trial": trial,
                              "satellite_weights": sw, "core_weights": cw,
                              "prefix": prefix, "outcomes": sorted(observed)})
    assert len(mixed) == 36

    # All-zero customers retain every tie. The chosen satellite joins a class
    # whose child outcome contains distinct final loads; both lifts are needed.
    zero = SymmetricSolver(4, 1, 3, [0, 0], [0, 0])
    prefix = (0, 0, 1, 1)
    target_child = (0, 1, 1, 2)
    transitions = zero.child_transitions(prefix, 1)
    lifted = sorted({q for q, value in transitions if q[0] == 0})
    expected = {zero.canonical(prefix, q)
                for q in ExactSPESolver(zero.instance()).outcomes(prefix)}
    assert set(zero.solve(prefix)) == expected
    assert (0, 1, 1, 2) in lifted and (0, 2, 1, 1) in lifted
    zero_control = {"m": 4, "k": 1, "ell": 3,
                    "satellite_weights": [0, 0], "core_weights": [0, 0],
                    "prefix": prefix, "child_state": (0, 1, 1, 1),
                    "target_child_outcome": target_child,
                    "its_distinct_parent_lifts": [(0, 1, 1, 2), (0, 2, 1, 1)],
                    "all_parent_outcomes": sorted(zero.solve(prefix))}

    reports = []
    for filename in ["symmetric_m8_k3_l8.json", "symmetric_m9_k2_l9.json"]:
        old = json.loads((BASE / "original" / filename).read_text())
        p = old["parameters"]
        rows = []
        ratios = []
        pricing_scores = []
        for row in old["records"]:
            solver = SymmetricSolver(p["players"], p["cores"], p["satellites"],
                                     row["satellite_weights"], row["core_weights"])
            instance = solver.instance()
            outcomes = solver.solve()
            q = tuple(row["worst"])
            assert q in outcomes
            # Canonical Instance uses separate Fraction/type incidence formulas.
            welfares = {c: instance.welfare(c) for c in outcomes}
            assert all(solver.welfare(c) == w for c, w in welfares.items())
            W = min(welfares.values())
            OPT = instance.optimal_welfare()
            assert instance.welfare(q) == W == row["W"]
            assert OPT == row["OPT"]
            ratio = F(OPT, W)
            assert ratio == F(row["ratio"])
            assert len(outcomes) == row["outcomes"]
            assert len(solver.cache) == row["states"]
            payoffs = instance.topic_payoffs(q)
            minimum = min(value for a, value in enumerate(payoffs) if q[a])
            assert minimum == F(row["min_occupied_payoff"])
            assert all(F(solver.utilities(q)[a], solver.L) == payoffs[a]
                       for a in range(instance.topic_count) if q[a])
            result = {"step": row["step"], "outcomes": sorted(outcomes),
                      "states": len(solver.cache), "W": W, "OPT": OPT,
                      "ratio": str(ratio), "min_occupied_payoff": str(minimum)}
            ratios.append(ratio)
            if "best_price_portfolio_over_W" in row:
                price_q = tuple(row["price_counts"])
                assert price_q in outcomes
                price = min(value for a, value in enumerate(
                    instance.topic_payoffs(price_q)) if price_q[a])
                assert price == F(row["price"])
                compact_z = tuple(map(F, row["z_cores_and_common_satellite"]))
                z = compact_z[:-1] + (compact_z[-1],) * p["satellites"]
                score = portfolio(instance, price_q, price, z)
                assert score == F(row["best_price_portfolio_over_W"])
                # All eight-player saved roots have one orbit. No numeric
                # portfolio solver, optimum or exact upper bound is certified.
                assert len(outcomes) == 1
                result["saved_feasible_portfolio_over_W"] = str(score)
                pricing_scores.append(score)
            rows.append(result)
        assert len(rows) == p["steps"]
        assert max(ratios) == F(old["best_ratio"])
        report = {"file": filename, "parameters": p, "records": rows,
                  "best_ratio": str(max(ratios)),
                  "pricing_LP_executions": 0,
                  "production_argv_or_code_hash_recovered": False}
        if pricing_scores:
            assert max(pricing_scores) == F(old["best_exact_price_lower_over_W"])
            report["best_saved_feasible_portfolio_over_W"] = str(max(pricing_scores))
        reports.append(report)

    review = json.loads((BASE / "original/satellite_quotient_review.json").read_text())
    assert len(review["records"]) == review["comparisons"] == 36
    assert sum(row["outcome_orbits"] == 2 for row in review["records"]) == 2
    assert all(set(row) == {"m", "k", "ell", "trial", "prefix", "outcome_orbits"}
               for row in review["records"])

    output = {"status": "all concrete checks passed", "source_fingerprints": fingerprints,
              "original_self_test": basic, "new_mixed_seed": 2026110207,
              "new_mixed_comparisons": mixed, "zero_customer_merge_control": zero_control,
              "saved_reports_recomputed": reports,
              "old_36_case_review": {"records_read": 36, "two_orbit_records": 2,
                  "replayed": False, "missing": ["customer weights", "generation program",
                                                   "exact old outcome sets"]},
              "main_executions": 0, "pricing_LP_executions": 0}
    dump(BASE / "verification.json", output)
    print(json.dumps({"status": output["status"], "basic_comparisons": 288,
                      "new_mixed_comparisons": 36, "zero_customer_controls": 1,
                      "saved_input_records": sum(len(r["records"]) for r in reports),
                      "pricing_LP_executions": 0, "old_36_replayed": False}))


if __name__ == "__main__":
    main()
