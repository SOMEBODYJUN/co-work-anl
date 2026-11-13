"""Independently replay every mathematical entry of the saved exact report.

The two million byte JSON is parsed completely, never printed as a substitute
for reading. All ordered strategy rows and all static backgrounds are checked
against the frozen original strategy and explicitly recovered rational inputs.
No search, LP solver, or existing audit implementation is imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "archives/customer-attraction/tools/evidence/aggregate-static-security-cone-four-snapshots-primary"
OUT = Path(__file__).with_name("audit-report-summary.json")


def unique(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, key
        result[key] = value
    return result


def load(path, exact=False):
    return json.loads(path.read_text(), object_pairs_hook=unique,
                      **({"parse_float": F} if exact else {}))


def audit_strategy(k, m, sigma, weights, target, include_rows):
    histories = [h for depth in range(m) for h in product(range(k), repeat=depth)]
    assert set(sigma) == set(histories)
    assert all(type(a) is int and 0 <= a < k for a in sigma.values())

    @lru_cache(None)
    def leaf(h):
        if len(h) == m:
            return h
        return leaf((*h, sigma[h]))

    def u(z, i):
        return sum((mass / sum(bool(mask & (1 << a)) for a in z)
                    for mask, mass in weights.items() if mask & (1 << z[i])), F(0))

    def welfare(z):
        union = 0
        for a in z:
            union |= 1 << a
        return sum((mass for mask, mass in weights.items() if mask & union), F(0))

    rows, minima, first = [], {}, None
    for h in histories:
        values = [u(leaf((*h, a)), len(h)) for a in range(k)]
        slacks = [values[sigma[h]] - value for value in values]
        margin = min(slacks)
        minima[len(h)] = min(minima.get(len(h), margin), margin)
        if margin < 0 and first is None:
            first = {"history": list(h), "chosen": sigma[h],
                     "values": list(map(str, values)), "slack": str(margin)}
        rows.append({"h": list(h), "a": sigma[h], "terminal": list(leaf(h)),
                     "values": list(map(str, values)), "slacks": list(map(str, slacks))})
    actual = leaf(())
    assert sorted(actual) == target
    w = welfare(actual)
    opt = max(welfare(z) for z in combinations_with_replacement(range(k), m))
    result = {"histories": len(histories), "action_comparisons_including_self": k * len(histories),
              "actual_path": list(actual), "target_count_representative": target,
              "payoffs": [str(u(actual, i)) for i in range(m)], "welfare": str(w),
              "optimum_m_coverage": str(opt), "half_margin_2W_minus_OPT": str(2*w-opt),
              "min_slack": str(min(minima.values())),
              "layer_min_slack": {str(d): str(x) for d, x in minima.items()}, "first_negative": first}
    assert sum(map(F, result["payoffs"])) == w
    if include_rows:
        result["rows"] = rows
    return result


def main():
    report_path = BASE / "rerun/exact-report.json"
    report = load(report_path)
    assert set(report) == {"method", "cases"}
    assert report["method"] == "standard-library Fraction, all ordered histories and all static background multisets"
    assert set(report["cases"]) == {f"security_best_{x}.json" for x in ["4_3", "5_4", "6_3", "7_5"]}
    summary = {"report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
               "report_bytes": report_path.stat().st_size,
               "review_method": "Complete JSON parse; every case field, ordered IC row, static payoff row and summary recomputed with Fraction from original sigma and declared recovery.",
               "cases": {}}
    case_keys = {"k", "m", "original_gap", "recovered_weights", "unit_client_multiplicities", "unit_scale",
                 "max_recovery_error_r", "max_recovery_error_p", "literal_decimal_weight_sum", "literal_decimal_p_sum",
                 "literal_decimal_strategy_audit", "recovered_SPE", "recovered_static_security", "recovered_gap_m_v_minus_W"}
    for name, case in report["cases"].items():
        assert set(case) == case_keys
        original_path = BASE / "original" / name
        original = load(original_path, exact=True)
        assert set(original) == {"k", "m", "gap", "masks", "r", "target", "query_p", "sigma"}
        k, m = case["k"], case["m"]
        assert (k, m) == (original["k"], original["m"])
        assert original["masks"] == list(range(1, 1 << k))
        assert len(original["r"]) == (1 << k)-1 and len(original["query_p"]) == k
        sigma = {tuple(map(int, h.split(","))) if h else (): a for h, a in original["sigma"].items()}
        assert len(sigma) == len(original["sigma"])
        recovered = {int(mask): F(value) for mask, value in case["recovered_weights"].items()}
        assert all(0 < mask < 1 << k and value > 0 for mask, value in recovered.items())
        assert sum(recovered.values()) == 1
        assert {str(mask): int(value * case["unit_scale"]) for mask, value in recovered.items()} == case["unit_client_multiplicities"]
        assert all(F(case["unit_client_multiplicities"][str(mask)], case["unit_scale"]) == value for mask, value in recovered.items())
        p = list(map(F, case["recovered_static_security"]["p"]))
        assert len(p) == k and min(p) >= 0 and sum(p) == 1
        assert str(original["gap"]) == case["original_gap"]
        assert F(case["max_recovery_error_r"]) == max(abs(value-recovered.get(mask, 0)) for mask, value in zip(original["masks"], original["r"]))
        assert F(case["max_recovery_error_p"]) == max(abs(a-b) for a, b in zip(original["query_p"], p))
        assert F(case["max_recovery_error_r"]) <= F(1,10**12) and F(case["max_recovery_error_p"]) <= F(1,10**12)
        literal = {mask: value for mask, value in zip(original["masks"], original["r"]) if value}
        assert F(case["literal_decimal_weight_sum"]) == sum(literal.values())
        assert F(case["literal_decimal_p_sum"]) == sum(original["query_p"])
        spe = audit_strategy(k, m, sigma, recovered, original["target"], True)
        assert spe == case["recovered_SPE"], name
        assert F(spe["min_slack"]) == 0
        assert audit_strategy(k, m, sigma, literal, original["target"], False) == case["literal_decimal_strategy_audit"]

        def f(a,b):
            return sum((value / (1+sum(bool(mask & (1 << x)) for x in b))
                        for mask,value in recovered.items() if mask & (1 << a)), F(0))

        rows = []
        for b in combinations_with_replacement(range(k), m-1):
            pure = [f(a,b) for a in range(k)]
            rows.append({"background": list(b), "pure_query_values": list(map(str,pure)),
                         "p_query_value": str(sum((p[a]*pure[a] for a in range(k)),F(0)))})
        security = case["recovered_static_security"]
        dual = security["dual_background"]
        assert len(dual) == m-1 and all(type(a) is int and 0 <= a < k for a in dual)
        upper_vector = [f(a,dual) for a in range(k)]
        lower = min(F(row["p_query_value"]) for row in rows)
        upper = max(upper_vector)
        assert lower == upper
        assert security == {"p": list(map(str,p)), "background_count": len(rows), "rows": rows,
                            "dual_background": dual, "dual_probability": "1", "dual_pure_query_values": list(map(str,upper_vector)),
                            "primal_lower_bound": str(lower), "dual_upper_bound": str(upper), "exact_value": str(lower)}
        assert F(case["recovered_gap_m_v_minus_W"]) == m*lower-F(spe["welfare"]) == 0
        summary["cases"][name] = {"original_sha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
                                   "histories": spe["histories"], "comparisons": spe["action_comparisons_including_self"],
                                   "backgrounds": len(rows), "welfare": spe["welfare"], "security_value": str(lower),
                                   "actual_path": spe["actual_path"], "literal_min_slack": case["literal_decimal_strategy_audit"]["min_slack"],
                                   "recovery_min_slack": spe["min_slack"], "status": "all-report-fields-exactly-matched"}
    summary["totals"] = {key: sum(case[key] for case in summary["cases"].values())
                          for key in ["histories", "comparisons", "backgrounds"]}
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
