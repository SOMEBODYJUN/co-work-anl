"""Independent Fraction audit; imports no discovery code or SPE solver.

The universal result rests on the symbolic identities in the review, not these
finite checks. Arbitrary legal menu maps need not have rational followers.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import random


def harmonic_increment(base, count):
    return sum((F(1, base+j) for j in range(1, count+1)), F(0))


def main():
    thresholds = 0
    etas = (F(0), F(1, 10), F(1, 3), F(1, 2), F(2, 3), F(1), F(2))
    for base in range(9):
        for a in (0, 1):
            for followers in range(13):
                for eta in etas:
                    values = [F(1, base+1+k)+eta*harmonic_increment(base+a, k)
                              for k in range(followers+1)]
                    if eta == 0:
                        chosen = followers
                    else:
                        w = 1/eta-base-2+a
                        ceiling = -((-w.numerator)//w.denominator)
                        chosen = min(followers, max(0, ceiling))
                    assert values[chosen] == min(values)
                    if followers and eta == F(1, 2):
                        expected = (F(1, base+1) if base else
                                    F(3, 4) if a else F(1))
                        assert min(values) == expected
                    for k in range(followers+1):
                        kap = F(1, base+1)-F(1, base+k+1)
                        assert harmonic_increment(base+a, k) == harmonic_increment(base, k)-a*kap
                    thresholds += 1

    rng = random.Random(977714)
    menus = 0
    pointwise = 0
    terminal_best_reply = 0
    for r in range(1, 8):
        for sample in range(40):
            labels, customers = 4, 9
            topic = [[rng.randrange(2) for _ in range(customers)] for _ in range(labels)]
            past = [rng.randrange(labels) for _ in range(rng.randrange(5))]
            base = [sum(topic[t][x] for t in past) for x in range(customers)]
            tails = [[rng.randrange(labels) for _ in range(r-1)] for _ in range(labels)]
            if r == 2:
                for t in range(labels):
                    best = max(range(labels), key=lambda q: sum(
                        (F(topic[q][x], base[x]+topic[t][x]+1) for x in range(customers)), F(0)))
                    tails[t] = [best]
            counts = [[sum(topic[q][x] for q in tail) for x in range(customers)] for tail in tails]

            def payoff(t, q):
                return sum((F(topic[t][x], base[x]+1+counts[q][x])
                            for x in range(customers)), F(0))

            actual = max(range(labels), key=lambda t: payoff(t, t))
            u = payoff(actual, actual)

            def potential(t, q):
                return sum((harmonic_increment(base[x]+topic[t][x], counts[q][x])
                            for x in range(customers)), F(0))

            psi = potential(actual, actual)
            z = [F(rng.randrange(1, 6), 5) for _ in range(labels)]
            tau = sum(z)
            assert tau >= 1
            pi = [v/tau for v in z]
            reg = sum((pi[t]*potential(t, t) for t in range(labels)), F(0))-sum(
                (pi[t]*pi[q]*potential(t, q) for t in range(labels) for q in range(labels)), F(0))
            dec = sum((pi[t]*payoff(t, t) for t in range(labels)), F(0))-sum(
                (pi[t]*pi[q]*payoff(t, q) for t in range(labels) for q in range(labels)), F(0))
            assert reg == dec
            zet = psi-sum((pi[t]*potential(actual, t) for t in range(labels)), F(0))
            slack = tau*u-sum((z[t]*payoff(t, t) for t in range(labels)), F(0))
            assert slack >= 0
            if r == 2:
                assert reg >= 0 and zet >= 0
                terminal_best_reply += 1
            for eta in etas:
                weights = [F(rng.randrange(6), 5) for _ in range(customers)]
                d = [sum(z[t]*topic[t][x] for t in range(labels)) for x in range(customers)]
                coverage = sum((weights[x]*min(F(1), d[x]) for x in range(customers)), F(0))
                rho = sum((pi[t]*(weights[x]*min(F(1), d[x])-
                           d[x]/(base[x]+1+counts[t][x])-
                           eta*harmonic_increment(base[x]+topic[actual][x], counts[t][x]))
                           for t in range(labels) for x in range(customers)), F(0))
                assert coverage-tau*u == eta*psi+rho-(slack+tau*reg+eta*zet)
                threshold = [min(F(1, base[x]+1+k)+eta*harmonic_increment(
                    base[x]+topic[actual][x], k) for k in range(r)) for x in range(customers)]
                upper = eta*psi+sum((max(F(0), weights[x]-threshold[x])
                                    for x in range(customers)), F(0))-tau*reg-eta*zet
                assert coverage-tau*u <= upper
                pointwise += 1
            menus += 1
    report = dict(seed=977714, threshold_parameter_cases=thresholds,
                  arbitrary_legal_menus=menus, pointwise_price_checks=pointwise,
                  terminal_best_reply_menus=terminal_best_reply,
                  status="exact independent checks passed",
                  scope="Finite arithmetic audit of general symbolic formulas; no general SPE debt payment.")
    target = Path(__file__).with_name("harmonic_menu_independent_audit.json")
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
