"""Exploratory variable-cardinality oblivious blocking LP; not a proof oracle.

For a positive threshold t, minimize E|B| subject to E f_B(a)<=t for
all legal a. Unlike v_n, B is allowed variable nonnegative cardinality.
All equilibrium menus use the repository's complete-history set-valued BI.
"""
from pathlib import Path
import sys,json,itertools,random,time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def counts(p,k):
    if p==1:
        yield(k,);return
    for j in range(k+1):
        for tail in counts(p-1,k-j):yield(j,)+tail

def blocker(inst,t,K):
    p=inst.topic_count
    C=np.array([c for j in range(K+1)for c in counts(p,j)],dtype=int)
    masks=np.array([[int(a in x.topics)for a in range(p)]for x in inst.customers],dtype=int)
    w=np.array([x.multiplicity for x in inst.customers])
    A=(w[None,:]/(1+C@masks.T))@masks
    r=linprog(C.sum(axis=1),A_ub=A.T,b_ub=np.full(p,float(t)),A_eq=np.ones((1,len(C))),b_eq=[1.],bounds=(0,None),method='highs')
    assert r.success,r.message
    nu=float(r.eqlin.marginals[0]);lam=-r.ineqlin.marginals
    return {'d':float(r.fun),'td':float(t)*r.fun,'nu':nu,'certified_cutoff':nu<=K+1+1e-8,'support':[(C[i].tolist(),float(q))for i,q in enumerate(r.x)if q>1e-8],'dual_lambda':lam.tolist()}

def analyze(inst,K):
    sol=ExactSPESolver(inst);rows=[]
    for c in sol.outcomes():
        W=inst.welfare(c)
        eligible=[]
        for a in range(inst.topic_count):
            prefix=tuple(int(b==a)for b in range(inst.topic_count))
            if c in sol.outcomes(prefix)and inst.topic_payoff(a,c)>=sol.threshold((0,)*inst.topic_count):eligible.append(a)
        if not eligible:continue
        a=min(eligible,key=lambda b:inst.topic_payoff(b,c));t=inst.topic_payoff(a,c)
        if not t:continue
        b=blocker(inst,t,K);rows.append(dict(counts=c,W=W,first=a,t=str(t),gap=W-b['td'],**b))
    return sorted(rows,key=lambda x:x['gap'])

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--random',type=int,default=0);ap.add_argument('--players',type=int,default=3);ap.add_argument('--topics',type=int,default=5);ap.add_argument('--cutoff',type=int,default=6);ap.add_argument('--seed',type=int,default=71);a=ap.parse_args()
    rng=random.Random(a.seed);best=None;start=time.time()
    paths=['coverage_opportunity_failure','individual_security_failure','worst_pne_welfare_failure','local_security_increment']
    if a.random:
        games=[]
        for j in range(a.random):
            cs=[CustomerType(frozenset(i for i in range(a.topics)if B>>i&1),rng.randrange(1,5))for B in range(1,1<<a.topics)if rng.random()<.3]
            games.append((str(j),Instance(tuple(map(str,range(a.topics))),tuple(cs),a.players)))
    else:games=[(name,Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())))for name in paths]
    for name,inst in games:
        rows=analyze(inst,a.cutoff)
        if not rows:continue
        row=rows[0]
        if best is None or row['gap']<best['row']['gap']:
            best={'instance':inst.to_dict(),'name':name,'row':row};print(json.dumps(best),flush=True)
        if row['gap']<-1e-7:print('NEGATIVE CANDIDATE',name,flush=True);break
    print(json.dumps({'elapsed':time.time()-start,'best':best}),flush=True)

if __name__=='__main__':main()
