"""Independent cap checks in Q[t]/(7t^2-60t+33), no teammate imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import json


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def mul(x, y):
    return (x[0]*y[0]-F(33, 7)*x[1]*y[1],
            x[0]*y[1]+x[1]*y[0]+F(60, 7)*x[1]*y[1])


def scale(c, x):
    return c*x[0], c*x[1]


def subtract(x, y):
    return add(x, scale(-1, y))


def positive(x):
    # The smaller root t lies strictly between 59/100 and 3/5.
    return min(x[0]+x[1]*F(59, 100), x[0]+x[1]*F(3, 5)) > 0


def polynomial(t):
    return 7*t*t-60*t+33


def expected_reciprocal(b, k, t):
    return sum((F(comb(k, j), b+1+j)*t**j*(1-t)**(k-j)
                for j in range(k+1)), F(0))


def main():
    assert polynomial(F(59, 100)) > 0 > polynomial(F(3, 5))
    assert 14*F(3, 5)-60 < 0
    zero, one, t = (F(0), F(0)), (F(1), F(0)), (F(0), F(1))
    assert add(add(scale(7, mul(t, t)), scale(-60, t)), scale(33, one)) == zero
    q = [zero, t, (F(1, 2), F(-1, 2)), (F(1, 2), F(-1, 2))]
    assert sum(x[0] for x in q) == 1 and sum(x[1] for x in q) == 0
    clients = [frozenset({1})]*4 + [frozenset({2}), frozenset({3})] + [frozenset({0, 2, 3})]*2

    def payoff(a, bg):
        return sum((F(1, 1+sum(x in client for x in bg))
                    for client in clients if a in client), F(0))

    cap = []
    for a in range(4):
        value = zero
        for b, c in product(range(4), repeat=2):
            value = add(value, scale(payoff(a, (b, c)), mul(q[b], q[c])))
        cap.append(value)
    rho = (F(-16, 7), F(52, 7))
    assert cap[1:] == [rho]*3
    assert positive(subtract(rho, cap[0]))
    assert positive(subtract(rho, scale(2, one)))
    W = zero
    for a, b, c in product(range(4), repeat=3):
        covered = sum(bool(client.intersection((a, b, c))) for client in clients)
        W = add(W, scale(covered, mul(mul(q[a], q[b]), q[c])))
    assert W == scale(3, rho)
    assert positive(subtract(W, scale(F(544, 87), one)))

    # Genuine cap realized by non-identical independent marginals.
    marginal2 = [F(0), F(3, 23), F(10, 23), F(10, 23)]
    product_caps = [sum((marginal2[b]*payoff(a, (1, b)) for b in range(4)), F(0))
                    for a in range(4)]
    assert product_caps == [F(26, 23), F(44, 23), F(44, 23), F(44, 23)]
    assert max(product_caps) < 2

    # Exact reciprocal finite-difference formula behind general convexity.
    finite_difference_checks = 0
    for b in (0, 1, 5, 19):
        for j in range(30):
            B = b+1+j
            delta2 = F(1, B+2)-F(2, B+1)+F(1, B)
            assert delta2 == F(2, B*(B+1)*(B+2)) > 0
            finite_difference_checks += 1
    jensen_checks = 0
    for b, k in product((0, 1, 5), range(9)):
        for x, y, lam in product((F(0), F(1, 5), F(2, 3), F(1)), repeat=3):
            assert expected_reciprocal(b, k, lam*x+(1-lam)*y) <= (
                lam*expected_reciprocal(b, k, x)+(1-lam)*expected_reciprocal(b, k, y))
            jensen_checks += 1
    report = {
        'scope': 'Independent fixed-instance iid/product cap and general convexity implementation checks',
        'number_field': 'Q[t]/(7t^2-60t+33), t in (59/100,3/5)',
        'rho': {'constant': str(rho[0]), 't_coefficient': str(rho[1])},
        'iid_query_payoffs': [[str(v) for v in a] for a in cap],
        'Z3': [str(v) for v in W],
        'independent_nonidentical_product_caps': [str(v) for v in product_caps],
        'finite_difference_checks': finite_difference_checks,
        'rational_jensen_checks': jensen_checks,
        'all_checks_passed': True,
        'not_claimed': ['general half coverage', 'aggregate security bridge', 'necessity of correlated opponents'],
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
