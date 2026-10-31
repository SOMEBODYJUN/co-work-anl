"""Verify three frozen paired-cone primal points by explicit unit customers.
No original module, numerical solver, LP or policy search is imported/run.
"""
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction as F
from math import lcm
import json

base=Path(__file__).resolve().parent/'root-mj-paired-and-square-originals'
records=[]
for sid in ['56e5fe0224fc3057d7fa','376e65e5dec9b7bbebc6','0ff5ed0483e6f60a136c']:
 source=next((base/sid).glob('*.json'));j=json.loads(source.read_text())
 original={tuple(z['history']):z['action'] for z in j['actions']} if isinstance(j['actions'][0],dict) else {tuple(h):a for h,a in j['actions']}
 p=max([a for a in original.values()]+[a for h in original for a in h])+1
 root=tuple(j.get('actual_root',j.get('root')));n=len(root);N=(1<<p)-1
 assert len(original)==len(j['actions']) and set(original)=={h for d in range(n)for h in product(range(p),repeat=d)}
 assert all(0<=a<p for a in original.values()) and len(j['x'])==2*N
 reps={tuple(root[:-1].count(a)for a in range(p)):root[:-1]}
 for h in product(range(p),repeat=n-1):reps.setdefault(tuple(h.count(a)for a in range(p)),h)
 normal=original.copy()
 for h in product(range(p),repeat=n-1):normal[h]=original[reps[tuple(h.count(a)for a in range(p))]]
 if 'normalized_actions'in j:assert normal=={tuple(h):a for h,a in j['normalized_actions']}
 weights=list(map(F,j['x']));assert min(weights)>=0
 scale=lcm(*(x.denominator for x in weights));populations=[]
 for half in [weights[:N],weights[N:]]:
  populations.append([mask for mask,w in enumerate(half,1)for _ in range(int(w*scale))])
 def terminals(policy):
  ends={h:h for h in product(range(p),repeat=n)}
  for d in range(n-1,-1,-1):
   for h in product(range(p),repeat=d):ends[h]=ends[h+(policy[h],)]
  return ends
 ends0,ends1=terminals(original),terminals(normal)
 assert ends0[()]==ends1[()]==root
 def payoff(end,action,clients):
  return sum((F(1,sum(bool(mask&(1<<a))for a in end))for mask in clients if mask&(1<<action)),F(0))/scale
 def welfare(end,clients):return F(sum(any(mask&(1<<a)for a in end)for mask in clients),scale)
 coverage=welfare(root,populations[0])+welfare(root,populations[1]);assert coverage==1
 paired_early=terminal_rows=individual_rows=0;separate_min=[None,None]
 for h in sorted(original,key=lambda h:(len(h),h)):
  for a in range(p):
   if a==original[h]:continue
   slacks=[]
   for q,(policy,ends,clients)in enumerate(zip([original,normal],[ends0,ends1],populations)):
    chosen=policy[h]
    # Early prescribed actions agree; at terminal nodes the alternate loop is
    # rebuilt below because each policy may prescribe a different last label.
    if len(h)==n-1:continue
    v=payoff(ends[h],chosen,clients)-payoff(ends[h+(a,)],a,clients)
    slacks.append(v);individual_rows+=1
    separate_min[q]=v if separate_min[q]is None else min(separate_min[q],v)
   if slacks:assert sum(slacks)>=0;paired_early+=1
 for q,(policy,ends,clients)in enumerate(zip([original,normal],[ends0,ends1],populations)):
  for h in product(range(p),repeat=n-1):
   for a in range(p):
    if a==policy[h]:continue
    v=payoff(ends[h],policy[h],clients)-payoff(ends[h+(a,)],a,clients)
    assert v>=0;terminal_rows+=1;individual_rows+=1
    separate_min[q]=v if separate_min[q]is None else min(separate_min[q],v)
 assert all(v>=0 for v in separate_min)
 support=tuple(j['support']);value=sum(welfare(support,clients)for clients in populations)
 assert value==F(j['value'])
 opt=max(sum(welfare(s,clients)for clients in populations)for s in combinations(range(p),min(n,p)))
 records.append(dict(source=sid,players=n,topics=p,policy_nodes=len(original),unit_scale=scale,unit_population_sizes=list(map(len,populations)),positive_type_weights=[dict(population='u'if i<N else'v',mask=i%N+1,weight=str(w))for i,w in enumerate(weights)if w],root=list(root),normalization=str(coverage),recorded_support_value=str(value),exact_paired_population_OPT=str(opt),paired_early_constraints=paired_early,independent_terminal_constraints=terminal_rows,individual_nonself_rows_actually_checked=individual_rows,separate_populations_min_IC=list(map(str,separate_min)),both_separately_SPE_for_these_three_points=True,does_not_prove_global_optimum_or_general_separation=True))
print(json.dumps(dict(status='all_three_frozen_points_exactly_feasible',records=records,new_LP_calls=0,new_original_program_entries=0,new_random_searches=0,scope='One independent data-only explicit-unit-customer audit; not blind/external review or a universal paired-cone bound'),ensure_ascii=False,indent=2))
