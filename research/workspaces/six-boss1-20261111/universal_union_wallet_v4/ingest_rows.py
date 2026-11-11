"""Exact v4 row intake. No optimizer import/call; Main release is mandatory."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from copy import deepcopy
import argparse
import json
import re

HERE = Path(__file__).resolve().parent
WS = HERE.parent
BASE_SHA = 'd5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55'
BASE_CERT_SHA = '1d9a898e3ca429b6af3611f01ada831ad50cf7f0708f14d7c518478573f0a9e3'
SLOTS = ['ACTUAL_OPT_REQUERY_30', 'ACTUAL_RC_30', 'SOURCE2_MAX_SIZE_31', 'ROOT72_FIXED_DUAL_30']


def read(p):
    return json.loads(p.read_text())


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def exact(value):
    if type(value) not in (str, int):
        raise ValueError('Exact coefficients must be rational strings or integers, never floats/bools.')
    return F(value)


def source_path(name):
    if not isinstance(name, str) or Path(name).is_absolute():
        raise ValueError('Source paths must be relative to the RUN workspace.')
    p = (WS/name).resolve()
    p.relative_to(WS.resolve())
    if not p.is_file():
        raise ValueError('Missing released source: '+name)
    return p


def source_artifact(spec):
    if not re.fullmatch('[0-9a-f]{64}', spec.get('sha256', '')):
        raise ValueError('A released source requires an exact SHA256.')
    p = source_path(spec['path'])
    if digest(p) != spec['sha256']:
        raise ValueError('Released source SHA mismatch: '+spec['path'])
    return p


def pointer(obj, ptr):
    if ptr == '':
        return obj
    if not isinstance(ptr, str) or not ptr.startswith('/'):
        raise ValueError('Use an explicit JSON pointer.')
    for token in ptr[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    return obj


def dense_coefficients(entry):
    spec = entry['coefficient_source']
    obj = read(source_artifact(spec))
    if 'all257_pointer' in spec:
        values = pointer(obj, spec['all257_pointer'])
        if set(values) != {str(j) for j in range(257)}:
            raise ValueError('all257_pointer must expose all257 named columns, including zeros.')
        return [exact(values[str(j)]) for j in range(257)]
    values = pointer(obj, spec['atoms256_pointer'])
    if set(values) != {str(j) for j in range(256)}:
        raise ValueError('atoms256_pointer must expose every original Boolean type, including o=0.')
    if ('K_pointer' in spec) == ('K_literal' in spec):
        raise ValueError('Specify exactly one explicit signed K coefficient source.')
    kval = pointer(obj, spec['K_pointer']) if 'K_pointer' in spec else spec['K_literal']
    return [exact(values[str(j)]) for j in range(256)] + [exact(kval)]


def baseline():
    p = WS/'universal_union_wallet_v3/exact_input.json'
    cp = WS/'universal_union_wallet_v3/exact_certificate.json'
    assert digest(p) == BASE_SHA and digest(cp) == BASE_CERT_SHA
    data = read(p)
    assert data['variables'] == 257 and data['K_column'] == 256
    assert data['nonnegative_columns'] == list(range(257))
    assert len(data['raw_rows']) == data['raw_inequality_count'] == 221
    assert len(data['atom_columns']) == 256
    for j, a in enumerate(data['atom_columns']):
        bits = [int(x) for x in format(j, '08b')]
        assert a == {'index':j, 'a':bits[:6], 'x':bits[6], 'o':bits[7]}
    for pinfile in ['prior_83_frozen_hashes.json', 'v3_face_frozen_hashes.json']:
        for name, h in read(HERE/pinfile).items():
            assert digest(WS/name) == h, name
    return data


def ingest(release_file, release_sha):
    data = baseline()
    if not re.fullmatch('[0-9a-f]{64}', release_sha):
        raise ValueError('An explicitly supplied Main release SHA256 is required.')
    release_file = release_file.resolve()
    release_file.relative_to(WS.resolve())
    if digest(release_file) != release_sha:
        raise ValueError('Main release SHA mismatch.')
    release = read(release_file)
    assert release['schema'] == 'boss1-universal-wallet-v4-release-v1'
    assert release['status'] == 'MAIN_EXPLICIT_FOUR_ROW_RELEASE'
    assert release['run'] == 'six-boss1-20261111'
    assert release['base_input_sha256'] == BASE_SHA
    assert release['base_certificate_sha256'] == BASE_CERT_SHA
    assert release['expected_raw_rows'] == 225 and release['expected_columns'] == 257
    entries = release['rows']
    assert len(entries) == 4 and {e['slot'] for e in entries} == set(SLOTS)
    entries = {e['slot']:e for e in entries}
    weak = read(source_artifact(read(HERE/'preparation_config.json')['forbidden_C36_coefficient_artifact']))
    weak_C36 = [exact(weak['actual_all256_coefficients'][str(j)]) for j in range(256)] + [F(0)]
    byold = {r['name']:r for r in data['raw_rows']}
    old_RC36 = [exact(byold['RC_8_8']['a'].get(str(j),'0')) for j in range(257)]
    old_root = [exact(byold['ROOT_TRUE_TAIL']['a'].get(str(j),'0')) for j in range(257)]
    newrows = []
    provenance = []
    used_names = set(byold)
    for slot in SLOTS:
        e = entries[slot]
        assert e['orientation'] == 'ge' and exact(e['rhs']) == 0
        assert isinstance(e['name'], str) and e['name'] not in used_names
        used_names.add(e['name'])
        assert e['all256_types'] is True and e['same_genuine_ordered_history'] is True
        if slot in ['ACTUAL_OPT_REQUERY_30','ACTUAL_RC_30','ROOT72_FIXED_DUAL_30']:
            assert e['ordered_query_index_pairs'] == 30
            assert e['repeated_query_labels_allowed'] is True
        proofs = e['proof_sources']
        assert {'proof','exact_certificate','independent_check'} <= {q['role'] for q in proofs}
        for q in proofs:
            source_artifact(q)
        v = dense_coefficients(e)
        if slot == 'ACTUAL_OPT_REQUERY_30':
            assert v[256] == 0 and v != weak_C36, 'C36 substitution is forbidden.'
        elif slot == 'ACTUAL_RC_30':
            assert v[256] == 0 and v != old_RC36, 'RC36 substitution is forbidden.'
        elif slot == 'SOURCE2_MAX_SIZE_31':
            assert v[256] == 4
            for j in range(256):
                a = list(map(int,format(j,'08b'))); c = sum(a[:6])
                u2 = F(a[1],c) if c else F(0)
                assert v[j] == 31*u2-4*a[5]-F(30*a[5],a[0]+5)-F(a[6],a[0]+1+4*a[5])
        else:
            assert v != old_root, 'The old root line is not the released root72/30 strengthening.'
        if e.get('preserve_source_row') is True:
            released_row = read(source_artifact(e['coefficient_source']))
            assert released_row['name'] == e['name'] and exact(released_row['rhs']) == 0
            assert [exact(released_row['a'][str(j)]) for j in range(257)] == v
            assert exact(released_row['numerical_divisor']) > 0
            newrows.append(deepcopy(released_row))
        else:
            newrows.append({'name':e['name'],'family':slot,'a':{str(j):str(q) for j,q in enumerate(v) if q},'rhs':'0'})
        provenance.append(deepcopy(e))
    result = deepcopy(data)
    result['scope'] = 'v4: all221 frozen v3 raw inequalities plus exactly four Main-released cuts; full256 types+K. Intake is not an optimization or a source-proof certificate.'
    result['raw_rows'] = deepcopy(data['raw_rows'])+newrows
    assert result['raw_rows'][:221] == data['raw_rows']
    assert len(result['raw_rows']) == 225
    unique, zero, seen, duplicates = [], [], {}, []
    for row in result['raw_rows']:
        a = tuple(exact(row['a'].get(str(j),'0')) for j in range(257))
        rhs = exact(row['rhs'])
        if not any(a) and rhs == 0:
            zero.append(row['name']); continue
        key = (a,rhs)
        if key in seen:
            duplicates.append({'name':row['name'],'identical_to':seen[key]}); continue
        seen[key] = row['name']; unique.append(deepcopy(row))
    result['unique_rows'] = unique
    result['raw_inequality_count'] = 225
    result['unique_inequality_count'] = len(unique)
    result['removed_zero_rows'] = zero
    result['removed_exact_duplicate_rows'] = duplicates
    result['v4_main_release_sha256'] = release_sha
    result['v4_row_provenance'] = provenance
    result['inherited_source_review_note'] = 'source_review_sha256 is the unchanged v3 baseline review; v4 rows are bound by v4_row_provenance and require separate literal source review before any authorized LP.'
    scales = {}
    for row in unique:
        scale = exact(row['numerical_divisor']) if 'numerical_divisor' in row else max([F(1),abs(exact(row['rhs']))]+[abs(exact(q)) for q in row['a'].values()])
        assert scale > 0
        scales[row['name']] = str(scale)
    for name in ['exact_input.json','main_release.json','numerical_scaling.json','row_ingest_check.json']:
        if (HERE/name).exists():
            raise ValueError('Refusing to overwrite an already ingested v4 artifact: '+name)
    baseline()  # Verify old pins again immediately before writes.
    (HERE/'main_release.json').write_bytes(release_file.read_bytes())
    (HERE/'exact_input.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (HERE/'numerical_scaling.json').write_text(json.dumps({'scope':'Positive exact row scaling only; no LP called.','rule':'Released new rows use their explicit numerical_divisor; inherited rows use max(1,abs(rhs),max(abs(coeff))). Original rows stay unscaled in exact input.','scales':scales},indent=2)+'\n')
    report = {'status':'PASS_STRUCTURAL_ROW_INGEST_ONLY','optimizer_calls':0,'raw_rows':225,'columns':257,
        'original221_rows_exactly_preserved':True,'original221x257_coefficients_unchanged':56797,
        'all256_types_preserved':True,'positive_scaling':True,'unique_rows':len(unique),
        'main_release_sha256':release_sha,'input_sha256':digest(HERE/'exact_input.json'),
        'source_mathematical_rederivation_complete':False,'lp_authorized_by_this_script':False}
    (HERE/'row_ingest_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release',type=Path,required=True)
    parser.add_argument('--release-sha256',required=True)
    args = parser.parse_args()
    ingest(args.release,args.release_sha256)
