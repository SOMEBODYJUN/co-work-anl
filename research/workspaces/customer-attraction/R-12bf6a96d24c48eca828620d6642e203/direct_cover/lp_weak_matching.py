"""Find a bridge counterexample in fixed complete strategy cones; diagnostic only."""
import sys,json,random,itertools,math
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.certificate import StrategyCertificate,verify_certificate
from customer_attraction.exact import ExactSPESolver
from check_weak_matching import evaluate


def search(k=6,m=4,steps=50,seed=20261023,kind="solver",bridge="match",min_depth=0):
    rng=random.Random(seed)
    masks=tuple(range(1,1<<k)); n=len(masks)
    bit=np.array([[bool(B>>a&1) for a in range(k)] for B in masks],dtype=int)
    @lru_cache(None)
    def utility(h,a):
        d=bit[:,h].sum(axis=1)
        return bit[:,a]/np.maximum(d,1)
    @lru_cache(None)
    def cover(h):return bit[:,h].any(axis=1).astype(float)
    histories=tuple(h for i in range(m) for h in itertools.product(range(k),repeat=i))
    profiles=tuple(itertools.combinations(range(k),m))
    best=1e9
    for step in range(steps):
        # Include concentrated/near-disjoint inputs and broad random inputs.
        mult=np.array([rng.randrange(0,10) if B.bit_count()<=2 else (rng.randrange(0,3) if step%2 else 0) for B in masks])
        if step%3==0:
            mult[:]=[rng.randrange(0,20) if rng.random()<.2 else 0 for B in masks]
        if kind=="solver":
            inst0=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if B>>a&1),int(v)) for B,v in zip(masks,mult) if v),m)
            solver=ExactSPESolver(inst0)
            target0=rng.choice(sorted(solver.worst_outcomes()))
            cert0=solver.certificate(target0,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
            actions=dict(cert0.actions)
        else:actions={}
        for h in (() if kind=="solver" else histories):
            if len(h)<m-1:actions[h]=0
            else:
                vals=[utility(h+(a,),a)@mult for a in range(k)]
                mx=max(vals); ties=[a for a,v in enumerate(vals) if abs(v-mx)<1e-10]
                actions[h]=rng.choice(ties)
        @lru_cache(None)
        def terminal(h):return h if len(h)==m else terminal(h+(actions[h],))
        actual=terminal(())
        rows=[]
        for h in histories:
            if len(h)<min_depth:continue
            own=utility(terminal(h),actions[h])
            for a in range(k):
                if a==actions[h]:continue
                rows.append(np.r_[utility(terminal(h+(a,)),a)-own,0.])
        V=[[utility(terminal(actual[:i]+(a,)),a) for a in range(k)] for i in range(m)]
        for target in rng.sample(list(profiles),min(len(profiles),4)):
            O=cover(target)
            rr=list(rows)
            for p in profiles:
                if p!=target:rr.append(np.r_[cover(p)-O,0.])
            if bridge=="match":
                for p in itertools.permutations(target):
                    rr.append(np.r_[sum((V[i][a] for i,a in enumerate(p)),np.zeros(n)),-1.])
                obj=np.r_[cover(actual)-O,1.]
            else:
                vd=sum((V[i][a] for i in range(m) for a in target),np.zeros(n))/m
                cw=(m-1)/m if bridge=="strong_average" else 1.
                obj=np.r_[cw*cover(actual)+vd-O,0.]
            sol=linprog(obj,A_ub=np.array(rr),b_ub=np.zeros(len(rr)),A_eq=[np.r_[O,0.]],b_eq=[1.],bounds=[(0,None)]*(n+1),method='highs')
            if sol.success and sol.fun<best-1e-8:
                best=sol.fun
                print('best',step,target,best,flush=True)
                if best < -1e-7:
                    vals=[F(float(v)).limit_denominator(100000) for v in sol.x[:-1]]
                    den=math.lcm(*(v.denominator for v in vals)); ints=[int(v*den) for v in vals]
                    gcd=math.gcd(*ints); ints=[v//gcd for v in ints]
                    inst=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if B>>a&1),v) for B,v in zip(masks,ints) if v),m)
                    cert=StrategyCertificate(actions,inst.counts(actual))
                    chk=verify_certificate(inst,cert)
                    out={'search':{'step':step,'target':target,'score':best},'instance':inst.to_dict(),'certificate':cert.to_dict(),'verified':chk.valid,'violations':len(chk.violations)}
                    if chk.valid:out['evaluation']=evaluate(inst,cert)
                    Path(__file__).with_name('weak_matching_lp_candidate.json').write_text(json.dumps(out,indent=2)+'\n')
                    print('candidate',out.get('evaluation'),flush=True)
                    if chk.valid:return
    print('finished best',best,flush=True)
if __name__=='__main__':search(steps=int(sys.argv[1]) if len(sys.argv)>1 else 100,bridge=sys.argv[2] if len(sys.argv)>2 else 'match',k=int(sys.argv[3]) if len(sys.argv)>3 else 6,m=int(sys.argv[4]) if len(sys.argv)>4 else 4,min_depth=int(sys.argv[5]) if len(sys.argv)>5 else 0)
