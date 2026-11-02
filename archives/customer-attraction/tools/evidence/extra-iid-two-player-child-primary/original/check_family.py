"""Independent Fraction audit of the subset-design branch mechanism."""
from fractions import Fraction as F
from math import comb

def g(t):
    return 1-t+t*t/3

def audit(m, s, copies, private, expected_gap=None):
    M = copies * comb(m, s)
    d = copies * comb(m-1, s-1)
    e = copies * comb(m-2, s-2) if s >= 2 else 0
    t, G = F(s, m), g(F(1, m))
    alpha_h = M*g(t)
    lam = d*g(t)+private*G
    L_N = (M-d)*g(t)/G
    U_B = M-F(3, 2)*d+F(1, 2)*e
    U_D = d*(g(t)-F(1, 2))/(1-G)
    assert max(F(M-d, 2), L_N) <= private <= U_B
    assert private < U_D
    assert alpha_h <= lam
    # Exhaust all two-player actions by their three actual types.
    # At hub: hub, each peripheral.
    at_h = [F(M, 2)] + [F(d, 2)+private]*m
    assert at_h[1] == max(at_h)
    # At any peripheral: hub, same peripheral, each other peripheral.
    at_p = [M-F(d, 2), F(d+private, 2)] + [d+private-F(e, 2)]*(m-1)
    assert at_p[0] == max(at_p)
    first_h = M-F(d, 2)
    first_p = F(d, 2)+private
    assert first_h >= first_p
    assert first_p < lam < first_h
    if expected_gap is not None:
        assert lam-first_p == expected_gap
    return {"m":m, "s":s, "copies":copies, "private":private,
            "clients": M+m*private, "lambda":str(lam),
            "q_real_mean":str(first_p), "first":str(first_h),
            "gap":str(lam-first_p)}

print(audit(8,4,1,24,F(1,24)))
for m in range(8, 22, 2):
    C=comb(m,m//2)
    M=3*C
    gap=F(M*(3*m*m-24*m+8),72*m*m)
    result=audit(m,m//2,3,C,gap)
    assert gap > 0
    assert g(F(1,m)) > F(7,8)
    assert F(M*(m-4),24*(m-1)) > 0
    print(result)
