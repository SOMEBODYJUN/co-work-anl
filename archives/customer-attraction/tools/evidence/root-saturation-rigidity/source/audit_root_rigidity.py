"""Exact audit of a general root-to-terminal rigidity inequality.
No source code from the discovery LP or its pricing evaluators is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,sys

def share(num,den):return F(num,den) if num else F(0)

def residual(m,p,n,z,q):
 c=p+n+z
 lhs=F(q,1+(m-1)*p)-F(q,1+p+n)+share(z-p,c)
 rhs=F(n-(m-2)*p,2)+(z-p)+m*(m-2)*(share(p,c)-F(p,m))
 return rhs-lhs

def audit_local():
 cases=0
 for m in range(2,101):
  for p,n,z,q in product((0,1),range(m-1),(0,1),(0,1)):
   rr=residual(m,p,n,z,q)
   assert rr>=0,(m,p,n,z,q,rr)
   if p==1 and q==0 and z==0:
    assert rr==F((n+1-(m-1))*(n+1-2*(m-1)),2*(n+1))
   if p==1 and q==0 and z==1:
    assert rr==F((m-2-n)*(2*m-n-6),2*(n+2))
   cases+=1
 return {'scope':'Exact arithmetic implementation audit at m=2,...,100; all-m proof is the four-case factorization in root_rigidity.md','cases':cases}

def audit_point(path):
 raw=path.read_bytes();d=json.loads(raw);names='ABCDEUVWXY';at=[]
 for a in d['atoms']:
  mass=F(a['exact_mass']);bits=tuple(map(int,a['bits']));at.append((bits,mass))
 u=sum((mass*share(bits[0],sum(bits[:5])) for bits,mass in at),F(0))
 sizes={n:sum((mass*bits[j] for bits,mass in at),F(0)) for j,n in enumerate(names)}
 rows=[]
 for j,T in enumerate(names):
  for k,Q in enumerate(names):
   f=sum((mass*F(bits[k],1+4*bits[j]) for bits,mass in at),F(0))
   delta=5*u-sizes[T];slack=u+F(11,2)*delta-f
   rows.append({'T':T,'Q':Q,'root_size_slack':str(delta),'rigidity_slack':str(slack),'rigidity_slack_float':float(slack)})
 rows.sort(key=lambda r:F(r['rigidity_slack']))
 return {'source':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'scope':'Frozen necessary-condition point; not an SPE or counterexample','root_profit':str(u),'fixed_pairs_checked':len(rows),'negative_rows':sum(F(r['rigidity_slack'])<0 for r in rows),'minimum':rows[0],'saturated_topic_names':[n for n,s in sizes.items() if s==5*u],'all_negative_rows':[r for r in rows if F(r['rigidity_slack'])<0]}

if __name__=='__main__':
 here=Path(__file__).resolve().parent;root=next(p for p in here.parents if (p/'AGENTS.md').exists())
 default=root/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_primal_overlap1.json'
 paths=[Path(x) for x in sys.argv[1:]] or [default]
 out={'local_algebra_audit':audit_local(),'points':[audit_point(p) for p in paths]}
 here.joinpath('audit_root_rigidity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
