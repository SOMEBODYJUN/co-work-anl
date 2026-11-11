#!/usr/bin/env python3
"""Same exact fixed weights: one-step, finite geometric, and infinite orbit."""
from fractions import Fraction as F
from itertools import product
import hashlib,json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
from prepare_discounted_cuts import Audit,canonical,read_member,ratio

HERE=Path(__file__).resolve().parent
pack_path=HERE/'priority_named_discounted_M1_19556.json'
pack_raw=pack_path.read_bytes()
assert hashlib.sha256(pack_raw).hexdigest()=='7aefad539b2e01a1894cbbf744470624e1312dca39f41a041a5299064a8cca4b'
pack=json.loads(pack_raw)
record=next(r for r in pack['selected_rows'] if r['actual_source_zero_based']==2 and r['forced']=='H3')
point_path=Path(pack['source']);raw=point_path.read_bytes()
assert hashlib.sha256(raw).hexdigest()==pack['source_sha256']
point=json.loads(raw);columns=point['columns'];weights=[F(c['weight']) for c in columns]
original=Audit(record)
zero_record=dict(record,theta='0')
one=Audit(zero_record)
zero_row,ncols,nzero=one.row(columns)
zero_slack=sum((v*weights[i] for i,v in zero_row.items()),F())
assert zero_slack>0
infinite_row,_,_=original.row(columns)
infinite_slack=sum((v*weights[i] for i,v in infinite_row.items()),F())
assert infinite_slack==F(record['slack'])<0

hist={i:c for i,c in enumerate(columns) if c['kind']=='hist'}
family_indices=[i for i,c in enumerate(columns[:4849]) if c['kind']=='maximum-root-family-state']
P=original.par;k=original.k;theta=original.theta;source=original.source
cap=(k-2)*P.get('beta_middle',F())+P.get('beta_last',F())
types={};state_keys={}
for i in family_indices:
    c=columns[i];a=tuple(map(int,hist[c['hist_column']]['actual_bits']))
    qs=tuple(read_member(c,a,q) for q in original.fixed)
    key=(sum(a[:source]),sum(a[:5]),qs)
    state_keys[i]=(key,int(read_member(c,a,record['forced'])),a)
    if key in types:continue
    p,ell,qs=key
    edges={(t,g):min(original.cost(p,ell,t,g,middle,qs)
                     for middle in product((0,1),repeat=k-2)) for t,g in product((0,1),repeat=2)}
    types[key]={'edges':edges,'value':(F(),F())}

results=[];first_negative=None
for depth in range(1,25):
    for item in types.values():
        old=item['value'];e=item['edges']
        item['value']=tuple(min(e[t,g]+theta*old[g] for g in (0,1)) for t in (0,1))
    normalization=(1-theta)/(1-theta**depth)
    row={0:cap} if cap else {}
    for i,(key,t0,a) in state_keys.items():
        wallet=P.get('source',F())*ratio(a[source],sum(a))
        wallet+=((k-2)*P.get('alpha_middle',F())+P.get('alpha_last',F()))*ratio(a[5],sum(a))
        coef=wallet-normalization*types[key]['value'][t0]
        if coef:row[i]=coef
    slack=sum((v*weights[i] for i,v in row.items()),F())
    if depth==1:assert row==zero_row and slack==zero_slack
    r={'depth':depth,'slack':str(slack),'slack_float':float(slack),'normalized_geometric_weight_sum':'1'}
    if slack<0 and first_negative is None:
        first_negative=depth
        encoded=canonical(row.items())
        r.update(coefficients=json.loads(encoded),vector_sha256=hashlib.sha256(encoded).hexdigest())
    results.append(r)

out={'scope':'Same fixed rational parameters on SHA-bound point; finite/infinite requery comparison, not closure of any optimized parameter cone',
     'source':str(point_path),'source_sha256':pack['source_sha256'],'input_W':point['W'],
     'frozen_pack_sha256':hashlib.sha256(pack_raw).hexdigest(),'selected_name':record['name'],
     'parameters':record['parameters'],'theta':record['theta'],
     'one_step_exact_slack':str(zero_slack),'one_step_slack_float':float(zero_slack),
     'one_step_coefficients':json.loads(canonical(zero_row.items())),
     'infinite_exact_slack':str(infinite_slack),'infinite_slack_float':float(infinite_slack),
     'fixed_parameter_sign_reversal':True,'columns':len(columns),'original_columns':4849,
     'constructed_family_columns':ncols,'constructed_zero_mass_columns':nzero,
     'first_negative_depth_within_1_to_24':first_negative,'finite_depths':results,
     'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
target=HERE/'same_parameters_discount_comparison_19556.json'
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('one_step_coefficients','finite_depths')},ensure_ascii=False))
print(json.dumps({'output':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))
