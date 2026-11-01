from fractions import Fraction
from itertools import product,combinations_with_replacement
p=6;masks=list(range(1,1<<p));rho=(1,4,4,4,5,4)
weights={1:Fraction(523,2200),2:Fraction(147,550),4:Fraction(403,1100),8:Fraction(501,2200),17:Fraction(87,2200),18:Fraction(109,1100),24:Fraction(61,440),33:Fraction(87,2200),34:Fraction(109,1100),40:Fraction(61,440),49:Fraction(61,440),52:Fraction(61,440),54:Fraction(87,2200),58:Fraction(87,2200)}
def u(a,b,i,B):
    return Fraction(1,int(B>>a&1)+int(B>>b&1)) if (B>>(a,b)[i]&1) else Fraction(0)
def cov(a,b,B): return int(bool(B>>a&1 or B>>b&1))
def dot(fn): return sum(w*fn(B) for B,w in weights.items())
print('sum',sum(weights.values()),'C',dot(lambda B:cov(0,1,B)),'O',dot(lambda B:cov(2,3,B)),'R',dot(lambda B:cov(2,3,B)*(1-cov(0,1,B))))
print('residual-minus-C',dot(lambda B:cov(2,3,B)*(1-cov(0,1,B))-cov(0,1,B)))
mins=[]
for a,b in product(range(p),repeat=2): mins.append(('rho',a,b,dot(lambda B,a=a,b=b:u(a,rho[a],1,B)-u(a,b,1,B))))
for b in range(p): mins.append(('root',b,dot(lambda B,b=b:u(0,1,0,B)-u(b,rho[b],0,B))))
print('min BR',min(x[-1] for x in mins),[x for x in mins if x[-1]==min(y[-1] for y in mins)])
opt=dot(lambda B:cov(2,3,B))
gaps=[]
for a,c in combinations_with_replacement(range(p),2):
 if (a,c)==(2,3):continue
 gaps.append((opt-dot(lambda B,a=a,c=c:cov(a,c,B)),a,c))
print('min static gap',min(gaps), 'all min', [x for x in gaps if x[0]==min(y[0] for y in gaps)])
