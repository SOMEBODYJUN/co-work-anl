from fractions import Fraction
from itertools import product
weights={1:Fraction(4,13),2:Fraction(5,13),4:Fraction(3,13),8:Fraction(3,13),20:Fraction(2,13),24:Fraction(2,13),36:Fraction(2,13),40:Fraction(2,13),49:Fraction(2,13),50:Fraction(2,13)}
p=6; rho=(1,4,4,4,5,4)
def u(a,b,i,B):
    bit=(a,b)[i]
    if not (B>>bit)&1:return Fraction(0)
    return Fraction(1, ((B>>a)&1)+((B>>b)&1))
rows=[]
for a,b in product(range(p),repeat=2):
    lhs=sum(w*u(a,rho[a],1,B) for B,w in weights.items())
    rhs=sum(w*u(a,b,1,B) for B,w in weights.items())
    rows.append((f'follower a={a} b={b}',lhs-rhs))
for b in range(p):
    lhs=sum(w*u(0,1,0,B) for B,w in weights.items())
    rhs=sum(w*u(b,rho[b],0,B) for B,w in weights.items())
    rows.append((f'root b={b}',lhs-rhs))
C=sum(w for B,w in weights.items() if ((B>>0)&1) or ((B>>1)&1))
R=sum(w for B,w in weights.items() if not (((B>>0)&1) or ((B>>1)&1)) and (((B>>2)&1) or ((B>>3)&1)))
print('sum',sum(weights.values()),'C',C,'R',R,'objective',C-R)
print('violations',[(n,v) for n,v in rows if v<0])
print('min_slack',min(v for _,v in rows))
for n,v in rows: print(n,v)
