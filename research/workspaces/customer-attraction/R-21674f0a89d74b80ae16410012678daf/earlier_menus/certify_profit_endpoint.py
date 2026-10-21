from probe_tax_endpoint import rows
from fractions import Fraction as F
from scipy.optimize import linprog
import numpy as np,json
from pathlib import Path
A,y,states=rows(3,[0,1,2])
ncols=A.shape[1]; nstates=len(states)//3
# rows() outer loop histogram,p,abc. use mapping.
mat={}
for rr,st in zip(A,states):mat[st]=[F(float(v)).limit_denominator(1000000) for v in rr]
coefs=[];targets=[];coefstates=[]
for p,a,b,c,hist in states:
 if p:continue
 vals=[]; yy=[]
 d=sum(hist[i]*((i>>2)&1) for i in range(8));s=a+b+c
 for pp in range(3):
  D=(pp+1)*(pp+2)*(pp+3)
  vals.append([v*D for v in mat[(pp,a,b,c,hist)]])
  tar=(F(s+3*a,pp+s) if s else 0)-(F(d,pp+d) if d else 0)
  yy.append(tar*D)
 for kk in range(ncols):pass
 row0=vals[0]; row2=[(v2-2*v1+v0)/2 for v0,v1,v2 in zip(*vals)];row1=[v1-v0-v2 for v0,v1,v2 in zip(vals[0],vals[1],row2)]
 tar0=yy[0];tar2=(yy[2]-2*yy[1]+yy[0])/2;tar1=yy[1]-yy[0]-tar2
 coefs.extend([row0,row1,row2]);targets.extend([tar0,tar1,tar2]);coefstates.extend([(a,b,c,hist,j) for j in range(3)])
AA=np.array(coefs,dtype=float);bb=np.array(targets,dtype=float)
r=linprog(np.ones(ncols),A_ub=AA,b_ub=bb,bounds=(0,None),method='highs')
print('success',r.success,'sum',r.fun,flush=True)
if not r.success:raise SystemExit
support=[j for j,x in enumerate(r.x) if x>1e-7]
print('support',[(j,r.x[j]) for j in support])
for maxden in [100,1000,10000,100000,1000000,10000000]:
 xx=[F(float(v)).limit_denominator(maxden) for v in r.x]
 slacks=[b-sum(a*x for a,x in zip(row,xx)) for row,b in zip(coefs,targets)]
 print(maxden,min(slacks),sum(v<0 for v in slacks),flush=True)
 if min(slacks)>=0:
  out={'status':'exact_polynomial_certificate','claim':'F3(p)-R<=3u_first','rows':93,'states':nstates,'coefficients':2880,'multipliers':{str(j):str(xx[j]) for j in support},'min_coefficient_slack':str(min(slacks))}
  Path(__file__).with_name('profit_endpoint_certificate.json').write_text(json.dumps(out,indent=2)+'\n');break
