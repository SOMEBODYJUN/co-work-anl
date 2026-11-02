"""Exact C5 obstruction to propagating theta from successor floors alone."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

EDGES=tuple(frozenset([a,(a+1)%5]) for a in range(5))

def payoff(h,i):
    return sum((Fraction(1,sum(a in edge for a in h))
                for edge in EDGES if h[i] in edge),Fraction())

def immediate(h,a):return payoff(h+(a,),len(h))

def main():
    levels={}
    for h in product(range(5),repeat=2):
        best=max(immediate(h,a) for a in range(5))
        levels.setdefault(str(best),0);levels[str(best)]+=1
    theta=min(max(immediate(h,a) for a in range(5))
              for h in product(range(5),repeat=2))
    assert theta==Fraction(3,2)
    witnesses=[]
    for a in range(5):
        b,c=(a-1)%5,(a+1)%5
        h=(a,b,c)
        u=tuple(payoff(h,i) for i in range(3))
        assert u==(1,theta,theta)
        # The final player instead has a customer-disjoint theme with payoff 2.
        best=max(immediate((a,b),d) for d in range(5))
        assert best==2>u[-1]
        witnesses.append({'root':a,'terminal':h,'payoffs':list(map(str,u)),
                         'welfare':sum(any(v in e for v in h) for e in EDGES),
                         'last_best_reply':str(best)})
    instance=Instance(tuple(map(str,range(5))),
                      tuple(CustomerType(e) for e in EDGES),3)
    solver=ExactSPESolver(instance)
    outcomes=solver.outcomes()
    paths=list(solver.ordered_outcomes())
    min_player=min(payoff(h,i) for h in paths for i in range(3))
    assert solver.minimum_welfare()==5
    assert min_player==theta
    report={'identity':'C5 induction-only theta propagation obstruction',
            'arithmetic':'exact Fraction',
            'theta':str(theta),'last_prefix_count':25,
            'last_best_payoff_histogram':levels,
            'bad_interface_witnesses':witnesses,
            'full_SPE_crosscheck':{'oracle':'canonical ExactSPESolver',
                'root_terminal_count_vectors':len(outcomes),
                'root_ordered_paths':len(paths),
                'minimum_root_welfare':solver.minimum_welfare(),
                'minimum_any_player_root_payoff':str(min_player)},
            'scope':'five explicit arbitrary continuations, not SPE. '
                    'No general theta-floor theorem proved or refuted.'}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
