"""Find shared weights for true single-prefix five-tail comparisons."""
import json
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'research/workspaces/six-boss1-20261111/background_five_bridge'
def ratio(n,d):
    return F(n,d) if n else F()
def minima(mode,b):
    filename=SOURCE/f'fixed53_b{b}_{mode}.json' if b else SOURCE/'fixed53_b0_profit.json'
    return {(q['actual'],q['d']):F(q['min_rho']) for q in json.loads(filename.read_text())['min_by_actual_and_d']}
def data():
    ms={(mode,b):minima(mode,b) for mode in ('profit','coverage') for b in (0,1)}
    for b,*e in product(range(2),repeat=6):
        e=tuple(e);c=sum(e);w=int(b+c>0);u=[ratio(x,b+c) for x in e];ru=ratio(b,b+c);v=sum(u)
        s=''.join(map(str,e)); f=(b,)+e
        for d in range(6 if len(sys.argv)<2 or sys.argv[1]=='bg' else 7):
            m=5 if len(sys.argv)<2 or sys.argv[1]=='bg' else 6
            o=int(d>0);t=ratio(d,b+d)
            rows={}
            for mode in ('profit','coverage'):
                def var(k):
                    tgt=ratio(k,b+k) if mode=='profit' else int(k>0)
                    left=2*v if mode=='profit' else 2*w
                    return left - tgt - ms[mode,b][s,k]
                if m==5:
                    rows[mode]=var(d)
                else:
                    rows[mode]=(ratio(m-d,m)*var(d) if d<m else 0)+(ratio(d,m)*var(d-1) if d else 0)
            for i in range(5):
                p=b+sum(e[:i]);h=5-i
                qs={'z':b,'target':F(d,m)}
                qs.update({f'e{j}':e0 for j,e0 in enumerate(e)})
                for n,weight in qs.items():
                    rows[f'floor{i}_{n}']=u[i]-ratio(weight,p+h)
            p=b+sum(e[:3]);g=lambda t:ratio(t,(p+1)*(p+2));ff=lambda t:ratio(t,p+1)
            acttax=g(e[3]);pair=u[3]+u[4]+acttax
            opt=F(d,m);queries={'z':b,'target':opt};queries.update({f'e{j}':vv for j,vv in enumerate(e)})
            for j,(a,x) in enumerate(queries.items()):
                for l,(h,y) in enumerate(queries.items()):
                    if l<j:continue
                    dxy=(ratio(d*(d-1),m*(m-1)) if a==h=='target' else x*y)
                    rows[f'pair_{a}_{h}']=pair-ff(x+y)+g(dxy)
            rows['R']=m*u[3]+F(1,2)*u[4]-ratio(d,p+1)+max(F(),ratio(d,(p+1)*(p+2))-ratio(1,2*(p+e[3]+1)))
            if m==6:
                for j,x in enumerate(f):rows[f'root_{j}']=ru-ratio(x,6)
                rows['root_target']=ru-ratio(d,36)
            yield (b,s,d),rows,(t if m==5 else o),(v if m==5 else w)
def run():
    points=list(data())
    keys=tuple(points[0][1]);print('points,rows',len(points),len(keys))
    A=np.array([[float(r[k]) for k in keys]+[-float(w)] for _,r,_,w in points]);bb=np.array([-float(t) for _,_,t,_ in points])
    res=linprog([0.]*len(keys)+[1.],A_ub=A,b_ub=bb,bounds=(0,None),method='highs')
    print(res.message)
    if res.success:
        print('factor',res.fun)
        for k,u in zip(keys,res.x):
            if u>1e-9:print(k,round(u,12))
        print('primal',[(s,round(-p,6)) for (s,*_),p in zip(points,res.ineqlin.marginals) if p < -1.e-8])
if __name__=='__main__':run()
