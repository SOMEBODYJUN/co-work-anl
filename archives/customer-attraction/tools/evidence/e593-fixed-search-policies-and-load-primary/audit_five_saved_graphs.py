"""One fixed-record exact review; no original import, BI, LP, RNG or scan.

Source JSON numeric values are kept unchanged.  Binary/decimal literal
interpretations and a separately defined integer-client calibration are
reported independently, including every failure.
"""
from collections import Counter, defaultdict
from decimal import Decimal
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import gzip
import hashlib
import json
import math
import platform
import sys
import time


CASES = [
    ("83aeac84ff59ae42a9d6", "search_m5p7.json"),
    ("351b0859f830ed409806", "search_m5p7_allj.json"),
    ("e18b70bbb8719f4a182c", "search_m5p7_mix.json"),
    ("d73387b0668aa5956e1b", "search_m5p9_mix.json"),
    ("8172fb7830818f6b58f1", "search_m6p7_mix.json"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tuple_levels(p, m):
    levels = []
    for degree in range(m + 1):
        rows = []
        for choices in combinations_with_replacement(range(p), degree):
            count = Counter(choices)
            rows.append(tuple(count.get(a, 0) for a in range(p)))
        levels.append(sorted(rows))
    return levels


def examine(source, source_id):
    raw = source.read_bytes()
    original = json.loads(raw)
    decimal = json.loads(raw, parse_float=Decimal)
    p, m = original["args"]["topics"], original["args"]["players"]
    levels = tuple_levels(p, m)
    states = [q for level in levels for q in level]
    terminals = levels[-1]
    index = {q: i for i, q in enumerate(states)}
    tidx = {q: t for t, q in enumerate(terminals)}
    nonterm = len(states) - len(terminals)
    policy = {}
    for row in original["policy"]:
        assert isinstance(row, list) and len(row) == 4
        i, t, a, branches = row
        assert (i, t) not in policy
        assert 0 <= i < nonterm and 0 <= t < len(terminals) and 0 <= a < p
        assert len(branches) == p and all(0 <= b < len(terminals) for b in branches)
        assert all(x <= y for x, y in zip(states[i], terminals[t]))
        assert branches[a] == t
        policy[i, t] = (a, tuple(branches))
    root_count = tuple(original["best"]["root"])
    assert sum(root_count) == m
    root = (0, tidx[root_count])
    assert root in policy
    multiplicity = Counter({root: 1})
    representatives = {root: ()}
    checked_nodes = []
    ordered_by_depth = []
    for depth in range(m):
        keys = sorted(key for key in multiplicity if sum(states[key[0]]) == depth)
        assert sum(multiplicity[key] for key in keys) == p ** depth
        ordered_by_depth.append(p ** depth)
        for key in keys:
            assert key in policy
            i, t = key
            a, branches = policy[key]
            for b, desired in enumerate(branches):
                child = list(states[i]); child[b] += 1; child = tuple(child)
                assert all(x <= y for x, y in zip(child, terminals[desired]))
                if depth + 1 == m:
                    assert child == terminals[desired]
                else:
                    ck = (index[child], desired)
                    assert ck in policy
                    multiplicity[ck] += multiplicity[key]
                    representatives.setdefault(ck, representatives[key] + (b,))
            checked_nodes.append(key)
    assert set(checked_nodes) == set(policy)
    actual_path = []
    node = root
    for depth in range(m):
        a, branches = policy[node]
        actual_path.append(a)
        if depth + 1 < m:
            child = list(states[node[0]]); child[a] += 1
            node = (index[tuple(child)], branches[a])
    assert tuple(actual_path.count(a) for a in range(p)) == root_count
    source_weights = original["weights_float"]
    assert len(source_weights) == (1 << p) - 1
    positive = [mask for mask, value in enumerate(source_weights, 1) if value != 0]
    assert all(value >= 0 for value in source_weights)
    largest = max(positive, key=lambda mask: source_weights[mask - 1])
    assert source_weights[largest - 1] == 1.0 and len(positive) == m
    interpretations = {
        "source_binary_float_exact_value": {mask: F.from_float(source_weights[mask - 1]) for mask in positive},
        "source_JSON_decimal_token_exact_value": {mask: F(decimal["weights_float"][mask - 1]) for mask in positive},
        "separately_defined_integer_clients": {mask: F(m if mask == largest else 1) for mask in positive},
    }
    local_detail = []
    outputs = {}
    support = tuple(original["best"]["support"])
    assert len(support) == min(p, m) and len(set(support)) == len(support)
    total_count = sum(ordered_by_depth)
    for label, weights in interpretations.items():
        payoff = {}
        def value(t, a):
            key = (t, a)
            if key not in payoff:
                q = terminals[t]
                payoff[key] = sum((weight / sum(q[b] for b in range(p) if mask >> b & 1)
                                   for mask, weight in weights.items() if mask >> a & 1), F(0))
            return payoff[key]
        minimum = None
        negative_local = negative_ordered = zero_local = zero_ordered = local_ic = 0
        first_negative = None
        for key in checked_nodes:
            i, t = key
            a, branches = policy[key]
            row = []
            for b, desired in enumerate(branches):
                if b == a:
                    continue
                gap = value(t, a) - value(desired, b)
                local_ic += 1
                row.append(str(gap))
                minimum = gap if minimum is None else min(minimum, gap)
                if gap < 0:
                    negative_local += 1; negative_ordered += multiplicity[key]
                    if first_negative is None:
                        first_negative = {"key": list(key), "history": list(representatives[key]),
                                          "prescribed": a, "deviation": b, "gap": str(gap)}
                if gap == 0:
                    zero_local += 1; zero_ordered += multiplicity[key]
            local_detail.append({"interpretation": label, "key": list(key),
                                 "ordered_history_multiplicity": multiplicity[key],
                                 "nonself_gaps_in_action_order": row})
        def coverage(topic_set):
            mask_set = sum(1 << a for a in topic_set)
            return sum((v for mask, v in weights.items() if mask & mask_set), F(0))
        actual_W = coverage({a for a, number in enumerate(root_count) if number})
        comparisons = [(coverage(set(S)), S) for S in combinations(range(p), min(p, m))]
        optimum = max(v for v, _ in comparisons)
        fixed = coverage(set(support))
        outputs[label] = {"weights": {str(k): str(v) for k, v in weights.items()},
                          "SPE_by_complete_graph_check": negative_local == 0,
                          "compact_nonself_IC_checks": local_ic,
                          "ordered_history_IC_multiplicity_covered": total_count * (p - 1),
                          "minimum_gap": str(minimum), "negative_compact_IC": negative_local,
                          "negative_ordered_IC_multiplicity": negative_ordered,
                          "zero_compact_IC": zero_local, "zero_ordered_IC_multiplicity": zero_ordered,
                          "first_negative": first_negative,
                          "actual_W": str(actual_W), "fixed_comparison": str(fixed),
                          "true_OPT": str(optimum), "true_OPT_over_W": str(optimum / actual_W),
                          "fixed_comparison_is_optimal": fixed == optimum}
    records = original["records"]
    for record in records:
        assert set(record) == {"step", "ratio", "cone_value", "rows", "root", "support", "positive_types"}
        assert sum(record["root"]) == m and len(record["root"]) == p
        assert 0 <= record["step"] < original["args"]["iterations"]
        assert all(0 <= a < p for a in record["support"])
    assert original["best"] in records
    aliases = defaultdict(list)
    for a in range(p):
        aliases[tuple(mask for mask in positive if mask >> a & 1)].append(a)
    assert source.read_bytes() == raw
    return {"source_id": source_id, "source_sha256": sha(raw), "players": m, "topics": p,
            "args": original["args"], "best": original["best"], "record_count": len(records),
            "record_step_range": [min(x["step"] for x in records), max(x["step"] for x in records)],
            "elapsed_field_present": "elapsed" in original, "elapsed_field": original.get("elapsed"),
            "raw_source_weights_nonzero": {str(mask): repr(source_weights[mask - 1]) for mask in positive},
            "policy_rows_fully_checked": len(policy), "graph_keys_all_reachable": True,
            "total_count_states": len(states), "terminal_count_states": len(terminals),
            "ordered_nonterminal_histories_covered": total_count,
            "ordered_depth_counts": ordered_by_depth, "actual_ordered_path": actual_path,
            "alias_classes": [{"interest_support": list(k), "labels": v} for k, v in aliases.items()],
            "all_records": records, "interpretations": outputs}, local_detail


def main():
    base = Path(__file__).resolve().parent
    output = base / "fixed-five-001"
    if (output / "report.json").exists():
        raise SystemExit("event exists; preserve it and replay only in a package copy")
    output.mkdir(exist_ok=True)
    start_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    started = time.perf_counter()
    results, local = [], []
    for source_id, filename in CASES:
        record, rows = examine(base / "original" / source_id / filename, source_id)
        results.append(record); local.extend(rows)
    elapsed = time.perf_counter() - started
    report = {"status": "completed-with-source-literal-failures-preserved", "cases": results,
              "scope": "five fixed compact complete graphs only; integer calibration is a separately defined input, never a repair attributed to the old search",
              "execution": {"run_count": 1, "start_utc": start_utc, "argv": [sys.executable, *sys.argv],
                            "python_version": platform.python_version(), "internal_elapsed_seconds": elapsed,
                            "native_search_calls": 0, "LP_calls": 0, "RNG_calls": 0, "BI_calls": 0,
                            "native_CG_checker_calls": 0, "native_load_solve_calls": 0,
                            "explicit_ordered_tree_materializations": 0},
              "limits": ["All ordered histories are covered by a checked layered graph and integer path multiplicities, not by materializing those keys.",
                         "Binary floats and exact decimal tokens are distinct interpretations of original stored numbers.",
                         "No negative margin is silently rounded or removed.",
                         "No saved finite best is called a global optimum over all policies."]}
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    with gzip.open(output / "all-compact-node-margins.json.gz", "wt", encoding="utf-8") as stream:
        json.dump(local, stream, ensure_ascii=False, separators=(",", ":"))
    summary = {"cases": [{"file": filename, "compact_nodes": r["policy_rows_fully_checked"],
                           "ordered_nodes_covered": r["ordered_nonterminal_histories_covered"],
                           "SPE_by_interpretation": {k: v["SPE_by_complete_graph_check"] for k, v in r["interpretations"].items()},
                           "minima": {k: v["minimum_gap"] for k, v in r["interpretations"].items()}}
                          for (_, filename), r in zip(CASES, results)], "seconds": elapsed}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
