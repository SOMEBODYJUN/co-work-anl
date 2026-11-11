#!/usr/bin/env python3
"""Re-evaluate and fully vector-deduplicate known early rows at one exact point.

The 4752 screening values and every full vector are computed independently.
All zero-mass columns remain in vectors; auxiliary coordinates extend by zero.
Frozen generators are imported read-only, with bytecode writing disabled.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
RESEARCH_WORKSPACES = RUN.parent
OLD = RUN/'cross_branch_math'
BOSS2 = RESEARCH_WORKSPACES/'six-boss2-20261111-cross'
sys.path.insert(0, str(OLD))
import new_theme_early_projections as early
import observed_first_branch_requery as observed
import direct_old_r_queries as direct


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sparse(row):
    row = row.items() if isinstance(row, dict) else row
    return [[int(i), str(F(v))] for i, v in sorted(row) if F(v)]


def key(row):
    return json.dumps(sparse(row), separators=(',', ':')).encode()


def summaries(records):
    out = {}
    for mechanism in sorted({r['mechanism'] for r in records}):
        group = [r for r in records if r['mechanism'] == mechanism]
        minimum = min(group, key=lambda r:F(r['slack']))
        out[mechanism] = {
            'records': len(group),
            'distinct_vectors': len({r['vector_sha256'] for r in group}),
            'negative': sum(F(r['slack']) < 0 for r in group),
            'zero': sum(F(r['slack']) == 0 for r in group),
            'strictly_positive': sum(F(r['slack']) > 0 for r in group),
            'records_identical_to_baseline': sum(bool(r['baseline_matches']) for r in group),
            'distinct_vectors_identical_to_baseline': len({r['vector_sha256'] for r in group if r['baseline_matches']}),
            'minimum_name': minimum['name'], 'minimum_slack': minimum['slack'],
            'minimum_slack_float': float(F(minimum['slack'])),
        }
    return out


def boss2_rows(point_path, point):
    """Rebuild the eleven frozen rows, rather than only trusting their vectors."""
    source_path = BOSS2/'master_cuts/merged_5716_exact.json'
    original_raw = source_path.read_bytes()
    original = json.loads(original_raw)
    desc = lambda c: {k: v for k, v in c.items() if k != 'weight'}
    assert [desc(c) for c in original['columns']] == [desc(c) for c in point['columns'][:4849]]
    sys.path.insert(0, str(BOSS2/'joint_requery'))
    import separate_master as pair
    sys.path.insert(0, str(BOSS2/'coverage_bridge'))
    import joint_discounted_requery as discounted
    pair_path = BOSS2/'joint_requery/selected_cuts_5716.json'
    pair_pack = json.loads(pair_path.read_text())
    assert pair_pack['source_sha256'] == sha(original_raw)
    blocks = pair.blocks_from_columns(point['columns'])
    out = []
    for index, r in enumerate(pair_pack['cuts']):
        parameters = {name:F(value) for name, value in r['weights'].items()}
        assert min(parameters.values()) >= 0
        row, au, aK, _ = pair.make_row(point['columns'], blocks, r['member'], tuple(r['orb']), r['query'], parameters)
        coeff = sparse(enumerate(row))
        assert key(coeff) == key(r['sparse_row'])
        out.append({'name': f'boss2-frozen-cross-pair:{index}', 'mechanism': 'boss2-cross-pair',
                    'fixed_input_row': index, 'fixed_pack': str(pair_path),
                    'parameters': r['weights'], 'source_weight_sum': '1',
                    'u6_coefficient': str(au), 'K_coefficient': str(aK),
                    'full_vector_rebuilt_equal': True, 'coefficients': coeff})
    discount_path = BOSS2/'coverage_bridge/new5716_joint_discounted.json'
    discount_pack = json.loads(discount_path.read_text())
    assert discount_pack['input_sha256'] == sha(original_raw)
    _, columns, histories, _, _ = discounted.read_input(point_path)
    for index, r in enumerate(discount_pack['results']):
        if 'row_nonzero' not in r:
            continue
        parameters = tuple(F(r['parameters'].get(n, '0')) for n in discounted.NAMES)
        assert min(parameters) >= 0
        row, projected_states = discounted.exact_row(columns, histories, r['source']-1, r['member'], tuple(r['orbit']), parameters, F(r['theta']))
        coeff = sparse(enumerate(row))
        assert key(coeff) == key(r['row_nonzero'])
        out.append({'name': f'boss2-frozen-discount:{index}', 'mechanism': 'boss2-discount',
                    'fixed_input_row': index, 'fixed_pack': str(discount_path),
                    'parameters': r['parameters'], 'theta': r['theta'],
                    'actual_source_zero_based': r['source']-1, 'member': r['member'],
                    'orbit': r['orbit'], 'full_projected_states': projected_states,
                    'full_vector_rebuilt_equal': True, 'coefficients': coeff})
    assert len(out) == 11
    return out, {'origin_point': str(source_path), 'origin_point_sha256': sha(original_raw),
                 'all_4849_descriptors_equal': True,
                 'packs': {str(p): sha(p.read_bytes()) for p in (pair_path, discount_path)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point', type=Path, default=RUN/'zz_closure_lp/augmented_lp_exact.json')
    ap.add_argument('--matrix', type=Path, default=RUN/'zz_closure_lp/exact_matrix.json.gz')
    ap.add_argument('--label', default='13931')
    ap.add_argument('--output-dir', type=Path, default=HERE)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw = args.point.read_bytes(); matrix_raw = args.matrix.read_bytes()
    point = json.loads(raw); matrix = json.loads(gzip.decompress(matrix_raw))
    columns, hist, weights, _, family, _ = early.topology(point)
    descriptors = [{k:v for k,v in c.items() if k != 'weight'} for c in columns]
    assert descriptors == matrix['columns']
    assert point['original_columns'] == 4849
    baseline = defaultdict(list)
    for i, row in enumerate(matrix['rows']):
        baseline[key(row)].append({'index': i, 'name': matrix['row_names'][i]})
    seeds, _ = early.screen(point, 10000)
    print(json.dumps({'phase':'seed-screen', 'count':len(seeds), 'negative':sum(F(r['slack'])<0 for r in seeds)}), flush=True)
    observed_rows = observed.build(point)
    direct_rows, theta = direct.build(point)
    extra_rows, extra_origin = boss2_rows(args.point, point)
    vector_path = args.output_dir/f'existing_vectors_{args.label}.jsonl.gz'
    records = []
    seen = {}
    selected = []
    duplicates = []
    with gzip.open(vector_path, 'wt', encoding='utf-8', compresslevel=6) as stream:
        def register(record, coefficients):
            coefficients = sparse(coefficients)
            assert not coefficients or max(i for i, _ in coefficients) < 4849
            exact_value = sum((F(v)*weights[i] for i,v in coefficients if weights[i]), F())
            if 'slack' in record:
                assert exact_value == F(record['slack'])
            encoded = key(coefficients)
            full = dict(record, slack=str(exact_value), slack_float=float(exact_value),
                        vector_sha256=sha(encoded), nonzero_count=len(coefficients),
                        full_column_count=len(columns),
                        baseline_matches=baseline.get(encoded, []),
                        duplicate_of=seen.get(encoded))
            if encoded in seen:
                duplicates.append({'name':full['name'], 'same_as':seen[encoded]})
            else:
                seen[encoded] = full['name']
                if exact_value < 0:
                    assert not full['baseline_matches']
                    selected.append(dict(full, coefficients=coefficients))
            records.append(full)
            stream.write(json.dumps(dict(full, coefficients=coefficients), ensure_ascii=False, separators=(',', ':'))+'\n')
        for index, record in enumerate(seeds):
            register(record, early.row_coefficients(record, columns, hist, family))
            if (index+1) % 300 == 0:
                print(json.dumps({'phase':'full-vectors', 'completed':index+1}), flush=True)
        for record in observed_rows:
            record = dict(record, mechanism='observed-first')
            register({k:v for k,v in record.items() if k != 'coefficients'}, record['coefficients'])
        for record in direct_rows:
            record = dict(record, mechanism='direct-old-R')
            register({k:v for k,v in record.items() if k != 'coefficients'}, record['coefficients'])
        for record in extra_rows:
            register({k:v for k,v in record.items() if k != 'coefficients'}, record['coefficients'])
    assert len(records) == 4752+86+57+11
    out = {
        'scope':'Complete vectors for the specified finite early families at this exact necessary-LP point; not SPE closure',
        'source':str(args.point.resolve()), 'source_sha256':sha(raw),
        'matrix':str(args.matrix.resolve()), 'matrix_sha256':sha(matrix_raw),
        'input_W':point['W'], 'columns':len(columns), 'original_columns':4849,
        'baseline_rows':len(matrix['rows']), 'records':len(records), 'distinct_vectors':len(seen),
        'negative_records':sum(F(r['slack'])<0 for r in records),
        'distinct_negative_vectors':len(selected),
        'per_mechanism':summaries(records),
        'complete_vectors':str(vector_path.resolve()), 'complete_vectors_sha256':sha(vector_path.read_bytes()),
        'dedup_method':'Canonical sorted full sparse Fraction vectors; exact bytes compared, not support-only or point-value equality',
        'auxiliary_coordinates':'All zero outside the original 4849-column prefix',
        'duplicates':duplicates, 'rows':records, 'selected_rows':selected,
        'direct_R_theta':theta, 'boss2_origins':extra_origin,
        'generator_sha256':{str(p):sha(p.read_bytes()) for p in (OLD/'new_theme_early_projections.py',OLD/'observed_first_branch_requery.py',OLD/'direct_old_r_queries.py')},
    }
    target = args.output_dir/f'existing_at_{args.label}.json'
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','selected_rows','duplicates','direct_R_theta','generator_sha256')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
