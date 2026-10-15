#!/usr/bin/env python3
"""Exact rational checks of WC-R1-TWOATTACK-POLYNOMIAL-REDUCTION v1.

Finite checks are implementation evidence; proof.md proves the real-domain claim.
No numerical optimization or floating-point arithmetic is used.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


def ev(poly, x):
    return sum((c * x**j for j, c in enumerate(poly)), F(0))


def margins(n, w, p, q, alpha):
    return (
        ev(p, F(1)) + n*ev(q, 1+w)
        - alpha*(ev(p, 1+n*w) + n*ev(q, F(1))),
        ev(p, 1+w) + ev(q, w)
        - alpha*(ev(p, n*w) + ev(q, 1+w)),
    )


def reduce_certificate(n, w, p, q, alpha):
    d = max(len(p), len(q))-1
    assert d >= 2 and n >= 1 and w > 0 and alpha > 1
    assert all(c >= 0 for c in p+q)
    assert min(margins(n, w, p, q, alpha)) > 0
    input_margins = margins(n, w, p, q, alpha)
    if w > 1:
        assert n == 1
        p, q = ([c*w**j for j, c in enumerate(q)],
                [c*w**j for j, c in enumerate(p)])
        w = 1/w
        assert margins(n, w, p, q, alpha) == input_margins[::-1]
    a, r = 1+w, n*w
    A = a**d
    C = sum((c*(A-a**j)/(A-1) for j,c in enumerate(q)), F(0))
    D = sum((c*(a**j-1)/(A-1) for j,c in enumerate(q)), F(0))
    q_endpoint = [C] + [F(0)]*(d-1) + [D]
    assert C >= 0 and D > 0
    assert ev(q_endpoint, F(1)) == ev(q, F(1))
    assert ev(q_endpoint, a) == ev(q, a)
    assert ev(q_endpoint, w) >= ev(q, w)
    q_pure = [F(0)]*d + [D]
    assert min(margins(n, w, p, q_pure, alpha)) > 0
    norm = ev(p, F(1))
    assert norm > 0
    p = [c/norm for c in p]
    beta = D/norm
    q_pure = [F(0)]*d + [beta]
    assert min(margins(n, w, p, q_pure, alpha)) > 0
    rho = (w/a)**d
    assert A > alpha and alpha > rho
    fs = [n*(1-alpha/A)*(a**k-alpha*r**k)
          -(alpha-rho)*(alpha*(1+r)**k-1) for k in range(d+1)]
    assert fs[0] < 0
    assert sum((c*fs[k] for k,c in enumerate(p)), F(0)) > 0
    k = next(k for k in range(1,d+1) if fs[k] > 0)
    lower = (alpha*(1+r)**k-1)/(n*(1-alpha/A))
    upper = (a**k-alpha*r**k)/(alpha-rho)
    assert 0 < lower < upper < A
    beta_out = (lower+upper)/(2*A)
    p_out = [F(0)]*(d+1)
    p_out[k] = F(1)
    q_out = [F(0)]*d + [beta_out]
    assert 0 < w <= 1 and 0 < beta_out < 1
    out_margins = margins(n, w, p_out, q_out, alpha)
    assert min(out_margins) > 0
    return dict(d=d, n=n, w=str(w), k=k, beta=str(beta_out),
                alpha=str(alpha), input_margins=list(map(str,input_margins)),
                output_margins=list(map(str,out_margins)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    endpoint_checks = 0
    for d in range(2,17):
        for w in [F(1,50),F(1,10),F(1,3),F(2,3),F(1)]:
            a,A=1+w,(1+w)**d
            for j in range(d+1):
                C,D=(A-a**j)/(A-1),(a**j-1)/(A-1)
                assert C >= 0 and D >= 0
                assert C+D == 1 and C+D*A == a**j
                assert C+D*w**d >= w**j
                endpoint_checks += 1

    examples = []
    p=[F(0),F(1,100),F(99,100)]+[F(0)]*6
    q=[F(0)]*9
    q[4],q[8]=F(1,1000),F(11,25)
    examples.append(reduce_certificate(2,F(1,10),p,q,F(6,5)))
    # Reversed weights are a real obligation: the endpoint reduction alone
    # need not preserve feasibility before the player/resource exchange.
    examples.append(reduce_certificate(1,F(2),[F(0),F(0),F(9,40)],
                                       [F(0),F(1),F(0)],F(51,50)))

    feasible_count=0
    candidate_count=0
    for d in [2,4,8,12]:
        for n in [1,2,3,5]:
            for w in [F(1,2),F(1,5),F(1,10),F(1,20)]:
                for k in range(1,d+1):
                    for beta in [F(j,10) for j in range(1,10)]:
                        p=[F(0)]*(d+1)
                        q=[F(0)]*(d+1)
                        p[k],p[k-1]=F(99,100),F(1,100)
                        q[d],q[d-1]=F(99,100)*beta,F(1,100)*beta
                        for alpha in [F(11,10),F(6,5)]:
                            candidate_count += 1
                            if min(margins(n,w,p,q,alpha)) > 0:
                                reduce_certificate(n,w,p,q,alpha)
                                feasible_count += 1

    # Zero costs and equal weights are checked as original inequalities.
    boundaries=[]
    for name,n,w,p,q in [
        ('all_zero',1,F(1,5),[F(0)]*3,[F(0)]*3),
        ('main_zero',2,F(1,10),[F(0)]*3,[F(0),F(0),F(1)]),
        ('side_zero',2,F(1,10),[F(0),F(1),F(0)],[F(0)]*3),
        ('side_constant',2,F(1,10),[F(0),F(1),F(0)],[F(1),F(0),F(0)]),
        ('equal_weights',1,F(1),[F(0),F(1),F(0)],[F(0),F(0),F(1)]),
        ('large_light_weights',2,F(2),[F(0),F(0),F(1)],[F(0),F(1),F(0)]),
    ]:
        ms=margins(n,w,p,q,F(51,50))
        assert min(ms) <= 0
        boundaries.append(dict(name=name, margins=list(map(str,ms))))

    # Scope check requested by R1: the conservative test itself may lose
    # a game which the full-state analysis can still certify.
    p=[F(0),F(1),F(0)]
    q=[F(0),F(0),F(1,2)]
    H=(ev(p,1)+3*ev(q,F(6,5)))/(ev(p,F(8,5))+3*ev(q,1))
    L=(ev(p,F(6,5))+ev(q,F(1,5)))/(ev(p,F(3,5))+ev(q,F(6,5)))
    assert min(H,L)==F(61,66)<1
    result=dict(claim='WC-R1-TWOATTACK-POLYNOMIAL-REDUCTION v1',
                arithmetic='fractions.Fraction; no floating point',
                endpoint_checks=endpoint_checks,
                candidate_count=candidate_count,
                feasible_certificates_reduced=feasible_count,
                examples=examples,boundaries=boundaries,
                conservative_scope_example=dict(d=2,n=3,k=1,w='1/5',
                    beta='1/2',H=str(H),L=str(L)),
                result='PASS',
                limitation='Finite checks; the general proof is proof.md.')
    payload=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.write_text(payload)
    print(payload,end='')


if __name__=='__main__':
    main()
