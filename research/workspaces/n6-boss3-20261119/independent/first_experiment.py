"""Exact support test for a common-menu six-player tree.

The vector w[I-1] counts clients incident to exactly the nonempty label mask I.
The compressed dynamic program records final multiplicity and last label.
Its validation program visits every ordered prefix and keeps full ordered paths.
"""
from functools import lru_cache
from itertools import product
import argparse
import json
import random

PLAYERS = 6
SCALE = 60


def metrics(weights, k):
    masks = range(1, 1 << k)
    labels = tuple(tuple(a for a in range(k) if mask & (1 << a)) for mask in masks)

    @lru_cache(None)
    def terminal(counts):
        u = [0] * k
        missing = [0] * k
        welfare = 0
        for w, incident in zip(weights, labels):
            if not w:
                continue
            load = sum(counts[a] for a in incident)
            if load:
                welfare += w
                for a in incident:
                    u[a] += w * (SCALE // load)
            else:
                for a in incident:
                    missing[a] += w
        return tuple(u), welfare, tuple(missing)

    return terminal


def bump(counts, a):
    return counts[:a] + (counts[a] + 1,) + counts[a + 1:]


def support(weights, k):
    leaf = metrics(weights, k)

    @lru_cache(None)
    def solve(prefix):
        n = sum(prefix)
        if n == PLAYERS - 1:
            rows = [(bump(prefix, a), a) for a in range(k)]
            threshold = max(leaf(c)[0][a] for c, a in rows)
            return frozenset((c, a) for c, a in rows if leaf(c)[0][a] >= threshold)
        branches = [solve(bump(prefix, a)) for a in range(k)]
        threshold = max(min(leaf(c)[0][a] for c, _ in branch)
                        for a, branch in enumerate(branches))
        return frozenset((c, z) for a, branch in enumerate(branches)
                         for c, z in branch if leaf(c)[0][a] >= threshold)

    return solve((0,) * k), leaf


def counts_of(s, k):
    return tuple(s.count(a) for a in range(k))


def ordered_support(weights, k):
    # Separate representation: each set is explicitly realized, each tied
    # terminal is an ordered word and each ordered history is a distinct node.
    sets = [set() for a in range(k)]
    client = 0
    for mask, w in enumerate(weights, 1):
        for a in range(k):
            if mask & (1 << a):
                sets[a].update(range(client, client + w))
        client += w

    def payoff(word, i):
        return sum(SCALE // sum(x in sets[a] for a in word)
                   for x in sets[word[i]])

    def rec(h):
        i = len(h)
        if i == PLAYERS:
            return (h,)
        children = [rec(h + (a,)) for a in range(k)]
        # Compare only different siblings directly, no global threshold formula.
        return tuple(s for a, child in enumerate(children) for s in child
                     if all(any(payoff(t, i) <= payoff(s, i) for t in children[b])
                            for b in range(k) if b != a))

    return {(counts_of(s, k), s[-1]) for s in rec(())}


def report_cases(catalogs, k, check_ordered=False):
    result = {"catalogs": 0, "terminal_types": 0, "M_violating_catalogs": 0,
              "final_pay_violating_catalogs": 0, "half_violating_catalogs": 0,
              "min_strict_M_example": None, "min_strict_final_pay_example": None}
    for w in catalogs:
        w = tuple(w)
        roots, leaf = support(w, k)
        if check_ordered:
            assert set(roots) == ordered_support(w, k), w
        result["catalogs"] += 1
        result["terminal_types"] += len(roots)
        bad_m = bad_final = bad_half = False
        for c, z in sorted(roots):
            u, welfare, missing = leaf(c)
            if 2 * welfare < sum(w):
                assert k <= PLAYERS
                bad_half = True
            for stat, violated in [("M", 6 * max(missing) > welfare),
                                   ("final_pay", 6 * u[z] > SCALE * welfare)]:
                if violated:
                    if stat == "M":
                        bad_m = True
                    else:
                        bad_final = True
                    key = "min_strict_" + stat + "_example"
                    prev = result[key]
                    if prev is None or (sum(w), w, c, z) < (sum(prev["w"]), tuple(prev["w"]), tuple(prev["c"]), prev["z"]):
                        result[key] = {"w": w, "c": c, "z": z,
                                       "u_times_60": u, "W": welfare, "missing": missing}
        result["M_violating_catalogs"] += int(bad_m)
        result["final_pay_violating_catalogs"] += int(bad_final)
        result["half_violating_catalogs"] += int(bad_half)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=2)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--ordered", action="store_true")
    parser.add_argument("--draws", type=int)
    parser.add_argument("--seed", type=int, default=20261119)
    args = parser.parse_args()
    if not 1 <= args.k <= PLAYERS:
        raise ValueError("this comparison uses k<=6 so OPT is the union of the menu")
    if args.draws is None:
        catalogs = product(range(args.bits + 1), repeat=(1 << args.k) - 1)
    else:
        rng = random.Random(args.seed)
        catalogs = (tuple(rng.choice((0, 0, 0, 0, 1, 2, 4, 7, 11, 17))
                          for _ in range((1 << args.k) - 1)) for _ in range(args.draws))
    print(json.dumps(report_cases(catalogs, args.k, args.ordered), indent=2))


if __name__ == "__main__":
    main()
