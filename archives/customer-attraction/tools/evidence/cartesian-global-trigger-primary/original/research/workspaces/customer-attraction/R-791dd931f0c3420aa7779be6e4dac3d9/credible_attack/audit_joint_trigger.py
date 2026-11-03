"""Independent finite exact audit; no customer_attraction or scipy imports.
Rebuilds local outcome sets from generic customer incidence and checks the
stored finite LP dual on every script (including all empty-action scripts),
then checks the exact positive mixture that contains a locally >2 bad script.
This is a finite audit, not an all-input HALF proof or half counterexample.
"""
from fractions import Fraction as F
from itertools import product,combinations
from functools import lru_cache
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
REPORT=HERE/'joint_trigger_overlap_probe.json'

def independent_local(data):
 p=len(data['topics']);m=data['players']
 customers=[(tuple(row['topics']),row['multiplicity']) for row in data['customers']]
 @lru_cache(None)
 def payoff(q):
  u=[F(0)]*p
  for support,size in customers:
   load=sum(q[j] for j in support)
   if load:
    for j in support:
     if q[j]:u[j]+=F(size,load)
  return tuple(u)
 @lru_cache(None)
 def welfare(q):return sum(size for support,size in customers if any(q[j] for j in support))
 @lru_cache(None)
 def children(k):
  if sum(k)==m:return frozenset([k])
  ch=[children(k[:a]+(k[a]+1,)+k[a+1:]) for a in range(p)]
  theta=max(min(payoff(q)[a] for q in s) for a,s in enumerate(ch))
  return frozenset(q for a,s in enumerate(ch) for q in s if payoff(q)[a]>=theta)
 @lru_cache(None)
 def floor(k):
  assert sum(k)<m
  return max(min(payoff(q)[a] for q in children(k[:a]+(k[a]+1,)+k[a+1:])) for a in range(p))
 optimum=max(sum(size for support,size in customers if any(j in selected for j in support)) for selected in combinations(range(p),min(p,m)))
 def script(path):
  q=tuple(path.count(a) for a in range(p));u=payoff(q);prefix=[0]*p;g=[]
  for a in path:g.append(u[a]-floor(tuple(prefix)));prefix[a]+=1
  return tuple(g),welfare(q),optimum
 return p,m,script

def main():
 report=json.loads(REPORT.read_text());beta=F(report['finite_exact_dual']['beta'])
 lam=[F(report['finite_exact_dual']['lambda_by_player'].get(str(i+1),'0')) for i in range(5)]
 assert min(lam)>=0
 local={};checked=0;retained=0;dedup=set();minimum=None
 for name,data in report['inputs'].items():
  p,m,script=independent_local(data);assert m==5;local[name]=script
  for path in product(range(p),repeat=m):
   g,w,o=script(path);checked+=1
   # For arbitrary paths last mover's gap is nonpositive. No nonnegative
   # feasible mix can contain a strictly negative last gap, with positive mass.
   assert g[-1]<=0
   if g[-1]<0:continue
   retained+=1;dedup.add(g+(w,o))
   slack=beta*w-o-sum(x*y for x,y in zip(lam,g))
   assert slack>=0,(name,path,slack)
   minimum=slack if minimum is None else min(minimum,slack)
 assert len(dedup)==report['columns']
 def verify_mix(mix):
  gs=[F(0)]*5;w=o=F(0);bad=0;not_local=0
  for row in mix['weights']:
   x=F(row['weight']);assert x>0
   g,ww,oo=local[row['source']](tuple(row['path']))
   assert (tuple(map(F,row['gaps'])),row['w'],row['o'])==(g,ww,oo)
   for i,v in enumerate(g):gs[i]+=x*v
   w+=x*ww;o+=x*oo
   bad+=oo>2*ww;not_local+=any(t<0 for t in g)
  assert w==1 and min(gs)>=0
  assert list(map(str,gs))==mix['aggregate_gaps'] and str(o)==mix['ratio']
  return {'ratio':str(o),'aggregate_gaps':list(map(str,gs)),'locally_more_than_two_scripts':bad,'locally_non_SPE_scripts':not_local}
 primal=verify_mix(report['finite_exact_optimal_primal']);assert F(primal['ratio'])==beta
 mixed=verify_mix(report['nonlocal_path_mixture']);assert mixed['locally_more_than_two_scripts']>0 and mixed['locally_non_SPE_scripts']>0
 out={'status':'independent exact finite audit passed; no universal bound','input_games':len(local),'all_local_scripts':checked,'last_BR_scripts':retained,'deduplicated_columns':len(dedup),'exact_dual_beta':str(beta),'minimum_exact_dual_slack':str(minimum),'optimal_primal':primal,'nonlocal_mixture':mixed,'input_sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (HERE/'joint_trigger_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
