"""Fixed complete-child-SPE cone attacks of general ROW contract; numeric discovery only."""
from functools import lru_cache
from math import lcm
from pathlib import Path
import random,json
import numpy as np
from scipy.optimize import linprog

def probe(k,r,weights,prefix):
    masks=list(range(1,1<<k));n=len(masks)
    @lru_cache(None)
    def coeff(q,a):
        return np.array([((1/sum(q[j] for j in range(k) if mask>>j&1)) if mask>>a&1 and sum(q[j] for j in range(k) if mask>>j&1) else 0.) for mask in masks])
    @lru_cache(None)
    def cov(q):return np.array([float(any(q[j] for j in range(k) if mask>>j&1)) for mask in masks])
    @lru_cache(None)
    def val(q,a):return float(coeff(q,a)@weights)
    @lru_cache(None)
    def outcomes(q,left):
        if not left:return (q,)
        cs=[]
        for a in range(k):
            q1=list(q);q1[a]+=1
            cs.append(outcomes(tuple(q1),left-1))
        cap=max(min(val(z,a) for z in cs[a]) for a in range(k))
        return tuple(set(z for a in range(k) for z in cs[a] if val(z,a)>=cap-1e-9))
    children=[]
    for a in range(k):
        q=list(prefix);q[a]+=1
        children.append(outcomes(tuple(q),r-1))
    leaves=[min(children[a],key=lambda z:val(z,a)) for a in range(k)]
    ds=[val(leaves[a],a) for a in range(k)]
    # Find the most nearly failing choice with A0 not constrained to minimizing root payoff.
    best=None
    for a0 in range(k):
        for z0 in children[a0]:
            W0=float(cov(z0)@weights)
            for bits in range(1,1<<k):
                U=sum(weights[t] for t,mask in enumerate(masks) if mask&bits)
                d=sum((val(z0,a) if a==a0 else ds[a]) for a in range(k) if bits>>a&1)
                gap=U-W0-d
                if best is None or gap>best[0]:best=(gap,a0,z0,bits)
    gap,a0,z0,bits=best;leaves[a0]=z0
    policy={}
    def build(q,left,target,h):
        if not left:return
        cs=[]
        for a in range(k):
            q1=list(q);q1[a]+=1
            cs.append(outcomes(tuple(q1),left-1))
        cap=max(min(val(z,a) for z in cs[a]) for a in range(k))
        candidates=[a for a in range(k) if target in cs[a] and val(target,a)>=cap-1e-9]
        a=candidates[0];policy[h]=a
        for b in range(k):
            q1=list(q);q1[b]+=1
            z=target if b==a else min(cs[b],key=lambda z:val(z,b))
            build(tuple(q1),left-1,z,h+(b,))
    for a in range(k):
        q=list(prefix);q[a]+=1;build(tuple(q),r-1,leaves[a],(a,))
    def terminal(h):
        h=list(h)
        while len(h)<r:h.append(policy[tuple(h)])
        q=list(prefix)
        for a in h:q[a]+=1
        return tuple(q)
    rows=[]
    for h,a in policy.items():
        z=terminal(h+(a,))
        for b in range(k):
            if b!=a:rows.append(coeff(terminal(h+(b,)),b)-coeff(z,a))
    objective=np.array([float(mask&bits!=0) for mask in masks])-cov(z0)
    for a in range(k):
        if bits>>a&1:objective-=coeff(leaves[a],a)
    result=linprog(-objective,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
    return result,dict(k=k,r=r,prefix=prefix,A0=a0,subset=[a for a in range(k) if bits>>a&1],policy={','.join(map(str,h)):a for h,a in policy.items()},children=leaves,initial_gap=gap,constraints=len(rows))

def main():
    rng=random.Random(725018)
    best=0
    for it in range(100):
        k=5 if it<60 else 6;r=4 if it%3 else 5
        weights=np.array([rng.randrange(1,41) if rng.random()<(0.3 if mask.bit_count()<=2 else 0.08) else 0 for mask in range(1,1<<k)],dtype=float)
        prefix=[0]*k
        for _ in range(rng.randrange(0,3)):prefix[rng.randrange(k)]+=1
        result,meta=probe(k,r,weights,tuple(prefix))
        if result.success:
            opt=-result.fun
            if opt>1e-8:
                meta.update(weights=result.x.tolist(),gap=opt)
                p=Path(__file__).with_name('child_menu_cone_discovery.json');p.write_text(json.dumps(meta,indent=2))
                print('FOUND',json.dumps(meta),flush=True);return
        print('iteration',it,'gap',None if not result.success else -result.fun,flush=True)
    print('NO COUNTEREXAMPLE: finite cones only',flush=True)
if __name__=='__main__':main()
