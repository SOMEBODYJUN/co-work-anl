#!/usr/bin/env python3
"""Exact independent audit of the base-profile exchange-distance candidate.

Enumerates every labelled matroid on at most --max-n elements through the
equal-cardinality basis exchange axiom, then every distinct nonempty subset
of its bases as a profile. Repeated bases do not affect the exchange digraph.
No author implementation or linear-representation oracle is imported.
This finite audit is not the general proof and does not certify novelty.
"""
import argparse
from collections import deque
from itertools import combinations
import json
from pathlib import Path
import platform


def masks(n, size):
    return [sum(1 << x for x in xs) for xs in combinations(range(n), size)]


def is_basis_family(bases):
    family = set(bases)
    for a in bases:
        for b in bases:
            for r in range(a.bit_length()):
                if (a & ~b) >> r & 1:
                    if not any((a ^ (1 << r) ^ (1 << s)) in family
                               for s in range(b.bit_length())
                               if (b & ~a) >> s & 1):
                        return False
    return True


def girth(n, bases):
    for size in range(1, n + 1):
        for s in masks(n, size):
            if not any(s & b == s for b in bases):
                return size
    return None


def distances(n, graph, source):
    d = [None] * n
    d[source] = 0
    queue = deque([source])
    while queue:
        a = queue.popleft()
        for b in range(n):
            if graph >> (a * n + b) & 1 and d[b] is None:
                d[b] = d[a] + 1
                queue.append(b)
    return d


def run(max_n):
    totals = dict(matroids=0, profiles=0, distinct_graphs=0, reachable_pairs=0)
    strata = []
    witnesses = {}
    for n in range(max_n + 1):
        for rank in range(n + 1):
            possible = masks(n, rank)
            row = dict(n=n, rank=rank, matroids=0, profiles=0,
                       distinct_graphs=0, reachable_pairs=0)
            for family_bits in range(1, 1 << len(possible)):
                bases = [b for i, b in enumerate(possible) if family_bits >> i & 1]
                if not is_basis_family(bases):
                    continue
                row['matroids'] += 1
                g = girth(n, bases)
                basis_set = set(bases)
                per_base = []
                for b in bases:
                    graph = 0
                    for r in range(n):
                        for s in range(n):
                            if b >> r & 1 and not (b >> s & 1):
                                if (b ^ (1 << r) ^ (1 << s)) in basis_set:
                                    graph |= 1 << (r * n + s)
                    per_base.append(graph)
                unions = [0] * (1 << len(bases))
                graphs = set()
                for subset in range(1, 1 << len(bases)):
                    least = subset & -subset
                    unions[subset] = unions[subset ^ least] | per_base[least.bit_length()-1]
                    graphs.add(unions[subset])
                row['profiles'] += len(unions) - 1
                row['distinct_graphs'] += len(graphs)
                for graph in graphs:
                    for source in range(n):
                        for target, length in enumerate(distances(n, graph, source)):
                            if target == source or length is None:
                                continue
                            row['reachable_pairs'] += 1
                            assert g is not None, (n, rank, bases, 'free matroid has an arc')
                            bound = rank - g + 3
                            assert length <= bound, dict(n=n, rank=rank, girth=g,
                                bases=bases, graph=graph, source=source,
                                target=target, length=length, bound=bound)
                            delta = rank - g
                            key = str(delta)
                            if key not in witnesses or length > witnesses[key]['distance']:
                                witnesses[key] = dict(n=n, rank=rank, girth=g,
                                    bases=bases, graph=graph, source=source,
                                    target=target, distance=length, bound=bound)
            strata.append(row)
            for key in totals:
                totals[key] += row[key]
    return dict(status='all finite cases passed', max_n=max_n,
                arithmetic='integer bitsets; no floating point; exhaustive',
                seed=None, python=platform.python_version(), totals=totals,
                strata=strata, longest_witnesses=witnesses,
                limits='All abstract labelled matroids up to max_n, all subsets of bases. '
                       'Does not prove larger n, game-cost corollaries, or novelty.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--max-n', type=int, default=5)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    if not 0 <= a.max_n <= 5:
        p.error('exact audit bounded to 0 <= max-n <= 5')
    result = run(a.max_n)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        with a.output.open('x') as f:
            f.write(encoded)
    print(json.dumps(result['totals'], sort_keys=True))
