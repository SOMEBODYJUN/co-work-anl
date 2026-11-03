"""Read every saved scalar and replay every count-policy IC; no LP or search.

The two exact inputs are (a) encoded decimal masses, and (b) those masses
individually limited to denominator 10**6, matching the old scope audit.
Neither is silently identified with the discovery program's binary floats.
All count keys, not merely their number, are checked. Integer payoff scaling
avoids floating tolerance and does not import the discovery implementation.
"""
import gzip
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parent
FILES = ["count_m5k6.json", "count_m7k7.json", "strong_count_m5k6.json", "price_m5k7.json"]


def counts(k, total):
    if k == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in counts(k - 1, total - first):
                yield (first,) + tail


def traverse(obj, c):
    c[type(obj).__name__] += 1
    if isinstance(obj, dict):
        for key, value in obj.items():
            c["dictionary_keys"] += 1
            traverse(key, c)
            traverse(value, c)
    elif isinstance(obj, list):
        for value in obj:
            traverse(value, c)


def audit_record(rec, k, m, coefficient, mode):
    raw = rec["actions"]
    actions = {tuple(row["counts"]): row["action"] for row in raw}
    expected = {q for d in range(m) for q in counts(k, d)}
    assert len(raw) == len(actions) and set(actions) == expected
    assert all(type(a) is int and 0 <= a < k for a in actions.values())
    assert all(type(x) is int and x >= 0 for q in actions for x in q)
    root = tuple(rec["root"])
    assert len(root) == k and sum(root) == m
    target = rec["target_action"]
    assert 0 <= target < k and root[target] > 0
    weights = []
    for mask, value in rec["weights"].items():
        mask, value = int(mask), F(str(value))
        assert 0 < mask < 1 << k and value >= 0
        if mode == "limit_denominator_1000000":
            value = value.limit_denominator(10**6)
        weights.append((mask, value))
    denominator = math.lcm(*(v.denominator for _, v in weights))
    integer_weights = [(mask, int(value * denominator)) for mask, value in weights]
    L = math.lcm(*range(1, m + 1))

    @lru_cache(None)
    def terminal(q):
        if sum(q) == m:
            return q
        child = list(q)
        child[actions[q]] += 1
        return terminal(tuple(child))

    @lru_cache(None)
    def scaled_pay(q, a):
        total = 0
        for mask, weight in integer_weights:
            if mask >> a & 1:
                den = sum(q[b] for b in range(k) if mask >> b & 1)
                assert den > 0
                total += weight * (L // den)
        return total

    assert terminal((0,) * k) == root
    low, witness, negative = 0, None, 0
    for q, a in actions.items():
        chosen = scaled_pay(terminal(q), a)
        for b in range(k):
            if b == a:
                continue
            child = list(q)
            child[b] += 1
            alt_root = terminal(tuple(child))
            slack = chosen - scaled_pay(alt_root, b)
            if slack < 0:
                negative += 1
            if slack < low:
                low = slack
                witness = {"counts": q, "chosen": a, "alternative": b,
                           "chosen_terminal": terminal(q), "alternative_terminal": alt_root}
    scale = denominator * L
    u = F(scaled_pay(root, target), scale)
    W = sum((v for mask, v in weights if any(root[a] and mask >> a & 1 for a in range(k))), F(0))
    total = sum((v for _, v in weights), F(0))
    out = {"trial": rec["trial"], "states": len(actions), "comparisons": len(actions) * (k - 1),
           "ordered_histories_represented": sum(k**d for d in range(m)),
           "mass_sum": str(total), "W": str(W), "target_payoff": str(u),
           "minimum_IC_slack": str(F(low, scale)), "negative_IC_rows": negative,
           "SPE_for_this_exact_input": low >= 0, "minimum_witness": witness}
    if "comparison" in rec:
        comp = rec["comparison"]
        assert len(comp) == min(m, k) and len(set(comp)) == len(comp)
        assert all(type(a) is int and 0 <= a < k for a in comp)
        C = sum((v for mask, v in weights if any(mask >> a & 1 for a in comp)), F(0))
        objective = C - W - coefficient * u
        # The stored comparison is one optimizer's chosen witness, not all LPs.
        out["comparison_coverage"] = str(C)
        out["mass_normalization_error"] = str(total - 1)
    else:
        queries = [F(str(z)) for z in rec["queries"]]
        if mode == "limit_denominator_1000000":
            queries = [z.limit_denominator(10**6) for z in queries]
        assert len(queries) == k and all(z >= 0 for z in queries)
        tau = sum(queries, F(0))
        C = sum((v * min(F(1), sum((queries[a] for a in range(k) if mask >> a & 1), F(0)))
                 for mask, v in weights), F(0))
        objective = C - W - tau  # LP normalization requires u == 1.
        out.update({"iteration": rec["iteration"], "query_mass": str(tau),
                    "fractional_coverage": str(C), "payoff_normalization_error": str(u - 1),
                    "physical_price_gap": str(C - W - tau * u)})
    out["saved_objective_recomputed"] = str(objective)
    out["difference_from_saved_float"] = float(objective - F(str(rec["value"])))
    return out


def main():
    reports = []
    for name in FILES:
        data = gzip.decompress((BASE / "original" / (name + ".gz")).read_bytes())
        obj = json.loads(data)
        every = Counter()
        traverse(obj, every)
        k, m = obj["parameters"]["topics"], obj["parameters"]["players"]
        coefficient = F(str(obj["parameters"].get("coefficient", m)))
        rs = obj["records"]
        assert [r["trial"] for r in rs] == list(range(len(rs)))
        report = {"file": name, "uncompressed_sha256": hashlib.sha256(data).hexdigest(),
                  "parameters": obj["parameters"], "scope": obj["scope"],
                  "original_elapsed": obj.get("elapsed"), "structure_counts": dict(every),
                  "records": len(rs), "value_range": [min(r["value"] for r in rs), max(r["value"] for r in rs)],
                  "all_record_audits": {}}
        for mode in ("encoded_decimal", "limit_denominator_1000000"):
            results = [audit_record(r, k, m, coefficient, mode) for r in rs]
            summary = {"valid_exact_inputs": sum(r["SPE_for_this_exact_input"] for r in results),
                       "count_states_checked": sum(r["states"] for r in results),
                       "IC_rows_checked": sum(r["comparisons"] for r in results),
                       "ordered_histories_represented": sum(r["ordered_histories_represented"] for r in results),
                       "negative_IC_rows": sum(r["negative_IC_rows"] for r in results),
                       "minimum_IC_slack": str(min(F(r["minimum_IC_slack"]) for r in results)),
                       "max_saved_objective_difference": max(abs(r["difference_from_saved_float"]) for r in results)}
            report[mode] = summary
            report["all_record_audits"][mode] = results
        reports.append(report)
        print(json.dumps({key: value for key, value in report.items() if key not in ("all_record_audits", "parameters", "structure_counts")}), flush=True)
    output = {"scope": "complete saved-table structural and exact fixed-input replay only; no LP or random-search replay; no exact optimality certificate",
              "decimal_note": "encoded decimal and denominator-limited masses are separately defined exact inputs; neither is the original binary float LP model",
              "reports": reports}
    (BASE / "saved-table-audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
