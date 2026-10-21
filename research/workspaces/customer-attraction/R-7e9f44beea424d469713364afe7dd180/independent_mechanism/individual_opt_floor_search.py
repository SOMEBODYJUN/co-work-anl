"""Candidate search for individual u_i >= OPT_m/(2m-1), inside fixed full SPE cones.
Numerical optima are observations only; any proposed violation is independently
checked on exact integer customer clones and every ordered history.
"""
from pathlib import Path
import json,sys
from fractions import Fraction
from itertools import combinations
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,payoff_row,integer_clones,independently_verify,serializable,instance_from_clones

def strategies(obj):
 if isinstance(obj,dict):
  aa=obj.get('actions')
  if isinstance(aa,list) and aa and isinstance(aa[0],dict) and 'history' in aa[0] and 'action' in aa[0]:
   yield aa
  for v in obj.values():yield from strategies(v)
 elif isinstance(obj,list):
  for v in obj:yield from strategies(v)

if __name__=='__main__':
 results=[];seen=set()
 paths=list((ROOT/'evidence/certificates/customer_attraction').glob('*.json'))+[ROOT/'evidence/runs/2026-10-09/cone_attack_credible_selected.json']
 for path in sorted(paths):
  try:obj=json.loads(path.read_text())
  except Exception:continue
  for aa in strategies(obj):
   if len(aa)>4000:continue
   acts={tuple(x['history']):x['action'] for x in aa}
   key=tuple(sorted(acts.items()))
   if key in seen:continue
   seen.add(key)
   p=1+max(max(h+(a,)) for h,a in acts.items());m=1+max(map(len,acts))
   if p>7:continue
   try:cone=StrategyCone(p,m,acts)
   except ValueError:continue
   h=()
   while len(h)<m:h+=(acts[h],)
   for a in sorted(set(h)):
    cone.welfare=payoff_row(p,cone.root,a)
    for support in combinations(range(p),min(m,p)):
     r=cone.optimize(support)
     if not r.get('certified'):continue
     ratio=r['value'];record={'source':str(path.relative_to(ROOT)),'m':m,'p':p,'root':h,'action':a,'ratio':ratio,'threshold':2*m-1,'exact_dual':r['dual_optimal']}
     results.append(record)
     print(json.dumps(serializable(record)),flush=True)
     if ratio>2*m-1:
      clones=integer_clones(r['values'])
      assert independently_verify(cone,clones)
      inst=instance_from_clones(p,m,clones)
      record['clones']=clones;record['actions']=aa;record['actual_optimum']=inst.optimal_welfare()
      dest=Path(__file__).with_name('individual_floor_counterexample.json')
      dest.write_text(json.dumps(serializable(record),indent=2)+'\n')
      print('VIOLATION_SAVED',dest,flush=True);sys.exit()
 Path(__file__).with_name('individual_floor_scan.json').write_text(json.dumps(serializable(results),indent=2)+'\n')
