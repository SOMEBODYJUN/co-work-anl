"""Main checks frozen complete1586 routing before authorizing one new LP."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

P=Path(__file__).resolve().parent
names={'input':'visible_maximum_joint_v4/exact_input.json',
       'manifest':'visible_maximum_joint_v4/freeze_manifest.json',
       'old':'visible_maximum_joint_v3/exact_input.json',
       'old_scale':'visible_maximum_joint_v3/numerical_scaling.json',
       'new':'all_source_joint_reweighted_safe/exact_family.json',
       'main_source_check':'main_all_source_joint_check.json',
       'prepared_check':'visible_maximum_joint_v4/literal_check_result.json',
       'scale':'visible_maximum_joint_v4/numerical_scaling.json'}
data={key:json.loads((P/path).read_text()) for key,path in names.items()}
pins={key:hashlib.sha256((P/path).read_bytes()).hexdigest() for key,path in names.items()}
assert pins['input']=='fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839'
assert pins['manifest']=='21da98ff5b72702363824200e25320fc7d510633be48d91de6e2eea5e708c337'
assert pins['new']=='c8a40df9458e2add557ef14b8282880a1d14b05d55238ecf0715f63968907c18'
x,old,new=data['input'],data['old'],data['new']
assert data['main_source_check']['status']=='PASS'
assert data['prepared_check']['status']=='PREPARED_NO_OPTIMIZER'
assert data['prepared_check']['result'].startswith('PASS')
assert len(x['raw_rows'])==1586 and len(old['raw_rows'])==1050
assert x['raw_rows'][:1050]==old['raw_rows']
assert x['raw_rows'][1050:]==new['rows']
keys=['variables','bit_order','atom_columns','K_column','nonnegative_columns',
      'objective','equalities','equality_count','inequality_convention']
for key in keys:assert x[key]==old[key],key
assert x['variables']==513 and x['K_column']==512 and x['equality_count']==2
assert len(x['atom_columns'])==512
assert len(data['scale']['raw_order'])==1586
assert data['scale']['raw_order']==[r['name'] for r in x['raw_rows']]
assert set(data['scale']['raw_scales'])=={r['name'] for r in x['raw_rows']}
assert {r['name']:data['scale']['raw_scales'][r['name']] for r in x['raw_rows'][:1050]}==data['old_scale']['raw_scales']
for k,r in enumerate(x['raw_rows']):
    divisor=data['scale']['raw_scales'][r['name']]
    assert F(divisor)>0
    if 'numerical_divisor' in r:assert r['numerical_divisor']==divisor
    assert all(0<=int(c)<513 for c in r['a'])
    if k>=1050:
        assert F(r['numerical_divisor'])==25
        assert F(r['a']['512'])==F(7-r['source'],2)
        assert r['uses_C_size_equality'] is False
assert data['manifest']['optimizer_calls']==0
assert pins=={key:hashlib.sha256((P/path).read_bytes()).hexdigest() for key,path in names.items()}
result={'owner':'Boss1/Main','status':'PASS','optimizer_calls':0,'input_sha256':pins['input'],
        'manifest_sha256':pins['manifest'],'source_sha256':pins,
        'literal_old_rows':1050,'literal_added_rows':536,'variables':513,'equalities':2,
        'Main_direct_new_source_check':'67 vertices/8064 states/444 minima/274968 coefficients independently verified',
        'source_review_read':'visible_maximum_joint_v4/source_review.md and final family proof',
        'all_raw_rows_and_coordinates_preserved':True,'fixed_K':False,'support_restriction':False,
        'raw_divisor_strings_preserved':True,'intermediate1050_remains_unsolved':True,
        'preparation_literal_result':data['prepared_check']['result'],
        'scope':'Input is ready for a separate single-call authorization. This precheck itself does not call an optimizer.'}
(P/'main_visible_c_v4_preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
