"""Test only the exact general auxiliary FLOW matching inequality.

For a realizable on-path terminal, off-path children minimize the deviator's
payoff independently.  This is a full-history SPE by the canonical oracle.
The candidate is max_matching D >= OPT - W for each optimal m-slot tuple.
Finite output has no force as a general theorem.
"""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def inc(c,a):
    return c[:a]+(c[a]+1,)+c[a+1:]


def check(instance, max_paths=300):
    solver=ExactSPESolver(instance)
    optimum=instance.optimal_welfare()
    k=instance.topic_count
    optima=[]
    for s in range(1,min(instance.players,k)+1):
        for support in combinations(range(k),s):
            counts=tuple(int(a in support) for a in range(k))
            if instance.welfare(counts)==optimum:
                # All fillings of unused slots are not needed for a witness.
                optima.append(support+(support[0],)*(instance.players-s))
    tested=0
    for target in sorted(solver.outcomes(),key=instance.welfare):
        welfare=instance.welfare(target)
        if welfare==optimum:
            continue
        actual=instance.topic_payoffs(target)
        for path in solver.ordered_outcomes(target):
            d=[]
            c=(0,)*k
            for action in path:
                row=[]
                for a in range(k):
                    if a==action:
                        row.append(actual[a])
                    else:
                        row.append(min(solver._utility(t,a) for t in solver.outcomes(inc(c,a))))
                d.append(row)
                c=inc(c,action)
            for topics in optima:
                matching=max(sum(d[i][a] for i,a in enumerate(order)) for order in set(permutations(topics)))
                if matching<optimum-welfare:
                    certificate=solver.certificate(on_path=path)
                    return {"instance":instance.to_dict(),"path":path,"optimum":optimum,"welfare":welfare,
                            "topics":topics,"matching":str(matching),"D":[list(map(str,row)) for row in d],
                            "actions":[{"history":list(h),"action":a} for h,a in certificate.actions.items()]}
            tested+=1
            if tested>=max_paths:
                return None
    return None


def main():
    rng=random.Random(20261024)
    for trial in range(120):
        m=3+trial%3
        k=4+trial%2
        customers=[]
        for mask in range(1,1<<k):
            if rng.random()<.6:
                customers.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randint(1,15)))
        instance=Instance(tuple(f'T{a}' for a in range(k)),tuple(customers),m)
        result=check(instance)
        if result:
            output=Path(__file__).with_name('flow_matching_counterexample.json')
            output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            print('FAIL',trial,output)
            return
        if trial%10==0:
            print('checked',trial,flush=True)
    print('No failure in 120 exact candidate checks; this is not a theorem.')


if __name__=='__main__':
    main()
