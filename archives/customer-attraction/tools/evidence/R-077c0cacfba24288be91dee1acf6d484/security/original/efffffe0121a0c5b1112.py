"""Discovery: all ordered-history policies in anonymous exact-potential n=3 games.
Adds clone domination or full binary four-term taxes; floating MIP is not proof.
"""
import argparse,itertools,json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
P=argparse.ArgumentParser();P.add_argument('--k',type=int,default=3);P.add_argument('--tax',action='store_true');P.add_argument('--seconds',type=float,default=20);P.add_argument('--path',default='0,1,2');P.add_argument('--p',default=None);args=P.parse_args()
k=args.k;n=3;path=tuple(map(int,args.path.split(',')));p=np.ones(k) if args.p is None else np.array(list(map(float,args.p.split(','))));p/=sum(p)
p3=list(itertools.combinations_with_replacement(range(k),3));p2=list(itertools.combinations_with_replacement(range(k),2));i3={z:i for i,z in enumerate(p3)};i2={z:len(p3)+i for i,z in enumerate(p2)};d=len(p3)+len(p2)
hs=[h for l in range(3) for h in itertools.product(range(k),repeat=l)];vi={(h,j):d+3*i+j for i,h in enumerate(hs) for j in range(3)};zi={(h,a):d+3*len(hs)+k*i+a for i,h in enumerate(hs) for a in range(k)};t=d+(3+k)*len(hs);D=t+1
lo=np.r_[np.full(d,-20.),np.zeros((3+k)*len(hs)+1)];hi=np.r_[np.full(d,20.),np.full(3*len(hs),10.),np.ones(k*len(hs)),10.];integ=np.zeros(D);integ[list(zi.values())]=1
rows=[];lbs=[];ubs=[]
def add(r,l=-np.inf,u=np.inf):rows.append(r);lbs.append(l);ubs.append(u)
def unit(i):r=np.zeros(D);r[i]=1;return r
def U(a,H):
 r=np.zeros(D);r[i3[tuple(sorted((*H,a)))]]=1;r[i2[tuple(sorted(H))]]=-1;return r
def V(h,j):
 if len(h)<3:return unit(vi[(h,j)])
 return U(h[j],h[:j]+h[j+1:])
for H in p2:
 for a in range(k):add(U(a,H),0,10)
for h in range(k):
 for a,b in itertools.product(range(k),repeat=2):add(U(a,(h,b))-U(a,(h,a)),0)
 if args.tax:
  for a,b,c in itertools.product(range(k),repeat=3):add(U(b,(h,a))-U(b,(h,c))+U(a,(h,c))-U(a,(h,a)),0)
M=10.
for h in hs:
 r=sum((unit(zi[(h,a)]) for a in range(k)),np.zeros(D));add(r,1,1)
 for a in range(k):
  z=unit(zi[(h,a)])
  for j in range(3):
   diff=V(h,j)-V((*h,a),j)
   add(diff-M*z,-M);add(diff+M*z,u=M)
  add(V(h,len(h))-V((*h,a),len(h)),0)
for l,a in enumerate(path):add(unit(zi[(path[:l],a)]),1,1)
add(sum((V((),j) for j in range(3)),np.zeros(D)),1,1)
for H in p2:add(sum((p[a]*U(a,H) for a in range(k)),np.zeros(D))-unit(t),0)
c=np.zeros(D);c[t]=-1
sol=milp(c,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(np.array(rows),lbs,ubs),options={'time_limit':args.seconds,'mip_rel_gap':1e-7})
out={'success':sol.success,'status':sol.status,'message':sol.message,'bound':getattr(sol,'mip_dual_bound',None),'tax':args.tax,'p':p.tolist(),'path':path}
if sol.x is not None:
 out.update(value=sol.x[t],F=sol.x[:len(p3)].tolist(),G=sol.x[len(p3):d].tolist(),policy={str(h):int(np.argmax([sol.x[zi[(h,a)]] for a in range(k)])) for h in hs},p3=p3,p2=p2)
print(json.dumps(out,indent=2))
