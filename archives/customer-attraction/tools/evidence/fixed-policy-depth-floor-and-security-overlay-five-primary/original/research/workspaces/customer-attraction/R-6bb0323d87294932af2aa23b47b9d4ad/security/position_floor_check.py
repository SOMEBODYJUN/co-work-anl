"""Exact diagnosis of the candidate sum of all-history position floors >= m v_m.

No equilibrium solver is imported. Full saved policies are verified at every
ordered history; supplied matching static primal/dual certificates are checked
where present. Numerical LP values are clearly marked discovery only.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement as cwr, product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).with_suffix('.json')

def check(name):
    game = json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert = json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    n,k = game['players'],len(game['topics'])
    types=[(frozenset(x['topics']),x['multiplicity']) for x in game['customers']]
    policy={tuple(x['history']):x['action'] for x in cert['strategy']['actions']}
    histories=tuple(h for d in range(n) for h in product(range(k),repeat=d))
    assert set(policy)==set(histories)
    @lru_cache(None)
    def leaf(h):return h if len(h)==n else leaf(h+(policy[h],))
    def counts(h):return tuple(h.count(a) for a in range(k))
    @lru_cache(None)
    def query(a,q):return sum((F(w,1+sum(q[b] for b in s)) for s,w in types if a in s),F())
    def utility(i,z):return query(z[i],counts(z[:i]+z[i+1:]))
    floors=[None]*n
    witness=[None]*n
    comparisons=0
    for h in histories:
        i=len(h); z=leaf(h);u=utility(i,z)
        if floors[i] is None or u<floors[i]:floors[i]=u;witness[i]=h
        for a in range(k):
            assert u>=utility(i,leaf(h+(a,))), (name,h,a)
            comparisons+=1
    static=tuple(cwr(range(k),n-1))
    matrix=tuple(tuple(query(a,counts(B)) for a in range(k)) for B in static)
    sc=cert.get('security',{})
    p=sc.get('primary',sc.get('p'))
    Q=sc.get('dual',sc.get('Q'))
    result={'instance':name,'positions':n,'catalog':k,'histories':len(histories),
            'comparisons':comparisons,'position_floors':list(map(str,floors)),
            'floor_witness_histories':witness,'floor_sum':str(sum(floors)),
            'root':leaf(()),'root_utilities':[str(utility(i,leaf(()))) for i in range(n)]}
    if p is not None and Q is not None and isinstance(Q,list) and Q and isinstance(Q[0],dict):
        p=list(map(F,p));assert len(p)==k and sum(p)==1 and min(p)>=0
        lower=min(sum((pa*x for pa,x in zip(p,row)),F()) for row in matrix)
        opponents=[]
        for row in Q:
            B=row.get('rivals',row.get('competitors',row.get('background')))
            q=row.get('probability',row.get('weight'))
            if B is None or q is None:break
            opponents.append((counts(B),F(q)))
        else:
            assert sum(q for B,q in opponents)==1
            upper=max(sum((q*query(a,B) for B,q in opponents),F()) for a in range(k))
            assert lower==upper
            result.update(security_value=str(lower),security_status='exact matched saved primal/dual',
                          floor_security_gap=str(sum(floors)-n*lower))
            return result
    mat=np.asarray(matrix,dtype=float)
    lp=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(k),0.]],b_eq=[1.],bounds=[(0,None)]*k+[(None,None)],method='highs')
    assert lp.success,lp.message
    value=float(lp.x[-1])
    result.update(security_value_discovery=value,security_status='floating LP discovery only',floor_security_gap_discovery=float(sum(floors))-n*value)
    return result

if __name__=='__main__':
    names=['individual_security_failure','aggregate_theta_failure','root_tax_failure','global_decorrelation_failure','local_security_increment','five_individual_security']
    results=[]
    for name in names:
        try:r=check(name)
        except (KeyError,TypeError) as exc:r={'instance':name,'unsupported_saved_schema':str(exc)}
        results.append(r);print(json.dumps(r))
    OUT.write_text(json.dumps(results,indent=2)+'\n')
