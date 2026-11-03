"""Check the one saved 21-term dual, without LP, BI, or author imports.

The report already contains an old definition-level all-history SPE check.
This new check addresses only the previously unbound exact upper certificate:
its row indices refer to sorted distinct nonzero full-strategy IC rows.
The formulas and row ordering are the mature StrategyCone convention.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round4_credible/dummy_joint_trial.json"


def main():
    raw = SOURCE.read_bytes()
    report = json.loads(raw)
    exact = report["exact"]
    actions = {}
    for item in exact["strategy"]["actions"]:
        h = tuple(item["history"])
        if h in actions:
            raise ValueError("repeated history")
        actions[h] = item["action"]
    p, m = 7, 5
    expected = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert set(actions) == expected
    assert all(type(a) is int and a in range(p) for a in actions.values())

    @lru_cache(None)
    def finish(h):
        if len(h) == m:
            return tuple(h.count(a) for a in range(p))
        return finish(h + (actions[h],))

    @lru_cache(None)
    def payoff_row(q, a):
        return tuple(F(1, sum(q[b] for b in range(p) if mask >> b & 1))
                     if mask >> a & 1 else F(0)
                     for mask in range(1, 1 << p))

    rows = set()
    for h, a in actions.items():
        chosen = payoff_row(finish(h), a)
        for b in range(p):
            if b == a:
                continue
            other = payoff_row(finish(h + (b,)), b)
            row = tuple(x - y for x, y in zip(chosen, other))
            if any(row):
                rows.add(row)
    rows = sorted(rows)
    q = finish(())
    assert q == tuple(exact["strategy"]["terminal_counts"])
    actual_mask = sum(1 << a for a in range(p) if q[a])
    comparison_mask = sum(1 << a for a in exact["portfolio"])
    w = [F(bool(mask & actual_mask)) for mask in range(1, 1 << p)]
    v = [F(bool(mask & comparison_mask)) for mask in range(1, 1 << p)]
    beta = F(exact["dual_bound"])
    mu = {}
    for i, value in exact["dual_support"]:
        assert type(i) is int and i in range(len(rows)) and i not in mu
        mu[i] = F(value)
        assert mu[i] >= 0
    residual = [beta * w[j] - sum(value * rows[i][j] for i, value in mu.items()) - v[j]
                for j in range((1 << p) - 1)]
    assert min(residual) >= 0
    # Point evaluation is only a lower witness to this one fixed J objective.
    # It does not rerun the already saved SPE check or optimize another J.
    clones = exact["integer_clones"]
    W = sum(x * y for x, y in zip(w, clones))
    V = sum(x * y for x, y in zip(v, clones))
    assert V / W == beta == F(exact["objective_value"])
    selected = []
    for item in report["milp"]["selected"]:
        b = item["branch"]
        digest = hashlib.sha256(repr(sorted((h, a) for h, a in actions.items()
                                            if h and h[0] == b)).encode()).hexdigest()
        assert digest == item["digest"]
        assert finish((b,)) == tuple(item["target"])
        selected.append({"branch": b, "digest_matches_exact_strategy": True,
                         "target_matches_exact_strategy": True})
    result = {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "purpose": "one saved fixed-J dual and selected-subtree identity, not a new SPE or LP run",
        "strategy_decision_nodes_read_for_row_reconstruction": len(actions),
        "distinct_nonzero_IC_rows": len(rows),
        "dual_nonzero_multipliers": len(mu),
        "customer_type_residuals": len(residual),
        "minimum_dual_residual": str(min(residual)),
        "beta": str(beta), "portfolio": exact["portfolio"],
        "normalized_point_objective": str(V / W),
        "selected_subtrees": selected,
        "residuals_by_mask_1_to_127": list(map(str, residual)),
        "not_checked": ["new SPE replay", "all-portfolio exact upper bound", "MILP neighbourhood optimality", "author main", "LP", "BI"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
