"""Optimize over every word/RT-member completion of a coarse B-menu point.

Unlike simply setting l=ell/6 on endpoint columns, this retains only each
(actual,hist,Q,R) group's mass and first ell moment. A free affine ell minorant
and all per-word assignments account for every possible indexed completion.
The local lambda row is from swap_B_L_visible_projection; root-preserving reset
is required only for the two minimum-selection rows, which can be disabled.
"""
from swap_B_L_visible_projection import geometry,HERE
from itertools import product
from fractions import Fraction as F
import argparse,json,numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--point',default='../research_2/coupled_B_master_exact.json');ap.add_argument('--prefix',default='swap_B_coupling_5259');ap.add_argument('--omit-minimum',action='store_true');a=ap.parse_args();point=json.loads((HERE/a.point).read_text());cols=point['columns'];states,names,tab=geometry();nv=len(names);idx={s:i for i,s in enumerate(states)};groups={};words=list(product((0,1),repeat=3))
 for c in cols:
  if c['kind']!='actual-B-branch-state' or not F(c['weight']):continue
  old=cols[c['hist_column']];key=(tuple(map(int,old['actual_bits'])),tuple(old['hist']),c['Q'],c['R']);m,e=groups.get(key,(F(0),F(0)));w=F(c['weight']);groups[key]=(m+w,e+w*c['ell'])
 gs=list(groups);ng=len(gs);nzs=sum(2*sum(v>0 for v in key[1]) for key in gs);zstart=nv;phistart=zstart+nzs;rhostart=phistart+ng;nvar=rhostart+ng
 zcols={};cur=zstart
 for gi,key in enumerate(gs):
  for wi,n in enumerate(key[1]):
   if n:
    for l in (0,1):zcols[gi,wi,l]=cur;cur+=1
 rr=[];cc=[];vv=[];rhs=[];row=0
 def add(cs,vs,b=0):
  nonlocal row
  for c,v in zip(cs,vs):
   if v:rr.append(row);cc.append(c);vv.append(float(v))
  rhs.append(float(b));row+=1
 for gi,(actual,hist,h,i) in enumerate(gs):
  nz=[wi for wi,n in enumerate(hist) if n]
  for wi in nz:
   for l in (0,1):
    si=idx[(actual,*words[wi],h,i,l)]
    for hidden in range(2):add(list(range(nv))+[zcols[gi,wi,l]],[-F(int(v),60) for v in tab[si,hidden]]+[1])
  # phi + rho*ell <= mean hidden credit, for all word-wise assignments.
  for ls in product((0,1),repeat=len(nz)):
   ell=sum(hist[wi]*l for wi,l in zip(nz,ls))
   add([phistart+gi,rhostart+gi]+[zcols[gi,wi,l] for wi,l in zip(nz,ls)],[1,ell]+[-F(hist[wi],6) for wi in nz])
 A=coo_matrix((vv,(rr,cc)),shape=(row,nvar)).tocsr();us=[F(0)]*6
 for c in cols:
  if c['kind']=='hist':
   ac=tuple(map(int,c['actual_bits']));w=F(c['weight']);den=sum(ac)
   for j,v in enumerate(ac):us[j]+=w*F(v,den) if v else 0
 K=F(cols[0]['weight']);obj=np.zeros(nvar)
 for j,n in enumerate(names):
  if n.startswith('price:'):obj[j]=float(us[int(n.split(':')[1])])
  if n.startswith('cap:'):obj[j]=float(K)
 for gi,key in enumerate(gs):obj[phistart+gi]=-float(groups[key][0]);obj[rhostart+gi]=-float(groups[key][1])
 eq=np.zeros((1,nvar));eq[0,0]=eq[0,1]=1;bounds=[(0,100)]*nv+[(None,None)]*(nvar-nv);bounds[names.index('tie')]=(-100,100)
 if a.omit_minimum:bounds[names.index('minimumB')]=bounds[names.index('minimumT')]=(0,0)
 sol=linprog(obj,A_ub=A,b_ub=rhs,A_eq=eq,b_eq=[1],bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 print('groups',ng,'LP',A.shape,sol.success,sol.message,'separation',None if sol.fun is None else -sol.fun-float(us[3]),flush=True);out={'status':'local projection over all word/reply completions of this necessary point; not half proof','point':a.point,'omit_minimum':a.omit_minimum,'success':sol.success,'message':sol.message}
 if sol.success:
  lam=[F(float(v)).limit_denominator(10**7) for v in sol.x[:nv]];rhos=[F(float(v)).limit_denominator(10**7) for v in sol.x[rhostart:]];assert all(v>=0 for n,v in zip(names,lam) if n!='tie')
  budget=us[3]*(lam[0]+lam[1])+sum(lam[j]*us[int(n.split(':')[1])] for j,n in enumerate(names) if n.startswith('price:'))+sum(lam[j]*K for j,n in enumerate(names) if n.startswith('cap:'));credit=F(0);groupdata=[]
  for gi,(ac,hist,h,i) in enumerate(gs):
   rho=rhos[gi];psi=F(0)
   for wi,n in enumerate(hist):
    if not n:continue
    z=[]
    for l in (0,1):
     si=idx[(ac,*words[wi],h,i,l)];z.append(min(sum(F(int(v),60)*la for v,la in zip(co,lam)) for co in tab[si]))
    psi+=F(n,6)*min(z[0],z[1]-6*rho)
   m,e=groups[(ac,hist,h,i)];credit+=m*psi+e*rho;groupdata.append({'actual_bits':ac,'hist':hist,'Q':h,'R':i,'mass':str(m),'ell_moment':str(e),'rho':str(rho),'psi':str(psi)})
  score=credit-budget;print('EXACT_SCORE',str(score),float(score),'active',[(n,str(v)) for n,v in zip(names,lam) if v],flush=True)
  out.update({'lambda':{n:str(v) for n,v in zip(names,lam) if v},'source_coefficient':str(lam[0]+lam[1]),'exact_separation':str(score),'groups':groupdata,'budget':str(budget),'credit':str(credit)})
 (HERE/(a.prefix+'.json')).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
