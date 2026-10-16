"""守恒通道证书搜索与非单位需求参数的精确根树构造。

Contract: high k>=2K; transit 1<=k<=2K-1.  Separate
parent-choice tree enumeration is the oracle, not the flow constructor.
No floating point, no overwritten frozen evidence, stdlib only.
"""
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, platform, random, time


def structure(n, edges, k, root=0):
    assert type(n) is int and n>=1 and len(k)==n
    assert type(root) is int and 0<=root<n
    assert all(type(v) is int and v>=0 for v in k)
    assert len(set(edges))==len(edges)
    out=[[] for _ in range(n)];ins=[[] for _ in range(n)]
    for u,v in edges:
        assert type(u) is int and type(v) is int and 0<=u<n and 0<=v<n and u!=v
        out[u].append(v);ins[v].append(u)
    assert not ins[root]
    assert all(k[v] or not out[v] for v in range(n))
    deg=list(map(len,ins));q=deque(v for v in range(n) if deg[v]==0);top=[]
    while q:
        v=q.popleft();top.append(v)
        for w in out[v]:
            deg[w]-=1
            if deg[w]==0:q.append(w)
    assert len(top)==n
    return out,ins,top


class Flow:
    def __init__(self,n):
        self.adj=[{} for _ in range(n)];self.initial={}
    def add(self,u,v,c):
        self.adj[u][v]=self.adj[u].get(v,0)+c
        self.adj[v].setdefault(u,0)
        self.initial[u,v]=self.initial.get((u,v),0)+c
    def solve(self,s,t):
        value=0;rounds=0
        while True:
            prev={s:None};q=deque([s])
            while q and t not in prev:
                u=q.popleft()
                for v,c in self.adj[u].items():
                    if c>0 and v not in prev:prev[v]=u;q.append(v)
            if t not in prev:return value,rounds
            v=t;delta=None
            while prev[v] is not None:
                u=prev[v];delta=self.adj[u][v] if delta is None else min(delta,self.adj[u][v]);v=u
            v=t
            while prev[v] is not None:
                u=prev[v];self.adj[u][v]-=delta;self.adj[v][u]+=delta;v=u
            value+=delta;rounds+=1
    def used(self,u,v):return self.initial[u,v]-self.adj[u][v]


def check_certificate(n,edges,k,K,W,f,root=0):
    structure(n,edges,k,root)
    assert type(K) is int and K>=1 and root in W and all(0<=v<n for v in W)
    allowed={(u,v) for u,v in edges if u in W and v in W}
    incoming=[F(0) for _ in k];outgoing=[F(0) for _ in k]
    for e,a in f.items():
        assert e in allowed and (type(a) is int or isinstance(a,F)) and a>=0
        u,v=e;incoming[v]+=a;outgoing[u]+=a
    for v in W:
        assert v==root or incoming[v]<=K
        if k[v]>=2*K:assert outgoing[v]>=k[v]
        elif k[v]>0:
            if v==root:assert outgoing[v]>=K
            else:assert outgoing[v]==incoming[v]
    return True


def network(n,edges,k,K,W,root,unit):
    W=set(W);B={v for v in W if k[v]>=2*K}
    s,t=2*n,2*n+1;net=Flow(2*n+2);sources={}
    cap=1 if unit else K
    for v in sorted(W):
        supply=(k[v]//K if unit else k[v]) if v in B else cap if v==root and k[v] else 0
        if supply:net.add(s,2*v+1,supply);sources[v]=supply
        if v in B or k[v]==0:net.add(2*v,t,cap)
        elif v!=root:net.add(2*v,2*v+1,cap)
    orig=[e for e in sorted(edges) if e[0] in W and e[1] in W]
    for u,v in orig:net.add(2*u+1,2*v,cap)
    value,rounds=net.solve(s,t)
    if value!=sum(sources.values()):return None
    return {(u,v):net.used(2*u+1,2*v) for u,v in orig if net.used(2*u+1,2*v)},rounds


def find(n,edges,k,K,W,root=0):
    structure(n,edges,k,root);assert type(K) is int and K>=1 and root in W
    got=network(n,edges,k,K,W,root,False)
    if got is None:return None
    f,_=got;check_certificate(n,edges,k,K,W,f,root);return f


def score(n,H,k,root=0):
    out=[[] for _ in k];indeg=[0]*n
    for u,v in H:out[u].append(v);indeg[v]+=1
    assert not indeg[root] and max(indeg)<=1
    seen={root};q=[root]
    for v in q:
        for w in out[v]:assert w not in seen;seen.add(w);q.append(w)
    assert all(u in seen and v in seen for u,v in H)
    return min([F(1)]+[F(len(out[v]),k[v]) for v in seen if k[v]])


def extract(n,edges,k,K,W,f,root=0):
    check_certificate(n,edges,k,K,W,f,root)
    if not k[root]:return []
    got=network(n,edges,k,K,W,root,True);assert got is not None
    used,rounds=got;assert rounds<=len(edges)
    out=[[] for _ in k]
    for u,v in used:out[u].append(v)
    seen={root};q=[root]
    for v in q:
        for w in out[v]:assert w not in seen;seen.add(w);q.append(w)
    H=[(u,v) for u,v in used if u in seen]
    assert score(n,H,k,root)>=F(1,2*K-1)
    return H


def search_support(n,edges,k,K,root=0):
    """Search every high subset; 2^h_K poly bit operations."""
    structure(n,edges,k,root);assert type(K) is int and K>=1
    if not k[root]:return set([root]), {}, []
    high=[v for v in range(n) if k[v]>=2*K]
    passive={v for v in range(n) if k[v]<2*K}
    for bits in product((False,True),repeat=len(high)):
        W=passive|{v for v,bit in zip(high,bits) if bit}
        if root not in W:continue
        f=find(n,edges,k,K,W,root)
        if f is not None:
            H=extract(n,edges,k,K,W,f,root)
            assert score(n,H,k,root)>=F(1,2*K-1)
            return W,f,H
    return None


def threshold_tree(n,edges,k,root=0):
    """Exact score>=1 test; returns actual edges or None."""
    got=search_support(n,edges,k,1,root)
    return None if got is None else got[2]


def min_certificate(n,edges,k,W,root=0):
    """Least feasible integer K for fixed W; no value-sized loop."""
    structure(n,edges,k,root);assert root in W
    upper=max(k[v] for v in W)//2+1
    witness=find(n,edges,k,upper,W,root)
    if witness is None:return None
    lower=1
    while lower<upper:
        mid=(lower+upper)//2;candidate=find(n,edges,k,mid,W,root)
        if candidate is None:lower=mid+1
        else:upper,witness=mid,candidate
    check_certificate(n,edges,k,lower,W,witness,root)
    return lower,witness


def optimize(n,edges,k,root=0):
    out,_,_=structure(n,edges,k,root)
    gamma=sorted({F(1)}|{F(a,k[v]) for v in range(n) if k[v] for a in range(1,min(k[v],len(out[v]))+1)})
    best=[];value=F(0) if k[root] else F(1)
    for tau in gamma:
        scaled=[(tau.numerator*a+tau.denominator-1)//tau.denominator if a else 0 for a in k]
        H=threshold_tree(n,edges,scaled,root)
        if H is None:break
        actual=score(n,H,k,root)
        assert actual>=tau
        if actual>value:best,value=H,actual
    return value,best


def tree_oracle(n,edges,k,root=0):
    _,ins,_=structure(n,edges,k,root)
    order=[v for v in range(n) if v!=root]
    best=F(0) if k[root] else F(1);witness=[];tested=0
    for choices in product(*[[-1]+ins[v] for v in order]):
        child=[[] for _ in k]
        for v,p in zip(order,choices):
            if p>=0:child[p].append(v)
        seen={root};q=[root]
        for v in q:
            for w in child[v]:seen.add(w);q.append(w)
        val=min([F(1)]+[F(len(child[v]),k[v]) for v in seen if k[v]])
        tested+=1
        if val>best:best=val;witness=[(u,v) for u in seen for v in child[u]]
    return best,witness,tested


def exhaustive():
    count=trees=fixed=saturated=0
    for n in range(1,5):
        possible=[(u,v) for u in range(n) for v in range(u+1,n)]
        for bits in product((0,1),repeat=len(possible)):
            edges=[e for e,b in zip(possible,bits) if b]
            for k in product((0,1,2,4),repeat=n):
                if any(not k[u] for u,v in edges):continue
                count+=1
                truth,H,nt=tree_oracle(n,edges,k);trees+=nt
                actual,got=optimize(n,edges,k)
                assert actual==truth,(n,edges,k,truth,actual)
                assert score(n,got,k)==actual
                # This is separately a fixed-support relaxed-certificate check.
                W=set(range(n))
                feas=[]
                for K in (1,2,3):
                    f=find(n,edges,k,K,W);fixed+=1;feas.append(f is not None)
                    if f is not None:
                        g=extract(n,edges,k,K,W,f);saturated+=1
                        assert score(n,g,k)>=F(1,2*K-1)
                assert feas==sorted(feas)
    return dict(all_ordered_DAG_cases=count,parent_choices_enumerated=trees,full_support_K_cases=fixed,valid_full_support_extractions=saturated)


def fixtures():
    import importlib.util
    old=Path(__file__).with_name('rooted_dag_congestion_flow.py')
    s=importlib.util.spec_from_file_location('old',old);oldmod=importlib.util.module_from_spec(s);s.loader.exec_module(oldmod)
    result=[]
    for k0 in [1,3,5,9,10**100+1]:
        n=2;E=[(0,1)];k=[k0,0];W=set(range(n));K=(k0+1)//2
        f=find(n,E,k,K,W);assert f is not None
        H=extract(n,E,k,K,W,f);beta=score(n,H,k)
        oldK,_=oldmod.min_certificate(n,E,k,W)
        assert oldK==k0 and beta==F(1,k0)
        exact,_=optimize(n,E,k);assert exact==beta
        result.append(dict(type='single_edge_sharp',root_demand=k0,new_K=K,old_K=oldK,true_score=str(beta),new_guarantee=str(F(1,2*K-1))))
    n=4;E=[(0,1),(0,2),(1,3),(2,3)];k=[1,1,1,0];W=set(range(n))
    oldK,_=oldmod.min_certificate(n,E,k,W);f=find(n,E,k,1,W)
    assert oldK==2 and f is not None
    result.append(dict(type='unit_merge',old_K=oldK,new_K=1,score=str(score(n,extract(n,E,k,1,W,f),k))))
    # Root-terminal fixed-support distinction remains necessary.
    huge=10**100+39
    answer=min_certificate(2,[],[0,huge],set([0,1]),0)
    assert answer[0]==huge//2+1
    result.append(dict(type='terminal_root_remote_dead_high',minimum_K=answer[0]))
    # A valid old flow need not literally satisfy the new conservation rows.
    args=(5,[(0,1),(1,2),(1,3),(1,4)],[1,3,0,0,0],2,set(range(5)))
    old_f={(0,1):2,(1,2):1,(1,3):1,(1,4):1}
    oldmod.validate(*args,old_f)
    try:check_certificate(*args,old_f)
    except AssertionError:pass
    else:raise AssertionError('old-to-new must transform f, not reuse it')
    f=find(*args);assert f is not None
    result.append(dict(type='old_certificate_requires_trimming',old_flow_rejected_as_new=True,new_found=True))
    # Arbitrary root label and nonuniform huge rational optimal score.
    n=4;E=[(3,2),(2,0),(2,1)];k=[0,0,10**100+39,1]
    a,H=optimize(n,E,k,3);assert a==F(2,k[2]) and score(n,H,k,3)==a
    result.append(dict(type='huge_nonroot_arbitrary_root',h=1,score=str(a)))
    # An arbitrarily long all-unit corridor has h=0 and requires only flow.
    n=1502;E=[(v,v+1) for v in range(n-1)];k=[1]*(n-1)+[0]
    a,H=optimize(n,E,k);assert a==1 and len(H)==n-1
    result.append(dict(type='deep_unit_corridor',n=n,h=0,score=str(a)))
    return result


def random_cases():
    rng=random.Random(7102026);count=parent_tests=0
    for _ in range(500):
        n=rng.randrange(5,9)
        edges=[(u,v) for u in range(n) for v in range(u+1,n) if rng.random()<0.22]
        k=[rng.choice((1,1,1,2,3,7)) if any(u==v for u,w in edges) else rng.choice((0,1,2)) for v in range(n)]
        truth,H,nt=tree_oracle(n,edges,k);parent_tests+=nt
        a,H=optimize(n,edges,k);assert a==truth
        perm=list(range(n));rng.shuffle(perm)
        remap=[None]*n
        for v in range(n):remap[perm[v]]=k[v]
        b,G=optimize(n,[(perm[u],perm[v]) for u,v in edges],remap,perm[0]);assert b==truth
        count+=1
    return dict(random_graphs=count,seed=7102026,random_parent_choices=parent_tests,arbitrary_root_relabelings=count)


def main():
    started=time.monotonic()
    d={'title':'可守恒中等需求通道与非单位分叉参数的精确探索','python':platform.python_version(),'arithmetic':'int/Fraction; exact','sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    d.update(exhaustive());d['fixtures']=fixtures();d.update(random_cases())
    d['limits']='Finite experiment only; no claim of global novelty, no polynomial algorithm when h is unbounded, no UM-TARGET solution.'
    d['elapsed_seconds']=round(time.monotonic()-started,3)
    print(json.dumps(d,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
