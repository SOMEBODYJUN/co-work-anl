#!/usr/bin/env python3
"""Definition-level rational audit of four saved discovery points.

No search module, numerical solver, or equilibrium enumerator is imported.
The small rational instances below are recoveries, not the literal decimals.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
RECOVERY = {
    "security_best_4_3.json": {
        "weights": {1: "7/20", 3: "1/4", 5: "1/20", 6: "1/20", 7: "3/10"},
        "p": ["1", "0", "0", "0"], "dual": [0, 0], "v": "19/60", "unit_scale": 20,
    },
    "security_best_5_4.json": {
        "weights": {1: "1/7", 2: "1/7", 12: "4/7", 16: "1/7"},
        "p": ["2/9", "2/9", "1/3", "0", "2/9"], "dual": [2, 2, 2], "v": "1/7", "unit_scale": 7,
    },
    "security_best_6_3.json": {
        "weights": {1: "1/7", 4: "1/7", 8: "1/7", 16: "1/7", 34: "3/7"},
        "p": ["0", "1/4", "1/4", "1/4", "1/4", "0"], "dual": [1, 1], "v": "1/7", "unit_scale": 7,
    },
    "security_best_7_5.json": {
        "weights": {1: "1/7", 32: "1/7", 94: "5/7"},
        "p": ["1/4", "1/2", "0", "0", "0", "1/4", "0"], "dual": [1, 1, 1, 1], "v": "1/7", "unit_scale": 7,
    },
}


def no_duplicate_keys(pairs):
    d = {}
    for key, value in pairs:
        assert key not in d, ("duplicate JSON key", key)
        d[key] = value
    return d


def load_exact(path):
    return json.loads(path.read_text(), parse_float=F, object_pairs_hook=no_duplicate_keys)


def strategy_audit(d, weights, include_rows):
    k, m = d["k"], d["m"]
    sigma = {tuple(map(int, h.split(","))) if h else (): a for h, a in d["sigma"].items()}
    histories = [h for depth in range(m) for h in product(range(k), repeat=depth)]
    assert set(sigma) == set(histories)
    assert all(type(a) is int and 0 <= a < k for a in sigma.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (sigma[h],))

    def utility(z, i):
        return sum((r / sum((mask >> a) & 1 for a in z)
                    for mask, r in weights.items() if (mask >> z[i]) & 1), F(0))

    def welfare(z):
        return sum((r for mask, r in weights.items() if any((mask >> a) & 1 for a in z)), F(0))

    min_slack = None
    first_negative = None
    rows = []
    layer_min = {}
    for h in histories:
        z = terminal(h)
        candidate_z = [terminal(h + (a,)) for a in range(k)]
        values = [utility(zz, len(h)) for zz in candidate_z]
        selected = values[sigma[h]]
        slacks = [selected - x for x in values]
        margin = min(slacks)
        min_slack = margin if min_slack is None else min(min_slack, margin)
        layer_min[len(h)] = min(layer_min.get(len(h), margin), margin)
        if margin < 0 and first_negative is None:
            first_negative = {"history": h, "chosen": sigma[h], "values": list(map(str, values)), "slack": str(margin)}
        if include_rows:
            rows.append({"h": h, "a": sigma[h], "terminal": z,
                         "values": list(map(str, values)), "slacks": list(map(str, slacks))})
    actual = terminal(())
    assert sorted(actual) == d["target"], (actual, d["target"])
    target_w = welfare(tuple(d["target"]))
    assert welfare(actual) == target_w
    opt = max(welfare(z) for z in combinations_with_replacement(range(k), m))
    out = {"histories": len(histories), "action_comparisons_including_self": k * len(histories),
           "actual_path": actual, "target_count_representative": d["target"],
           "payoffs": list(map(str, [utility(actual, i) for i in range(m)])),
           "welfare": str(target_w), "optimum_m_coverage": str(opt),
           "half_margin_2W_minus_OPT": str(2 * target_w - opt),
           "min_slack": str(min_slack), "layer_min_slack": {str(x): str(y) for x, y in layer_min.items()},
           "first_negative": first_negative}
    if include_rows:
        out["rows"] = rows
    return out


def security_audit(d, weights, p, dual, v):
    k, m = d["k"], d["m"]
    assert len(p) == k and all(x >= 0 for x in p) and sum(p) == 1
    assert len(dual) == m - 1 and all(0 <= x < k for x in dual)

    def f(a, b):
        return sum((r / (1 + sum((mask >> x) & 1 for x in b))
                    for mask, r in weights.items() if (mask >> a) & 1), F(0))

    rows = [{"background": b, "pure_query_values": [str(f(a, b)) for a in range(k)],
             "p_query_value": str(sum((p[a] * f(a, b) for a in range(k)), F(0)))}
            for b in combinations_with_replacement(range(k), m - 1)]
    lower = min(F(row["p_query_value"]) for row in rows)
    upper_vector = [f(a, tuple(dual)) for a in range(k)]
    upper = max(upper_vector)
    assert lower == upper == v, (lower, upper, v)
    return {"p": list(map(str, p)), "background_count": len(rows), "rows": rows,
            "dual_background": dual, "dual_probability": "1", "dual_pure_query_values": list(map(str, upper_vector)),
            "primal_lower_bound": str(lower), "dual_upper_bound": str(upper), "exact_value": str(v)}


def main():
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    for record in manifest:
        path = BASE / "original" / Path(record["path"]).name
        assert len(path.read_bytes()) == record["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
    report = {"method": "standard-library Fraction, all ordered histories and all static background multisets", "cases": {}}
    summary = {}
    for name, rec in RECOVERY.items():
        d = load_exact(BASE / "original" / name)
        k, m = d["k"], d["m"]
        assert set(d) == {"k", "m", "gap", "masks", "r", "target", "query_p", "sigma"}
        assert d["masks"] == list(range(1, 1 << k)) and len(d["r"]) == (1 << k) - 1
        weights = {mask: F(x) for mask, x in rec["weights"].items()}
        assert all(x > 0 for x in weights.values()) and sum(weights.values()) == 1
        p = list(map(F, rec["p"]))
        delta_r = max(abs(F(x) - weights.get(mask, F(0))) for mask, x in zip(d["masks"], d["r"]))
        delta_p = max(abs(F(x) - y) for x, y in zip(d["query_p"], p))
        assert delta_r <= F(1, 10**12) and delta_p <= F(1, 10**12)
        units = {mask: int(x * rec["unit_scale"]) for mask, x in weights.items()}
        assert all(F(units[mask], rec["unit_scale"]) == x for mask, x in weights.items())
        spe = strategy_audit(d, weights, True)
        assert F(spe["min_slack"]) >= 0
        security = security_audit(d, weights, p, rec["dual"], F(rec["v"]))
        gap = m * F(security["exact_value"]) - F(spe["welfare"])
        assert gap == 0
        literal_weights = {mask: F(x) for mask, x in zip(d["masks"], d["r"]) if x}
        literal = strategy_audit(d, literal_weights, False)
        case = {"k": k, "m": m, "original_gap": str(d["gap"]),
                "recovered_weights": {str(a): str(r) for a, r in weights.items()},
                "unit_client_multiplicities": units, "unit_scale": rec["unit_scale"],
                "max_recovery_error_r": str(delta_r), "max_recovery_error_p": str(delta_p),
                "literal_decimal_weight_sum": str(sum(literal_weights.values())),
                "literal_decimal_p_sum": str(sum(map(F, d["query_p"]))),
                "literal_decimal_strategy_audit": literal, "recovered_SPE": spe,
                "recovered_static_security": security, "recovered_gap_m_v_minus_W": str(gap)}
        report["cases"][name] = case
        summary[name] = {"k": k, "m": m, "unit_clients": sum(units.values()),
                         **{key: value for key, value in spe.items() if key != "rows"},
                         "v": security["exact_value"], "gap": str(gap),
                         "literal_decimal_min_slack": literal["min_slack"],
                         "literal_decimal_first_negative": literal["first_negative"]}
    out = BASE / "rerun"
    out.mkdir(exist_ok=True)
    (out / "exact-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
