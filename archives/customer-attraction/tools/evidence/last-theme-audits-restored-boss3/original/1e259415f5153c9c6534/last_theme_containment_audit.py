"""Exact arithmetic audit of the last-theme containment sufficient condition."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import ExactSPESolver
from cascade_attack import Engine, seeds

def main():
    cases=0
    for m in range(1,26):
        for k in range(1,m+1):
            bound=1+F(m*(m-1),k*(2*m-k))
            assert (bound<=2)==((m-k)**2<=m)
            if k==m:assert bound==2-F(1,m)
            if m==1:assert bound==1
            for c in range(0,m+1):
                for in_b in (0,1):
                    if in_b and not c:continue
                    d=c-in_b
                    tax=F(d,d+1)
                    cover=int(c>0)
                    own=F(in_b,c) if c else F(0)
                    residual=F(1,c+1) if c and not in_b else F(0)
                    assert tax==cover-own-residual
                    for t in range(m+1):
                        assert int(t>0)<=F(t,d+1)+tax
                    cases+=1
    instances=[];ordered=0;strong=0
    for p,a in ((7,2),(8,3)):
        eng=Engine(p,5)
        for r in list(seeds(p,5,a))[:3]:
            inst=eng.instance(r); solver=ExactSPESolver(inst)
            ratio=eng.solve(r)
            assert {eng.term[int(i)] for i in eng.R[(0,)*p]}==set(solver.outcomes())
            assert ratio==solver.inefficiency_ratio()
            supports=[frozenset(j for j,x in enumerate(inst.customers) if i in x.topics) for i in range(p)]
            for path in solver.ordered_outcomes():
                ordered+=1
                q=inst.counts(path,terminal=True); pay=inst.player_payoffs(path); W=inst.welfare(q); u=pay[-1]; B=supports[path[-1]]
                k=sum(B<=supports[i] for i in path)
                assert inst.optimal_welfare()<=W+4*u
                assert W>=F(k*(10-k),5)*u
                if (5-k)**2<=5:
                    strong+=1;assert inst.optimal_welfare()<=2*W
            instances.append({'topics':p,'players':5,'ratio':str(ratio),'terminal_outcomes':len(solver.outcomes())})
    print(json.dumps({'per_customer_and_threshold_cases':cases,'exact_games':instances,'ordered_spe_paths':ordered,'paths_in_half_coverage_condition':strong,'status':'all exact checks passed'},indent=2))

if __name__=='__main__':main()
