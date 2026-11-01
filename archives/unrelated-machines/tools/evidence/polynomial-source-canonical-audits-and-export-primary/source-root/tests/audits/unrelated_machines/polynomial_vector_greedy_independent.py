#!/usr/bin/env python3
"""三次多项式真实最优源的压缩乘法向量贪心：独立精确审计。

Reconstruct actual schedules for every (a,b,c) in F_q^3. For q=3,5,7 form
integer-scaled centered feature Gram and every degree-three compressed matrix
numerator from those schedules, compare every coincident/distinct-job case,
then run the stated greedy vector rule using Fraction arithmetic. For q=13
verify all 1/2/3-wise raw and merged counts and every source capacity, then check
the scores via the independently derived block identity. No abstract independent
variables are substituted for the actual source distribution.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from hashlib import sha256
import json
import platform
from math import isqrt
import numpy as np


def primality(q):
    return q>=2 and all(q%d for d in range(2,isqrt(q)+1))


def source(q):
    assert primality(q)
    coeff=np.array(list(product(range(q),repeat=3)),dtype=np.int64)
    t=np.arange(q,dtype=np.int64)
    raw=(t[None,:]**3+coeff[:,0,None]*t[None,:]**2+
         coeff[:,1,None]*t[None,:]+coeff[:,2,None])%q
    merged=np.where(raw<=1,0,raw-1)
    # Every ordinary job has unit time on every ordinary machine; a separate
    # private anchor has processing time6 and is fixed in every actual schedule.
    loads=np.column_stack([(merged==k).sum(axis=1) for k in range(q-1)])
    assert int(loads.max())<=6
    assert all(np.max((raw==y).sum(axis=1))<=3 for y in range(q))
    assert np.all(loads.sum(axis=1)==q)
    full_schedules=np.column_stack((merged,np.full(q**3,q-1,dtype=np.int64)))
    assert np.all(full_schedules[:,-1]==q-1)
    full_loads=np.column_stack((loads,np.full(q**3,6,dtype=np.int64)))
    assert np.all(full_loads.max(axis=1)==6)
    return raw,merged,loads


def check_wise(raw,merged,q):
    counts=[]
    weights=np.array([2]+[1]*(q-2),dtype=np.int64)
    for degree in (1,2,3):
        tests=0
        for jobs in combinations(range(q),degree):
            code=sum(raw[:,job]*q**p for p,job in enumerate(jobs))
            actual=np.bincount(code,minlength=q**degree)
            assert np.all(actual==q**(3-degree))
            code2=sum(merged[:,job]*(q-1)**p for p,job in enumerate(jobs))
            actual2=np.bincount(code2,minlength=(q-1)**degree)
            expected=np.array([q**(3-degree)*np.prod([weights[(z//((q-1)**p))%(q-1)] for p in range(degree)])
                               for z in range((q-1)**degree)],dtype=np.int64)
            assert np.array_equal(actual2,expected)
            tests+=1
        counts.append(dict(degree=degree,job_subsets=tests,raw_count_each=q**(3-degree),
                           merged_product_counts_exact=True))
    return counts


def expected_gram(q):
    labels=[None]+[(t,k) for t in range(q) for k in range(q-2)]
    w=[2]+[1]*(q-2)
    d=len(labels)
    G=np.zeros((d,d),dtype=np.int64);G[0,0]=1
    for a,(t,k) in enumerate(labels[1:],1):
        for b,(u,l) in enumerate(labels[1:],1):
            if t==u:G[a,b]=q*w[k]*int(k==l)-w[k]*w[l]
    return labels,w,G


def expected_H_numerator(q,j,e,labels,w):
    n=q**3;scale=n//q;d=len(labels);H=np.zeros((d,d),dtype=np.int64)
    for a,la in enumerate(labels):
        for b,lb in enumerate(labels):
            if la is None and lb is None:v=scale*w[e]
            elif la is None or lb is None:
                t,k=lb if la is None else la
                v=scale*w[e]*(q*int(e==k)-w[k]) if t==j else 0
            else:
                t,k=la;u,l=lb
                if t!=u:v=0
                elif t==j:v=scale*w[e]*(q*int(e==k)-w[k])*(q*int(e==l)-w[l])
                else:v=scale*w[e]*(q*w[k]*int(k==l)-w[k]*w[l])
            H[a,b]=v
    return H


def solve_gram(q,vec):
    # Every retained centered block has omitted-machine weight1.
    out=[vec[0]]
    for t in range(q):
        block=vec[1+t*(q-2):1+(t+1)*(q-2)]
        total=sum(block,F(0))
        out.extend(v/F(q*(2 if k==0 else 1))+total/F(q) for k,v in enumerate(block))
    return out


def norm(vec,G):
    return sum(vec[a]*vec[b]*int(G[a,b]) for a in range(len(vec)) for b in range(len(vec)))


def exact_operators_and_greedy(q,merged,order):
    n=q**3
    labels,w,G=expected_gram(q);d=len(labels)
    B=np.column_stack([np.ones(n,dtype=np.int64)]+
                      [q*(merged[:,t]==k).astype(np.int64)-w[k] for t,k in labels[1:]])
    Gnum=B.T@B
    assert np.array_equal(Gnum,n*G)
    # Check the block inverse against every actual Gram basis column.
    for b in range(d):
        recovered=solve_gram(q,[F(int(G[a,b])) for a in range(d)])
        assert recovered==[F(int(a==b)) for a in range(d)]
    H={}
    for j in range(q):
        for e in range(q-1):
            actual=B.T@((merged[:,j]==e)[:,None]*B)
            expected=expected_H_numerator(q,j,e,labels,w)
            assert np.array_equal(actual,expected)
            H[j,e]=actual
    psi=[F(1)]+[F(0)]*(d-1);processed=[];trace=[];p=F(2,q)
    anchor_checks=0
    for r,j in enumerate(order):
        # The sole available anchor literal is exactly1 in every actual world,
        # hence its real H numerator is the already computed Gram numerator.
        anchor_next=solve_gram(q,[sum(F(int(Gnum[a,b]),n)*psi[b] for b in range(d)) for a in range(d)])
        assert anchor_next==psi and norm(psi,G)>0
        anchor_checks+=1
        scores=[];vectors=[]
        for e in range(q-1):
            hv=[sum(F(int(H[j,e][a,b]),n)*psi[b] for b in range(d)) for a in range(d)]
            nxt=solve_gram(q,hv);score=norm(nxt,G)
            pe=F(w[e],q)
            variance=F(0) if r==0 else r*p**(2*r-2)*p*(1-p)
            predicted=p**(2*r)*pe+variance*pe*pe
            assert score==predicted
            scores.append(score);vectors.append(nxt)
        choice=max(range(q-1),key=lambda e:(scores[e],-e))
        assert choice==0 and all(scores[0]>s for s in scores[1:])
        psi=vectors[choice];processed.append(j)
        expected=[p**(r+1)]+[p**r/F(q) if k==0 and t in processed else F(0) for t,k in labels[1:]]
        assert psi==expected
        trace.append(dict(job=j,scores=list(map(str,scores)),chosen=choice,
                          strict_gap=str(scores[0]-scores[1])))
    assert norm(psi,G)>0
    anchor_next=solve_gram(q,[sum(F(int(Gnum[a,b]),n)*psi[b] for b in range(d)) for a in range(d)])
    assert anchor_next==psi
    anchor_checks+=1
    return dict(order=order,dimension=d,gram=[[int(v)for v in row]for row in G],
                gram_sha256=sha256(Gnum.tobytes()).hexdigest(),
                degree_three_matrices_checked=len(H),
                actual_H_sha256={f'{j},{e}':sha256(a.tobytes()).hexdigest() for (j,e),a in H.items()},
                trace=trace,all_ordinary_choices=0,
                final_vector_nonzero=True,anchor_identity_positions_checked=anchor_checks)


def audit(q,full):
    raw,merged,loads=source(q)
    wise=check_wise(raw,merged,q)
    report=dict(q=q,source_states=q**3,ordinary_jobs=q,ordinary_machines=q-1,
                anchor_processing=6,anchor_private_machine=True,exact_OPT=6,
                max_source_ordinary_load=int(loads.max()),
                all_source_makespans=6,three_wise=wise,
                source_raw_sha256=sha256(raw.tobytes()).hexdigest(),
                source_merged_sha256=sha256(merged.tobytes()).hexdigest())
    if full:
        report['full_actual_gram_audits']=[exact_operators_and_greedy(q,merged,list(range(q))),
                                            exact_operators_and_greedy(q,merged,list(reversed(range(q))))]
    else:
        p=F(2,q)
        gaps=[]
        for r in range(q):
            variance=F(0) if r==0 else r*p**(2*r-2)*p*(1-p)
            main=p**(2*r)*p+variance*p*p
            other=p**(2*r)*F(1,q)+variance*F(1,q*q)
            assert main>other
            gaps.append(str(main-other))
        report['score_mode']='derived from actual checked three-wise distribution; no full Gram formed'
        report['strict_gaps']=gaps
    report['algorithm_makespan']=max(q,6)
    report['exact_ratio']=str(F(max(q,6),6))
    return report


def main():
    records=[audit(q,q in(3,5,7)) for q in(3,5,7,13)]
    path=Path(__file__)
    return dict(scope='specified compressed-multiplication vector greedy given explicit true optimal source',
                python=platform.python_version(),numpy=np.__version__,
                source_sha256=sha256(path.read_bytes()).hexdigest(),parameters=[3,5,7,13],runs=records,
                interpretation='q>=7: exact ratio q/6; prime family is unbounded',
                limitations=['no general approximation algorithm with source D is being claimed computable from P',
                             'q13 checked actual source and all 3-wise counts; full Gram only q3/5/7',
                             'arbitrary order conclusion uses the separate block proof, not finite order enumeration'])


if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
