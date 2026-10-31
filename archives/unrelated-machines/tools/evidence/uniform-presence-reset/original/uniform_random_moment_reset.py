#!/usr/bin/env python3
"""独立均匀后备选择的二阶矩运输：精确公式与实际矩审计。

Deterministically outputs rational moments, not a randomized approximation.
Reads no external data; explicit q defines m=2q,n=2q^2,p=1/q.
All output goes to stdout; frozen files are not overwritten.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform


def source_pair(q, e, f):
    i, a = e
    k, b = f
    m, n = 2*q, 2*q*q
    if a == b:
        return F(i == k, m)
    return F(q-(i == k), m*(n-1))


def conditional_rows(q, c):
    n, K = 2*q*q, 2*q-1
    r = n-c
    beta = F(1,K)-F(q-1,q*(n-1))
    gamma = F(1,K)+F(1,2*q*(n-1))
    same = 1+(r-1)*beta
    other = (r-1)*gamma
    false_same = other
    false_other = (same+(K-2)*other)/(K-1)
    return F(r,K), same, other, false_same, false_other


def actual_matrix(q,c):
    m,n,K=2*q,2*q*q,2*q-1
    jobs=list(range(c,n))
    edges=[(k,a) for k in range(1,m) for a in jobs]
    x={e:F(1,K) for e in edges}
    # Stochastic transition on each old deleted-machine choice: weight1/K.
    # Different jobs use independent coins. Same-job entries require the
    # categorical diagonal correction and cannot be given by R Y R^T alone.
    pre={e:[(e,F(1)),((0,e[1]),F(1,K))] for e in edges}
    y={}
    for e in edges:
        for f in edges:
            if e[1]==f[1]:
                value=x[e] if e==f else F()
            else:
                value=sum((we*wf*source_pair(q,oe,of)
                           for oe,we in pre[e] for of,wf in pre[f]),F())
            y[e,f]=value
    mu,same,other,fs,fo=conditional_rows(q,c)
    violations=0
    for e in edges:
        assert y[e,e]==x[e]
        assert all(y[e,f]==y[f,e] and 0<=y[e,f]<=x[e] for f in edges)
        for a in jobs:
            assert sum(y[(k,a),e] for k in range(1,m))==x[e]
        for k in range(1,m):
            mean=sum(x[k,a] for a in jobs)
            plus=sum(y[(k,a),e] for a in jobs)/x[e]
            minus=(mean-x[e]*plus)/(1-x[e])
            assert mean==mu
            assert plus==(same if k==e[0] else other)
            assert minus==(fs if k==e[0] else fo)
            violations+=int(plus>q)+int(minus>q)
    assert bool(violations)==(c<q+2)
    return dict(q=q,c=c,literal_count=len(edges),joint_entries=len(y),
                true_false_rows=2*len(edges)*K,violations=violations,
                mean=str(mu),true_same=str(same),true_other=str(other),
                false_same=str(fs),false_other=str(fo))


def main():
    count=0
    for q in range(2,129):
        n,K=2*q*q,2*q-1
        D=q*K*(n-1)
        for c in range(q+3):
            vals=conditional_rows(q,c)
            assert vals[1]>vals[2]
            assert max(vals)<=q if c==q+2 else max(vals)>q
            count+=1
        same1=conditional_rows(q,q+1)[1]
        same2=conditional_rows(q,q+2)[1]
        assert same1-q==F((q-2)*q*(2*q+1)+2,D)>0
        assert q-same2==F(q*q+4*q-3,D)>0
    matrices=[actual_matrix(q,c) for q in range(2,5) for c in [q+1,q+2]]
    return dict(title='逐任务独立均匀后备的条件矩尖锐门槛',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                python=platform.python_version(),arithmetic='fractions.Fraction; deterministic; no seed',
                scalar_q_range=[2,128],scalar_parameter_cases=count,
                explicit_matrices=matrices,
                claim='q>=2 minimal absorbed job count q+2 for this stochastic transition matrix',
                limitations=['uniform source family only','matrix output is deterministic; individual transported schedules may have load2T','not the fixed deterministic RYR^T contract; includes categorical diagonal correction','no general approximation guarantee'])


if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
