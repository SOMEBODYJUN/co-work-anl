import sys,json,itertools
from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,'/workspace/scratch/8f60daf7a28c/sevenchk/seven_checkpoint_review')
import independent_seat_assets as a

def cols(n,route): return a.columns(n,route)
def descs(n): return a.descriptions(n,[0,5,3,4])+[('seat',t,j,k) for t in range(n-1) for j in range(7) for k in range(1,n-t+1)]
def setup(n):return a.setup(n)
def solve(route,K):
 n=6; D,A,B=setup(n); ds=descs(n); C=cols(n,route)
 # rows matrix coefficients; residual target b = welfare - target/2; require sum lambda row <= b, maximize eps via -? impose b - A lam >= eps => A lam + eps <= b
 M=np.empty((len(C),len(ds)),dtype=float)
 for ri,desc in enumerate(ds): M[:,ri]=[float(a.row(n,I,J,desc,D,A,B))/D for I,J in C] # normalized
 b=np.array([float((int(bool(J))-int(bool(I&K))/2)) for I,J in C])
 # vars lambda nonnegative and eps free? maximize eps => min -eps; constraints M lam + eps <= b
 Aub=np.hstack([M,np.ones((len(C),1))]); c=np.zeros(len(ds)+1); c[-1]=-1
 res=linprog(c,A_ub=Aub,b_ub=b,bounds=[(0,None)]*len(ds)+[(None,None)],method='highs',options={'presolve':True})
 return res,ds,C,b,M
if __name__=='__main__':
 p='/workspace/scratch/8f60daf7a28c/sevenchk/seven_maxima_new_rows/scan_n6_seat.json'; d=json.load(open(p)); fails=[x for x in d['failures'] if 'rounding_failed' not in x]
 print('fails',len(fails))
 for ii,x in enumerate(fails):
  route=tuple(x['route']);K=x['target'];res,ds,C,b,M=solve(route,K)
  print(ii,route,K,'status',res.status,'eps',res.x[-1] if res.success else None,'ncol',len(C),'nrow',len(ds),flush=True)
