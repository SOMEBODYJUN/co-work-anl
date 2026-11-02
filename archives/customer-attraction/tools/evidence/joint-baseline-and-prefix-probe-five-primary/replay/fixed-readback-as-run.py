"""Fixed saved-input readback, not the original 400-input random search."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util, hashlib, json, sys, time
started=time.perf_counter()
rt=Path(__file__).resolve().parent
source=Path('/workspace/scratch/dbba67e5e59f/boss1-runtime/sources/research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/background_induction/prefix_penalty_probe.json')
oracle=Path('/workspace/scratch/dbba67e5e59f/co-work-anl-boss1/archives/customer-attraction/tools/evidence/pay-original-implementation-comparison/original/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py')
assert hashlib.sha256(oracle.read_bytes()).hexdigest()=='7f6186785c5186ff2e591e4ef91bf1a5d75e70c73569ccef0f719e35ca9f9205'
x=json.loads(source.read_text());q=x['q'];m=x['m'];weights={int(a):w for a,w in x['weights'].items()};path=x['actual_path'];actual=tuple(path.count(a) for a in range(q))
assert m==5 and q==6 and sum(weights.values())==46 and actual==tuple(x['actual_counts'])
counts=[z for z in product(range(m+1),repeat=q) if sum(z)==m]
def covered(c): return sum(w for mask,w in weights.items() if any(c[a] and mask>>a&1 for a in range(q)))
opt=max(map(covered,counts));opts=[z for z in counts if covered(z)==opt]
assert len(counts)==252 and opt==46 and len(opts)==101
assert F(x['welfare'])==covered(actual)==opt==F(x['optimum'])
loads={mask:sum(actual[a] for a in range(q) if mask>>a&1) for mask in weights}
pays=[sum((F(w,loads[mask]) for mask,w in weights.items() if mask>>a&1),F(0)) if actual[a] else None for a in range(q)]
assert [pays[a] for a in path]==[F(48,5)]*3+[F(43,5)]*2
# Rebuild all endpoints independently from the formula, without importing probe.
def charge(k,prefix,c):
 types=[];breaks={F(0),F(4)}
 for mask,w in weights.items():
  d=sum(c[a] for a in range(q) if mask>>a&1)
  if not d:continue
  b=sum(prefix[a] for a in range(q) if mask>>a&1)
  types.append((w,b,d));breaks.add(F(4*m*(b+1),d*(k-1)+m*(b+1)))
 def score(t):
  return sum((w*(1-F(2*(k-2)*d,m*(b+k))-min(t*d/(m*(b+1)),(t*d/m+4-t)/(b+k))) for w,b,d in types),F(0))
 return min((score(t),t) for t in breaks)
prefix=[0]*q;early=F(0);rows=[]
for depth in range(m-1):
 k=m-depth;value,t,c=min((charge(k,prefix,c)+(c,)) for c in opts)
 row={'k':k,'best_margin':str(value-2*early),'best_t':str(t),'optimal_counts':list(c)}
 assert row==x['margins'][depth];rows.append(row)
 a=path[depth];prefix[a]+=1;early+=pays[a]
assert min(F(r['best_margin']) for r in rows)==F(x['minimum_prefix_payment_margin'])==F(-1138,25)
# One fixed original oracle input, no random search, no complete action certificate.
spec=importlib.util.spec_from_file_location('fixed_prior_background_oracle',oracle);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
sol=mod.BackgroundSolver(q,m,[0]*q,weights);minimum,terminal=sol.minimum();idx=sol.tidx[terminal]
assert minimum==46 and terminal==actual
prefix=[0]*q;reconstructed=[]
for depth in range(m):
 floor=sol.thresholds[tuple(prefix)];legal=[]
 for a in range(q):
  child=prefix.copy();child[a]+=1
  if (sol.solve(tuple(child))>>idx)&1 and sol.pays[idx][a]>=floor:legal.append(a)
 assert legal
 a=legal[0];reconstructed.append(a);prefix[a]+=1
assert reconstructed==path
result={'source_json_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'oracle_sha256':hashlib.sha256(oracle.read_bytes()).hexdigest(),'original_random_main_invocations':0,'new_fixed_oracle_instances':1,'canonical_package_imports':0,'LP_MIP_calls':0,'full_strategy_certificates_created':0,'static_terminal_count_profiles':len(counts),'unit_customers':sum(weights.values()),'static_optimum':opt,'optimal_count_profiles':len(opts),'saved_actual_counts':list(actual),'saved_path':path,'reconstructed_lexicographic_credible_path':reconstructed,'minimum_realizable_SPE_welfare_for_this_fixed_input':str(minimum),'actual_position_payoffs':[str(pays[a]) for a in path],'all_four_saved_margin_records_match':True,'margins':rows,'minimum_prefix_payment_margin':x['minimum_prefix_payment_margin'],'original_completed_trials_and_no_positive_flag_not_replayed':True,'elapsed_seconds':time.perf_counter()-started}
(rt/'fixed-readback.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
