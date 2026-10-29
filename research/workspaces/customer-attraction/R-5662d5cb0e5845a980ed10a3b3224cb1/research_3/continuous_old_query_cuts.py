"""Continuous nonnegative middle/last prices and true terminal IC multiplier.

Finite support separation only. Every returned rational cut uses the proved
priced-hidden-reply projection and is valid for every original-model SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import sys,json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
sys.path.insert(0,str(ROOT))
from customer_attraction.priced_hidden_reply import projected_by_count
import old_query_reply_cuts as oq
PAT=oq.PAT;GS=oq.GS

@lru_cache(None)
def psi(i,p,ell,t,q,am,al,mu):
 n=5-i
 return projected_by_count(p,ell,t,q,(am,)*(n-1)+(al,),(F(),)*n,mu)

def row(cols,cut):
 i,member,f,diag,qi,ams,als,mus=cut;am,al,mu=map(F,(ams,als,mus));n=5-i;out=[F()]*len(cols);hi=None
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=c;a=tuple(map(int,c['actual_bits']));whole=sum(a);p=sum(a[:i]);ell=sum(a[:5]);ct=6 if diag else 30
   own=F(a[i],whole) if a[i] else F();last=F(a[5],whole) if a[5] else F();v=ct*(own+((n-1)*am+al)*last)
   for (ff,dd,wi,wj),count in oq.groups(c['hist']).items():
    if (ff,dd)==(f,diag):v-=count*psi(i,p,ell,0,(wi+wj)[qi],am,al,mu)
   out[j]=v
  elif c['kind']=='joint-reply':
   ff,dd,wi,wj=c['group']
   if (ff,dd)!=(f,diag) or not c['state'][member]:continue
   ni=hi['hist'][PAT.index(tuple(wi))];nj=hi['hist'][PAT.index(tuple(wj))];count=ni if diag else ni*nj-(ni if wi==wj else 0)
   a=tuple(map(int,hi['actual_bits']));p=sum(a[:i]);ell=sum(a[:5]);q=(tuple(wi)+tuple(wj))[qi]
   out[j]=-count*(psi(i,p,ell,1,q,am,al,mu)-psi(i,p,ell,0,q,am,al,mu))
 return out

def sufficient_stats(cols,ys):
 hs=[];h=None;us=[0.]*6
 for c,w in zip(cols,ys):
  w=float(w)
  if c['kind']=='hist':
   a=tuple(map(int,c['actual_bits']));whole=sum(a)
   h={'a':a,'mass':w,'groups':oq.groups(c['hist']),'tmass':{}};hs.append(h)
   for i in range(6):us[i]+=w*a[i]/whole if a[i] else 0
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));v=h['tmass'].setdefault(g,[0.,0.])
   for m in range(2):v[m]+=w*c['state'][m]
 data={}
 for member,fdiag,qi in product(range(2),GS,range(6)):
  byhist=[]
  for h in hs:
   nq=[0.,0.];mt=[0.,0.]
   for g,count in h['groups'].items():
    f,d,wi,wj=g
    if (f,d)!=fdiag:continue
    q=(wi+wj)[qi];nq[q]+=h['mass']*count;mt[q]+=count*h['tmass'].get(g,[0.,0.])[member]
   byhist.append((h['a'],((nq[0]-mt[0],mt[0]),(nq[1]-mt[1],mt[1]))))
  data[member,*fdiag,qi]=byhist
 return data,us

def find_cuts(cols,ys,maxcuts=32):
 data,us=sufficient_stats(cols,ys);cuts=[];attempted=0
 for i,member,fdiag,qi in product(range(5),range(2),GS,range(6)):
  f,diag=fdiag;n=5-i;ct=6 if diag else 30;states=defaultdict(float)
  for a,masses in data[member,f,diag,qi]:
   for q,t in product(range(2),repeat=2):states[sum(a[:i]),sum(a[:5]),t,q]+=masses[q][t]
  states={s:max(0.,w) for s,w in states.items() if w>1e-12};ss=list(states);nv=3+len(ss);obj=[ct*(n-1)*us[5],ct*us[5],0.]+[-states[s] for s in ss];A=[];b=[]
  for j,(p,ell,t,q) in enumerate(ss):
   for s,g in product(range(n),range(2)):
    denom=p+t+s+g;base=t/denom if t else 0.;cmu=q/(p+t+s+1)-(g/denom if g else 0.)
    rr=[0.]*nv;rr[0]=-s/(ell+1);rr[1]=-g/(ell+1);rr[2]=-cmu;rr[3+j]=1.;A.append(rr);b.append(base)
  sol=linprog(obj,A_ub=A,b_ub=b,bounds=[(0,0 if n==1 else 1000),(0,1000),(0,1000)]+[(None,None)]*len(ss),method='highs')
  attempted+=1
  if sol.success and ct*us[i]+sol.fun < -1e-8:
   am,al,mu=(str(F(float(v)).limit_denominator(1000000)) for v in sol.x[:3]);cut=(i,member,f,diag,qi,am,al,mu)
   rr=row(cols,cut);slack=sum(float(v)*float(y) for v,y in zip(rr,ys))
   if slack < -1e-8:cuts.append((slack,cut,rr))
 cuts.sort(key=lambda x:x[0]);return cuts[:maxcuts],attempted

if __name__=='__main__':
 point=json.loads(Path(sys.argv[1]).read_text());cols=point['columns'];ys=[F(c['weight']) for c in cols]
 found,attempted=find_cuts(cols,ys,64);out=[]
 for slack,cut,rr in found:
  exact=sum(v*y for v,y in zip(rr,ys));assert exact<0;out.append({'cut':cut,'slack':str(exact)})
 report={'scope':'continuous alpha_middle,alpha_last,mu separation on necessary point only','input':sys.argv[1],'parameter_bounds':[0,1000],'LPs':attempted,'selected':out}
 Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n');print({'LPs':attempted,'negative_structures':len(found),'worst':out[0] if out else None})
