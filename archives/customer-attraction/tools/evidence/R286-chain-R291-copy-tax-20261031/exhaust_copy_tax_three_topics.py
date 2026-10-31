#!/usr/bin/env python3
"""Exhaustive small-universe attack on the harmonic-potential/copy-tax candidate.

For three topics enumerate counts 0,1,2, and for four topics enumerate binary
counts.  At every count state, retain every terminal count vector
that can be selected by some complete ordered-history pure SPE, together with
the minimum copy tax among realizing action orders.  Count caching is only for
the set of possible continuations; different ordered histories may select
different members of that set.
"""
from functools import lru_cache
from itertools import product
from math import lcm
import json
from pathlib import Path


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for x in range(n + 1):
        for tail in compositions(n - x, k - 1):
            yield (x,) + tail


def run_case(m, topics, max_multiplicity):
    types = tuple(product((0, 1), repeat=topics))[1:]
    scale = lcm(*range(1, m + 1))
    harmonic = [0]
    for k in range(1, m + 1):
        harmonic.append(harmonic[-1] + scale // k)
    finals = tuple(compositions(m, topics))
    load = {q: tuple(sum(t[a] * q[a] for a in range(topics)) for t in types)
            for q in finals}
    utility = {
        (q, a): tuple(t[a] * (scale // z if z else 0)
                      for t, z in zip(types, load[q]))
        for q in finals for a in range(topics)
    }
    potential = {q: tuple(harmonic[z] for z in load[q]) for q in finals}
    covered = {q: tuple(scale * int(z > 0) for z in load[q]) for q in finals}
    checked = 0
    largest_gap = None
    witness = None
    max_states = 0
    max_root_outcomes = 0

    for weights in product(range(max_multiplicity + 1), repeat=len(types)):
        if not any(weights):
            continue
        checked += 1

        def dot(row):
            return sum(x * w for x, w in zip(row, weights))

        @lru_cache(None)
        def all_spe(prefix):
            if sum(prefix) == m:
                return {prefix: 0}
            remaining = m - sum(prefix)
            past = tuple(sum(t[a] * prefix[a] for a in range(topics)) for t in types)
            children = []
            for a in range(topics):
                child = list(prefix)
                child[a] += 1
                children.append(all_spe(tuple(child)))
            threshold = max(min(dot(utility[q, a]) for q in outcomes)
                            for a, outcomes in enumerate(children))
            kept = {}
            for a, outcomes in enumerate(children):
                tax_row = tuple(t[a] * (scale // (b + 1) - scale // (b + remaining))
                                for t, b in zip(types, past))
                tax = dot(tax_row)
                for q, tail_tax in outcomes.items():
                    if dot(utility[q, a]) >= threshold:
                        kept[q] = min(kept.get(q, 10**100), tail_tax + tax)
            assert kept
            return kept

        roots = all_spe((0,) * topics)
        max_states = max(max_states, all_spe.cache_info().currsize)
        max_root_outcomes = max(max_root_outcomes, len(roots))
        best_potential = max(dot(potential[q]) for q in finals)
        for q, tax in roots.items():
            gap = best_potential - dot(covered[q]) - tax
            if largest_gap is None or gap > largest_gap:
                largest_gap = gap
            if gap > 0:
                witness = {
                    "weights": list(weights),
                    "terminal_counts": list(q),
                    "gap_scaled": gap,
                    "scale": scale,
                    "root_outcomes": len(roots),
                }
                return {
                    "m": m, "catalog_size": topics, "status": "REFUTED_IN_FINITE_UNIVERSE",
                    "checked_instances": checked, "witness": witness,
                }
    return {
        "m": m, "catalog_size": topics, "status": "NO_REFUTATION_IN_ENUMERATED_UNIVERSE",
        "multiplicity_domain": f"each of {len(types)} nonempty interest types has count 0..{max_multiplicity}; all-zero omitted",
        "checked_instances": checked, "largest_gap_scaled": largest_gap, "scale": scale,
        "maximum_count_states": max_states, "maximum_root_terminal_counts": max_root_outcomes,
    }


def main():
    report = {
        "candidate": "maximum m-slot harmonic potential <= actual W + ordered self-copy tax",
        "scope": "exact exhaustive finite attack; not a general proof",
        "results": ([run_case(m, 3, 2) for m in range(2, 7)]
                    + [run_case(6, 4, 1)]),
    }
    target = Path(__file__).with_name("copy_tax_three_topics_exact.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
