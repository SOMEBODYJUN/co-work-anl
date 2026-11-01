from fractions import Fraction
from itertools import product,combinations_with_replacement
import numpy as np, json, hashlib, scipy, sys
from scipy.optimize import milp,Bounds,LinearConstraint
src='cleanup/workspaces/Boss7/current-batch/36628191e3d12eec94ce/source.py'
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
def u(a,b,i,B):
    return Fraction(1,int(B>>a&1)+int(B>>b&1)) if B>>(a,b)[i]&1 else Fraction(0)
def cov(a,b):return np.array([int(bool(B>>a&1 or B>>b&1)) for B in masks],dtype=float)
rows=[]; labels=[]
for a,b in product(range(p),repeat=2):
    rows.append([2*(u(a,rho[a],1,B)-u(a,b,1,B)) for B in masks]); labels.append(('response',a,b))
for b in range(p):
    rows.append([2*(u(0,1,0,B)-u(b,rho[b],0,B)) for B in masks]); labels.append(('root',b))
C=cov(0,1);O=cov(2,3);R=O*(1-C)
A=[np.array(row,dtype=float) for row in rows];lower=[0]*len(A);
A.append(R-C); lower.append(1); labels.append(('cover-gap',))
for a,b in combinations_with_replacement(range(p),2):
    if (a,b)==(2,3):continue
    A.append(O-cov(a,b));lower.append(1);labels.append(('omit',a,b))
A=np.array(A);lower=np.array(lower)
for integer in (False,True):
    res=milp(np.ones(len(masks)),integrality=np.ones(len(masks)) if integer else None,bounds=Bounds(np.zeros(len(masks)),np.full(len(masks),np.inf)),constraints=LinearConstraint(A,lower,np.full(len(A),np.inf)),options={'time_limit':120})
    print('integer',integer,'status',res.status,res.message,'fun',res.fun,'gap',getattr(res,'mip_gap',None))
    if res.x is None:continue
    print('nonzero',[(B,x) for B,x in zip(masks,res.x) if x>1e-7])
    sl=A@res.x-lower
    print('min slack',sl.min(),'near zero',sum(abs(x)<1e-7 for x in sl))
    print('tight labels',[(labels[i],float(sl[i])) for i in range(len(sl)) if abs(sl[i])<1e-7])
    if integer:
      w={B:int(round(x)) for B,x in zip(masks,res.x) if x>.5}
      def sumu(a,b,i):return sum(Fraction(w.get(B,0))*u(a,b,i,B) for B in masks)
      print('root payoffs',[(b,sumu(0,1,0)-sumu(b,rho[b],0)) for b in range(6)])
      print('resp min',min((sumu(a,rho[a],1)-sumu(a,b,1),a,b) for a,b in product(range(6),repeat=2)))
      print('C,O,R',sum(w.get(B,0)*int(C[j]) for j,B in enumerate(masks)),sum(w.get(B,0)*int(O[j]) for j,B in enumerate(masks)),sum(w.get(B,0)*int(R[j]) for j,B in enumerate(masks)))
      print('hash',hashlib.sha256(open(src,'rb').read()).hexdigest())
      json.dump({'source_sha256':hashlib.sha256(open(src,'rb').read()).hexdigest(),'masks':masks,'rho':rho,'weights':w,'objective':sum(w.values()),'rows':labels,'slacks_float':[float(x) for x in sl],'scipy_version':scipy.__version__},open('evidence.json','w'),indent=2)
