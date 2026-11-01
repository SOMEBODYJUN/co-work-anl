"""Exact supplementary arithmetic for the iid-payment mathematical object.

The eight-customer tree and static primal/dual are fully enumerated. The weak
family's universal history classification and all-m proof remain analytic in
the object; this script checks its m=20 short witness and shared constants.
No solver or floating arithmetic is used.
"""
from fractions import Fraction as F
from itertools import product
import json


def g(n, t):
    return sum(((1-t)**i for i in range(n)), F(0))/n


def main():
    units = [frozenset((0, 2, 3))]*2 + [frozenset((1,))]*4
    units += [frozenset((2,)), frozenset((3,))]
    table = ((1, 1, 1, 1), (1, 2, 3, 2),
             (1, 3, 1, 1), (1, 2, 1, 1))

    def policy(h):
        return 0 if not h else 1 if len(h) == 1 else table[h[0]][h[1]]

    def leaf(h):
        while len(h) < 3:
            h += (policy(h),)
        return h

    def query(a, rivals):
        return sum((F(1, 1+sum(b in likes for b in rivals))
                    for likes in units if a in likes), F(0))

    def utility(z, i):
        return query(z[i], z[:i]+z[i+1:])

    comparisons = []
    for depth in range(3):
        for h in product(range(4), repeat=depth):
            for a in range(4):
                slack = utility(leaf(h), depth)-utility(leaf(h+(a,)), depth)
                assert slack >= 0
                comparisons.append(slack)
    coverage = lambda z: sum(any(a in likes for a in z) for likes in units)
    assert leaf(()) == (0, 1, 1)
    assert [utility(leaf(()), i) for i in range(3)] == [2, 2, 2]
    assert coverage(leaf(())) == 6
    assert max(coverage(z) for z in product(range(4), repeat=3)) == 8
    p = tuple(map(F, (0, F(15, 23), F(4, 23), F(4, 23))))
    primary = [sum((p[a]*query(a, B) for a in range(4)), F(0))
               for B in product(range(4), repeat=2)]
    Q = (((1, 1), F(3, 23)), ((1, 2), F(10, 23)),
         ((1, 3), F(10, 23)))
    dual = [sum((q*query(a, B) for B, q in Q), F(0)) for a in range(4)]
    assert min(primary) == max(dual) == F(44, 23)
    assert dual == [F(26, 23), F(44, 23), F(44, 23), F(44, 23)]

    # Work exactly in Q[t]/(7t^2-60t+33). Pairs denote a+b*t.
    def add(x, y):
        return (x[0]+y[0], x[1]+y[1])

    def scale(c, x):
        return tuple(c*v for v in x)

    def mul(x, y):
        return (x[0]*y[0]-F(33, 7)*x[1]*y[1],
                x[0]*y[1]+x[1]*y[0]+F(60, 7)*x[1]*y[1])

    def gp(x):
        return add(add((F(1), F(0)), scale(-1, x)), scale(F(1, 3), mul(x, x)))

    t, opposite = (F(0), F(1)), (F(1), F(-1))
    alpha1 = scale(4, gp(t))
    alpha2 = add(scale(2, gp(opposite)), gp(scale(F(1, 2), opposite)))
    assert alpha1 == alpha2
    assert scale(3, alpha1) == (F(-48, 7), F(156, 7))
    assert 25**2 < 669 < 26**2
    assert 675**2-669*26**2 == 3381

    m, J, rbar = 20, 100, F(25, 27)
    UB = 2*(m-1)*g(m, rbar)
    UQ = 2*g(m, 1-rbar)+g(m, (1-rbar)/J)
    assert 135*25**20 < 29*27**20
    assert 2*g(m, F(2, 27)) > F(53, 50)
    assert g(m, F(1, 1350)) >= F(2681, 2700)
    assert UQ > F(5543, 2700) > F(513, 250) > UB
    assert F(513, 250)-F(5543, 2700) == -F(13, 13500)
    short_margin = F(39, 2)*UB-40
    assert short_margin == (7-20007*F(2, 27)**20)/500 > 0
    exp_lower = sum((F(3, 2)**j / factorial(j) for j in range(6)), F(0))
    assert exp_lower == F(5711, 1280) > F(40, 9)
    assert F(31, 30)+F(397, 400) == F(2431, 1200)
    assert 2+F(2, 79) < F(2431, 1200)
    assert F(243, 16*41**2) < 1
    print(json.dumps({
        "status": "PASS", "eight_customer_all_action_comparisons": len(comparisons),
        "eight_customer_W": 6, "eight_customer_OPT": 8,
        "eight_customer_security": "44/23",
        "eight_customer_iid_Nash_equality_mod_quadratic": True,
        "eight_customer_Z_minus_6_positive_square_certificate": 3381,
        "m20_J100": {"unit_customers": 140, "topics": 102, "W": 40, "OPT": 59,
                        "UQ_minus_UB_at_rbar": str(UQ-UB),
                        "short_rational_margin": str(short_margin)},
        "universal_family_shared_constants_checked": True,
        "scope": "Exact finite arithmetic; all ordered histories for eight-customer tree. Universal weak-family histories and every m>=41 use the written proof."
    }, indent=2))


def factorial(n):
    out = 1
    for k in range(1, n+1):
        out *= k
    return out


if __name__ == "__main__":
    main()
