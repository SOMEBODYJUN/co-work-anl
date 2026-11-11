#!/usr/bin/env python3
"""Exact 36-row visible-prefix projection; no point values or optimization.

Use already generated real-source budgets, nonnegative mu remainders and
signed mass equalities.  Compare only the nine visible query orbits per source
against the frozen C* and H3 interfaces.  This adds no constraints or columns.
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
INPUTS = {
    'append': HERE / 'symbolic_append.json.gz',
    'prefix_interface': WORK / 'main_prefix_maxx_interface/rows_51.json',
    'H3_interface': WORK / 'maxb_h3_bridge/rows_17.json',
    'prefix_proof': WORK / 'main_prefix_safety_maxx_family.md',
    'H3_proof': WORK / 'maxb_h3_bridge.md',
}
PINS = {
    'append': '1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0',
    'prefix_interface': '1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c',
    'H3_interface': '3c9d360cbb0313ae84b4be7add4f4b3f6b67ba57f71cb8f366a2341e8f128d8d',
}
WEIGHTS = {
    1: (F(25), F(51, 20), F(6), F(3, 8), F(0), F(206, 5)),
    2: (F(20), F(7, 4), F(5), F(3, 5), F(0), F(121, 4)),
    3: (F(15), F(2, 3), F(4), F(1), F(0), F(61, 3)),
    4: (F(10), F(0), F(0), F(1), F(2), F(10)),
}


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def save(name, value):
    path = HERE / name
    assert not path.exists(), ('refuse_overwrite', str(path))
    payload = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    if path.suffix == '.gz':
        with path.open('wb') as out:
            with gzip.GzipFile(filename='', mode='wb', fileobj=out, mtime=0) as f:
                f.write(payload)
    else:
        path.write_bytes(payload)


def add(row, j, v):
    if v:
        row[j] = row.get(j, F()) + v
        if not row[j]:
            del row[j]


def unpack(row):
    return {j: F(a) for j, a in row}


def sparse(row):
    return [[j, str(a)] for j, a in sorted(row.items()) if a]


def remainder(i, b, k, x, ys, t, q):
    alpha, sy, st, ay, at, C = WEIGHTS[i]
    r, n, p, y = 7 - i, b + 1, b + k, sum(ys)
    target = -(C - 1) * F(x, b + r) - q * (F(x, b + r) + F(1 - x, n))
    paid = -alpha * F(x, n + y + t)
    paid -= (sy * y + st * t) / (b + r)
    paid += ay * F(len(ys) * x - y, p + 1) + at * F(x - t, p + 1)
    paid += (F(t) - q) / (n + x + y)
    return target - paid


def main():
    hashes = {k: sha256(p.read_bytes()).hexdigest() for k, p in INPUTS.items()}
    for key in ('append', 'prefix_interface', 'H3_interface'):
        assert hashes[key] == PINS[key]
    packet = read(INPUTS['append'])
    prefix_rows = read(INPUTS['prefix_interface'])['rows']
    h3_rows = read(INPUTS['H3_interface'])['rows']
    hist = {h['hist_column']: h for h in packet['base_contract']['histograms']}
    cols = packet['new_columns']
    branches = {b['source_player']: b for b in packet['branches']}
    raw = packet['raw_inequality_provenance']
    ge = packet['inequalities']
    eq = packet['equalities']
    eq_by_name = {tuple(v['name'][1:]): v for v in eq}
    old_count = packet['old_columns']

    def choose(family, i, query=None, actual_source=None):
        rows = [v for v in raw if v['family'] == family and v['branch_source_player'] == i]
        if query is not None:
            rows = [v for v in rows if v.get('query') == query]
        if actual_source is not None:
            rows = [v for v in rows if v.get('actual_source_player') == actual_source]
        assert len(rows) == 1, (family, i, query, actual_source, len(rows))
        return rows[0]

    all_type_records, universal_counts = [], {}
    for i in range(1, 5):
        m = 5 - i
        counts = Counter()
        for b, k in product(range(i), range(m + 1)):
            for bits in product((0, 1), repeat=m + 3):
                x, ys, t, q = bits[0], bits[1:-2], bits[-2], bits[-1]
                value = remainder(i, b, k, x, ys, t, F(q))
                assert value >= 0
                counts['total'] += 1
                counts['zero' if value == 0 else 'positive'] += 1
                all_type_records.append({'source': i, 'b': b, 'actual_k': k, 'x': x,
                                         'middle_bits': list(ys), 'terminal_bit': t, 'query_bit': q,
                                         'E': str(value)})
        universal_counts[str(i)] = dict(counts)
    assert len(all_type_records) == 1568

    certificates = []
    for i in range(1, 5):
        branch = branches[i]
        alpha, sy, st, ay, at, C = WEIGHTS[i]
        for query in packet['fixed_known_queries']:
            members = ([['A', query['player'] - 1]] if query['kind'] == 'actual' else
                       [[query['family'], j] for j in range(6)])
            candidates = h3_rows if i == 4 else [v for v in prefix_rows if v['actual_player'] == i]
            matching = [v for v in candidates if v['query_members'] == members]
            assert len(matching) == 1
            target_source = matching[0]
            target = unpack(target_source['row'])
            assert all(j < old_count for j in target)
            payments = []

            def pay(rec, weight):
                if weight:
                    assert weight >= 0
                    payments.append({'raw_row_id': rec['raw_id'], 'unique_row_id': rec['unique_row_id'],
                                     'family': rec['family'], 'weight': str(weight)})

            pay(choose('source-IC', i), alpha)
            for tail in branch['ordered_tail_labels'][:-1]:
                pay(choose('actual-source-SAFE', i, tail, i), sy)
                pay(choose('same-P-MAX', i, tail), ay)
            terminal = branch['ordered_tail_labels'][-1]
            pay(choose('actual-source-SAFE', i, terminal, i), st)
            pay(choose('same-P-MAX', i, terminal), at)
            pay(choose('branch-terminal-BR', i, query), F(1))
            combined = {}
            for payment in payments:
                for j, a in ge[payment['unique_row_id']]['row']:
                    add(combined, j, F(payment['weight']) * F(a))
            nonnegative_mu = []
            all_state_E = []
            for offset, c in enumerate(cols):
                if c['source_player'] != i:
                    continue
                h = hist[c['hist_column']]
                b = h['actual_backgrounds'][i - 1]
                k = h['P'] - b
                q = (F(int(h['actual_bits'][query['player'] - 1])) if query['kind'] == 'actual' else
                     F(h['indexed_membership_counts'][query['family']], 6))
                E = remainder(i, b, k, c['X_bit'], c['middle_bits'], c['terminal_bit'], q)
                # Linearity in q is the exact six-query averaging argument.
                E0 = remainder(i, b, k, c['X_bit'], c['middle_bits'], c['terminal_bit'], F(0))
                E1 = remainder(i, b, k, c['X_bit'], c['middle_bits'], c['terminal_bit'], F(1))
                assert E == (1 - q) * E0 + q * E1 and E >= 0
                j = old_count + offset
                add(combined, j, E)
                all_state_E.append([j, str(E)])
                if E:
                    nonnegative_mu.append([j, str(E)])
            equality_payments = []
            for h in hist:
                for x in (0, 1):
                    mass_row = eq_by_name[(i, h, x)]
                    indices = [j for j, a in mass_row['row'] if j >= old_count]
                    coefficients = {combined.get(j, F()) for j in indices}
                    assert len(coefficients) == 1, ('tail-dependent mass remainder', i, query, h, x)
                    weight = -next(iter(coefficients))
                    equality_payments.append({'equality_row_id': mass_row['id'], 'weight': str(weight)})
                    for j, a in mass_row['row']:
                        add(combined, j, weight * F(a))
            assert combined == target
            certificates.append({'id': len(certificates), 'source_player': i, 'C': str(C), 'query': query,
                                 'target_interface_file': str(INPUTS['H3_interface' if i == 4 else 'prefix_interface'].relative_to(WORK)),
                                 'target_row_name': target_source['name'], 'target_row': sparse(target),
                                 'nonnegative_budget_payments': payments,
                                 'nonnegative_mu_payments': nonnegative_mu,
                                 'all_source_mu_remainders_including_zero': all_state_E,
                                 'signed_mass_equality_payments': equality_payments,
                                 'identity': 'target = sum(weight*generated >= row) + sum(E_mu*mu) + sum(weight*generated mass equality)',
                                 'all_hidden_coefficients_canceled': True,
                                 'target_matches_frozen_interface_exactly': True})
    assert len(certificates) == 36
    assert hashes == {k: sha256(p.read_bytes()).hexdigest() for k, p in INPUTS.items()}
    save('visible_prefix_projection.json.gz', {
        'schema': 'early-shared-X-visible-prefix-projection/v1', 'status': 'EXACT_36_IDENTITIES_NO_SOLVE',
        'input_sha256': hashes, 'universal_remainder_domain_counts': universal_counts,
        'certificates': certificates, 'scope': 'Only 6 actual labels and 3 six-index means per source: 27 C* plus 9 H3 rows.',
        'omitted_queries': 'The eight R/Z/H old query orbits are not present in this hidden-tail layer; no implication of all 51 or all 17 interface rows is claimed.',
        'optimizer_calls': 0, 'point_values_read': False, 'append_input_bytes_unchanged': True})
    save('visible_prefix_all_type_remainders.json.gz', {
        'scope': 'All real (b,k,x,ordered middle bits,t,q) Boolean domains for i=1,2,3,4; no sampled customer support or point values.',
        'counts': universal_counts, 'all_1568_nonnegative': True, 'records': all_type_records})
    report = {'status': 'PASS', 'projected_rows': 36, 'C_star_rows': 27, 'H3_rows': 9,
              'hidden_state_remainders_checked_in_identities': sum(len(v['all_source_mu_remainders_including_zero']) for v in certificates),
              'universal_boolean_remainders': len(all_type_records), 'universal_counts': universal_counts,
              'mass_equality_payments': sum(len(v['signed_mass_equality_payments']) for v in certificates),
              'all_target_rows_match_frozen_interfaces': True, 'all_1920_hidden_coordinates_cancel_per_identity': True,
              'excluded_RZH_query_orbits': 8, 'optimizer_calls': 0,
              'projection_sha256': sha256((HERE / 'visible_prefix_projection.json.gz').read_bytes()).hexdigest(),
              'inputs': {k: {'path': str(p.relative_to(WORK)), 'sha256': hashes[k]} for k, p in INPUTS.items()}}
    save('visible_prefix_projection_summary.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
