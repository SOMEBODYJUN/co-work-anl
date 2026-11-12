"""Main's full literal4177 audit; no optimization and no release creation.

Source domain/true-budget proofs were personally reviewed and independently
checked first.  This separate program audits the final lossless assembly.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from collections import Counter
import json

W = Path(__file__).resolve().parent
R = W.parents[2]
P = W/'visible_maximum_joint_v6'
B = W/'visible_maximum_joint_v5'


def read(p):
    return json.loads(p.read_text())


def h(p):
    return sha256(p.read_bytes()).hexdigest()


def objhash(obj):
    return sha256((json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def main():
    assert h(P/'exact_input.json') == '8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769'
    assert h(P/'freeze_manifest.json') == '0aa45d8f1517b6958ae6187b5ebbf89a3ea31926347d997a696fe20fd4b35da2'
    man = read(P/'freeze_manifest.json')
    for name,digest in man['artifacts'].items():
        assert Path(name).name == name and h(P/name) == digest, name
    pins = read(P/'source_pins.json')['files']
    for pin in pins:
        assert h(R/pin['path']) == pin['sha256'], pin['path']
    data,base = read(P/'exact_input.json'),read(B/'exact_input.json')
    scale,oldscale = read(P/'numerical_scaling.json'),read(B/'numerical_scaling.json')
    catalog,oldcatalog = read(P/'row_catalog.json'),read(B/'row_catalog.json')
    rows = data['raw_rows']
    assert len(rows) == data['raw_inequality_count'] == 4177
    assert data['variables'] == 513 and data['K_column'] == 512
    assert data['equality_count'] == 2 and data['nonnegative_columns'] == list(range(513))
    assert rows[:3056] == base['raw_rows']
    assert catalog[:3056] == oldcatalog
    for key in ['variables','bit_order','atom_columns','K_column','nonnegative_columns','objective',
                'equalities','equality_count','inequality_convention']:
        assert data[key] == base[key], key
    expected = [('source2_lambda_strip',230,'raw_coefficients'),
                ('source2_lambda_anchor_complete',160,'raw_coefficients'),
                ('later_sources_lambda_cells',550,'a'),
                ('source2_conditional_redistribution',180,'a')]
    k = 3056
    blocks = []
    for package,count,field in expected:
        originals = read(W/package/'exact_family.json')['rows']
        assert len(originals) == count
        source_catalog = read(W/package/'row_catalog.json') if (W/package/'row_catalog.json').exists() else None
        begin = k
        for local,source in enumerate(originals):
            assembled = rows[k]
            coefs = source[field]
            expected_coefs = {str(j):v for j,v in enumerate(coefs)} if isinstance(coefs,list) else coefs
            assert assembled['a'] == expected_coefs
            assert assembled['rhs'] == source.get('rhs','0')
            assert assembled['name'] == package+'::'+source['id']
            assert assembled['source_package'] == package
            assert assembled['source_file'] == 'exact_family.json'
            assert assembled['source_row_index'] == local
            assert assembled['id'] == assembled['source_row_id'] == source['id']
            assert assembled['source_row_object_sha256'] == objhash(source)
            metadata = {key:value for key,value in source.items() if key not in {'a','raw_coefficients','coefficients_divided_by_25'}}
            assert assembled['source_row_metadata'] == metadata
            assert catalog[k]['source_row_metadata'] == metadata
            if source_catalog is not None:
                assert catalog[k]['original_source_catalog_entry'] == source_catalog[local]
            if field == 'raw_coefficients':
                assert all(F(a)/25 == F(b) for a,b in zip(source[field],source['coefficients_divided_by_25']))
            k += 1
        blocks.append({'package':package,'start':begin,'stop':k,'raw_count':count,
                       'source_family_sha256':h(W/package/'exact_family.json')})
    root = read(W/'main_root270_strict_outside/ROOT270_STRICT_C_OUTSIDE.json')
    assert k == 4176 and rows[k] == root
    assert scale['raw_order'] == [r['name'] for r in rows]
    assert len(scale['raw_scales']) == len(set(scale['raw_order'])) == 4177
    assert scale['raw_order'][:3056] == oldscale['raw_order']
    for k,row in enumerate(rows):
        divisor = scale['raw_scales'][row['name']]
        assert F(divisor) > 0
        assert divisor == (oldscale['raw_scales'][row['name']] if k<3056 else '25' if k<4176 else '1')
        assert all(isinstance(j,str) and j == str(int(j)) and 0<=int(j)<513 for j in row['a'])
        for j in range(513):
            F(row['a'].get(str(j),'0'))
        F(row['rhs'])
    assert Counter(r['rhs'] for r in rows) == {'0':4147,'-1':30}
    assert rows[45]['a'] == {} and rows[45]['rhs'] == '0'
    eta = F(1087978231314917,84387869309613600)
    for j,bits in enumerate(product((0,1),repeat=9)):
        assert data['atom_columns'][j] == {'index':j,'old_index':j//2,'a':list(bits[:6]),'x':bits[6],'o':bits[7],'c':bits[8]}
        assert F(data['objective'].get(str(j),'0')) == int(any(bits[:6]))
        assert F(data['equalities'][0]['a'].get(str(j),'0')) == bits[7]
        assert F(data['equalities'][1]['a'].get(str(j),'0')) == bits[8]
        assert F(rows[4176]['a'].get(str(j),'0'))-F(rows[868]['a'].get(str(j),'0')) == -eta*bits[8]*(1-bits[7])
    assert rows[4176]['a']['512'] == rows[868]['a']['512']
    assert F(data['objective'].get('512','0')) == F(data['equalities'][0]['a'].get('512','0')) == 0
    assert F(data['equalities'][1]['a']['512']) == -1
    assert [F(e['rhs']) for e in data['equalities']] == [F(1),F(0)]
    checks = ['main_source2_lambda_strip_check.json','main_source2_lambda_anchor_complete_check.json',
              'main_later_lambda_check.json','main_source2_delta_check.json','main_root270_strict_outside/check_result.json']
    for name in checks:
        assert read(W/name)['status'].startswith('PASS'), name
    model = read(P/'model_contract.json')
    assert model['global_O_role'] == 'chosen_OPT6_union' and model['normalization_requires_positive_OPT6']
    correction = W/'visible_maximum_joint_v6_model_erratum.md'
    assert correction.exists(), 'The inherited maximal-potential X scope must be corrected before release.'
    result = {'status':'PASS_MAIN_FULL4177_LITERAL_SOURCE_CONCATENATION_AND_CORRECT_MODEL',
              'input_sha256':h(P/'exact_input.json'),'preparation_manifest_sha256':h(P/'freeze_manifest.json'),
              'raw_rows':4177,'variables':513,'equalities':2,'all_rational_column_positions_checked':4177*513,
              'literal_old_rows':3056,'appended_rows':1121,'rhs_minus_one_rows':30,'source_blocks':blocks,
              'original_ids_all_metadata_and_catalogs_preserved':True,
              'zero_duplicate_window_and_all_customer_types_preserved':True,
              'independent_source_true_cost_and_domain_checks':{name:h(W/name) for name in checks},
              'artifact_checks':len(man['artifacts']),'source_sha_checks':len(pins),
              'model_scope':{'O':'a six-label optimum union attaining OPT6; normalize only when OPT6>0',
                             'C':'a genuine maximum bare-size legal label',
                             'X':'a full-catalog maximum of the inherited actual-prefix-four potential; arbitrary legal X is NOT enough for all inherited rows',
                             'new_local_sources':'any legal pure target and any six-query union, specialized to these global labels',
                             'frozen_X_wording_erratum':{'path':str(correction.relative_to(R)),'sha256':h(correction)}},
              'optimizer_calls':0,'optimization_release_created':False,'half_status':'OPEN'}
    with (W/'main_visible_c_v6_preflight.json').open('x') as stream:
        stream.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','input_sha256','raw_rows','variables','all_rational_column_positions_checked','optimizer_calls']},ensure_ascii=False))


if __name__ == '__main__':
    main()
