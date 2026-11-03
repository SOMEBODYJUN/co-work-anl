"""LP attack of strong uniform true-deviation smoothness, for fixed full SPE trees."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver
from customer_attraction.certificate import StrategyCertificate, verify_certificate
from fractions import Fraction
from itertools import combinations
from functools import lru_cache
import json, random
import numpy as np
from scipy.optimize import linprog


def cone_data(inst,cert):
    k,m=inst.topic_count,inst.players
    masks=list(range(1,1<<k))
    membership=np.array([[(b>>j)&1 for j in range(k)] for b in masks])
    @lru_cache(None)
    def util(counts,a):
        hits=membership@np.array(counts)
        return membership[:,a]/np.maximum(hits,1)
    outcomes={}
    rows=[]
    def walk(h):
        if len(h)==m:
            return inst.counts(h)
        kids=[walk(h+(a,)) for a in range(k)]
        chosen=cert.actions[h]
        actual=kids[chosen]
        actualu=util(actual,chosen)
        for a in range(k):
            if a!=chosen:
                rows.append(actualu-util(kids[a],a))
        outcomes[h]=kids
        return actual
    target=walk(())
    actual=[]
    while len(actual)<m:
        actual.append(cert.actions[tuple(actual)])
    wc=(membership@np.array(target)>0).astype(float)
    v=[]
    for t in range(k):
        v.append(sum((util(outcomes[tuple(actual[:i])][t],t) for i in range(m)),np.zeros(len(masks))))
    return masks,membership,np.array(rows),wc,np.array(v),tuple(actual)


def run(trials=100):
    rng=random.Random(374957)
    best=-1e10
    for trial in range(trials):
        k,m=rng.choice([(4,3),(4,4),(5,3),(5,4),(5,5)])
        cs=[]
        for b in range(1,1<<k):
            n=rng.choice([0,0,0,0,1,2,3])
            if n:
                cs.append(CustomerType(frozenset(t for t in range(k) if b>>t&1),n))
        inst=Instance(tuple(map(str,range(k))),tuple(cs),m)
        solver=ExactSPESolver(inst)
        if solver.minimum_welfare()==0:
            continue
        target=min(solver.worst_outcomes())
        cert=solver.certificate(target_counts=target)
        masks,mem,rows,wc,v,actual=cone_data(inst,cert)
        for query in combinations(range(k), min(k,m)):
            if len(query)<m:
                query=query+(query[0],)*(m-len(query))
            oc=(np.sum(mem[:,list(query)],axis=1)>0).astype(float)
            gap=m*oc-(m-1)*wc-sum((v[t] for t in query),np.zeros(len(masks)))
            lp=linprog(-gap,A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=wc.reshape(1,-1),b_eq=[1],bounds=(0,None),method='highs')
            if not lp.success:
                raise RuntimeError(lp.message)
            val=-lp.fun
            best=max(best,val)
            if val>1e-7:
                result=dict(trial=trial,k=k,m=m,query=query,actual=actual,gap=val,
                            weights={str(b):float(x) for b,x in zip(masks,lp.x) if x>1e-10},
                            certificate=cert.to_dict())
                out=Path(__file__).with_name('uniform_portfolio_cone_candidate.json')
                out.write_text(json.dumps(result,indent=2))
                print('FOUND',dict((key,value) for key,value in result.items() if key!='certificate'),flush=True)
                return
        if trial%10==0:
            print('trial',trial,'best',best,flush=True)
    print('finished',trials,'best',best)

if __name__=='__main__':
    run(int(sys.argv[1]) if len(sys.argv)>1 else 100)
