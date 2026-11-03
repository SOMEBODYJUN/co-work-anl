"""Exact fixed-record arithmetic, no LP/BI/random process or original import.

Checks saved necessary relaxations and terminal witness payoffs. It does not
assert that an archived witness leaf belongs to the claimed SPE outcome set.
"""
import ast, json, math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from collections import Counter
import hashlib

HERE=Path(__file__).resolve().parent
MAN=json.loads((HERE/'source-manifest.json').read_text())
SRC=HERE/'original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/counter'
def read(n):return json.loads((SRC/n).read_text())
def dot(a,b):return sum((v*w for v,w in zip(a,b)),F(0))
def serial(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [serial(v) for v in x]
 return x
def rows_for(types,path,p):
 q=[path.count(a) for a in range(p)];rows=[];labels=[]
 for i,a in enumerate(path):
  old=[path[:i].count(b) for b in range(p)];r=len(path)-i
  for t in range(p):
   vals=[]
   for typ in types:
    actual=F(1,sum(q[b] for b in typ)) if a in typ else F(0)
    alt=F(1,sum(old[b] for b in typ)+r) if t in typ else F(0)
    vals.append(actual-alt)
   rows.append(vals);labels.append((i+1,t))
 return rows,labels
def standard_types(path):
 n=max(path)+1;edges=list(combinations(range(5),2))
 types=[tuple(a for a in range(n) if S>>a&1)+(n+j,) for S in range(1,1<<n) for j in range(5)]
 types +=[(n+j,)+tuple(n+5+k for k,e in enumerate(edges) if j in e) for j in range(5)]
 return types
def necessary_record(d,types,point,p):
 path=d['path'];rows,labels=rows_for(types,path,p);lookup={tuple(t):i for i,t in enumerate(types)}
 x=[F(0)]*len(types)
 for typ,v in point:x[lookup[tuple(typ)]]=F(v)
 n=max(path)+1;W=[F(any(a<n for a in t)) for t in types];L=[1-v for v in W]
 assert min(x)>=0 and dot(W,x)==1 and min(dot(r,x) for r in rows)>=0
 mu=[F(0)]*len(rows)
 for lab,v in d['dual']:mu[labels.index(tuple(lab))]=F(v)
 beta=F(d['beta']);res=[beta*W[j]-sum(mu[i]*rows[i][j] for i in range(len(rows)))-L[j] for j in range(len(types))]
 assert min(mu)>=0 and min(res)>=0 and dot(L,x)==beta
 return {'types':len(types),'security_rows':len(rows),'positive_point':sum(v>0 for v in x),
  'beta':beta,'W':dot(W,x),'L':dot(L,x),'minimum_primal_slack':min(dot(r,x) for r in rows),
  'minimum_dual_residual':min(res),'all_saved_primal_dual_flags_true':d['primal_exact'] and d['dual_exact'],'residual':res}
def path_records():
 out=[]
 for d in read('path_incidence_obstruction.json'):
  path=d['path'];types=[tuple(t) for t in d['types']];n=max(path)+1;q=[path.count(a) for a in range(n)];rows=[]
  for i,a in enumerate(path):
   old=[path[:i].count(b) for b in range(n)];r=5-i;line=[]
   for S,degree in types:
    load=sum(q[b] for b in range(n) if S>>b&1);pref=sum(old[b] for b in range(n) if S>>b&1)
    line.append((F(5,load) if S>>a&1 else F(0))-F(degree,pref+r))
   rows.append(line)
  W=[F(bool(S)) for S,t in types];V=[F(not S)-F(bool(S) and t==0) for S,t in types]
  sparse={tuple(ast.literal_eval(k)):F(v) for k,v in d['point']};x=[sparse.get(t,F(0)) for t in types]
  mu=list(map(F,d['mu']));beta=F(d['beta']);res=[beta*W[j]-sum(mu[i]*rows[i][j] for i in range(5))-V[j] for j in range(len(types))]
  assert min(x)>=0 and dot(W,x)==1 and min(dot(r,x) for r in rows)>=0
  assert min(mu)>=0 and min(res)>=0 and res==list(map(F,d['residual']))
  assert dot(V,x)==F(d['value'])==beta and min(res)==F(d['minimum_residual'])
  out.append({'path':path,'omitted_min_degree':d['minimum_omitted_degree'],'types':len(types),
   'beta':beta,'mu':mu,'all_saved_residuals_match':True,'primal_dual_exact':True})
 return out
def candidate_input(kind):
 if kind=='partial':return [(tuple(t),F(v)) for t,v in read('partial_insured_bank_lp.json')['point']],20
 point=[(tuple(t),F(v)*137) for t,v in read('insurance_security_lp.json')[1]['point']]
 if kind=='cycle':
  edges=[(j,(j+1)%5) for j in range(5)]
  point=[(t if any(a<5 for a in t) else (t[0],)+tuple(10+k for k,e in enumerate(edges) if t[0]-5 in e),v) for t,v in point]
  return point,15
 if kind=='specialist':
  result=[]
  for t,v in point:
   ext=tuple(range(20,23)) if t==(4,5) else tuple(range(23,25)) if t==(4,9) else (20+t[0]-5,) if not any(a<5 for a in t) else ()
   result.append((t+ext,v))
  result.append(((0,6),F(8)));return result,25
 return point,20
def payoff(point,counts,a):
 return sum((v/F(sum(counts[t] for t in typ)) for typ,v in point if a in typ),F(0))
def diagnose_records():
 result=[]
 for kind in ['private','cycle','partial','specialist']:
  d=read('diagnose_'+kind+'_insurance.json');point,p=candidate_input(kind)
  assert all(v.denominator==1 and v>=0 for _,v in point)
  counts=[int(a<5) for a in range(p)];U=[payoff(point,counts,a) for a in range(5)]
  assert sum(v for _,v in point)==d['unit_clients'] and sum(U)==d['target_W']
  assert F(d['target_ratio'])==F(d['target_OPT'],d['target_W'])
  assert d['target_OPT']==d['unit_clients']
  # The five T_i actually cover every input type, proving this OPT bound.
  assert all(any(a in typ for a in range(5,10)) for typ,_ in point)
  assert math.comb(p+5,5)==d['count_states'] and math.comb(p+4,5)==d['terminal_counts']
  for i,x in enumerate(d['prefix_diagnosis']):
   assert F(x['actual_payoff'])==U[i] and x['target_current_passes']==(U[i]>=F(x['threshold']))
   f=x['maximizing_forced'];c=f['one_min_leaf'];a=f['action']
   assert len(c)==p and sum(c)==5 and all(type(v)is int and v>=0 for v in c)
   assert all(c[j]>=int(j<i)+int(j==a) for j in range(p))
   assert payoff(point,c,a)==F(f['min_forced_payoff'])==F(x['threshold'])
  result.append({'kind':kind,'topics':p,'unit_clients':d['unit_clients'],'target_utilities':U,
   'thresholds':[x['threshold'] for x in d['prefix_diagnosis']],
   'all_saved_forced_leaf_payoffs_exactly_match':True,'target_W':sum(U),'OPT':d['target_OPT'],
   'archived_min_SPE_welfare_not_recomputed':d['minimum_SPE_welfare'],
   'current_generator_has_insurance_graph_field':True,'archived_has_insurance_graph_field':'insurance_graph'in d})
 return result
def main():
 fields={}
 def walk(x,c):
  c[type(x).__name__]+=1
  if isinstance(x,dict):
   for k,v in x.items():walk(k,c);walk(v,c)
  elif isinstance(x,list):
   for v in x:walk(v,c)
  elif isinstance(x,float):assert math.isfinite(x)
 for m in MAN:
  p=HERE/'original'/m['path'];assert p.stat().st_size==m['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
  if p.suffix=='.py':ast.parse(p.read_text())
  if p.suffix=='.json':
   x=json.loads(p.read_text());c=Counter();walk(x,c);fields[p.name]={'top_fields':list(x) if isinstance(x,dict) else ['list'],'all_recursive_value_types_consumed':dict(c),'records':len(x) if isinstance(x,list) else None}
 cy=read('cycle_bank_attack.json');cytypes=[tuple(t) for t in cy['types']]
 cycle=necessary_record(cy,cytypes,[(ast.literal_eval(t),v) for t,v in cy['point'].items()],8)
 assert cycle['residual']==list(map(F,cy['residual']))
 insurance=[necessary_record(d,standard_types(d['path']),d['point'],max(d['path'])+16) for d in read('insurance_security_lp.json')]
 partial=read('partial_insured_bank_lp.json');pt,p=candidate_input('partial');rr,_=rows_for([t for t,v in pt],list(range(5)),p);xx=[v for t,v in pt]
 slacks=[dot(r,xx) for r in rr];assert min(slacks)>=0
 W=sum(v for t,v in pt if any(a<5 for a in t));L=sum(v for t,v in pt if not any(a<5 for a in t));insured=sum(v for t,v in pt if any(a<5 for a in t) and any(a>=10 for a in t))
 assert (W,L,insured)==tuple(F(partial[k]) for k in ['W','L','F_insured'])
 alpha=lambda m,q:1-math.prod(F(q*r-1,q*r) for r in range(1,m+1))
 result={'status':'PASS','scope':'fixed-record arithmetic; no LP/BI or game-realization rerun',
  'cycle_necessary_certificate':cycle,'insurance_necessary_certificates':insurance,'path_relaxation_certificates':path_records(),
  'partial_integer_necessary_point':{'W':W,'L':L,'F_insured':insured,'minimum_all_100_security_rows':min(slacks),'insured_exactly_half':2*insured==W},
  'diagnostic_saved_witness_arithmetic':diagnose_records(),'all_JSON_fields_read':fields,
  'alpha_5_5':alpha(5,5),'alpha_5_10':alpha(5,10),
  'source_multiplier_note':'For full J inequality use (1995,2100,2250,2500,3125)/6049; denominator12098 certifies its half.',
  'original_main_LP_BI_random_calls':0}
 (HERE/'saved-arithmetic-audit.json').write_text(json.dumps(serial(result),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(serial({'status':'PASS','path_records':len(result['path_relaxation_certificates']),'path_residual_columns':sum(x['types'] for x in result['path_relaxation_certificates']),'diagnostic_cases':4,'alpha_5_5':alpha(5,5),'alpha_5_10':alpha(5,10),'partial_exactly_half':2*insured==W}),ensure_ascii=False))
if __name__=='__main__':main()
