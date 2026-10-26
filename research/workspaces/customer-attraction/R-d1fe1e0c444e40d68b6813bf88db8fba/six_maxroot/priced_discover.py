#!/usr/bin/env python3
"""One directed cross-branch price separation at the parent exact point.

Discovery only. Restricts base-row supports to the accepted local envelopes.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
from discover import build

HERE=Path(__file__).resolve().parent

def run():
    cert=json.loads((HERE.parent/'parent/joint_system.json').read_text())['certificate']
    us=[F(0)]*6
    for z in cert['support']:
        b=list(map(int,z['actual_bits']));w=F(z['weight']);d=sum(b)
        if d:
            for i in range(6):us[i]+=w*b[i]/d
    r,u,K=map(float,[us[0],us[-1],F(cert['K'])])
    bits,paths,fullnames,fullrows,full_o,vT=build(6,2)
    support={k for c in json.loads((HERE/'exact_cuts.json').read_text()) for k in c['multipliers']}
    take=[i for i,k in enumerate(fullnames) if k in support]
    names=[fullnames[i] for i in take];base=fullrows[:,take];oc=full_o[take]
    states=[(q,y,e) for y in (0,1) for q in range(y,y+5) for e in (0,1)]
    mats=[]
    # Variables: base lambdas, root IC lambda, price lambdas, actual CAPs, B,D,C.
    for q,y,e in states:
        ar=y/(q+e) if y else 0
        al=e/(q+e) if e else 0
        R=np.full(len(bits),ar)-vT
        prices=al-bits/(q+1)
        caps=np.column_stack([bits[:,0]-y,bits[:,0]-e])
        target=np.column_stack([np.full(len(bits),-ar),np.full(len(bits),-al),-bits[:,0]])
        mats.append(np.column_stack([base,R,prices,caps,target]))
    mat=np.concatenate(mats)
    cost=np.r_[np.zeros(mat.shape[1]-3),r,u,K]
    eq=np.zeros(mat.shape[1]);eq[:len(names)]=-oc
    bounds=[(0,None)]*(mat.shape[1]-3)+[(0,500),(0,500),(-100,100)]
    rng=np.random.default_rng(2031)
    chosen=set(rng.choice(len(mat),min(8000,len(mat)),replace=False).tolist())
    for step in range(30):
        ids=np.array(sorted(chosen))
        sol=linprog(cost,A_ub=mat[ids],b_ub=np.zeros(len(ids)),A_eq=[eq],b_eq=[1],bounds=bounds,method='highs')
        if not sol.success:
            print(sol.message,flush=True);return
        violations=mat@sol.x
        worst=np.max(violations)
        print('step',step,'rows',len(ids),'rhs',sol.fun,'worst',worst,'BDC',sol.x[-3:].tolist(),flush=True)
        if worst<1e-8:
            result=dict(scope='floating discovery only',r=str(us[0]),u6=str(us[-1]),K=cert['K'],objective=float(sol.fun),worst_violation=float(worst),B=float(sol.x[-3]),D=float(sol.x[-2]),C=float(sol.x[-1]),names=names,base_multipliers=sol.x[:len(names)].tolist(),root_multiplier=float(sol.x[len(names)]),price_multipliers=sol.x[len(names)+1:len(names)+1+len(bits[0])].tolist(),actual_cap_multipliers=sol.x[-5:-3].tolist())
            (HERE/'priced_discovery.json').write_text(json.dumps(result,indent=2));return
        add=np.flatnonzero(violations>1e-8)
        if len(add)>8000:add=add[np.argsort(violations[add])[-8000:]]
        chosen.update(add.tolist())

if __name__=='__main__':run()
