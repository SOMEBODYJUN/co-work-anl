import itertools,numpy as np,json
from fractions import Fraction as Q
from scipy.optimize import linprog
names=['KQ','KR','Psum','Zsum','Ssum+Vsum/3','F','Jsum']
rows=[];bounds=[];states=[]
for a,b,c,q,r in itertools.product((0,1),repeat=5):
 for ts in itertools.product((0,1),repeat=3):
  for ls in itertools.product((0,1),repeat=3):
   d=sum(ts);ell=sum(ls);h=sum(t*l for t,l in zip(ts,ls));w=int(a+b+c>0);o=int(d>0)
   alpha=Q(a,a+b+c)if a else Q(0);beta=Q(b,a+b+c)if b else Q(0);gamma=Q(c,a+b+c)if c else Q(0)
   fc=Q(c,c+q+r)if c else Q(0);fr=Q(r,c+q+r)if r else Q(0);D=(1+a)*(2+a)
   slack=[3*alpha-q,3*alpha-r,3*gamma-Q(d,1+a+b),3*gamma-Q(ell,1+a+b),3*beta-Q(d,1+a)+Q(d*ell,3*D),alpha-fc,3*fr-Q(d,1+c+q)]
   rows.append(list(map(float,slack)));bounds.append(float(w+3*alpha-o));states.append((a,b,c,q,r,d,ell))
res=linprog(np.ones(len(names)),A_ub=np.array(rows),b_ub=np.array(bounds),bounds=[(0,None)]*len(names),method='highs')
print(res.message)
if res.success:print({n:str(Q(v).limit_denominator(1000000))for n,v in zip(names,res.x)},'min',min(np.array(bounds)-np.array(rows)@res.x))
else:
 # Optimize smallest root coefficient beta >=? Target W+t alpha-O
 aa=np.array([[*row,-float(Q(state[0],sum(state[:3]))if state[0]else 0)]for row,state in zip(rows,states)])
 bb=np.array([v-3*float(Q(st[0],sum(st[:3]))if st[0]else 0)for v,st in zip(bounds,states)])
 rr=linprog([0]*len(names)+[1],A_ub=aa,b_ub=bb,bounds=[(0,None)]*(len(names)+1),method='highs')
 print(rr.message,rr.x)
