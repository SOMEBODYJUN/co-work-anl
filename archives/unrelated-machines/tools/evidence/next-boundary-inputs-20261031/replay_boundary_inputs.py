#!/usr/bin/env python3
"""Exact structural replay for three claimed unrelated-machines input examples."""
from __future__ import annotations
import argparse, collections, hashlib, json, math
from fractions import Fraction
from pathlib import Path


def replay_reset(d, raw):
    p = [[Fraction(x) for x in row] for row in d["processing_times"]]
    assert len(p) == 4 and all(len(row) == 8 for row in p)
    assert set(x for row in p for x in row) == {Fraction(1, 2)}
    fallback = {int(k): v for k, v in d["fallbacks"].items()}
    return {
        "sha256": hashlib.sha256(raw).hexdigest(), "machines": len(p), "jobs": len(p[0]),
        "q": d["q"], "T": d["T"], "absorbed_jobs": d["absorbed_jobs"],
        "all_processing_times_one_half": True,
        "fallbacks": fallback, "fallback_pairs": sorted((k, v) for k, v in fallback.items()),
        "balanced_schedule_count": math.factorial(8) // (math.factorial(2) ** 4),
        "scope": "input and counting replay; pushforward threshold claims remain in related audit",
    }


def replay_three_host(d, raw):
    p = [[None if x is None else Fraction(x) for x in row] for row in d["p"]]
    finite = [[(i, j, str(x)) for j, x in enumerate(row) if x is not None] for i, row in enumerate(p)]
    return {
        "sha256": hashlib.sha256(raw).hexdigest(), "T": d["T"], "hosts": d["hosts"],
        "shape": [len(p), len(p[0])], "finite_edges": sum(len(x) for x in finite),
        "S1": d["S1"], "S2": d["S2"],
        "expected_bad_optima": d["expected_bad_optima"],
        "claim": d["claim"], "santa_sharp_claim": d["santa_sharp"]["claim"],
        "scope": "finite sharp profile input; no general selector or Santa theorem by this replay",
    }


def replay_pool(d, raw):
    selected = d["selected_groups"]
    resources = [tuple(x) for group in selected.values() for x in group]
    assert len(set(resources)) == len(resources)
    assert len(resources) == d["used_resources"]
    return {
        "sha256": hashlib.sha256(raw).hexdigest(), "K": d["K"], "s": d["s"],
        "vertices": d["vertices"], "edges": d["edges"],
        "original_edges": len(d["original_edges"]), "residual_edges": len(d["residual_edges"]),
        "root_demand": d["root_demand"], "score": d["score"],
        "selected_group_count": len(selected), "selected_resources": len(resources),
        "selected_resources_pairwise_disjoint": True,
        "checks": d["checks"],
        "scope": "finite counterexample input and selected tree replay; exact frontier is in related review",
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("directory", type=Path); ap.add_argument("--output", type=Path)
    args = ap.parse_args(); out = {}
    for name, fn in [("symmetric_reset_q2.json", replay_reset), ("three_host_selector_sharp_profiles.json", replay_three_host), ("two_state_pool_partial_tree_counterexample.json", replay_pool)]:
        raw = (args.directory / name).read_bytes(); out[name] = fn(json.loads(raw), raw)
    text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if args.output: args.output.write_text(text)
    else: print(text, end="")

if __name__ == "__main__": main()
