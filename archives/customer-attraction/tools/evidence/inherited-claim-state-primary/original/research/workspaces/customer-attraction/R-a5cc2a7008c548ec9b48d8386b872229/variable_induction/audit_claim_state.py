"""Finite exact diagnostics for the variable-r inherited-claim state.

This is not a proof of Q-CAG-HALF.  It deliberately uses the canonical
set-valued solver to test a proposed compression of that solver.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def inc(b, a):
    return b[:a] + (b[a]+1,) + b[a+1:]


def inspect(instance):
    solver = ExactSPESolver(instance)
    k = instance.topic_count
    zeros = (0,)*k
    solver.outcomes()

    @lru_cache(None)
    def claims(b, ell):
        if sum(b) == instance.players:
            utility = instance.topic_payoffs(b)
            return frozenset({b}) if all(utility[a] >= ell[a] for a in range(k)) else frozenset()
        floor = solver.threshold(b)
        answer = set()
        for a in range(k):
            new_ell = ell[:a] + (max(ell[a], floor),) + ell[a+1:]
            answer.update(claims(inc(b,a), new_ell))
        return frozenset(answer)

    assert claims(zeros, zeros) == solver.outcomes()
    # More strongly compare every one-cut conditional state with filtering
    # the canonical unrestricted outcome set.
    states = 0
    for b in list(solver._outcomes):
        if sum(b) == instance.players:
            cuts = [F(0)]
        else:
            cuts = sorted({F(0), solver.threshold(b)})
        for a in range(k):
            if not b[a]:
                continue
            for cut in cuts:
                ell = tuple(cut if j == a else F(0) for j in range(k))
                filtered = frozenset(q for q in solver.outcomes(b)
                                     if instance.topic_payoff(a,q) >= cut)
                assert claims(b,ell) == filtered
                states += 1

    lowest = None
    witness = None
    for path in solver.ordered_outcomes():
        b=zeros
        ell=zeros
        for a in path:
            floor=solver.threshold(b)
            ell=ell[:a]+(max(ell[a],floor),)+ell[a+1:]
            b=inc(b,a)
        credit=sum((b[a]*ell[a] for a in range(k)),F(0))
        if lowest is None or credit < lowest:
            lowest=credit
            witness={'instance': instance.to_dict(), 'path':path,
                     'credit':str(credit), 'welfare':instance.welfare(b),
                     'optimum':instance.optimal_welfare(),
                     'cuts':list(map(str,ell))}
    return states, lowest, witness


def main():
    rng=random.Random(20261023)
    checked=0
    conditional=0
    failures=[]
    for m in range(2,5):
        for k in range(2,5):
            for repeat in range(70):
                customers=[]
                for mask in range(1,1<<k):
                    n=rng.randrange(4)
                    if n:
                        customers.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),n))
                I=Instance(tuple(f'T{a}' for a in range(k)),tuple(customers),m)
                states,credit,witness=inspect(I)
                conditional+=states
                checked+=1
                if 2*credit < I.optimal_welfare():
                    failures.append(witness)
                    # A concrete failure is sufficient to retire this shortcut.
                    report={'status':'FINITE_EXACT', 'instances':checked,
                            'conditional_states':conditional,
                            'threshold_credit_half_counterexample':witness}
                    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
                    print(json.dumps(report,indent=2))
                    return
    report={'status':'FINITE_EXACT','instances':checked,'conditional_states':conditional,
            'threshold_credit_half_counterexample':None}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
