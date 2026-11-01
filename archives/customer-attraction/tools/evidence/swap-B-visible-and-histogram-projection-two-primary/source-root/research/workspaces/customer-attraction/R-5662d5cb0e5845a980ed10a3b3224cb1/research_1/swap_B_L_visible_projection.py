"""Two genuinely new last replies link old Ti and actual-B three-player branches.

Visible old branches: (prefix,Ti,Bi,Ci), (prefix,B,Q,R).
New clone second queries give (prefix,Ti,B,R_B) and (prefix,B,Ti,R_T).
Their last background is common; reset normal form additionally gives minimum
selection. The entire old zero-signal tree is retained, so old branch labels
may be held visible. All actual u_i safety prices and the common K are paid.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE=Path(__file__).resolve().parent

def sh(a,d):return F(a,d) if a else F(0)
def geometry():
 states=[(a,t,f,g,h,i,l) for a in product((0,1),repeat=6) for t,f,g,h,i,l in product((0,1),repeat=6)]
 names=['sourceT','sourceB','middleT','middleB']+[f'last{who}:query{j}' for who in ('G','I','RB','RT') for j in range(8)]+['minimumB','minimumT','tie']+[f'price:{ai}:{j}' for ai in range(6) for j in range(6)]+[f'cap:{j}' for j in range(6)]
 tables=[]
 for a,t,f,g,h,i,l in states:
  p=sum(a[:3]);ell=sum(a[:5]);q=a[5];zT=p+t+f+g;zB=p+q+h+i;b=p+t+q;UF=sh(f,zT);UG=sh(g,zT);UH=sh(h,zB);UI=sh(i,zB);tab=[]
  for k in (0,1):
   hidden=(f,g,h,i,k,l);bits=(t,q,*hidden);row=[sh(t,zT),sh(q,zB),sh(q,b+k)-UF,sh(t,b+l)-UH]
   for who in ('G','I','RB','RT'):
    if who=='G':own,denom=UG,p+t+f+1
    elif who=='I':own,denom=UI,p+q+h+1
    elif who=='RB':own,denom=sh(k,b+1),b+1
    else:own,denom=sh(l,b+1),b+1
    row.extend(F(x,denom)-own for x in bits)
   row.extend([-sh(q*(k-l),b*(b+1)),-sh(t*(l-k),b*(b+1)),-F(k-l,b+1)])
   for ai in range(6):row.extend(F(x,sum(a[:ai])+6-ai) for x in hidden)
   row.extend(map(F,hidden));assert len(row)==len(names)
   scaled=[v*60 for v in row];assert all(v.denominator==1 for v in scaled)
   tab.append([int(v) for v in scaled])
  tables.append(tab)
 return states,names,np.array(tables,dtype=np.int16)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--point',default='../research_5/compact_B_QR_L_word_5259.json');ap.add_argument('--prefix',default='swap_B_L_visible_5259');ap.add_argument('--omit-minimum',action='store_true');a=ap.parse_args();point=json.loads((HERE/a.point).read_text());states,names,tables=geometry();nv=len(names);ns=len(states);idx={s:j for j,s in enumerate(states)};weights=[F(0)]*ns
 for row in point['weights']:
  key=(tuple(map(int,row['actual_bits'])),*row['word'],row['Q'],row['R'],row['ell']//6);assert row['ell'] in (0,6);weights[idx[key]]+=F(row['weight'])
 ar=[];ac=[];av=[]
 for si,tab in enumerate(tables):
  for hi,co in enumerate(tab):
   ri=2*si+hi
   for j,v in enumerate(co):
    if v:ar.append(ri);ac.append(j);av.append(-float(v)/60)
   ar.append(ri);ac.append(nv+si);av.append(1.)
 A=coo_matrix((av,(ar,ac)),shape=(2*ns,nv+ns)).tocsr();obj=np.r_[np.zeros(nv),-np.array(list(map(float,weights)))];us=list(map(F,point['actual_utilities']));K=F(point['K']);r=us[3]
 for j,n in enumerate(names):
  if n.startswith('price:'):obj[j]=float(us[int(n.split(':')[1])])
  if n.startswith('cap:'):obj[j]=float(K)
 eq=np.zeros((1,nv+ns));eq[0,0]=eq[0,1]=1;bounds=[(0,None)]*nv+[(None,None)]*ns;bounds[names.index('tie')]=(None,None)
 if a.omit_minimum:bounds[names.index('minimumB')]=bounds[names.index('minimumT')]=(0,0)
 sol=linprog(obj,A_ub=A,b_ub=np.zeros(2*ns),A_eq=eq,b_eq=[1],bounds=bounds,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
 print(sol.success,sol.message,'separation',None if sol.fun is None else -sol.fun-float(r),flush=True);out={'status':'float discovery plus exact row recovery; not a half certificate','point':a.point,'omit_minimum':a.omit_minimum,'success':sol.success,'message':sol.message}
 if sol.success:
  lam=[F(float(v)).limit_denominator(10**7) for v in sol.x[:nv]];assert all(v>=0 for n,v in zip(names,lam) if n!='tie')
  budget=r*(lam[0]+lam[1])+sum(lam[j]*us[int(n.split(':')[1])] for j,n in enumerate(names) if n.startswith('price:'))+sum(lam[j]*K for j,n in enumerate(names) if n.startswith('cap:'))
  psi=[min(sum(F(int(v),60)*l for v,l in zip(co,lam)) for co in tab) for tab in tables];score=sum(w*v for w,v in zip(weights,psi))-budget
  print('exact score',str(score),float(score),'active',[(n,str(v)) for n,v in zip(names,lam) if v],flush=True)
  out.update({'lambda':{n:str(v) for n,v in zip(names,lam) if v},'exact_recovered_separation':str(score),'source_coefficient':str(lam[0]+lam[1]),'states':[[list(x[0]),*x[1:]] for x in states],'psi':[str(v) for v in psi],'complete_types':ns*2})
 (HERE/(a.prefix+'.json')).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
