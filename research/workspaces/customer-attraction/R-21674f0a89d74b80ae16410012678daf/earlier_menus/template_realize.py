from template_primal import A,y,states,res
from itertools import permutations,product
from fractions import Fraction as F
from math import lcm
from collections import defaultdict
import numpy as np
pat=list(product(range(2),repeat=3));r={}
for x,(p,a,b,c,hist) in zip(res.x,states):
 if x<=1e-8:continue
 coeff=F(float(x)).limit_denominator(1000000)
 seq=[]
 for h,v in zip(hist,pat):seq.extend([v]*h)
 perms=set(permutations(seq));coeff/=len(perms)
 for seq in perms:
  mask=a+2*b+4*c
  for j,(t,q,rr) in enumerate(seq):mask|=t<<(3+3*j);mask|=q<<(4+3*j);mask|=rr<<(5+3*j)
  r[mask]=r.get(mask,F(0))+coeff
k=12; util=np.zeros((k,k,k,3));wel=np.zeros((k,k,k))
for aa,bb,cc in product(range(k),repeat=3):
 for mask,x in r.items():
  bits=[(mask>>j)&1 for j in [aa,bb,cc]];ss=sum(bits)
  if ss:
   for i,bit in enumerate(bits):util[aa,bb,cc,i]+=float(x)*bit/ss
   wel[aa,bb,cc]+=float(x)
feas={}
for aa in range(k):
 menus=[]
 for bb in range(k):
  vals=util[aa,bb,:,2];mx=max(vals);br=[cc for cc in range(k) if vals[cc]>=mx-1e-8]
  menus.append(br)
 threshold=max(min(util[aa,bb,cc,1] for cc in br) for bb,br in enumerate(menus))
 feas[aa]=[(bb,cc) for bb,br in enumerate(menus) for cc in br if util[aa,bb,cc,1]>=threshold-1e-8]
 print('root',aa,'twoSPE',feas[aa],'rootfloor',min(util[aa,bb,cc,0] for bb,cc in feas[aa]))
print('ABC',util[0,1,2],wel[0,1,2], 'pair feasible',(1,2) in feas[0])
print('root maxfloors',max(min(util[aa,bb,cc,0] for bb,cc in feas[aa]) for aa in range(k)))
print('fixedbranch endbr')
for j in range(3):
 aa=3+3*j;bb=aa+1;cc=aa+2; print(j,util[aa,bb,cc],(bb,cc) in feas[aa],min(util[aa,bb,cc,0] for bb,cc in feas[aa]))
