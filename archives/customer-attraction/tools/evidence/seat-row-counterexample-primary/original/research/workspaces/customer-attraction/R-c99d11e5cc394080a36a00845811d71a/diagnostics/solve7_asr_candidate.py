import sys,json,itertools,numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
sys.path.insert(0,'/workspace/scratch/8f60daf7a28c/sevenchk/seven_checkpoint_review');import independent_seat_assets as a
n=6; D,A,B=a.setup(n)
def asr_coeff(route,I,J,owner):
 vals=[];r=n # t handled externally

def asr_row(route,t,I,J,owner):
 r=n-t
 # routed prefix p_j
 p=[route[q] for q in range(t)]
 pj=[p.count(j) for j in range(7)]
 # top r-1 seats by 1/(pj+k), collect tuples sorted desc
 seats=[(F(1,pj[j]+k),j,k) for j in range(7) for k in range(1,r+1)]
 seats=sorted(seats,key=lambda z:(-z[0],z[1],z[2]))[:r-1]
 # sum q coefficient for one customer type I
 m=len(I.bit_count() and range(1) or [])
 q=F(0)
 for j in range(7):
  if not (I>>j)&1:continue
  if I.bit_count()==1:
   q += sum(F(1,pj[j]+k) for k in range(1,r+1))
  else:
   pI=sum(pj[a] for a in range(7) if (I>>a)&1)
   q += r*F(1,pI+r)
 # top U owner membership
 sub=F(0)
 if (I>>owner)&1:
  sub=sum(F(1,pj[j]+k) for _,j,k in seats)
 # coefficient row u_t - (q-sub)/(6r+1)
 cnt=J.bit_count(); share=F(1,cnt) if (J>>t)&1 else F(0)
 return share-(q-sub)/F(6*r+1)

def solve(route,K):
 ds=[('base',d) for d in a.descriptions(n,[0,5,3,4])]
 # ASR row tuple owner,t
 ds += [('asr',owner,t) for owner in range(7) for t in range(n)]
 C=a.columns(n,route)
 M=[]
 for I,J in C:
  row=[]
  for item in ds:
   if item[0]=='base': row.append(float(a.row(n,I,J,item[1],D,A,B))/D)
   else: row.append(float(asr_row(route,item[2],I,J,item[1])))
  M.append(row)
 M=np.array(M);b=np.array([float(int(bool(J))-int(bool(I&K))/2) for I,J in C]);
 Aub=np.hstack([M,np.ones((len(C),1))]); c=np.r_[np.zeros(len(ds)),-1];res=linprog(c,A_ub=Aub,b_ub=b,bounds=[(0,None)]*len(ds)+[(None,None)],method='highs');return res,len(C),len(ds)
if __name__=='__main__':
 Dscan=json.load(open('/workspace/scratch/8f60daf7a28c/sevenchk/seven_maxima_new_rows/scan_n6_seat.json'));fails=[x for x in Dscan['failures'] if 'rounding_failed' not in x]
 for x in fails:
  r,nc,nr=solve(tuple(x['route']),x['target']);print(x['route'],x['target'],r.status,r.x[-1] if r.success else None,nc,nr,flush=True)
