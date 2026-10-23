"""Independent unit-client audit of the two-PNE/three-iid obstruction."""
from fractions import Fraction as F

def g(z):
    # Direct Binomial(2,z) expectation, not the simplified polynomial.
    return (1-z)**2 + 2*z*(1-z)*F(1,2) + z*z*F(1,3)

m=26
A,B=0,1
clients=[]
for block in (A,B):
    for j in range(m):
        interests={block, 2+j, 2+(j+1)%m, 2+(j+2)%m}
        clients.extend([interests.copy(), interests.copy()])
for j in range(m):
    clients.extend([{2+j} for _ in range(2*m-9)])
themes=[{x for x,C in enumerate(clients) if a in C} for a in range(m+2)]
q=[F(0),F(0)]+[F(1,m)]*m

def utility(a, rivals):
    return sum((F(1,1+sum(x in themes[b] for b in rivals))
                for x in themes[a]),F(0))

assert len(clients)==m*(2*m-5)==1222
assert len(themes[A])==len(themes[B])==2*m
assert all(len(themes[a])==2*m+3 for a in range(2,m+2))
assert utility(A,(B,))==utility(B,(A,))==2*m
assert utility(B,(A,))==max(utility(c,(A,)) for c in range(m+2))
assert utility(A,(B,))==max(utility(c,(B,)) for c in range(m+2))

coverage_prob=[sum((q[a] for a in C),F(0)) for C in clients]
alpha=[sum((g(coverage_prob[x]) for x in themes[a]),F(0))
       for a in range(m+2)]
lam=sum((q[a]*alpha[a] for a in range(m+2)),F(0))
assert all(v<=lam for v in alpha)
assert all(q[a]==0 or alpha[a]==lam for a in range(m+2))
assert alpha[A]==alpha[B]==2*m-6+F(6,m)
assert lam==2*m+1-F(79,3*m)+F(33,m*m)
assert lam-2*m==F(73,2028)>0
assert lam==F(105529,2028)

for n in range(26,101):
    assert F(3*n*n-79*n+99,3*n*n)>0
    assert 7-F(97,3*n)+F(33,n*n)>0
    assert 12*g(F(3,n))+(2*n-9)*g(F(1,n)) == 2*n+1-F(79,3*n)+F(33,n*n)
print({"m":m,"clients":len(clients),"PNE_payoffs":[2*m,2*m],
       "lambda3":str(lam),"gap":str(lam-2*m),
       "outside_query":str(alpha[A]),"max_single_topic":2*m+3})
