#!/usr/bin/env python3
"""Definition-level audit of a true SPE with circulation beyond payoff SCCs.
No canonical model, solver, optimization package, or colleague audit is imported.
"""
from fractions import Fraction as Q
from itertools import product
from collections import defaultdict
import json

P,M=3,3
SIGMA={():0,(0,):2,(1,):0,(2,):0,
       (0,0):2,(0,1):0,(0,2):0,
       (1,0):0,(1,1):0,(1,2):0,
       (2,0):1,(2,1):0,(2,2):0}
WEIGHTS=(3,2,3,2,3,1,1)


def rank(rows):
    piv={}
    for row in rows:
        v=list(map(Q,row))
        for j in sorted(piv):
            if v[j]:
                scale=v[j]
                v=[x-scale*y for x,y in zip(v,piv[j])]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:
            scale=v[j];piv[j]=[x/scale for x in v]
    return len(piv)


def add(x,y):
    return tuple(a+b for a,b in zip(x,y))


def sub(x,y):
    return tuple(a-b for a,b in zip(x,y))


def terminal(h):
    h=tuple(h)
    while len(h)<M:
        h+=(SIGMA[h],)
    return h


def q_of(h):
    return tuple(h.count(a) for a in range(P))


def payoff(v):
    q,a=v
    return tuple(Q(1,sum(q[j] for j in range(P) if B>>j&1)) if B>>a&1 else Q(0)
                 for B in range(1,1<<P))


def endpoint(h,a):
    return q_of(terminal(h+(a,))),a


def potential_edge(v):
    q,a=v
    r=list(q);r[a]-=1
    return {q:1,tuple(r):-1}


def potential_sum(terms):
    out=defaultdict(int)
    for sign,v in terms:
        for c,z in potential_edge(v).items():
            out[c]+=sign*z
    return {k:v for k,v in out.items() if v}


def counts(n,p):
    if p==1:
        yield (n,)
    else:
        for k in range(n+1):
            for tail in counts(n-k,p-1):yield (k,)+tail


def audit():
    hs=[h for d in range(M) for h in product(range(P),repeat=d)]
    assert set(hs)==set(SIGMA)
    rows={};ends={};graph=defaultdict(set)
    for h in hs:
        target=endpoint(h,SIGMA[h])
        for a in range(P):
            source=endpoint(h,a)
            rows[h,a]=sub(payoff(target),payoff(source))
            ends[h,a]=source,target
            graph[source].add(target);graph[target]
    slacks={k:sum(a*w for a,w in zip(row,WEIGHTS)) for k,row in rows.items()}
    assert min(slacks.values())>=0
    # A second, expanded-unit calculation checks every ordered comparison.
    clients=[B for B,w in enumerate(WEIGHTS,1) for _ in range(w)]
    def value(leaf,i):
        return sum(Q(1,sum(B>>a&1 for a in leaf)) for B in clients if B>>leaf[i]&1)
    for h in hs:
        actual=terminal(h)
        for a in range(P):
            dev=terminal(h+(a,))
            assert value(actual,len(h))-value(dev,len(h))==slacks[h,a]
    assert all(any(bool(B>>a&1)!=bool(B>>b&1) for B in clients)
               for a in range(P) for b in range(a))
    def reach(v):
        seen={v};stack=[v]
        while stack:
            for w in graph[stack.pop()]:
                if w not in seen:seen.add(w);stack.append(w)
        return seen
    accessible={v:reach(v) for v in graph}
    remain=set(graph);components=[]
    while remain:
        v=min(remain)
        C={w for w in accessible[v] if v in accessible[w]}
        components.append(C);remain-=C
    nontrivial=[sorted(C) for C in components if len(C)>1]
    expected=sorted([((1,1,1),1),((2,0,1),0)])
    assert nontrivial==[expected]
    H=[]
    for C in components:
        base=min(C)
        H.extend(sub(payoff(v),payoff(base)) for v in C)
    assert rank(H)==1
    keys=[((),1),((0,),0),((1,),2),((2,0),0)]
    selected=[rows[k] for k in keys]
    assert tuple(map(sum,zip(*selected)))==(Q(0),)*7
    assert rank(H+[selected[0]])==2
    assert all(slacks[k]==0 for k in keys)
    terms=[]
    for key in keys:
        source,target=ends[key]
        terms.extend([(1,target),(-1,source)])
    assert potential_sum(terms)=={}
    # Universal triangle mechanism: finite regressions from direct reciprocal rows.
    triangles=0
    for p in range(3,6):
        for m in range(2,6):
            for r in counts(m-2,p):
                def F(q,a):
                    return tuple(Q(1,sum(q[j] for j in range(p) if B>>j&1)) if B>>a&1 else Q(0)
                                 for B in range(1,1<<p))
                def augment(a,b):
                    q=list(r);q[a]+=1;q[b]+=1;return tuple(q)
                a,b,c=0,1,2
                qab,qbc,qca=augment(a,b),augment(b,c),augment(c,a)
                cycle=add(add(sub(F(qab,a),F(qab,b)),sub(F(qbc,b),F(qbc,c))),sub(F(qca,c),F(qca,a)))
                assert cycle==(Q(0),)*((1<<p)-1)
                triangles+=1
    leaf=terminal(())
    W=len([B for B in clients if any(B>>a&1 for a in leaf)])
    opt=max(len([B for B in clients if any(B>>a&1 for a in h)]) for h in product(range(P),repeat=M))
    assert leaf==(0,2,0) and W==13 and opt==15
    return {'status':'passed','scope':'true SPE and strict circulation-space expansion only; not a half counterexample',
            'unit_customers':len(clients),'ordered_histories':len(hs),'all_action_comparisons':len(rows),
            'minimum_slack':str(min(slacks.values())),'root_path':leaf,
            'root_payoffs':list(map(str,[value(leaf,i) for i in range(M)])),
            'welfare':W,'OPT':opt,'payoff_SCC_space_rank':rank(H),
            'SCC_plus_root_row_rank':rank(H+[selected[0]]),
            'only_nontrivial_SCC':nontrivial,
            'zero_circulation_rows':[{'history':h,'deviation':a,'row':list(map(str,rows[h,a]))} for h,a in keys],
            'potential_endpoint_balance':{},'triangle_regressions':triangles,
            'complete_strategy':[{'history':h,'action':SIGMA[h]} for h in hs],
            'all_exact_slacks':[{'history':h,'deviation':a,'slack':str(slacks[h,a])} for h in hs for a in range(P)]}

if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
