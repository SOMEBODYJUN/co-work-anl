"""Exact local audit of an odd-perfect-matching compilation into UM.

Research draft only.  This script verifies the stated finite cases, and does
not replace the published arbitrary-degree PSD lemma used by the manuscript.
It is self-contained and imports no canonical scheduling proof code.
"""

from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import lcm
import argparse
import hashlib
import json
import time


def edge(u, v):
    return tuple(sorted((u, v)))


def matching_union(a, b):
    out = tuple(sorted(set(a) | set(b)))
    flat = [v for e in out for v in e]
    return out if len(flat) == len(set(flat)) else None


def poly_add(a, b, factor=F(1)):
    out = defaultdict(F, a)
    for s, w in b.items():
        out[s] += factor * w
    return {s: w for s, w in out.items() if w}


def poly_scale(a, w):
    return {s: c*w for s, c in a.items() if c*w}


def poly_mul(a, b):
    out = defaultdict(F)
    for s, c in a.items():
        for t, w in b.items():
            u = matching_union(s, t)
            if u is not None:
                out[u] += c*w
    return {s: w for s, w in out.items() if w}


ONE = {(): F(1)}


def bit(e):
    return {(e,): F(1)}


def complement(p):
    return poly_add(ONE, p, F(-1))


def all_matchings(n, max_size):
    ans = [()]
    es = list(combinations(range(n), 2))
    for k in range(1, max_size+1):
        ans.extend(s for s in combinations(es, k)
                   if len({v for e in s for v in e}) == 2*k)
    return ans


class OddMatching:
    def __init__(self, n):
        self.n = n

    @lru_cache(None)
    def moment(self, s):
        if matching_union(s, ()) is None:
            return F(0)
        z = F(1)
        for k in range(len(set(s))):
            z /= self.n - 2*k - 1
        return z

    def expect(self, p):
        return sum((w*self.moment(s) for s, w in p.items()), F())


def psd_bareiss(matrix):
    """Exact symmetric fraction-free elimination, checking every tail sign."""
    scale = lcm(*(x.denominator for row in matrix for x in row))
    a = [[int(scale*x) for x in row] for row in matrix]
    dim = len(a)
    prev = 1
    largest_bits = 0
    for k in range(dim):
        neg = next((r for r in range(k, dim) if a[r][r] < 0), None)
        if neg is not None:
            return {'psd': False, 'stage': k, 'negative_row': neg,
                    'value': str(a[neg][neg]), 'dimension': dim}
        p = next((r for r in range(k, dim) if a[r][r]), None)
        if p is None:
            bad = next(((r, c) for r in range(k, dim)
                        for c in range(r, dim) if a[r][c]), None)
            return {'psd': bad is None, 'rank': k, 'dimension': dim,
                    'integer_scale': scale, 'zero_tail_nonzero': bad,
                    'largest_pivot_bits': largest_bits}
        if p != k:
            a[k], a[p] = a[p], a[k]
            for row in a:
                row[k], row[p] = row[p], row[k]
        pivot = a[k][k]
        largest_bits = max(largest_bits, pivot.bit_length())
        for r in range(k+1, dim):
            ark = a[r][k]
            for c in range(r, dim):
                numerator = pivot*a[r][c]-ark*a[k][c]
                assert numerator % prev == 0
                a[r][c] = a[c][r] = numerator//prev
        for r in range(k+1, dim):
            a[r][k] = a[k][r] = 0
        prev = pivot
    return {'psd': True, 'rank': dim, 'dimension': dim,
            'integer_scale': scale, 'largest_pivot_bits': largest_bits}


def build(n):
    """Return sparse P, affine assignment substitution, and true row laws."""
    es = list(combinations(range(n), 2))
    neighbors = {v: [u for u in range(n) if u != v] for v in range(n)}
    pos = {(v, u): a for v, ns in neighbors.items()
           for a, u in enumerate(ns)}
    machines = [('L', e) for e in es] + [('R', e) for e in es]
    machines += [('A', v) for v in range(n)]
    machines += [('B', v, k) for v in range(n) for k in range(n-2)]
    jobs = {}
    substitution = {}

    def add(j, i, p, polynomial):
        jobs.setdefault(j, {})[i] = F(p)
        substitution[i, j] = polynomial

    for e in es:
        z = bit(e)
        add(('a', e), ('L', e), 1, z)
        add(('a', e), ('R', e), 1, complement(z))
        for v in e:
            u = next(w for w in e if w != v)
            a = pos[v, u]
            add(('b', e, v), ('L', e), F(1, 2), complement(z))
            add(('b', e, v), ('A', v), 1, z)
            add(('c', e, v), ('R', e), F(1, 2), z)
            if a > 0:
                polynomial = {}
                for w in neighbors[v][:a]:
                    polynomial = poly_add(polynomial, bit(edge(v, w)))
                add(('c', e, v), ('B', v, a-1), 1, polynomial)
            if a < n-2:
                polynomial = {}
                for w in neighbors[v][a+1:]:
                    polynomial = poly_add(polynomial, bit(edge(v, w)))
                add(('c', e, v), ('B', v, a), 1, polynomial)

    rows = {i: [j for j in jobs if i in jobs[j]] for i in machines}
    laws = {}
    p = F(1, n-1)
    for e in es:
        laws['L', e] = [(p, frozenset([('a', e)])),
                        (1-p, frozenset(('b', e, v) for v in e))]
        laws['R', e] = [(1-p, frozenset([('a', e)])),
                        (p, frozenset(('c', e, v) for v in e))]
    for v in range(n):
        laws['A', v] = [(p, frozenset([('b', edge(v, u), v)]))
                         for u in neighbors[v]]
        for k in range(n-2):
            # When selected neighbor has index b, removing it shifts positions.
            law = defaultdict(F)
            for b in range(n-1):
                a = k if k < b else k+1
                j = ('c', edge(v, neighbors[v][a]), v)
                law[frozenset([j])] += p
            laws['B', v, k] = [(w, s) for s, w in law.items()]
    return machines, jobs, substitution, rows, laws, neighbors, pos


def schedule_three_halves(n, jobs, neighbors, pos):
    matched_edges = {edge(v, v+1) for v in range(0, n-1, 2)}
    mate = {v: w for e in matched_edges for v in e for w in e if w != v}
    root = n-1
    exceptional_neighbor = 0
    selected_at = dict(mate, **{})
    selected_at[root] = exceptional_neighbor
    sigma = {}
    for e in combinations(range(n), 2):
        selected = e in matched_edges
        sigma['a', e] = ('L' if selected else 'R', e)
        for v in e:
            u = next(w for w in e if w != v)
            sigma['b', e, v] = ('A', v) if selected else ('L', e)
            if selected or (v == root and u == exceptional_neighbor):
                sigma['c', e, v] = ('R', e)
            else:
                a = pos[v, u]
                b = pos[v, selected_at[v]]
                assert a != b
                sigma['c', e, v] = ('B', v, a if a < b else a-1)
    load = defaultdict(F)
    for j, i in sigma.items():
        assert i in jobs[j]
        load[i] += jobs[j][i]
    assert len(sigma) == len(jobs)
    assert max(load.values()) == F(3, 2)
    return {'makespan': str(max(load.values())),
            'over_one_rows': sum(w > 1 for w in load.values())}


def feasibility_oracle(jobs, cap):
    order = sorted(jobs, key=lambda j: (len(jobs[j]),
                   -max(jobs[j].values()), str(j)))
    load = defaultdict(F)
    nodes = 0

    def rec(k):
        nonlocal nodes
        nodes += 1
        if k == len(order):
            return True
        j = order[k]
        for i, p in jobs[j].items():
            if load[i]+p <= cap:
                load[i] += p
                if rec(k+1):
                    return True
                load[i] -= p
        return False

    return {'feasible': rec(0), 'search_nodes': nodes}


def finite_audit(n=9, run_psd=True):
    started = time.monotonic()
    assert n % 2 and n >= 9
    om = OddMatching(n)
    basis = all_matchings(n, 2)
    psd = None
    if run_psd:
        gram = []
        for s in basis:
            row = []
            for t in basis:
                u = matching_union(s, t)
                row.append(om.moment(u) if u is not None else F())
            gram.append(row)
        psd = psd_bareiss(gram)
        assert psd['psd']

    ms, jobs, sub, rows, laws, ns, pos = build(n)
    expected = {'machines': 2*n*(n-1), 'jobs': 5*n*(n-1)//2,
                'finite_edges': 6*n*n-8*n}
    assert len(ms) == expected['machines']
    assert len(jobs) == expected['jobs']
    assert len(sub) == expected['finite_edges']
    assert max(map(len, jobs.values())) <= 3

    # Base moment recurrence proves all vertex equations through cubic tests.
    recurrence_tests = 0
    for s in all_matchings(n, 3):
        for v in range(n):
            val = F()
            for u in ns[v]:
                z = matching_union(s, (edge(v, u),))
                if z is not None:
                    val += om.moment(z)
            assert val == om.moment(s)
            recurrence_tests += 1

    # Each assignment choice is a subset of one perfect-matching star, or a
    # complement of a single bit, so Boolean/one-hot follow from that recurrence.
    for j, allowed in jobs.items():
        summation = {}
        for i in allowed:
            summation = poly_add(summation, sub[i, j])
        assert om.expect(summation) == 1
        for i in allowed:
            f = sub[i, j]
            assert om.expect(poly_mul(f, f)) == om.expect(f)
        for i, h in combinations(allowed, 2):
            assert not poly_mul(sub[i, j], sub[h, j])

    local_checks = 0
    for i, rjobs in rows.items():
        law = laws[i]
        assert sum(w for w, s in law) == 1
        assert all(sum(jobs[j][i] for j in s) <= 1 for w, s in law)
        for k in range(min(4, len(rjobs))+1):
            for js in combinations(rjobs, k):
                polynomial = ONE
                for j in js:
                    polynomial = poly_mul(polynomial, sub[i, j])
                target = sum((w for w, s in law if set(js) <= s), F())
                assert om.expect(polynomial) == target
                local_checks += 1
        load = {}
        for j in rjobs:
            load = poly_add(load, sub[i, j], jobs[j][i])
        # Localizer is exactly zero against every matching monomial of degree≤3.
        residual = poly_add(ONE, load, F(-1))
        for s in all_matchings(n, 3):
            assert om.expect(poly_mul(residual, {s: F(1)})) == 0

    schedule = schedule_three_halves(n, jobs, ns, pos)
    _, jobs3, _, _, _, ns3, pos3 = build(3)
    tiny = {'n': 3, 'cap_1': feasibility_oracle(jobs3, F(1)),
            'cap_3_2': feasibility_oracle(jobs3, F(3, 2)),
            'explicit': schedule_three_halves(3, jobs3, ns3, pos3)}
    assert not tiny['cap_1']['feasible'] and tiny['cap_3_2']['feasible']
    return {'N': n, **expected, 'max_job_options': 3,
            'base_matching_M2': psd,
            'vertex_recurrence_checks': recurrence_tests,
            'all_row_subsets_degree_le_4_checks': local_checks,
            'all_localizers_exact_zero': True,
            'explicit_schedule': schedule, 'small_integer_oracle': tiny,
            'seconds': round(time.monotonic()-started, 3)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--N', type=int, default=9)
    ap.add_argument('--skip-psd', action='store_true')
    args = ap.parse_args()
    out = finite_audit(args.N, not args.skip_psd)
    out['script_sha256'] = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()
    print(json.dumps(out, indent=2))
