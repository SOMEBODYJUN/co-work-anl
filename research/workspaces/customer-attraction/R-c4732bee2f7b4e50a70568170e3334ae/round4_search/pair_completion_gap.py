"""Exact finite warning: retained-overlap pair rows are not completion.
The complete two-player reply-envelope formula is checked on all ordered paths.
No new general welfare bound is asserted.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import ExactSPESolver
from customer_attraction_strategy_lp import instance_from_clones,serializable
# A=0, T=1, B=2, unit clones. Neither A nor T contains the other.
clones=(2,4,2,5,0,0,0)
inst=instance_from_clones(3,2,clones)
f=lambda a:sum(F(n) for mask,n in enumerate(clones,1) if mask&(1<<a))
g=lambda a,b:sum(F(n,2) for mask,n in enumerate(clones,1) if mask&(1<<a) and mask&(1<<b))
u=lambda a,b:f(a)-g(a,b)
A,B=0,2;ua,ub=u(A,B),u(B,A);H=ua+ub+g(A,A)
pair_slacks={(a,b):H-f(a)-f(b)+g(a,b) for a,b in product(range(3),repeat=2)}
assert min(pair_slacks.values())==0 and all(s>=0 for s in pair_slacks.values())
BR={a:tuple(b for b in range(3) if u(b,a)==max(u(c,a) for c in range(3))) for a in range(3)}
L={a:min(u(a,b) for b in BR[a]) for a in range(3)}
assert B in BR[A] and BR[1]==(B,) and L[1]>ua
solver=ExactSPESolver(inst)
ordered=tuple(solver.ordered_outcomes())
for a,b in product(range(3),repeat=2):
 criterion=b in BR[a] and u(a,b)>=max(L.values())
 assert criterion==((a,b) in ordered)
report={'scope':'three-topic two-player exact illustration; necessary pair rows alone do not characterize SPE completion','instance':inst.to_dict(),'advertised_path':[A,B],'advertised_welfare':inst.welfare(inst.counts((A,B),terminal=True)),'advertised_payoffs':[ua,ub],'H':H,'pair_slacks':[{'queries':[a,b],'slack':s} for (a,b),s in pair_slacks.items()],'BR':BR,'minimum_leader_payoffs_over_best_replies':L,'all_true_ordered_SPE_paths':ordered,'OPT':inst.optimal_welfare(),'exact_reply_envelope_matches_all_nine_paths':True,'identity_at_queries_T_B':{'root_deviation_slack':ua-u(1,B),'reply_optimality_slack':u(B,1)-u(B,1),'actual_last_comparison_slack':ub-u(B,A),'self_tax_difference':g(A,A)-g(A,B)}}
Path(__file__).with_suffix('.json').write_text(json.dumps(serializable(report),indent=2)+'\n')
print(json.dumps(serializable(report)))
