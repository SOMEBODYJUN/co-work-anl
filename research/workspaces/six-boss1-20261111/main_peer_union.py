"""Main's exact union of already reviewed fixed peer rows.

This audits finite row transport and current signs.  The discounted, PAIR,
portfolio and neighbour-bridge proofs are reviewed separately, not proved by
their source matrix's feasible point.  Positive scaling is used only for
deduplication; every exported coefficient retains its original value.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import gzip
import json

WS = Path(__file__).resolve().parent
REPO = WS.parents[2]
PEER = REPO / 'research/workspaces/six-boss2-20261111-cross/master_cuts'
OUT = WS / 'peer_union_transfer'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(raw):
    raw = raw['nonzero'] if isinstance(raw, dict) else raw
    result = sorted((int(i), F(v)) for i, v in raw if F(v))
    assert len({i for i, _ in result}) == len(result)
    return result


def normalized(raw):
    result = canonical(raw)
    scale = abs(result[0][1]) if result else F(1)
    return tuple((i, str(v/scale)) for i, v in result)


def main():
    paths = [WS/'peer_augmented_lp/exact_matrix.json.gz', WS/'peer_augmented_lp/augmented_lp_exact.json',
             PEER/'dynamic_5799_matrix.json.gz', PEER/'dynamic_5799_exact.json']
    pins = ['6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9',
            'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f',
            '0b4bd0a81097b022a638fdc44324c731768255579a5bf07618e12c35c9342bec',
            '63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1']
    assert list(map(digest, paths)) == pins
    ours, point, peer, oldpoint = [json.loads(gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes()) for p in paths]
    assert len(ours['rows']) == 19621 and len(ours['columns']) == 15593
    assert len(peer['rows']) == 5799 and len(peer['columns']) == 4849
    assert ours['columns'][:4849] == peer['columns']
    assert ours['columns'] == [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']]
    assert peer['columns'] == [{k: v for k, v in c.items() if k != 'weight'} for c in oldpoint['columns']]
    for name in ('objective', 'normalization'):
        assert list(map(F, ours[name][:4849])) == list(map(F, peer[name]))
        assert not any(map(F, ours[name][4849:]))
    assert all(normalized(ours['rows'][i]) == normalized(peer['rows'][i]) for i in range(5692))
    x, oldx = [[F(c['weight']) for c in p['columns']] for p in (point, oldpoint)]
    original = {}
    for i, row in enumerate(ours['rows']):
        if all(j < 4849 for j, v in row):
            original.setdefault(normalized(row), i)
    records, mapping, seen = [], [], set()
    all_current, all_old = [], []
    for i, row in enumerate(peer['rows']):
        assert i == row['index']
        raw = canonical(row)
        assert all(0 <= j < 4849 for j, _ in raw)
        old_slack = sum((v*oldx[j] for j, v in raw), F())
        current = sum((v*x[j] for j, v in raw), F())
        assert old_slack >= 0
        all_current.append(current); all_old.append(old_slack)
        key = normalized(row)
        if key in original:
            j = original[key]
            other = canonical(ours['rows'][j])
            scale = raw[0][1]/other[0][1] if raw else F(1)
            assert scale > 0 and raw == [(k, scale*v) for k, v in other]
            mapping.append({'peer_row': i, 'existing_row': j, 'positive_scale': str(scale)})
        else:
            assert key not in seen
            seen.add(key)
            vector = [[j, str(v)] for j, v in raw]
            label = 'peer5799:'+str(i)+':'+row['name']
            records.append({'name': label, 'source_matrix_row': i, 'source_row_name': row['name'],
                            'source_matrix': str(paths[2].relative_to(REPO)), 'source_matrix_sha256': pins[2],
                            'source_point_sha256': pins[3], 'original_exact_slack': str(old_slack),
                            'slack': str(current), 'slack_float': float(current), 'coefficients': vector,
                            'vector_sha256': sha256(json.dumps(vector, separators=(',', ':')).encode()).hexdigest(),
                            'all_auxiliary_coefficients_zero': True})
            mapping.append({'peer_row': i, 'new_row_name': label, 'positive_scale': '1'})
    assert len(records) == 40 and sum(F(r['slack']) < 0 for r in records) == 5
    OUT.mkdir(exist_ok=True)
    package = {'scope': 'All forty rows absent up to positive scaling from the fully preserved reviewed peer5799 finite system; original support only, no new mathematical mechanism or SPE claim.',
               'point': str(paths[1].relative_to(REPO)), 'point_sha256': pins[1],
               'matrix': str(paths[0].relative_to(REPO)), 'matrix_sha256': pins[0],
               'original_columns': 4849, 'columns': 15593, 'baseline_rows': 19621,
               'input_records': 40, 'distinct_rows': 40, 'negative_rows': 5,
               'selected_rows': records,
               'sources': [{'path': str(p.relative_to(REPO)), 'sha256': h} for p, h in zip(paths, pins)]}
    target = OUT/'all_missing_rows_19621.json'
    target.write_text(json.dumps(package, ensure_ascii=False, indent=2)+'\n')
    report = {'scope': 'Exact arithmetic/provenance and positive-scaling row inclusion audit, not a substitute for the separately reviewed mathematical row contracts.',
              'all_4849_descriptors_equal': True, 'original_5692_rows_equal_up_to_positive_scale': True,
              'objectives_and_normalization_equal': True, 'all_5799_source_primal_rows_nonnegative': True,
              'minimum_source_slack': str(min(all_old)), 'minimum_current_peer_slack': str(min(all_current)),
              'old_peer_rows': 5799, 'represented_in_existing_system': len(original.keys() & {normalized(r) for r in peer['rows']}),
              'new_distinct_rows': len(records), 'new_negative_rows': 5,
              'negative_names': [r['name'] for r in records if F(r['slack']) < 0],
              'package_sha256': digest(target), 'source_sha256': digest(Path(__file__)),
              'row_inclusion': mapping, 'sources': package['sources']}
    (OUT/'audit_19621.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('row_inclusion', 'sources')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
