"""Independent definition-level unit-customer replay; no canonical solver import."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'zero_regret_repair_witness.json').read_text())
customers=[frozenset(t['topics']) for t in data['customers'] for _ in range(t['multiplicity'])]
K=range(len(data['topics']))

def utility(background, tail, actor):
    topic=tail[actor]
    return sum((Fraction(1,sum(background[a] for a in x)+sum(a in x for a in tail))
                for x in customers if topic in x),Fraction())

def welfare(tail):
    return sum(any(a in x for a in tail) for x in customers)

def all_spe(background):
    valid=[]
    tested=0
    for last in product(K,repeat=len(data['topics'])):
        if any(utility(background,(a,last[a]),1)<utility(background,(a,b),1)
               for a in K for b in K):continue
        for first in K:
            tested+=1
            if all(utility(background,(first,last[first]),0)>=utility(background,(a,last[a]),0) for a in K):
                valid.append((first,last))
    return valid,tested

def three_player_root_classification():
    children=[]
    for d in K:
        background=[int(a==d) for a in K]
        strategies,_=all_spe(background)
        leaves=sorted(set((first,last[first]) for first,last in strategies))
        incumbent=[utility([0]*len(data['topics']),(d,)+tail,0) for tail in leaves]
        children.append((leaves,incumbent))
    root_floor=max(min(v) for _,v in children)
    outcomes=[(d,)+tail for d,(leaves,values) in enumerate(children)
              for tail,value in zip(leaves,values) if value>=root_floor]
    assert outcomes==[(1,3,2)]
    return [{'background_topic':d,'tail_outcomes':leaves,'incumbent_values':list(map(str,values))}
            for d,(leaves,values) in enumerate(children)]

old=data['old_background'];new=data['deleted_background']
old_spe,old_root_checks=all_spe(old)
new_spe,new_root_checks=all_spe(new)
policy=data['old_tail_strategy'];first=policy['first_action'];last=tuple(policy['last_after_first'])
assert old_spe==[(2,(2,2,1,2))]
assert new_spe==[(3,(2,3,1,1))]
q=(first,last[first])
R1=max(utility(new,(a,last[a]),0)-utility(new,q,0) for a in K)
R2=max(utility(new,(first,a),1)-utility(new,q,1) for a in K)
assert (R1,R2)==(0,0)
assert welfare(q)==17
assert [welfare((a,l[a])) for a,l in new_spe]==[16]
assert max(welfare((a,b)) for a in K for b in K)==17

tables={}
for label,background in [('old',old),('deleted',new)]:
    tables[label]=[[str(utility(background,(a,b),1)) for b in K] for a in K]

report={
    'contract':'Definition-level complete ordered-history SPE enumeration in the exact 2-tail witness; not a main-target search.',
    'unit_customers':len(customers),
    'full_strategies_per_game':len(data['topics'])**(len(data['topics'])+1),
    'old_SPEs':[{'first':a,'last':l,'tail_welfare':welfare((a,l[a]))} for a,l in old_spe],
    'deleted_SPEs':[{'first':a,'last':l,'tail_welfare':welfare((a,l[a]))} for a,l in new_spe],
    'actual_node_regrets':[str(R1),str(R2)],
    'retained_root_payoffs_after_deletion':[str(utility(new,(a,last[a]),0)) for a in K],
    'last_payoff_tables':tables,
    'deleted_optimum':17,
    'minimum_welfare_repair_loss':1,
    'original_three_player_child_classification':three_player_root_classification(),
    'original_three_player_unique_root_outcome':[1,3,2],
    'uniform_replication':'All utilities and welfare multiply by the positive integer replication factor; strict inequalities and ties are preserved, so repair loss is unbounded while both actual-node regrets remain zero.'
}
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',default='zero_regret_repair_audit.json');args=parser.parse_args()
out=ROOT/args.output
if out.exists():raise FileExistsError(out)
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
