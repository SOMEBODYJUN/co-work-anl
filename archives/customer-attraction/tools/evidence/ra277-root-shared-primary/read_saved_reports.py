"""Lossless reading/structure helper. No LP, payoff audit, or certificate test.

Only the two frozen JSON reports and two related atom prefixes are parsed.
Output is a new directory; original files are never changed. Per-field runs
contain [dictionary_index, repetition_count], including every zero-mass column.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

FIELDS = ('bits', 'AB_hist', 'AE_hist', 'second_hist', 'menus_lh')


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def key(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def inspect(report):
    assert len(report) == 9
    assert len(report['row_names']) == len(report['K_column'])
    assert len(report['atoms']) == len(report['primal_float'])
    assert len(set(report['row_names'])) == len(report['row_names'])
    assert len({key(a) for a in report['atoms']}) == len(report['atoms'])
    dist, positive_dist = collections.Counter(), collections.Counter()
    for a, weight in zip(report['atoms'], report['primal_float']):
        assert set(a) == set(FIELDS)
        assert len(a['bits']) == 10 and set(a['bits']) <= {'0', '1'}
        d = sum(a['AB_hist'][4:])
        for name, width in [('AB_hist', 8), ('AE_hist', 8), ('second_hist', 16)]:
            h = a[name]
            assert len(h) == width and all(type(v) is int and v >= 0 for v in h)
            assert sum(h) == 5 and sum(h[width // 2:]) == d
        assert len(a['menus_lh']) == 3
        for ell, h in a['menus_lh']:
            assert type(ell) is int and type(h) is int
            assert 0 <= h <= d and 0 <= ell - h <= 5 - d
        dist[d] += 1
        if weight > 0:
            positive_dist[d] += 1
    return {
        'top_level_fields': list(report),
        'rows': len(report['row_names']), 'atoms': len(report['atoms']),
        'primal_positive': sum(v > 0 for v in report['primal_float']),
        'primal_zero': sum(v == 0 for v in report['primal_float']),
        'primal_negative': sum(v < 0 for v in report['primal_float']),
        'zero_hex_counts': dict(collections.Counter(v.hex() for v in report['primal_float'] if not v)),
        'd_counts': dict(sorted(dist.items())),
        'positive_d_counts': dict(sorted(positive_dist.items())),
        'saved_positive_multipliers': len(report['dual_multipliers_float']),
        'history_length': len(report['history']),
        'initial_columns_in_history': report['history'][0]['columns'] - report['history'][0]['new_columns'],
        'all_new_columns_in_history': sum(v['new_columns'] for v in report['history']),
        'last_new_columns': report['history'][-1]['new_columns'],
        'all_atom_domain_and_alignment_checks_pass': True,
        'float_weight_sum_readout': sum(report['primal_float']),
        'float_W_readout': sum(w for a, w in zip(report['atoms'], report['primal_float']) if '1' in a['bits'][:5]),
        'float_O_readout': sum(w for a, w in zip(report['atoms'], report['primal_float']) if sum(a['AB_hist'][4:]) > 0),
        'note': 'Readout of frozen floats and discrete domain checks only; no primal feasibility, optimality, IC, or exact certificate acceptance.'
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--evidence-dir', required=True, type=Path)
    p.add_argument('--repo-root', required=True, type=Path)
    p.add_argument('--output-dir', required=True, type=Path)
    args = p.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    original = args.evidence_dir / 'original'
    old = load(original / '5b7c5fd5d7726ecc1c54/root_shared_max_cg.json')
    copy = load(original / '88ae1829da05e1bd6eb6/root_shared_max_copy_cg.json')
    dictionary, vectors, runs = {}, {}, {}
    for field in FIELDS:
        values, lookup, ids = [], {}, []
        for a in copy['atoms']:
            v = a[field]
            if key(v) not in lookup:
                lookup[key(v)] = len(values)
                values.append(v)
            ids.append(lookup[key(v)])
        dictionary[field], vectors[field] = values, ids
        runs[field] = [[i, len(list(g))] for i, g in itertools.groupby(ids)]
    rebuilt = [{f: dictionary[f][vectors[f][i]] for f in FIELDS}
               for i in range(len(copy['atoms']))]
    assert rebuilt == copy['atoms']
    assert rebuilt[:len(old['atoms'])] == old['atoms']
    for field in FIELDS:
        assert [i for i, count in runs[field] for _ in range(count)] == vectors[field]
    projection = {
        'codec': 'Each field dictionary uses first-occurrence indexing. Per-field runs [value_id,count] concatenate to the complete2753-entry vector; zip fields to recover atoms. Old report is exactly first2725 atoms. Literal arrays and strings, not digest substitutes.',
        'dictionaries': dictionary, 'field_runs': runs,
        'length': len(copy['atoms']), 'old_prefix_length': len(old['atoms'])
    }
    dump(args.output_dir / 'whole-2753-atom-reading-projection.json', projection)
    metadata = {}
    for name, data in [('old', old), ('copy', copy)]:
        meta = {k: v for k, v in data.items() if k not in ('atoms', 'primal_float')}
        # Hex-run representation preserves even negative-zero signs exactly.
        meta['primal_float_hex_runs'] = [[v, len(list(g))] for v, g in itertools.groupby(x.hex() for x in data['primal_float'])]
        meta['primal_float_nonzero_by_index'] = [[i, v] for i, v in enumerate(data['primal_float']) if v]
        restored = [float.fromhex(v) for v, count in meta['primal_float_hex_runs'] for _ in range(count)]
        assert [v.hex() for v in restored] == [v.hex() for v in data['primal_float']]
        metadata[name] = meta
    dump(args.output_dir / 'complete-report-reading.json', metadata)
    pkg = args.repo_root / 'archives/customer-attraction/tools/evidence/ra277-root-saturation-primary'
    parent_path = pkg / 'original/research/workspaces/customer-attraction/R-a27734a8bba345cbb5fad186c120d0bf/root_saturation_cg.json'
    warm_path = pkg / 'related-original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/cg_overlap1_final.json'
    related = {}
    for name, path in [('parent_root_690', parent_path), ('fallback_old557', warm_path)]:
        d = load(path)
        assert old['atoms'][:len(d['atoms'])] == d['atoms']
        related[name] = {
            'path': str(path.relative_to(args.repo_root)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'atoms': len(d['atoms']), 'whole_atom_array_is_exact_primary_prefix': True,
            'first557_row_names_match': old['row_names'][:557] == d['row_names'][:557],
            'actual_read_scope': 'All atom records through exact equality with fully read primary prefix; row-name prefix. Other old history/primal/dual fields not semantically audited.'
        }
    assert set(copy['row_names']) - set(old['row_names']) == {'KRS:maxsource-opt'}
    assert not (set(old['row_names']) - set(copy['row_names']))
    summary = {
        'scope': 'lossless reading and structural identity; not a mathematical certificate execution',
        'old': inspect(old), 'copy': inspect(copy),
        'old_atoms_exact_prefix_of_copy': True,
        'field_dictionary_sizes': {f: len(dictionary[f]) for f in FIELDS},
        'field_run_counts': {f: len(runs[f]) for f in FIELDS},
        'row_name_set_addition': ['KRS:maxsource-opt'],
        'base557_names_equal': old['row_names'][:557] == copy['row_names'][:557],
        'base557_K_columns_zero': set(old['K_column'][:557]) == set(copy['K_column'][:557]) == {0.0},
        'related_prefix_checks': related,
        'original_program_executions': 0, 'LP_or_price_executions': 0,
        'full_SPE_certifications': 0, 'new_exact_primal_or_dual_certifications': 0
    }
    dump(args.output_dir / 'reading-structure-report.json', summary)
    print(json.dumps({'old_rows': summary['old']['rows'], 'copy_rows': summary['copy']['rows'],
                      'old_atoms': len(old['atoms']), 'copy_atoms': len(copy['atoms']),
                      'lossless_and_prefix_checks': 'PASS', 'LP_or_certificate_run': False}))


if __name__ == '__main__':
    main()
