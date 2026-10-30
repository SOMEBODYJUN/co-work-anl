from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,ast,hashlib,platform,time
c=Path(__file__).resolve().parent
source=c/'tests/audits/unrelated_machines/independent_set_big_residual_audit.py'
tr=ast.parse(source.read_text());params=[]
for n in ast.walk(tr):
 if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [getattr(x,'id','') for x in n.target.elts]==['q','r']:params=ast.literal_eval(n.iter)
assert params==((3,0),(3,1),(4,2))
def opt(n,edges,k,h,r):
 jobs=[[(i,F(1)) for i in range(n)] for _ in range(k)]
 jobs += [[(i,h)] for i in range(n) for _ in range(r)]
 jobs += [[(u,h),(v,h)] for u,v in edges]
 rows=[]
 for a in product(*jobs):
  load=[F(0)]*n
  for i,p in a:load[i]+=p
  rows.append((max(load,default=F(0)),load))
 return min(v for v,_ in rows),len(rows)
cases=[]
for name,n,es,k,h,r in [('zero-private-endpoint-cap',1,[],2,F(2),0),('actual-third-main-parameter',3,[(0,1),(1,2),(0,2)],2,F(1,4),2),('zero-macro-excluded-from-positive-yes',1,[],0,F(1,3),0)]:
 val,total=opt(n,es,k,h,r);alpha=1+r*h
 cases.append(dict(name=name,n=n,edges=es,k=k,h=str(h),r=r,alpha=str(alpha),opt=str(val),assignments=total,old_uncapped_alpha_plus_h=str(alpha+h),corrected_lower=str(alpha+min(F(1),h)) if name!='zero-macro-excluded-from-positive-yes' else None))
assert F(cases[0]['opt'])==2<3 and F(cases[1]['opt'])==F(7,4) and F(cases[2]['opt'])==0
out=dict(scope='Three new literal boundary checks; original 1080-instance main not executed',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),actual_main_parameters=params,historical_report_scope='incorrectly claims q=3 for every r=0,1,2',static_instance_count=sum([1*2,2*3,8*4,64*5])*3,cases=cases,python=platform.python_version())
(c/'independent-residual-boundary-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
