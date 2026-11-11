"""Recover and verify the small discovery by exact rational elimination.

No optimization is used in this file; model() loads discovery coefficients.
The final independent verifier does not import this file or model().
"""
from collections import defaultdict
from fractions import Fraction as F
import json
from math import lcm

from common import HERE, BASE, digest, names, rows_json, write_json
from solve_coupling import model


def solve_square(matrix, rhs):
    n = len(rhs)
    assert len(matrix) == n and all(len(r) == n for r in matrix)
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        assert pivot is not None, ('singular', j)
        a[j], a[pivot] = a[pivot], a[j]
        lead = a[j][j]
        a[j] = [v / lead for v in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                v = a[i][j]
                a[i] = [x - v * y for x, y in zip(a[i], a[j])]
    return [r[-1] for r in a]


def main():
    cols, en, eq, be, un, ub, bu = model('rebudget')
    discovered = json.loads((HERE / 'rebudget_coupling_discovery.json').read_text())
    support = [v['column'] for v in discovered['positive_support']]
    active = [v['index'] for v in discovered['active_rows']]
    matrix = [[row[j] for j in support] for row in eq]
    matrix += [[ub[i][j] for j in support] for i in active]
    rhs = be + [bu[i] for i in active]
    masses = solve_square(matrix, rhs)
    assert len(masses) == 17 and min(masses) > 0
    full = [F(0)] * len(cols)
    for j, m in zip(support, masses):
        full[j] = m
    assert all(sum(a*x for a,x in zip(row, full)) == b for row,b in zip(eq,be))
    slacks = [b - sum(a*x for a,x in zip(row, full)) for row,b in zip(ub,bu)]
    assert min(slacks) >= 0
    root_cost = sum(c['root'] * x for c,x in zip(cols,full))
    root_pos = un.index(('root-source',))
    assert slacks[root_pos] > 0
    atoms = []
    roots = defaultdict(F)
    for j,m in zip(support,masses):
        c = cols[j]
        atoms.append({k:c[k] for k in ['original_column_index','joint_atom_index','actual','old_words','new_words']} | {
                      'source_column': j, 'mass': str(m)})
        roots[c['joint_atom_index']] += m
    denominator = lcm(*[(m/720).denominator for m in masses])
    out = {'status': 'EXACT SHARED OLD-C / SIX-ROOT-TAIL FINITE PROJECTION COMPLETION',
           'scope': 'Only declared hist, root budgets and 216 terminal queries; no complete SPE or six-player half conclusion.',
           'point_sha256': digest(BASE / 'peer_augmented_lp/augmented_lp_exact.json'),
           'input_snapshot_sha256': digest(HERE / 'input_snapshot_exact.json'),
           'discovery_sha256': digest(HERE / 'rebudget_coupling_discovery.json'),
           'symmetrization': 'For each displayed atom, every common permutation of the six old/new indices has mass atom.mass/720.',
           'normalization': 'Root source coefficient 1; all other 175 legal budget multipliers arbitrary nonnegative.',
           'old_hist_records': 16, 'positive_old_hist_records': len(eq),
           'incidence_orbit_domain': len(cols), 'support_atoms': len(atoms),
           'literal_atoms_before_duplicate_merging': 720*len(atoms),
           'total_mass': str(sum(masses)),
           'unit_customer_scale': str(denominator),
           'root_cost': str(root_cost), 'root_cost_float': float(root_cost),
           'root_budget': str(bu[root_pos]), 'root_slack': str(slacks[root_pos]),
           'root_slack_float': float(slacks[root_pos]),
           'old_budget_count': 163, 'new_interface_orbits': 12, 'new_literal_queries': 216,
           'budget_slacks': [{'row': list(n), 'budget': str(b), 'slack': str(s), 'float': float(s)}
                             for n,b,s in zip(un,bu,slacks)],
           'active_recovery_rows': [list(n) for n in en] + [list(un[i]) for i in active],
           'new_root_state_margins': [{'original_root_state': j, 'mass': str(roots[j])}
                                    for j in range(17)],
           'atoms': atoms}
    write_json(HERE / 'joint_completion_exact.json', out)

    # Exact fixed-marginal bounds. These are explicitly restricted to the
    # previous 17 root-state masses and do not separate the rebudgeted completion.
    fc, fen, feq, fbe, fun, fub, fbu = model('fixed')
    fd = json.loads((HERE / 'fixed_coupling_discovery.json').read_text())
    bounds = []
    for row in fd['single_interface_maxima_over_margins_only']:
        if row['maximum_float'] >= 0:
            continue
        name = tuple(row['row'])
        k = names().index(name)
        dual = [F(x).limit_denominator(10**6) for x in row['equality_dual']]
        costs = [-c['interface'][k] for c in fc]
        gaps = [v - sum(y*a[j] for y,a in zip(dual,feq)) for j,v in enumerate(costs)]
        assert min(gaps) >= 0
        upper = -sum(y*b for y,b in zip(dual,fbe))
        assert upper < 0
        bounds.append({'row': list(name), 'upper_bound': str(upper), 'upper_bound_float': float(upper),
                       'is_exact_invariant': all(v == 0 for v in gaps),
                       'dual_potentials': [{'margin': list(n), 'value': str(y)} for n,y in zip(fen,dual)],
                       'all_32_column_dual_gaps': list(map(str,gaps))})
    write_json(HERE / 'fixed_root_marginal_obstruction_exact.json', {
        'scope': 'Only fixed OLD root-state masses; not a general necessary cut. Rebudgeted completion exists.',
        'point_sha256': out['point_sha256'], 'incidence_orbits': len(fc),
        'old_root_certificate_sha256': digest(BASE / 'cross_root_pricing/joint_completion_exact.json'),
        'bounds': bounds})
    print('EXACT RECOVERY PASSED', len(atoms), 'atoms;', len(slacks), 'nonnegative rows')
    print('root cost', float(root_cost), 'slack', float(slacks[root_pos]))
    print('positive new root states', sum(v > 0 for v in roots.values()))
    for n,s in zip(un,slacks):
        if n[0] in ('C-to-Y','Y5-to-C'):
            print(n,float(s))


if __name__ == '__main__':
    main()
