"""Shared true terminal IC portfolio, followed by one hidden-reply projection.

Queries are actual6, old wi/wj6, and the forced new reply itself. This extends
single-Q projections while keeping their terminal reply identity shared.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from functools import lru_cache
import sys,json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import old_query_reply_cuts as oq
HERE=Path(__file__).resolve().parent
PAT=oq.PAT;GS=oq.GS

def qvec(a,wi,wj,t,hist=None,diag=None):
 out=tuple(a)+tuple(wi)+tuple(wj)+(t,)
 if hist is not None:
  total=[sum(n*w[q] for n,w in zip(hist,PAT)) for q in range(3)]
  excluded=tuple(wi) if diag else tuple(x+y for x,y in zip(wi,wj))
  out+=tuple(F(v-e,5 if diag else 4) for v,e in zip(total,excluded))
 return out
def share(n,d):return F(n,d) if n else F()
@lru_cache(None)
def psi(i,p,ell,t,qs,am,al,bm,bl,mus):
 n=5-i;M=sum(mus);Q=sum(mu*q for mu,q in zip(mus,qs))
 return min(share(t-M*g,p+t+s+g)+F(am*s+al*g,ell+1)+bm*s+bl*g+F(Q,p+t+s+1) for s,g in product(range(n),range(2)))

def row(cols,cut):
 i,member=cut['i'],cut['member'];f,diag=cut['orb'];am=F(cut['alpha_middle']);al=F(cut['alpha_last']);bm=F(cut.get('beta_middle','0'));bl=F(cut.get('beta_last','0'));mus=tuple(map(F,cut['mu']));n=5-i;ct=6 if diag else 30;out=[F()]*len(cols);hi=None
 out[0]=(n-1)*bm+bl
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=c;a=tuple(map(int,c['actual_bits']));whole=sum(a);p=sum(a[:i]);ell=sum(a[:5]);v=share(a[i],whole)+((n-1)*am+al)*share(a[5],whole)
   for (ff,dd,wi,wj),count in oq.groups(c['hist']).items():
    if (ff,dd)==(f,diag):v-=F(count,ct)*psi(i,p,ell,0,qvec(a,wi,wj,0,c['hist'],diag),am,al,bm,bl,mus)
   out[j]=v
  elif c['kind']=='joint-reply':
   ff,dd,wi,wj=c['group']
   if (ff,dd)!=(f,diag) or not c['state'][member]:continue
   ni=hi['hist'][PAT.index(tuple(wi))];nj=hi['hist'][PAT.index(tuple(wj))];count=ni if diag else ni*nj-(ni if wi==wj else 0)
   a=tuple(map(int,hi['actual_bits']));p=sum(a[:i]);ell=sum(a[:5])
   v1=psi(i,p,ell,1,qvec(a,wi,wj,1,hi['hist'],diag),am,al,bm,bl,mus);v0=psi(i,p,ell,0,qvec(a,wi,wj,0,hi['hist'],diag),am,al,bm,bl,mus)
   out[j]=-F(count,ct)*(v1-v0)
 return out

def parse(cols,ys):
 hs=[];h=None;us=[0.]*6
 for c,w in zip(cols,ys):
  w=float(w)
  if c['kind']=='hist':
   a=tuple(map(int,c['actual_bits']));whole=sum(a);h={'a':a,'hist':c['hist'],'mass':w,'groups':oq.groups(c['hist']),'tmass':{}};hs.append(h)
   for i in range(6):us[i]+=w*a[i]/whole if a[i] else 0.
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));vv=h['tmass'].setdefault(g,[0.,0.])
   for m in range(2):vv[m]+=w*c['state'][m]
 return hs,us

def find_cuts(cols,ys,maxcuts=30):
 hs,us=parse(cols,ys);K=sum(float(y) for c,y in zip(cols,ys) if c['kind']=='K');found=[];attempted=0
 for i,member,orb in product(range(5),range(2),GS):
  f,diag=orb;n=5-i;ct=6 if diag else 30;states=defaultdict(float)
  for h in hs:
   a=h['a'];p=sum(a[:i]);ell=sum(a[:5])
   for (ff,dd,wi,wj),count in h['groups'].items():
    if (ff,dd)!=orb:continue
    one=h['tmass'].get((ff,dd,wi,wj),[0.,0.])[member]
    for t,w in ((0,h['mass']-one),(1,one)):
     if w>1e-12:states[p,ell,t,qvec(a,wi,wj,t,h['hist'],diag)]+=count*w/ct
  ss=list(states);nq=len(ss[0][3]) if ss else 16;npar=4+nq;nv=npar+len(ss);rr=[];cc=[];vv=[];bb=[]
  def add(j,v):
   if v:rr.append(len(bb));cc.append(j);vv.append(v)
  for j,(p,ell,t,qs) in enumerate(ss):
   for s,g in product(range(n),range(2)):
    denom=p+t+s+g;base=t/denom if t else 0.;last=g/denom if g else 0.
    add(0,-s/(ell+1));add(1,-g/(ell+1));add(2,-s);add(3,-g)
    for q,bit in enumerate(qs):add(4+q,-(float(bit)/(p+t+s+1)-last))
    add(npar+j,1.);bb.append(base)
  A=coo_matrix((vv,(rr,cc)),shape=(len(bb),nv)).tocsr();obj=[(n-1)*us[5],us[5],(n-1)*K,K]+[0.]*nq+[-states[s] for s in ss]
  bounds=[(0,0 if n==1 else 1000),(0,1000),(0,0 if n==1 else 1000)]+[(0,1000)]*(nq+1)+[(None,None)]*len(ss)
  sol=linprog(obj,A_ub=A,b_ub=bb,bounds=bounds,method='highs');attempted+=1
  if sol.success and us[i]+sol.fun < -1e-9:
   pars=[str(F(float(v)).limit_denominator(1000000)) for v in sol.x[:npar]]
   cut={'i':i,'member':member,'orb':list(orb),'alpha_middle':pars[0],'alpha_last':pars[1],'beta_middle':pars[2],'beta_last':pars[3],'mu':pars[4:]}
   r=row(cols,cut);slack=sum(float(x)*float(y) for x,y in zip(r,ys))
   if slack < -1e-9:found.append((slack,cut,r))
 found.sort(key=lambda x:x[0]);return found[:maxcuts],attempted

if __name__=='__main__':
 point=json.loads(Path(sys.argv[1]).read_text());ys=[F(c['weight']) for c in point['columns']];found,attempted=find_cuts(point['columns'],ys)
 cuts=[]
 for v,c,r in found:
  exact=sum(x*y for x,y in zip(r,ys));assert exact<0;cuts.append({'cut':c,'slack':str(exact)})
 report={'scope':'shared terminal IC portfolio separation on one necessary graph point only','source':sys.argv[1],'LPs':attempted,'parameter_bounds':[0,1000],'selected':cuts}
 Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n');print({'LPs':attempted,'negative_structures':len(cuts),'worst':cuts[0] if cuts else None})
