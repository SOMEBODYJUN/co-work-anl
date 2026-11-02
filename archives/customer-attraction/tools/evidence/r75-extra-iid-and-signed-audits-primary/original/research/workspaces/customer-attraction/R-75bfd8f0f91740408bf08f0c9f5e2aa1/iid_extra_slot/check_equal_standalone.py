"""Independent exact arithmetic audit of the equal-standalone two-player lemma.

The universal argument is in README.md; this script checks its identities and
inequality directions directly, without importing the research implementation.
"""
from fractions import Fraction as F
from itertools import product
from math import comb

checked=0
for background in range(10):
    for a,b in product((0,1),repeat=2):
        u=F(a,background+a+b) if a else F(0)
        f=F(a,background+1)
        collision=F(a*b,(background+1)*(background+2))
        assert u==f-collision
        checked+=1
    for t in [F(i,12) for i in range(13)]:
        pair=t*((1-t)*F(1,background+1)+t*F(1,background+2))
        for n in range(2,10):
            many=t*sum(F(comb(n-1,k))*t**k*(1-t)**(n-1-k)
                       /F(background+1+k) for k in range(n))
            assert many<=pair
            checked+=1
print({"exact_checks":checked,"status":"passed"})
