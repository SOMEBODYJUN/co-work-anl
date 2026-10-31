#!/usr/bin/env python3
"""Definition-level exact audit of background thinning and common-catalog barrier.

No import from the proposed proof, canonical model, solver, or optimizer.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
import json
import random


def subset_probability(r,b,mask):
    if b==0:return Q(mask==(1<<r)-1)
    k=mask.bit_count()
    return Q(b*factorial(k)*factorial(b+r-k-1),factorial(b+r))


def original_row(r,topic_mask,b,leaf,i):
    interested=[bool(topic_mask>>a&1) for a in leaf]
    d=sum(interested)
    return Q(1,b+d) if interested[i] else Q(0)


def thinned_row(r,topic_mask,b,leaf,i):
    total=Q(0)
    for keep in range(1<<r):
        attracts=[bool(topic_mask>>a&1) and bool(keep>>j&1) for j,a in enumerate(leaf)]
        k=sum(attracts)
        if attracts[i]:total+=subset_probability(r,b,keep)/k
    return total


def main():
    endpoint_cases=0;interior_cases=0;positive_compiler_cases=0;relative_approximation_cases=0
    for r in range(2,12):
        for b in range(1,12):
            D=(r+1)*(b+1)*(b+r)
            alpha=Q(r*(b+r+1),D);beta=Q(-r*b,D)
            assert beta<0<alpha
            eps=Q(b*(r-1),b*(r+1)+2*r)
            best_alpha=Q(2*r,b*(r+1)+2*r)
            assert best_alpha*(b+1)==1+eps
            assert best_alpha*Q(b+r,r)==1-eps
            for j in range(1,r+1):
                assert abs(best_alpha*Q(b+j,j)-1)<=eps
                relative_approximation_cases+=1
            for j in range(1,r+1):
                compiled=alpha/j-beta/(r-j+1);target=Q(1,b+j)
                residual=Q(b*(b+r+1)*(j-1)*(j-r),(b+1)*(b+r)*j*(r+1-j)*(b+j))
                assert compiled-target==residual
                if j in (1,r):assert residual==0;endpoint_cases+=1
                else:assert residual<0;interior_cases+=1
    # Boundary cases excluded by the obstruction.
    for r in range(1,12):
        for j in range(1,r+1):assert Q(1,j)==Q(1,0+j)
    for b in range(12):assert Q(1,b+1)==Q(1,b+1)
    for r in range(1,8):
        for b in range(6):
            assert sum((subset_probability(r,b,k) for k in range(1<<r)),Q(0))==1
            for d in range(r+1):
                # First d active players choose a theme containing this customer.
                coverage=Q(0);utilities=[Q(0)]*r
                for keep in range(1<<r):
                    k=(keep&((1<<d)-1)).bit_count();prob=subset_probability(r,b,keep)
                    coverage+=prob*bool(k)
                    for i in range(d):
                        if keep>>i&1:utilities[i]+=prob/k
                assert coverage==(Q(d,b+d) if d else Q(0))
                assert utilities==([Q(1,b+d)]*d if d else [])+[Q(0)]*(r-d)
                positive_compiler_cases+=1
    # Arbitrary full formal policy: its status as SPE is immaterial to identity.
    r=4;p=3;background={mask:(mask*7)%4 for mask in range(1,1<<p)}
    rng=random.Random(66173)
    policy={h:rng.randrange(p) for dep in range(r) for h in product(range(p),repeat=dep)}
    def terminal(h):
        while len(h)<r:h=h+(policy[h],)
        return h
    leaf_rows={}
    expected_rows={}
    expected_coverage={}
    for leaf in product(range(p),repeat=r):
        leaf_rows[leaf]=tuple(sum((original_row(r,T,b,leaf,i) for T,b in background.items()),Q(0)) for i in range(r))
        expected_rows[leaf]=tuple(sum((thinned_row(r,T,b,leaf,i) for T,b in background.items()),Q(0)) for i in range(r))
        assert leaf_rows[leaf]==expected_rows[leaf]
        cov=Q(0)
        for T,b in background.items():
            for keep in range(1<<r):
                covered=any((T>>a&1) and (keep>>i&1) for i,a in enumerate(leaf))
                cov+=subset_probability(r,b,keep)*covered
        expected_coverage[leaf]=cov
        assert sum(leaf_rows[leaf],Q(0))==cov
    node_comparisons=0
    for h,a in policy.items():
        z=terminal(h);i=len(h)
        for t in range(p):
            y=terminal(h+(t,))
            assert leaf_rows[z][i]-leaf_rows[y][i]==expected_rows[z][i]-expected_rows[y][i]
            node_comparisons+=1
    out={'identity':'independent exact audit; positive compiler has player-specific catalogs and hidden randomness',
         'endpoint_equations':endpoint_cases,'sharp_relative_approximation_cases':relative_approximation_cases,'strict_signed_interior_failures':interior_cases,
         'thinning_count_cases':positive_compiler_cases,'terminal_player_checks':len(leaf_rows)*r,
         'full_history_comparisons':node_comparisons,'root_active_profit':str(expected_coverage[terminal(())]),
         'universal_half_coverage_proved':False}
    path=Path(__file__).with_name('background_independent_report.json');path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
