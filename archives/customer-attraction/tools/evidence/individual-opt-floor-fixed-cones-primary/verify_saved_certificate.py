"""Verify all saved fixed-cone bounds using only exact rational arithmetic.

Rebuild every ordered-history incentive coefficient from the original action
tables. No solver, imported game library, discovery, or strategy search is used.
The report saves one attaining primal per role, and a dual for every portfolio.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent


def check():
    started = time.monotonic()
    report_path = HERE / "original/individual_opt_floor_fixed_cones.json"
    raw = report_path.read_bytes()
    report = json.loads(raw)
    results = []
    for test in report["tests"]:
        source = HERE / "inputs" / Path(test["source"]).name
        data = source.read_bytes()
        assert sha256(data).hexdigest() == test["source_sha256"]
        m, p = test["players"], test["topics"]
        masks = tuple(range(1, 1 << p))
        entries = json.loads(data)["strategy"]["actions"]
        policy = {tuple(r["history"]): r["action"] for r in entries}
        histories = [h for d in range(m) for h in product(range(p), repeat=d)]
        assert len(policy) == len(entries) == len(histories) == test["ordered_nodes"]
        assert set(policy) == set(histories) and all(0 <= a < p for a in policy.values())

        def terminal(h):
            while len(h) < m:
                h = h + (policy[h],)
            return h

        def utility(outcome, role):
            return tuple(F(1, sum(bool(mask & (1 << a)) for a in outcome))
                         if mask & (1 << outcome[role]) else F(0) for mask in masks)

        def coverage(outcome):
            return tuple(F(any(mask & (1 << a) for a in outcome)) for mask in masks)

        rows = {}
        for h in histories:
            prescribed = utility(terminal(h), len(h))
            for a in range(p):
                alternative = utility(terminal(h + (a,)), len(h))
                rows[h, a] = tuple(u - v for u, v in zip(prescribed, alternative))
        assert len(rows) == test["whole_IC_rows_including_self"]
        actual = terminal(())
        assert list(actual) == test["actual_path"] and len(masks) == test["interest_types"]
        roles = []
        for role in test["roles"]:
            i = role["role_one_based"] - 1
            pay = utility(actual, i)
            bound = F(role["exact_maximum_gap"])
            expected = set(combinations_with_replacement(range(p), m))
            seen = set()
            dual_terms = 0
            for item in role["comparison_duals"]:
                portfolio = tuple(item["comparison"])
                assert portfolio in expected and portfolio not in seen
                seen.add(portfolio)
                objective = tuple(v - (2 * m - 1) * u
                                  for v, u in zip(coverage(portfolio), pay))
                upper = F(item["exact_upper"])
                assert upper <= bound
                slack = [upper - v for v in objective]
                for term in item["dual"]:
                    coefficient = F(term["multiplier"])
                    assert coefficient >= 0
                    row = rows[tuple(term["history"]), term["action"]]
                    for j, v in enumerate(row):
                        slack[j] -= coefficient * v
                    dual_terms += 1
                assert min(slack) >= 0
            assert seen == expected
            witness = role["attaining_primal"]
            masses = {mask: F(weight) for mask, weight in witness["weights"]}
            assert len(masses) == len(witness["weights"]) and set(masses) <= set(masks)
            assert min(masses.values()) >= 0 and sum(masses.values()) == 1
            weights = [masses.get(mask, F(0)) for mask in masks]
            for row in rows.values():
                assert sum(v * w for v, w in zip(row, weights)) >= 0
            objective = tuple(v - (2 * m - 1) * u
                              for v, u in zip(coverage(witness["comparison"]), pay))
            value = sum(v * w for v, w in zip(objective, weights))
            assert value == F(witness["value"]) == bound
            roles.append({"role": i + 1, "exact_maximum_gap": str(bound),
                          "portfolios": len(seen), "dual_terms": dual_terms,
                          "dual_coefficient_checks": len(seen) * len(masks),
                          "attaining_primal_IC_rows": len(rows)})
        results.append({"source_sha256": sha256(data).hexdigest(),
                        "players": m, "topics": p, "ordered_nodes": len(histories),
                        "IC_rows_including_self": len(rows), "actual_path": actual,
                        "roles": roles})
    return {"status": "PASS", "saved_report_sha256": sha256(raw).hexdigest(),
            "tests": results, "elapsed_seconds": time.monotonic() - started,
            "scope": "all saved portfolio duals and four saved attaining primals; no LP or search"}


if __name__ == "__main__":
    result = check()
    (HERE / "exact-recheck.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
