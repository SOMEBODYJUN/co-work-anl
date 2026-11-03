"""Verify the saved MG upper certificates, without LP/MILP or model imports.

This verifies complete ordered action maps and every saved dual coefficient.
The historical reports do not retain the primal vectors underlying their
best_normalized_violation fields; those fields are only checked for literal
consistency with the reported largest upper bound, not certified as lower bounds.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import collections
import hashlib
import json

HERE = Path(__file__).resolve().parent


def load(name, directory="original"):
    return json.loads((HERE / directory / name).read_text())


@lru_cache(None)
def payoff(p, q, a):
    return tuple(F(1, sum(q[b] for b in range(p) if mask & (1 << b)))
                 if mask & (1 << a) else F(0)
                 for mask in range(1, 1 << p))


def coverage(p, support):
    mask = sum(1 << a for a in support)
    return tuple(F(bool(mask & s)) for s in range(1, 1 << p))


def policy(strategy, p, m):
    entries = strategy["actions"]
    actions = {tuple(e["history"]): e["action"] for e in entries}
    required = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert len(actions) == len(entries) and set(actions) == required
    assert all(type(a) is int and 0 <= a < p for a in actions.values())
    terminals = {h: tuple(h.count(a) for a in range(p))
                 for h in product(range(p), repeat=m)}
    for d in reversed(range(m)):
        for h in product(range(p), repeat=d):
            terminals[h] = terminals[h + (actions[h],)]
    root = terminals[()]
    if "terminal_counts" in strategy:
        assert tuple(strategy["terminal_counts"]) == root
    rows = set()
    for h, a in actions.items():
        actual = payoff(p, terminals[h], a)
        for b in range(p):
            if b != a:
                dev = payoff(p, terminals[h + (b,)], b)
                row = tuple(x - y for x, y in zip(actual, dev))
                if any(row):
                    rows.add(row)
    rows = tuple(sorted(rows))
    w = coverage(p, (a for a, n in enumerate(root) if n))
    signature = hashlib.sha256(json.dumps(sorted((list(h), a) for h, a in actions.items()),
                                         separators=(",", ":")).encode()).hexdigest()
    return {"actions": actions, "root": root, "rows": rows, "w": w,
            "p": p, "m": m, "signature": signature}


def check_scan(report, cone):
    assert set(report) == {"status", "origin", "best_normalized_violation", "lp_calls",
                           "all_objectives_have_exact_duals", "exact_dual_upper_bound",
                           "failed_duals", "duals"}
    assert report["status"] == "no_counterexample_found"
    p, m, q, rows, w = (cone[k] for k in ("p", "m", "root", "rows", "w"))
    expected = {(J, a) for J in combinations(range(p), min(p, m))
                for a, n in enumerate(q) if n}
    assert report["lp_calls"] == len(expected)
    seen = set()
    bounds = []
    multipliers = residuals = strict_residuals = 0
    details = []
    for proof in report["duals"]:
        assert set(proof) == {"support", "topic", "upper_bound", "nonzero_multipliers"}
        key = (tuple(proof["support"]), proof["topic"])
        assert key in expected and key not in seen
        seen.add(key)
        J, a = key
        c = tuple(o - v - m * u for o, v, u in
                  zip(coverage(p, J), w, payoff(p, q, a)))
        beta = F(proof["upper_bound"])
        mu = {}
        for i, value in proof["nonzero_multipliers"]:
            assert type(i) is int and i in range(len(rows)) and i not in mu
            mu[i] = F(value)
            assert mu[i] > 0
        rs = [beta * w[j] - sum((v * rows[i][j] for i, v in mu.items()), F(0)) - c[j]
              for j in range((1 << p) - 1)]
        assert min(rs) >= 0 and beta <= F(-1, 4)
        bounds.append(beta)
        multipliers += len(mu)
        residuals += len(rs)
        strict_residuals += sum(r > 0 for r in rs)
        details.append({"support": list(J), "topic": a, "upper_bound": str(beta),
                        "nonzero_multipliers": len(mu), "minimum_residual": str(min(rs))})
    missing = sorted(expected - seen)
    assert report["failed_duals"] == len(missing)
    assert report["all_objectives_have_exact_duals"] is (not missing)
    assert F(report["exact_dual_upper_bound"]) == max(bounds)
    # An agreement of two saved numbers is not an independent primal check.
    assert F(report["best_normalized_violation"]) == max(bounds)
    return {"origin": report["origin"], "topics": p, "players": m,
            "decision_histories": len(cone["actions"]),
            "nonself_ordered_deviations": len(cone["actions"]) * (p - 1),
            "nonzero_distinct_IC_rows": len(rows), "root_counts": list(q),
            "strategy_signature": cone["signature"], "expected_objectives": len(expected),
            "verified_duals": len(bounds), "verified_nonzero_multipliers": multipliers,
            "verified_coefficient_residuals": residuals, "strict_positive_residuals": strict_residuals,
            "largest_verified_upper_bound": str(max(bounds)),
            "missing_duals": [{"support": list(J), "topic": a} for J, a in missing],
            "primal_vectors_saved": False, "dual_details": details}


def main():
    manifest = load("source-manifest.json", ".")
    for entry in manifest:
        data = (HERE / entry["artifact"]).read_bytes()
        assert len(data) == entry["size"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == entry["blob"]
    fixed = load("minimum_gap_scan.json")
    assert len(fixed) == 73
    sample = load("customer_attraction_strategy_lp_m4p5_certified.json", "dependencies")
    assert len(sample["cone_proofs"]) == 70
    records = []
    for i, r in enumerate(fixed):
        if i < 3:
            name, p, m = [("root_tax_failure.json", 6, 4),
                          ("individual_security_failure.json", 6, 3),
                          ("eight_cce_welfare_gap.json", 4, 3)][i]
            obj = load(name, "dependencies")
            strategy = obj.get("strategy", obj)
            assert r["origin"] == "evidence/certificates/customer_attraction/" + name
        else:
            p, m = 5, 4
            strategy = sample["cone_proofs"][i - 3]
            assert r["origin"] == ("evidence/runs/2026-10-09/"
                                    "customer_attraction_strategy_lp_m4p5_certified.json:cone=" + str(i - 3))
        records.append(check_scan(r, policy(strategy, p, m)))
    joint = load("minimum_gap_joint.json")
    assert len(joint) == 4
    joint_records = []
    for i, r in enumerate(joint):
        assert set(r) == {"topics", "path", "portfolio", "tested_topic", "milp", "strategy", "exact_scan"}
        assert (r["topics"], r["path"], r["portfolio"], r["tested_topic"]) == (
            4, [0, 1, 1] if i < 2 else [0, 1, 2], [1, 2, 3] if i % 2 == 0 else [0, 2, 3], 0)
        meta = r["milp"]
        assert set(meta) == {"status", "message", "variables", "binary_actions",
                             "inequalities_and_equalities", "seconds", "floating_objective",
                             "floating_mip_gap", "floating_bound_not_a_certificate"}
        assert meta["status"] == 0 and meta["variables"] == 183
        assert meta["binary_actions"] == 84 and meta["inequalities_and_equalities"] == 952
        assert meta["floating_bound_not_a_certificate"] is True and meta["floating_mip_gap"] == 0
        assert meta["seconds"] > 0
        cone = policy(r["strategy"], 4, 3)
        h = ()
        while len(h) < 3:
            h += (cone["actions"][h],)
        assert list(h) == r["path"]
        checked = check_scan(r["exact_scan"], cone)
        checked.update({"case": i, "path": list(h), "MILP_target_portfolio": r["portfolio"],
                        "MILP_target_topic": r["tested_topic"], "historical_milp": meta})
        joint_records.append(checked)
    all_records = records + joint_records
    report = {"scope": "saved complete-policy MG upper certificates only; no LP or MILP executed",
              "source_files_integrity_verified": len(manifest),
              "fixed_scan_records": len(records),
              "fixed_scan_distinct_policy_signatures": len({r["strategy_signature"] for r in records}),
              "fixed_scan_objectives": sum(r["expected_objectives"] for r in records),
              "fixed_scan_verified_duals": sum(r["verified_duals"] for r in records),
              "fixed_scan_complete_dual_cones": sum(not r["missing_duals"] for r in records),
              "joint_records": len(joint_records),
              "joint_distinct_policy_signatures": len({r["strategy_signature"] for r in joint_records}),
              "joint_objectives": sum(r["expected_objectives"] for r in joint_records),
              "joint_verified_duals": sum(r["verified_duals"] for r in joint_records),
              "verified_nonzero_multipliers": sum(r["verified_nonzero_multipliers"] for r in all_records),
              "verified_coefficient_residuals": sum(r["verified_coefficient_residuals"] for r in all_records),
              "largest_verified_upper_bound": str(max(F(r["largest_verified_upper_bound"]) for r in all_records)),
              "historical_primal_best_fields_independently_certified": False,
              "floating_global_MILP_bounds_certified": False,
              "fixed_records": records, "joint_details": joint_records}
    (HERE / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("fixed_records", "joint_details")}))


if __name__ == "__main__":
    main()
