"""Independent exact reading and structural audit of the saved 1905-column point.

This does not import the original graph builder, solve an LP, or certify all
5075 rows. Full metadata and all weights are read, not only nonzero support.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
SOURCE = None
SHA = 'abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246'
PAT = tuple(product((0, 1), repeat=3))


def group(raw):
    f, d, wi, wj = raw
    assert f in (0, 1) and d in (0, 1) and (f or not d)
    assert tuple(wi) in PAT and tuple(wj) in PAT
    return f, d, tuple(wi), tuple(wj)


def multiplicity(g, hist):
    _, diag, wi, wj = g
    ni, nj = hist[PAT.index(wi)], hist[PAT.index(wj)]
    return ni if diag else ni * nj - (ni if wi == wj else 0)


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    raw = SOURCE.read_bytes()
    assert len(raw) == 816661 and hashlib.sha256(raw).hexdigest() == SHA
    p = json.loads(raw)
    assert set(p) == {'scope', 'base_rows', 'first_raw_rows', 'additional_index_class_rows',
                      'O', 'W', 'strict_half_gap', 'verified_rows', 'minimum_slack',
                      'positive_columns', 'continuous_cut_rows', 'columns'}
    assert (p['base_rows'], p['first_raw_rows'], p['additional_index_class_rows'],
            p['verified_rows'], p['minimum_slack']) == (5043, 37, 100, 5075, '0')
    assert p['continuous_cut_rows'] == 32
    cols = p['columns']
    assert len(cols) == 1905 and cols[0]['kind'] == 'K'
    assert all(isinstance(c['weight'], str) for c in cols)
    weights = [F(c['weight']) for c in cols]
    assert min(weights) >= 0 and sum(w > 0 for w in weights) == p['positive_columns'] == 179
    assert set(cols[0]) == {'kind', 'weight'}
    k = weights[0]
    hist = {}
    hi = None
    kind_counts = Counter()
    positive_counts = Counter()
    for i, c in enumerate(cols):
        kind_counts[c['kind']] += 1
        positive_counts[c['kind']] += weights[i] > 0
        if c['kind'] == 'hist':
            assert set(c) == {'kind', 'actual_bits', 'd', 'hist', 'weight'}
            assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'}
            assert len(c['hist']) == 8 and all(isinstance(n, int) and n >= 0 for n in c['hist'])
            assert sum(c['hist']) == 6
            assert c['d'] == sum(n*w[0] for n, w in zip(c['hist'], PAT)) == 1
            hi = i
            hist[i] = {'column': c, 'mass': weights[i], 'states': {}, 'old_id': None}
        elif c['kind'] == 'joint-reply':
            assert set(c) == {'kind', 'hist_column_old', 'group', 'state', 'weight'}
            assert hi is not None and len(hist) <= 16
            h = hist[hi]
            if h['old_id'] is None:
                h['old_id'] = c['hist_column_old']
            assert h['old_id'] == c['hist_column_old']
            g, st = group(c['group']), tuple(c['state'])
            assert st in {(0, 1), (1, 0), (1, 1)}
            states = h['states'].setdefault(g, {})
            assert st not in states
            states[st] = weights[i]
        else:
            assert c['kind'] in ('K', 'overlap')
    assert kind_counts == {'K': 1, 'hist': 16, 'joint-reply': 582, 'overlap': 1306}
    implicit = []
    expected_old_hist_column = 1
    for h in hist.values():
        assert h['old_id'] == expected_old_hist_column
        expected_old_hist_column += 1 + len(h['states'])
        words = tuple(word for n, word in zip(h['column']['hist'], PAT) for _ in range(n))
        expected = {(f, int(i == j), words[i], words[j])
                    for f, i, j in product(range(2), range(6), range(6)) if f or i != j}
        assert set(h['states']) == expected
        h['R'], h['Z'] = {}, {}
        for g, st in h['states'].items():
            assert set(st) == {(0, 1), (1, 0), (1, 1)}
            q00 = h['mass'] - sum(st.values())
            assert q00 >= 0
            implicit.append(q00)
            h['R'][g] = st[1, 0] + st[1, 1]
            h['Z'][g] = st[0, 1] + st[1, 1]
        assert sum(multiplicity(g, h['column']['hist']) for g in expected) == 66
    assert len(implicit) == 194
    overlaps, overlap_slacks = {}, []
    literal_intersection_obstructions = []
    for i, c in enumerate(cols):
        if c['kind'] != 'overlap':
            continue
        assert set(c) == {'kind', 'hist_column', 'groups', 'weight'}
        hc = c['hist_column']
        assert hc in hist and len(c['groups']) == 2
        g1, g2 = map(group, c['groups'])
        assert g1 != g2 and g1 in hist[hc]['R'] and g2 in hist[hc]['R']
        key = hc, frozenset((g1, g2))
        assert key not in overlaps
        overlaps[key] = weights[i]
        lower = max(F(), hist[hc]['R'][g1] + hist[hc]['R'][g2] - hist[hc]['mass'])
        if weights[i] < lower:
            literal_intersection_obstructions.append({
                'column': i, 'hist_column': hc, 'hist_mass': str(hist[hc]['mass']),
                'groups': c['groups'], 'R_masses': [str(hist[hc]['R'][g1]), str(hist[hc]['R'][g2])],
                'saved_overlap': str(weights[i]), 'frechet_lower_bound': str(lower),
                'lower_minus_saved': str(lower-weights[i])})
        for g in (g1, g2):
            slack = hist[hc]['R'][g] - weights[i]
            assert slack >= 0
            overlap_slacks.append(slack)
    expected_pairs = {(hc, frozenset(gs)) for hc, h in hist.items()
                      for gs in combinations(h['states'], 2)}
    assert set(overlaps) == expected_pairs and len(overlap_slacks) == 2612
    total = sum((h['mass'] for h in hist.values()), F())
    welfare = sum((h['mass'] for h in hist.values() if '1' in h['column']['actual_bits']), F())
    assert total == F(p['O']) == 1 and welfare == F(p['W'])
    assert 1 - 2*welfare == F(p['strict_half_gap']) > 0
    profits = [sum((h['mass']*F(int(h['column']['actual_bits'][j]),
                                   sum(map(int, h['column']['actual_bits'])))
                    for h in hist.values() if '1' in h['column']['actual_bits']), F())
               for j in range(6)]
    assert sum(profits) == welfare
    capacities = []
    for family, diag in ((0, 0), (1, 0), (1, 1)):
        count = 6 if diag else 30
        for reply in ('R', 'Z'):
            amount = sum((multiplicity(g, h['column']['hist'])*v
                          for h in hist.values() for g, v in h[reply].items()
                          if g[:2] == (family, diag)), F())
            slack = count*k - amount
            assert slack >= 0
            capacities.append({'reply': reply, 'family': family, 'diagonal': diag,
                               'indexed_themes': count, 'total_theme_mass': str(amount),
                               'capacity_slack': str(slack)})
    old_floors = []
    for word_bit, name in ((1, 'B'), (2, 'C')):
        for j in range(6):
            price = sum((h['mass'] * sum(n*w[word_bit] for n, w in zip(h['column']['hist'], PAT))
                         / (sum(map(int, h['column']['actual_bits'][:j]))+6-j)
                         for h in hist.values()), F())
            slack = 6*profits[j]-price
            assert slack >= 0
            old_floors.append({'reply': name, 'actual_player': j+1, 'slack': str(slack)})
    new_floors = []
    for family, diag in ((0, 0), (1, 0), (1, 1)):
        count = 6 if diag else 30
        for reply in ('R', 'Z'):
            for j in range(6):
                price = sum((multiplicity(g, h['column']['hist'])*v
                             / (sum(map(int, h['column']['actual_bits'][:j]))+6-j)
                             for h in hist.values() for g, v in h[reply].items()
                             if g[:2] == (family, diag)), F())
                slack = count*profits[j]-price
                assert slack >= 0
                new_floors.append({'reply': reply, 'family': family, 'diagonal': diag,
                                   'actual_player': j+1, 'slack': str(slack)})
    saturation = Counter()
    for (hc, pair), value in overlaps.items():
        a, b = pair
        top = min(hist[hc]['R'][a], hist[hc]['R'][b])
        saturation['equal_to_minimum_R_marginal'] += int(value == top)
        saturation['strictly_below_minimum_R_marginal'] += int(value < top)
    summary = []
    for hc, h in hist.items():
        summary.append({'hist_column': hc, 'hist_column_old': h['old_id'],
                        'actual_bits': h['column']['actual_bits'], 'hist': h['column']['hist'],
                        'mass': str(h['mass']), 'groups': len(h['states']),
                        'positive_joint_states': sum(v > 0 for s in h['states'].values() for v in s.values())})
    assert len(literal_intersection_obstructions) == 165
    example = next(x for x in literal_intersection_obstructions if x['column'] == 992)
    assert example['R_masses'] == [example['hist_mass']]*2 and F(example['saved_overlap']) == 0
    return {'status': 'PASS_EXACT_RELAXED_STRUCTURE_AND_REPLY_FLOORS',
            'scope': 'All 1905 column records; nonnegativity, all 194 implicit 00 masses, 2612 overlap upper bounds, six split R/Z capacities, twelve actual B/C safety floors, 36 actual R/Z safety floors, norm and welfare. Not original all-5075-row replay.',
            'source_sha256': SHA, 'source_bytes': len(raw), 'python_version': sys.version,
            'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'top_level_metadata': {key: value for key, value in p.items() if key != 'columns'},
            'column_counts': dict(kind_counts), 'positive_counts': dict(positive_counts),
            'histograms': summary, 'minimum_implicit_00': str(min(implicit)),
            'overlap_upper_bounds_checked': len(overlap_slacks),
            'minimum_overlap_upper_slack': str(min(overlap_slacks)),
            'normalization_O': str(total), 'actual_W': str(welfare),
            'strict_half_gap': str(1-2*welfare), 'six_actual_payoffs': list(map(str, profits)),
            'K': str(k), 'split_capacities': capacities, 'actual_BC_safety_floors': old_floors,
            'actual_RZ_safety_floors': new_floors, 'overlap_saturation_counts': dict(saturation),
            'literal_intersection_diagnostic': {
                'scope': 'These are auxiliary relaxed overlaps, not all literal intersections of the given R marginals. This does not rule out replacing overlaps by minima or a different complete-game realization.',
                'frechet_lower_violations': len(literal_intersection_obstructions),
                'simple_example': example, 'all_violations': literal_intersection_obstructions},
            'reused_independent_implementation': 'combined-branch-master-point/audit_point.py; source identity and metadata adapted, all old hist indices checked, new R/Z floors and overlap saturation added',
            'not_certified': ['all original 5075 inequalities', 'exact optimality',
                              'a complete-history SPE', 'six-half counterexample']}


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    SOURCE = args.source
    report = run()
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'histograms','split_capacities','actual_BC_safety_floors','actual_RZ_safety_floors','literal_intersection_diagnostic'}},ensure_ascii=False,indent=2))
