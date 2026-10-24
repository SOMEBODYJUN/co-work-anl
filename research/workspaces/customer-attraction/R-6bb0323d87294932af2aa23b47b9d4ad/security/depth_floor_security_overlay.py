"""Overlay genuine static-security LPs on direct agent's exact depth floors.

The floors come from all histories and all SPE continuations, not one sigma.
Security values here are floating discovery numbers only, never certificates.
"""
import json
from fractions import Fraction as F
from itertools import combinations_with_replacement as C
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
data=json.loads((HERE.parent/'direct/depth_floor_checks.json').read_text())
out=[]
for r in data['records']:
    g=json.loads((ROOT/r['input']).read_text())
    n,k=g['players'],len(g['topics'])
    types=[(set(x['topics']),x['multiplicity']) for x in g['customers']]
    M=np.array([[sum(float(F(w,1+sum(b in s for b in B))) for s,w in types if a in s)
                 for a in range(k)] for B in C(range(k),n-1)])
    lp=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-M,np.ones(len(M))],
               b_ub=np.zeros(len(M)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],
               bounds=[(0,None)]*k+[(None,None)],method='highs')
    assert lp.success,lp.message
    v=float(lp.x[-1])
    record={'input':r['input'],'floor_sum':r['floor_sum'],
            'security_discovery':v,
            'floor_security_gap_discovery':float(F(r['floor_sum']))-n*v,
            'query_candidate':[str(F(float(q)).limit_denominator(1000000)) for q in lp.x[:-1]]}
    out.append(record)
    print(json.dumps(record),flush=True)
(HERE/'depth_floor_security_discovery.json').write_text(json.dumps(out,indent=2)+'\n')
