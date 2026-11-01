#!/usr/bin/env python3
"""Exact finite audits for truncated-intersection representation; no half theorem.

Uses only standard-library Fractions. Outputs JSON. The general claims are
proved in truncated_intersection_moments.md, not inferred from these tests.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from random import Random
import json


def subsets(mask):
    sub=mask
    while sub:
        yield sub
        sub=(sub-1)&mask


def counts(m,p):
    if p==1:
        yield (m,)
    else:
        for k in range(m+1):
            for tail in counts(m-k,p-1):
                yield (k,)+tail


def payoff(q,a,b):
    if not (b>>a)&1:
        return Q(0)
    return Q(1,sum(c for j,c in enumerate(q) if b>>j&1))


def mobius(values,p):
    c=list(values)
    for i in range(p):
        for a in range(1<<p):
            if a>>i&1:
                c[a]-=c[a^(1<<i)]
    return c


def rank(rows):
    piv={}
    for row in rows:
        v=list(map(Q,row))
        for j in sorted(piv):
            if v[j]:
                scale=v[j]
                v=[x-scale*y for x,y in zip(v,piv[j])]
        pivot=next((j for j,x in enumerate(v) if x),None)
        if pivot is not None:
            z=v[pivot]
            piv[pivot]=[x/z for x in v]
    return len(piv)


def moments(w,p,m):
    return {a:sum(v for b,v in w.items() if b&a==a)
            for a in range(1,1<<p) if a.bit_count()<=m}


def utility(w,q,a):
    return sum(v*payoff(q,a,b) for b,v in w.items())


def welfare(w,q):
    used=sum(1<<j for j,c in enumerate(q) if c)
    return sum(v for b,v in w.items() if b&used)


def dependence(columns):
    """Return a rational nonzero dependence when columns are dependent."""
    piv={}
    n=len(columns)
    for j,col in enumerate(columns):
        v=list(map(Q,col))
        coeff=[Q(int(k==j)) for k in range(n)]
        for i,(base,expansion) in sorted(piv.items()):
            if v[i]:
                scale=v[i]
                v=[x-scale*y for x,y in zip(v,base)]
                coeff=[x-scale*y for x,y in zip(coeff,expansion)]
        pivot=next((i for i,x in enumerate(v) if x),None)
        if pivot is None:
            assert any(coeff)
            assert all(sum(coeff[j]*columns[j][i] for j in range(n))==0
                       for i in range(len(col)))
            return coeff
        scale=v[pivot]
        piv[pivot]=([x/scale for x in v],[x/scale for x in coeff])
    return None


def compress(w,p,m):
    labels=tuple(a for a in range(1,1<<p) if a.bit_count()<=m)
    w={b:Q(v) for b,v in w.items() if v}
    steps=0
    while len(w)>len(labels):
        bs=tuple(w)
        cols=[[int(b&a==a) for a in labels] for b in bs]
        delta=dependence(cols)
        assert delta is not None
        if not any(x>0 for x in delta):
            delta=[-x for x in delta]
        alpha=min(w[b]/x for b,x in zip(bs,delta) if x>0)
        w={b:w[b]-alpha*x for b,x in zip(bs,delta)}
        assert all(x>=0 for x in w.values())
        w={b:v for b,v in w.items() if v}
        steps+=1
    return w,steps


def audit():
    coefficient_rows=0
    rank_cases=[]
    for p in range(1,7):
        for m in range(1,5):
            rows=[]
            for q in counts(m,p):
                for a in range(p):
                    if not q[a]:
                        continue
                    values=[payoff(q,a,b) for b in range(1<<p)]
                    coeff=mobius(values,p)
                    assert coeff[0]==0
                    assert all(c==0 for b,c in enumerate(coeff) if b.bit_count()>m)
                    assert all(c==0 for b,c in enumerate(coeff) if not b>>a&1)
                    coefficient_rows+=1
            for A in range(1,1<<p):
                s=A.bit_count()
                if s>m:
                    continue
                a=(A&-A).bit_length()-1
                q=tuple((m-s+1 if j==a else 1 if A>>j&1 else 0)
                        for j in range(p))
                row=[payoff(q,a,b) for b in range(1,1<<p)]
                coeff=mobius([Q(0)]+row,p)
                assert coeff[A]==Q((-1)**(s-1),s*comb(m,s))
                rows.append(row)
            expected=sum(comb(p,s) for s in range(1,min(m,p)+1))
            actual=rank(rows)
            assert actual==expected
            rank_cases.append({'players':m,'topics':p,'rank':actual})
    parity=[]
    for m in range(1,5):
        p=m+1
        even={b:1 for b in range(1,1<<p) if b.bit_count()%2==0}
        odd={b:1 for b in range(1,1<<p) if b.bit_count()%2==1}
        assert moments(even,p,m)==moments(odd,p,m)
        checked=0
        for h in product(range(p),repeat=m):
            q=tuple(h.count(a) for a in range(p))
            assert welfare(even,q)==welfare(odd,q)
            for a in h:
                assert utility(even,q,a)==utility(odd,q,a)
                checked+=1
        all_topics=(1,)*p
        assert abs(welfare(even,all_topics)-welfare(odd,all_topics))==1
        parity.append({'players':m,'topics':p,'ordered_player_payoffs':checked,
                       'even_customers':len(even),'odd_customers':len(odd)})
    compressed=[]
    for p,m,seed in [(4,1,123),(5,2,124),(6,2,125),(5,3,126)]:
        rng=Random(seed)
        w={b:rng.randrange(1,10) for b in range(1,1<<p)}
        c,steps=compress(w,p,m)
        assert moments(w,p,m)==moments(c,p,m)
        checked=0
        z=moments(w,p,m)
        for q in counts(m,p):
            assert welfare(w,q)==welfare(c,q)
            for a in range(p):
                if q[a]:
                    assert utility(w,q,a)==utility(c,q,a)
                    h=tuple(j for j,n in enumerate(q) for _ in range(n))
                    i=h.index(a)
                    others=tuple(j for j in range(m) if j!=i)
                    expanded=Q(0)
                    for J in range(1<<(m-1)):
                        mask=1<<a
                        for j,position in enumerate(others):
                            if J>>j&1:
                                mask|=1<<h[position]
                        expanded+=Q((-1)**J.bit_count(),J.bit_count()+1)*z[mask]
                    assert utility(w,q,a)==expanded
                    checked+=1
        if m>=2:
            for a in range(p):
                for b in range(p):
                    original=sum(v for t,v in w.items() if bool(t>>a&1)!=bool(t>>b&1))
                    current=sum(v for t,v in c.items() if bool(t>>a&1)!=bool(t>>b&1))
                    assert original==current
        compressed.append({'players':m,'topics':p,'seed':seed,'before':len(w),
                           'after':len(c),'elimination_steps':steps,
                           'terminal_action_checks':checked})
    # Coordinatewise monotonicity is not a characterization of the moment cone.
    singles={0:Q(1),1:Q(1),2:Q(1)}
    pairs={(0,1):Q(9,10),(1,2):Q(9,10),(0,2):Q(1,10)}
    assert all(0<=v<=min(singles[a],singles[b]) for (a,b),v in pairs.items())
    violation=pairs[0,1]+pairs[1,2]-pairs[0,2]-singles[1]
    assert violation==Q(7,10)
    for x in product((0,1),repeat=3):
        assert x[0]*x[1]+x[1]*x[2]-x[0]*x[2]<=x[1]
    # Degree-two nonnegative polynomial requiring three-label positivity.
    values=[]
    for x in product((0,1),repeat=3):
        value=x[1]-x[0]*x[1]-x[1]*x[2]+x[0]*x[2]
        assert value>=0
        values.append((x,value))
    positive={x for x,v in values if v}
    assert positive=={(0,1,0),(1,0,1)}
    for fixed in range(1<<3):
        if fixed.bit_count()>2:
            continue
        for assignment in range(1<<3):
            support={x for x in product((0,1),repeat=3)
                     if all(x[j]==bool(assignment>>j&1) for j in range(3) if fixed>>j&1)}
            if (1,0,1) in support:
                assert not (support-{(0,0,0)})<=positive
    return {'status':'passed','scope':'exact finite audits, not a half-coverage proof',
            'payoff_rows_mobius_checked':coefficient_rows,'rank_cases':rank_cases,
            'parity_games':parity,'compression_cases':compressed,
            'infeasible_moment_excess':str(violation),
            'nonnegative_quadratic_positive_assignments':sorted(positive)}

if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
