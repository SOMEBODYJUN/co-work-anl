"""Read and exactly check the four frozen early-A inputs; no LP or imports.

This is a new informed definition-level replay, not a historical generator run.
The only shared implementation convention is sorting distinct rational IC rows,
which binds the saved sparse dual indices. Every ordered node is retained first.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "original"
P, M = 7, 5
EXPECTED = {
    "earlyA_efficiency.py": "70c648671a4c5367172ab709e8b4a7633a9a54b2c938fbdbb5086acf9a74adb9",
    "earlyA_m5p7_efficiency.json": "503257e98d708099375660285536717612414be61e221178570c1a83ea64b534",
    "earlyA_m5p7_scalar.json": "0dde8498f4e4a22131ec83b0ba350505386321b192373cc0ee90021e1164ba58",
    "earlyA_scalar.py": "d2ab3107758923059fe09975f4255e6779d8c6d0f2657339c7284c5b19fea121",
}
MASKS = tuple(range(1, 1 << P))
HISTORIES = tuple(h for d in range(M) for h in product(range(P), repeat=d))
PORTFOLIOS = tuple(combinations(range(P), M))


def load(name):
    data = (ORIGINAL / name).read_bytes()
    assert sha256(data).hexdigest() == EXPECTED[name], name
    return json.loads(data) if name.endswith(".json") else None


def strategy(data):
    assert set(data) == {"terminal_counts", "actions"}
    entries = data["actions"]
    assert all(set(x) == {"history", "action"} for x in entries)
    assert all(type(a) is int and a in range(P) for x in entries for a in x["history"])
    assert all(type(x["action"]) is int and x["action"] in range(P) for x in entries)
    actions = {tuple(x["history"]): x["action"] for x in entries}
    assert len(actions) == len(entries) == len(HISTORIES)
    assert set(actions) == set(HISTORIES)
    for h, a in actions.items():
        expected = 0 if len(h) < M - 1 or h.count(0) < M - 2 else 5 if 6 in h else 6
        assert a == expected, (h, a, expected)

    @lru_cache(None)
    def terminal(h):
        z = h
        while len(z) < M:
            z += (actions[z],)
        return tuple(z.count(a) for a in range(P))

    root = terminal(())
    assert list(root) == data["terminal_counts"] == [4, 0, 0, 0, 0, 0, 1]
    return actions, terminal, root


@lru_cache(None)
def row(q, a):
    return tuple(F(1, sum(q[b] for b in range(P) if mask & (1 << b)))
                 if mask & (1 << a) else F(0) for mask in MASKS)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b) if x and y), F(0))


def coverage(clones, support):
    mask = sum(1 << a for a in support)
    return sum(n for b, n in zip(MASKS, clones) if b & mask)


def check_point(clones, actions, terminal, root):
    assert len(clones) == len(MASKS)
    assert all(type(n) is int and n >= 0 for n in clones)
    assert any(clones)
    utility = {}

    def u(q, a):
        key = q, a
        if key not in utility:
            utility[key] = dot(row(q, a), clones)
        return utility[key]

    slacks = Counter()
    minimum = None
    for h in HISTORIES:
        a = actions[h]
        actual = u(terminal(h), a)
        for b in range(P):
            slack = actual - u(terminal(h + (b,)), b)
            assert slack >= 0, (h, b, slack)
            slacks["zero" if slack == 0 else "positive"] += 1
            minimum = slack if minimum is None else min(minimum, slack)
    welfare = coverage(clones, [a for a, c in enumerate(root) if c])
    optimum = max(coverage(clones, J) for J in PORTFOLIOS)
    path = ()
    while len(path) < M:
        path += (actions[path],)
    payoffs = [u(root, a) for a in path]
    assert sum(payoffs) == welfare
    label_coverages = [tuple(i for i, (mask, n) in enumerate(zip(MASKS, clones))
                             if n and mask & (1 << a)) for a in range(P)]
    return {"unit_clients": sum(clones), "nonzero_types": [[b, n] for b, n in zip(MASKS, clones) if n],
            "root_path": list(path), "payoffs": list(map(str, payoffs)), "W": welfare,
            "OPT5": optimum, "ratio_OPT_over_W": str(F(optimum, welfare)),
            "distinct_label_coverages": len(set(label_coverages)),
            "including_self_comparisons": sum(slacks.values()),
            "zero_slacks": slacks["zero"], "positive_slacks": slacks["positive"],
            "minimum_slack": str(minimum)}


def main():
    for name in EXPECTED:
        load(name)
    eff = load("earlyA_m5p7_efficiency.json")
    scalar = load("earlyA_m5p7_scalar.json")
    assert set(eff) == {"scope", "universal_bound_proved", "batches"}
    assert eff["scope"] == "one early-A complete strategy cone, all comparison portfolios; not all SPE cones"
    assert eff["universal_bound_proved"] is False
    assert len(eff["batches"]) == 1
    batch = eff["batches"][0]
    assert set(batch) == {"players", "topics", "cone_proofs"}
    assert batch["players"] == M and batch["topics"] == P
    assert len(batch["cone_proofs"]) == 1
    record = batch["cone_proofs"][0]
    assert set(record) == {"strategy", "root_counts", "portfolio_proofs"}
    actions, terminal, root = strategy(record["strategy"])
    assert record["root_counts"] == list(root)
    assert scalar["strategy"] == record["strategy"]
    rows = set()
    for h in HISTORIES:
        actual = row(terminal(h), actions[h])
        for b in range(P):
            if b != actions[h]:
                r = tuple(x - y for x, y in zip(actual, row(terminal(h + (b,)), b)))
                if any(r):
                    rows.add(r)
    rows = tuple(sorted(rows))
    assert len(rows) == 1302 == scalar["rows"]
    welfare_row = tuple(F(bool(mask & ((1 << 0) | (1 << 6)))) for mask in MASKS)
    proofs = record["portfolio_proofs"]
    assert [tuple(x["portfolio"]) for x in proofs] == list(PORTFOLIOS)
    verified = []
    for proof in proofs:
        assert set(proof) == {"portfolio", "integer_clones", "objective_value", "ratio", "optimum",
                              "welfare", "dual_bound", "dual_support"}
        point = check_point(proof["integer_clones"], actions, terminal, root)
        assert point["W"] == proof["welfare"] and point["OPT5"] == proof["optimum"]
        assert point["ratio_OPT_over_W"] == proof["ratio"]
        J = tuple(proof["portfolio"])
        value = F(coverage(proof["integer_clones"], J), point["W"])
        beta = F(proof["dual_bound"])
        assert value == F(proof["objective_value"]) == beta
        multipliers = {}
        for i, mu in proof["dual_support"]:
            assert type(i) is int and i in range(len(rows)) and i not in multipliers
            multipliers[i] = F(mu)
            assert multipliers[i] > 0
        target = tuple(F(bool(mask & sum(1 << a for a in J))) for mask in MASKS)
        residual = [beta * w - v - sum(mu * rows[i][j] for i, mu in multipliers.items())
                    for j, (w, v) in enumerate(zip(welfare_row, target))]
        assert min(residual) >= 0
        verified.append({"portfolio": list(J), "objective_value": str(value), "dual_bound": str(beta),
                         "dual_terms": len(multipliers), "dual_minimum_coordinate_residual": str(min(residual)),
                         "target_is_optimal_for_this_integer_point": value == F(point["ratio_OPT_over_W"]),
                         **point})
    assert set(scalar) == {"m", "p", "threshold", "rows", "root", "floating_max_scalar", "status", "scope",
                           "scalar_exact", "integer_clones", "strategy", "W", "OPT", "normalization"}
    assert (scalar["m"], scalar["p"], scalar["threshold"]) == (M, P, 3)
    assert scalar["root"] == list(root) and scalar["normalization"] == "W=1"
    assert scalar["scope"] == "fixed complete policy cone only"
    assert scalar["status"] == "Optimization terminated successfully. (HiGHS Status 7: Optimal)"
    assert abs(scalar["floating_max_scalar"] - 0.2) < 1e-12
    point = check_point(scalar["integer_clones"], actions, terminal, root)
    assert point["W"] == scalar["W"] == 12 and point["OPT5"] == scalar["OPT"] == 12
    last = 6
    D = sum(F(n, sum(root[a] for a in range(P) if mask & (1 << a)) + 1)
            for mask, n in zip(MASKS, scalar["integer_clones"])
            if not mask & (1 << last) and mask & (1 << 0))
    u_last = F(point["payoffs"][-1])
    gap = (M - 1) * u_last - point["W"] - D
    assert D == F(8, 5) and gap == F(12, 5)
    assert gap / point["W"] == F(scalar["scalar_exact"]) == F(1, 5)
    point.update({"D": str(D), "integer_bridge_gap": str(gap),
                  "W_normalized_bridge_gap": str(gap / point["W"]),
                  "scalar_optimal_dual_saved": False,
                  "exact_scalar_optimum_certified_by_this_replay": False})
    result = {"scope": "one fixed five-player seven-label complete policy; not universal half",
              "original_generator_runs_this_batch": 0, "new_standard_library_fixed_input_replays": 1,
              "source_sha256": EXPECTED, "ordered_decision_histories_per_strategy": len(HISTORIES),
              "comparisons_per_point_including_self": P * len(HISTORIES),
              "nonself_comparisons_per_point": (P - 1) * len(HISTORIES), "distinct_sorted_IC_rows": len(rows),
              "same_full_strategy_in_both_reports": True,
              "exact_efficiency_primals_and_optimal_duals": verified,
              "fixed_cone_maximum_OPT5_over_W": str(max(F(x["dual_bound"]) for x in verified)),
              "fixed_cone_minimum_W_over_OPT5": str(1 / max(F(x["dual_bound"]) for x in verified)),
              "scalar_witness": point,
              "all_point_comparisons_including_self": P * len(HISTORIES) * (len(verified) + 1),
              "new_LP_or_random_search_runs": 0, "six_player_half_verified": False}
    (HERE / "fixed-input-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                     {"source_sha256", "exact_efficiency_primals_and_optimal_duals", "scalar_witness"}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
