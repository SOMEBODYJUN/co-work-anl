#!/usr/bin/env python3
"""One local phase-I call; all 141 inequalities relaxed, masses exact."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import numpy as np
from scipy.optimize import linprog
H=Path(__file__).resolve().parent
def main():
    marker=H/'DISCOVERY_CALL_CONSUMED.json'
    if marker.exists():raise SystemExit('One authorized discovery call already consumed.')
    inp=json.loads((H/'exact_input.json').read_text());sha=hashlib.sha256((H/'exact_input.json').read_bytes()).hexdigest()
    chk=json.loads((H/'literal_input_check.json').read_text());assert chk['status']=='PASS' and chk['input_sha256']==sha
    A=[[float(F(r['a'].get(str(j),'0'))) for j in range(160)]+[-1.] for r in inp['raw_rows']]
    b=[float(F(r['rhs'])) for r in inp['raw_rows']]
    E=[[float(F(r['a'].get(str(j),'0'))) for j in range(160)]+[0.] for r in inp['equalities']]
    f=[float(F(r['rhs'])) for r in inp['equalities']]
    c=np.zeros(161);c[-1]=1
    marker.write_text(json.dumps({'input_sha256':sha,'calls_reserved':1,'formulation':'min epsilon, A nu-epsilon<=b, E nu=w, nu/epsilon>=0','epoch':time.time()},indent=2)+'\n')
    t=time.monotonic()
    r=linprog(c,A_ub=np.array(A),b_ub=np.array(b),A_eq=np.array(E),b_eq=np.array(f),bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    def plain(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,(np.integer,np.floating)):return x.item()
        if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
        return x
    out=plain(dict(r));out.update(input_sha256=sha,optimizer_calls=1,elapsed_seconds=time.monotonic()-t)
    (H/'discovery_output.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['success','status','message','fun','nit','elapsed_seconds','optimizer_calls']},indent=2))
if __name__=='__main__':main()
