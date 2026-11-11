"""Rebind the same 93 analytic rows to the certified complete624 opt_v2 point.

This uses the proved sorting/positive-part formulas, with no LP or parameter
grid.  Each selected affine piece is saved as a necessary row on the old
4849 columns.  All later auxiliary and 624 hidden columns have coefficient0.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

from boss1_transport_static_zz_v1 import (
    CURRENT, CURRENT_SHA, FAMILIES, HERE, ORBIT_SIZE, load, parse, serial,
)


def plus(row, j, value):
    if value:
        row[j] += value
        if not row[j]:
            del row[j]


def dot(row, values):
    return sum((v * values[j] for j, v in row.items()), F())


def qcols(ids, member):
    states = {'R': ((1, 0), (1, 1)), 'Z': ((0, 1), (1, 1)),
              'union': ((0, 1), (1, 0), (1, 1)), 'intersection': ((1, 1),)}[member]
    return [ids[s] for s in states]


def subtract_sorted_quote(row, ids, member, states, omega, masses):
    columns = qcols(ids, member)
    q = sum(masses[j] for j in columns)
    exact = q / 6
    for j in columns:
        plus(row, j, -omega / 6)
    for k in range(1, 6):
        high = [j for j, _, denom, _, _ in states if denom > k]
        high_mass = sum(masses[j] for j in high)
        positive = max(F(), q - high_mass)
        exact += positive / (k * (k + 1))
        if positive:
            scale = omega / (k * (k + 1))
            for j in columns:
                plus(row, j, -scale)
            for j in high:
                plus(row, j, scale)
    # Independent descending-price filling of this scalar query.
    left = q
    greedy = F()
    for _, eta, denom, _, _ in sorted(states, key=lambda s: -s[2]):
        take = min(left, eta)
        greedy += take / denom
        left -= take
    assert left == 0 and greedy == exact
    return omega * exact


def main():
    output = HERE / 'boss1_transport_93_at624_v2.json'
    assert not output.exists()
    current_path = HERE.parent / 'master_cuts/complete624_actual4_R00_opt_v2_original4849_exact.json'
    full_path = HERE.parent / 'master_cuts/complete624_actual4_R00_opt_v2_exact.json'
    point, digest = load(current_path, '75cf981c8e9a6554b796735b3e96c7e1145f420addec0ba045b25a293139803c')
    full, full_sha = load(full_path, '02bcb92f33f7e7e4fac00a4c64fd39b0a4f0c68a736559c300bbfba255168817')
    assert len(full['columns']) == 12631 and len(point['columns']) == 4849
    assert full['columns'][:4849] == point['columns']
    assert point['parent_full_point_sha256'] == full_sha
    frozen_formula = HERE / 'boss1_transport_single_zz_v1.py'
    frozen_report = json.loads((HERE / 'boss1_transport_single_zz_v1.json').read_bytes())
    assert sha256(frozen_formula.read_bytes()).hexdigest() == frozen_report['script_sha256']
    _, masses, hist, groups, family, labels = parse(point)
    records = []
    for f in FAMILIES:
        terminal = sum(s[1] * s[3] for ss in family[f].values() for s in ss)
        for orbit in ORBIT_SIZE:
            queries = [('new-to-R',), ('new-to-Z',)]
            queries += [('Z-to-new', i, label) for i, label in enumerate(labels[f])]
            queries += [('new-to-RZ-equal',)]
            for query in queries:
                row = defaultdict(F)
                exact_cost = F()
                budget = F()
                if query[0] != 'Z-to-new':
                    coefficient = 2 if query[0] == 'new-to-RZ-equal' else 1
                    budget = coefficient * terminal
                    for ss in family[f].values():
                        for j, _, _, payoff, _ in ss:
                            plus(row, j, coefficient * payoff)
                for h, gs in groups.items():
                    p = sum(map(int, hist[h]['actual_bits'][:4]))
                    ss = family[f][h]
                    for g, (ids, rho, omega) in gs.items():
                        if g[:2] != orbit:
                            continue
                        if query[0] == 'Z-to-new':
                            oldpay = rho[1] / (p + 1) + rho[3] / (p + 2)
                            budget += omega * oldpay
                            plus(row, ids[0, 1], omega / (p + 1))
                            plus(row, ids[1, 1], omega / (p + 2))
                            y = sum(eta * member[query[1]] for _, eta, _, _, member in ss)
                            q = rho[2] + rho[3]
                            extra = max(F(), y - q)
                            exact_cost += omega * (y / (p + 2) + extra / ((p + 1) * (p + 2)))
                            for j, _, _, _, member in ss:
                                plus(row, j, -omega * member[query[1]] / (p + 2))
                            if extra:
                                scale = omega / ((p + 1) * (p + 2))
                                for j, _, _, _, member in ss:
                                    plus(row, j, -scale * member[query[1]])
                                for j in qcols(ids, 'R'):
                                    plus(row, j, scale)
                        else:
                            members = ('union', 'intersection') if query[0] == 'new-to-RZ-equal' else (query[0][-1],)
                            for member in members:
                                exact_cost += subtract_sorted_quote(row, ids, member, ss, omega, masses)
                slack = budget - exact_cost
                assert dot(row, masses) == slack
                records.append({'family': f, 'orbit': orbit, 'query': query,
                                'budget': budget, 'minimum_cost': exact_cost, 'slack': slack,
                                'slack_float': float(slack),
                                'row_nonzero': [[j, v] for j, v in sorted(row.items())]})
    singles = [r for r in records if r['query'][0] != 'new-to-RZ-equal']
    pairs = [r for r in records if r['query'][0] == 'new-to-RZ-equal']
    assert len(singles) == 81 and len(pairs) == 12
    summary = {'input_sha256': digest, 'optimizer_calls': 0,
               'single_queries': 81, 'single_negative': sum(r['slack'] < 0 for r in singles),
               'equal_pairs': 12, 'pair_negative': sum(r['slack'] < 0 for r in pairs),
               'minimum_single': min(r['slack'] for r in singles),
               'minimum_pair': min(r['slack'] for r in pairs)}
    out = {**summary,
           'full_point_sha256': full_sha,
           'projection_equals_full_prefix_including_weights': True,
           'frozen_formula_source_sha256': frozen_report['script_sha256'],
           'scope': 'Static existing analytic minima only; no shared-transport feasibility or full SPE assertion',
           'column_domain': '4849 original columns; zero on ZZ auxiliaries and all 624 hidden columns',
           'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
           'records': records}
    output.write_text(json.dumps(serial(out), ensure_ascii=False, indent=2) + '\n')
    pack_path = HERE / 'boss1_transport_negative_rows_at624_v2.json'
    assert not pack_path.exists()
    pack = {'scope': 'Existing analytic terminal-query necessary rows; same certified complete624 point; not a new theorem or SPE counterexample',
            'input_sha256': digest, 'full_point_sha256': full_sha,
            'projection_equals_full_prefix_including_weights': True,
            'original_columns': 4849, 'zero_extension_to_columns': 12631,
            'direction': 'row dot x >= 0',
            'source_report_sha256': sha256(output.read_bytes()).hexdigest(),
            'cuts': [r for r in records if r['slack'] < 0]}
    pack_path.write_text(json.dumps(serial(pack), ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'negative_pack': str(pack_path), 'sha256': sha256(pack_path.read_bytes()).hexdigest()}, ensure_ascii=False))
    print(json.dumps(serial({**summary, 'output_sha256': sha256(output.read_bytes()).hexdigest(),
                             'negative_queries': [{k: r[k] for k in ('family', 'orbit', 'query', 'slack_float')}
                                                  for r in records if r['slack'] < 0]}), ensure_ascii=False))


if __name__ == '__main__':
    main()
