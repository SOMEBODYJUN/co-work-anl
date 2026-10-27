import sys,json,numpy as np
from scipy.optimize import linprog
sys.path.insert(0,'/workspace/scratch/8f60daf7a28c/sevenchk/seven_checkpoint_review');import independent_seat_assets as a
n=6;D,A,B=a.setup(n)
def solve(route,K):
 ds=a.descriptions(n,[0,5,3,4]);
 # one valid seat per (t,j), k=1 + count of j in future positions
 for t in range(n-1):
  for j in range(7):
   k=1+sum(route[q]==j for q in range(t+1,n)); ds.append(('seat',t,j,k))
 C=a.columns(n,route);M=np.array([[float(a.row(n,I,J,d,D,A,B))/D for d in ds] for I,J in C]); b=np.array([float(int(bool(J))-int(bool(I&K))/2) for I,J in C]);
 Aub=np.hstack([M,np.ones((len(C),1))]); c=np.r_[np.zeros(len(ds)),-1];res=linprog(c,A_ub=Aub,b_ub=b,bounds=[(0,None)]*len(ds)+[(None,None)],method='highs');return res,len(C),len(ds)
Dscan=json.load(open('/workspace/scratch/8f60daf7a28c/sevenchk/seven_maxima_new_rows/scan_n6_seat.json'));fails=[x for x in Dscan['failures'] if 'rounding_failed' not in x]
for x in fails:
 r,nc,nr=solve(tuple(x['route']),x['target']);print(x['route'],x['target'],r.status,r.x[-1] if r.success else None,nc,nr,flush=True)
