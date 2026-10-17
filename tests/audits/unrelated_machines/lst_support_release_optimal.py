#!/usr/bin/env python3
"""Exact Fraction audit for the optimal-value LST-support release family."""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def block(m: int):
    q = Fraction(m-1, m)
    machines = [f"c{i}" for i in range(m)] + ["s"]
    jobs = [f"a{i}" for i in range(m)] + ["g"]
    p = {}
    for i in range(m):
        p[(f"a{i}", f"c{i}")] = q
        p[(f"a{i}", "s")] = q
    for i in range(m):
        p[("g", f"c{i}")] = Fraction(1)
    p[("g", "s")] = Fraction(1)
    return machines, jobs, p


def enumerate_block(m: int):
    machines, jobs, p = block(m)
    choices = [[i for i in machines if (j, i) in p] for j in jobs]
    rows = []
    for assn in product(*choices):
        loads = {i: Fraction(0) for i in machines}
        zero_edges = 0
        for j, i in zip(jobs, assn):
            loads[i] += p[(j, i)]
            # x has positive mass only a_i-c_i and g-c_i.
            positive = (j.startswith("a") and i == "c" + j[1:]) or (j == "g" and i.startswith("c"))
            zero_edges += int(not positive)
        rows.append({"assignment": assn, "makespan": max(loads.values()), "zero_edges": zero_edges})
    return rows


def main():
    out = {"family": "UM-LST-SUPPORT-RELEASE-OPTIMAL-v1", "cases": []}
    for m in range(2, 6):
        rows = enumerate_block(m)
        opt = min(r["makespan"] for r in rows)
        assert opt == 1, (m, opt)
        for r in range(1, 4):
            for k in range(r + 1):
                # Independent blocks: a block with no released edge has the bad value;
                # a released block can attain 1. The formula is checked against the
                # exact one-block enumeration rather than used as its proof.
                no_release = min(x["makespan"] for x in rows if x["zero_edges"] == 0)
                with_release = min(x["makespan"] for x in rows if x["zero_edges"] >= 1)
                predicted = Fraction(2 * m - 1, m) if k < r else Fraction(1)
                observed = no_release if k < r else with_release
                assert no_release == Fraction(2 * m - 1, m)
                assert with_release == 1
                assert observed == predicted, (m, r, k, observed, predicted)
                out["cases"].append({"m": m, "r": r, "k": k, "block_opt": str(opt),
                                     "zero_support_makespan": str(no_release),
                                     "released_block_makespan": str(with_release),
                                     "predicted_global": str(predicted)})
    out["checks"] = {"fraction": True, "m": [2, 5], "r": [1, 3], "all_cases_pass": True}
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
