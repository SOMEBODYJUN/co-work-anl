#!/usr/bin/env python3
"""Nine exact 31/25/19 menu-prefix projections, keeping the explicit Pi term.

Only the old frozen four-source layer supplies budgets and mass equalities.
No PAIR closure row is needed for these identities.  No point or optimizer is
read.  The original 36-row projection and all old files remain untouched.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
INPUTS = {
    'old_append': WORK / 'early_shared_x_joint/symbolic_append.json.gz',
    'old_prefix_rows': WORK / 'main_prefix_maxx_interface/rows_51.json',
    'averaged_menu_proof': WORK / 'main_averaged_menu_prefix.md',
    'optimal_union_proof': WORK / 'main_optimal_union_prefix.md',
}
PINS = {
    'old_append': '1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0',
    'old_prefix_rows': '1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c',
}
WEIGHTS = {1: (F(25), F(6), F(4, 5), F(31)),
           2: (F(20), F(5), F(19, 20), F(25)),
           3: (F(15), F(4), F(7, 6), F(19))}
OLD_C = {1: F(206, 5), 2: F(121, 4), 3: F(61, 3)}


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    data = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    if path.suffix == '.gz':
        with path.open('wb') as stream:
            with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as f:
                f.write(data)
    else:
        path.write_bytes(data)


def add(row, j, a):
    if a:
        row[j] = row.get(j, F()) + a
        if not row[j]:
            del row[j]


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def unpack(row):
    return {j: F(a) for j, a in row}


def correction(i, n, k, count):
    m, a = 5 - i, WEIGHTS[i][2]
    values = [j * (F(count, 6 * n * (n + j)) - a / (n + k)) for j in range(m + 1)]
    return max(values), values


def uncorrected_E(i, n, k, x, ys, t, theta):
    alpha, r, a, C = WEIGHTS[i]
    D, j, m = n + 6 - i, sum(ys), 5 - i
    return (alpha * F(x, n + j + t) + r * F(t, D)
            - (C - 1) * F(x, D) - theta * (F(x, D) + F(1 - x, n))
            - a * F(m * x - j, n + k) - (F(t) - theta) / (n + x + j))


def main():
    before = {key: sha256(path.read_bytes()).hexdigest() for key, path in INPUTS.items()}
    assert all(before[k] == v for k, v in PINS.items())
    old = read(INPUTS['old_append'])
    prefix_rows = read(INPUTS['old_prefix_rows'])['rows']
    hist = {h['hist_column']: h for h in old['base_contract']['histograms']}
    assert all(h['indexed_membership_counts']['T'] == 1 for h in hist.values())
    branches = {b['source_player']: b for b in old['branches']}
    raw, ge, eq = old['raw_inequality_provenance'], old['inequalities'], old['equalities']
    eq_map = {tuple(v['name'][1:]): v for v in eq}
    incomes = {i: unpack(old['base_contract']['actual_income_rows'][str(i)]) for i in range(1, 4)}

    def choose(family, i, query=None, actual_source=None):
        rows = [v for v in raw if v['family'] == family and v['branch_source_player'] == i]
        if query is not None:
            rows = [v for v in rows if v.get('query') == query]
        if actual_source is not None:
            rows = [v for v in rows if v.get('actual_source_player') == actual_source]
        assert len(rows) == 1
        return rows[0]

    universal, pi_table, universal_counts, union_count = [], [], Counter(), 0
    for i in range(1, 4):
        m = 5 - i
        for n, k, count in product(range(1, i + 1), range(m + 1), range(7)):
            pi, options = correction(i, n, k, count)
            theta = F(count, 6)
            actual_max_deficit = F()
            for x in (0, 1):
                for tail in product((0, 1), repeat=m + 1):
                    ys, t = tail[:-1], tail[-1]
                    E = uncorrected_E(i, n, k, x, ys, t, theta)
                    rho = E + (1 - x) * pi
                    assert rho >= 0
                    if x:
                        assert E >= 0
                    else:
                        actual_max_deficit = max(actual_max_deficit, -E)
                    universal_counts['zero' if rho == 0 else 'positive'] += 1
                    universal_counts['total'] += 1
                    universal.append({'source': i, 'n': n, 'k': k, 'menu_count': count,
                                      'x': x, 'middle_bits': list(ys), 'terminal_bit': t,
                                      'E': str(E), 'Pi': str(pi), 'corrected_E': str(rho)})
                    union_theta = F(int(count > 0), 6)
                    union_E = uncorrected_E(i, n, k, x, ys, t, union_theta)
                    query_weakening = (theta - union_theta) / (n + x + sum(ys))
                    assert union_E >= 0 and query_weakening >= 0
                    union_count += 1
            assert pi == actual_max_deficit
            pi_table.append({'source': i, 'n': n, 'k': k, 'menu_count': count, 'Pi': str(pi),
                             'values_by_middle_count': [str(v) for v in options],
                             'maximizing_middle_counts': [j for j, value in enumerate(options) if value == pi],
                             'minimum_nonnegative_x0_correction': str(actual_max_deficit)})
    assert universal_counts['total'] == union_count == 5040 and len(pi_table) == 154

    certificates, projected_rows, nonzero_support_pi = [], [], []
    saved_counts = Counter()
    for i in range(1, 4):
        branch = branches[i]
        alpha, r, a, C = WEIGHTS[i]
        for query in old['fixed_known_queries'][6:]:
            family = query['family']
            payments = []

            def pay(rec, weight):
                assert weight >= 0
                payments.append({'raw_row_id': rec['raw_id'], 'unique_row_id': rec['unique_row_id'],
                                 'family': rec['family'], 'weight': str(weight)})

            pay(choose('source-IC', i), alpha)
            pay(choose('actual-source-SAFE', i, branch['ordered_tail_labels'][-1], i), r)
            for middle in branch['ordered_tail_labels'][:-1]:
                pay(choose('same-P-MAX', i, middle), a)
            pay(choose('branch-terminal-BR', i, query), F(1))
            combined = {}
            for payment in payments:
                for j, coef in ge[payment['unique_row_id']]['row']:
                    add(combined, j, F(payment['weight']) * F(coef))
            target = {j: C * value for j, value in incomes[i].items()}
            hist_corrections = []
            for h, data in hist.items():
                n = data['actual_backgrounds'][i - 1] + 1
                k = data['P'] - n + 1
                count = data['indexed_membership_counts'][family]
                theta, D = F(count, 6), n + 6 - i
                pi, _ = correction(i, n, k, count)
                add(target, h, -theta / n + pi)
                add(target, data['X_column'], -(C - 1) / D + theta * F(6 - i, n * D) - pi)
                rec = {'hist_column': h, 'X_column': data['X_column'], 'n': n, 'k': k,
                       'menu_count': count, 'Pi': str(pi),
                       'old_column_correction': [[h, str(pi)], [data['X_column'], str(-pi)]]}
                hist_corrections.append(rec)
                if pi:
                    nonzero_support_pi.append({'source': i, 'menu': family, **rec})
            state_remainders = []
            for offset, col in enumerate(old['new_columns']):
                if col['source_player'] != i:
                    continue
                data = hist[col['hist_column']]
                n = data['actual_backgrounds'][i - 1] + 1
                k = data['P'] - n + 1
                count = data['indexed_membership_counts'][family]
                pi, _ = correction(i, n, k, count)
                E = uncorrected_E(i, n, k, col['X_bit'], col['middle_bits'], col['terminal_bit'], F(count, 6))
                rho = E + (1 - col['X_bit']) * pi
                assert rho >= 0
                j = 21021 + offset
                add(combined, j, rho)
                state_remainders.append({'column': j, 'E': str(E), 'Pi': str(pi), 'corrected_E': str(rho)})
                saved_counts['zero' if rho == 0 else 'positive'] += 1
                saved_counts['total'] += 1
            equality_payments = []
            for h, data in hist.items():
                n = data['actual_backgrounds'][i - 1] + 1
                k = data['P'] - n + 1
                count = data['indexed_membership_counts'][family]
                pi, _ = correction(i, n, k, count)
                theta, D = F(count, 6), n + 6 - i
                for x in (0, 1):
                    mass_row = eq_map[(i, h, x)]
                    indices = [j for j, coef in mass_row['row'] if j >= 21021]
                    coefs = {combined.get(j, F()) for j in indices}
                    assert len(coefs) == 1
                    weight = -next(iter(coefs))
                    beta = (C - 1) * F(x, D) + theta * (F(x, D) + F(1 - x, n))
                    beta += (5 - i) * a * F(x, data['P'] + 1) - (1 - x) * pi
                    assert weight == beta
                    equality_payments.append({'equality_row_id': mass_row['id'], 'weight': str(weight)})
                    for j, coef in mass_row['row']:
                        add(combined, j, weight * F(coef))
            assert combined == target and all(j < 21021 for j in combined)
            members = [[family, index] for index in range(6)]
            old_targets = [v for v in prefix_rows if v['actual_player'] == i and v['query_members'] == members]
            assert len(old_targets) == 1
            delta = OLD_C[i] - C
            interface_check = unpack(old_targets[0]['row'])
            for j, value in incomes[i].items():
                add(interface_check, j, -delta * value)
            for h, data in hist.items():
                D = data['actual_backgrounds'][i - 1] + 7 - i
                add(interface_check, data['X_column'], delta / D)
            for correction_record in hist_corrections:
                for j, value in correction_record['old_column_correction']:
                    add(interface_check, j, F(value))
            assert interface_check == target
            if family == 'T':
                assert all(F(v['Pi']) == 0 for v in hist_corrections)
            row_id = len(projected_rows)
            projected_rows.append({'id': row_id, 'name': ['common-X-averaged-menu-prefix-Pi', i, family],
                                   'source_player': i, 'menu': family, 'C': str(C),
                                   'row': sparse(target), 'rhs': '0', 'sense': '>=',
                                   'no_penalty_on_current_support': all(F(v['Pi']) == 0 for v in hist_corrections),
                                   'hist_corrections': hist_corrections})
            certificates.append({'id': row_id, 'source_player': i, 'menu': family, 'C': str(C),
                                 'nonnegative_budget_payments': payments,
                                 'mu_remainders': state_remainders,
                                 'signed_mass_equality_payments': equality_payments,
                                 'target_row': sparse(target),
                                 'comparison_to_old_Cstar': {'old_row_name': old_targets[0]['name'], 'delta': str(delta),
                                                            'identity': 'new=old_Cstar-delta*(actual u_i-kappa_i(X))+sum_h Pi*(H_h-x_h)'},
                                 'all_hidden_coefficients_canceled': True})
    assert len(certificates) == 9 and saved_counts['total'] == 5376
    assert before == {key: sha256(path.read_bytes()).hexdigest() for key, path in INPUTS.items()}
    save('averaged_prefix_rows_9.json', {'schema': 'averaged-prefix-with-Pi-rows/v1', 'columns': 22941,
                                      'new_columns': 0, 'rows': projected_rows, 'point_values_read': False,
                                      'scope': 'Three T averages have Pi=0 because dT=1 on current16 hist; all six B/C rows retain the explicit universal Pi formula, even if some values vanish.'})
    save('averaged_prefix_projection.json.gz', {'schema': 'averaged-prefix-with-Pi-projection/v1',
                                              'status': 'EXACT_NINE_IDENTITIES_NO_SOLVE',
                                              'input_sha256': before, 'certificates': certificates,
                                              'identity': 'target=sum nonnegative old436 budget rows + sum corrected_E_mu*mu + sum signed old128 mass equations',
                                              'all_pair_closure_rows_used': False,
                                              'old_36_projection_unchanged': True,
                                              'no_point_values': True, 'optimizer_calls': 0})
    save('averaged_prefix_full_domain.json.gz', {'schema': 'averaged-prefix-Pi-full-domain/v1',
                                              'all_5040_corrected_remainders_nonnegative': True,
                                              'all_154_Pi_are_minimal_x0_corrections': True,
                                              'counts': dict(universal_counts), 'Pi_table': pi_table,
                                              'remainder_records': universal,
                                              'union_bridge': {'checked_states': union_count,
                                                               'o': '1[d>0]', 'weakened_query_theta': 'o/6',
                                                               'added_terminal_nonnegative_term': '(d-o)/(6*(n+x+sum_ys))',
                                                               'union_E_nonnegative': True,
                                                               'no_union_action_or_customer_deletion': True}})
    summary = {'status': 'PASS_NINE_EXACT_MENU_PREFIX_PROJECTIONS', 'rows': 9,
               'constants_by_source': {'1': '31', '2': '25', '3': '19'},
               'middle_MAX_weights': {'1': '4/5', '2': '19/20', '3': '7/6'},
               'universal_domain_counts': dict(universal_counts), 'Pi_backgrounds': len(pi_table),
               'saved_state_remainder_counts': dict(saved_counts),
               'nonzero_Pi_on_current_support': nonzero_support_pi,
               'budget_payment_terms': sum(len(v['nonnegative_budget_payments']) for v in certificates),
               'mass_equality_payment_terms': sum(len(v['signed_mass_equality_payments']) for v in certificates),
               'all_old_rows_unchanged': True, 'optimizer_calls': 0,
               'input_sources': {key: {'path': str(path.relative_to(REPO)), 'sha256': before[key]}
                                 for key, path in INPUTS.items()},
               'projection_sha256': sha256((HERE / 'averaged_prefix_projection.json.gz').read_bytes()).hexdigest(),
               'rows_sha256': sha256((HERE / 'averaged_prefix_rows_9.json').read_bytes()).hexdigest()}
    save('averaged_prefix_projection_summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
