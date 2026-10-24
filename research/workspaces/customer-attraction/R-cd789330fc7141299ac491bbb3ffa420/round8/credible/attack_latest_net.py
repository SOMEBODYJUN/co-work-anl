#!/usr/bin/env python3
r"""Exact separation oracle for one stated general structural candidate.

This is NOT a CAG SPE solver and cannot witness failure of Q-CAG-HALF.
One fresh source is uniformly split on an initial query's coverers.  At each
natural occurrence i, an arbitrary actual-reset profile U contains i and only
roles >=i.  Let b=|V|, a=|U|.  If a>b, NET sends h/a to the latest a-b members
of U\V and absorbs the remainder.  Candidate: the aggregate incoming density
sum_{contexts at j} |V_context| h_context is at most the source stock 1.

DP maximizes that quantity over arbitrary reset-profile trees.  Prescribed
topic labels may be distinct, so leaves need not be SPE.  A separation is only
a structural routing counterexample; lack of separation proves no general
claim.  Exact Fraction arithmetic throughout.
"""
from fractions import Fraction
from functools import cache
import argparse
import json


def run(m):
    records = []
    tested = 0
    for target in range(1, m):
        choices = {}

        @cache
        def value(v, i):
            b = v.bit_count()
            if i == target:
                return Fraction(b)
            if i > target:
                return Fraction(0)
            best = Fraction(0)
            suffix = ((1 << m) - 1) ^ ((1 << (i + 1)) - 1)
            sub = suffix
            while True:
                u = sub | (1 << i)
                a = u.bit_count()
                if a > b:
                    new = [k for k in range(i + 1, m) if (u >> k) & 1 and not (v >> k) & 1]
                    selected = new[-(a - b):]
                    score = sum((value(u, k) for k in selected), Fraction(0)) / a
                    if score > best:
                        best = score
                        choices[(v, i)] = (u, selected)
                if sub == 0:
                    break
                sub = (sub - 1) & suffix
            return best

        for v in range(1, 1 << m, 2):
            tested += 1
            total = sum((value(v, i) for i in range(1, m) if (v >> i) & 1), Fraction(0)) / v.bit_count()
            if total > 1:
                def tree(v, i, h):
                    record = {"profile": [k for k in range(m) if (v >> k) & 1], "role": i,
                              "incoming": str(h), "density": str(h * v.bit_count())}
                    if i != target and (v, i) in choices:
                        u, selected = choices[(v, i)]
                        record["reset"] = [k for k in range(m) if (u >> k) & 1]
                        record["selected"] = selected
                        record["children"] = [tree(u, k, h / u.bit_count()) for k in selected if k <= target]
                    return record
                records.append({"m": m, "target": target, "density": str(total),
                                "initial_profile": [k for k in range(m) if (v >> k) & 1],
                                "initial_future": [tree(v, i, Fraction(1, v.bit_count()))
                                                   for i in range(1, m) if (v >> i) & 1 and i <= target]})
                return {"status": "structural_separation", "tested_initial_target_pairs": tested,
                        "not_an_SPE_counterexample": True, "witness": records[0]}
    return {"status": "no_separation_in_this_finite_attack", "m": m,
            "tested_initial_target_pairs": tested, "general_candidate_proved": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=9)
    args = parser.parse_args()
    results = []
    for m in range(2, args.max_m + 1):
        result = run(m)
        results.append(result)
        if result["status"] == "structural_separation":
            break
    print(json.dumps({"candidate": "fresh_latest_NET_aggregate_role_density_le_source_stock",
                      "results": results}, ensure_ascii=False, indent=2))
