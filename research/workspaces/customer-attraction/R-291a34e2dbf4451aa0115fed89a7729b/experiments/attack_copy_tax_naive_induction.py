#!/usr/bin/env python3
"""Find a finite counterexample to the naive branchwise induction interface.

This does not attack the harmonic-potential/copy-tax candidate itself.  It
tests the stronger step saying that the prescribed root child's continuation
bank pays every credible off-child potential bank separately.
"""
from functools import lru_cache
from itertools import product
from math import lcm
import json
from pathlib import Path


P = 3
TYPES = tuple(product((0, 1), repeat=P))[1:]


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for x in range(n + 1):
        for tail in compositions(n - x, k - 1):
            yield (x,) + tail


def search(m, max_count=2):
    scale = lcm(*range(1, m + 1))
    finals = tuple(compositions(m, P))
    load = {q: tuple(sum(t[a] * q[a] for a in range(P)) for t in TYPES)
            for q in finals}
    utility = {(q, a): tuple(t[a] * (scale // z if z else 0)
                              for t, z in zip(TYPES, load[q]))
               for q in finals for a in range(P)}

    for weights in product(range(max_count + 1), repeat=len(TYPES)):
        if not any(weights):
            continue

        def dot(row):
            return sum(x * w for x, w in zip(row, weights))

        @lru_cache(None)
        def outcomes(prefix):
            """terminal -> minimum tail copy tax among SPE realizations."""
            if sum(prefix) == m:
                return {prefix: 0}
            remaining = m - sum(prefix)
            past = tuple(sum(t[a] * prefix[a] for a in range(P)) for t in TYPES)
            child = []
            for a in range(P):
                z = list(prefix); z[a] += 1
                child.append(outcomes(tuple(z)))
            threshold = max(min(dot(utility[q, a]) for q in ys)
                            for a, ys in enumerate(child))
            kept = {}
            for a, ys in enumerate(child):
                first_tax = dot(tuple(t[a] * (scale // (b + 1)
                                               - scale // (b + remaining))
                                      for t, b in zip(TYPES, past)))
                for q, tail_tax in ys.items():
                    if dot(utility[q, a]) >= threshold:
                        kept[q] = min(kept.get(q, 10**100), first_tax + tail_tax)
            return kept

        root_children = []
        for a in range(P):
            z = [0] * P; z[a] = 1
            root_children.append(outcomes(tuple(z)))
        threshold = max(min(dot(utility[q, a]) for q in ys)
                        for a, ys in enumerate(root_children))

        # B_child is total utility of the remaining m-1 providers plus their tax.
        def child_bank(a, q, tail_tax):
            remaining_utility = sum((q[j] - int(j == a)) * dot(utility[q, j])
                                    for j in range(P))
            return remaining_utility + tail_tax

        root_arrival = [sum(w for t, w in zip(TYPES, weights) if t[a]) * scale
                        for a in range(P)]
        root_tax = [sum(t[a] * (scale - scale // m) * w
                        for t, w in zip(TYPES, weights)) for a in range(P)]

        for actual_a, actual_outcomes in enumerate(root_children):
            for qa, taxa in actual_outcomes.items():
                ua = dot(utility[qa, actual_a])
                if ua < threshold:
                    continue
                actual_budget = ua + root_tax[actual_a] + child_bank(actual_a, qa, taxa)
                for dev_a, dev_outcomes in enumerate(root_children):
                    for qt, taxt in dev_outcomes.items():
                        # This off-child can be selected while actual_a remains optimal.
                        if dot(utility[qt, dev_a]) > ua:
                            continue
                        demanded = root_arrival[dev_a] + child_bank(dev_a, qt, taxt)
                        if demanded > actual_budget:
                            return {
                                "status": "NAIVE_BRANCH_INDUCTION_FALSE",
                                "m": m, "catalog_size": P, "scale": scale,
                                "weights": list(weights),
                                "actual_action": actual_a,
                                "actual_terminal_counts": list(qa),
                                "deviation_action": dev_a,
                                "deviation_terminal_counts": list(qt),
                                "actual_root_payoff": ua,
                                "deviation_root_payoff": dot(utility[qt, dev_a]),
                                "actual_budget": actual_budget,
                                "deviation_demand": demanded,
                                "gap_scaled": demanded - actual_budget,
                            }
    return {"status": "NO_COUNTEREXAMPLE_IN_DOMAIN", "m": m}


def main():
    results = []
    for m in range(2, 7):
        result = search(m)
        results.append(result)
        if result["status"] != "NO_COUNTEREXAMPLE_IN_DOMAIN":
            break
    report = {
        "claim_attacked": "branchwise induction for the potential/copy-tax candidate",
        "scope": "exact finite search; a witness refutes only the stronger induction interface",
        "results": results,
    }
    target = Path(__file__).with_name("copy_tax_naive_induction_attack.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
