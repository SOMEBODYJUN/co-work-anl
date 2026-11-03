"""Optimize genuine welfare ratio in early-A/terminal-switch full policy cones."""
import sys,json,time,argparse
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import StrategyCertificate
from customer_attraction_strategy_lp import StrategyCone,serializable
from cone_attack_credible_variants import exact_export
ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
p,m=a.topics,a.players;E,F=p-2,p-1
report={'scope':'one early-A complete strategy cone, all comparison portfolios; not all SPE cones','universal_bound_proved':False,'batches':[]}
actions={h:0 if len(h)<m-1 or h.count(0)<m-2 else E if F in h else F for d in range(m) for h in product(range(p),repeat=d)}
cone=StrategyCone(p,m,actions);record={'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),'root_counts':cone.root,'portfolio_proofs':[]}
for J in combinations(range(p),min(p,m)):
    r=cone.optimize(J)
    if r['certified']:record['portfolio_proofs'].append(exact_export(cone,r))
    print(json.dumps(serializable({'J':J,'value':r.get('value'),'certified':r['certified'],'dual':r.get('dual_bound')})),flush=True)
report['batches']=[{'players':m,'topics':p,'cone_proofs':[record]}]
a.output.write_text(json.dumps(serializable(report),indent=2)+'\n')
