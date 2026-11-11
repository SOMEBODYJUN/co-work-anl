#!/usr/bin/env python3
"""One129-column root72 LP with recorded positive row scaling."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import numpy as np
from scipy.optimize import linprog
H=Path(__file__).resolve().parent
def main():
    marker=H/'DISCOVERY_CALL_CONSUMED.json'
    if marker.exists():raise SystemExit('One-call budget consumed.')
    inp=json.loads((H/'exact_input.json').read_text());digest=hashlib.sha256((H/'exact_input.json').read_bytes()).hexdigest()
    audit=json.loads((H/'literal_input_check.json').read_text());assert audit['status']=='PASS' and audit['input_sha256']==digest
    A=[];b=[]
    for row in inp['raw_rows']:
        scale=F(row['numerical_divisor']);assert scale>0
        A.append([-float(F(row['a'].get(str(j),'0'))/scale) for j in range(129)]);b.append(-float(F(row['rhs'])/scale))
    E=[[float(F(row['a'].get(str(j),'0'))) for j in range(129)] for row in inp['equalities']]
    f=[float(F(row['rhs'])) for row in inp['equalities']];c=np.zeros(129);c[-1]=1
    marker.write_text(json.dumps({'input_sha256':digest,'calls_reserved':1,'fixed_K':inp['fixed_K'],'rows':72,'columns':129,'epoch':time.time()},indent=2)+'\n')
    t=time.monotonic()
    r=linprog(c,A_ub=np.array(A),b_ub=np.array(b),A_eq=np.array(E),b_eq=np.array(f),bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    def native(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,(np.integer,np.floating)):return x.item()
        if isinstance(x,dict):return {k:native(v) for k,v in x.items()}
        return x
    out=native(dict(r));out.update(input_sha256=digest,optimizer_calls=1,elapsed_seconds=time.monotonic()-t,
                                 row_numerical_divisors=[row['numerical_divisor'] for row in inp['raw_rows']],
                                 dual_unscaling_rule='Original GE weight = -solver_inequality_marginal / row_numerical_divisor')
    (H/'discovery_output.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','success','message','fun','nit','elapsed_seconds','optimizer_calls']},indent=2))
if __name__=='__main__':main()
