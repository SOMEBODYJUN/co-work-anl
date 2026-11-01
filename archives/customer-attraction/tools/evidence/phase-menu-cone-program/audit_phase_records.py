"""One standard-library structural/data audit; no source import, payoff matrix, BI, LP.

Checks every recorded action against the reported phase rule and records that
all prescribed labels cover one common block. Scalar B/n-private comparisons
are recorded for both decimal literals and exact binary-float interpretations.
The all-history SPE and exact PAIR=0 conclusions for the separate integer
calibrations are proved analytically, rather than by recomputing an IC matrix.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement,groupby
from collections import Counter
from datetime import datetime,timezone
import hashlib,json,time

BASE=Path(__file__).resolve().parent
OUT=BASE/'round21-phase-data-audit'
assert not OUT.exists(), 'Preserve the unique audit; do not overwrite or rerun.'
OUT.mkdir()
START=datetime.now(timezone.utc).isoformat();CLOCK=time.monotonic()
def fp(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def plain(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return list(map(plain,x))
 return x
def action(h,k,phase):
 if not h:return 0
 groups=(tuple(range(k//2)),tuple(range(k//2,k)))
 owner=lambda x: int(x>=k//2)
 ref=phase['ref'];bits=phase['bits'];pick=phase['pick']
 g=owner(h[0] if ref=='first' else h[-1])^((bits>>(len(h)-1))&1)
 G=groups[g]
 if pick=='fresh':return min(G,key=lambda x:(h.count(x),x))
 if pick=='cycle':return G[sum(owner(x)==g for x in h)%len(G)]
 assert pick=='repeat';return G[0]

records=[]
for n,k,name in [(4,8,'round21-phase-n4k8.json'),(5,7,'round21-phase-n5k7.json')]:
 path=BASE/name
 raw=json.loads(path.read_text(),parse_float=str)
 x=json.loads(path.read_text(),parse_float=F)
 binary=json.loads(path.read_text())
 assert set(x)=={'status','n','k','completed','elapsed','phases','best'}
 assert x['n']==n and x['k']==k and x['status']=='numerical screening only'
 assert len(x['phases'])==x['completed']==6*(1<<(n-1))
 fullphase=[(ref,bits,pick) for ref in ('first','last') for bits in range(1<<(n-1)) for pick in ('fresh','cycle','repeat')]
 assert [(p['ref'],p['bits'],p['pick']) for p in x['phases']]==fullphase
 phase_rows=[]
 for ph,rph in zip(x['phases'],raw['phases']):
  h=()
  while len(h)<n:h+=action(h,k,ph),
  if 'feasible_without_universal' in ph:
   assert set(ph)=={'ref','bits','pick','feasible_without_universal'} and ph['feasible_without_universal'] is False
  else:
   assert set(ph)=={'ref','bits','pick','path','gap'} and list(h)==ph['path']
  phase_rows.append({'ref':ph['ref'],'bits':ph['bits'],'pick':ph['pick'],'derived_path':list(h),'recorded':rph})
 b=x['best'];rb=raw['best']
 assert set(b)=={'gap','weights','p','q','first','rivals','iteration','policy','phase'}
 assert b['phase'] in x['phases'] and b['phase']['gap']==b['gap'] and b['iteration']==0
 assert b['first']==b['phase']['path'][:2]
 histories=[h for d in range(n) for h in product(range(k),repeat=d)]
 assert len(b['policy'])==len(histories)
 assert [tuple(r['history']) for r in b['policy']]==histories
 assert all(set(r)=={'history','action'} for r in b['policy'])
 assert all(r['action']==action(h,k,b['phase']) for h,r in zip(histories,b['policy']))
 assert len(b['weights'])==(1<<k)-1 and len(b['p'])==k
 pos={mask:F(w) for mask,w in enumerate(b['weights'],1) if w}
 bigmask=239 if n==4 else 13
 unit=F(1,5) if n==4 else F('0.11111111111111112')
 expected={239:4,16:1} if n==4 else {13:5,2:1,16:1,32:1,64:1}
 assert pos=={mask:unit*mass for mask,mass in expected.items()}
 binary_weights=[F.from_float(v) if isinstance(v,float) else F(v) for v in binary['best']['weights']]
 private_masks=[mask for mask in expected if mask!=bigmask]
 scalar_checks=[{'private_mask':mask,'decimal_big_over_n_minus_private':pos[bigmask]/n-pos[mask],
                 'binary_big_over_n_minus_private':binary_weights[bigmask-1]/n-binary_weights[mask-1]}
                for mask in private_masks]
 assert all((bigmask>>r['action'])&1 for r in b['policy'])
 assert b['p']==[F(1)]+[F(0)]*(k-1)
 rivals=list(combinations_with_replacement(range(k),n-3))
 assert [tuple(B) for B in b['rivals']]==rivals and len(b['q'])==len(rivals)
 assert sum(b['q'])==1 and all(q>=0 for q in b['q'])
 qs=[(list(B),q) for B,q in zip(rivals,b['q']) if q]
 assert qs==[([7],F(1))] if n==4 else qs==[([3,3],F(1))]
 actions=[r['action'] for r in b['policy']]
 # Lossless reading view: histories have already been checked to be complete
 # length-then-lexicographic order, so their actions can be run-length encoded.
 level_rle=[];offset=0
 for d in range(n):
  count=k**d;aa=actions[offset:offset+count];offset+=count
  rr=[{'action':a,'repeat':len(list(g))} for a,g in groupby(aa)]
  level_rle.append({'depth':d,'histories':count,'action_runs':rr})
 report={'source':fp(path),'top_field_count':len(x),'best_field_count':len(b),'n':n,'k':k,
 'all_phase_rows':phase_rows,'reported_initial_LP_unsuccessful':sum('feasible_without_universal' in p for p in x['phases']),
 'full_policy_nodes':len(histories),'all_history_keys_in_expected_order':True,'phase_rule_matches_every_stored_action':True,
 'all_prescribed_actions_cover_big_block':True,'action_counts':dict(Counter(actions)),'policy_lossless_level_runs':level_rle,
 'weight_literals':rb['weights'],'positive_weights':pos,'common_scale_literal':unit,'integer_ray':expected,
 'literal_total_weight':sum(b['weights']),'literal_total_weight_minus_one':sum(b['weights'])-1,
 'binary_exact_positive_weights':{mask:w for mask,w in enumerate(binary_weights,1) if w},
 'binary_exact_total_weight_minus_one':sum(binary_weights)-1,'scalar_root_bounds':scalar_checks,
 'scalar_root_bound_comparison_count':2*len(private_masks),
 'root_query':b['p'],'tail_rivals':b['rivals'],'tail_Q':b['q'],'tail_Q_support':qs,'saved_gap_literal':rb['gap'],
 'saved_phase':rb['phase'],'source_iteration_field':b['iteration'],
 'scope':'Data/structure plus the explicit scalar B/n-private bounds in two interpretations. No full-policy completion, payoff or incentive matrix was recomputed. Analytic integer-calibration proof is separate.'}
 records.append(report)
REPORT=OUT/'reported-data-audit.json'
REPORT.write_text(json.dumps(plain({'status':'PASS_DATA_AND_FULL_POLICY_STRUCTURE','records':records,'new_payoff_tables':0,'new_full_history_IC_comparisons':0,'scalar_root_bound_comparisons':sum(r['scalar_root_bound_comparison_count'] for r in records),'LP_calls':0,'original_function_calls':0}),ensure_ascii=False,indent=2)+'\n')
event={'started_utc':START,'finished_utc':datetime.now(timezone.utc).isoformat(),'seconds':time.monotonic()-CLOCK,'script':fp(Path(__file__)),'report':fp(REPORT),'source_inputs':[r['source'] for r in records],'data_structure_audit_calls':1,'original_function_calls':0,'LP_calls':0,'new_payoff_tables':0,'new_full_history_IC_comparisons':0,'scalar_root_bound_comparisons':sum(r['scalar_root_bound_comparison_count'] for r in records),'DP_calls':0}
(OUT/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS_DATA_AND_FULL_POLICY_STRUCTURE','histories':[r['full_policy_nodes'] for r in records],'phases':[len(r['all_phase_rows']) for r in records],'LP':0}))
