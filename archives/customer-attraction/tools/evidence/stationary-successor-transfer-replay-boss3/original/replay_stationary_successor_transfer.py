from fractions import Fraction as F
from math import floor
checked=0
for n in range(1,13):
    kappa=F(n,n+(n*n)//4)
    for b in range(16):
        for t in (0,1):
            for z in range(n+1):
                denom=b+t+z
                R=F(t,denom) if t else F(0)
                FF=F(z,n*denom) if z else F(0)
                slack=R-kappa*FF-kappa*F(n*t-z,n*(b+1))
                assert slack>=0,(n,b,t,z,slack)
                checked+=1
    if n>=2:
        k=n//2
        # Unnormalised masses 1 and n-k on (1,k),(0,1).
        R=F(1,1+k)
        FF=F(k,n*(1+k))+F(n-k,n)
        assert R/FF==kappa,(n,R,FF,kappa)
print({'checked':checked,'negative_slacks':0,'sharp_relaxation_cases':11})
