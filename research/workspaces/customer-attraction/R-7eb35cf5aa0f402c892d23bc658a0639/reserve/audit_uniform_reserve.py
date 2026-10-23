"""Exact finite audit of a general proof, not a search proof of Q-CAG-HALF.

Catalog coverage is deduplicated. All tail SPE outcomes come from the canonical
set-valued recurrence; payoffs are recomputed independently from expanded unit
customers using Fraction. No fixed tie selector is used.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,time
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/model.py').is_file());sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,ExactSPESolver

def build(k,t,x,a,b,d,extra=(),remaining=None,deviate=True):
 blocks={}
 for i in range(k):
  blocks[f'X{i}']={f'x{i}:{j}' for j in range(x)}
  blocks[f'Y{i}']={f'y{i}:{j}' for j in range(a)}
 for s in range(t):
  blocks[f'Z{s}']={f'z{s}:{j}' for j in range(b)}
  blocks[f'V{s}']={f'v{s}:{j}' for j in range(d)}
 topics={}
 for i in range(k):
  topics[f'A{i}']=blocks[f'X{i}']|blocks[f'Y{i}']
  topics[f'C{i}']=blocks[f'X{i}']
  for s in range(t):topics[f'B{i}.{s}']=blocks[f'X{i}']|blocks[f'Z{s}']
 for s in range(t):topics[f'D{s}']=blocks[f'Z{s}']|blocks[f'V{s}']
 coverage=[];labels=[];ids={}
 for label,covered in topics.items():
  frozen=frozenset(covered)
  if frozen not in coverage:coverage.append(frozen);labels.append(label)
  ids[label]=coverage.index(frozen)
 prefix=tuple(ids[f'C{i}'] for i in range(k-1))+(ids[f'A{k-1}' if deviate else f'C{k-1}'],)+tuple(ids[s] for s in extra)
 n=t if remaining is None else remaining
 I=Instance.from_topic_sets(coverage,players=len(prefix)+n,labels=labels)
 units=[]
 for c in I.customers:units.extend([c.topics]*c.multiplicity)
 return I,prefix,ids,units,coverage

def unit_payoffs(q,units):
 out=[F(0) for _ in q]
 for accepted in units:
  count=sum(q[z] for z in accepted)
  if count:
   for z in accepted:
    if q[z]:out[z]+=F(1,count)
 return tuple(out)

def tail_case(k,t,x,a,b,d,extra=(),remaining=None,deviate=True):
 I,prefix,ids,units,cov=build(k,t,x,a,b,d,extra,remaining,deviate)
 before=I.counts(prefix);n=I.players-len(prefix);H=F(b+d)
 qfresh=sum(not any(before[ids[f'D{s}']] or before[ids[f'B{i}.{s}']] for i in range(k)) for s in range(t))
 assert qfresh>=n and d>=F(x,2) and a+F(x,2)<=H
 E=ExactSPESolver(I);outcomes=E.outcomes(before);minimum_deviator=None
 for terminal in outcomes:
  pay=unit_payoffs(terminal,units)
  assert pay==I.topic_payoffs(terminal)
  for z in range(I.topic_count):
   if terminal[z]>before[z]:assert pay[z]==H,(prefix,terminal,z,pay[z],H)
  if deviate:
   got=pay[ids[f'A{k-1}']]
   minimum_deviator=got if minimum_deviator is None else min(minimum_deviator,got)
   assert got>=a+F(x,2)
   assert terminal[ids[f'A{k-1}']]==before[ids[f'A{k-1}']]
   assert sum(terminal[ids[f'B{k-1}.{s}']]-before[ids[f'B{k-1}.{s}']] for s in range(t))<=1
 return {'k':k,'t':t,'x':x,'a':a,'b':b,'d':d,'extra':list(extra),'remaining':n,'prefix':list(prefix),'fresh':qfresh,'tail_outcomes':len(outcomes),'count_states':E.stats.count_states,'terminal_states':E.stats.terminal_states,'tail_utility':str(H),'minimum_deviator_utility':str(minimum_deviator) if minimum_deviator is not None else None,'required_deviator_bound':str(a+F(x,2)) if deviate else None,'checked_every_attainable_tail_outcome':True,'deduplicated_catalog_topics':I.topic_count}

def whole_case(k,t,x,a,b,d):
 I,pre,ids,units,cov=build(k,t,x,a,b,d,remaining=0,deviate=False)
 I=Instance.from_topic_sets(cov,players=k+t,labels=I.topics)
 target=tuple(ids[f'C{i}'] for i in range(k))+tuple(ids[f'D{s}'] for s in range(t))
 E=ExactSPESolver(I);q=I.counts(target,terminal=True);possible=q in E.outcomes()
 if possible:
  # Counts alone do not force this order. Explicitly request the ordered path.
  try:E.certificate(on_path=target);ordered=True
  except ValueError:ordered=False
 else:ordered=False
 W=I.welfare(q);O=I.optimal_welfare()
 assert O==k*(x+a)+t*(b+d)
 if a>F(x,2):assert not ordered
 return {'k':k,'t':t,'x':x,'a':a,'b':b,'d':d,'candidate_W':W,'OPT':O,'candidate_ratio':str(F(O,W)),'candidate_counts_possible':possible,'candidate_ordered_path_possible':ordered,'all_SPE_outcome_count':len(E.outcomes())}

start=time.monotonic();tails=[]
for k,t in [(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,2),(2,3),(3,2)]:
 tails.append(tail_case(k,t,6,4,4,3))
# Nontrivial occupied-bait prefixes and arbitrary extra A/C histories.
for extra,remaining in [(('B0.0',),2),(('D0',),2),(('A0','C0','B0.0'),2),(('B0.0','D1'),1)]:
 tails.append(tail_case(2,3,6,4,4,3,extra,remaining))
# Duplicate coverage when a=0 is genuinely deduplicated.
tails.append(tail_case(2,3,2,0,1,1,deviate=False))
whole=[whole_case(k,t,6,a,4,3) for k,t,a in [(1,1,4),(1,2,4),(1,3,4),(2,2,4),(2,3,4),(1,2,3),(2,2,3)]]
data={'scope':'finite exact audit of uniform independent-reserve obstruction; general theorem rests on written induction, no Q-CAG-HALF resolution','seed':None,'deterministic_parameters':True,'tails':tails,'whole_games':whole,'elapsed_seconds':time.monotonic()-start,'independent_payoff_arithmetic':'Fraction over expanded distinct unit customers','strategy_scope':'all pure full-history SPE tail outcome sets; no fixed tie selector'}
# Replay leaves the frozen JSON intact; data remains available to runpy.
print(json.dumps({'tail_cases':len(tails),'tail_outcomes_checked':sum(z['tail_outcomes'] for z in tails),'whole_game_cases':len(whole),'elapsed_seconds':data['elapsed_seconds'],'all_assertions_passed':True}))
