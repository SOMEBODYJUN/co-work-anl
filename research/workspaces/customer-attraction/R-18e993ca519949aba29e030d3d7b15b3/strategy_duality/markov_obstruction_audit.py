#!/usr/bin/env python3
"""Exact complete finite counterexample to count-Markov welfare reduction.

This is not a counterexample to Q-CAG-HALF. No canonical solver imports.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from functools import lru_cache
import json
from pathlib import Path

P=5; MPLAY=3
PAIR=[0,1,1,0,1,1,0,1,1,0]
TRIPLE=[0,0,1,1,1,1,0,1,1,1]
F={frozenset(q):v for t,vs in ((2,PAIR),(3,TRIPLE)) for q,v in zip(combinations(range(P),t),vs)}

def us(q,a):return F[q]-F[q-{a}]
def acts(q):return tuple(a for a in range(P) if a not in q)
def mask(q):return sum(1<<a for a in q)
def fmt(q):return ''.join(str(a) for a in sorted(q))

def compile_exact():
 table=[F.get(frozenset(a for a in range(P) if b>>a&1),0) for b in range(1<<P)]
 c=table[:]
 for a in range(P):
  for b in range(1<<P):
   if b>>a&1:c[b]-=c[b^(1<<a)]
 z=[0]+[(-1)**(b.bit_count()+1)*b.bit_count()*c[b] for b in range(1,1<<P)]
 x=z[:]
 for a in range(P):
  for b in range(1<<P):
   if not b>>a&1:x[b]-=x[b|(1<<a)]
 x[0]=0
 # independently check every Boolean potential entry
 H=[Q(0)]+[sum((Q(1,j) for j in range(1,d+1)),Q(0)) for d in range(1,P+1)]
 for s in range(1<<P):assert sum((x[b]*H[(b&s).bit_count()] for b in range(1,1<<P)),Q(0))==table[s]
 magnitude=sum(map(abs,x));K=4*magnitude+1
 r=[0]+[x[b]+K for b in range(1,1<<P)]
 assert min(r[1:])>=1
 return table,x,magnitude,K,r

@lru_cache(None)
def full_R(k):
 if len(k)==MPLAY:return frozenset([k])
 aa=acts(k);child={a:full_R(k|{a}) for a in aa}
 floor=max(min(us(q,a) for q in child[a]) for a in aa)
 return frozenset(q for a in aa for q in child[a] if us(q,a)>=floor)

def fresh_certificate(target):
 policy={}
 def visit(h,q):
  if len(h)==MPLAY:return
  k=frozenset(h);aa=acts(k);child={a:full_R(k|{a}) for a in aa}
  floor=max(min(us(z,a) for z in child[a]) for a in aa)
  a=next(a for a in aa if q in child[a] and us(q,a)>=floor)
  policy[h]=a
  for b in aa:
   qb=q if b==a else min(child[b],key=lambda z:(us(z,b),tuple(sorted(z))))
   visit(h+(b,),qb)
 visit((),target)
 return policy

def all_markov_roots():
 """Exhaust every common unordered-pair reply and every one-theme reply.

 Last-player preferences only depend on unordered pair. Once these are fixed,
 each first-theme node's optimal actions are determined. Their independent
 choices exhaust all remaining count policies. Root chooses any best action.
 """
 pairs=list(map(frozenset,combinations(range(P),2)))
 menus={k:tuple(a for a in acts(k) if us(k|{a},a)==max(us(k|{b},b) for b in acts(k))) for k in pairs}
 roots=set();last_count=0;second_count=0;last_records=[]
 for seq in product(*(menus[k] for k in pairs)):
  last_count+=1;last=dict(zip(pairs,seq));second={}
  for a in range(P):
   aa=acts(frozenset([a]));vals={b:us(frozenset([a,b,last[frozenset([a,b])]]),b) for b in aa}
   second[a]=tuple(b for b in aa if vals[b]==max(vals.values()))
  local=set()
  for bs in product(*(second[a] for a in range(P))):
   second_count+=1
   terminal={a:frozenset([a,bs[a],last[frozenset([a,bs[a]])]]) for a in range(P)}
   values={a:us(terminal[a],a) for a in range(P)}
   best=max(values.values())
   local.update(terminal[a] for a in range(P) if values[a]==best)
  roots.update(local)
  last_records.append({'last':{fmt(k):last[k] for k in pairs},'roots':sorted(fmt(q) for q in local)})
 return roots,last_count,second_count,last_records

def main():
 table,x,magnitude,K,r=compile_exact()
 def U(z,a):
  return sum((Q(r[b],sum(bool(b>>c&1) for c in z)) for b in range(1,1<<P) if b>>a&1),Q(0))
 def W(q):return sum(r[b] for b in range(1,1<<P) if b&mask(q))
 bias=Q((1<<P)-(1<<(P-MPLAY)),MPLAY)
 baseline=K*((1<<P)-(1<<(P-MPLAY)))
 # Every distinct triple action gets exactly the same additive bias.
 for q in map(frozenset,combinations(range(P),MPLAY)):
  for a in q:assert U(tuple(q),a)==us(q,a)+K*bias
  assert W(q)==baseline+sum(us(q,a) for a in q)
 # Direct finite boundary proof: at any last prefix every old action is worse
 # than every fresh action; at depth 1 old current moves are worse under all
 # possible fresh last continuations. This does not assume Markov tie choices.
 last_gaps=[]
 for h in product(range(P),repeat=2):
  aa=acts(frozenset(h));old=set(h)
  for a in aa:
   for b in old:last_gaps.append(U(h+(a,),a)-U(h+(b,),b))
 assert min(last_gaps)>0
 second_gaps=[]
 for a in range(P):
  worst_old=max(U((a,a,b),a) for b in range(P) if b!=a)
  best_bound=min(U((a,b,c),b) for b in range(P) if b!=a for c in range(P) if c not in (a,b))
  second_gaps.append(best_bound-worst_old)
 assert min(second_gaps)>0
 target=frozenset([0,2,3]);policy=fresh_certificate(target)
 for a in range(P):policy[a,a]=max(range(P),key=lambda b:(U((a,a,b),b),-b))
 assert set(policy)=={h for d in range(3) for h in product(range(P),repeat=d)}
 check_count=0
 def verify(h):
  nonlocal check_count
  if len(h)==3:return h
  ends={a:verify(h+(a,)) for a in range(P)};a=policy[h];own=U(ends[a],a)
  for b in range(P):assert own>=U(ends[b],b);check_count+=1
  return ends[a]
 root=verify(())
 assert frozenset(root)==target
 roots,last_count,second_count,records=all_markov_roots()
 full=full_R(frozenset())
 assert target in full and target not in roots
 assert min(W(q) for q in full)<min(W(q) for q in roots)
 report={'identity':'count-Markov root outcome and worst-welfare reduction counterexample; not half-coverage counterexample',
  'players':3,'topics':list(range(P)),'F_boolean':table,'signed_types':x[1:],'M':magnitude,'K':K,'legal_types':r[1:],
  'total_unit_customers':sum(r),'baseline_distinct_coverage':baseline,
  'full_policy':{','.join(map(str,h)):a for h,a in sorted(policy.items(),key=lambda z:(len(z[0]),z[0]))},
  'root_path':root,'root_payoffs':[str(U(root,a)) for a in root],'root_welfare':W(target),'OPT':max(W(frozenset(q)) for q in combinations(range(P),3)),
  'all_full_SPE_root_sets':sorted(fmt(q) for q in full),'all_count_Markov_SPE_root_sets':sorted(fmt(q) for q in roots),
  'full_min_welfare':min(W(q) for q in full),'Markov_min_welfare':min(W(q) for q in roots),
  'Markov_last_maps_exhausted':last_count,'Markov_second_maps_exhausted':second_count,'complete_SPE_comparisons':check_count,
  'minimum_last_old_fresh_gap':str(min(last_gaps)),'minimum_second_old_fresh_gap':str(min(second_gaps)),
  'Markov_last_map_results':records}
 out=Path(__file__).with_name('markov_obstruction_report.json')
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('Markov_last_map_results','full_policy','F_boolean','signed_types','legal_types')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
