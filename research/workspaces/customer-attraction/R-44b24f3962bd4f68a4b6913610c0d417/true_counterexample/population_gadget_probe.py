"""Finite seed probe of continuation_order's population gadget plus private topics.
No general inference or target counterexample is claimed.
"""
import json
from pathlib import Path
import sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import instance_from_clones
from customer_attraction import ExactSPESolver
rows=[]
for weight in range(1,13):
    c=[0]*127
    for mask,v in {1:12,2:12,4:4,3:4,5:8,6:8,8:weight,16:weight,32:weight,64:weight}.items():c[mask-1]=v
    i=instance_from_clones(7,5,c);s=ExactSPESolver(i);q=min(s.worst_outcomes())
    rows.append({'private_multiplicity':weight,'worst_root':q,'worst_welfare':i.welfare(q),'optimum':i.optimal_welfare(),'ratio':str(s.inefficiency_ratio())})
out={'scope':'12 finite legal seeds only; no general theorem','source':'sibling continuation_order/population_paradox.md, original gadget scaled fourfold','players':5,'topics':7,'base_types':{1:12,2:12,4:4,3:4,5:8,6:8},'added_types':[8,16,32,64],'rows':rows}
newpath=Path(__file__).with_name('restricted_m5p7_population.json')
if newpath.exists():
    new=json.loads(newpath.read_text())['exact_candidate']['integer_clones']
    old=json.loads(Path(__file__).with_name('population_gadget_seed.json').read_text())['exact_candidate']['integer_clones']
    mixed=[]
    for factor in (1,2,5,10,100,1000):
        c=[factor*x+y for x,y in zip(new,old)]
        solver=ExactSPESolver(instance_from_clones(7,5,c));R=solver.outcomes()
        mixed.append({'new_to_old_scale':factor,'root_221_realizable':(2,2,1,0,0,0,0) in R,'root_outcome_count':len(R),'all_state_retained_outcomes':solver.stats.retained_outcomes,'ratio':str(solver.inefficiency_ratio())})
    out['finite_vertex_degeneracy_probe']=mixed
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
