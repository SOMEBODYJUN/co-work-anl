#!/usr/bin/env python3
"""Two actual integer-flow formulations versus exact original scheduling oracles."""
from collections import deque
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class Flow:
    def __init__(self):
        self.g = {}
        self.arcs = []

    def add(self, a, b, cap):
        self.g.setdefault(a, []); self.g.setdefault(b, [])
        e = [b, len(self.g[b]), cap, cap]
        rev = [a, len(self.g[a]), 0, 0]
        self.g[a].append(e); self.g[b].append(rev)
        self.arcs.append((a, e))
        return e

    def run(self, s, t):
        val = 0
        while True:
            prev = {s: None}; q = deque([s])
            while q and t not in prev:
                a = q.popleft()
                for e in self.g[a]:
                    if e[2] and e[0] not in prev:
                        prev[e[0]] = (a, e); q.append(e[0])
            if t not in prev:
                cut = sum(e[3] for a, e in self.arcs if a in prev and e[0] not in prev)
                assert cut == val
                return val, cut
            inc = 10**30; v = t
            while v != s:
                a, e = prev[v]; inc = min(inc, e[2]); v = a
            v = t
            while v != s:
                a, e = prev[v]; e[2] -= inc; self.g[v][e[1]][2] += inc; v = a
            val += inc


def params(c):
    return c['nh'], c['E'], F(c['p']), F(c['u']), F(c['T']), c['H'], c['Z']


def solve(c, outbound):
    nh, E, p, u, T, H, Z = params(c)
    n = sum(nh)
    if H and p > T:
        return None, {'guard': 'frozen macro exceeds T'}
    if u == 0:
        return ['h'] * n, {'zero_quantum': True}
    flow = Flow(); flow.g['s'] = []; flow.g['t'] = []
    edges = []; jobs = [(h, j) for h, n0 in enumerate(nh) for j in range(n0)]
    if outbound:
        r = int((T-p)//u); k = [max(0, n0-r) for n0 in nh]
        need = sum(k)
        for h in range(H): flow.add('s', ('home', h), k[h])
        for a, (h, j) in enumerate(jobs):
            node = ('job', a); flow.add(('home', h), node, 1)
            for z in E[h][j]: edges.append((a, z, flow.add(node, ('sink', z), 1)))
    else:
        need = n
        for a, (h, j) in enumerate(jobs):
            node = ('job', a); flow.add('s', node, 1)
            edges.append((a, 'h', flow.add(node, ('home', h), 1)))
            for z in E[h][j]: edges.append((a, z, flow.add(node, ('sink', z), 1)))
        for h in range(H): flow.add(('home', h), 't', min(n, int((T-p)//u)))
    for z in range(Z): flow.add(('sink', z), 't', min(n, int(T//u)))
    val, cut = flow.run('s', 't')
    if val != need:
        return None, {'flow': val, 'required': need, 'mincut_capacity': cut}
    ds = ['h']*n if outbound else [None]*n
    for a, dest, e in edges:
        if e[3]-e[2]:
            if not outbound: assert ds[a] is None
            ds[a] = dest
    assert all(d is not None for d in ds)
    loads = [p]*H+[F(0)]*Z
    for (h, j), d in zip(jobs, ds):
        assert d == 'h' or d in E[h][j]
        loads[h if d == 'h' else H+d] += u
    assert all(l <= T for l in loads)
    return ds, {'flow': val, 'required': need, 'loads': list(map(str, loads))}


def brute(c, all_macros=False):
    nh, E, p, u, T, H, Z = params(c)
    jobs = [(h, j) for h, n0 in enumerate(nh) for j in range(n0)]
    macro_choices = product(range(H), repeat=H) if all_macros else [tuple(range(H))]
    best = None; feasible = False
    for macros in macro_choices:
        base = [F(0)]*(H+Z)
        for h in macros: base[h] += p
        for ds in product(*[('h', *E[h][j]) for h, j in jobs]):
            loads = base.copy()
            for (h, j), d in zip(jobs, ds): loads[h if d == 'h' else H+d] += u
            peak = max(loads, default=F(0))
            feasible |= peak <= T
            if best is None or peak < best: best = peak
    return feasible, best


def make_case(nh, E, p, u, Z=2):
    return {'nh': list(nh), 'E': E, 'p': str(p), 'u': str(u), 'T': '1', 'H': len(nh), 'Z': Z}


original = json.loads((ROOT/'original-actual-inputs.json').read_text())
stats = {'original_inputs': len(original), 'supplemental_inputs': 0,
         'feasible': 0, 'infeasible': 0, 'mincut_failures': 0,
         'promise_optimum_checks': 0, 'promise_domain_checks': 0}
results = []
def check(c, oracle, origin, idx):
    a, ai = solve(c, False); b, bi = solve(c, True)
    assert (a is not None) == (b is not None) == oracle
    stats['feasible' if oracle else 'infeasible'] += 1
    stats['mincut_failures'] += int(not oracle and 'mincut_capacity' in bi)
    results.append({'origin': origin, 'index': idx, 'all_job_flow': ai, 'outbound_flow': bi})

for i, c in enumerate(original):
    check(c, bool(c['enumerated_feasible_assignments']), 'original-actual-inputs', i)

groups = [tuple()] + [(m,) for m in range(4)] + list(product(range(4), repeat=2))
supp = []
for H in (1, 2):
    for gs in product(groups, repeat=H):
        E = [[[z for z in range(2) if m & (1 << z)] for m in g] for g in gs]
        for p in (F(3, 5), F(4, 5), F(1)):
            for u in (F(1, 5), F(2, 5), F(3, 5)):
                c = make_case([len(g) for g in gs], E, p, u)
                oracle, _ = brute(c)
                check(c, oracle, 'supplemental-inputs', len(supp))
                # First 120 samples explicitly enumerate all macro placements,
                # so the promise comparison does not freeze occupancy in its oracle.
                if stats['promise_domain_checks'] < 120 and H == 2:
                    _, opt = brute(c, all_macros=True)
                    S = sorted({p+k*u for k in range(max(c['nh'], default=0)+1)} |
                               {k*u for k in range(sum(c['nh'])+1)})
                    candidates = [t for t in S if p <= t < 2*p]
                    accepted = []
                    for t in candidates:
                        cc = dict(c, T=str(t))
                        if solve(cc, False)[0] is not None: accepted.append(t)
                    assert bool(accepted) == (opt < 2*p)
                    if accepted:
                        assert min(accepted) == opt
                        stats['promise_optimum_checks'] += 1
                    stats['promise_domain_checks'] += 1
                supp.append(c)

# Explicit degenerate inputs, including an isolated frozen overload guard.
for c in [make_case([], [], F(3, 5), F(2, 5), 0),
          make_case([2], [[[], []]], F(3, 5), F(0), 0),
          make_case([0], [[]], F(2), F(1), 0)]:
    oracle, _ = brute(c)
    check(c, oracle, 'supplemental-inputs', len(supp)); supp.append(c)
stats['supplemental_inputs'] = len(supp)
stats['total_inputs'] = len(original)+len(supp)
stats['all_passed'] = True
stats['limits'] = ['Two real flow formulations, but finite tests only.',
    'No generic rational LP, homogeneous-macro ST or ratio joint-slot backend tested here.',
    'Original oracle enumerates all choices of each sampled matrix; random matrices are not exhaustive.']
(ROOT/'supplemental-inputs.json').write_text(json.dumps(supp, indent=2)+'\n')
(ROOT/'independent-results.json').write_text(json.dumps(results, indent=2)+'\n')
(ROOT/'independent-report.json').write_text(json.dumps(stats, indent=2)+'\n')
print(json.dumps(stats, indent=2))
