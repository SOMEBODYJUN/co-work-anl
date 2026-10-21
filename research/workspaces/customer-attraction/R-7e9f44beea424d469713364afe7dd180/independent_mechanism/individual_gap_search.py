"""Fixed-cone attack on OPT_m <= W + m*u_i (candidate, not a theorem)."""
from individual_opt_floor_search import *
import numpy as np
from scipy.optimize import linprog
from customer_attraction_strategy_lp import coverage_row,dot

def optimize(cone,objective):
 r=linprog(-np.array(objective,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
 if not r.success:return None
 vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in r.x)
 if not cone.verify(vals) or dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(r.x)
 if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:return None
 return vals,dot(objective,vals)

if __name__=='__main__':
 results=[];seen=set();paths=list((ROOT/'evidence/certificates/customer_attraction').glob('*.json'))+[ROOT/'evidence/runs/2026-10-09/cone_attack_credible_selected.json']
 for path in sorted(paths):
  try:obj=json.loads(path.read_text())
  except Exception:continue
  for aa in strategies(obj):
   if len(aa)>4000:continue
   acts={tuple(x['history']):x['action'] for x in aa};key=tuple(sorted(acts.items()))
   if key in seen:continue
   seen.add(key);p=1+max(max(h+(a,)) for h,a in acts.items());m=1+max(map(len,acts))
   if p>7:continue
   try:cone=StrategyCone(p,m,acts)
   except ValueError:continue
   actualw=cone.welfare;h=()
   while len(h)<m:h+=(acts[h],)
   for a in sorted(set(h)):
    cone.welfare=payoff_row(p,cone.root,a)
    for support in combinations(range(p),min(m,p)):
     objective=tuple(x-y for x,y in zip(coverage_row(p,support),actualw));r=optimize(cone,objective)
     if r is None:continue
     vals,value=r;record={'source':str(path.relative_to(ROOT)),'m':m,'p':p,'root':h,'action':a,'gap_over_payoff':value,'threshold':m}
     results.append(record);print(json.dumps(serializable(record)),flush=True)
     if value>m:
      clones=integer_clones(vals);assert independently_verify(cone,clones)
      inst=instance_from_clones(p,m,clones);record.update({'clones':clones,'actions':aa,'actual_optimum':inst.optimal_welfare()})
      dest=Path(__file__).with_name('individual_gap_counterexample.json');dest.write_text(json.dumps(serializable(record),indent=2)+'\n');print('VIOLATION_SAVED',dest,flush=True);sys.exit()
 Path(__file__).with_name('individual_gap_scan.json').write_text(json.dumps(serializable(results),indent=2)+'\n')
