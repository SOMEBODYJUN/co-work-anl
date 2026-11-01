import importlib.util
from pathlib import Path
from scipy.optimize import linprog
from fractions import Fraction as F
import numpy as np
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('temp',P/'three_price_template_weak.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
for flavor in ['discounted','W']:
 A=[];b=[]
 for p in range(101):
  aa,bb,states=m.rows(F(2),p)
  for row,tar,state in zip(aa,bb,states):
   a,bt,c,q,r,d,l=state
   if flavor=='W':tar=F(2*a,p+a+bt+c) if a else F();tar+=int(p+a+bt+c>0)-min(1,d)
   A.append(row);b.append(tar)
 lp=linprog(np.ones(7),A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),bounds=(0,None),method='highs')
 print(flavor,lp.success,[str(F(v).limit_denominator(1000000)) for v in lp.x] if lp.success else lp.message)
