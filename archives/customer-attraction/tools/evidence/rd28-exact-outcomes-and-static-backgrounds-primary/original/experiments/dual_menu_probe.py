"""Exploratory static minimax caps for real equilibrium deviation menus.
LP output is numerical discovery only. Reads existing immutable certificates.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]

def inspect(name):
    game=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    m,n=len(game['topics']),game['players']
    policy={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
    types=[(set(r['topics']),r['multiplicity']) for r in game['customers']]
    @lru_cache(None)
    def finish(h):
        return h if len(h)==n else finish(h+(policy[h],))
    def query(a,B):
        return sum((F(w,1+sum(b in T for b in B)) for T,w in types if a in T),F(0))
    def payoff(z,i):
        return sum((F(w,sum(b in T for b in z)) for T,w in types if z[i] in T),F(0))
    z=finish(())
    for h in policy:
        assert all(payoff(finish(h),len(h))>=payoff(finish(h+(a,)),len(h)) for a in range(m))
    W=sum(payoff(z,i) for i in range(n))
    menu=set()
    for i in range(n):
        for a in range(m):
            zz=finish(z[:i]+(a,))
            menu.add(tuple(sorted(zz[:i]+zz[i+1:])))
    deletions=set(tuple(sorted(z[:i]+z[i+1:])) for i in range(n))
    caps={}
    for key,Bs in [('onpath_menu',menu),('onpath_deletions',deletions)]:
        Bs=sorted(Bs)
        A=np.array([[float(query(a,B)) for B in Bs] for a in range(m)])
        c=np.r_[np.zeros(len(Bs)),1.0]
        r=linprog(c,A_ub=np.c_[A,-np.ones(m)],b_ub=np.zeros(m),A_eq=[np.r_[np.ones(len(Bs)),0]],b_eq=[1],bounds=[(0,None)]*len(Bs)+[(None,None)],method='highs')
        assert r.success,r.message
        support=[(B,float(q)) for B,q in zip(Bs,r.x[:-1]) if q>1e-8]
        caps[key]={'cap':r.fun,'strong_gap':r.fun-float(W)/n,'half_gap':r.fun-float(W)/(n-.5),'support':support,'backgrounds':len(Bs)}
    return {'name':name,'n':n,'m':m,'z':z,'utilities':[str(payoff(z,i)) for i in range(n)],'W':str(W),'caps':caps}

if __name__=='__main__':
    results=[]
    for f in (ROOT/'evidence/certificates/customer_attraction').glob('*.json'):
        try:
            cert=json.loads(f.read_text())
            if 'strategy' in cert and isinstance(cert['strategy'],dict) and 'actions' in cert['strategy'] and (ROOT/'examples/customer_attraction'/f.name).exists():
                results.append(inspect(f.stem))
        except Exception as e: print('ERROR',f.name,e)
    print(json.dumps(results,indent=2))
