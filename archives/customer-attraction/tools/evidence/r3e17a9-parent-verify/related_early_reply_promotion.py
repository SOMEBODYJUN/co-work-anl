"""Same source promotes its first true follower; complete two-person tails.
Rows are necessary conditions; projection diagnostics are not SPE instances.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
PAT=tuple(product(range(2),repeat=3))
def sh(n,d):return F(n,d) if n else F()
def phi(b,x,y):return F(x+y,b+1)-F(x*y,(b+1)*(b+2))
def budget(p,a,b,c):return sh(b+c,p+a+b+c)+F(b,(p+a+1)*(p+a+2))
NAMES=['source','oldpair-newpair']
NAMES += [('oldC',q) for q in ('D','E')]
NAMES += [('newE',q) for q in ('T','B','C','D','E','opt','oldB','oldC')+tuple('a'+str(i) for i in range(6))]
NAMES += [('pair',tuple(qs)) for qs in combinations_with_replacement(('T','B','C')+tuple('a'+str(i) for i in range(6)),2)]
NAMES += [('pair','opt'),('pair','Topt'),('pair','Bopt'),('pair','Copt')]
NAMES += [('price',q,i) for q in ('D','E') for i in range(6)]
NAMES += [('capacity',q) for q in ('D','E')]
NAMES += [('actualpair',qs) for qs in (('D','E'),('B','D'),('B','E'),('C','D'),('C','E'),('T','D'),('T','E'))]

def coefficients(a,h,word,de):
 p=sum(a[:3]);ell=sum(a[:5]);s=sum(a);t,b,c=word;D,E=de
 d=sum(n*t for n,(t,b,c) in zip(h,PAT));nb=sum(n*b for n,(t,b,c) in zip(h,PAT));nc=sum(n*c for n,(t,b,c) in zip(h,PAT))
 mem={'T':t,'B':b,'C':c,'D':D,'E':E,'opt':F(d,6),'oldB':F(nb,6),'oldC':F(nc,6)}|{'a'+str(i):a[i] for i in range(6)}
 u4=sh(a[3],s);oldC=sh(c,p+t+b+c);newE=sh(E,p+b+D+E)
 newbudget=budget(p,b,D,E);abudget=budget(p,a[3],a[4],a[5]);v=[]
 for name in NAMES:
  if name=='source':value=u4-sh(b,p+b+D+E)
  elif name=='oldpair-newpair':value=budget(p,t,b,c)-phi(p+t,D,E)
  elif name[0]=='oldC':value=oldC-F(mem[name[1]],p+t+b+1)
  elif name[0]=='newE':value=newE-F(mem[name[1]],p+b+D+1)
  elif name[0]=='pair':
   q=name[1]
   if q=='opt':qphi=F(d,3*(p+b+1))-F(d*(d-1),30*(p+b+1)*(p+b+2))
   elif isinstance(q,str):qphi=phi(p+b,mem[q[0]],F(d,6))
   else:qphi=phi(p+b,*(mem[z] for z in q))
   value=newbudget-qphi
  elif name[0]=='price':_,q,i=name;value=sh(a[i],s)-F(mem[q],sum(a[:i])+6-i)
  elif name[0]=='capacity':value=-F(mem[name[1]])
  elif name[0]=='actualpair':value=abudget-phi(sum(a[:4]),*(mem[z] for z in name[1]))
  v.append(value)
 return v

def main():
 data=json.loads((OLD/'attractive_nested_exact.json').read_text());K=F(data['columns'][0]['weight'])
 types=[(tuple(map(int,c['actual_bits'])),tuple(c['hist']),F(c['weight'])) for c in data['columns'] if c['kind']=='hist' and F(c['weight'])]
 terms=[(a,h,word,mass*n) for a,h,mass in types for word,n in zip(PAT,h) if n]
 nw=len(NAMES);rr=[];cc=[];vv=[];row=0
 for j,(a,h,word,mass) in enumerate(terms):
  for de in product(range(2),repeat=2):
   vals=coefficients(a,h,word,de)
   for k,v in enumerate(vals):
    if v:rr.append(row);cc.append(k);vv.append(float(v))
   rr.append(row);cc.append(nw+j);vv.append(-1.);row+=1
 A=coo_matrix((vv,(rr,cc)),shape=(row,nw+len(terms))).tocsr()
 obj=[float(6*K) if isinstance(name,tuple) and name[0]=='capacity' else 0. for name in NAMES]+[float(z[-1]) for z in terms]
 result=linprog(obj,A_ub=A,b_ub=np.zeros(row),A_eq=[[1.]*nw+[0.]*len(terms)],b_eq=[1.],bounds=[(0,None)]*nw+[(None,None)]*len(terms),method='highs')
 report={'scope':'promoted-first-follower local-envelope separation at old necessary point; not an equilibrium or welfare result','shape':list(A.shape),'status':result.message,'slack_float':result.fun,'weights':[(str(n),float(v)) for n,v in zip(NAMES,result.x[:nw]) if v>1e-8]}
 if result.fun < -1e-9:
  weights=[F(float(v)).limit_denominator(1000000) if v>1e-8 else F() for v in result.x[:nw]]
  exact=6*K*sum(v for v,n in zip(weights,NAMES) if isinstance(n,tuple) and n[0]=='capacity')
  for a,h,word,mass in terms:exact+=mass*max(sum(w*v for w,v in zip(weights,coefficients(a,h,word,de))) for de in product(range(2),repeat=2))
  report['exact_slack']=str(exact);report['exact_weights']=[str(w) for w in weights]
 print(json.dumps({k:v for k,v in report.items() if k!='exact_weights'},indent=2),flush=True)
 (HERE/'early_reply_promotion.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
