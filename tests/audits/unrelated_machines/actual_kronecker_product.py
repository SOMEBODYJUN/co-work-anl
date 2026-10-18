"""Exact complete-matrix counterexample audit; no optimizer is imported.

Rebuilds all base/square finite edges, checks two different stored certificates,
reconstructs the formula plus fifteen simultaneous replacements, and checks its
fourth-power tensor schedule.  The LP identity has a separate analytic proof.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
import platform

ROOT = Path(__file__).resolve().parents[3]
M = [('S', g, l) for g, l in product(range(2), repeat=2)] + [('R', a, b) for a, b in product(range(2), repeat=2)]
J = [('A', g) for g in range(2)] + [('B', g, l, a) for g, l, a in product(range(2), repeat=3)]


def time(i, j):
    m, q = M[i], J[j]
    if q[0] == 'A':
        return F(1) if m[0] == 'S' and m[1] == q[1] else None
    _, g, l, a = q
    if m == ('S', g, l):
        return F(1, 2)
    return F(1) if m == ('R', a, l ^ (g * a)) else None


def start(j, k):
    q, z = J[j], J[k]
    if q[0] == z[0] == 'A':
        return M.index(('S', q[1], z[1])), M.index(('S', z[1], q[1]))
    if q[0] == 'A':
        _, h, l, a = z
        return M.index(('S', q[1], h)), M.index(('R', a, l ^ (h * a)))
    if z[0] == 'A':
        _, g, l, a = q
        return M.index(('R', a, l ^ (g * a))), M.index(('S', z[1], g))
    _, g, l, a = q
    _, h, k0, c = z
    if l == h and k0 == g:
        return M.index(('R', a, l ^ (g * a))), M.index(('R', c, k0 ^ (h * c)))
    return M.index(('S', g, l)), M.index(('S', h, k0))


CHANGES = {(0, 7): (0, 2), (2, 1): (0, 3), (2, 6): (4, 2), (2, 7): (4, 2), (2, 8): (4, 3), (3, 9): (6, 3), (4, 7): (1, 7), (5, 7): (1, 7), (6, 1): (2, 3), (6, 8): (4, 3), (7, 9): (7, 6), (8, 7): (5, 7), (9, 1): (3, 2), (9, 7): (6, 7), (9, 9): (6, 3)}


def verify_square(assignment):
    assert len(assignment) == 100
    assert all(type(i) is int and 0 <= i < 64 for i in assignment)
    loads = [F(0)] * 64
    for z, (j, k) in enumerate(product(range(10), repeat=2)):
        i, h = divmod(assignment[z], 8)
        a, b = time(i, j), time(h, k)
        assert a is not None and b is not None
        loads[assignment[z]] += a * b
    assert loads == [F(1)] * 64
    return loads


def run():
    inp_path = ROOT / 'examples/unrelated_machines/actual_kronecker_square_input.json'
    cert_paths = [ROOT / ('evidence/certificates/unrelated_machines/' + name) for name in ['actual_kronecker_square_assignment.json', 'actual_kronecker_square_independent_assignment.json']]
    inp = json.loads(inp_path.read_text())
    assert inp['machines'] == [list(v) for v in product(range(8), repeat=2)]
    assert inp['jobs'] == [list(v) for v in product(range(10), repeat=2)]
    edges = []
    for j, k in product(range(10), repeat=2):
        e = {}
        for i, h in product(range(8), repeat=2):
            a, b = time(i, j), time(h, k)
            if a is not None and b is not None:
                e[8 * i + h] = a * b
        edges.append(e)
    assert sum(map(len, edges)) == 400
    assert len(inp['finite_edges']) == 100
    for row in inp['finite_edges']:
        assert len(row) == 4
        ids = [i for i, _ in row]
        assert all(type(i) is int and 0 <= i < 64 for i in ids)
        assert len(set(ids)) == 4
    assert [{i: F(v) for i, v in e} for e in inp['finite_edges']] == edges
    seed_options = [[i for i in range(8) if time(i, j) is not None] for j in range(10)]
    best = None
    for ass in product(*seed_options):
        load = [F(0)] * 8
        for j, i in enumerate(ass):
            load[i] += time(i, j)
        peak = max(load)
        best = peak if best is None else min(best, peak)
    assert best == F(3, 2)
    distinct = []
    for p in cert_paths:
        cert = json.loads(p.read_text())
        raw = cert['assignment']
        assert len(raw) == 100
        if raw and isinstance(raw[0], dict):
            expected_jobs = [('f', q[1]) if q[0] == 'A' else ('e',) + q[1:] for q in J]
            assert cert['seed_machines'] == [list(v) for v in M]
            assert cert['seed_jobs'] == [list(v) for v in expected_jobs]
            ass = []
            for z, (j, k) in enumerate(product(range(10), repeat=2)):
                row = raw[z]
                assert row['job'] == [list(expected_jobs[j]), list(expected_jobs[k])]
                i, h = [M.index(tuple(v)) for v in row['machine']]
                assert F(row['p']) == time(i, j) * time(h, k)
                ass.append(8 * i + h)
            assert cert['loads'] == [{'machine': [list(M[i]), list(M[h])], 'load': '1'} for i, h in product(range(8), repeat=2)]
        else:
            ass = raw
            assert cert['loads'] == ['1'] * 64
        verify_square(ass)
        distinct.append(ass)
    assert distinct[0] != distinct[1]
    before = defaultdict(F)
    assignment = []
    changed = 0
    for j, k in product(range(10), repeat=2):
        old = start(j, k)
        before[old] += time(old[0], j) * time(old[1], k)
        new = CHANGES.get((j, k), old)
        assignment.append(8 * new[0] + new[1])
        changed += int(new != old)
    defects = {(6, 6): F(2), (7, 7): F(2), (6, 7): F(0), (7, 6): F(0)}
    assert all(before[m] == defects.get(m, F(1)) for m in product(range(8), repeat=2))
    assert changed == 15
    loads = verify_square(assignment)
    fourth = defaultdict(F)
    for z, w in product(range(100), repeat=2):
        j, k = divmod(z, 10)
        q, r = divmod(w, 10)
        i, h = divmod(assignment[z], 8)
        a, b = divmod(assignment[w], 8)
        fourth[64 * assignment[z] + assignment[w]] += time(i, j) * time(h, k) * time(a, q) * time(b, r)
    assert len(fourth) == 4096 and set(fourth.values()) == {F(1)}
    dual = [F(1, 6)] * 4 + [F(1, 12)] * 4
    assert sum(dual) == 1
    fractional_loads = [F(0)] * 8
    for j, options in enumerate(seed_options):
        assert len(options) == 2
        for i in options:
            fractional_loads[i] += F(1, 2) * time(i, j)
    assert fractional_loads == [F(1)] * 8
    assert sum(min(dual[i] * time(i, j) for i in seed_options[j]) for j in range(10)) == 1
    return {'status': 'passed', 'arithmetic': 'fractions.Fraction', 'python': platform.python_version(), 'seed_assignments_enumerated': 1024, 'seed_optimum': str(best), 'square_machines': 64, 'square_jobs': 100, 'square_finite_edges': 400, 'stored_certificates_checked': 2, 'simultaneous_changes': changed, 'all_square_loads': '1', 'fourth_power_jobs_checked': 10000, 'fourth_power_machines_checked': 4096, 'all_fourth_power_loads': '1', 'seed_unpruned_lp_primal_dual_value': '1', 'limitations': ['Finite certificate verification is distinct from the analytic all-even-power proof.', 'No generic LP solver, hardness reduction, odd powers, or general seed behavior checked.'], 'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), inp_path] + cert_paths}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite frozen output')
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['sha256', 'limitations']}, ensure_ascii=False))
