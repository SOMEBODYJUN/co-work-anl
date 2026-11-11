#!/usr/bin/env python3
"""Bind an explicitly released NEXT 23676 point; never solve or seek a point.

This program reads only the packaged weight-free template and one explicit
release JSON supplied on the command line.  It has no default gamepoint path,
no numerical libraries, and no optimizer.  A missing/null release fails before
any output is written.  The release must contain all 21021 rational strings.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json
import re

HERE = Path(__file__).resolve().parent


def bind(template, release):
    assert template['schema'] == 'early-shared-X-fixed-point-template/v1'
    assert template['status'] == 'UNFILLED_AWAIT_MAIN_NEXT_23676_EXACT_POINT'
    assert release['schema'] == 'main-next-23676-point-release/v1'
    assert isinstance(release.get('main_release_reference'), str) and release['main_release_reference'].strip(), 'Main release reference is required'
    point_sha = release.get('exact_point_sha256')
    assert isinstance(point_sha, str) and re.fullmatch(r'[0-9a-f]{64}', point_sha), 'Exact next-point SHA256 is required'
    base = template['base_contract']
    assert release['base_matrix_sha256'] == base['base_matrix_sha256']
    assert release['base_descriptors_sha256'] == base['base_descriptors_sha256']
    raw = release.get('old_vector')
    assert isinstance(raw, list) and len(raw) == 21021, 'All 21021 old coordinates are required'
    assert all(isinstance(a, str) and re.fullmatch(r'\d+(?:/[1-9]\d*)?', a) for a in raw), 'Use nonnegative exact rational strings; floating inputs are rejected'
    old = [F(a) for a in raw]
    norm = sum((F(a) * old[j] for j, a in base['existing_normalization']['row']), F())
    assert norm == F(base['existing_normalization']['rhs']), 'The fixed old point must preserve old normalization'
    for h in base['histograms']:
        assert 0 <= old[h['X_column']] <= old[h['hist_column']], 'Common X must be a genuine submass'
    rows = []
    for record in template['rows']:
        rhs = F(record['rhs_constant']) + sum((F(a) * old[j] for j, a in record['rhs_old_linear_form']), F())
        rows.append({'id': record['id'], 'sense': record['sense'],
                     'row': record['hidden_coefficients'], 'rhs': str(rhs)})
    return {'schema': 'early-shared-X-fixed-point-feasibility-input/v1',
            'status': 'PREPARED_EXACT_FIXED_POINT_INPUT_NOT_SOLVED',
            'point_binding': {k: release[k] for k in ('main_release_reference', 'exact_point_sha256',
                                                   'base_matrix_sha256', 'base_descriptors_sha256')},
            'fixed_old_vector': raw, 'hidden_columns': template['hidden_columns'],
            'hidden_column_count': 1920, 'hidden_lower_bounds': ['0'] * 1920,
            'rows': rows, 'objective': None, 'optimizer_calls': 0,
            'optimizer_authorization': False,
            'scope': template['interpretation'],
            'baseline_feasibility_note': 'Main is responsible for certifying the supplied old vector against all 23676 old rows. This binder checks dimensions, exact format, normalization and H/X bounds only; it does not reclassify a supplied vector as an SPE.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-json', type=Path, required=True,
                        help='Explicit Main release JSON for the NEXT exact 23676x21021 point; no automatic point discovery.')
    parser.add_argument('--output-name', required=True,
                        help='New filename inside this directory, ending in .json.gz; no overwrite.')
    args = parser.parse_args()
    assert Path(args.output_name).name == args.output_name and args.output_name.endswith('.json.gz')
    out = HERE / args.output_name
    assert not out.exists(), ('refuse_overwrite', str(out))
    release_bytes = args.release_json.read_bytes()
    template_path = HERE / 'fixed_point_feasibility_template.json.gz'
    with gzip.open(template_path, 'rt', encoding='utf-8') as stream:
        template = json.load(stream)
    prepared = bind(template, json.loads(release_bytes))
    prepared['input_template_sha256'] = sha256(template_path.read_bytes()).hexdigest()
    prepared['main_release_json_sha256'] = sha256(release_bytes).hexdigest()
    with out.open('xb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as packed:
            packed.write((json.dumps(prepared, indent=2, ensure_ascii=False) + '\n').encode())
    print(json.dumps({'status': prepared['status'], 'output': str(out),
                      'sha256': sha256(out.read_bytes()).hexdigest(), 'rows': len(prepared['rows']),
                      'columns': 1920, 'optimizer_calls': 0}, indent=2))


if __name__ == '__main__':
    main()
