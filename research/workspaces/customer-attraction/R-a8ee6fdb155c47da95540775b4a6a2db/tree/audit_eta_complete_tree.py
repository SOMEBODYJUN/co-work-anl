"""Enumerate literal full ordered-history strategies to audit eta tree DP.

No outcome-set recurrence is used in the brute-force oracle. This checks the
quantifier over all nonanonymous tie choices, including empty/duplicate topics.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

from eta_complete_tree import Tree


def brute(instance):
    m, p = instance["players"], len(instance["topics"])
    clients = [frozenset(row["topics"]) for row in instance["customers"]
               for _ in range(row["multiplicity"])]
    histories = [h for length in range(m) for h in product(range(p), repeat=length)]

    def covered(h):
        return frozenset(i for i, B in enumerate(clients) if any(a in B for a in h))

    def payoff(a, z):
        return sum((F(1, sum(b in B for b in z)) for B in clients if a in B), F(0))

    @lru_cache(None)
    def completion(h):
        best = len(covered(h))
        for size in range(1, min(m - len(h), p) + 1):
            for rest in combinations(range(p), size):
                best = max(best, len(covered(h + rest)))
        return best

    best = None
    outcomes, accepted = set(), 0
    for rules in product(range(p), repeat=len(histories)):
        actions = dict(zip(histories, rules))
        leaves = {}
        legal = True
        def replay(h):
            nonlocal legal
            if len(h) == m:
                return h
            children = [replay(h + (a,)) for a in range(p)]
            a = actions[h]
            z = children[a]
            if any(payoff(a, z) < payoff(b, children[b]) for b in range(p)):
                legal = False
            leaves[h] = z
            return z
        z = replay(())
        if not legal:
            continue
        accepted += 1
        outcomes.add(tuple(z.count(a) for a in range(p)))
        eta_sum = F(0)
        for length in range(m):
            h, s, r = z[:length], z[length], m - length
            terms = []
            for a in range(p):
                if completion(h + (a,)) != completion(h):
                    continue
                d = leaves[h + (a,)] if r > 1 else h + (a,)
                M = covered((a,)) - covered(h + (s,))
                tail = d[length + 1:]
                t = M - covered(tail)
                eta = r * payoff(a, d) - len(M) - (r - 1) * len(t)
                assert eta >= 0
                terms.append(eta / r)
            eta_sum += min(terms)
        defect = eta_sum - 2 * len(covered(z)) + completion(())
        best = defect if best is None else max(best, defect)
    assert best is not None
    return best, outcomes, accepted, p ** len(histories)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    groups = []
    for p, m in [(2, 3), (3, 2)]:
        instances = strategy_checks = accepted = 0
        for presence in product((0, 1), repeat=(1 << p) - 1):
            instance = {"players": m, "topics": [str(a) for a in range(p)],
                        "customers": [{"topics": [a for a in range(p) if mask >> a & 1],
                                       "multiplicity": presence[mask - 1]}
                                      for mask in range(1, 1 << p) if presence[mask - 1]]}
            value, outcomes, count, strategies = brute(instance)
            tree = Tree(instance)
            report = tree.solve()
            assert F(report["max_defect_over_all_complete_SPE"]) == value
            assert set(tree.outcomes(tree.zero)) == outcomes
            instances += 1
            strategy_checks += strategies
            accepted += count
            for method in ["cov", "pay", "outcomes", "threshold", "optimum", "envelope", "path_best"]:
                getattr(tree, method).cache_clear()
        groups.append({"topics": p, "players": m, "all_binary_type_instances": instances,
                       "all_literal_complete_strategies_checked": strategy_checks,
                       "SPE_strategies_accepted": accepted,
                       "outcome_sets_and_eta_maxima_agree": True})
    report = {"status": "PASS", "oracle": "Literal full ordered-history strategy enumeration, unit clients, Fraction shares; no BI in oracle.",
              "scope": "Implementation and quantifier audit only; no universal half or eta inequality is inferred.",
              "groups": groups,
              "sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                         for name in ["eta_complete_tree.py", "audit_eta_complete_tree.py"]}}
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
