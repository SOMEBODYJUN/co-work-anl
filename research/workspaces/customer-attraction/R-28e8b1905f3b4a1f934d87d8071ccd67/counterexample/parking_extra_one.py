"""Directed independent-parking attack on the weak extra-one individual bridge.

Discovery computes all SPE outcome sets numerically; only an exact successful
reconstruction could certify a bridge counterexample. Negative output is not a
universal conclusion. The one parameter H is the private parking block size.
"""
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog
from utp_attack import compositions

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver


def diagnostic(base,k,H):
    p=len(base['topics'])+1; m=base['players']+k
    support=[tuple(t['topics']) for t in base['customers']]+[(p-1,)]
    weight=np.array([t['multiplicity'] for t in base['customers']]+[H],dtype=float)
    member=np.zeros((len(support),p),int)
    for i,s in enumerate(support): member[i,list(s)]=1
    terms=list(compositions(m,p)); arr=np.array(terms,int)
    idx={c:i for i,c in enumerate(terms)}
    den=arr@member.T
    u=np.array([member.T/np.maximum(d,1)@weight for d in den])
    add=np.array([member.T/(d+1)@weight for d in den])
    @lru_cache(None)
    def solve(b):
        if sum(b)==m: return {idx[b]}
        kids=[]
        for a in range(p):
            c=list(b); c[a]+=1
            kids.append(solve(tuple(c)))
        floor=max(min(u[i,a] for i in kid) for a,kid in enumerate(kids))
        return {i for a,kid in enumerate(kids) for i in kid if u[i,a]>=floor-1e-9}
    outs=solve((0,)*p)
    mins=[min(u[i,a] for a in range(p) if arr[i,a]) for i in outs]
    oi=min(outs,key=lambda i:min(u[i,a] for a in range(p) if arr[i,a]))
    lp=linprog(np.r_[np.zeros(p),-1.],A_ub=np.c_[-add,np.ones(len(terms))],b_ub=np.zeros(len(terms)),A_eq=[np.r_[np.ones(p),0]],b_eq=[1],bounds=[(0,None)]*p+[(None,None)],method='highs')
    assert lp.success
    return {'parking':k,'H':H,'min_spe_player':min(mins),'extra_one_value':-lp.fun,'gap':-lp.fun-min(mins),'target':terms[oi],'query':lp.x[:-1].tolist(),'outcomes':len(outs)}


def main():
    base=json.loads((ROOT/'examples/customer_attraction/individual_security_failure.json').read_text())
    out=[]
    for k in (1,2,3):
        # Intervals around H=(k+1)*10, the low original player payoff scale.
        for H in range(8*(k+1),13*(k+1)+1):
            r=diagnostic(base,k,H); out.append(r)
            if r['gap']>1e-7:
                obj=dict(base);obj['players']+=k;obj['topics']=obj['topics']+['Parking'];obj['customers']=obj['customers']+[{'topics':[len(obj['topics'])-1],'multiplicity':H}]
                inst=Instance.from_dict(obj);sol=ExactSPESolver(inst)
                target=tuple(r['target'])
                assert target in sol.outcomes()
                r['exact_payoffs']=list(map(str,inst.topic_payoffs(target)))
                r['instance']=obj
                print(json.dumps(r));break
        print(json.dumps({'k':k,'best_gap':max(r['gap'] for r in out if r['parking']==k)}),flush=True)
    Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'directed private-parking parameter diagnostic; no universal claim','results':out},indent=2)+'\n')

if __name__=='__main__':main()
