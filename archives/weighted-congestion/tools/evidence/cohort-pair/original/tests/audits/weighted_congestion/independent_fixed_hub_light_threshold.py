"""Independent literal audit of fixed-hub, one-light-per-side response games.

This scratch program does not import the candidate implementation. Thresholds
are reconstructed from literal resource-cost comparisons and the potential is
implemented as pair interactions plus one-player offsets.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import random
import sys


def sign(x):
    return (x > 0) - (x < 0)


def value(c, x):
    ans = Q(0)
    for a in reversed(c):
        ans = ans*x + a
    return ans


def audit(hubw, hubbits, lightw, source, mains, sides):
    nh, nl = len(hubw), len(lightw)
    weights = tuple(hubw) + tuple(lightw)
    coeffs = []
    strategies = [[set(), set()] for _ in weights]
    for v, c in enumerate(mains):
        for b in (0, 1):
            r = len(coeffs)
            coeffs.append(c)
            strategies[v][b].add(r)
            for i, src in enumerate(source):
                if src == v:
                    strategies[nh+i][b].add(r)
    for i, hubs, c in sides:
        for b in (0, 1):
            r = len(coeffs)
            coeffs.append(c)
            strategies[nh+i][1-b].add(r)
            for v in hubs:
                strategies[v][b].add(r)

    states = tuple(product((0, 1), repeat=nl))
    cost = {}
    for s in states:
        bits = tuple(hubbits) + s
        loads = [Q(0) for _ in coeffs]
        for p, b in enumerate(bits):
            for r in strategies[p][b]:
                loads[r] += weights[p]
        cost[s] = tuple(sum((value(coeffs[r], loads[r])
                             for r in strategies[nh+i][s[i]]), Q(0))
                        for i in range(nl))

    groups = tuple(tuple(i for i in range(nl) if source[i] == v)
                   for v in range(nh))
    thresholds, flat_delta, comparison_rows = {}, {}, []
    tie_rows = 0
    domination = {'always_0': 0, 'always_1': 0}
    for v, group in enumerate(groups):
        for i in group:
            samples = {}
            for s in states:
                s0, s1 = list(s), list(s)
                s0[i], s1[i] = hubbits[v], 1-hubbits[v]
                x = sum((lightw[j] for j in group if j != i
                         and s[j] == hubbits[v]), Q(0))
                d = cost[tuple(s0)][i] - cost[tuple(s1)][i]
                assert x not in samples or samples[x] == d
                samples[x] = d
            ordered = sorted(samples)
            if any(mains[v][1:]):
                assert all(samples[a] < samples[b]
                           for a, b in zip(ordered, ordered[1:]))
                zero = [x for x in ordered if samples[x] == 0]
                lower = [x for x in ordered if samples[x] < 0]
                upper = [x for x in ordered if samples[x] > 0]
                if zero:
                    assert len(zero) == 1
                    t = zero[0]
                elif lower and upper:
                    t = (max(lower)+min(upper))/2
                elif lower:
                    t = max(ordered)+Q(1, 3)
                    domination['always_0'] += 1
                else:
                    t = min(ordered)-Q(1, 3)
                    domination['always_1'] += 1
                assert all(sign(samples[x]) == sign(x-t) for x in ordered)
                thresholds[i] = t
            else:
                assert len(set(samples.values())) == 1
                flat_delta[i] = samples[ordered[0]]
            tie_rows += sum(samples[x] == 0 for x in ordered)
            comparison_rows.extend((i, x, samples[x]) for x in ordered)

    def potential(s):
        energy = Q(0)
        for v, group in enumerate(groups):
            chosen = [i for i in group if s[i] == hubbits[v]]
            if any(mains[v][1:]):
                energy += sum((lightw[i]*lightw[j]
                               for i, j in combinations(chosen, 2)), Q(0))
                energy -= sum((lightw[i]*thresholds[i] for i in chosen), Q(0))
            else:
                energy += sum((flat_delta[i] for i in chosen), Q(0))
        return energy

    energy = {s: potential(s) for s in states}
    graph = {s: [] for s in states}
    indegree = dict.fromkeys(states, 0)
    equilibria, localmin = [], []
    tie_edges = strict_edges = 0
    for s in states:
        stable = minimal = True
        for i in range(nl):
            t = tuple(1-b if j == i else b for j, b in enumerate(s))
            dc, de = cost[t][i]-cost[s][i], energy[t]-energy[s]
            assert sign(dc) == sign(de), (s, i, dc, de)
            if dc == 0:
                tie_edges += 1
            if de < 0:
                minimal = False
            if dc < 0:
                stable = False
                strict_edges += 1
                graph[s].append(t)
                indegree[t] += 1
        if stable:
            equilibria.append(s)
        if minimal:
            localmin.append(s)
    assert equilibria == localmin and equilibria
    sweep_moves = []
    for reverse_ties in (False, True):
        s = tuple(hubbits[source[i]] for i in range(nl))
        moves = 0
        for v, group in enumerate(groups):
            if any(mains[v][1:]):
                order = sorted(group, key=lambda i: (thresholds[i], -i if reverse_ties else i))
                for i in order:
                    load = sum((lightw[j] for j in group if s[j] == hubbits[v]), Q(0))
                    if load-lightw[i] > thresholds[i]:
                        t = tuple(1-b if j == i else b for j, b in enumerate(s))
                        assert cost[t][i] < cost[s][i]
                        s, moves = t, moves+1
            else:
                for i in group:
                    if flat_delta[i] > 0:
                        t = tuple(1-b if j == i else b for j, b in enumerate(s))
                        assert cost[t][i] < cost[s][i]
                        s, moves = t, moves+1
        assert moves <= nl and s in equilibria
        sweep_moves.append(moves)
    queue = [s for s in states if indegree[s] == 0]
    seen = 0
    while queue:
        s = queue.pop()
        seen += 1
        for t in graph[s]:
            indegree[t] -= 1
            if indegree[t] == 0:
                queue.append(t)
    assert seen == len(states), 'strict light improvement cycle'
    return {'states': len(states), 'strict_edges': strict_edges,
            'tie_edges': tie_edges, 'pne': len(equilibria),
            'tie_threshold_samples': tie_rows,
            'two_sweeps_moves': sum(sweep_moves), **domination}


def multi_light_boundary():
    # Literal pair resources: each light uses exactly the opposite bit copy.
    # The extra fixed source hub has zero-fee mains and no side participation.
    weights = (Q(1), Q(2), Q(3))
    pairs = ((0, 1, Q(2100)), (0, 2, Q(1130)), (1, 2, Q(499)))
    def costs(bits):
        load = {(e, b): Q(0) for e in range(3) for b in (0, 1)}
        for e, (i, j, _) in enumerate(pairs):
            for p in (i, j):
                load[e, 1-bits[p]] += weights[p]
        out = [Q(0)]*3
        for e, (i, j, a) in enumerate(pairs):
            for p in (i, j):
                out[p] += a*load[e, 1-bits[p]]**2
        return out
    rows = []
    factors = []
    for s in product((0, 1), repeat=3):
        c = costs(s)
        arrivals = [costs(tuple(1-b if j == i else b
                               for j, b in enumerate(s)))[i] for i in range(3)]
        factors.append(max([Q(1)]+[a/b for a, b in zip(c, arrivals)]))
        assert any(a > b for a, b in zip(c, arrivals))
        rows.append({'state': s, 'costs': c, 'deviation_costs': arrivals,
                     'factor': factors[-1]})
    assert min(factors) == Q(20896, 20875)
    return {'weights': weights, 'pairs': pairs, 'hub_weight': Q(1),
            'main_coefficients': [Q(0)], 'best_factor': min(factors),
            'states': rows}


def main():
    seed = 930411
    rng = random.Random(seed)
    cases = []
    # Empty lights, zero/flat mains, all-tie and action-dependent side fees.
    for basebit in (0, 1):
        for f in ([Q(0)], [Q(7)], [Q(0), Q(1)], [Q(2), Q(0), Q(1)]):
            for ws in ([], [Q(1)], [Q(1), Q(1)], [Q(1, 11), Q(2, 3), Q(13)]):
                cases.append(([Q(1)], [basebit], ws, [0]*len(ws), [f], []))
                if ws:
                    cases.append(([Q(1)], [basebit], ws, [0]*len(ws), [f],
                                  [(0, [0], [Q(0), Q(1)]),
                                   (0, [], [Q(3)]),
                                   (len(ws)-1, [0], [Q(0), Q(20)])]))
    # Exact endpoint and interior ties, with duplicate reachable subset weights.
    cases += [([Q(1)], [0], [Q(1)]*n, [0]*n, [[Q(0), Q(1)]], sides)
              for n, sides in ((1, []), (2, []),
                               (2, [(0, [0], [Q(0), Q(2)])]),
                               (3, [(0, [0], [Q(0), Q(1)])]),
                               (4, []))]
    # Every fixed hub vector is audited. No source coupling via another light.
    for _ in range(90):
        nh, nl = rng.randint(1, 3), rng.randint(0, 6)
        hw = [Q(rng.randint(1, 13), rng.randint(1, 5)) for _ in range(nh)]
        lw = [Q(rng.randint(1, 9), rng.randint(1, 8)) for _ in range(nl)]
        src = [rng.randrange(nh) for _ in range(nl)]
        fs = [[Q(rng.randrange(4), rng.randint(1, 5))
               for _ in range(rng.randint(1, 5))] for _ in range(nh)]
        sides = [(rng.randrange(nl), [v for v in range(nh) if rng.randrange(2)],
                  [Q(rng.randrange(5), rng.randint(1, 7))
                   for _ in range(rng.randint(1, 5))])
                 for _ in range(rng.randint(0, 8))] if nl else []
        for hb in product((0, 1), repeat=nh):
            cases.append((hw, hb, lw, src, fs, sides))
    rows = [audit(*case) for case in cases]
    frozen = Path(__file__).resolve().parents[3] / 'research/current/weighted_congestion/fixed_hub_light_threshold_response.md'
    print(json.dumps({'status': 'passed', 'seed': seed, 'arithmetic': 'Fraction',
                      'python': sys.version, 'instances': len(rows),
                      'totals': {k: sum(r[k] for r in rows) for k in rows[0]},
                      'max_hubs': 3, 'max_lights': 6, 'max_degree': 4,
                      'scope': 'all states, all literal light deviations, full sign equivalence and improvement DAG',
                      'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'canonical_sha256': hashlib.sha256(frozen.read_bytes()).hexdigest(),
                      'multi_light_boundary': multi_light_boundary(),
                      'inputs': cases}, default=str, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
