#!/usr/bin/env python3
"""Independent finite reduction/rounding checks; no polynomial matching-selection algorithm."""
from fractions import Fraction as F
from itertools import product,combinations
import importlib.util,json,random,hashlib,platform
from pathlib import Path
spec=importlib.util.spec_from_file_location('baseline',Path(__file__).with_name('rounding_and_gap.py'))
baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)

def reduce_3dm(q,triples):
    if q==0:return [[]]
    if not triples:return [[F(1),F(1)]]
    s=len(triples);p=[[None]*(q+3*s) for _ in range(s+3*q)]
    for a in range(s):
        for j in range(q):p[a][j]=F(1)
        for dim,e in enumerate(triples[a]):
            j=q+3*a+dim;p[a][j]=F(1,3);p[s+dim*q+e][j]=F(1)
    return p

def perfect_3dm(q,triples):
    for chosen in combinations(triples,q):
        if all(len({t[d] for t in chosen})==q for d in range(3)):return chosen
    return None

def scheduling_oracle(p,T=F(1)):
    """Exponential independent scheduling oracle; no reduction-specific combinatorics."""
    from math import lcm
    scale=T.denominator
    for row in p:
        for value in row:
            if value is not None:scale=lcm(scale,F(value).denominator)
    p=[[None if value is None else int(F(value)*scale) for value in row] for row in p]
    T=int(T*scale)
    m=len(p);n=len(p[0]);loads=[0]*m;a=[None]*n;nodes=0
    choices=[[i for i in range(m) if p[i][j] is not None and p[i][j]<=T] for j in range(n)]
    mandatory={j for j in range(n) if all(2*p[i][j]>T for i in choices[j])}
    def dfs(todo):
        nonlocal nodes
        nodes+=1
        if not todo:return tuple(a)
        pool=todo&mandatory or todo
        avail={j:[i for i in choices[j] if loads[i]+p[i][j]<=T] for j in pool}
        j=min(pool,key=lambda j:(len(avail[j]),j))
        for i in sorted(avail[j],key=lambda i:(p[i][j],i)):
            a[j]=i;loads[i]+=p[i][j]
            ans=dfs(todo-{j})
            if ans is not None:return ans
            loads[i]-=p[i][j];a[j]=None
        return None
    answer=dfs(set(range(n)))
    return answer,nodes

def certificate_from_schedule(p,a,T=F(1)):
    H={j:i for j,i in enumerate(a) if p[i][j]>T/2}
    assert len(set(H.values()))==len(H)
    n=len(a);x=[[F(0)]*n for _ in p]
    for j,i in enumerate(a):
        if j not in H:x[i][j]=F(1)
    return H,x

def round_interface(p,T,H,x,delta=F(0)):
    m=len(p);n=len(p[0]);assert delta>=0 and len(set(H.values()))==len(H)
    hi=[F(0)]*m
    for j,i in H.items():
        assert T/2<p[i][j]<=T;hi[i]=p[i][j]
    unmatched=[j for j in range(n) if j not in H]
    pp=[[row[j] if row[j] is not None and row[j]<=T/2 else None for j in unmatched] for row in p]
    xx=[[row[j] for j in unmatched] for row in x]
    for jj,j in enumerate(unmatched):assert sum(xx[i][jj] for i in range(m))==1
    for i in range(m):
        assert sum((pp[i][z] or 0)*xx[i][z] for z in range(len(unmatched)))<=(1+delta)*T-hi[i]
    small_a,small_loads=baseline.round_slots(pp,xx,(1+delta)*T)
    a=[None]*n
    for j,i in H.items():a[j]=i
    for j,i in zip(unmatched,small_a):a[j]=i
    final=baseline.loads(p,a)
    assert all(final[i]<=(F(3,2)+delta)*T for i in range(m))
    assert all(final[i]==hi[i]+small_loads[i] for i in range(m))
    return a,final

def audit():
    rng=random.Random(20261016);cases=0;yes=0;nodes=0
    for q in (0,1,2):
        universe=list(product(range(q),repeat=3))
        for mask in range(1<<len(universe)):
            triples=[v for z,v in enumerate(universe) if mask>>z&1]
            expected=perfect_3dm(q,triples)
            p=reduce_3dm(q,triples);a,nn=scheduling_oracle(p)
            assert (a is not None)==(expected is not None),(q,triples,expected,a)
            if a is not None:
                H,x=certificate_from_schedule(p,a);round_interface(p,F(1),H,x);yes+=1
            cases+=1;nodes+=nn
    for _ in range(50):
        q=3;triples=rng.sample(list(product(range(q),repeat=3)),rng.randint(1,12))
        expected=perfect_3dm(q,triples);p=reduce_3dm(q,triples);a,nn=scheduling_oracle(p)
        assert (a is not None)==(expected is not None)
        if a is not None:
            H,x=certificate_from_schedule(p,a);round_interface(p,F(1),H,x);yes+=1
        cases+=1;nodes+=nn
    rounding_cases=[]
    # Truly fractional residual certificates, exact arithmetic.
    for T in (F(0),F(1),F(7,11),F(1,2**400+1)):
        if T==0:
            p=[[F(0),F(0)],[F(0),None]];H={};x=[[F(1,2),F(1)],[F(1,2),F(0)]]
        else:
            # One fixed big job on machine0; remaining eight small jobs split to residual capacities.
            p=[[3*T/4]+[T/4]*8,[None]+[T/4]*8,[None]+[T/4]*8]
            H={0:0};x=[[F(0)]+[F(1,8)]*8,[F(0)]+[F(7,16)]*8,[F(0)]+[F(7,16)]*8]
        a,ll=round_interface(p,T,H,x)
        rounding_cases.append({'T':str(T),'maximum_load':str(max(ll)),'bound':str(3*T/2),'assignment':a})
    return {'schema_version':1,'python_version':platform.python_version(),'arithmetic':'Fraction; exact; no floating point solver','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(Path(__file__).with_name('rounding_and_gap.py').read_bytes()).hexdigest(),'seed':20261016,'warning':'Finite checks only; NP-hardness uses universal equivalence proof and classical perfect3DM hardness.','reduction_instances':cases,'yes_instances':yes,'exhaustive_oracle_search_nodes':nodes,'fractional_rounding_cases':rounding_cases}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
