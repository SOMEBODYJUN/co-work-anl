"""Independent Fraction reconstruction of integer/fractional terminal projection."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)


def main():
    slack_checks = corner_checks = tax_checks = 0
    weight_sets = [(F(1, 3),)*3, (F(1, 2), F(3, 4)),
                   (F(2), F(1, 2), F(1, 3)), (F(1),)*3]
    for p, a, b in product(range(16), range(2), range(2)):
        alpha, beta = share(a, p+a+b), share(b, p+a+b)
        w = int(p+a+b > 0)
        tax = F(p, p+1) if p else F(0)
        fresh = int(p == 0 and a == 1)
        assert tax+beta+F(fresh, 2) <= w
        tax_checks += 1
        D = (p+1)*(p+2)
        for weights in weight_sets:
            tau = sum(weights)
            for T in product(range(2), repeat=len(weights)):
                for R in product(range(2), repeat=len(weights)):
                    d = sum(z*t for z, t in zip(weights, T))
                    ell = sum(z*r for z, r in zip(weights, R))
                    h = sum(z*t*r for z, t, r in zip(weights, T, R))
                    S = tau*alpha-sum(z*share(t, p+1+r)
                                      for z, t, r in zip(weights, T, R))
                    Z = tau*beta-sum(z*share(r, p+a+1)
                                     for z, r in zip(weights, R))
                    V = sum(weights[i]*weights[j]*(share(R[i], p+1+T[i])
                                                   -share(R[j], p+1+T[i]))
                            for i in range(len(weights)) for j in range(len(weights)))
                    assert S == tau*alpha-d/(p+1)+h/D
                    assert Z == tau*beta-ell/(p+a+1)
                    assert V == (d*ell-tau*h)/D
                    G = S+Z/(2*tau)+V/tau
                    formula = tau*alpha+beta/2-d/(p+1)-ell/(2*tau*(p+a+1))+d*ell/(tau*D)
                    assert G == formula
                    r = min(F(1), d)-d/(p+1)-ell/(2*tau*(p+a+1))+d*ell/(tau*D)
                    assert r <= tax+F(fresh, 4)
                    slack_checks += 1
        for tau in [F(1), F(10, 9), F(5, 4), F(3, 2), F(2), F(10), F(101, 3)]:
            for d, ell in product([F(0), F(1), tau], [F(0), tau]):
                r = min(F(1), d)-d/(p+1)-ell/(2*tau*(p+a+1))+d*ell/(tau*D)
                assert r <= tax+F(fresh, 4)
                corner_checks += 1
    out = {"status": "passed exact arithmetic reconstruction",
           "slack_membership_checks": slack_checks,
           "corner_checks": corner_checks, "tax_checks": tax_checks,
           "scope": "arbitrary fixed prefix, actual last two players; fractional query weights"}
    Path(__file__).with_name("terminal_projection_review_audit.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
