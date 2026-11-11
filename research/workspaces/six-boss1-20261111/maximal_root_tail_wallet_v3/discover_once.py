#!/usr/bin/env python3
"""Exactly one LP call after exact input, source review and independent precheck lock."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,time
import numpy as np
from scipy.optimize import linprog
H=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    inp=json.loads((H/'exact_input.json').read_text());audit=json.loads((H/'literal_input_check.json').read_text());d=digest(H/'exact_input.json')
    assert audit['status']=='PASS' and audit['input_sha256']==d and audit['positive_scaling_verified']
    assert audit['source_review_sha256']==inp['source_review_sha256']==digest(H/'source_review.md')
    assert len(inp['raw_rows'])==270 and len(inp['nonnegative_columns'])==129
    A=[];b=[]
    for row in inp['raw_rows']:
        div=F(row['numerical_divisor']);assert div>0
        A.append([-float(F(row['a'].get(str(j),'0'))/div) for j in range(129)])
        b.append(-float(F(row['rhs'])/div))
    E=[[float(F(e['a'].get(str(j),'0'))) for j in range(129)] for e in inp['equalities']]
    rhs=[float(F(e['rhs'])) for e in inp['equalities']];objective=np.zeros(129);objective[-1]=1
    marker={'input_sha256':d,'source_review_sha256':digest(H/'source_review.md'),
            'preflight_sha256':digest(H/'literal_input_check.json'),'calls_reserved':1,'rows':270,'columns':129,
            'fixed_K':inp['fixed_K'],'fixed_O':inp['fixed_O'],'epoch':time.time()}
    with (H/'DISCOVERY_CALL_CONSUMED.json').open('x') as out:json.dump(marker,out,indent=2);out.write('\n')
    start=time.monotonic()
    result=linprog(objective,A_ub=np.array(A),b_ub=np.array(b),A_eq=np.array(E),b_eq=np.array(rhs),
                   bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    def native(o):
        if isinstance(o,np.ndarray):return o.tolist()
        if isinstance(o,(np.integer,np.floating)):return o.item()
        if isinstance(o,dict):return {k:native(v) for k,v in o.items()}
        return o
    out=native(dict(result));out.update(input_sha256=d,optimizer_calls=1,elapsed_seconds=time.monotonic()-start,
       raw_rows_submitted=270,nonnegative_columns=129,row_numerical_divisors=[r['numerical_divisor'] for r in inp['raw_rows']],
       zero_and_duplicate_rows_removed=0,dual_unscaling_rule='Original GE row weight = -solver inequality marginal / recorded positive divisor')
    (H/'discovery_output.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out.get(k) for k in ['status','success','message','fun','nit','elapsed_seconds','optimizer_calls']},indent=2))
    if not result.success:raise SystemExit('The sole authorized solve failed; no retry authorized.')
if __name__=='__main__':main()
