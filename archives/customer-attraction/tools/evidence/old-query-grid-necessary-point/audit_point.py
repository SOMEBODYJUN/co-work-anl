"""Decode the frozen 4971-row point; no imports of author builders or solvers.

All columns are checked against the explicit coordinate construction.  This
does not rebuild or certify the 4927 inherited rows.  Only 36 appended floors,
8 saved grid cuts, and local mass bounds are evaluated here.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations
from pathlib import Path
import argparse
import json

POINT_SHA = '0c06316a0ad5b4079c54d36cf59255c36943af957644b0ffab1b34a249ee6f7c'
FLOOR_SHA = 'f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314'
GRID_SHA = '755ba74498e07b2372630b165885055529776434c96c8c64a1eed20943923884'
CONT_SHA = 'e9ce9c66ea5598038ad7f5aa19cfab44d5156c8e35b3081665481153a968c4fa'
PAT = tuple(product((0, 1), repeat=3))
STATES = ((0, 1), (1, 0), (1, 1))
ORBITS = ((0, 0), (1, 0), (1, 1))


def read(path, expected=None):
    data = path.read_bytes()
    if expected is not None:
        assert sha256(data).hexdigest() == expected, path
    return json.loads(data)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def share(a, s):
    return F(a, s) if a else F()


def main():
    if not __debug__:
        raise RuntimeError('Assertions must remain enabled for this audit')
    p = argparse.ArgumentParser()
    p.add_argument('--repository', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    args = p.parse_args()
    evidence = args.repository / 'archives/customer-attraction/tools/evidence'
    primary = evidence / 'continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json'
    point = read(primary, POINT_SHA)
    previous = read(evidence / 'all-reply-actual-floors-program/related/all_reply_floors_exact.json', FLOOR_SHA)
    grid = read(evidence / 'old-query-grid-cut-data/original/old_query_cuts.json', GRID_SHA)
    continuous = read(evidence / 'continuous-old-query-cuts-program/related/continuous_old_query_cuts.json', CONT_SHA)
    prior_audit_path = evidence / 'continuous-old-query-cuts-program/replay/local-row-audit.json'
    prior_audit = read(prior_audit_path)
    assert prior_audit['point_sha256'] == POINT_SHA and prior_audit['cuts_sha256'] == CONT_SHA
    fields = {'scope', 'base_rows', 'first_raw_rows', 'additional_index_class_rows', 'O', 'W',
              'strict_half_gap', 'verified_rows', 'minimum_slack', 'positive_columns',
              'additional_new_reply_floors', 'columns'}
    assert set(point) == fields
    assert (point['base_rows'], point['first_raw_rows'], point['additional_index_class_rows'],
            point['additional_new_reply_floors'], point['verified_rows']) == (702, 37, 100, 36, 4971)
    cols = point['columns']; masses = [F(c['weight']) for c in cols]
    assert len(cols) == 1905 and min(masses) >= 0
    assert sum(w > 0 for w in masses) == point['positive_columns'] == 176
    schemas = {
        'K': {'kind', 'weight'},
        'hist': {'kind', 'weight', 'actual_bits', 'd', 'hist'},
        'joint-reply': {'kind', 'weight', 'hist_column_old', 'group', 'state'},
        'overlap': {'kind', 'weight', 'hist_column', 'groups'},
    }
    for c in cols:
        assert set(c) == schemas[c['kind']]
        assert isinstance(c['weight'], str)
    kinds = Counter(c['kind'] for c in cols)
    assert kinds == {'K': 1, 'hist': 16, 'joint-reply': 582, 'overlap': 1306}
    expected = [{'kind': 'K'}]
    hist_data = []; old_index = 1; position = 1; group_records = []
    utilities = [F()] * 6; O = F(); W = F(); total = F()
    for hist_order in range(16):
        c = cols[position]; assert c['kind'] == 'hist'
        a = tuple(map(int, c['actual_bits'])); H = tuple(c['hist']); x = masses[position]
        assert len(a) == 6 and all(v in (0, 1) for v in a)
        assert len(H) == 8 and all(type(v) is int and v >= 0 for v in H) and sum(H) == 6
        assert c['d'] == sum(n*w[0] for n, w in zip(H, PAT))
        assert 0 <= c['d'] <= 6
        hi = position; position += 1
        expected.append({k: v for k, v in c.items() if k != 'weight'})
        words = [w for w, n in zip(PAT, H) for _ in range(n)]
        # Enumerate all literal ordered index edges, independent of H_w H_v formulas.
        counts = Counter((f, int(i == j), words[i], words[j])
                         for f, i, j in product(range(2), range(6), range(6)) if f or i != j)
        assert {o: sum(n for g, n in counts.items() if g[:2] == o) for o in ORBITS} == {(0, 0): 30, (1, 0): 30, (1, 1): 6}
        groups = {}
        for g in sorted(counts):
            state_mass = {}
            for st in STATES:
                descriptor = {'kind': 'joint-reply', 'hist_column_old': old_index,
                              'group': [g[0], g[1], list(g[2]), list(g[3])], 'state': list(st)}
                expected.append(descriptor)
                assert {k:v for k,v in cols[position].items() if k != 'weight'} == descriptor
                state_mass[st] = masses[position]; position += 1
            z01, z10, z11 = [state_mass[st] for st in STATES]
            z00 = x-z01-z10-z11; assert z00 >= 0
            groups[g] = {'states': state_mass, 'R': z10+z11, 'Z': z01+z11}
            group_records.append({'hist_ordinal': hist_order, 'hist_column': hi, 'hist_column_old': old_index,
                                  'group': [g[0], g[1], list(g[2]), list(g[3])], 'multiplicity': counts[g],
                                  'm00': str(z00), 'm01': str(z01), 'm10': str(z10), 'm11': str(z11),
                                  'R': str(z10+z11), 'Z': str(z01+z11)})
        for i in range(6): utilities[i] += x*share(a[i], sum(a))
        O += x*int(c['d'] > 0); W += x*int(any(a)); total += x
        hist_data.append({'ordinal': hist_order, 'column': hi, 'old_column': old_index,
                          'actual_bits': c['actual_bits'], 'd': c['d'], 'hist': c['hist'],
                          'mass': x, 'a': a, 'counts': counts, 'groups': groups})
        old_index += 1+len(groups)
    joint_end = position; overlap_details = []; below_frechet = []; positive_overlaps = []
    for h in hist_data:
        for g, gg in combinations(sorted(h['groups']), 2):
            descriptor = {'kind': 'overlap', 'hist_column': h['column'],
                          'groups': [[g[0], g[1], list(g[2]), list(g[3])],
                                     [gg[0], gg[1], list(gg[2]), list(gg[3])]]}
            expected.append(descriptor)
            assert {k:v for k,v in cols[position].items() if k != 'weight'} == descriptor
            v = masses[position]; r = h['groups'][g]['R']; rr = h['groups'][gg]['R']
            upper = min(r, rr); lower = max(F(), r+rr-h['mass'])
            assert v <= upper
            record = {'column': position, 'hist_column': h['column'], 'weight': str(v),
                      'upper': str(upper), 'frechet_lower': str(lower), 'upward_lift': str(upper-v)}
            overlap_details.append(record)
            if v < lower: below_frechet.append(record)
            if v > 0: positive_overlaps.append(record)
            position += 1
    assert position == len(cols) and len(group_records) == 194 and len(overlap_details) == 1306
    assert expected == [{k:v for k,v in c.items() if k != 'weight'} for c in cols]
    assert O == F(point['O']) == 1 and W == F(point['W']) == sum(utilities) and W < F(1, 2)
    assert O-2*W == F(point['strict_half_gap'])
    floors = []
    for i, member, orbit in product(range(6), range(2), ORBITS):
        n = 6 if orbit[1] else 30
        v = n*utilities[i]
        for h in hist_data:
            for g, mult in h['counts'].items():
                if g[:2] == orbit:
                    v -= mult*h['groups'][g]['R' if member == 0 else 'Z'] / (sum(h['a'][:i])+6-i)
        assert v >= 0
        floors.append({'key': [i, member, *orbit], 'slack': str(v)})
    cuts = []
    for ordinal, item in enumerate(grid['selected']):
        i, member, f, diag, qi, mode, aa, mu = item['cut']
        assert (i, member, aa, mu) == (4, 1, '1', '1') and mode in ('all', 'last')
        v = (6 if diag else 30)*(utilities[4]+utilities[5])
        for h in hist_data:
            b = sum(h['a'][:4]); D = (b+1)*(b+2)
            for g, mult in h['counts'].items():
                if g[:2] != (f, diag): continue
                q = (g[2]+g[3])[qi]
                psi0 = F(q, b+1)-F(h['a'][4], D)
                delta = F(1, b+1)-F(q, D)
                v -= mult*(h['mass']*psi0+h['groups'][g]['Z']*delta)
        assert v >= 0
        cuts.append({'ordinal': ordinal, 'cut': item['cut'], 'current_slack': str(v),
                     'preceding_floor_point_slack': item['slack']})
    assert len(cuts) == 8
    assert len(previous['columns']) == len(cols)
    assert [{k:v for k,v in c.items() if k!='weight'} for c in previous['columns']] == expected
    changes = [{'column': j, 'kind': c['kind'], 'previous': previous['columns'][j]['weight'], 'current': c['weight']}
               for j,c in enumerate(cols) if F(c['weight']) != F(previous['columns'][j]['weight'])]
    assert len(changes) == 114 and Counter(c['kind'] for c in changes) == {'joint-reply': 62, 'overlap': 52}
    assert previous['O'] == point['O'] and previous['W'] == point['W']
    saved_rows = prior_audit['row_results']
    assert len(saved_rows) == len(continuous['selected']) == 64
    for row, saved in zip(saved_rows, continuous['selected']):
        assert row['cut'] == saved['cut'] and row['exact_slack'] == saved['slack'] and F(saved['slack']) < 0
    report = {
        'status': 'PASS', 'scope': 'Complete field/coordinate decoding, local mass constraints, direct welfare and 44 appended row evaluations; no inherited 4927/full 4971 build, optimization or discovery.',
        'primary_sha256': POINT_SHA, 'bytes': primary.stat().st_size,
        'top_level_fields': sorted(point), 'original_metadata': {k:v for k,v in point.items() if k!='columns'},
        'column_kinds': dict(kinds), 'positive_by_kind': dict(Counter(c['kind'] for c,v in zip(cols,masses) if v>0)),
        'zero_columns': sum(v==0 for v in masses), 'all_weights_nonnegative': True,
        'all_1905_descriptors_reconstructed': True, 'descriptor_sha256': sha256(canonical(expected).encode()).hexdigest(),
        'old_base_columns': old_index, 'joint_base_columns': joint_end,
        'histogram_mass': str(total), 'K': str(masses[0]), 'O': str(O), 'W': str(W),
        'O_minus_2W': str(O-2*W), 'O_over_2_minus_W': str(O/2-W), 'actual_utilities': list(map(str,utilities)),
        'histograms': [{k:(str(v) if isinstance(v,F) else v) for k,v in h.items() if k not in ('a','counts','groups')}
                       | {'joint_groups':len(h['groups']), 'overlap_pairs':len(h['groups'])*(len(h['groups'])-1)//2}
                       for h in hist_data],
        'joint_groups': len(group_records), 'implicit_m00_zero': sum(F(g['m00'])==0 for g in group_records),
        'overlap_upper_constraints_checked': 2*len(overlap_details),
        'overlap_saturated_minimum': sum(F(v['upward_lift'])==0 for v in overlap_details),
        'overlap_strictly_below_minimum': sum(F(v['upward_lift'])>0 for v in overlap_details),
        'stored_overlap_below_frechet_count': len(below_frechet),
        'stored_overlap_below_frechet_lower': below_frechet,
        'positive_overlaps': positive_overlaps,
        'floors36': floors, 'floors_zero': sum(F(x['slack'])==0 for x in floors),
        'grid8': cuts, 'grid_zero': sum(F(x['current_slack'])==0 for x in cuts),
        'preceding_point_sha256': FLOOR_SHA, 'coordinate_changes_count':len(changes),
        'coordinate_changes_by_kind':dict(Counter(c['kind'] for c in changes)),
        'preceding_positive_columns': previous['positive_columns'],
        'prior_64cut_audit': {'path': str(prior_audit_path.relative_to(args.repository)),
                            'sha256': sha256(prior_audit_path.read_bytes()).hexdigest(),
                            'all_64_saved_records_compared_to_prior_audit': True,
                            'minimum_slack':prior_audit['minimum_saved_slack'],
                            'maximum_slack':prior_audit['maximum_saved_slack'],
                            'row_coefficients_rerun_here': False},
        'original_entrypoints_executed': 0, 'original_full_graph_rebuilt': False,
    }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'point-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (args.out/'joint-state-ledger.json').write_text(json.dumps(group_records,indent=2)+'\n')
    (args.out/'coordinate-delta.json').write_text(json.dumps(changes,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','column_kinds','positive_by_kind','zero_columns','O','W','joint_groups','overlap_upper_constraints_checked','overlap_saturated_minimum','overlap_strictly_below_minimum','stored_overlap_below_frechet_count','floors_zero','grid_zero','coordinate_changes_count']},indent=2))


if __name__ == '__main__':
    main()
