#!/usr/bin/env python3
"""门槛覆盖的精确成本缩放与共同槽恢复；输入LP见证，不含通用LP求解器。"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import platform

_spec = importlib.util.spec_from_file_location(
    'weighted_group_slots', Path(__file__).with_name('weighted_group_joint_slot.py'))
_slots = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_slots)
Flow = _slots.Flow


def exact(x):
    if isinstance(x, (bool, float)):
        raise ValueError('exact rational required')
    return F(x)


def ceilq(x):
    return -(-x.numerator // x.denominator)


def minimum_cover(weights, demand, eta):
    """Return original job indices, cost, and state cap; exact coverage retained."""
    w = [exact(x) for x in weights]
    d, eta = exact(demand), exact(eta)
    if d < 0 or eta <= 0 or any(x < 0 for x in w):
        raise ValueError('nonnegative weights/demand, positive eta required')
    if d == 0:
        return [], F(0), 0
    if sum(w, F(0)) < d:
        raise ValueError('uncoverable demand')
    candidates = [[j] for j, v in enumerate(w) if v >= d]
    prefix, total = [], F(0)
    for j, v in enumerate(w):
        if v < d:
            prefix.append(j)
            total += v
            if total >= d:
                candidates.append(prefix[:])
                break
    chosen = min(candidates, key=lambda a: (sum((w[j] for j in a), F(0)), a))
    upper = sum((w[j] for j in chosen), F(0))
    # Either a feasible all-small prefix costs <2d, or all covers need a large
    # singleton and the cheapest large singleton is optimal. Thus upper<=2OPT.
    step = eta * upper / (2 * len(w))
    cap = int(upper / step) + len(w)
    scaled = [ceilq(v / step) for v in w]
    # Each layer maps rounded cost to maximum EXACT coverage and its witness.
    # A copied previous layer prevents selecting an item more than once.
    dp = {0: (F(0), ())}
    for j, c in enumerate(scaled):
        nxt = dict(dp)
        for cost, (coverage, ids) in dp.items():
            newcost = cost + c
            if newcost <= cap:
                value = coverage + w[j]
                if newcost not in nxt or value > nxt[newcost][0]:
                    nxt[newcost] = (value, ids + (j,))
        dp = nxt
    cost = min(c for c, (v, _) in dp.items() if v >= d)
    coverage, ids = dp[cost]
    assert coverage == sum((w[j] for j in ids), F(0)) >= d
    return list(ids), coverage, cap


def round_certificate(groups, sink_count, macros, T, delta, tau, eta,
                      macro_flow, receiver_flow):
    """Same group schema as weighted_group_joint_slot.py; returns actual tasks.

    Receiver None is only a zero-demand bypass. Invalid witness => ValueError;
    this is NOT a sound OPT rejection oracle. Macro lower bounds are used by
    the theorem's completeness proof, not by successful witness recovery.
    """
    T, delta, tau, eta = map(exact, (T, delta, tau, eta))
    if T <= 0 or delta < 0 or not F(1, 2) <= tau < 1 or eta <= 0:
        raise ValueError('require T>0, delta>=0, 1/2<=tau<1, eta>0')
    H, B = len(groups), len(macros)
    if (isinstance(sink_count, bool) or not isinstance(sink_count, int)
            or sink_count < 0 or H + sink_count < 1):
        raise ValueError('machine domain')
    weights, eligible, covers, e = [], [], [], []
    for g in groups:
        w = [exact(v) for v in g['weights']]
        E = set(g['eligible'])
        if any(v < 0 or v > delta*T for v in w) or sum(w, F(0)) > T:
            raise ValueError('group weight bounds')
        if any(isinstance(z, bool) or not isinstance(z, int)
               or not 0 <= z < sink_count for z in E):
            raise ValueError('sink domain')
        X, cost, _ = minimum_cover(w, max(F(0), sum(w, F(0))-tau*T), eta)
        weights.append(w); eligible.append(E); covers.append(X); e.append(cost)
    if len(macro_flow) != B or len(receiver_flow) != H:
        raise ValueError('witness dimensions')
    p, a, y = [], [], []
    for row, fr in zip(macros, macro_flow):
        r = {h: exact(v) for h, v in row.items()}
        f = {h: exact(v) for h, v in fr.items()}
        if not r or any(isinstance(h, bool) or not isinstance(h, int)
                        or not 0 <= h < H or v < 0 for h, v in r.items()):
            raise ValueError('macro domain')
        if any(isinstance(h, bool) or not isinstance(h, int) or h not in r or v < 0 or (v and r[h] > T) for h, v in f.items()) or sum(f.values(), F(0)) != 1:
            raise ValueError('macro witness')
        p.append(r); a.append(f)
    for h, row in enumerate(receiver_flow):
        fr = {z: exact(v) for z, v in row.items()}
        occupancy = sum((f.get(h, F(0)) for f in a), F(0))
        if occupancy > 1 or sum(fr.values(), F(0)) != occupancy:
            raise ValueError('home conservation')
        if any(v < 0 or (z is None and e[h] != 0)
               or (z is not None and (isinstance(z, bool) or not isinstance(z, int)
                                      or z not in eligible[h])) for z, v in fr.items()):
            raise ValueError('receiver witness')
        y.append(fr)
    for z in range(sink_count):
        if sum((e[h]*y[h].get(z, F(0)) for h in range(H)), F(0)) > (1+eta)*T:
            raise ValueError('receiver budget')
    net = Flow(); s, t = ('source',), ('target',)
    for b, row in enumerate(a):
        net.add(s, ('b', b), 1)
        for h in sorted(row):
            if row[h]:
                net.add(('b', b), ('hi', h), 1)
    for h in range(H):
        net.add(('hi', h), ('ho', h), 1)
    neighbors = {h: [] for h in range(H)}; slots = set()
    for z in [None] + list(range(sink_count)):
        at = F(0)
        for h in sorted(range(H), key=lambda h: (-e[h], h)):
            right = at + y[h].get(z, F(0))
            for k in range(int(at), ceilq(right)):
                if min(right, F(k+1)) > max(at, F(k)):
                    slot = ('slot', z, k)
                    net.add(('ho', h), slot, 1); neighbors[h].append((z, k))
                    if slot not in slots:
                        slots.add(slot); net.add(slot, t, 1)
            at = right
    if net.maxflow(s, t) != B:
        raise AssertionError('valid rational witness must lift')
    mu = []; occupied = {}
    for b, row in enumerate(a):
        hs = [h for h in sorted(row) if net.used(('b', b), ('hi', h))]
        assert len(hs) == 1
        h = hs[0]; mu.append(h)
        targets = [z for z, k in neighbors[h] if net.used(('ho', h), ('slot', z, k))]
        assert len(targets) == 1 and h not in occupied
        occupied[h] = targets[0]
    home_loads = [F(0)]*H; sink_loads = [F(0)]*sink_count
    for b, h in enumerate(mu):
        home_loads[h] += p[b][h]
    assignments = []
    for h, w in enumerate(weights):
        X = set(covers[h]) if h in occupied else set()
        z = occupied.get(h)
        assert not X or z is not None
        row = [('z', z) if j in X else ('h', h) for j in range(len(w))]
        for j, v in enumerate(w):
            if j in X:
                sink_loads[z] += v
            else:
                home_loads[h] += v
        assignments.append(row)
    assert all(v <= (1+tau)*T for v in home_loads)
    assert all(v <= (1+eta)*(2-tau+delta)*T for v in sink_loads)
    return {'macro_assignment': mu, 'private_assignment': assignments,
            'cover_indices': covers, 'cover_costs': e,
            'home_loads': home_loads, 'sink_loads': sink_loads}


def audit():
    # Independent exhaustive subset oracle for the implemented cover FPTAS.
    cases = 0
    for n in range(6):
        for w in product(range(4), repeat=n):
            for d in range(sum(w)+1):
                optimum = min(sum(w[j] for j in range(n) if mask >> j & 1)
                              for mask in range(1 << n)
                              if sum(w[j] for j in range(n) if mask >> j & 1) >= d)
                for eta in (F(1, 3), F(1)):
                    ids, cost, cap = minimum_cover(w, d, eta)
                    assert len(set(ids)) == len(ids)
                    assert cost == sum((F(w[j]) for j in ids), F(0))
                    assert d <= cost <= (1+eta)*optimum
                    assert cap <= 2*n/eta+n
                    cases += 1
    w = [F(2,5), F(2,5), F(1,5)]
    X, cost, _ = minimum_cover(w, F(1,2), F(1,100))
    assert cost == F(3,5) and sum(w[:2]) == F(4,5) > cost
    # Large singleton must not displace a cheaper all-small cover in the UB.
    assert minimum_cover([6,4,100], 10, F(1,100))[1] == 10
    assert minimum_cover([F(6,10**80), F(4,10**80), F(100,10**80)],
                         F(10,10**80), F(1,100))[1] == F(10,10**80)
    zero = round_certificate([{'weights':[0], 'eligible':[]}], 0,
                             [], 1, 0, F(1,2), F(1,10), [], [{}])
    assert zero['home_loads'] == [0]
    # Two macros circulate fractionally across three homes and two sinks.
    groups = [{'weights':w, 'eligible':[0,1]} for _ in range(3)]
    macros = [{0:F(3,5),1:F(3,5)}, {1:F(3,5),2:F(3,5)}]
    a = [{0:F(1,2),1:F(1,2)}, {1:F(1,2),2:F(1,2)}]
    y = [{0:F(1,4),1:F(1,4)}, {0:F(1,2),1:F(1,2)},
         {0:F(1,4),1:F(1,4)}]
    result = round_certificate(groups, 2, macros, 1, F(2,5), F(1,2), F(1,100), a, y)
    # Independently sum actual ORIGINAL endpoint costs, not returned loads.
    homes = [F(0)]*3; sinks = [F(0)]*2
    for b, h in enumerate(result['macro_assignment']):
        homes[h] += macros[b][h]
    for h, row in enumerate(result['private_assignment']):
        for j, (kind, dest) in enumerate(row):
            if kind == 'h':
                assert dest == h; homes[h] += w[j]
            else:
                assert dest in groups[h]['eligible']; sinks[dest] += w[j]
    assert homes == result['home_loads'] and sinks == result['sink_loads']
    # Integral LP witnesses exposing the old prefix rule's unbounded error.
    prefix_family = []
    for r in (1, 2, 4):
        small = F(1, 10*r); H = 5*r
        ww = [F(1,5)] + [small]*(3*r+1)
        gg = [{'weights':ww, 'eligible':[0]} for _ in range(H)]
        mm = [{h:F(1,2)+small} for h in range(H)]
        aa = [{h:F(1)} for h in range(H)]; yy = [{0:F(1)} for _ in range(H)]
        rr = round_certificate(gg, 1, mm, 1, F(1,5), F(1,2), F(1,100), aa, yy)
        assert rr['sink_loads'] == [F(1,2)]
        assert all(v == 1+small for v in rr['home_loads'])
        # Actual OPT1 witness exports two small jobs/home; macro lower bound
        # and sink total force any schedule below1 to export >2small/home.
        assert H*2*small == 1
        assert F(1,2)+small+sum(ww,F(0))-2*small == 1
        prefix_family.append({'r':r, 'old_prefix_sink_load':str(H*F(1,5)),
                              'repaired_sink_load':str(rr['sink_loads'][0]),
                              'true_opt':'1'})
    invalid = 0
    for args in [([1],2,F(1,10)), ([-1],0,1), ([True],0,1), ([1],0,0)]:
        try:
            minimum_cover(*args)
        except ValueError:
            invalid += 1
        else:
            raise AssertionError('invalid input accepted')
    return {'arithmetic':'fractions.Fraction', 'python':platform.python_version(),
            'cover_oracle_cases':cases, 'invalid_cases':invalid,
            'prefix_counterexample':{'demand':'1/2','cover_cost':str(cost),'prefix_cost':'4/5'},
            'recovery_fixture':result, 'unbounded_prefix_family':prefix_family,
            'scope':'finite subset oracle plus actual LP-witness recovery; no general LP backend',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2, default=str))
