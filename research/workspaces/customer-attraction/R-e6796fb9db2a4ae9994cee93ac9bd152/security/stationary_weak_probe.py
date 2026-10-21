"""Finite LP attack on ONLY the prescribed root stationary kernel."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,math
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]

def main():
    packet=json.loads((ROOT/'evidence/certificates/customer_attraction/root_stationary_kernel.json').read_text())
    sigma={tuple(z['history']):z['action']for z in packet['strategy']['actions']}
    n=3;k=6;masks=range(1,1<<k)
    def terminal(h):
        while len(h)<n:h=h+(sigma[h],)
        return h
    def row(a,z):
        return [F(1,sum((t>>b)&1 for b in z))if(t>>a)&1 else F(0)for t in masks]
    gamma=[]
    for h,a in sigma.items():
        base=row(a,terminal(h))
        for b in range(k):gamma.append([x-y for x,y in zip(base,row(b,terminal(h+(b,))))])
    cover=[int(any((t>>a)&1 for a in terminal(())))for t in masks]
    # Root response K has unique stationary pi=(1,1,0,1,1,0)/4.
    # It induces Q(01)=Q(34)=1/2, held fixed for the entire strategy cone.
    beta=[]
    for a in range(k):
        beta.append([(x+y)/2 for x,y in zip(row(a,(0,1,a)),row(a,(3,4,a)))])
    best=None
    for a in range(k):
        obj=[F(5,2)*x-y for x,y in zip(beta[a],cover)]
        res=linprog(-np.array(obj,float),A_ub=-np.array(gamma,float),b_ub=np.zeros(len(gamma)),
            A_eq=[np.ones(63)],b_eq=[1],bounds=[(0,None)]*63,method='highs')
        assert res.success
        weights=[F(float(x)).limit_denominator(10**6)for x in res.x]
        exact_gap=sum(x*w for x,w in zip(obj,weights))
        assert sum(weights)==1
        assert all(sum(x*w for x,w in zip(r,weights))>=0 for r in gamma)
        if best is None or exact_gap>best['gap']:
            best={'gap':exact_gap,'query':a,'weights':weights}
    den=math.lcm(*(w.denominator for w in best['weights']))
    customers=[{'mask':t,'multiplicity':int(w*den)}for t,w in zip(masks,best['weights'])if w]
    result={'scope':'fixed complete three-player strategy cone; prescribed root stationary Q only',
       'query':best['query'],'normalized_weak_gap':str(best['gap']),
       'customers':customers,'scale':den,
       'W':str(sum(F(z['multiplicity'])*cover[z['mask']-1]for z in customers)),
       'query_values':[str(sum(F(z['multiplicity'])*r[z['mask']-1]for z in customers))for r in beta],
       'actions':packet['strategy']['actions']}
    (HERE/'stationary_weak_probe.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result|{'actions':'saved in output'}))
if __name__=='__main__':main()
