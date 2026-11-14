"""Recompute every attainable root count and its welfare from the frozen inputs.

Run from the repository root: python map/edges/customer-attraction-3a-3a-3e34cf53d63120f6/exact-worst-spe.py
"""
from functools import cache
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path


EVIDENCE = Path("archives/customer-attraction/tools/evidence/cascade-original-nine-boss3")
SOURCES = ("cascade_m5p7_best.json", "cascade_m5p7_open_best.json", "cascade_m5p8_private_best.json")


def analyze(instance):
    m = instance["players"]
    p = len(instance["topics"])
    scale = lcm(*range(1, m + 1))
    customers = [(tuple(row["topics"]), row["multiplicity"]) for row in instance["customers"]]

    @cache
    def payoff(q, action):
        return sum(n * (scale // sum(q[b] for b in group)) for group, n in customers if action in group)

    def child(q, action):
        return q[:action] + (q[action] + 1,) + q[action + 1:]

    @cache
    def attainable(q):
        if sum(q) == m:
            return frozenset([q])
        successors = [attainable(child(q, action)) for action in range(p)]
        threshold = max(min(payoff(z, action) for z in outcomes) for action, outcomes in enumerate(successors))
        return frozenset(z for action, outcomes in enumerate(successors) for z in outcomes if payoff(z, action) >= threshold)

    def coverage(support):
        return sum(n for group, n in customers if support.intersection(group))

    root = sorted(attainable((0,) * p))
    welfare = [(q, coverage({a for a, n in enumerate(q) if n})) for q in root]
    minimum = min(w for _, w in welfare)
    optimum = max(coverage(set(J)) for J in combinations(range(p), min(m, p)))
    return {
        "players": m,
        "labels": p,
        "payoff_scale": scale,
        "count_states_including_terminal": attainable.cache_info().currsize,
        "attainable_root_count_vectors": len(root),
        "all_root_counts_and_welfare": [{"counts": q, "welfare": w} for q, w in welfare],
        "minimum_SPE_welfare": minimum,
        "minimizing_root_counts": [q for q, w in welfare if w == minimum],
        "OPT": optimum,
    }


def main():
    manifest = json.loads((EVIDENCE / "source-manifest.json").read_bytes())
    entries = {Path(entry["path"]).name: entry for entry in manifest}
    results = {}
    for name in SOURCES:
        entry = entries[name]
        raw = (EVIDENCE / "original" / entry["id"] / name).read_bytes()
        sha = sha256(raw).hexdigest()
        if len(raw) != entry["size"] or sha != entry["sha256"]:
            raise ValueError(f"Frozen input changed: {name}")
        saved = json.loads(raw)
        result = analyze(saved["instance"])
        saved_target = saved["target"]
        target_welfare = next(row["welfare"] for row in result["all_root_counts_and_welfare"] if row["counts"] == tuple(saved_target))
        results[name] = {"source_sha256": sha, **result, "saved_strategy_welfare": target_welfare,
                         "saved_strategy_attains_minimum": target_welfare == result["minimum_SPE_welfare"]}
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
