"""Recover fresh masses exactly and test all 36 new rows on that ONE measure.

The 203-budget LP support is recovered before any pair constraint is used.
The 239-budget floating solution is a discovery diagnostic, not a premise.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import lcm
import json
import sys
from model import (HERE, PIN, input_snapshot, load_inputs, pair_names, root_contract,
                   seed_columns, sha, single_names, system, write_json)


def exact_solve(rows, rhs):
    """Gauss-Jordan over Fraction; require a nonsingular square system."""
    n = len(rows)
    assert n == len(rhs) and all(len(row) == n for row in rows)
    matrix = [list(map(F, row))+[F(v)] for row, v in zip(rows, rhs)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if matrix[i][col])
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        p = matrix[col][col]
        matrix[col] = [x/p for x in matrix[col]]
        for i in range(n):
            if i == col or not matrix[i][col]:
                continue
            p = matrix[i][col]
            matrix[i] = [x-p*y for x, y in zip(matrix[i], matrix[col])]
    assert all(matrix[i][j] == F(i == j) for i in range(n) for j in range(n))
    return [row[-1] for row in matrix]


def main():
    data = load_inputs()
    assert json.loads((HERE/'inputs_exact.json').read_text()) == input_snapshot(data)
    cols = seed_columns(data, root_contract())
    disc = json.loads((HERE/'seed_203_discovery.json').read_text())
    assert disc['status'] == 0 and disc['point_sha256'] == PIN and not disc['pairs_included']
    support = [r['column'] for r in disc['support']]
    en, eq, be, un, ub, bu = system(data, cols, False)
    active = [r['index'] for r in disc['active_rows']]
    rows = [[row[j] for j in support] for row in eq]+[[ub[i][j] for j in support] for i in active]
    rhs = be+[bu[i] for i in active]
    weights = exact_solve(rows, rhs)
    assert all(m > 0 for m in weights)
    for row, target in zip(eq, be):
        assert sum(m*row[j] for j, m in zip(support, weights)) == target
    rootmargins = defaultdict(F)
    atoms = []
    denominator = 1
    for j, m in zip(support, weights):
        c = cols[j]
        atom = {k: c[k] for k in ('hist', 'seed_root_state', 'actual', 'old_words', 'new_words')}
        atom.update({'column': j, 'mass': str(m)})
        atoms.append(atom)
        rootmargins[c['seed_root_state']] += m
        denominator = lcm(denominator, (m/720).denominator)
    assert sum(weights) == 1
    en2, eq2, be2, un2, ub2, bu2 = system(data, cols, True)
    assert eq == eq2 and en == en2 and be == be2
    budgets = []
    for name, row, budget in zip(un2, ub2, bu2):
        cost = sum(m*row[j] for j, m in zip(support, weights))
        slack = budget-cost
        assert slack >= 0, (name, slack)
        budgets.append({'row': list(name), 'budget': str(budget), 'cost': str(cost),
                        'slack': str(slack), 'float': float(slack)})
    saved = {tuple(r['row']): r for r in budgets}
    rootgap = F(saved['root-source',]['slack'])
    assert rootgap > 0
    newslacks = [F(saved[n]['slack']) for n in pair_names()]
    coefficient_table = {'scope': 'Constructor coefficients; independently recomputed by verifier.',
        'point_sha256': PIN, 'row_order': [list(n) for n in un2],
        'columns': [{**{k: c[k] for k in ('hist', 'seed_root_state', 'actual', 'old_words', 'new_words')},
                     'costs': [str(row[j]) for row in ub2]}
                    for j, c in enumerate(cols)]}
    write_json(HERE/'candidate_coefficients_exact.json', coefficient_table)
    base = {'scope': 'One finite common membership measure; not SPE and not R/Z full-own.',
        'point_sha256': PIN, 'input_snapshot_sha256': sha(HERE/'inputs_exact.json'),
        'coefficient_table_sha256': sha(HERE/'candidate_coefficients_exact.json'),
        'support_recovered_from': 'seed_203_discovery.json',
        'discovery_sha256': sha(HERE/'seed_203_discovery.json'),
        'recovery_equations': [{'kind': 'old-hist', 'hist': hi} for hi in en]
            + [{'kind': 'budget', 'row': list(un[i])} for i in active],
        'equation_count': len(rows), 'positive_atoms': len(atoms), 'atoms': atoms,
        'total_mass': '1', 'unit_customer_scale': str(denominator),
        'candidate_columns': 32, 'candidate_root_states': 17,
        'new_root_state_margins': [{'root_state': j, 'mass': str(rootmargins[j])}
                                  for j in range(len(data['seeds']))],
        'root_source_coefficient': 1, 'root_budget': str(data['u'][0]),
        'root_cost': saved['root-source',]['cost'], 'root_gap': str(rootgap)}
    cert203 = {**base, 'nonroot_budgets': 203,
        'budget_slacks': [r for r in budgets if tuple(r['row']) not in pair_names()]}
    write_json(HERE/'completion_203_exact.json', cert203)
    cert239 = {**base, 'nonroot_budgets': 239, 'budget_slacks': budgets,
        'unchanged_atoms_from_203_sha256': sha(HERE/'completion_203_exact.json'),
        'new_pair_row_minimum': str(min(newslacks)),
        'new_pair_rows_strict': sum(s > 0 for s in newslacks),
        'new_pair_rows_zero': sum(s == 0 for s in newslacks),
        'whole_family_nonseparation': 'Root-source coefficient fixed at 1; every other multiplier is globally fixed and nonnegative.'}
    write_json(HERE/'joint_completion_exact.json', cert239)
    write_json(HERE/'recovery_audit.json', {'actual_argv': [sys.executable, *sys.argv],
        'point_sha256': PIN, 'script_sha256': sha(__file__), 'exact_equations': len(rows),
        'equations_unique': True, 'all_masses_positive': True,
        'all_240_budgets_nonnegative': True, 'positive_atoms': len(atoms),
        'root_cost': saved['root-source',]['cost'], 'root_gap': str(rootgap),
        'root_gap_float': float(rootgap), 'new_pair_row_minimum': str(min(newslacks)),
        'new_pair_row_minimum_float': float(min(newslacks)),
        'new_pair_rows_strict': sum(s > 0 for s in newslacks),
        'active_rows': [r['row'] for r in budgets if F(r['slack']) == 0],
        'new_pair_rows': [r for r in budgets if tuple(r['row']) in pair_names()]})
    print(json.dumps({k: v for k, v in cert239.items() if k not in ('atoms', 'budget_slacks', 'new_root_state_margins')}, indent=2))
    for n in pair_names():
        print('PAIR', n, saved[n]['slack'], saved[n]['float'])


if __name__ == '__main__':
    main()
