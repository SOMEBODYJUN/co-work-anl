"""Exact replay of the frozen discovery certificate, without its LP/model code.

Only Python's standard library is needed. Rational customer masses are first
checked as linear combinations of unit-customer utilities, then cleared to
nonnegative integer multiplicities. No optimization or policy search is run.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, lcm
from functools import reduce
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/alternating_cone_result.json"
SOURCE_SHA = "b8df00d5d913d719e3641b42f283ff32ac7609222f4ba9963c0f018cebf0e048"


def audit(raw):
    weights = {int(mask): F(value) for mask, value in raw["weights"].items()}
    k, m = len(raw["lambda"]), len(raw["path"])
    lam = tuple(map(F, raw["lambda"]))
    action_rows = [(tuple(h), a) for h, a in raw["actions"]]
    actions = dict(action_rows)
    histories = [h for t in range(m) for h in product(range(k), repeat=t)]
    assert len(action_rows) == len(actions) == len(histories)
    assert set(actions) == set(histories)
    assert all(0 <= a < k for a in actions.values())
    assert min(weights.values()) >= 0 and min(lam) >= 0

    def terminal(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    def utilities(z):
        result = [F(0)] * m
        for mask, mass in weights.items():
            covering = [i for i, a in enumerate(z) if mask & (1 << a)]
            for i in covering:
                result[i] += mass / len(covering)
        return result

    def welfare(z):
        return sum((mass for mask, mass in weights.items()
                    if any(mask & (1 << a) for a in z)), F(0))

    path = terminal(())
    assert list(path) == raw["path"]
    spe_rows = []
    for h in histories:
        t = len(h)
        chosen_value = utilities(terminal(h))[t]
        values = [utilities(terminal(h + (a,)))[t] for a in range(k)]
        assert chosen_value == values[actions[h]]
        assert chosen_value >= max(values)
        spe_rows.append({"history": list(h), "chosen": actions[h],
                         "utilities": list(map(str, values))})
    slacks = [F(row["utilities"][row["chosen"]]) - F(v)
              for row in spe_rows for v in row["utilities"]]
    assert str(min(slacks)) == raw["min_SPE_slack"]
    assert welfare(path) == F(raw["W"])
    columns = {}
    minimizing_ordered = []
    gamma = None
    for z in product(range(k), repeat=m):
        w = welfare(z)
        assert sum(utilities(z)) == w
        gains = []
        for a in range(k):
            dev_sum = sum((utilities(z[:i] + (a,) + z[i + 1:])[i]
                           for i in range(m)), F(0))
            gains.append(w - dev_sum)
        direct = w - sum((a * b for a, b in zip(lam, gains)), F(0))
        # Independent per-customer inverse-load expansion of the same column.
        expanded = F(0)
        for mask, mass in weights.items():
            d = sum(bool(mask & (1 << a)) for a in z)
            lambda_b = sum((lam[a] for a in range(k) if mask & (1 << a)), F(0))
            inverse_load = F(m) if d == 0 else F(m + 1, d + 1)
            expanded += mass * ((1 - sum(lam)) * (d > 0) + lambda_b * inverse_load)
        assert direct == expanded
        q = tuple(z.count(a) for a in range(k))
        if q in columns:
            assert columns[q] == direct
        columns[q] = direct
        if gamma is None or direct < gamma:
            gamma, minimizing_ordered = direct, [list(z)]
        elif direct == gamma:
            minimizing_ordered.append(list(z))
    assert gamma == F(raw["CCE_lower"])
    assert gamma - welfare(path) == F(raw["gap"])
    assert raw["valid_strict_failure"] == (gamma > welfare(path))
    scale = lcm(*(v.denominator for v in weights.values()))
    integers = {mask: int(scale * v) for mask, v in weights.items()}
    assert all(F(integers[b], scale) == weights[b] for b in weights)
    optimum = max(welfare(z) for z in product(range(k), repeat=m))
    same_coverage = [[a, b] for a in range(k) for b in range(a + 1, k)
                     if all(bool(mask & (1 << a)) == bool(mask & (1 << b))
                            for mask in weights)]
    return {"players": m, "topics": k, "all_history_count": len(histories),
            "all_spe_comparisons_including_chosen": len(slacks),
            "minimum_spe_slack": str(min(slacks)), "path": list(path),
            "path_payoffs": list(map(str, utilities(path))),
            "W": str(welfare(path)), "OPT": str(optimum),
            "twice_welfare_minus_opt": str(2 * welfare(path) - optimum),
            "total_normalized_customer_mass": str(sum(weights.values())),
            "denominator_scale": scale, "integer_customer_counts": integers,
            "integer_customer_gcd": reduce(gcd, integers.values()),
            "unit_customer_total": sum(integers.values()),
            "scaled_W": str(scale * welfare(path)), "scaled_OPT": str(scale * optimum),
            "static_ordered_profiles": k ** m, "static_count_profiles": len(columns),
            "lambda_sum": str(sum(lam)), "certified_cce_lower": str(gamma),
            "certified_gap": str(gamma - welfare(path)),
            "scaled_cce_lower": str(scale * gamma),
            "scaled_gap": str(scale * (gamma - welfare(path))),
            "minimizing_ordered_profiles": minimizing_ordered,
            "count_columns": [[list(q), str(v)] for q, v in sorted(columns.items())],
            "identical_coverage_label_pairs": same_coverage,
            "spe_table": spe_rows}


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    source = json.loads(SOURCE.read_text())
    out = {"source_sha256": SOURCE_SHA, "discovery_code_executed": False,
           "independent_external_review": False, "cases": {}}
    for name, run in source.items():
        out["cases"][name] = {"source_status": run["status"], "rounds": []}
        for row in run["trace"]:
            result = audit(row["rational"])
            result["round"] = row["round"]
            out["cases"][name]["rounds"].append(result)
    # The later thirteen-customer certificate uses exactly this complete policy,
    # although its customer vector and CCE multipliers are different.
    later_path = HERE / "original/later_thirteen_certificate.json"
    later = json.loads(later_path.read_text())
    initial = source["strong_iid_policy"]["trace"][0]["rational"]
    later_actions = {tuple(row["history"]): row["action"] for row in later["actions"]}
    initial_actions = {tuple(h): a for h, a in initial["actions"]}
    assert later_actions == initial_actions
    out["same_complete_policy_as_later_thirteen_customer_certificate"] = True
    out["later_certificate_sha256"] = hashlib.sha256(later_path.read_bytes()).hexdigest()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
