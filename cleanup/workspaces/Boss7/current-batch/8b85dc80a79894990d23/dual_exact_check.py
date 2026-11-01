from fractions import Fraction as F
from itertools import product,combinations_with_replacement
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
def u(a,b,i,B): return F(1,int(B>>a&1)+int(B>>b&1)) if (B>>(a,b)[i]&1) else F(0)
def cov(a,b,B): return F(int(bool(B>>a&1 or B>>b&1)))
rows=[]; labels=[]
for a,b in product(range(p),repeat=2): rows.append([-(u(a,rho[a],1,B)-u(a,b,1,B)) for B in masks]); labels.append(('rho',a,b))
for b in range(p): rows.append([-(u(0,1,0,B)-u(b,rho[b],0,B)) for B in masks]); labels.append(('root',b))
C=[cov(0,1,B) for B in masks]; O=[cov(2,3,B) for B in masks]; R=[O[i]*(1-C[i]) for i in range(len(masks))]
rows.append([-(R[i]-C[i]) for i in range(len(masks))]); labels.append(('residual',))
bs=[F(0)]*(len(rows)-1)+[F(-1,100)]
for a,c in combinations_with_replacement(range(p),2):
 if (a,c)==(2,3): continue
 rows.append([cov(a,c,B)-O[i] for i,B in enumerate(masks)]); labels.append(('pair',a,c)); bs.append(F(0))
ys={
('rho',0,2):F(-9,11),('rho',0,3):F(-9,11),('rho',0,4):F(-6,77),('rho',0,5):F(-8,77),
('rho',2,3):F(-1,11),('rho',2,5):F(-8,77),('rho',4,1):F(-6,77),('rho',4,3):F(-6,77),('rho',5,1):F(-8,77),('rho',5,3):F(-8,77),
('root',2):F(-3,11),('root',4):F(-4,11),('residual',):F(-13,22),('pair',1,2):F(-1,2),('pair',1,3):F(-1,2)}
y=[ys.get(tuple(l),F(0)) for l in labels]; lam=F(-1,22)
# scipy min dual: A^T y + C*lam >=? check values
z=[sum(y[j]*rows[j][i] for j in range(len(rows))) + lam*C[i] for i in range(len(masks))]
zg=sum(y[j]*0 for j in range(len(rows))) # g coeff from pair ys only
# g col is 1 on pair rows
zg=sum(y[j] for j,l in enumerate(labels) if l[0]=='pair')
print('dual objective',sum(bs[j]*y[j] for j in range(len(rows)))+lam,'target',F(-87,2200))
print('g coefficient',zg,'target -1')
print('w coeff range',min(z),max(z),'all <=0?',all(v<=0 for v in z),'all >=0?',all(v>=0 for v in z))
print([(B,z[i]) for i,B in enumerate(masks) if z[i]])
