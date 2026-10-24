"""Exact finite implementation audit for Bernoulli optimal exchange kernels.

No finite audit is a substitute for the analytic all-m proof. This checks only
identities used to turn existing E2 subset constraints into the displayed kernel.
"""
from fractions import Fraction as F
from math import comb, factorial


def choose(n,k):
    return comb(n,k) if 0<=k<=n else 0


def run(limit=12):
    moments=betas=0
    grid=(F(0),F(1,7),F(1,3),F(1,2),F(6,7),F(1))
    for m in range(1,limit+1):
        for s in range(m+1):
            for c in range(s+1):
                for d in range(1,m+1):
                    factor=F(choose(s-c,d),choose(m,d))
                    beta=sum((F((-1)**j*choose(c,j), d+j+1)
                              for j in range(c+1)),F())
                    expected=F(factorial(c)*factorial(d),factorial(c+d+1))
                    assert beta==expected,(m,s,c,d,beta,expected)
                    betas += 1
                    for t in grid:
                        lhs=sum((F(choose(s-c,k)*choose(k,d),choose(m,d))*
                                 t**k*(1-t)**(s-k) for k in range(s+1)),F())
                        rhs=factor*t**d*(1-t)**c
                        assert lhs==rhs,(m,s,c,d,t,lhs,rhs)
                        moments += 1
    print({'status':'pass','m_limit':limit,'exact_moment_cases':moments,
           'exact_beta_cases':betas,
           'scope':'finite identity implementation audit; no SPE or half proof'})

if __name__=='__main__':run()
