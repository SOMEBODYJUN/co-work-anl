"""Main's exact original-coordinate interface and complete ZZ-min audit."""
from pathlib import Path
from fractions import Fraction as F
import gzip
import hashlib
import json
B=Path(__file__).resolve().parent
D=B/'master_cuts'
stem='complete624_actual4_R00_opt_v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fp,pp=D/(stem+'_exact.json'),D/(stem+'_original4849_exact.json')
full,projection=json.loads(fp.read_text()),json.loads(pp.read_text())
audit=json.loads((B/'main_verify_complete624_opt_v2.json').read_text())
assert audit['status']=='PASS' and audit['point_sha256']==sha(fp)
assert len(full['columns'])==12631 and len(projection['columns'])==4849
assert projection['columns']==full['columns'][:4849]
assert projection['parent_full_point_sha256']==sha(fp)
assert projection['parent_full_matrix_sha256']==audit['matrix_sha256']
assert F(projection['O'])==F(full['O'])==1
assert F(projection['W'])==F(full['W'])==F(audit['W'])
assert F(projection['K'])==F(full['columns'][0]['weight'])
assert sum(F(c['weight'])>0 for c in projection['columns'])==projection['positive_columns']==319
base=json.loads(gzip.decompress((D/'complete_zz_5799_v1_matrix.json.gz').read_bytes()))
mapping=json.loads((D/'complete_zz_5799_v1_mapping.json').read_text())
x=[F(c['weight']) for c in full['columns']]
for rec in mapping['auxiliaries']:
    q=sum((x[j] for j in rec['source_R_columns']),F(0))
    v=sum((x[j] for j in rec['query_Z_columns']),F(0))
    assert 0<=x[rec['column_index']]<=min(q,v)
    x[rec['column_index']]=min(q,v)
values=[]
for rec in mapping['classes']:
    row=base['rows'][rec['row_index']]
    value=sum((F(v)*x[j] for j,v in row['nonzero']),F(0))
    assert value>0
    values.append({'class':rec['class'],'slack':str(value)})
assert len(values)==39
out={'status':'PASS','scope':'The certified full624 point has exactly this original4849 projection; all39 canonical ZZ-min budgets strictly positive. Auxiliary values are not real cross intersections.',
     'full_point_sha256':sha(fp),'projection_sha256':sha(pp),
     'parent_matrix_sha256':audit['matrix_sha256'],'prefix_weights_and_descriptors_identical':True,
     'positive_original_columns':319,'ZZ_min_values':values,
     'minimum_ZZ_min_value':str(min(F(v['slack']) for v in values)),
     'verifier_sha256':sha(Path(__file__))}
op=Path(__file__).with_suffix('.json')
assert not op.exists()
op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='ZZ_min_values'},ensure_ascii=False,indent=2))
