"""Recover and check rational joint masses on the discovered finite support."""
import argparse
import json
import sympy as sp

from contract import (HERE, F, load_inputs, row_names, budgets, compressed_column,
                      column_roots, POINT_SHA, sha)


def S(x):
    return sp.Rational(x.numerator, x.denominator)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='restricted_discovery.json')
    ap.add_argument('--output', default='joint_completion_exact.json')
    args = ap.parse_args()
    path = HERE / args.input
    discovery = json.loads(path.read_text())
    assert discovery['success'] and discovery['point_sha256'] == POINT_SHA
    data = load_inputs()
    names = row_names(discovery['extended'])
    rhs = budgets(data, names)
    contexts = list(data['masses'])
    support = discovery['support']
    cols = [compressed_column(v['actual'], v['d'], column_roots(v['one_word'], v['zero_words']),
                              names, data['remainder']) for v in support]
    eq = [[F(int((v['actual'], v['d']) == context)) for v in support] for context in contexts]
    erhs = list(data['masses'].values())
    active = [i for i, value in enumerate(discovery['budget_slacks_float']) if abs(value) < 1e-8]
    for i in active:
        eq.append([b[i] for r, b in cols])
        erhs.append(rhs[i])
    matrix = sp.Matrix([[S(x) for x in row] for row in eq])
    target = sp.Matrix([S(x) for x in erhs])
    solution, params = matrix.gauss_jordan_solve(target)
    assert len(params) == 0, 'Recovery must resolve every free mass explicitly.'
    masses = [F(int(x.p), int(x.q)) for x in solution]
    assert min(masses) >= 0
    for row, value in zip(eq, erhs):
        assert sum(x * y for x, y in zip(row, masses)) == value
    slacks = [rhs[i] - sum(y * b[i] for y, (r, b) in zip(masses, cols)) for i in range(len(names))]
    assert min(slacks) >= 0, [(names[i], v) for i, v in enumerate(slacks) if v < 0]
    root = sum(y * r for y, (r, b) in zip(masses, cols))
    root_slack = data['u'][0] - root
    assert root_slack > 0
    output = {
        'status': 'EXACT SIX-ROOT SHARED-CUSTOMER COMPLETION OF THE DECLARED PROJECTION',
        'scope': 'A common distribution over all six root tails at each customer; not an SPE realization.',
        'point_sha256': POINT_SHA, 'discovery_sha256': sha(path), 'extended': discovery['extended'],
        'normalization': 'Customer masses sum to mu(actual,d); all root source costs use 1/6; root coefficient fixed to one.',
        'budget_count': len(names), 'contexts': len(contexts),
        'support': [{**{k: v[k] for k in ('actual', 'd', 'one_word', 'zero_words')}, 'mass': str(m)}
                    for v, m in zip(support, masses) if m],
        'context_masses': [{'actual': a, 'd': d, 'mass': str(m)} for (a, d), m in data['masses'].items()],
        'budget_slacks': [{'row': list(name), 'budget': str(budget), 'slack': str(slack)}
                          for name, budget, slack in zip(names, rhs, slacks)],
        'root_cost': str(root), 'root_budget': str(data['u'][0]), 'root_slack': str(root_slack),
        'root_slack_float': float(root_slack), 'active_recovery_rows': [list(names[i]) for i in active],
        'sources': data['sources'],
        'lift_to_original_hist_records': 'For record h of actual context c, split every common atom y_c,n with mass x_h*y_c,n/mu_c. This preserves all original hist record marginals; no new cross-identity constraints are claimed.'}
    (HERE / args.output).write_text(json.dumps(output, indent=2) + '\n')
    refined = []
    original_hist = []
    for index, record in enumerate(data['raw']['columns']):
        if record['kind'] != 'hist':
            continue
        original_hist.append({'original_column_index': index, **record})
        mass = F(record['weight'])
        if not mass:
            continue
        context = record['actual_bits'], record['d']
        for atom_index, atom in enumerate(output['support']):
            if (atom['actual'], atom['d']) != context:
                continue
            value = mass * F(atom['mass']) / data['masses'][context]
            refined.append({'original_column_index': index, 'joint_atom_index': atom_index,
                            'actual': context[0], 'd': context[1], 'old_hist': record['hist'],
                            'one_word': atom['one_word'], 'zero_words': atom['zero_words'],
                            'mass': str(value)})
    refined_output = {'status': 'EXACT PRODUCT REFINEMENT OF THE 16 ORIGINAL HIST RECORDS',
                      'scope': 'Preserves each old hist marginal and the new common six-root marginal; no old/new theme identity is asserted.',
                      'point_sha256': POINT_SHA, 'joint_completion_sha256': sha(HERE / args.output),
                      'original_hist_records': original_hist, 'atoms': refined}
    (HERE / 'original_hist_refinement_exact.json').write_text(json.dumps(refined_output, indent=2) + '\n')
    projection_inputs = {'point_sha256': POINT_SHA, 'sources': data['sources'],
                         'O': str(data['O']), 'W': str(data['raw']['W']), 'K': str(data['K']),
                         'u': list(map(str, data['u'])), 'original_hist_records': original_hist,
                         'context_masses': output['context_masses'],
                         'remainder_table': [{'t': t, 'word': w, 'comparison_count': q, 'value': str(value)}
                                             for (t, w, q), value in sorted(data['remainder'].items())]}
    (HERE / 'projection_inputs_exact.json').write_text(json.dumps(projection_inputs, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'support': len(output['support']),
                      'budget_count': len(names), 'root_slack': str(root_slack),
                      'root_slack_float': float(root_slack),
                      'active_budgets': sum(v == 0 for v in slacks),
                      'original_hist_refinement_atoms': len(refined)}, indent=2))


if __name__ == '__main__':
    main()
