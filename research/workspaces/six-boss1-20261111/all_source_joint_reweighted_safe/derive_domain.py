#!/usr/bin/env python3
"""Exact local-domain derivation. Standard library only; no optimizer or imports of project code.

Writes only this package. Reconstructs the genuine branch shares, all affine
residuals, facet-intersection vertices, and all exact minimum/attainment data.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
WS = OUT.parent
PINS = {
    'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md': 'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88',
    'research/workspaces/six-boss1-20261111/main_all_source25_family/proof.md': 'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
    'research/workspaces/six-boss1-20261111/main_all_source25_family/exact_family.json': '8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0',
    'research/workspaces/six-boss1-20261111/source2_joint_internal_safe/freeze_manifest.json': 'ec51f3eff143d0f555d2601deb1954a06f249aecbd4eabcfab3398d2c45d7b25',
    'research/workspaces/six-boss1-20261111/source2_joint_internal_safe/proof.md': 'e4ba6dd0e4cde35a9c899d35e85c53a98a042b257e6bb14a01078726138210e4',
    'research/workspaces/six-boss1-20261111/source2_joint_internal_safe/sixteen_reweighted_vertex_family.json': 'a38144bb000e8585d520a731ed4159269a7245e0616d020ca12550d55df3719e',
    'research/workspaces/six-boss1-20261111/visible_maximum_joint_v2/exact_input.json': '0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4',
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def stringlist(xs):
    return [str(x) for x in xs]

def protect_sources():
    for path, expected in PINS.items():
        assert digest(REPO / path) == expected, path
    old_path = WS / 'source2_joint_internal_safe/freeze_manifest.json'
    old = json.loads(old_path.read_text())
    protected = dict(old['prior_frozen_artifact_sha256'])
    protected.update({p: a['sha256'] for p, a in old['artifacts'].items()})
    protected[str(old_path.relative_to(REPO))] = digest(old_path)
    sums = WS / 'source2_joint_internal_safe/SHA256SUMS'
    protected[str(sums.relative_to(REPO))] = digest(sums)
    assert len(protected) == 105
    for path, expected in protected.items():
        assert digest(REPO / path) == expected, path
    dump('source_manifest.json', {
        'source_sha256': PINS,
        'prior_frozen_artifact_sha256': protected,
        'prior_frozen_artifacts_checked': len(protected),
        'optimizer_calls': 0,
        'other_project_programs_executed_or_imported': False,
    })

def genuine_cost(i, p, t, o, r, theta, s, menu_count=None):
    """Sum customer contributions from the true IC/caps/terminal/SAFE wallet."""
    n = 6 - i
    assert len(r) == n and len(theta) == n - 1
    load = p + t + sum(r)
    a = F(25) + sum(theta) - s
    vi = F(t, load) if load else F(0)
    v6 = F(r[-1], load) if load else F(0)
    answer = a * vi + F(sum(r[:-1]), 2) + r[-1] - v6
    d = o if menu_count is None else menu_count
    answer += F(d, 6 * (p + t + sum(r[:-1]) + 1))
    for k, j in enumerate(range(i + 1, 6)):
        vj = F(r[k], load) if load else F(0)
        safe = F(d, 6 * (p + t + sum(r[:k]) + 7 - j))
        answer += theta[k] * (safe - vj)
    return answer

def target(i, p, t, o, theta, s):
    n = 6 - i
    D = p + n + 1
    answer = F(n + 1, 2) * t + F(24 * t, D) + F(o, 6 * (p + 1 + n * t))
    answer -= s * F(t, min(D, 5))
    for w, j in zip(theta, range(i + 1, 6)):
        answer += w * F(o, 6 * (p + (j - i) * t + 7 - j))
    return answer

def raw_states(i):
    for p in range(i):
        for t, o in product((0, 1), repeat=2):
            for r in product((0, 1), repeat=6-i):
                yield p, t, o, r

def state_name(i, p, t, o, r):
    return f'I{i}_p{p}_t{t}_o{o}_r' + ''.join(map(str, r))

def halfspace(i, state):
    p, t, o, r = state
    m = 5 - i
    zero = [F(0)] * m
    base = genuine_cost(i, p, t, o, r, zero, F(0)) - target(i, p, t, o, zero, F(0))
    coeff = []
    for k in range(m + 1):
        v = [F(j == k) for j in range(m + 1)]
        delta = genuine_cost(i, p, t, o, r, v[:-1], v[-1]) - target(i, p, t, o, v[:-1], v[-1])
        coeff.append(delta - base)
    return base, coeff

def facets(i):
    js = list(range(i + 1, 6))
    dim = len(js) + 1
    ans = []
    for k, j in enumerate(js):
        v = [F(0)] * dim
        v[k] = F(1)
        ans.append((f'theta{j}_nonnegative', F(0), v))
        v = [F(0)] * dim
        v[k] = F(-1)
        for h in range(k + 1, len(js)):
            ell = js[h]
            v[h] = -F(1, 6 * (7 - ell) * (8 - ell))
        ans.append((f'theta{j}_cap', F(5, 12), v))
    v = [F(0)] * dim
    v[-1] = F(1)
    ans.append(('s_nonnegative', F(0), v))
    if i == 1:
        for k, j in enumerate(js):
            v = [F(0)] * dim
            v[k], v[-1] = F(5), F(-1)
            ans.append((f's_upper_from_missing_middle{j}', F(15), v))
    else:
        v = [F(0)] * dim
        v[-1] = F(-1)
        ans.append(('s_at_most9', F(9), v))
    return ans

def solve_square(rows, rhs):
    n = len(rows)
    a = [list(row) + [b] for row, b in zip(rows, rhs)]
    for j in range(n):
        pivot = next((k for k in range(j, n) if a[k][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [x / divisor for x in a[j]]
        for k in range(n):
            if k != j and a[k][j]:
                q = a[k][j]
                a[k] = [x - q*y for x, y in zip(a[k], a[j])]
    return tuple(a[j][-1] for j in range(n))

def affine_value(const, coefficients, v):
    return const + sum(a*b for a, b in zip(coefficients, v))

def vertices(i, ff):
    dim = 6 - i
    found = set()
    attempts = 0
    for pick in combinations(ff, dim):
        attempts += 1
        v = solve_square([f[2] for f in pick], [-f[1] for f in pick])
        if v is not None and all(affine_value(c, q, v) >= 0 for _, c, q in ff):
            found.add(v)
    return sorted(found), attempts

def expected_anchor(i, p, t):
    n = 6 - i
    if not t:
        return (0,) * n
    return (1,) * n if p + n + 1 <= 5 else (1,) * (n-1) + (0,)

def main():
    protect_sources()
    poly, spaces, checks, minimums, boundaries = [], [], [], [], []
    stats = []
    menu_checks = 0
    for i in range(1, 5):
        ff = facets(i)
        vv, attempts = vertices(i, ff)
        assert len(vv) == {1: 39, 2: 16, 3: 8, 4: 4}[i]
        js = list(range(i+1, 6))
        dim = len(js) + 1
        interior = [F(1, 10)] * len(js) + [F(1)]
        assert all(affine_value(c, q, interior) > 0 for _, c, q in ff)
        state_records = {}
        for state in raw_states(i):
            p, t, o, r = state
            c, q = halfspace(i, state)
            name = state_name(i, *state)
            rec = {'name': name, 'source': i, 'p': p, 't': t, 'o': o, 'tail': list(r), 'constant': str(c), 'coefficients_theta_then_s': stringlist(q)}
            spaces.append(rec)
            state_records[state] = (c, q)
        vrecords = []
        for vindex, v in enumerate(vv):
            vid = f'I{i}_V{vindex:02d}'
            theta, s = v[:-1], v[-1]
            a = F(25) + sum(theta) - s
            assert a > 0
            active = [label for label, c, q in ff if affine_value(c, q, v) == 0]
            vrecords.append({'id': vid, 'theta': stringlist(theta), 's': str(s), 'a': str(a), 'Theta': str(sum(theta)), 'active_facets': active})
            for p in range(i):
                for t, o in product((0, 1), repeat=2):
                    goal = target(i, p, t, o, theta, s)
                    values = []
                    for r in product((0, 1), repeat=6-i):
                        cost = genuine_cost(i, p, t, o, r, theta, s)
                        residual = cost - goal
                        assert residual >= 0, (i, v, p, t, o, r, residual)
                        constant, co = state_records[(p, t, o, r)]
                        assert residual == affine_value(constant, co, v)
                        checks.append({'vertex': vid, 'state': state_name(i, p, t, o, r), 'cost': str(cost), 'target': str(goal), 'residual': str(residual)})
                        values.append((r, cost))
                    assert min(x[1] for x in values) == goal
                    anchor = expected_anchor(i, p, t)
                    assert genuine_cost(i, p, t, o, anchor, theta, s) == goal
                    minimums.append({'vertex': vid, 'source': i, 'p': p, 't': t, 'o': o, 'minimum': str(goal), 'common_anchor': list(anchor), 'all_attaining_tails': [list(r) for r, cost in values if cost == goal]})
        # Every nontrivial domain bound has a genuine full-tail witness.
        for k, j in enumerate(js):
            r = tuple(int(h == k) for h in range(6-i))
            boundaries.append((i, f'theta{j}_cap', (0, 0, 1, r), F(1)))
        boundaries.append((i, 's_nonnegative', (i-1, 1, 0, (1,) * (6-i)), F(1, 30)))
        if i == 1:
            for k, j in enumerate(js):
                r = tuple(int(h != k) for h in range(4)) + (0,)
                boundaries.append((i, f's_upper_from_missing_middle{j}', (0, 1, 0, r), F(1, 20)))
        else:
            r = (1,) * (5-i) + (0,)
            boundaries.append((i, 's_at_most9', (i-2, 1, 0, r), F(1, 20)))
        # Explicit six-index menu averaging, preserving overlap and repeated labels.
        for p in range(i):
            for t in (0, 1):
                for r in product((0, 1), repeat=6-i):
                    for menu in product((0, 1), repeat=6):
                        d, o = sum(menu), int(any(menu))
                        direct0 = sum(F(bit, p+t+sum(r[:-1])+1) for bit in menu) / 6
                        assert direct0 - F(o, 6*(p+t+sum(r[:-1])+1)) == F(d-o, 6*(p+t+sum(r[:-1])+1))
                        for k, j in enumerate(js):
                            den = p+t+sum(r[:k])+7-j
                            exact = sum(F(bit, den) for bit in menu) / 6
                            assert exact - F(o, 6*den) == F(d-o, 6*den)
                        menu_checks += 1
        poly.append({'source': i, 'n': 6-i, 'c_i': str(F(7-i, 2)), 'parameter_order': [f'theta{j}' for j in js]+['s'], 'dimension': dim, 'facets': [{'name': label, 'constant': str(c), 'coefficients': stringlist(q)} for label, c, q in ff], 'strict_interior_point': stringlist(interior), 'facet_intersections_attempted': attempts, 'vertices': vrecords, 'minimum_a': str(min(F(x['a']) for x in vrecords)), 'maximum_s': str(max(v[-1] for v in vv))})
        stats.append({'source': i, 'states': len(state_records), 'facets': len(ff), 'vertices': len(vv), 'vertex_state_checks': len(vv)*len(state_records), 'minimum_tables': len(vv)*4*i})
    witness_records = []
    for i, facet, state, scale in boundaries:
        ff = {f[0]: f[1:] for f in facets(i)}
        c, q = halfspace(i, state)
        fc, fq = ff[facet]
        assert c == scale * fc and q == [scale*x for x in fq]
        witness_records.append({'source': i, 'facet': facet, 'state': state_name(i, *state), 'scale': str(scale), 'residual_constant': str(c), 'residual_coefficients': stringlist(q)})
    root = poly[0]
    balanced = [F(25, 63)]*4
    rootpoint = next(v for v in root['vertices'] if list(map(F, v['theta'])) == balanced and F(v['s']) == F(1070, 63))
    assert F(rootpoint['a']) == F(605, 63)
    assert sum(F(1, 6*(7-j)*(8-j)) for j in (3, 4, 5)) + 1 == F(21, 20)
    assert sum(s['states'] for s in stats) == 416
    assert len(checks) == 8064 and len(minimums) == 444 and menu_checks == 13312
    dump('parameter_polytopes.json', {'schema': 'all_source_joint_reweighted_affine_domain_v1', 'status': 'EXACT_DOMAINS_VERIFIED', 'facet_convention': 'constant + coefficients dot(theta...,s) >= 0', 'sources': poly, 'root_balanced_extremizer': rootpoint, 'attribution': 'Main proposed reweighting/generalization and root upper boundaries; domain enumeration and independent verification by this package.'})
    dump('state_halfspaces.json', spaces)
    dump('hidden_state_checks.json', checks)
    dump('minimum_tables.json', minimums)
    dump('necessary_boundary_witnesses.json', witness_records)
    dump('domain_checker_output.json', {'status': 'PASS', 'sources': stats, 'hidden_states': 416, 'vertices': 67, 'vertex_state_checks': len(checks), 'minimum_tables_with_all_attainers': len(minimums), 'necessary_boundary_witnesses': len(witness_records), 'explicit_menu_cases': menu_checks, 'minimum_residual': str(min(F(x['residual']) for x in checks)), 'optimizer_calls': 0, 'project_code_imported_or_executed': False, 'fixed_point_bound': False, 'full_global_row_family_generated_here': False})
    protect_sources()
    print(json.dumps({'status': 'PASS', 'sources': stats, 'checks': len(checks), 'all_attainment_tables': len(minimums), 'menu_cases': menu_checks, 'root_extremizer': rootpoint}, ensure_ascii=False))

if __name__ == '__main__':
    main()
