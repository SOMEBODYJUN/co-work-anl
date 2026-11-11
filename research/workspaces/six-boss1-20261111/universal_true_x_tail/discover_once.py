#!/usr/bin/env python3
"""Exactly one authorized phase-I LP; a marker prevents repeated discovery."""
from pathlib import Path
import json,gzip,hashlib,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from fractions import Fraction

H=Path(__file__).resolve().parent
def main():
    marker=H/'DISCOVERY_CALL_CONSUMED.json'
    if marker.exists():raise SystemExit('One discovery call already consumed; do not rerun.')
    checks=json.loads((H/'literal_input_check.json').read_text())
    inp=H/'exact_input.json.gz'; sha=hashlib.sha256(inp.read_bytes()).hexdigest()
    assert checks['status']=='PASS' and checks['input_sha256']==sha
    j=json.loads(gzip.decompress(inp.read_bytes())); n=len(j['columns']); m=len(j['inequalities'])
    rr=[];cc=[];vv=[]
    for r,row in enumerate(j['inequalities']):
        for c,v in row['a'].items():rr.append(r);cc.append(int(c));vv.append(float(Fraction(v)))
        rr.append(r);cc.append(n);vv.append(-1.)
    A=coo_matrix((vv,(rr,cc)),shape=(m,n+1)).tocsr(); b=np.array([float(Fraction(r['rhs'])) for r in j['inequalities']])
    er=[];ec=[];ev=[]
    for r,row in enumerate(j['equalities']):
        for c,v in row['a'].items():er.append(r);ec.append(int(c));ev.append(float(Fraction(v)))
    E=coo_matrix((ev,(er,ec)),shape=(len(j['equalities']),n+1)).tocsr(); f=np.array([float(Fraction(r['rhs'])) for r in j['equalities']])
    c=np.zeros(n+1);c[-1]=1.
    marker.write_text(json.dumps({'input_sha256':sha,'calls_reserved':1,'formulation':'min epsilon, A mu-epsilon<=b, E mu=z, all variables>=0','time_utc_epoch':time.time()},indent=2)+'\n')
    start=time.monotonic()
    result=linprog(c,A_ub=A,b_ub=b,A_eq=E,b_eq=f,bounds=(0,None),method='highs',options={'presolve':True,'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    def plain(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,(np.integer,np.floating)):return x.item()
        if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
        return x
    out=plain(dict(result));out['input_sha256']=sha;out['elapsed_seconds']=time.monotonic()-start;out['optimizer_calls']=1
    (H/'discovery_output.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['success','status','message','fun','nit','elapsed_seconds','optimizer_calls']},indent=2))
if __name__=='__main__':main()
