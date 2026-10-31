from fractions import Fraction as F
from itertools import product, permutations
from functools import lru_cache
import json


def instance(k,d):
    a=F(k-1,k); delta=F(k-1,k*k); c=F(1,k*k); beta=F(1,k)
    D=d+k-1
    roots=list(range(k+1)); P=[]; S0=[]; S1=[]; names=[]; chains=[]; machine=1
    # 0 is root; each entry records p at two endpoints. zero bit = root/home
    for g in roots:
        length=d if g<k else D
        home=list(range(machine,machine+length)); machine+=length
        chains.append(home)
        p0=delta+c/4 if g==0 else delta if g<k else a
        P.append(((0,p0),(home[0],F(1)))); names.append(f'g{g}')
        S0.append(int(g<k));S1.append(int(g==k))
    for g,home in enumerate(chains):
        for h,i in enumerate(home):
            dest=home[h+1] if h+1<len(home) else 0
            p1=F(1) if dest else c/2 if g==0 else c
            P.append(((i,a),(dest,p1))); names.append(f'e{g}_{h}')
            S0.append(int(g<k));S1.append(int(g==k))
    n=len(P);m=machine
    def loads(bits):
        out=[F(0)]*m
        for e,z in zip(P,bits):
            i,p=e[z];out[i]+=p
        return out
    x=[(beta if z0==0 else F(0))+(1-beta if z1==0 else F(0)) for z0,z1 in zip(S0,S1)]
    # Return x as fraction on endpoint0, endpoint1 has complementary mass.
    bad=[int(name.startswith('g0') or name.startswith('e0_')) for name in names]
    return P,S0,S1,x,bad,loads,names,m


def slots(P,x,m,tie_order=None):
    # Process exact positive intervals, use job labels as final stable ties only.
    edges=[[] for _ in P]; allslots=[]
    for i in range(m):
        entries=[]
        for j,e in enumerate(P):
            for z,(ii,p) in enumerate(e):
                if ii==i:
                    w=x[j] if z==0 else 1-x[j]
                    if w>0:entries.append((p,j,w))
        entries.sort(key=lambda e:(-e[0],e[1] if tie_order is None else tie_order.get(e[1],e[1])))
        cumulative=F(0)
        for p,j,w in entries:
            for s in range(cumulative.numerator//cumulative.denominator, -(-(cumulative+w).numerator//(cumulative+w).denominator)):
                overlap=min(cumulative+w,s+1)-max(cumulative,s)
                if overlap>0:
                    tag=(i,s)
                    if tag not in allslots:allslots.append(tag)
                    edges[j].append((tag,p))
            cumulative+=w
    index={tag:j for j,tag in enumerate(allslots)}
    return [[(index[tag],p,tag[0]) for tag,p in es] for es in edges],allslots


def matching_opt(P,x,m,tie_order=None):
    es,sl=slots(P,x,m,tie_order);n=len(P)
    assert len(sl)==n
    # Small cases; all minimum-cost machine assignments retained explicitly.
    order=sorted(range(n),key=lambda j:len(es[j]))
    @lru_cache(None)
    def rec(q,used):
        if q==n:return (F(0),frozenset({()}))
        j=order[q]; best=None;outs=set()
        for s,p,i in es[j]:
            if used>>s&1:continue
            val,suffix=rec(q+1,used|1<<s)
            if val is None:continue
            val+=p
            if best is None or val<best:best=val;outs=set()
            if val==best:outs.update((i,)+w for w in suffix)
        return best,frozenset(outs)
    val,out=rec(0,0)
    canonical=[]
    for o in out:
        vector=[None]*n
        for j,i in zip(order,o):vector[j]=i
        canonical.append(tuple(vector))
    return val,set(canonical),len(sl),rec.cache_info().currsize


def run(k,d,do_matching=True):
    P,S0,S1,x,bad,loads,names,m=instance(k,d);n=len(P)
    B=F(2)-F(3,k)+F(3,2*k*k)
    assert max(loads(S0))==max(loads(S1))==1
    assert max(loads(bad))==B
    assert all(0<t<1 for t in x)
    badmac=tuple(e[z][0] for e,z in zip(P,bad))
    opt=None;minjobs=None;minmachines=None;feasible=0;bestwitness=None
    for bits in product((0,1),repeat=n):
        cap=max(loads(bits))
        if opt is None or cap<opt:opt=cap
        if bits==tuple(bad) or cap>B:continue
        feasible+=1
        changed=[j for j,(z,v) in enumerate(zip(bits,bad)) if z!=v]
        machines={i for j in changed for i,_ in P[j]}
        if minjobs is None or len(changed)<minjobs:minjobs=len(changed);bestwitness=bits
        if minmachines is None or len(machines)<minmachines:minmachines=len(machines)
        assert len(changed)>=d+1 and len(machines)>=d+1,(k,d,bits)
    assert opt==1
    assert minjobs==minmachines==d+1
    # Existence same witness hitting both bounds with strict cap reduction.
    witness=list(bad)
    for j,name in enumerate(names):
        if name=='g1' or name.startswith('e1_'):witness[j]=1
    changed=[j for j,(z,v) in enumerate(zip(witness,bad)) if z!=v]
    touched={i for j in changed for i,_ in P[j]}
    assert len(changed)==len(touched)==d+1 and max(loads(witness))<B
    result=dict(k=k,d=d,n=n,m=m,schedules=2**n,OPT=str(opt),B=str(B),min_jobs=minjobs,min_machines=minmachines,other_B_feasible=feasible)
    if do_matching:
        val,assignments,ns,states=matching_opt(P,x,m)
        assert assignments=={badmac},(k,d,val,assignments,badmac)
        result.update(mincost=str(val),mincost_machine_assignments=len(assignments),slotcount=ns,matching_DP_states=states)
    return result

if __name__=='__main__':
    cases=[(3,1),(3,2),(4,1),(5,1)]
    records=[run(k,d,True) for k,d in cases]
    tie_checks=[]
    for k in (3,4):
        P,S0,S1,x,bad,loads,names,m=instance(k,1)
        badmac=tuple(e[z][0] for e,z in zip(P,bad))
        ordinary_tiny=[j for j,name in enumerate(names) if name in {f'g{v}' for v in range(1,k)}]
        ordinary_tail=[j for j,(e,name) in enumerate(zip(P,names)) if e[1][0]==0 and e[1][1]==F(1,k*k)]
        count=0
        for tinies in permutations(ordinary_tiny):
            for tails in permutations(ordinary_tail):
                order={j:q for q,j in enumerate(tinies)}
                order.update({j:q for q,j in enumerate(tails)})
                cost,assignments,ns,states=matching_opt(P,x,m,order)
                assert assignments=={badmac}
                count+=1
        tie_checks.append(dict(k=k,d=1,all_root_tie_orders=count))
    output=dict(exhaustive_cases=records,total_schedules=sum(r['schedules'] for r in records),all_tie_orders=tie_checks)
    print(json.dumps(output,indent=2))
