"""Independent ordered-history replay; no repository solver/model imports.

At each literal history, every action has its own complete child menu.
A chosen terminal is supportable iff its current payoff is at least the
largest child-menu minimum. Off-action children can choose their minima
independently. This constructs all supported ordered paths, not one tie rule.
Finite replay only; the universal proof is in the theorem object.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import json


def union(sets):
    return frozenset().union(*sets)


def utilities(sets, path):
    clients = union(sets)
    loads = {x: sum(x in sets[a] for a in path) for x in clients}
    return tuple(sum((F(1, loads[x]) for x in sets[a]), F(0)) for a in path)


def all_paths(sets, n):
    @lru_cache(None)
    def menus(history):
        if len(history) == n:
            return frozenset([history])
        i = len(history)
        children = [menus(history + (a,)) for a in range(len(sets))]
        threshold = max(min(utilities(sets, p)[i] for p in child) for child in children)
        return frozenset(p for child in children for p in child
                         if utilities(sets, p)[i] >= threshold)
    return menus(())


def spectrum(sets, path):
    n = len(path)
    maxima = [B for B in sets if not any(B < T for T in sets)]
    private = [B - union(T for T in maxima if T != B) for B in maxima]
    covered = union(sets[a] for a in path)
    missing = [P - covered for P in private]
    seats = sorted((F(len(Q), k) + F(len(B) - len(Q), n)
                    for B, Q in zip(maxima, missing) for k in range(1, n + 1)),
                   reverse=True)
    return union(private), covered, seats


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for a in range(total + 1):
            for tail in compositions(total - a, length - 1):
                yield (a,) + tail


def audit():
    pairs = paths = checks = corollaries = 0
    for family in range(1, 256):
        sets = tuple(frozenset(x for x in range(3) if mask >> x & 1)
                     for mask in range(8) if family >> mask & 1)
        for n in range(1, 4):
            pairs += 1
            possible = [union(c) for k in range(1, min(n, len(sets)) + 1)
                        for c in combinations(sets, k)]
            optimum = max(map(len, possible))
            optima = [O for O in possible if len(O) == optimum]
            for path in all_paths(sets, n):
                paths += 1
                private, covered, seats = spectrum(sets, path)
                pay = utilities(sets, path)
                assert sum(pay) == len(covered)
                for i in range(n):
                    assert pay[i] >= seats[n - i - 1]
                    checks += 1
                assert len(covered) >= sum(seats[:n])
                if any(O - covered <= private for O in optima):
                    corollaries += 1
                    assert (2*n - 1)*len(covered) >= n*optimum
    sharp = []
    for n in range(1, 7):
        counts = comparisons = 0
        for t in range(n):
            for p in compositions(t, n):
                counts += 1
                value = F(n, p[0] + n - t)
                for a in range(n):
                    other = value if a == 0 else F(1, p[a] + 1)
                    assert value >= other
                    comparisons += 1
        sets = [frozenset(range(n))] + [frozenset([n+j]) for j in range(n-1)]
        _, covered, seats = spectrum(sets, (0,)*n)
        assert len(covered) == n and seats[:n] == [F(1)]*n
        sharp.append(dict(n=n, prefix_count_states=counts, comparisons=comparisons))
    for n in (1, 2, 3, 6):
        _, covered, seats = spectrum([frozenset()], (0,)*n)
        assert not covered and seats == [F(0)]*n
    assert (pairs, paths, checks, corollaries) == (765, 1599, 3660, 1599)
    return dict(status='PASS', implementation='literal ordered-history menus; no repository imports',
                catalog_player_pairs=pairs, all_SPE_ordered_paths=paths,
                position_inequalities_checked=checks, private_missing_corollary_paths=corollaries,
                sharp_all_big=sharp, zero_player_counts=[1, 2, 3, 6],
                scope='finite three-customer replay; does not prove universal theorem')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    result = audit()
    rendered = json.dumps(result, indent=2) + '\n'
    args.output.write_text(rendered)
    print(rendered, end='')
