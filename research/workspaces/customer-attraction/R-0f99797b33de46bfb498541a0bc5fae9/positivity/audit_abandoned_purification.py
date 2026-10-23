"""Reproduce saved confluence/purification failures; no search."""
import json
from functools import lru_cache
from pathlib import Path
import argparse
from anonymous_extremal_probe import (
    Instance, CustomerType, ExactSPESolver, anonymous_outcomes, counts_layer, incr)
from customer_attraction.certificate import verify_certificate


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output')
    args=ap.parse_args()
    p=m=4
    w=[2,0,1,0,0,2,2,1,1,0,1,1,0,1,2]
    def instance(weights):
        return Instance(tuple('ABCD'),tuple(CustomerType(
            frozenset(a for a in range(p) if mask&(1<<a)),v)
            for mask,v in enumerate(weights,1) if v),m)
    g=instance(w)
    solver=ExactSPESolver(g)
    expected={(1,2,0,1),(2,0,1,1),(2,1,0,1),(2,1,1,0)}
    assert solver.outcomes()==expected
    q=(2,1,1,0)
    assert solver.worst_outcomes()==frozenset([q])
    cert=solver.certificate(q)
    check=verify_certificate(g,cert)
    check.assert_valid()
    wp=[x*100000 for x in w]
    for a,n in enumerate(q):wp[(1<<a)-1]+=n
    changed=ExactSPESolver(instance(wp))
    assert changed.outcomes()==frozenset([(2,1,0,1)])
    assert min(map(g.welfare,changed.outcomes()))==14>g.welfare(q)==13
    tables=[(3,3,2,0),(2,2,1,1),(1,1,0,0),(2,1,1,0),
        (2,2,1,0),(3,3,3,1),(3,1,0,0),(3,3,1,0),
        (3,2,2,0),(2,1,0,0),(3,2,0,0),(2,1,0,0),
        (3,3,3,0),(3,0,0,0),(2,2,1,0)]
    payoffs={z:tuple(sum(tables[mask-1][sum(z[b] for b in range(p)
            if mask&(1<<b))-1] for mask in range(1,1<<p)
            if mask&(1<<a)) if z[a] else 0 for a in range(p))
        for z in counts_layer(p,m)}
    class Congestion:
        topic_count=p
        players=m
        def topic_payoffs(self,z):return payoffs[z]
    @lru_cache(None)
    def full(z):
        if sum(z)==m:return frozenset([z])
        children=[full(incr(z,a)) for a in range(p)]
        threshold=max(min(payoffs[t][a] for t in c)
            for a,c in enumerate(children))
        return frozenset(t for a,c in enumerate(children)
            for t in c if payoffs[t][a]>=threshold)
    general=full((0,)*p)
    anonymous,_,count=anonymous_outcomes(Congestion(),10000)
    assert general==frozenset([(0,1,2,1),(1,1,1,1),(1,1,2,0)])
    assert anonymous==frozenset([(1,1,1,1),(1,1,2,0)])
    report=dict(status='passed',cag_original_outcomes=sorted(expected),
        cag_target=q,cag_original_welfare=13,
        cag_changed_outcomes=sorted(changed.outcomes()),
        cag_changed_original_welfare=14,
        complete_histories_checked=check.checked_histories,
        complete_deviations_checked=check.checked_deviations,
        general_congestion_full_outcomes=sorted(general),
        general_congestion_anonymous_outcomes=sorted(anonymous),
        general_congestion_anonymous_policies=count,
        scope='Specific purification direction fails; not a CAG count-reduction or half counterexample')
    payload=json.dumps(report,indent=2)
    if args.output:Path(args.output).write_text(payload+'\n')
    print(payload)


if __name__=='__main__':main()
