"""Exact comparison of the two frozen five-player cycle strategy cones.

This is a small stdlib-only certificate check, not an LP/MILP search or a
re-execution of the historical credible-menu enumeration.  The two original
customer vectors certify noncontainment in the fixed original label
coordinates.  The optimized vectors happen to belong to both cones.
"""

from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parents[4]
INPUT = (
    "archives/customer-attraction/tools/evidence/strategy-cones/original/"
    "evidence/runs/2026-10-09/cone_attack_credible_selected.json"
)
INPUT_SHA = "a47e0b1ab2ce611c5e4499c6fa0f28fbb52e02aae058da7c5a4dd3daa1cd8a25"
P = M = 5
F = Fraction


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), F(0))


def payoff(counts, action):
    return tuple(
        F(1, sum(counts[a] for a in range(P) if mask & (1 << a)))
        if mask & (1 << action) else F(0)
        for mask in range(1, 1 << P)
    )


def build(record):
    action_records = record["strategy"]["actions"]
    actions = {tuple(row["history"]): row["action"] for row in action_records}
    histories = {h for depth in range(M) for h in product(range(P), repeat=depth)}
    assert len(actions) == len(action_records) == 781
    assert set(actions) == histories
    assert all(type(a) is int and 0 <= a < P for a in actions.values())
    terminals = {
        h: tuple(h.count(a) for a in range(P))
        for h in product(range(P), repeat=M)
    }
    for depth in range(M - 1, -1, -1):
        for h in product(range(P), repeat=depth):
            terminals[h] = terminals[h + (actions[h],)]
    assert terminals[()] == tuple(record["root_counts"])
    assert terminals[()] == tuple(record["strategy"]["terminal_counts"])
    origins = {}
    for h in sorted(histories, key=lambda x: (len(x), x)):
        a = actions[h]
        for b in range(P):
            if a == b:
                continue
            row = tuple(
                x - y for x, y in zip(
                    payoff(terminals[h], a), payoff(terminals[h + (b,)], b)
                )
            )
            if any(row):
                origins.setdefault(row, []).append((h, a, b))
    rows = tuple(sorted(origins))
    assert len(rows) == record["constraint_rows"]
    support_mask = sum(1 << a for a, count in enumerate(terminals[()]) if count)
    welfare = tuple(F(bool(mask & support_mask)) for mask in range(1, 1 << P))
    actual_path = ()
    for _ in range(M):
        actual_path += (actions[actual_path],)
    for hash_key, field in (
        ("strategy_sha256", "strategy"),
        ("source_integer_clones_sha256", "source_integer_clones"),
        ("portfolio_proofs_sha256", "portfolio_proofs"),
    ):
        encoded = json.dumps(record[field], sort_keys=True, separators=(",", ":")).encode()
        assert hashlib.sha256(encoded).hexdigest() == record[hash_key]
    return actions, terminals, rows, welfare, origins, actual_path


def comparison(record, model, masses):
    actions, terminals, rows, welfare, _, _ = model
    assert len(masses) == 31 and all(type(x) is int and x >= 0 for x in masses)
    def finish(prefix):
        path = prefix
        while len(path) < M:
            path += (actions[path],)
        assert tuple(path.count(a) for a in range(P)) == terminals[prefix]
        return path
    violations = []
    for h in sorted(actions, key=lambda x: (len(x), x)):
        a = actions[h]
        actual = dot(payoff(terminals[h], a), masses)
        for b in range(P):
            if a == b:
                continue
            deviation = dot(payoff(terminals[h + (b,)], b), masses)
            if actual < deviation:
                violations.append({
                    "history": h,
                    "action": a,
                    "alternative": b,
                    "actual_terminal_path": finish(h),
                    "deviation_terminal_path": finish(h + (b,)),
                    "actual_terminal": terminals[h],
                    "deviation_terminal": terminals[h + (b,)],
                    "actual_payoff": str(actual),
                    "deviation_payoff": str(deviation),
                    "ic_slack": str(actual - deviation),
                })
    W = dot(welfare, masses)
    return {
        "target_family": record["source_family"],
        "checked_ordered_history_comparisons": 781 * 4,
        "violated_comparisons": len(violations),
        "violated_distinct_nonzero_rows": sum(dot(row, masses) < 0 for row in rows),
        "first_violations": violations[:3],
        "W": str(W),
        "OPT5": sum(masses),
        "ratio": str(F(sum(masses), W)),
    }


def main():
    raw = (ROOT / INPUT).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == INPUT_SHA
    report = json.loads(raw)
    assert len(report["batches"]) == 1
    batch = report["batches"][0]
    assert batch["topics"] == P and batch["players"] == M
    records = batch["cone_proofs"]
    assert [x["source_family"] for x in records] == [
        "reply_cycle_lift", "asymmetric_overlap_cycle"
    ]
    models = [build(record) for record in records]
    certificates = []
    for record, model in zip(records, models):
        _, _, rows, welfare, origins, path = model
        assert len(record["portfolio_proofs"]) == 1
        proof = record["portfolio_proofs"][0]
        assert proof["portfolio"] == list(range(P))
        primal = proof["integer_clones"]
        assert all(dot(row, primal) >= 0 for row in rows)
        W = dot(welfare, primal)
        assert W == proof["welfare"] and sum(primal) == proof["optimum"]
        beta = F(proof["dual_bound"])
        assert F(sum(primal), W) == beta == F(proof["objective_value"]) == F(proof["ratio"])
        multipliers = {}
        for index, value in proof["dual_support"]:
            assert index in range(len(rows)) and index not in multipliers
            multipliers[index] = F(value)
        assert all(value >= 0 for value in multipliers.values())
        residual = tuple(
            beta * w - sum(mu * rows[i][j] for i, mu in multipliers.items()) - 1
            for j, w in enumerate(welfare)
        )
        assert all(value >= 0 for value in residual)
        certificates.append({
            "family": record["source_family"],
            "strategy_sha256": record["strategy_sha256"],
            "source_integer_clones_sha256": record["source_integer_clones_sha256"],
            "portfolio_proofs_sha256": record["portfolio_proofs_sha256"],
            "ordered_decision_nodes": 781,
            "actual_path": path,
            "root_counts": model[1][()],
            "distinct_nonzero_ic_rows": len(rows),
            "primal_nonzero_masses": {str(i + 1): n for i, n in enumerate(primal) if n},
            "beta": str(beta),
            "dual_support": proof["dual_support"],
            "dual_row_origins": [
                {"row_index": i, "multiplier": str(mu), "one_ordered_comparison": origins[rows[i]][0]}
                for i, mu in multipliers.items()
            ],
            "dual_residual_by_mask": {str(i + 1): str(x) for i, x in enumerate(residual)},
        })
    comparisons = []
    for source_index, record in enumerate(records):
        for witness_kind, masses in (
            ("original_source", record["source_integer_clones"]),
            ("sharp_primal", record["portfolio_proofs"][0]["integer_clones"]),
        ):
            targets = [comparison(target, model, masses) for target, model in zip(records, models)]
            assert targets[source_index]["violated_comparisons"] == 0
            if witness_kind == "sharp_primal":
                assert all(x["violated_comparisons"] == 0 for x in targets)
            else:
                assert targets[1 - source_index]["violated_comparisons"] == (53, 101)[source_index]
            comparisons.append({
                "source_family": record["source_family"],
                "witness_kind": witness_kind,
                "masses_in_mask_order_1_through_31": masses,
                "nonzero_masses": {str(i + 1): n for i, n in enumerate(masses) if n},
                "targets": targets,
            })
    difference = tuple(b - a for a, b in zip(models[0][3], models[1][3]))
    assert all(x >= 0 for x in difference)
    assert [i + 1 for i, x in enumerate(difference) if x] == [4, 5, 6, 7]
    result = {
        "input": {"path": INPUT, "sha256": INPUT_SHA},
        "arithmetic": "stdlib fractions.Fraction; no numerical LP/MILP, no credible-menu enumeration",
        "certificates": certificates,
        "comparisons": comparisons,
        "action_table_disagreements": sum(models[0][0][h] != models[1][0][h] for h in models[0][0]),
        "objective_relation": "OPT5=sum(r_B); W_overlap-W_reply=r_4+r_5+r_6+r_7>=0 for every r>=0",
        "domain_conclusion": "Neither fixed original-label cone contains the other; each original source is an exact witness. Both sharp primals lie in the intersection.",
        "limits": "No customer-coordinate transformation, label-relabeling equivalence, strategy-union upper bound, or new enumeration of credible source menus is asserted.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
