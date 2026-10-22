"""Definition-level Fraction audit; no solver, optimizer, or discovery imports."""
from fractions import Fraction as F
from itertools import product
import json


def harmonic(n):
    return sum((F(1,j) for j in range(1,n+1)), F(0))


def audit(r):
    topics=({0},set(range(1,r+1)))
    def action(h): return 0 if not h else 1
    def finish(h):
        while len(h)<r: h=h+(action(h),)
        return h
    def payoff(z,i):
        loads=[sum(x in topics[a] for a in z) for x in range(r+1)]
        return sum((F(1,loads[x]) for x in topics[z[i]]),F(0))
    checked=0
    for depth in range(r):
        for h in product(range(2),repeat=depth):
            chosen=payoff(finish(h),depth)
            for a in range(2):
                assert chosen>=payoff(finish(h+(a,)),depth)
                checked+=1
    z=finish(())
    u=payoff(z,0)
    tail=sum((payoff(z,i) for i in range(1,r)),F(0))
    assert u==1 and tail==r
    assert finish((0,))[1:]==finish((1,))[1:]==(1,)*(r-1)
    psi=r*harmonic(r-1)
    theta=min(F(1,1+k)+harmonic(k)/2 for k in range(r))
    assert theta==1
    e=r*(harmonic(r-1)/2-F(r-1,r))
    price=F(r-1)
    balance=e-(psi-tail)/2
    assert balance==tail/2-price==1-F(r,2)
    assert price==(1-F(1,r))*tail
    # Direct price certificate on [0,1]^2: the objective is affine there.
    assert max(r*z_b-z_a-z_b for z_a,z_b in product((0,1),repeat=2))==price
    return dict(players=r,unit_customers=r+1,histories=(1<<r)-1,
                comparisons_including_self=checked,root_utility=str(u),
                tail_profit=str(tail),harmonic_potential=str(psi),
                protected_price=str(price),pointwise_slack=str(e),
                half_profit_balance=str(balance))


if __name__=='__main__':
    print(json.dumps(dict(status='PASS',scope='finite arithmetic and complete-strategy regression; universal proof is in the note',
                         cases=[audit(r) for r in range(2,11)]),indent=2))
