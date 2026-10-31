"""Exact finite checks for topic selection; no computational claim is a proof.

Run: python topic-selection-drafts/cross_field_battle/toy_checks.py
All arithmetic used in fairness checks is integer. Seed: 20261020.
"""
from itertools import permutations, product, combinations_with_replacement
import json
import random
from pathlib import Path


def copies_sd_ef1(owners, orders, n):
    for i, order in enumerate(orders):
        counts = [0] * n
        for g in order:
            for j in owners[g]:
                counts[j] += 1
            if max(counts) > counts[i] + 1:
                return False
    return True


def copies_exhaustive():
    # Normalize agent 0's strict type ranking by type relabeling.
    n, t = 3, 4
    perms = list(permutations(range(t)))
    checked = 0
    for mult in product((1, 2), repeat=t):
        choices = [list(__import__('itertools').combinations(range(n), c)) for c in mult]
        allocations = list(product(*choices))
        for p1 in perms:
            for p2 in perms:
                orders = [tuple(range(t)), p1, p2]
                assert any(copies_sd_ef1(a, orders, n) for a in allocations), (mult, orders)
                checked += 1
    return {"n": n, "types": t, "strict_profiles_mod_type_relabeling": checked,
            "allocations_per_profile": 3 ** t, "counterexamples": 0}


def maximum_matching(adj, m):
    owner = [-1] * m
    def augment(i, seen):
        for e in adj[i]:
            if seen[e]:
                continue
            seen[e] = True
            if owner[e] < 0 or augment(owner[e], seen):
                owner[e] = i
                return True
        return False
    for i in range(len(adj)):
        augment(i, [False] * m)
    return owner


def rank2_cost(i, bundle, words):
    return len({(words[e] >> i) & 1 for e in bundle})


def rank2_witness(words, n):
    m = len(words)
    assert m >= n
    present = set(words)
    if len(present) == 2 ** n:
        bundles = [[] for _ in range(n)]
        unused = set(range(m))
        complement = (1 << n) - 1
        pairs = [(w, w ^ complement) for w in range(2 ** n) if w < (w ^ complement)]
        for i, (a, b) in enumerate(pairs[:n]):
            ea = next(e for e in unused if words[e] == a)
            unused.remove(ea)
            eb = next(e for e in unused if words[e] == b)
            unused.remove(eb)
            bundles[i] = [ea, eb]
        bundles[0].extend(unused)
        return bundles
    for w in range(2 ** n):
        if w in present:
            continue
        adj = [[e for e, z in enumerate(words) if ((z >> i) & 1) != ((w >> i) & 1)] for i in range(n)]
        owner = maximum_matching(adj, m)
        if len({i for i in owner if i >= 0}) == n:
            for e in range(m):
                if owner[e] < 0:
                    owner[e] = next(i for i in range(n) if e in adj[i])
            return [[e for e in range(m) if owner[e] == i] for i in range(n)]
    raise AssertionError((n, words))


def rank2_exact():
    checked = 0
    for m in range(3, 9):
        for words in combinations_with_replacement(range(8), m):
            bundles = rank2_witness(words, 3)
            assert sorted(e for b in bundles for e in b) == list(range(m))
            assert all(rank2_cost(i, bundles[i], words) <= rank2_cost(i, bundles[j], words)
                       for i in range(3) for j in range(3)), (words, bundles)
            checked += 1
    return {"agents": 3, "chores": [3, 8], "word_multisets_tested": checked,
            "condition": "two loopless parallel classes per agent", "EF_failures": 0}


def key8_random():
    category_sizes = [3, 3, 2]
    allocations = []
    for by_cat in product(*[list(permutations(range(4), k)) for k in category_sizes]):
        flat = sum((list(x) for x in by_cat), [])
        if all(flat.count(i) == 2 for i in range(4)):
            allocations.append([[g for g, j in enumerate(flat) if i == j] for i in range(4)])
    rng = random.Random(20261020)
    for trial in range(1000):
        v = [[rng.randrange(21) for g in range(8)] for i in range(4)]
        def valid(a):
            for i in range(4):
                own = sum(v[i][g] for g in a[i])
                for j in range(4):
                    other = [v[i][g] for g in a[j]]
                    if own < sum(other) - max(other):
                        return False
                    if i < j and own < sum(other):
                        return False
            return True
        assert any(valid(a) for a in allocations), (trial, v)
    return {"agents": 4, "goods": 8, "categories": category_sizes,
            "complete_feasible_allocations": len(allocations),
            "seed": 20261020, "valuation_range_inclusive": [0, 20],
            "random_profiles": 1000, "ordered_no_envy_and_EF1_failures": 0}


if __name__ == '__main__':
    result = {"copies_sd_ef1": copies_exhaustive(),
              "rank2_chore_EF": rank2_exact(),
              "key8": key8_random()}
    out = Path(__file__).with_name('toy_results.json')
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))
