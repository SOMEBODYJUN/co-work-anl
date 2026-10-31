"""Numerical search of all enabling-set values for two nonnegative resource rays."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

rng=np.random.default_rng(20261020)
records=[];n=6
for rep in range(300):
    rays=rng.integers(1,9,size=(2,2))
    if np.linalg.det(rays)==0:continue
    types=rng.integers(0,2,size=n)
    if len(set(types))<2:continue
    scales=rng.integers(1,5,size=n)
    A=np.column_stack([rays[:,types[j]]*scales[j] for j in range(n)])
    cap=rng.integers(3,25,size=2)
    w=rng.integers(1,15,size=n)
    vals=[]
    for mask in range(1<<n):
        r=linprog(-w,A_ub=A,b_ub=cap,bounds=[(0,int(mask>>j&1)) for j in range(n)],method='highs')
        assert r.success
        vals.append(-r.fun)
    bad=None
    for mask in range(1<<n):
        for i in range(n):
            for j in range(i):
                if mask>>i&1 or mask>>j&1:continue
                defect=vals[mask|(1<<i)|(1<<j)]+vals[mask]-vals[mask|(1<<i)]-vals[mask|(1<<j)]
                if defect>1e-7:bad={'mask':mask,'i':i,'j':j,'defect':defect};break
            if bad:break
        if bad:break
    if bad:
        records.append({'rep':rep,'A':A.tolist(),'cap':cap.tolist(),'w':w.tolist(),'types':types.tolist(),'bad':bad,'values':vals});break
out={'seed':20261020,'trials':rep+1,'counterexamples':records,'scope':'Numerical evidence only; all b,w not exhausted.'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
