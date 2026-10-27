from fractions import Fraction as F

def G(p,a,b,d,ell):
    den=p+a+b
    alpha=F(a,den) if den else F(0)
    beta=F(b,den) if den else F(0)
    return 6*alpha+beta/F(2)-F(d,p+1)-F(ell,12*(p+a+1))+F(d*ell,6*(p+1)*(p+2))

def K(p,a,b,e):
    den=p+a+b
    return (F(e,den) if den else F(0))-F(a,6)+((F(b,den) if den else F(0))-F(e,p+a+1))/5

def row(label,p,a,b,e1,e2,d,ell):
    rhs=F(2*(p+a+b>0)-(d>0))-G(p,a,b,d,ell)
    return label,rhs,K(p,a,b,e1),K(p,a,b,e2)

rows=[
 row('A client',2,1,0,0,0,1,0),
 row('outside, E1 only',1,0,0,1,0,1,0),
 row('outside, E2 only',1,0,0,0,1,1,0),
]
for r in rows: print(r)
assert rows[0][1]==F(-2,3) and rows[0][2]==rows[0][3]==F(-1,6)
assert rows[1][1]==F(3,2) and rows[1][2]==F(9,10) and rows[1][3]==0
assert rows[2][1]==F(3,2) and rows[2][2]==0 and rows[2][3]==F(9,10)
print('necessary: lambda1+lambda2 >= 4; lambda1 <= 5/3; lambda2 <= 5/3')
