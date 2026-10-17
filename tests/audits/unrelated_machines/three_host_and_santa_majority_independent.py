"""三端选择器与加性分配多数传播的独立精确审计。

No CCK, UNSAT, configuration LP, repository imports or old extractor.
The constructors use no optimum oracle; the attaining two-job test is enumerated. Ordinary SC items may have arbitrary positive degree.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from random import Random
from pathlib import Path
import hashlib,json,platform,time

SOURCE_CLAIMS = (
    "UM-TWO-YES-SC-DUPLICATION-HALF-v1",
    "UM-THREE-HOST-SELECTOR-THREE-HALVES-v1",
)


def rational(x):
    assert isinstance(x,(int,F)) and not isinstance(x,bool), "exact rational required"
    x=F(x);assert x>=0
    return x


def values(profits,m,allocation):
    out=[F(0) for _ in range(m)]
    assert len(allocation)==len(profits)
    for row,v in zip(profits,allocation):
        assert v is None or type(v) is int and 0<=v<m
        if v is not None:out[v]+=row.get(v,F(0))
    return out


def majority_bad_allocation(profits,m,sa,sbc,specials):
    """Return actual integral only-B/only-C allocation with every value >=1/2.

    Input items are rows of nonnegative exact rational SC utilities, missing=0.
    Specials may have arbitrary nonnegative utility vectors. Allocation sa may use
    A but neither B nor C; sbc may use B,C but not A. Both have value >=1.
    Items omitted or given zero value in input are handled explicitly.
    """
    assert type(m) is int and m>=1
    profits=[{v:rational(p) for v,p in row.items()} for row in profits]
    assert all(type(v) is int and 0<=v<m and p>=0 for row in profits for v,p in row.items())
    a,b,c=specials;assert len({a,b,c})==3 and all(0<=e<len(profits) for e in specials)
    sa=list(sa);sbc=list(sbc)
    assert sa[b] is None and sa[c] is None and sbc[a] is None
    assert min(values(profits,m,sa))>=1 and min(values(profits,m,sbc))>=1
    ordinary=[e for e in range(len(profits)) if e not in specials]
    # Move zero-value or unused ordinary goods to one arbitrary positive owner.
    # This preserves both input guarantees; all-zero goods remain unused.
    for allocation in (sa,sbc):
        for e in ordinary:
            if allocation[e] is None or profits[e].get(allocation[e],F(0))==0:
                allocation[e]=next((v for v in sorted(profits[e]) if profits[e][v]>0),None)
    def finish(allocation,available,branch,colors=None,flips=0):
        allocation=list(allocation)
        for e in specials:
            if e!=available:allocation[e]=None
        utility=values(profits,m,allocation)
        assert min(utility)>=F(1,2)
        return {'allocation':allocation,'available':'b' if available==b else 'c',
                'minimum':min(utility),'utility':utility,'branch':branch,
                'colors':colors,'flips':flips}
    if sa[a] is None or profits[a].get(sa[a],F(0))==0:
        return finish(sa,b,'A_not_used_positively')
    if sbc[b] is None or profits[b].get(sbc[b],F(0))==0:
        return finish(sbc,c,'B_not_used_positively')
    if sbc[c] is None or profits[c].get(sbc[c],F(0))==0:
        return finish(sbc,b,'C_not_used_positively')
    alpha=sa[a]
    source_b,source_c=m,m+1
    incoming=[[] for _ in range(m)]
    for e in ordinary:
        target=sbc[e]
        if target is not None:
            assert sa[e] is not None and profits[e].get(target,0)>0
            incoming[target].append((sa[e],profits[e][target],e))
    incoming[sbc[b]].append((source_b,profits[b][sbc[b]],b))
    incoming[sbc[c]].append((source_c,profits[c][sbc[c]],c))
    total=[sum((p for source,p,e in row),F(0)) for row in incoming]
    assert min(total)>=1
    colors=[0]*m+[1,0];flips=0
    while True:
        v=next((v for v in range(m) if colors[v]==0 and
                2*sum((p for u,p,e in incoming[v] if colors[u]),F(0))>=total[v]),None)
        if v is None:break
        colors[v]=1;flips+=1;assert flips<=m
    for v in range(m):
        same=sum((p for u,p,e in incoming[v] if colors[u]==colors[v]),F(0))
        assert 2*same>=total[v]
    w=colors[alpha];allocation=sa[:];allocation[a]=None
    for e in ordinary:
        if sa[e] is not None and sbc[e] is not None and colors[sa[e]]==w and colors[sbc[e]]==w:
            allocation[e]=sbc[e]
    for e,source in ((b,source_b),(c,source_c)):
        allocation[e]=sbc[e] if colors[source]==w and colors[sbc[e]]==w else None
    # Verify the exact stronger mechanism, in addition to the half conclusion.
    actual=values(profits,m,allocation)
    for v in range(m):
        assert actual[v]>=(total[v]/2 if colors[v]==w else F(1))
    return finish(allocation,b if w else c,'monotone_majority',colors,flips)


def actual_loads(jobs,m,sigma,base):
    assert len(jobs)==len(sigma)
    out=list(base)
    for row,v in zip(jobs,sigma):
        assert type(v) is int and 0<=v<m and v in row
        out[v]+=row[v]
    return out


def actual_bad_schedule(jobs,I,sa,sbc,T=F(1),hosts=None):
    """Two unit-preload YES witnesses -> original-matrix bad sigma.

    There are I internal machines and three distinct hosts of arbitrary indices;
    hosts defaults to the final three indices. Missing endpoints are unavailable.
    Input times and T are exact nonnegative rationals.
    """
    T=rational(T);assert type(I) is int and I>=0
    jobs=[{v:rational(p) for v,p in row.items()} for row in jobs]
    m=I+3;hosts=tuple(range(I,m)) if hosts is None else tuple(hosts)
    assert len(hosts)==3 and len(set(hosts))==3
    assert all(type(v) is int and 0<=v<m for v in hosts)
    assert all(type(v) is int and 0<=v<m for row in jobs for v in row)
    def base(available):
        out=[F(0)]*m
        for k,v in enumerate(hosts):out[v]=F(0) if k in available else T
        return out
    assert all(jobs)
    assert max(actual_loads(jobs,m,sa,base({0})))<=T
    assert max(actual_loads(jobs,m,sbc,base({1,2})))<=T
    def certify(sigma,available,branch,sc=None):
        load=actual_loads(jobs,m,sigma,base({available}))
        assert max(load)<=F(3,2)*T
        return {'assignment':list(sigma),'available':'b' if available==1 else 'c',
                'loads':load,'makespan':max(load),'branch':branch,
                'SC_minimum':None if sc is None else sc['minimum'],
                'flips':0 if sc is None else sc['flips']}
    if T==0:return certify(sa,1,'zero_deadline')
    fixed=[F(0)]*m;incident=[F(0)]*m;flex=[]
    for j,(row,u,v) in enumerate(zip(jobs,sa,sbc)):
        if u==v:fixed[u]+=row[u]
        else:
            flex.append((j,u,v))
            incident[u]+=row[u];incident[v]+=row[v]
    assert all(fixed[v]==0 and incident[v]<=T for v in hosts)
    assert all(2*fixed[v]+incident[v]<=2*T for v in range(m) if v not in hosts)
    if incident[hosts[0]]==0:return certify(sa,1,'zero_a')
    if incident[hosts[1]]==0:return certify(sbc,2,'zero_b')
    if incident[hosts[2]]==0:return certify(sbc,1,'zero_c')
    demand=[incident[v] if v in hosts else fixed[v]+incident[v]-T for v in range(m)]
    retained=[v for v in range(m) if demand[v]>0]
    to_sc={v:k for k,v in enumerate(retained)}
    profits=[];left=[];right=[]
    for j,u,v in flex:
        profits.append({to_sc[w]:jobs[j][w]/demand[w] for w in (u,v)
                        if w in to_sc and jobs[j][w]>0})
        left.append(to_sc[v] if v in to_sc and jobs[j][v]>0 else None)
        right.append(to_sc[u] if u in to_sc and jobs[j][u]>0 else None)
    special=[]
    for k,v in enumerate(hosts):
        special.append(len(profits));profits.append({to_sc[v]:F(1)})
        left.append(to_sc[v] if k==0 else None)
        right.append(to_sc[v] if k!=0 else None)
    sc=majority_bad_allocation(profits,len(retained),left,right,special)
    sigma=list(sa)
    for e,(j,u,v) in enumerate(flex):
        recipient=sc['allocation'][e]
        if recipient is not None:
            machine=retained[recipient];assert machine in (u,v)
            sigma[j]=v if machine==u else u
    return certify(sigma,1 if sc['available']=='b' else 2,'actual_majority',sc)


def random_weights(dest,m,rng,capacity):
    out=[0]*len(dest)
    for i in range(m):
        js=[j for j,d in enumerate(dest) if d==i]
        if len(js)>capacity:return None
        values=[1]*len(js)
        for unused in range(capacity-len(js)):
            if not js:break
            k=rng.randrange(len(js)+1)
            if k<len(js):values[k]+=1
        for j,w in zip(js,values):out[j]=w
    return out


def jsonable(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [jsonable(y) for y in x]
    return x


def main():
    started=time.perf_counter();rng=Random(220611);stats=Counter();flips=Counter();hist=Counter()
    examples=[]
    # Equality, coincident special owners and no ordinary resources.
    profits=[{0:F(1)},{0:F(1,2)},{0:F(1,2)}]
    z=majority_bad_allocation(profits,1,[0,None,None],[None,0,0],(0,1,2))
    assert z['minimum']==F(1,2);examples.append(z)
    # All three specials have two positive owners; actual recipients matter.
    p=[{0:F(1),1:F(1)},{0:F(1),1:F(1)},
       {0:F(1,2),1:F(1,2)},{0:F(1,2),1:F(1,2)}]
    z=majority_bad_allocation(p,2,[1,0,None,None],[0,None,1,1],(1,2,3))
    assert z['minimum']==F(1,2);examples.append(z)
    z=majority_bad_allocation([{0:F(1)},{1:F(1)},{},{},{}],2,
        [0,1,None,None,None],[0,1,None,None,None],(2,3,4))
    examples.append(z);stats['all_zero_specials']+=1
    # Exact exhaustive 2-agent,2-ordinary instances with fixed positive specials.
    allocation_options=list(product((None,0,1),repeat=2))
    for weights in product((F(0),F(1,2),F(1)),repeat=4):
        rows=[{0:weights[0],1:weights[1]},{0:weights[2],1:weights[3]}]
        for owners in product(range(2),repeat=3):
            for specialvalues in product((F(1,2),F(1)),repeat=3):
                p=rows+[{v:w} for v,w in zip(owners,specialvalues)]
                left=[];right=[]
                for os in allocation_options:
                    a=list(os)+[owners[0],None,None]
                    b=list(os)+[None,owners[1],owners[2]]
                    if min(values(p,2,a))>=1:left.append(a)
                    if min(values(p,2,b))>=1:right.append(b)
                for a in left:
                    for b in right:
                        z=majority_bad_allocation(p,2,a,b,(2,3,4))
                        stats['exhaustive_SC_pairs']+=1;flips[z['flips']]+=1
    # Exhaustive multi-owner special vectors with one shared ordinary good.
    for weights in product((F(0),F(1,2),F(1)),repeat=6):
        p=[{0:F(1),1:F(1)}]+[{0:weights[2*k],1:weights[2*k+1]} for k in range(3)]
        left=[];right=[]
        for u,v in product((None,0,1),repeat=2):
            a=[u,v,None,None]
            if min(values(p,2,a))>=1:left.append(a)
        for u,v,w in product((None,0,1),repeat=3):
            b=[u,None,v,w]
            if min(values(p,2,b))>=1:right.append(b)
        for a in left:
            for b in right:
                z=majority_bad_allocation(p,2,a,b,(1,2,3))
                stats['exhaustive_arbitrary_degree_special_pairs']+=1
                flips[z['flips']]+=1
    # Direct SC cases: arbitrary ordinary/special degree, zero/unused goods.
    for _ in range(3000):
        m=rng.randrange(2,12);alpha,beta,gamma=[rng.randrange(m) for unused in range(3)]
        p=[];sa=[];sbc=[]
        for u in range(m):
            if u==alpha:continue
            v=rng.randrange(m);row={u:F(1)}
            if v!=u:row[v]=F(rng.randrange(1,9),8)
            # Extra positive owners do not occur in either witness.
            for w in rng.sample(range(m),rng.randrange(m+1)):
                if w not in row:row[w]=F(rng.randrange(0,9),8)
            p.append(row);sa.append(u);sbc.append(v)
        sbvalues=values(p,m,sbc)
        for v in range(m):
            need=F(1)-(v==beta)-(v==gamma)-sbvalues[v]
            if need<=0:continue
            u=rng.choice([w for w in range(m) if w!=v]);row={v:need,u:F(1,100*m)}
            p.append(row);sa.append(u);sbc.append(v)
        # Explicit all-zero, unassigned and zero-valued-assigned ordinary item.
        p.extend([{0:F(0)},{0:F(0),1:F(1,1000)}]);sa.extend([None,0]);sbc.extend([0,None])
        special=tuple(range(len(p),len(p)+3))
        for owner in (alpha,beta,gamma):
            row={v:F(rng.randrange(0,9),8) for v in range(m)}
            row[owner]=F(1);p.append(row)
        sa.extend([alpha,None,None]);sbc.extend([None,beta,gamma])
        z=majority_bad_allocation(p,m,sa,sbc,special)
        stats['random_arbitrary_degree_SC']+=1;flips[z['flips']]+=1
    # Degenerate positive-use branches, with harmless zero-valued owners.
    for missing in range(3):
        p=[{0:F(1)},{1:F(1)},{0:F(1)},{0:F(1)},{1:F(1)}]
        a=[0,1,0,None,None];b=[0,1,None,0,1]
        if missing==0:a[2]=1
        elif missing==1:b[3]=1
        else:b[4]=0
        z=majority_bad_allocation(p,2,a,b,(2,3,4));examples.append(z)
        stats['SC_degenerate_branches']+=1
    # Actual attaining two-job gate.
    gate=[{0:F(1,2),1:F(1)},{0:F(1,2),2:F(1)}]
    z=actual_bad_schedule(gate,0,[0,0],[1,2]);assert z['makespan']==F(3,2);examples.append(z)
    # Independent finite optimality check, outside the constructor.
    for free in (1,2):
        base=[F(0) if k==free else F(1) for k in range(3)]
        optimum=min(max(actual_loads(gate,3,sigma,base))
                    for sigma in product(*(row.keys() for row in gate)))
        assert optimum==F(3,2);stats['two_job_bad_optima_enumerated']+=1
    for _ in range(2500):
        I=rng.randrange(5);m=I+3
        n=rng.randrange(0,min(11,4*(I+1))+1)
        a=[rng.randrange(I+1) for j in range(n)]
        b=[rng.choice(list(range(I))+[I+1,I+2]) for j in range(n)]
        wa=random_weights(a,m,rng,4);wb=random_weights(b,m,rng,4)
        if wa is None or wb is None:continue
        jobs=[]
        for u,v,s,t in zip(a,b,wa,wb):
            jobs.append({u:F(min(s,t),4)} if u==v else {u:F(s,4),v:F(t,4)})
        # Add a third finite alternative, absent from both witnesses.
        if jobs:
            missing=next((v for v in range(m) if v not in jobs[0]),None)
            if missing is not None:jobs[0][missing]=F(17,13)
        permutation=rng.sample(range(m),m)
        jobs=[{permutation[v]:p for v,p in row.items()} for row in jobs]
        a=[permutation[v] for v in a];b=[permutation[v] for v in b]
        hosts=tuple(permutation[v] for v in range(I,m))
        z=actual_bad_schedule(jobs,I,a,b,hosts=hosts)
        stats['random_actual_'+z['branch']]+=1;hist[str(z['makespan'])]+=1
    fixed=[{1:F(1,2),0:F(3,4)},{0:F(3,4),2:F(1)},
           {1:F(1,2),3:F(1)},{0:F(1,4),3:F(11,3)}]
    for T in (F(1),F(1,10**120+151),F(10**120+151,37)):
        jobs=[{v:p*T for v,p in row.items()} for row in fixed]
        z=actual_bad_schedule(jobs,1,[1,0,1,0],[0,2,3,0],T);examples.append(z)
        stats['fixed_positive_internal_and_huge_rational']+=1
    permutation=[2,0,3,1]
    permuted=[{permutation[v]:p for v,p in row.items()} for row in fixed]
    examples.append(actual_bad_schedule(permuted,1,[0,2,0,2],[2,3,1,2],hosts=(0,3,1)))
    stats['explicit_nonconsecutive_host_indices']+=1
    for jobs,I,a,b,T in [([{0:F(0),1:F(0),2:F(9)}],0,[0],[1],F(0)),
                          ([{0:F(0),1:F(0),2:F(9)}],0,[0],[1],F(1)),
                          ([],2,[],[],F(1)),([],0,[],[],F(0))]:
        examples.append(actual_bad_schedule(jobs,I,a,b,T));stats['actual_zero_and_empty_boundaries']+=1
    result={'python':platform.python_version(),'seed':220611,'precision':'Fraction exact',
            'source_claims':SOURCE_CLAIMS,'algorithm':'independent monotone majority; direct actual complement',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'counts':stats,'SC_flip_histogram':flips,'actual_makespan_histogram':hist,
            'examples':examples,'runtime_seconds':round(time.perf_counter()-started,3),
            'limits':'Finite exact audit, no general UM hardness. Direct majority proof uses two supplied YES allocations and three distinct special items; arbitrary ordinary and special utility degree. Actual contexts are exactly fixed T preloads.'}
    print(json.dumps(jsonable(result),indent=2,sort_keys=True))

if __name__=='__main__':main()
