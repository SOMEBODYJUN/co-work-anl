"""Definition-level exact audit for replicated-block cycle payment.

No canonical solver, optimizer, or generated certificate is imported.  The
general claim is carried by the accompanying analytic proof, not this sweep.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def robust_row(r, sizes, bits, beta):
    total=F(0)
    ell=len(sizes)
    for i,L in enumerate(sizes):
        a,b=bits[i],bits[(i+1)%ell]
        if a and not b:
            total+=F(1,beta+r-L)
        elif b and not a:
            total-=F(1,beta+L)
    return total


def payoff(q, a, interest, beta):
    if a not in interest:
        return F(0)
    denominator=beta+sum(q[j] for j in interest)
    assert denominator>0
    return F(1,denominator)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output')
    args=ap.parse_args()
    profiles=0
    coefficient_checks=0
    admitted_profiles=0
    rejected_profiles=0
    internal_omission_checks=0
    for r in range(2,10):
        for ell in range(2,5):
            for sizes in product(range(1,r),repeat=ell):
                criterion=all(sizes[i]+sizes[j]>=r
                    for i in range(ell) for j in range(i))
                profiles+=1
                admitted_profiles+=criterion
                rejected_profiles+=not criterion
                for beta in (0,1,7):
                    minimum=min(robust_row(r,sizes,bits,beta)
                        for bits in product((0,1),repeat=ell))
                    coefficient_checks+=2**ell
                    assert (minimum>=0)==criterion,(r,sizes,beta,minimum)
                # Interior subtopic omissions can only increase each local
                # comparison, after the load-independent p/n lower bounds.
                if criterion and r<=6:
                    for bits in product((0,1),repeat=ell):
                        allowed=[range(bits[(i+1)%ell]+1) for i in range(ell)]
                        for subbits in product(*allowed):
                            bound=F(0)
                            for i,L in enumerate(sizes):
                                if bits[i] and not subbits[i]:bound+=F(1,r-L)
                                if subbits[i] and not bits[i]:bound-=F(1,L)
                            assert bound>=robust_row(r,sizes,bits,0)>=0
                            internal_omission_checks+=1
    menu_checks=0
    negative_flux_checks=0
    for N in range(2,16):
        r=N+1
        qs=[(1,N-1,1,0),(N-1,1,0,1),
            (1,0,1,N-1),(0,1,N-1,1)]
        for beta in (0,1,7):
            for mask in range(1,16):
                B={j for j in range(4) if mask&(1<<j)}
                pair=payoff(qs[0],0,B,beta)+payoff(qs[1],1,B,beta)
                pair-=payoff(qs[0],1,B,beta)+payoff(qs[1],0,B,beta)
                if N>=3:
                    assert pair>=0,(N,beta,B,pair)
                menu_checks+=1
            B={0,1}
            deltas=[]
            for i,q in enumerate(qs):
                root=payoff(q,i,B,beta)
                tail=sum((q[a]-(a==i))*payoff(q,a,B,beta)
                    for a in range(4) if q[a]-(a==i)>0)
                deltas.append(root-tail/N)
            actual=sum(deltas,F(0))/4
            expected=F(1,2*N)*(F(1,beta+N)-F(1,beta+1))
            assert actual==expected<0
            negative_flux_checks+=1
    report=dict(status='passed',profiles=profiles,
        admitted_profiles=admitted_profiles,rejected_profiles=rejected_profiles,
        coefficient_checks=coefficient_checks,
        internal_omission_checks=internal_omission_checks,
        four_maxima_pair_checks=menu_checks,
        uniform_negative_flux_checks=negative_flux_checks,
        scope='Exact audit of analytic block-cycle criterion; no general half theorem or SPE counterexample')
    payload=json.dumps(report,indent=2)
    if args.output:
        Path(args.output).write_text(payload+'\n')
    print(payload)


if __name__=='__main__':
    main()
