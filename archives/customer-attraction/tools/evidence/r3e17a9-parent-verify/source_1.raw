"""Move old indexed B_i from actual fourth-source branch to actual third source.
This keeps the actual A3 background difference and a complete genuine 3-person tail.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import defaultdict
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE=Path(__file__).resolve().parent
PAT=tuple(product(range(2),repeat=3));INPUT=('T','B','C')+tuple('a'+str(i) for i in range(6))
NAMES=['source']+[('first',q) for q in INPUT]+[('last',q) for q in INPUT+('opt','oldB','oldC')]
NAMES += [('newpair',qs) for qs in combinations_with_replacement(INPUT,2)]
NAMES += [('newthree',qs) for qs in combinations_with_replacement(('T','B','C','a4','a5'),3)]
NAMES += [('oldC',q) for q in ('D','E','F')]+[('oldpair',qs) for qs in combinations_with_replacement(('D','E','F'),2)]
NAMES += [('price',q,i) for q in ('D','E','F') for i in range(6)]+[('capacity',q) for q in ('D','E','F')]
NAMES += [('actualpair',qs) for qs in combinations_with_replacement(('T','B','C','D','E','F'),2)]
def sh(n,d):return F(n,d) if n else F()
def phi(p,x,y):return F(x+y,p+1)-F(x*y,(p+1)*(p+2))
def pair(p,x,y):return sh(x+y,p+x+y)+F(x,(p+1)*(p+2))
def coefficients(a,h,word,xyz):
 t,b,c=word;D,E,Ff=xyz;p=sum(a[:2]);pold=p+a[2];s=sum(a);den=p+b+D+E+Ff
 opts=sum(n*t for n,(t,b,c) in zip(h,PAT));bs=sum(n*b for n,(t,b,c) in zip(h,PAT));cs=sum(n*c for n,(t,b,c) in zip(h,PAT))
 mem={'T':t,'B':b,'C':c,'D':D,'E':E,'F':Ff,'opt':F(opts,6),'oldB':F(bs,6),'oldC':F(cs,6)}|{'a'+str(i):x for i,x in enumerate(a)}
 vals=[]
 for name in NAMES:
  if name=='source':v=sh(a[2],s)-sh(b,den)
  elif name[0]=='first':v=sh(D,den)-F(mem[name[1]],p+b+3)
  elif name[0]=='last':v=sh(Ff,den)-F(mem[name[1]],p+b+D+E+1)
  elif name[0]=='newpair':v=pair(p+b+D,E,Ff)-phi(p+b+D,*(mem[z] for z in name[1]))
  elif name[0]=='newthree':
   q=sum(mem[z] for z in name[1]);v=F(5,3)*sh(D+E+Ff,den)-sh(q,p+b+q)
  elif name[0]=='oldC':v=sh(c,pold+t+b+c)-F(mem[name[1]],pold+t+b+1)
  elif name[0]=='oldpair':v=pair(pold+t,b,c)-phi(pold+t,*(mem[z] for z in name[1]))
  elif name[0]=='price':_,q,i=name;v=sh(a[i],s)-F(mem[q],sum(a[:i])+6-i)
  elif name[0]=='capacity':v=-F(mem[name[1]])
  elif name[0]=='actualpair':v=pair(sum(a[:4]),a[4],a[5])-phi(sum(a[:4]),*(mem[z] for z in name[1]))
  vals.append(v)
 return vals

def main():
 data=json.loads((HERE/'promotion_joint_atoms_exact.json').read_text());masses=defaultdict(F)
 for at in data['RZ_atoms']:masses[at['hist_index']]+=F(at['weight'])
 K=F(data['K']);terms=[]
 for hi,mass in masses.items():
  h=data['histograms'][hi];a=tuple(map(int,h['actual_bits']))
  for word,n in zip(PAT,h['hist']):
   if n:terms.append((a,tuple(h['hist']),word,mass*n))
 nw=len(NAMES);rr=[];cc=[];vv=[];row=0
 for j,(a,h,word,mass) in enumerate(terms):
  for xyz in product(range(2),repeat=3):
   for k,v in enumerate(coefficients(a,h,word,xyz)):
    if v:rr.append(row);cc.append(k);vv.append(float(v))
   rr.append(row);cc.append(nw+j);vv.append(-1.);row+=1
 A=coo_matrix((vv,(rr,cc)),shape=(row,nw+len(terms))).tocsr();obj=[float(6*K) if isinstance(n,tuple) and n[0]=='capacity' else 0. for n in NAMES]+[float(q[-1]) for q in terms]
 sol=linprog(obj,A_ub=A,b_ub=np.zeros(row),A_eq=[[1.]*nw+[0.]*len(terms)],b_eq=[1.],bounds=[(0,None)]*nw+[(None,None)]*len(terms),method='highs')
 report={'scope':'actual third re-query of old actual-fourth first follower; both backgrounds exact; not a SPE or half theorem','rows':nw,'shape':list(A.shape),'status':sol.message,'slack_float':sol.fun,'weights':[(str(n),float(w)) for n,w in zip(NAMES,sol.x[:nw]) if w>1e-8]}
 if sol.fun<-1e-8:
  weights=[F(float(w)).limit_denominator(1000000) if w>1e-8 else F() for w in sol.x[:nw]];slack=6*K*sum(w for w,n in zip(weights,NAMES) if isinstance(n,tuple) and n[0]=='capacity')
  for a,h,word,mass in terms:slack+=mass*max(sum(w*v for w,v in zip(weights,coefficients(a,h,word,xyz))) for xyz in product(range(2),repeat=3))
  report|={'exact_slack':str(slack),'exact_weights':[str(w) for w in weights]}
  (HERE/'third_requery_old_early_separation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='exact_weights'},indent=2),flush=True)
if __name__=='__main__':main()
