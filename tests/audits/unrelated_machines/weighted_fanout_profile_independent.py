#!/usr/bin/env python3
"""独立加权fanout/profile预算与简化树审计：原始helper逻辑依赖内联。

No scratch or normative program is imported.  The weighted construction,
all-blocked-mask optimum oracle, original q-color/two-color tests and
simplified-root tree checks retain their separately developed bodies.
Default stdout is reproducible JSON; --output uses exclusive creation.
The finite oracle belongs to this audit only and is not an algorithmic
input for the weighted constructor.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import lcm
from random import Random
from pathlib import Path
import argparse
import hashlib
import json
import platform

def loads(p, s):
    out = [F(0)] * len(p)
    for j, i in enumerate(s):
        assert p[i][j] is not None
        out[i] += p[i][j]
    return out

def verify_yes(p, s1, s2, T, q):
    first, second = loads(p, s1), loads(p, s2)
    assert all(first[i] + (T if 1 <= i <= q else 0) <= T for i in range(len(p)))
    assert all(second[i] + (T if i == 0 else 0) <= T for i in range(len(p)))
    return first, second

def splice(p, s1, s2, W):
    return [v if u in W and v in W else u for u, v in zip(s1, s2)]

def multi(p, s1, s2, T, q):
    first, _ = verify_yes(p, s1, s2, T, q)
    m, n = len(p), len(s1)
    colors = [None] * m
    for r in range(q):
        colors[r + 1] = r
    flips = []
    for r in range(q - 1):
        while True:
            eligible = [i for i in range(m) if colors[i] is None and
                        q * sum((p[i][j] for j in range(n)
                                 if s1[j] == i and colors[s2[j]] == r), F(0)) >= first[i]]
            if not eligible:
                break
            i = eligible[0]
            colors[i] = r
            flips.append((i, r))
    for i in range(m):
        if colors[i] is None:
            colors[i] = q - 1
    for i in range(m):
        same = sum((p[i][j] for j in range(n)
                    if s1[j] == i and colors[s2[j]] == colors[i]), F(0))
        assert q * same >= first[i]
    W = {i for i in range(m) if colors[i] == colors[0]}
    free = next(i for i in range(1, q + 1) if i in W)
    assert len(W.intersection(range(1, q + 1))) == 1
    sigma = splice(p, s1, s2, W)
    total = loads(p, sigma)
    for i in [0] + [i for i in range(1, q + 1) if i != free]:
        total[i] += T
    assert max(total) <= F(2 * q - 1, q) * T
    return free, total, sigma, flips

def missing(p, s1, s2, T, q, x, y):
    first, _ = verify_yes(p, s1, s2, T, q)
    m, n = len(p), len(s1)
    color = [0] * m
    color[x] = 1
    flips = []
    while True:
        eligible = [i for i in range(m) if i not in (x, y) and color[i] == 0 and
                    2 * sum((p[i][j] for j in range(n)
                             if s1[j] == i and color[s2[j]]), F(0)) >= first[i]]
        if not eligible:
            break
        i = eligible[0]
        color[i] = 1
        flips.append(i)
    W = {i for i in range(m) if color[i] == color[0]}
    blocked = x if x not in W else y
    assert blocked not in W
    sigma = splice(p, s1, s2, W)
    total = loads(p, sigma)
    total[0] += T
    total[blocked] += T
    assert max(total) <= F(3, 2) * T
    return blocked, total, sigma, flips

def exact(p, T, q):
    denom = T.denominator
    for row in p:
        for v in row:
            if v is not None:
                denom = lcm(denom, v.denominator)
    choices = [[(i, int(p[i][j] * denom)) for i in range(len(p))
                if p[i][j] is not None] for j in range(len(p[0]))]
    unit = int(T * denom)
    only = [None] * q
    absent = [None] * q
    count = 0
    for sigma in product(*choices):
        task = [0] * len(p)
        for i, value in sigma:
            task[i] += value
        for b in range(1, q + 1):
            one = max(task[i] + (unit if i == 0 or 1 <= i <= q and i != b else 0)
                      for i in range(len(p)))
            gap = max(task[i] + (unit if i in (0, b) else 0) for i in range(len(p)))
            if only[b - 1] is None or one < only[b - 1]:
                only[b - 1] = one
            if absent[b - 1] is None or gap < absent[b - 1]:
                absent[b - 1] = gap
        count += 1
    return [F(x, denom) for x in only], [F(x, denom) for x in absent], count

def check(p, s1, s2, T, q):
    a = multi(p, s1, s2, T, q)
    b = [missing(p, s1, s2, T, q, x, y)
         for x, y in combinations(range(1, q + 1), 2)]
    only, absent, count = exact(p, T, q)
    assert only[a[0] - 1] <= max(a[1])
    for output in b:
        assert absent[output[0] - 1] <= max(output[1])
    assert sum(v > F(3, 2) * T for v in absent) <= 1
    return only, absent, count

def shapes(q):
    if q == 1:
        return [None]
    return [(left, right) for k in range(1, q)
            for left in shapes(k) for right in shapes(q - k)]

def oracle(p, T, q):
    denom = T.denominator
    for row in p:
        for value in row:
            if value is not None:
                denom = lcm(denom, value.denominator)
    unit = int(T * denom)
    options = [[(i, int(p[i][j] * denom)) for i in range(len(p)) if p[i][j] is not None]
               for j in range(len(p[0]))]
    best = [None] * (1 << q)
    count = 0
    for assignment in product(*options):
        task = [0] * len(p)
        for i, value in assignment:
            task[i] += value
        task[0] += unit
        baseline = max(task)
        for mask in range(1 << q):
            value = max([baseline] + [task[i + 1] + unit for i in range(q) if mask >> i & 1])
            if best[mask] is None or value < best[mask]:
                best[mask] = value
        count += 1
    return [F(x, denom) for x in best], count

def weighted(p, s1, s2, T, q, beta):
    assert len(beta) == q and all(v >= 0 for v in beta) and sum(beta) == 1
    first, _ = verify_yes(p, s1, s2, T, q)
    m, n = len(p), len(s1)
    colors = [None] * m
    for r in range(q):
        colors[r + 1] = r
    for r in range(q - 1):
        while True:
            choices = [i for i in range(m) if colors[i] is None and
                       sum((p[i][j] for j in range(n)
                            if s1[j] == i and colors[s2[j]] == r), F(0)) >= beta[r] * first[i]]
            if not choices:
                break
            colors[choices[0]] = r
    for i in range(m):
        if colors[i] is None:
            colors[i] = q - 1
    for i in range(m):
        same = sum((p[i][j] for j in range(n)
                    if s1[j] == i and colors[s2[j]] == colors[i]), F(0))
        assert same >= beta[colors[i]] * first[i]
    W = {i for i in range(m) if colors[i] == colors[0]}
    free = next(i for i in range(1, q + 1) if i in W)
    assignment = splice(p, s1, s2, W)
    total = loads(p, assignment)
    total[0] += T
    for i in range(1, q + 1):
        if i != free:
            total[i] += T
    assert max(total) <= (2 - beta[free - 1]) * T
    return free, assignment, max(total)

def local_weighted(p, s1, s2, T, q, K, beta):
    order = [0] + list(K) + [i for i in range(1, q + 1) if i not in K] + list(range(q + 1, len(p)))
    inverse = {i: j for j, i in enumerate(order)}
    free, assignment, cost = weighted([p[i] for i in order], [inverse[i] for i in s1],
                                      [inverse[i] for i in s2], T, len(K), beta)
    free = order[free]
    assignment = [order[i] for i in assignment]
    actual = loads(p, assignment)
    actual[0] += T
    for i in K:
        if i != free:
            actual[i] += T
    assert max(actual) == cost
    return free, cost

def weighted_audit():
    rng = Random(202610171654)
    assignments = calls = budget_checks = 0
    for case in range(400):
        q = rng.randrange(2, 7)
        m = q + 1 + rng.randrange(4)
        n = rng.randrange(9)
        T = [F(0), F(1), F(7, 3)][case % 3]
        internal = list(range(q + 1, m))
        s1 = [rng.choice([0] + internal) for _ in range(n)]
        s2 = [rng.choice([i for i in list(range(1, q + 1)) + internal if i != u]) for u in s1]
        p = [[None] * n for _ in range(m)]
        for sigma in (s1, s2):
            for i in range(m):
                js = [j for j in range(n) if sigma[j] == i]
                weights = [rng.randrange(5) for _ in js]
                denom = sum(weights) + rng.randrange(1, 5)
                for j, w in zip(js, weights):
                    p[i][j] = T * F(w, denom)
        if n and case % 7 == 0:
            j = rng.randrange(n)
            extra = [i for i in range(m) if p[i][j] is None]
            if extra:
                p[rng.choice(extra)][j] = F(1, 7)
        best, count = oracle(p, T, q)
        assignments += count
        for k in range(2, q + 1):
            for K in combinations(range(1, q + 1), k):
                states = [sum(1 << (j - 1) for j in K if j != i) for i in K]
                assert sum(best[mask] for mask in states) <= (2 * k - 1) * T
                budget_checks += 1
                weights = [rng.randrange(6) for _ in K]
                if not any(weights):
                    weights[0] = 1
                beta = [F(w, sum(weights)) for w in weights]
                free, cost = local_weighted(p, s1, s2, T, q, K, beta)
                mask = sum(1 << (j - 1) for j in K if j != free)
                assert best[mask] <= cost
                calls += 1
        for i in range(q):
            beta = [F(int(j == i)) for j in range(q)]
            weighted(p, s1, s2, T, q, beta)
            calls += 1
    stars = 0
    for q in range(2, 9):
        for _ in range(20):
            weights = [rng.randrange(5) for _ in range(q)]
            if not any(weights):
                weights[0] = 1
            w = [F(v, sum(weights)) for v in weights]
            p = [[None] * q for _ in range(q + 1)]
            for j in range(q):
                p[0][j], p[j + 1][j] = w[j], F(1)
            best, count = oracle(p, F(1), q)
            assignments += count
            only = [best[((1 << q) - 1) ^ (1 << i)] for i in range(q)]
            assert only == [2 - v for v in w]
            assert sum(only) == 2 * q - 1
            weighted(p, [0] * q, list(range(1, q + 1)), F(1), q, w)
            calls += 1
            stars += 1
    return {'status': 'passed', 'seed': 202610171654, 'random_instances': 400,
            'full_assignments': assignments, 'all_local_K_budget_checks': budget_checks,
            'actual_weighted_constructions': calls, 'weighted_star_budget_equalities': stars,
            'precision': 'exact Fraction / denominator-cleared integer oracle',
            'scope': 'weighted-candidate scratch audit; no canonical or global novelty status'}

def build(tree, q, T):
    next_internal, next_leaf = q + 1, 1
    edges = []

    def visit(t, is_root=False):
        nonlocal next_internal, next_leaf
        if t is None:
            i = next_leaf
            next_leaf += 1
            return i
        if is_root:
            i = 0
        else:
            i = next_internal
            next_internal += 1
        for child in t:
            v = visit(child)
            edges.append((i, v))
        return i

    visit(tree, True)
    assert next_leaf == q + 1 and next_internal == 2 * q - 1
    p = [[None] * len(edges) for _ in range(2 * q - 1)]
    s1, s2 = [], []
    for j, (u, v) in enumerate(edges):
        p[u][j], p[v][j] = T / 2, T
        s1.append(u)
        s2.append(v)
    return p, s1, s2

def simplified_tree_audit():
    count = trees = 0
    for T in (F(0), F(1), F(7, 3)):
        for q in range(2, 7):
            for tree in shapes(q):
                p, s1, s2 = build(tree, q, T)
                _, absent, c = check(p, s1, s2, T, q)
                assert absent == [F(3, 2) * T] * q
                count += c
                trees += 1
    return {'status': 'passed', 'ordered_trees_per_scale': 64,
            'scales': ['0', '1', '7/3'], 'total_instances': trees,
            'full_assignments': count,
            'precision': 'Fraction and exact denominator-cleared integers'}

ORIGINAL_SOURCE_SHA256 = {'multiport_selector_statement_first_probe.py': 'bfdf8fc233659567b8fd5d49c43e5801d406d79638ffff8780722ee0c81c3554', 'multiport_missing_r_statement_probe.py': 'fcbefb15350013a99c1ad40683919991a327ac03cf5d9f21c786b28d0e2d3cd1', 'weighted_multiport_profile_budget_independent_probe.py': '15b7a377ec402e3916540dfac516836b7bf118af2bcc2137e635dfcc80d326a4', 'simple_root_host_tree_independent_probe.py': 'fae587f04302789d169e6aff1a5f18428ed94cc89ac1fe1c2cacd3259fe88e8b'}

def main():
    weighted_result = weighted_audit()
    tree_result = simplified_tree_audit()
    assert weighted_result['random_instances'] == 400
    assert weighted_result['full_assignments'] == 32975
    assert weighted_result['all_local_K_budget_checks'] == 6722
    assert weighted_result['actual_weighted_constructions'] == 8376
    assert weighted_result['weighted_star_budget_equalities'] == 140
    assert tree_result['total_instances'] == 192
    assert tree_result['full_assignments'] == 140844
    return {'status': 'passed', 'weighted_profile_budget': weighted_result,
            'simplified_root_host_tree': tree_result,
            'original_source_sha256': ORIGINAL_SOURCE_SHA256,
            'source_relation': 'function bodies inlined from the four original independent scratch files; entry point only merged',
            'precision': 'exact Fraction and denominator-cleared integer oracles',
            'runtime': {'implementation': platform.python_implementation(),
                        'python_version': platform.python_version()},
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limits': ['finite audits do not prove the general claims',
                       'does not solve unknown YES witnesses or query profile OPT in construction',
                       'no source satisfiability, global hardness or novelty certification']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    options = parser.parse_args()
    payload = json.dumps(main(), indent=2, sort_keys=True) + '\n'
    if options.output is None:
        print(payload, end='')
    else:
        with options.output.open('x') as stream:
            stream.write(payload)
