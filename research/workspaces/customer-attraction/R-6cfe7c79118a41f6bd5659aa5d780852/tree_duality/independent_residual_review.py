"""Independent expanded-unit-customer audit of global_proof's supplied JSON."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
BASE=Path(__file__).resolve().parents[1]
doc=json.loads((BASE/'global_proof'/'residual_counterexample.json').read_text())
inst=doc['instance'];p=len(inst['topics']);assert inst['players']==2
# Materialize distinct unit customers; compute all payoffs from set membership.
interest=[]
for block in inst['customers']:
    assert isinstance(block['multiplicity'],int) and block['multiplicity']>=0
    interest.extend([frozenset(block['topics']) for _ in range(block['multiplicity'])])
topics=[{x for x,B in enumerate(interest) if a in B} for a in range(p)]
assert len(interest)==27 and len({frozenset(T) for T in topics})==p

def utility(a,path):
    return sum((F(1,sum(x in topics[b] for b in path)) for x in topics[a]),F(0))
actions={tuple(x['history']):x['action'] for x in doc['certificate']['actions']}
assert set(actions)=={()}|{(a,) for a in range(p)}
comparisons=[];table=[]
for a in range(p):
    values=[utility(b,(a,b)) for b in range(p)]
    chosen=actions[a,];actual=values[chosen]
    assert actual==max(values)
    for b in range(p):comparisons.append(actual-values[b])
    table.append([str(x) for x in values])
root_values=[utility(a,(a,actions[a,])) for a in range(p)]
actual_first=root_values[actions[()]]
for v in root_values:comparisons.append(actual_first-v)
assert len(comparisons)==42 and all(s>=0 for s in comparisons)
path=(actions[()],actions[actions[()],]);C=set().union(*(topics[a] for a in path));W=len(C)
pairs={f'{a},{b}':len(topics[a]|topics[b]) for a,b in combinations_with_replacement(range(p),2)}
opt=max(pairs.values());optimal_pairs=[k for k,v in pairs.items() if v==opt]
residues={f'{a},{b}':len((topics[a]|topics[b])-C) for a,b in combinations_with_replacement(range(p),2)}
R=max(residues.values())
assert path==(0,1) and W==13 and opt==14 and R==14
assert optimal_pairs==['1,2','1,3','2,3']
assert len((topics[2]|topics[3])-C)==14 and 2*W>=opt
# Exhaust every possible complete follower strategy; no canonical solver.
BRs=[[b for b in range(p) if utility(b,(a,b))==max(utility(t,(a,t)) for t in range(p))] for a in range(p)]
minW=10**9;maps=0;spe_profiles=0;witness=None
for replies in product(*BRs):
    maps+=1;vals=[utility(a,(a,replies[a])) for a in range(p)];best=max(vals)
    for a in range(p):
        if vals[a]==best:
            spe_profiles+=1;w=len(topics[a]|topics[replies[a]])
            if w<minW:minW=w;witness={'root':a,'replies':list(replies)}
assert minW==12
out={'status':'passed','unit_customers':len(interest),'nodes':len(actions),'all_action_comparisons':len(comparisons),'follower_payoff_table':table,'root_deviation_values':[str(v) for v in root_values],'actual_path':path,'actual_welfare':W,'optimal_welfare':opt,'optimal_pairs':optimal_pairs,'maximum_residual_union':R,'all_follower_BR_maps_enumerated':maps,'complete_SPE_root_choices':spe_profiles,'minimum_SPE_welfare':minW,'minimum_welfare_witness':witness,'identity':'counterexample only to W >= maximal residual union; Q-CAG-HALF remains open'}
Path(__file__).with_name('independent_residual_review.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
