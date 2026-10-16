#!/usr/bin/env python3
"""独立均匀随机单机重置矩的精确阈值审计（scratch）。

The original balanced assignment is sampled uniformly. Retained tasks formerly
on the deleted machine are each rerouted uniformly and INDEPENDENTLY among the
K remaining machines. The output is a deterministic rational moment matrix,
not one random schedule and not a makespan approximation algorithm.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
from pathlib import Path
import hashlib
import json
import platform


def pair_probabilities(q):
    """Independent posterior derivation, then check simplified formulas."""
    assert q >= 2
    m, n, k = 2*q, 2*q*q, 2*q-1
    # Given new a=t, old a=t has posterior K/m, old a=i posterior 1/m.
    def other_job_probability(same_machine):
        ordinary_old_a = F(q-int(same_machine),n-1) + F(q,k*(n-1))
        deleted_old_a = F(q,n-1) + F(q-1,k*(n-1))
        return F(k,m)*ordinary_old_a + F(1,m)*deleted_old_a
    alpha = other_job_probability(True)
    beta = other_job_probability(False)
    assert alpha == F(1,k)-F(k-1,m*(n-1))
    assert beta == F(1,k)+F(1,m*(n-1))
    assert alpha+(k-1)*beta == 1
    return alpha,beta


def capacity_quantities(q,c):
    m,n,k=2*q,2*q*q,2*q-1
    r=n-c
    assert 0<=c<=n
    alpha,beta=pair_probabilities(q)
    base=F(r,k)
    if r==0:
        return base,None,None,None
    true_same=1+(r-1)*alpha
    true_other=(r-1)*beta
    false_same=true_other
    false_other=F(r-true_other,k-1)
    # Reconstruct complement conditions by total expectation independently.
    assert false_same==F(r-true_same,k-1)
    assert false_other==F(r-true_other,k-1)
    assert true_other<base
    assert 0<base-true_other<=F(1,k)
    assert false_other==base+F(base-true_other,k-1)
    return base,true_same,true_other,false_other


def formula_audit(q):
    n,k=2*q*q,2*q-1
    passing=[]
    for c in range(n+1):
        values=capacity_quantities(q,c)
        valid=all(v is None or v<=q for v in values)
        if valid:
            passing.append(c)
        if c<=q+1:
            assert values[1]>q
        if c>=q+2:
            assert valid
    assert min(passing)==q+2
    below=capacity_quantities(q,q+1)
    at=capacity_quantities(q,q+2)
    assert below[1]-q == F(q*(q-2)*(2*q+1)+2,q*k*(n-1))>0
    assert at[1]-q == -F(q*q+4*q-3,q*k*(n-1))<0
    return dict(q=q,first_passing_c=min(passing),c_values_checked=n+1,
                alpha=str(pair_probabilities(q)[0]),beta=str(pair_probabilities(q)[1]),
                below_true_same_excess=str(below[1]-q),
                endpoint_capacity_quantities=list(map(str,at)))


def balanced_assignments(q):
    m,n=2*q,2*q*q
    state=[-1]*n
    def rec(machine,remaining):
        if machine==m-1:
            for j in remaining:state[j]=machine
            yield tuple(state)
            return
        for block in combinations(remaining,q):
            chosen=set(block)
            for j in block:state[j]=machine
            yield from rec(machine+1,tuple(j for j in remaining if j not in chosen))
    yield from rec(0,tuple(range(n)))


def direct_moment_audit(q,c):
    """Enumerate actual old worlds AND every independent random branch."""
    m,n,k=2*q,2*q*q,2*q-1
    deleted=m-1
    residual=tuple(range(c,n))
    r=len(residual)
    old_worlds=factorial(n)//factorial(q)**m
    denominator=old_worlds*(k**q)
    variable_count=r*k
    x=[0]*variable_count
    y=[[0]*variable_count for _ in range(variable_count)]
    branch_count=0
    weight_sum=0
    world_count=0
    for old in balanced_assignments(q):
        world_count+=1
        redraw=[z for z,j in enumerate(residual) if old[j]==deleted]
        for destinations in product(range(k),repeat=len(redraw)):
            final=[old[j] for j in residual]
            for z,dest in zip(redraw,destinations):final[z]=dest
            weight=k**(q-len(redraw))
            weight_sum+=weight
            branch_count+=1
            selected=[z*k+dest for z,dest in enumerate(final)]
            for a in selected:
                x[a]+=weight
                for b in selected:y[a][b]+=weight
    assert world_count==old_worlds and weight_sum==denominator
    if q==1:
        assert k==1
        assert all(v==denominator for v in x)
        assert all(v==denominator for row in y for v in row)
        return dict(q=q,c=c,old_worlds=old_worlds,random_branches=branch_count,
                    all_capacity_pass=(r<=1),zero_probability_false_literals=True)
    alpha,beta=pair_probabilities(q)
    for a in range(r):
        for machine in range(k):
            v=a*k+machine
            assert F(x[v],denominator)==F(1,k)
            for b in range(r):
                for dest in range(k):
                    w=b*k+dest
                    expected=(F(int(machine==dest),k) if a==b else
                              (alpha if machine==dest else beta)/k)
                    assert F(y[v][w],denominator)==expected
    true_values=[]
    false_values=[]
    for a in range(r):
        for literal_machine in range(k):
            v=a*k+literal_machine
            assert 0<x[v]<denominator
            for machine in range(k):
                moment_sum=sum(y[b*k+machine][v] for b in range(r))
                marginal_sum=sum(x[b*k+machine] for b in range(r))
                yes=F(moment_sum,x[v])
                no=F(marginal_sum-moment_sum,denominator-x[v])
                base,same,other,false_other=capacity_quantities(q,c)
                assert F(marginal_sum,denominator)==base
                assert yes==(same if machine==literal_machine else other)
                assert no==(other if machine==literal_machine else false_other)
                true_values.append(yes);false_values.append(no)
    values=capacity_quantities(q,c)
    valid=all(v is None or v<=q for v in values)
    assert valid==all(v<=q for v in true_values+false_values)
    return dict(q=q,c=c,old_worlds=old_worlds,random_branches=branch_count,
                unit_denominator=denominator,
                variables=variable_count,joint_entries=variable_count**2,
                literal_machine_checks=len(true_values)+len(false_values),
                max_true=str(max(true_values)) if true_values else None,
                max_false=str(max(false_values)) if false_values else None,
                all_capacity_pass=valid)


def main():
    formulas=[formula_audit(q) for q in range(2,65)]
    direct=[direct_moment_audit(1,c) for c in range(3)]
    direct += [direct_moment_audit(2,c) for c in range(9)]
    source=Path(__file__)
    return dict(scope="fixed balanced old distribution; old nondeleted choices unchanged; independent uniform redraws",
                statement="q>=2: sharp minimum c is q+2; q=1: minimum c is 1",
                python=platform.python_version(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                formulas=formulas,direct_moment_audits=direct,
                limitations=["deterministic exact moment output from a random transfer kernel",
                             "not an actual makespan approximation algorithm",
                             "does not exclude reselecting or recoupling residual moments"])


if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
