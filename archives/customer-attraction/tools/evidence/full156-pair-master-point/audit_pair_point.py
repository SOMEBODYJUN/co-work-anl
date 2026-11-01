"""Current exact audit of saved pair slabs and ONLY the 5236 added rows.

Does not import old generators, optimize, reconstruct the 5108 old rows,
generate either 156-topic matrix, or assert an SPE. Also creates a lossless
53-rational / 364-row representation whose decoded JSON bytes equal the source.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
PAIR = HERE / 'original/pair_master_exact.json'
MASTER = HERE.parent / 'full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'
EXPECTED = {
    PAIR: '090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2',
    MASTER: 'd1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8',
}
PAT = tuple(product((0, 1), repeat=3))


def partition(indices):
    seen = {}
    return tuple(seen.setdefault(i, len(seen)) for i in indices)


def group(raw):
    f, diag, wi, wj = raw
    return f, diag, tuple(wi), tuple(wj)


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled.')
    for path, sha in EXPECTED.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
    source = json.loads(PAIR.read_text())
    master = json.loads(MASTER.read_text())
    assert set(source) == {'scope', 'W', 'O', 'rows', 'original_Z_variables',
                           'overlap_variables', 'minimum_slack',
                           'free_vertex_variables', 'variables'}
    assert source['scope'] == 'complete cube feasible point after all chosen terminal and strong pair classes; not SPE'
    assert (source['rows'], source['original_Z_variables'], source['overlap_variables'],
            source['free_vertex_variables'], source['minimum_slack']) == (10344, 364, 2528, 80, '0')
    assert source['W'] == master['W'] and source['O'] == master['O'] == '1'
    rows = source['variables']
    assert len(rows) == 364

    # This is a complete, reversible reading representation, not a sparse summary.
    fractions = sorted({v[k] for v in rows for k in ('left', 'right', 'weight')})
    findex = {v: i for i, v in enumerate(fractions)}
    compact = []
    rebuilt = {k: v for k, v in source.items() if k != 'variables'}
    decoded = []
    for v in rows:
        assert set(v) == {'hist_column', 'left', 'right', 'group', 'r', 'weight'}
        f, diag, wi, wj = v['group']
        code = ''.join(map(str, (f, diag, *wi, *wj)))
        assert len(code) == 8 and set(code) <= {'0', '1'}
        entry = [v['hist_column'], findex[v['left']], findex[v['right']], code,
                 v['r'], findex[v['weight']]]
        compact.append(entry)
        hi, lo, up, code, r, yi = entry
        decoded.append({'hist_column': hi, 'left': fractions[lo], 'right': fractions[up],
                        'group': [int(code[0]), int(code[1]), list(map(int, code[2:5])),
                                  list(map(int, code[5:8]))],
                        'r': r, 'weight': fractions[yi]})
    rebuilt['variables'] = decoded
    encoded = (json.dumps(rebuilt, indent=2) + '\n').encode()
    assert encoded == PAIR.read_bytes()
    lossless = {'scope': 'Complete reversible reading of every original field and all 364 rows.',
                'source_sha256': EXPECTED[PAIR],
                'metadata_in_original_order': {k: v for k, v in source.items() if k != 'variables'},
                'rational_dictionary': fractions,
                'row_columns': ['hist_column', 'left_id', 'right_id', 'group_8_bits_f_diag_wi_wj', 'r', 'weight_id'],
                'rows': compact,
                'decoded_original_json_bytes_equal': True}

    hist = {}
    hi = None
    for j, col in enumerate(master['columns']):
        if col['kind'] == 'hist':
            hi = j
            hist[j] = {'row': col, 'mass': F(col['weight']), 'states': {}}
        elif col['kind'] == 'joint-reply':
            hist[hi]['states'].setdefault(group(col['group']), {})[tuple(col['state'])] = F(col['weight'])
    assert len(hist) == 16
    for h in hist.values():
        assert sum(h['row']['hist']) == 6
        assert sum(n * word[0] for n, word in zip(h['row']['hist'], PAT)) == 1
        for st in h['states'].values():
            assert set(st) == {(0, 1), (1, 0), (1, 1)}
            assert min(st.values()) >= 0 and sum(st.values()) <= h['mass']
        h['rad'] = {g: st[1, 0] + st[1, 1] for g, st in h['states'].items()}
    assert sum(h['mass'] for h in hist.values()) == 1
    assert sum((h['mass'] for h in hist.values() if '1' in h['row']['actual_bits']), F()) == F(source['W'])
    positive = {j: h for j, h in hist.items() if h['mass']}
    assert len(positive) == 10
    expected_metadata = []
    slabs = []
    cursor = 0
    hist_summary = []
    for j, h in positive.items():
        cuts = sorted({F(), h['mass'], *h['rad'].values()})
        words = tuple(word for word, n in zip(PAT, h['row']['hist']) for _ in range(n))
        edge_groups = {(f, int(i == k), words[i], words[k])
                       for f, i, k in product(range(2), range(6), range(6)) if f or i != k}
        assert edge_groups == set(h['rad'])
        start = cursor
        for lo, up in zip(cuts, cuts[1:]):
            assert up > lo
            slab = {'hist': j, 'left': lo, 'right': up, 'mass': up-lo, 'r': {}, 'y': {}}
            for g in h['rad']:
                r = int(up <= h['rad'][g])
                expected = {'hist_column': j, 'left': str(lo), 'right': str(up),
                            'group': [g[0], g[1], list(g[2]), list(g[3])], 'r': r}
                actual = rows[cursor]
                assert {k: v for k, v in actual.items() if k != 'weight'} == expected
                y = F(actual['weight'])
                assert 0 <= y <= slab['mass']
                slab['r'][g] = r
                slab['y'][g] = y
                expected_metadata.append(expected)
                cursor += 1
            slabs.append(slab)
        hist_summary.append({'hist_column': j, 'actual_bits': h['row']['actual_bits'],
                             'histogram': h['row']['hist'], 'mass': str(h['mass']),
                             'groups': len(h['rad']), 'slabs': len(cuts)-1,
                             'variables': cursor-start,
                             'positive_Z': sum(F(v['weight']) > 0 for v in rows[start:cursor])})
    assert cursor == 364 and len(slabs) == 29

    p4 = sorted({partition(x) for x in product(range(4), repeat=4)})
    assert len(p4) == 15
    classes = tuple(product(range(2), range(2), p4))
    zz = dict.fromkeys(classes, F())
    rz = dict.fromkeys(classes, F())
    zpair = dict.fromkeys(classes, F())
    multiplicities = {}
    for j, h in positive.items():
        words = tuple(word for word, n in zip(PAT, h['row']['hist']) for _ in range(n))
        edges = [(f, i, k) for f, i, k in product(range(2), range(6), range(6)) if f or i != k]
        assert len(edges) == 66
        counts = Counter()
        for f, i, k in edges:
            ge = (f, int(i == k), words[i], words[k])
            for ff, ii, kk in edges:
                gf = (ff, int(ii == kk), words[ii], words[kk])
                counts[(f, ff, partition((i, k, ii, kk)), ge, gf)] += 1
        assert sum(counts.values()) == 4356
        multiplicities[j] = counts

    overlap_count = upper_count = 0
    upper_minimum = None
    upper_zero = 0
    for slab in slabs:
        h = positive[slab['hist']]
        a = tuple(map(int, h['row']['actual_bits']))
        pa, total = sum(a[:4]), sum(a)
        den = (pa+1)*(pa+2)
        ha = (F(a[4]+a[5], total) if total else F()) + F(a[4], den)
        for ge, gf in combinations(slab['y'], 2):
            overlap_count += 1
            ov = min(slab['y'][ge], slab['y'][gf])
            for g in (ge, gf):
                slack = slab['y'][g]-ov
                assert slack >= 0
                upper_count += 1
                upper_zero += slack == 0
                upper_minimum = slack if upper_minimum is None else min(upper_minimum, slack)
        for (f, ff, pat, ge, gf), count in multiplicities[slab['hist']].items():
            key = f, ff, pat
            re = slab['r'][ge]
            ye, yf = slab['y'][ge], slab['y'][gf]
            zz[key] += count * (ye-yf) / (pa+1+re)
            rz[key] += count * (slab['mass']*(ha-F(re, pa+1))
                               - yf/F(pa+1) + re*yf/den)
            zpair[key] += count * (slab['mass']*ha-(ye+yf)/F(pa+1)
                                  + min(ye, yf)/den)
    assert overlap_count == 2528 and upper_count == 5056
    family_reports = {}
    for name, values in [('Z_to_Z', zz), ('PAIR_RZ', rz), ('PAIR_ZZ', zpair)]:
        assert len(values) == 60 and min(values.values()) >= 0
        family_reports[name] = {
            'rows': 60, 'minimum_slack': str(min(values.values())),
            'zero_rows': sum(v == 0 for v in values.values()),
            'all_slacks': [{'families': [f, ff], 'equality_pattern': pat, 'slack': str(v)}
                           for (f, ff, pat), v in values.items()]}
    weights = [F(v['weight']) for v in rows]
    uppers = [F(v['right'])-F(v['left']) for v in rows]
    stats = {'zero': sum(y == 0 for y in weights),
             'at_upper': sum(y == u for y, u in zip(weights, uppers)),
             'strict_interior': sum(0 < y < u for y, u in zip(weights, uppers)),
             'positive': sum(y > 0 for y in weights)}
    assert stats == {'zero': 183, 'at_upper': 101, 'strict_interior': 80, 'positive': 181}
    assert 5108+180+5056 == source['rows']
    report = {
        'status': 'PASS_CURRENT_SLAB_METADATA_AND_5236_ADDED_ROWS',
        'scope': 'All 364 variable metadata aligned with fixed combined hist/R; exact 60 Z->Z, 120 strong PAIR, 5056 min-overlap upper bounds and Z bounds. Not original 10344 replay; no 5108 old affine rows evaluated at changed Z.',
        'python_version': sys.version,
        'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_sha256': {str(p.relative_to(HERE.parent)): sha for p, sha in EXPECTED.items()},
        'primary_bytes': len(PAIR.read_bytes()), 'lossless_rational_dictionary_size': len(fractions),
        'all_364_row_metadata_matches_generated_slabs': True,
        'decoded_lossless_bytes_equal_original': True,
        'histogram_columns': 16, 'positive_histograms': 10, 'slabs': 29,
        'histogram_summary': hist_summary, 'Z_variables': 364, 'Z_position_statistics': stats,
        'min_overlap_variables': overlap_count, 'overlap_upper_bounds': upper_count,
        'minimum_overlap_upper_slack': str(upper_minimum), 'zero_overlap_upper_slacks': upper_zero,
        'added_row_families': family_reports, 'current_added_rows_checked': 5236,
        'old_rows_not_replayed_at_new_Z': 5108,
        'normalized_total_customer_mass': '1', 'every_hist_T_membership_count': 1,
        'actual_W': source['W'], 'OPT6_from_six_T_full_coverage': '1',
        'positive_half_gap': str(1-2*F(source['W'])),
        'free_vertex_field_matches_current_interior_count_only': True,
        'not_certified': ['original LP run', 'vertex basis or uniqueness', 'all 10344 rows anew',
                          'complete-history SPE', 'universal half counterexample'],
    }
    return report, lossless


if __name__ == '__main__':
    report, lossless = run()
    (HERE/'current-added-row-audit.json').write_text(json.dumps(report, indent=2)+'\n')
    (HERE/'lossless-variable-reading.json').write_text(json.dumps(lossless, indent=2)+'\n')
