"""Separate explicit new replies by legal r<=4 true-tail profit projections.

No five-player background bound is used. Alpha/gamma are discovered by an LP,
then rationalized and each negative row is checked exactly on its source point.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import sys,json,hashlib
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
BETA={1:F(1),2:F(3,2),3:F(5,3),4:F(1499,750)}
ORBS=((0,0),(1,0),(1,1))
QUERIES=('actual4','actual5','self','wi0','wi1','wi2','wj0','wj1','wj2')
PAT=tuple(product(range(2),repeat=3))

def frac(n,d):return F(n,d) if n else F()
def query(q,a,wi,wj,t):
 if q=='self':return t
 if q.startswith('actual'):return a[int(q[-1])]
 return (wi if q.startswith('wi') else wj)[int(q[-1])]
def psi(b,ell,t,q,r,alpha,gamma):
 return gamma*frac(q,b+t+q)+min(frac(t-gamma*BETA[r]*z,b+t+z)+alpha*F(z,ell+1) for z in range(r+1))

def parse(point):
 hs={};hi=None
 for j,c in enumerate(point['columns']):
  if c['kind']=='hist':hi=j;hs[hi]={'data':c,'groups':{}}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));hs[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=(j,F(c['weight']))
 return hs

def states(point,cut):
 hs=parse(point);st=defaultdict(F);ui=F();u6=F();i,member,orb,q=cut['i'],cut['member'],tuple(cut['orb']),cut['q'];r=5-i;n=6 if orb[1] else 30
 for hi,dd in hs.items():
  c=dd['data'];hm=F(c['weight']);a=tuple(map(int,c['actual_bits']));s=sum(a);b=sum(a[:i]);ell=sum(a[:5]);ui+=hm*frac(a[i],s);u6+=hm*frac(a[5],s);hc=dict(zip(PAT,c['hist']))
  if not hm:continue
  for g,gs in dd['groups'].items():
   f,diag,wi,wj=g
   if (f,diag)!=orb:continue
   count=hc[wi] if diag else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
   one=sum(w for (rr,zz),(j,w) in gs.items() if (rr,zz)[member]);zero=hm-one
   assert min(one,zero)>=0
   for t,mass in ((0,zero),(1,one)):
    qq=r*query(q,a,wi,wj,t);st[b,ell,t,qq]+=F(count,n)*mass
 return {k:v for k,v in st.items() if v},ui,u6

def coefficient_rows(cols,cut):
 i,member,orb,q=cut['i'],cut['member'],tuple(cut['orb']),cut['q'];r=5-i;n=6 if orb[1] else 30;alpha=F(cut['alpha']);gamma=F(cut['gamma']);row=[F()]*len(cols);hs={};hi=None
 for j,c in enumerate(cols):
  if c['kind']=='hist':hi=j;hs[hi]={'data':c,'groups':{}}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));hs[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=j
 for hi,dd in hs.items():
  c=dd['data'];a=tuple(map(int,c['actual_bits']));s=sum(a);b=sum(a[:i]);ell=sum(a[:5]);hc=dict(zip(PAT,c['hist']))
  row[hi]=frac(a[i],s)+r*alpha*frac(a[5],s)
  for g,gs in dd['groups'].items():
   f,diag,wi,wj=g
   if (f,diag)!=orb:continue
   count=hc[wi] if diag else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
   v0=psi(b,ell,0,r*query(q,a,wi,wj,0),r,alpha,gamma);v1=psi(b,ell,1,r*query(q,a,wi,wj,1),r,alpha,gamma)
   row[hi]-=F(count,n)*v0
   for st,j in gs.items():
    if st[member]:row[j]-=F(count,n)*(v1-v0)
 return row

def discover(point):
 selected=[];best=(0,None)
 for i,member,orb,q in product(range(1,5),range(2),ORBS,QUERIES):
  cut={'i':i,'member':member,'orb':list(orb),'q':q};r=5-i;st,ui,u6=states(point,cut);ks=list(st);A=[];bb=[]
  for j,(b,ell,t,qq) in enumerate(ks):
   rc=frac(qq,b+t+qq)
   for z in range(r+1):
    v=[0.]*(2+len(ks));v[0]=-float(F(z,ell+1));v[1]=-float(rc-BETA[r]*frac(z,b+t+z));v[2+j]=1
    A.append(v);bb.append(float(frac(t,b+t+z)))
  obj=[float(r*u6),0.]+[-float(st[k]) for k in ks]
  sol=linprog(obj,A_ub=A,b_ub=bb,bounds=[(0,None),(0,None)]+[(None,None)]*len(ks),method='highs')
  if not sol.success:continue
  gap=float(ui)+sol.fun
  if gap<best[0]:best=(gap,{**cut,'float_alpha':sol.x[0],'float_gamma':sol.x[1]})
  if gap>=-1e-8:continue
  alpha=F(float(sol.x[0])).limit_denominator(1000000);gamma=F(float(sol.x[1])).limit_denominator(1000000)
  slack=ui+r*alpha*u6-sum(w*psi(*k,r,alpha,gamma) for k,w in st.items())
  if slack<0:
   cut.update({'alpha':str(alpha),'gamma':str(gamma),'slack':str(slack)})
   row=coefficient_rows(point['columns'],cut);rowvalue=sum(v*F(c['weight']) for v,c in zip(row,point['columns']));assert rowvalue==slack
   selected.append(cut)
 return {'best_float':best,'selected':selected}

def main():
 source=HERE/'early_reply_floors_exact.json'
 if '--point' in sys.argv:source=Path(sys.argv[sys.argv.index('--point')+1])
 tag='tail_reply_cuts'
 if '--tag' in sys.argv:tag=sys.argv[sys.argv.index('--tag')+1]
 point=json.loads(source.read_text());out=discover(point);out.update({'scope':'exactly negative legal r<=4 tail-profit projected rows on one necessary graph point; not SPE or half proof','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_W':point['W']})
 (HERE/(tag+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='selected'},indent=2));print('negative directions',len(out['selected']))
if __name__=='__main__':main()
