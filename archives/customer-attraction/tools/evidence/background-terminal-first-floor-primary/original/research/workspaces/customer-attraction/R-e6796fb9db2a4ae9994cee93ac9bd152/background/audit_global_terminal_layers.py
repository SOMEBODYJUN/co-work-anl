"""Exact audit for global terminal-layer / global robust-row obstruction.
No repository model/solver import. Counts describe one explicitly Markov policy;
all ordered histories are covered because that policy and all share formulas
are invariant under order. This does not impose Markov behavior on arbitrary SPE.
"""
from fractions import Fraction
from functools import lru_cache
from math import factorial,lcm
from pathlib import Path
import json

def counts(q,total):
    if q==1:
        yield (total,)
    else:
        for a in range(total+1):
            for rest in counts(q-1,total-a):yield (a,)+rest

def check(k,m):
    n=m-k;L=k+1;q=m+1;sizes=(n,)+(L,)*m;scale=lcm(*range(1,m+1))
    def plus(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
    def payoff(c,a):return sizes[a]*scale//c[a]
    @lru_cache(None)
    def tail(c):
        if sum(c)==m:return c
        branches=[tail(plus(c,a)) for a in range(q)]
        # Positive Q labels have priority, E last; yields fresh Q on actual tail.
        a=max(range(q),key=lambda a:(payoff(branches[a],a),int(a>0),-a))
        return branches[a]
    def completion(c):
        if sum(c)<n:c=(c[0]+n-sum(c),)+c[1:]
        return tail(c)
    tailstates=tailrows=earlystates=earlyrows=0
    tailordered=earlyordered=0
    min_tail=None;min_robust=None
    for depth in range(m):
        for c in counts(q,depth):
            multiplicity=factorial(depth)
            for z in c:multiplicity//=factorial(z)
            final=completion(c)
            if depth>=n:
                tailstates+=1;tailrows+=q;tailordered+=multiplicity*q
                # Determine action from increase in ordered policy via same maximizer.
                branches=[tail(plus(c,a)) for a in range(q)]
                a=max(range(q),key=lambda a:(payoff(branches[a],a),int(a>0),-a))
                assert final==branches[a]
                own=payoff(final,a)
                assert own>=L*scale
                slack=min(own-payoff(branches[b],b) for b in range(q))
                assert slack>=0
                min_tail=slack if min_tail is None else min(min_tail,slack)
            else:
                earlystates+=1;earlyrows+=q;earlyordered+=multiplicity*q
                own=Fraction(sizes[0],final[0])
                assert own>=1
                r=m-depth
                for a in range(q):
                    slack=own-Fraction(sizes[a],c[a]+r)
                    assert slack>=0
                    min_robust=slack if min_robust is None else min(min_robust,slack)
    actual=completion((0,)*q)
    W=sum(s for s,c in zip(sizes,actual) if c)
    OPT=sum(sorted(sizes,reverse=True)[:m])
    assert W==m+k*k
    assert OPT==(k+2)*m-2*k-1
    assert OPT>2*W
    assert actual==(n,)+(1,)*k+(0,)*(m-k)
    # True early optimality is omitted: player n deviates to fresh Q and
    # the tail cannot repeat it; the payoff increases from 1 to L.
    dev=tail((n-1,1)+(0,)*(m-1))
    assert Fraction(L,dev[1])==L
    return {'k':k,'m':m,'unit_customers':sum(sizes),'actual_counts':actual,
      'W':W,'OPT_m':OPT,'OPT_minus_2W':OPT-2*W,
      'tail_count_states':tailstates,'tail_action_comparisons':tailrows,
      'tail_ordered_action_comparisons_represented':tailordered,
      'early_count_states':earlystates,'early_robust_comparisons':earlyrows,
      'early_ordered_robust_comparisons_represented':earlyordered,
      'min_tail_SPE_slack_scaled':min_tail,'payoff_scale':scale,
      'min_early_robust_slack':str(min_robust),
      'first_unverified_layer_actual_true_deviation_gain':L-1,
      'scope':'all global terminal k layers genuine SPE; global earlier robust rows; not complete root SPE'}

if __name__=='__main__':
    result={'status':'exact witness audit only; arbitrary k,m proof in companion markdown',
      'reports':[check(1,6),check(2,9)]}
    print(json.dumps(result,indent=2))
    Path(__file__).with_name('global_terminal_layers_audit.json').write_text(json.dumps(result,indent=2)+'\n')
