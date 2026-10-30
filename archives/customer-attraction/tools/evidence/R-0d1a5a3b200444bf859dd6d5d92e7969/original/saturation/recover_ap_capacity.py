from search_ap_capacity import states,rows,q,names,R,v,cc,o,M
from fractions import Fraction as F
import scipy.optimize as so
import numpy as np
from pathlib import Path
import json
res=so.linprog([.21,1]+[0]*len(names),A_ub=M,b_ub=-o,bounds=[(0,None),(None,None)]+[(0,None)]*len(names),method='highs')
sel=[i for i,x in enumerate(res.x[2:]) if x>1e-8];rn=[names[i] for i in sel];vv=[res.x[0],res.x[1]]+list(res.x[2:][sel]);aa=np.column_stack([v,cc,-R[:,sel]])
tight=[j for j in range(len(states)) if abs(float(aa[j]@vv-o[j]))<1e-7]
exact=[];rhs=[]
for j in tight:
 b,d=states[j];rs=rows(b,d)
 exact.append([q(b[0],sum(b)),b[0]]+[-F(rs[n]) for n in rn]);rhs.append(int(d>0))
mat=[[F(x) for x in rr]+[F(y)] for rr,y in zip(exact,rhs)]
rank=0;piv=[]
for col in range(len(vv)):
 pi=next((j for j in range(rank,len(mat)) if mat[j][col]),None)
 if pi is None:continue
 mat[rank],mat[pi]=mat[pi],mat[rank];qq=mat[rank][col];mat[rank]=[x/qq for x in mat[rank]]
 for j in range(len(mat)):
  if j!=rank and mat[j][col]:
   qq=mat[j][col];mat[j]=[x-qq*y for x,y in zip(mat[j],mat[rank])]
 piv.append(col);rank+=1
assert rank==len(vv),(rank,len(vv))
ff=[F(0)]*len(vv)
for i,col in enumerate(piv):ff[col]=mat[i][-1]
print('support',rn,'tight',len(tight),'solution',ff)
assert all(x>=0 for x in ff[2:]) and ff[0]>=0
minimum=None;strmin=None
for b,d in states:
 rs=rows(b,d);z=ff[0]*q(b[0],sum(b))+ff[1]*b[0]-int(d>0)-sum(l*rs[n] for n,l in zip(rn,ff[2:]));zz=z-F(1,5)*(d-int(d>0))
 minimum=z if minimum is None else min(z,minimum);strmin=zz if strmin is None else min(zz,strmin)
 assert zz>=0,(b,d,zz)
print('min',minimum,'repeat-credit min',strmin)
print('inequality O <=',ff[0],'r +',ff[1],'K')
print('repetition inequality 4O+J <=',5*ff[0],'r +',5*ff[1],'K')
obj={'alpha':str(ff[0]),'beta':str(ff[1]),'rows':{n:str(l) for n,l in zip(rn,ff[2:])},'tight_count':len(tight),'repeat_credit':'1/5'}
Path(__file__).with_name('ap_capacity_exact.json').write_text(json.dumps(obj,indent=2)+'\n')
