"""Main reviews the newly frozen 181-row face diagnostics, without optimization."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

W=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def h(p):return sha256(p.read_bytes()).hexdigest()
out=W/'main_ordered181_face_review.json';assert not out.exists()
base=read(W/'visible_maximum_joint_v4/exact_input.json')
face=read(W/'visible_maximum_joint_v4_solve/optimal_face.json')
coords={x['column']:[F(x['constant'])]+list(map(F,x['parameter_coefficients'])) for x in face['coordinates']}
fam=read(W/'all_source_ordered_menu_cells/exact_family.json')['rows']
reported=read(W/'ordered181_on_1586_diagnostic/all181_point_and_face_rows.json')['rows']
root=read(W/'ordered181_on_1586_diagnostic/root119_positive_payments.json')
b=F(1767904008200582,16877573861922720);c=F(337340181272013,16877573861922720)
r270=base['raw_rows'][868];menub=base['raw_rows'][1001]
negative=[];weights=[];column_checks=0
for j,(r,rep) in enumerate(zip(fam,reported)):
    vals=[sum((F(r['a'].get(str(k),'0'))*v[t] for k,v in coords.items()),F(0)) for t in range(8)]
    assert rep['name']==r['name'] and vals==[F(rep['face_constant'])]+list(map(F,rep['face_parameter_coefficients']))
    assert not any(vals[1:])
    if vals[0]<0:negative.append(j)
    if r['source']==1:
        a=F(r['source_IC_weight']);G=F(r['G_by_prefix_load']['0'])
        m=3+a*b;v=a*c+m/6-G
        assert min(a,m,v)>0
        for k in range(513):
            o=((k>>1)&1) if k<512 else 0
            want=a*F(r270['a'].get(str(k),'0'))+m*F(menub['a'].get(str(k),'0'))+v*o
            assert want==F(r['a'].get(str(k),'0')),(r['name'],k)
            column_checks+=1
        weights.append((v,r['name']))
assert len(fam)==len(reported)==181
assert negative==[122,126,130,132,136,138,140,142,144,146]
assert len(weights)==119 and column_checks==61047
minimum=min(weights)[0]
assert minimum==F(1418409404670832709,178005661824966187500)==F(root['minimum_O_weight'])
result={'status':'PASS_MAIN_ALL181_WHOLE_FACE_AND119_ROOT_POSITIVE_PAYMENTS',
        'optimizer_calls':0,'full_face_prior_Main_review':'main_visible_c_v4_certificate_check.json',
        'all181_affine_expressions':181,'seven_parameter_coefficients_all_zero':True,
        'strict_negative_whole_face_rows':negative,'root_vertices':119,'root_full_column_identities':column_checks,
        'root_minimum_O_weight':str(minimum),'root_minimum_attainers':[n for v,n in weights if v==minimum],
        'proof_personally_read_complete':True,'proof_sha256':h(W/'ordered181_on_1586_diagnostic/proof.md'),
        'scope':'Complete fixed-CAP root continuous family is redundant by independently checked full cell affinity. No pruning and no new LP value.'}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
