from fourcopy_discover import build
from scipy.optimize import linprog
from fractions import Fraction as F
from pathlib import Path
import json,numpy as np,time
start=time.time();bits,paths,names,rows,ocoef,vT=build(6,4)
# normalized x=lambda/B,y=C/B,z=1/B; maximize 2z-y.
A=np.column_stack([rows,-bits[:,0],np.zeros(len(bits))])
eq=np.r_[-ocoef,0,-1][None,:]
c=np.r_[np.zeros(len(names)),1,-2]
r=linprog(c,A_ub=A,b_ub=vT,A_eq=eq,b_eq=[0],bounds=[(0,None)]*len(names)+[(None,None),(0,None)],method='highs')
print(r.success,r.message,'threshold',-r.fun,'seconds',time.time()-start,flush=True)
if r.success:
 z=r.x[-1];B=1/z;C=r.x[-2]/z
 out=dict(n=6,copies=4,paths=paths,bits=len(bits[0]),B=str(F(float(B)).limit_denominator(10**8)),B_float=B,C=str(F(float(C)).limit_denominator(10**8)),threshold_float=-r.fun,multipliers={k:str(F(float(x/z)).limit_denominator(10**8)) for k,x in zip(names,r.x[:-2]) if x>1e-8},status='float discovery; exact recovery required')
 print('B,C',B,C,flush=True)
 (Path(__file__).resolve().parent/'fourcopy_threshold_discovery.json').write_text(json.dumps([out],indent=2)+'\n')
