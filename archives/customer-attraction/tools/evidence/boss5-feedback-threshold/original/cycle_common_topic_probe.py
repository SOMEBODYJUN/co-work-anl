"""One common actual-reply-cycle topic law versus all retained histories.
Necessary-condition fixed-source completion; feasibility is not SPE existence.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_optimum_primal_overlap1.json'
TY3=list(product((0,1),repeat=3));TY4=list(product((0,1),repeat=4))
LABELS='ABCDEUVWXY'
def sh(a,b):return F(a,b) if a else F(0)
def build():
 j=json.loads(SOURCE.read_text());ats=j['atoms']; n=len(ats)
 masses=[F(a['exact_mass']) for a in ats]
 names=[];coeff=[];rhs=[]
 def add(name,c,r):
  names.append(name);coeff.append([m*x for m,x in zip(masses,c)]);rhs.append(sum(m*x for m,x in zip(masses,r)))
 bits=[list(map(int,a['bits'])) for a in ats]
 ds=[sum(h*t[0] for h,t in zip(a['AB_hist'],TY3)) for a in ats]
 p=[sum(b[:3]) for b in bits]
 d=[sh(b[3],sum(b[:5])) for b in bits]
 # All comparison themes known via fixed bits or menu membership sums.
 menus={k:[b[i] for b in bits] for i,k in enumerate(LABELS)}
 menus['opt'] = ds
 for tag,ty in [('AB',TY3),('AE',TY3),('second',TY4)]:
  for k in range(1,len(ty[0])):
   menus[tag+str(k)]=[sum(h*t[k] for h,t in zip(a[tag+'_hist'],ty)) for a in ats]
 for r in range(3):menus['old'+str(r)]=[a['menus_lh'][r][0] for a in ats]
 for name,mem in menus.items():
  size=1 if name in LABELS else 5
  add('cycle_cap:'+name,[-sh(t,(q+1)*(q+2)) for t,q in zip(mem,p)],
      [size*z-sh(t,q+1) for z,t,q in zip(d,mem,p)])
 add('cycle_own_floor',[sh(1,q+2) for q in p],d)
 # Actual and two E-deviation paths, every true optimization node.
 paths=[('actual',[b[:5] for b in bits],range(5)),
        ('second',[ [b[k] for k in (0,4,5,6,7)] for b in bits],range(2,5)),
        ('third',[ [b[k] for k in (0,1,4,8,9)] for b in bits],range(3,5))]
 for tag,path,positions in paths:
  for pos in positions:
   pay=[sh(z[pos],sum(z)) for z in path]
   den=[sum(z[:pos])+5-pos for z in path]
   add(tag+':floor:'+str(pos),[sh(1,q) for q in den],pay)
  qload=[sum(z[:3]) for z in path]
  HH=[sh(z[3]+z[4],sum(z))+sh(z[3],(q+1)*(q+2)) for z,q in zip(path,qload)]
  add(tag+':tax:repeat_cycle',[sh(2,q+2) for q in qload],HH)
  for name,mem in menus.items():
   size=1 if name in LABELS else 5
   add(tag+':tax:cycle+'+name,
       [sh(size,q+1)-sh(2*t,(q+1)*(q+2)) for t,q in zip(mem,qload)],
       [size*h-sh(t,q+1) for h,t,q in zip(HH,mem,qload)])
 # Indexed true nodes. Sum over the five query indices preserves true match.
 for tag,ty in [('AB',TY3),('AE',TY3),('second',TY4)]:
  pre=[b[0]+(b[1] if tag=='AB' else b[4] if tag=='AE' else 0) for b in bits]
  H=[a[tag+'_hist'] for a in ats]
  for k in range(1,len(ty[0])):
   c=[];rr=[]
   for q,h in zip(pre,H):
    c.append(sum(cnt*sh(1,q+sum(t[:k])+len(t)-k) for cnt,t in zip(h,ty)))
    rr.append(sum(cnt*sh(t[k],q+sum(t)) for cnt,t in zip(h,ty)))
   add(tag+':floor:'+str(k),c,rr)
  # Each indexed two-tail starts after t (plus h for second-position family).
  HH=[];c_re=[]
  for q,h in zip(pre,H):
   HH.append(sum(cnt*(sh(t[-2]+t[-1],q+sum(t))+sh(t[-2],(q+sum(t[:-2])+1)*(q+sum(t[:-2])+2))) for cnt,t in zip(h,ty)))
   c_re.append(sum(cnt*sh(2,q+sum(t[:-2])+2) for cnt,t in zip(h,ty)))
  add(tag+':tax:repeat_cycle',c_re,HH)
  for name,mem in menus.items():
   size=1 if name in LABELS else 5
   c=[];rr=[]
   for q,h,targ,Hval in zip(pre,H,mem,HH):
    c.append(sum(cnt*(sh(size,q+sum(t[:-2])+1)-sh(2*targ,(q+sum(t[:-2])+1)*(q+sum(t[:-2])+2))) for cnt,t in zip(h,ty)))
    rr.append(size*Hval-sum(cnt*sh(targ,q+sum(t[:-2])+1) for cnt,t in zip(h,ty)))
   add(tag+':tax:cycle+'+name,c,rr)
  # A cycle topic paired with this branch's own t/r/s etc.
  for k in range(len(ty[0])):
   c=[];rr=[]
   for q,h,Hval in zip(pre,H,HH):
    c.append(sum(cnt*(sh(1,q+sum(t[:-2])+1)-sh(2*t[k],(q+sum(t[:-2])+1)*(q+sum(t[:-2])+2))) for cnt,t in zip(h,ty)))
    rr.append(Hval-sum(cnt*sh(t[k],q+sum(t[:-2])+1) for cnt,t in zip(h,ty)))
   add(tag+':tax:cycle+own'+str(k),c,rr)
 # Old final reply menus at fixed two-tail prefixes, sum five true final BRs.
 bgs=[ [b[0]+b[1]+b[2],b[0]+b[4]+b[5],b[0]+b[1]+b[4]] for b in bits]
 for k in range(3):
  c=[];rr=[]
  for a,qall,jj in zip(ats,bgs,ds):
   q=qall[k];ell,h=a['menus_lh'][k]
   c.append(sh(5,q+1)-sh(jj,(q+1)*(q+2)))
   rr.append(sh(ell,q+1)-sh(h,(q+1)*(q+2)))
  add('oldreply:floor_cycle:'+str(k),c,rr)
 return names,coeff,rhs

def main():
 names,cs,rs=build();A=np.asarray(cs,dtype=float);b=np.asarray(rs,dtype=float)
 n=A.shape[1]
 # Minimize uniform additive infeasibility; slack may be negative.
 res=linprog(np.r_[np.zeros(n),1.],A_ub=np.c_[A,-np.ones(len(names))],b_ub=b,bounds=[(0,1)]*n+[(None,None)],method='highs')
 out={'source':str(SOURCE.relative_to(ROOT)),'rows':len(names),'variables':n,'status':res.message,'scope':'common-cycle-topic-law necessary completion only; not SPE realization'}
 if res.success:
  out['minimum_uniform_violation']=float(res.fun)
  out['active_rows']={name:float(-v) for name,v in zip(names,res.ineqlin.marginals) if v< -1e-9}
  out['mean_cycle_membership']=res.x[:-1].tolist()
  out['nonzero_dual']=[{'name':name,'multiplier':float(-v)} for name,v in zip(names,res.ineqlin.marginals) if v< -1e-9]
 (HERE/'cycle_common_topic_probe.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('mean_cycle_membership','nonzero_dual')},indent=2))
if __name__=='__main__':main()
