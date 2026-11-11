#!/usr/bin/env python3
"""One authorized 129-column optimization; permanent guard before call."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import numpy as np
from scipy.optimize import linprog

H=Path(__file__).resolve().parent
def main():
    guard=H/'DISCOVERY_CALL_CONSUMED.json'
    if guard.exists():raise SystemExit('The only discovery call is already consumed.')
    path=H/'exact_input.json';sha=hashlib.sha256(path.read_bytes()).hexdigest()
    checked=json.loads((H/'literal_input_check.json').read_text());assert checked['status']=='PASS' and checked['input_sha256']==sha
    inp=json.loads(path.read_text());A=[];b=[];E=[];f=[]
    for row in inp['raw_rows']:
        A.append([-float(F(row['a'].get(str(j),'0'))) for j in range(129)]);b.append(-float(F(row['rhs'])))
    for row in inp['equalities']:
        E.append([float(F(row['a'].get(str(j),'0'))) for j in range(129)]);f.append(float(F(row['rhs'])))
    c=np.zeros(129);c[-1]=1
    guard.write_text(json.dumps({'input_sha256':sha,'calls_reserved':1,'task':'minimize actual root u at fixed K0,O1 in the 128-type root-C branch cone','epoch':time.time()},indent=2)+'\n')
    start=time.monotonic()
    res=linprog(c,A_ub=np.array(A),b_ub=np.array(b),A_eq=np.array(E),b_eq=np.array(f),bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    def native(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,(np.integer,np.floating)):return x.item()
        if isinstance(x,dict):return {k:native(v) for k,v in x.items()}
        return x
    out=native(dict(res));out['input_sha256']=sha;out['optimizer_calls']=1;out['elapsed_seconds']=time.monotonic()-start
    (H/'discovery_output.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','success','message','fun','nit','elapsed_seconds','optimizer_calls']},indent=2))
if __name__=='__main__':main()
