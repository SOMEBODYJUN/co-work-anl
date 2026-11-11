"""Seven true-IC rows for same-source T -> final C -> new branch.

Applies the existing same_source_reply_requery mechanism to explicit new R/Z.
Nonnegative weights are found numerically; returned rational rows are exact.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import json,sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import old_query_reply_cuts as oq
import terminal_portfolio_cuts as pc
HERE=Path(__file__).resolve().parent

def share(n,d):return F(n,d) if n else F()
@lru_cache(None)
def candidates(i,p,ell,t,q):
 k=6-i;out=[]
 for s,ss,B,C,J,V in product(range(k-2),range(k-2),range(2),range(2),range(2),range(2)):
  z1=p+t+s+B+C;z2=p+C+ss+J+V;base=share(C,z2)
  co=(share(t,z1)-base,share(B,p+C+ss+J+1)-share(V,z2),F(J,ell+1),F(V,ell+1),F(V),F(q,p+t+s+B+1)-share(C,z1))
  out.append((base,co))
 return tuple(out)
@lru_cache(None)
def psi(i,p,ell,t,q,pars):
 return min(base+sum(v*w for v,w in zip(co,pars)) for base,co in candidates(i,p,ell,t,q))
def row(cols,cut):
 i,member=cut['i'],cut['member'];f,diag=cut['orb'];qi=cut['query'];ct=6 if diag else 30;pars=tuple(map(F,cut['parameters']));a,cw,d,e,cap,mu=pars;out=[F()]*len(cols);out[0]=cap;hi=None
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=c;bits=tuple(map(int,c['actual_bits']));whole=sum(bits);p=sum(bits[:i]);ell=sum(bits[:5]);v=share(bits[i],whole)+(d+e)*share(bits[5],whole)
   for (ff,dd,wi,wj),count in oq.groups(c['hist']).items():
    if (ff,dd)==(f,diag):v-=F(count,ct)*psi(i,p,ell,0,pc.qvec(bits,wi,wj,0,c['hist'],diag)[qi],pars)
   out[j]=v
  elif c['kind']=='joint-reply':
   ff,dd,wi,wj=c['group']
   if (ff,dd)!=(f,diag) or not c['state'][member]:continue
   ni=hi['hist'][oq.PAT.index(tuple(wi))];nj=hi['hist'][oq.PAT.index(tuple(wj))];count=ni if diag else ni*nj-(ni if wi==wj else 0)
   bits=tuple(map(int,hi['actual_bits']));p=sum(bits[:i]);ell=sum(bits[:5]);q0=pc.qvec(bits,wi,wj,0,hi['hist'],diag)[qi];q1=pc.qvec(bits,wi,wj,1,hi['hist'],diag)[qi]
   out[j]=-F(count,ct)*(psi(i,p,ell,1,q1,pars)-psi(i,p,ell,0,q0,pars))
 return out

def find_cuts(cols,ys,queries=(5,),sources=range(4)):
 hs,us=pc.parse(cols,ys);K=sum(float(y) for c,y in zip(cols,ys) if c['kind']=='K');found=[];attempted=0
 for i,member,orb,qi in product(sources,range(2),oq.GS,queries):
  f,diag=orb;ct=6 if diag else 30;states=defaultdict(float)
  for h in hs:
   bits=h['a'];p=sum(bits[:i]);ell=sum(bits[:5])
   for (ff,dd,wi,wj),count in h['groups'].items():
    if (ff,dd)!=orb:continue
    one=h['tmass'].get((ff,dd,wi,wj),[0.,0.])[member]
    for t,mass in ((0,h['mass']-one),(1,one)):
     if mass>1e-12:states[p,ell,t,pc.qvec(bits,wi,wj,t,h['hist'],diag)[qi]]+=count*mass/ct
  ss=list(states);nv=6+len(ss);rr=[];cc=[];vv=[];bb=[]
  def add(j,v):
   if v:rr.append(len(bb));cc.append(j);vv.append(float(v))
  for j,(p,ell,t,q) in enumerate(ss):
   for base,co in candidates(i,p,ell,t,q):
    for jj,v in enumerate(co):add(jj,-v)
    add(6+j,1.);bb.append(float(base))
  A=coo_matrix((vv,(rr,cc)),shape=(len(bb),nv)).tocsr();obj=[0.,0.,us[5],us[5],K,0.]+[-states[s] for s in ss]
  sol=linprog(obj,A_ub=A,b_ub=bb,bounds=[(0,1)]+[(0,1000)]*5+[(None,None)]*len(ss),method='highs');attempted+=1
  if sol.success and us[i]+sol.fun < -1e-9:
   pars=[str(F(float(v)).limit_denominator(1000000)) for v in sol.x[:6]];cut={'i':i,'member':member,'orb':list(orb),'query':qi,'parameters':pars}
   r=row(cols,cut);slack=sum(float(x)*float(y) for x,y in zip(r,ys))
   if slack<-1e-9:found.append((slack,cut,r))
 found.sort(key=lambda x:x[0]);return found,attempted
if __name__=='__main__':
 point=json.loads(Path(sys.argv[1]).read_text());ys=[F(c['weight']) for c in point['columns']]
 queries=range(16) if '--all-queries' in sys.argv else (5,)
 found,attempted=find_cuts(point['columns'],ys,queries);selected=[]
 for v,c,r in found:
  exact=sum(x*y for x,y in zip(r,ys));assert exact<0;selected.append({'cut':c,'slack':str(exact)})
 report={'scope':'existing same-source requery on explicit R/Z, necessary point only','source':sys.argv[1],'LPs':attempted,'parameter_bounds':'a in [0,1], other five in [0,1000]','selected':selected}
 Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n');print({'LPs':attempted,'negative_structures':len(found),'worst':selected[0] if selected else None})
