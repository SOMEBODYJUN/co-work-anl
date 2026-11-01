"""Floating fixed-point test of a general promoted-last-reply fork.

No welfare LP is reoptimized. Positive separation requires exact recovery.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

ROOT = Path(__file__).resolve().parents[5]
POINT = ROOT / 'research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/combined_702.json'

def part(a, n):
    return F(a, n) if a else F(0)

def local_coeff(p, t, q, s, b, c, v):
    """True source/interior/terminal inequalities, written cost <= cap."""
    z1, z2 = p+t+s+b+c, p+t+s+c+v
    return [part(t,z1), part(c,z2)-part(b,z1),
            F(q,p+t+s+b+1)-part(c,z1),
            F(q,p+t+s+c+1)-part(v,z2),
            F(v,p+t+s+b+1)-part(c,z1),
            F(b,p+t+s+c+1)-part(v,z2)]

def main():
    data=json.loads(POINT.read_text())
    m=data['m']; K=F(data['K'])
    support=[(tuple(map(int,x['actual_bits'])),x['d'],F(x['weight'])) for x in data['support']]
    us=[sum((w*part(a[i],sum(a)) for a,d,w in support),F(0)) for i in range(m)]
    results=[]
    for i in range(m-2):
      k=m-i
      for target in ['optimal']+list(range(m)):
       for query in ['same']+list(range(m)):
        groups=[]
        for a,d,w in support:
          for t,prob in ([(0,1-F(d,m)),(1,F(d,m))] if target=='optimal' else [(a[target],F(1))]):
            if prob: groups.append((a,t,t if query=='same' else a[query],w*prob))
        configs=list(product(range(k-2),range(2),range(2),range(2)))
        rows=6+4*(m+1);cols=len(groups)*len(configs)
        A=lil_matrix((rows,cols+1),dtype=float)
        E=lil_matrix((len(groups),cols+1),dtype=float)
        bounds=[us[i],F(0),F(0),F(0),F(0),F(0)]
        for tag in range(4):
          mult=k-3 if tag==3 else 1
          bounds.extend([mult*u for u in us]+[mult*K])
        for gi,(a,t,q,w) in enumerate(groups):
          p=sum(a[:i]);prices=[F(1,sum(a[:j])+m-j) for j in range(m)]
          for ci,(s,b,c,v) in enumerate(configs):
            j=gi*len(configs)+ci
            coeff=local_coeff(p,t,q,s,b,c,v)
            for bit in (b,c,v,s):coeff.extend([bit*z for z in prices]+[F(bit)])
            A[:,j]=np.array(list(map(float,coeff)))[:,None];E[gi,j]=1
        A[:,-1]=-1
        objective=np.zeros(cols+1);objective[-1]=1
        r=linprog(objective,A_ub=A.tocsr(),b_ub=list(map(float,bounds)),
                  A_eq=E.tocsr(),b_eq=[float(g[3]) for g in groups],bounds=(0,None),method='highs')
        assert r.success,r.message
        results.append({'source':i+1,'remaining':k,'target':target,'query':query,'phase_one_slack':float(r.fun)})
    print(json.dumps({'point':str(POINT.relative_to(ROOT)),
      'scope':'floating fixed-point completion diagnostic, not SPE or a welfare LP',
      'cases':len(results),'max_phase_one_slack':max(x['phase_one_slack'] for x in results),
      'separated':[x for x in results if x['phase_one_slack']>1e-8]},indent=2))

if __name__=='__main__':main()
