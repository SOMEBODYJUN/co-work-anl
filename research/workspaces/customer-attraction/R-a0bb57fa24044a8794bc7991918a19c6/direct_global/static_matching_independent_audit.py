"""Definition-level independent audit; no customer_attraction imports.

Customer multiplicities are expanded into individually indexed unit customers.
All ordered terminal tuples, all ordered decision histories, all topic deviations,
and every optimal target assignment (repetitions allowed a priori) are checked.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import sys

BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'static_matching'/'static_matching_counterexample.json'
OUTPUT=BASE/'static_matching_independent_audit.json'

def main():
 d=json.loads(SOURCE.read_text());raw=d['instance'];k=len(raw['topics']);m=raw['players']
 assert k==6 and m==4
 assert len(set(raw['topics']))==k
 clients=[]
 for row in raw['customers']:
  choices=frozenset(row['topics']);mult=row['multiplicity']
  assert type(mult) is int and mult>0
  assert all(type(a) is int and 0<=a<k for a in choices)
  clients.extend(choices for _ in range(mult))
 assert len(clients)==52
 topic_sets=[frozenset(i for i,c in enumerate(clients) if a in c) for a in range(k)]
 assert len(set(topic_sets))==k, 'six genuinely different coverage sets required'
 rows=d['certificate']['actions'];actions={}
 for row in rows:
  h=tuple(row['history']);a=row['action']
  assert len(h)<m and all(type(b) is int and 0<=b<k for b in h)
  assert type(a) is int and 0<=a<k
  assert h not in actions, 'duplicate decision history'
  actions[h]=a
 histories=[h for dep in range(m) for h in product(range(k),repeat=dep)]
 assert set(actions)==set(histories)
 assert len(histories)==259
 def finish(prefix):
  path=tuple(prefix)
  while len(path)<m:path=path+(actions[path],)
  return path
 def pay(path):
  assert len(path)==m
  ans=[Fraction(0) for _ in path]
  for client in clients:
   interested=[i for i,a in enumerate(path) if a in client]
   if interested:
    share=Fraction(1,len(interested))
    for i in interested:ans[i]+=share
  return tuple(ans)
 def welfare(path):return sum(any(a in client for a in path) for client in clients)
 actual=finish(());u=pay(actual);W=welfare(actual)
 assert actual==(3,3,2,2) and list(actual)==d['actual']
 assert u==(Fraction(47,4),)*4 and list(map(str,u))==d['payoffs']
 assert W==47==d['welfare'] and sum(u)==W
 counts=tuple(Counter(actual)[a] for a in range(k))
 assert list(counts)==d['certificate']['terminal_counts']
 minslack=None;ties=0;checks=0;strict=0
 for h in histories:
  i=len(h);eq=pay(finish(h))[i]
  for a in range(k):
   alternative=finish(h+(a,));dev=pay(alternative)[i];slack=eq-dev
   if minslack is None or slack<minslack:minslack=slack
   assert slack>=0,(h,a,eq,dev,alternative)
   ties+=int(slack==0);strict+=int(slack>0);checks+=1
 all_terminal=list(product(range(k),repeat=m))
 OPT=max(map(welfare,all_terminal))
 optimal=[z for z in all_terminal if welfare(z)==OPT]
 supports=sorted(set(tuple(sorted(set(z))) for z in optimal))
 assert OPT==52==d['optimum']
 assert supports==[(0,1,4,5)]
 assert len(optimal)==24 and all(len(set(z))==4 for z in optimal)
 queries=[]
 for target in optimal:
  value=Fraction(0)
  for i,a in enumerate(target):
   frozen=list(actual);frozen[i]=a
   value+=pay(tuple(frozen))[i]
  queries.append((target,value))
 minimum=min(value for _,value in queries)
 assert minimum==48==Fraction(d['minimum_query']) and minimum>W
 assert sorted((tuple(r['target']),Fraction(r['query'])) for r in d['all_assignments'])==sorted(queries)
 assert (tuple(d['minimum_assignment']),minimum) in queries
 matrix=[]
 for i in range(m):
  row=[]
  for a in (0,1,4,5):
   frozen=list(actual);frozen[i]=a;row.append(str(pay(tuple(frozen))[i]))
  matrix.append(row)
 summary={
  'status':'passed_independently_from_expanded_unit_customers',
  'source':str(SOURCE.relative_to(BASE.parent)),
  'unit_customers':len(clients),'different_topics':k,'players':m,
  'decision_histories':len(histories),'deviation_checks_including_self':checks,
  'minimum_spe_slack':str(minslack),'tied_checks':ties,'strict_checks':strict,
  'actual':actual,'payoffs':list(map(str,u)),'welfare':W,
  'all_ordered_terminal_tuples':len(all_terminal),'optimum':OPT,
  'optimal_ordered_tuples_including_repetition_check':len(optimal),
  'unique_optimal_supports':supports,
  'static_query_columns':[0,1,4,5],'static_query_matrix':matrix,
  'query_sum_distribution':dict(sorted(Counter(str(v) for _,v in queries).items())),
  'minimum_static_matching_query_sum':str(minimum),
  'queries':[{'target':target,'query':str(value)} for target,value in queries],
  'scope':'Auxiliary static frozen-continuation matching bridge is false; half-coverage target is not refuted.'
 }
 OUTPUT.write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='queries'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
