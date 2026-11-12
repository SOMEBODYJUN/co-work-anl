"""Saved copy of the inline fixed-input verification executed by this task's worker.

The executable body below is copied from the successful inline invocation. It
independently checks the two assigned saved inputs and their existing JSON
certificates; it does not invoke the original probe CLI or audit script.
Run from the repository root.
"""
import json,math,itertools
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
root=Path('archives/customer-attraction/tools/evidence/matroid-bundle-four-boss3')
report=json.loads((root/'fixed-best-exact-audit.json').read_text())
cases=[(4,[[11],[492],[21],[108,286,392],[152],[199],[25]],{1:1,2:1,4:1,8:3,16:1,32:1,64:1}), (5,[[913],[343,575,934],[605],[971],[625],[325,521],[206]],{1:1,2:2,4:1,8:1,16:1,32:2,66:1})]
def rank(vs):
 basis={}
 for v in vs:
  while v:
   p=v.bit_length()-1
   if p in basis:v^=basis[p]
   else:basis[p]=v;break
 return len(basis)
def comps(n,k):
 if k==1:yield(n,);return
 for i in range(n+1):
  for rest in comps(n-i,k-1):yield(i,)+rest
for m,bundles,types in cases:
 k=len(bundles); L=math.lcm(*range(1,m+1)); data=report['results'][m-3]
 C=[rank(v for a in range(k) if mask>>a&1 for v in bundles[a]) for mask in range(1<<k)]
 cov=[sum(w for b,w in types.items() if mask&b) for mask in range(1<<k)]
 assert C==cov==data['all_rank_values']
 @lru_cache(None)
 def pay(q,a):
  return sum(w*(L//sum(q[b] for b in range(k) if mask>>b&1)) for mask,w in types.items() if mask>>a&1)
 def welfare(q):return C[sum((1<<a) for a in range(k) if q[a])]
 @lru_cache(None)
 def solve(q):
  if sum(q)==m:return frozenset([q])
  children=[]
  for a in range(k):
   x=list(q);x[a]+=1;children.append(solve(tuple(x)))
  theta=max(min(pay(s,a) for s in children[a]) for a in range(k))
  return frozenset(s for a in range(k) for s in children[a] if pay(s,a)>=theta)
 outcomes=solve((0,)*k);worst=min(outcomes,key=lambda q:(welfare(q),q));minW=welfare(worst)
 assert minW==data['minimum_welfare'];assert len(outcomes)==data['root_outcomes'];assert solve.cache_info().currsize==data['DP_states']
 # Independent player-coalition Shapley formula, preserving player positions and repetitions.
 occupied=0
 for q in comps(m,k):
  actions=tuple(a for a,n in enumerate(q) for _ in range(n))
  for a in range(k):
   if not q[a]:continue
   occupied+=1;i=actions.index(a);others=[j for j in range(m) if j!=i];value=F(0)
   for sm in range(1<<(m-1)):
    chosen=[others[j] for j in range(m-1) if sm>>j&1]
    mask=sum(set(1<<actions[j] for j in chosen));z=len(chosen)
    value+=F(math.factorial(z)*math.factorial(m-z-1),math.factorial(m))*(C[mask|1<<a]-C[mask])
   assert value==F(pay(q,a),L)
 assert occupied==data['occupied_payoff_checks']
 name='matroid_k7_m4_d9-new-full-strategy.json' if m==4 else 'matroid_k7_m5_d10-new-full-strategy.json'
 raw=json.loads((root/name).read_text());rows=raw['actions'];policy={tuple(row['history']):row['action'] for row in rows}
 histories={h for d in range(m) for h in itertools.product(range(k),repeat=d)}
 assert len(policy)==len(rows)==len(histories)==data['new_certificate_histories'];assert set(policy)==histories
 assert all(type(a)==int and 0<=a<k for a in policy.values())
 def complete(h):
  while len(h)<m:h=h+(policy[h],)
  return h
 def own(h,i):
  q=tuple(h.count(a) for a in range(k));return pay(q,h[i])
 checks=strict=0;slack=[]
 for h in sorted(histories,key=lambda h:(len(h),h)):
  actual=complete(h);i=len(h)
  for a in range(k):
   diff=own(actual,i)-own(complete(h+(a,)),i);assert diff>=0;slack.append(F(diff,L));strict+=diff>0;checks+=1
 assert checks==data['full_action_comparisons'];assert strict==data['strict_comparisons'];assert min(slack)==F(data['minimum_IC_slack'])
 actual=complete(());assert list(actual)==data['new_certificate_actual_path']
 assert tuple(actual.count(a) for a in range(k))==worst
 p=list(map(F,data['stored_query_rationalized']));assert sum(p)==1 and min(p)>=0
 backgrounds=list(comps(m-1,k))
 def query(b,a):
  q=list(b);q[a]+=1;return F(pay(tuple(q),a),L)
 guarantees=[sum(p[a]*query(b,a) for a in range(k)) for b in backgrounds]
 assert len(backgrounds)==data['static_backgrounds'];assert sorted(guarantees)==sorted(map(F,data['query_guarantees']))
 dual=data['exact_dual_backgrounds'];assert sum(F(d['probability']) for d in dual)==1
 assert all(len(d['counts'])==k and sum(d['counts'])==m-1 and min(d['counts'])>=0 and F(d['probability'])>=0 for d in dual)
 upper=[sum(F(d['probability'])*query(tuple(d['counts']),a) for d in dual) for a in range(k)]
 assert upper==list(map(F,data['exact_dual_pure_query_values']))
 v=F(data['exact_security']);assert min(guarantees)==max(upper)==v
 OPT=max(welfare(q) for q in comps(m,k));assert OPT==data['point_OPT_m'];assert F(minW)-m*v==F(data['exact_gap'])
 if m==4:
  analytic=[F(3,4*(a+1))+F(9+a,16) for a in range(4)];assert min(analytic)==v
 else:
  analytic=[(a,b,F(4,5*(a+1))+F(2,5*(b+1))+F(4+a+b,15)) for a in range(5) for b in range(5-a)];assert min(z for a,b,z in analytic)==v
 print(json.dumps({'m':m,'rank_and_coverage_values_checked':len(C),'all_root_outcomes':[list(q) for q in sorted(outcomes)],'minimum_welfare':minW,'BI_states':solve.cache_info().currsize,'Shapley_position_checks':occupied,'strategy_rows_parsed':len(rows),'IC_comparisons':checks,'IC_strict':strict,'actual_path':actual,'backgrounds':len(backgrounds),'query_min':str(min(guarantees)),'dual_pure_query_values':[str(x) for x in upper],'OPT':OPT,'gap':str(F(minW)-m*v),'analytic_lower_bound':str(min(analytic) if m==4 else min(z for a,b,z in analytic))},ensure_ascii=False))
