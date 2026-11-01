"""Actual fourth forces explicit new R/Z; true fifth then queries actual B.

Hidden q,r,y memberships describe T,Q,R and T,B,Y from the same SPE.
This uses true intermediate-player IC, unlike a terminal-only price projection.
A nonnegative weighted row is maximized over the complete hidden cube.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import sys,json,hashlib
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
PAT=tuple(product(range(2),repeat=3));ORBS=((0,0),(1,0),(1,1))
NAMES=('source','middleB','lastB','lastY','innerQ','innerR','innerT','G','E','innerE','Pq','Pr','Py','Cq','Cr','Cy','H2q','H2r','H2y','H3q','H3r','H3y','PAIRaa','PAIRab','PAIRbb')
NI={n:i for i,n in enumerate(NAMES)}

def share(n,d):return F(n,d) if n else F()
def raw(a,d,t,q,r,y,L):
 p=sum(a[:3]);a5=a[4];b=a[5];bg=p+t;den=bg+q+r;den2=bg+b+y;total=sum(a);u=[share(z,total) for z in a];ell=sum(a[:5]);D=(bg+1)*(bg+2)
 vals=[u[3]-share(t,den),share(q,den)-share(b,den2),share(r,den)-F(b,bg+q+1),share(r,den)-F(y,bg+q+1),share(y,den2)-F(q,bg+b+1),share(y,den2)-F(r,bg+b+1),share(y,den2)-F(t,bg+b+1)]
 vals += [6*share(q,den)+share(r,2*den)-F(d,bg+1)-F(L,12*(bg+q+1))+F(d*L,6*D),6*share(r,den)-F(d,bg+q+1),6*share(y,den2)-F(d,bg+b+1)]
 vals += [u[5]-F(z,ell+1) for z in (q,r,y)]
 vals += [-F(z) for z in (q,r,y)]
 vals += [u[1]-F(z,5+a[0]) for z in (q,r,y)]
 vals += [u[2]-F(z,4+a[0]+a[1]) for z in (q,r,y)]
 H=share(q+r,den)+F(q,D)
 vals += [H-F(2*a5,bg+1)+F(a5,D),H-F(a5+b,bg+1)+F(a5*b,D),H-F(2*b,bg+1)+F(b,D)]
 assert len(vals)==len(NAMES)
 return tuple(vals)

def parse(point,member,orb):
 hs={};hi=None
 for j,c in enumerate(point['columns']):
  if c['kind']=='hist':hi=j;hs[hi]={'data':c,'groups':{}}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));hs[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=F(c['weight'])
 states=defaultdict(F);ct=6 if orb[1] else 30
 for hi,h in hs.items():
  c=h['data'];hm=F(c['weight']);a=tuple(map(int,c['actual_bits']));d=c['d'];hc=dict(zip(PAT,c['hist']))
  for (f,dg,wi,wj),gs in h['groups'].items():
   if (f,dg)!=orb:continue
   count=hc[wi] if dg else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
   one=sum(v for st,v in gs.items() if st[member]);zero=hm-one;assert min(one,zero)>=0
   for t,mass in ((0,zero),(1,one)):states[a,d,t]+=F(count,ct)*mass
 return {k:v for k,v in states.items() if v}

def coeff(a,d,t,weights):
 return max(sum(w*v for w,v in zip(weights,raw(a,d,t,q,r,y,L))) for q,r,y,L in product(range(2),range(2),range(2),(0,6)))

def row(cols,cut):
 member=cut['member'];orb=tuple(cut['orb']);weights=[F(cut['weights'].get(n,'0')) for n in NAMES];ct=6 if orb[1] else 30;out=[F()]*len(cols);out[0]=sum(weights[NI[n]] for n in ('Cq','Cr','Cy'));hi=None
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=c;a=tuple(map(int,c['actual_bits']));v0=coeff(a,c['d'],0,weights);out[j]=v0
  elif c['kind']=='joint-reply':
   f,dg,wi,wj=c['group']
   if (f,dg)!=orb or not c['state'][member]:continue
   hc=dict(zip(PAT,hi['hist']));count=hc[tuple(wi)] if dg else hc[tuple(wi)]*hc[tuple(wj)]-(hc[tuple(wi)] if wi==wj else 0)
   a=tuple(map(int,hi['actual_bits']));out[j]=F(count,ct)*(coeff(a,hi['d'],1,weights)-coeff(a,hi['d'],0,weights))
 return out

def discover(point):
 K=F(point['columns'][0]['weight']);cuts=[]
 for member,orb in product(range(2),ORBS):
  st=parse(point,member,orb);ks=list(st);nr=len(NAMES);nv=nr+len(ks);A=[];bb=[]
  for j,(a,d,t) in enumerate(ks):
   for q,r,y,L in product(range(2),range(2),range(2),(0,6)):
    v=list(map(float,raw(a,d,t,q,r,y,L)))+[0.]*len(ks);v[nr+j]=-1;A.append(v);bb.append(0.)
  obj=[float(K) if n in ('Cq','Cr','Cy') else 0. for n in NAMES]+[float(st[k]) for k in ks]
  sol=linprog(obj,A_ub=A,b_ub=bb,A_eq=[[1.]*nr+[0.]*len(ks)],b_eq=[1.],bounds=[(0,None)]*nr+[(None,None)]*len(ks),method='highs')
  if not sol.success or sol.fun>=-1e-9:continue
  ws=[F(float(v)).limit_denominator(1000000) for v in sol.x[:nr]]
  val=K*sum(ws[NI[n]] for n in ('Cq','Cr','Cy'))+sum(mass*coeff(a,d,t,ws) for (a,d,t),mass in st.items())
  if val<0:
   cut={'member':member,'orb':list(orb),'weights':{n:str(w) for n,w in zip(NAMES,ws) if w},'slack':str(val)}
   rr=row(point['columns'],cut);assert sum(v*F(c['weight']) for v,c in zip(rr,point['columns']))==val
   cuts.append(cut)
 return cuts

def main():
 source=HERE/'combined_branch_latest_exact.json'
 if '--point' in sys.argv:source=Path(sys.argv[sys.argv.index('--point')+1])
 point=json.loads(source.read_text());cuts=discover(point);out={'scope':'true middle IC nested local projection, negative necessary-point separation only; not SPE or half','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_W':point['W'],'selected':cuts}
 (HERE/'nested_reply_cuts.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
