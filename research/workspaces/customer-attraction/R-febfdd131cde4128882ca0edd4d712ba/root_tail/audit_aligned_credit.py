#!/usr/bin/env python3
"""Exact reconstruction of retained four-tail credits and aligned union identity.

The canonical background certificate is read as an explicit algebra definition;
no floating LP, SPE solver, or random samples are used. This verifies the new
coefficient deduction, not the open five-player half-coverage theorem.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import runpy

ROOT = Path(__file__).resolve().parents[5]
canonical = runpy.run_path(str(ROOT / 'tests/audits/customer_attraction_four_remaining_profit.py'))
rho = canonical['direct_rho']
poly = canonical['rho_poly']
evaluate = canonical['evaluate']
D4 = canonical['D4']
ALPHA = F(1499, 750)
C = F(251, 1500)

EXPECTED = (
    ('0', '0'), ('0', '133/750'), ('1/750', '2003/12000'),
    ('1/1500', '61853/180000'), ('1/1500', '251/3000'),
    ('39/500', '6331/22500'), ('1/1000', '7363/36000'),
    ('623/3000', '26047/60000'), ('2747/12000', '239/1200'),
    ('691/6000', '14579/45000'), ('47/1500', '22183/90000'),
    ('1919/12000', '5177/12000'), ('0', '15767/90000'),
    ('77/750', '63893/180000'), ('1/4000', '43349/180000'),
    ('1169/6000', '41143/90000'),
)


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F(0)


def main():
    table = {}
    min_ratios = []
    all_types = 0
    witnesses = []
    for index, actual in enumerate(product((0, 1), repeat=4)):
        k = sum(actual)
        minima = []
        for p in (0, 1):
            entries = []
            for aux in product((0, 1), repeat=3):
                eta = (*actual, *aux)
                value = rho(eta, F(p))
                assert value == evaluate(poly(eta), F(p)) / (12000 * D4(F(p)))
                assert value >= 0
                entries.append(value)
                all_types += 1
            minima.append(min(entries))
        assert tuple(minima) == tuple(map(F, EXPECTED[index]))
        assert minima[1] >= C * share(k, 1 + k)
        if k:
            ratio = minima[1] / share(k, 1 + k)
            min_ratios.append(ratio)
            if ratio == C:
                for aux in product((0, 1), repeat=3):
                    if rho((*actual, *aux), F(1)) == minima[1]:
                        witnesses.append(''.join(map(str, (*actual, *aux))))
        table[''.join(map(str, actual))] = list(map(str, minima))
    assert min(min_ratios) == C

    # Each of all 32 indexed-optimum membership types, including e=0.
    complement_cases = 0
    for optimal in product((0, 1), repeat=5):
        e = sum(optimal)
        aligned = sum(share(e - t, e) if t else F(int(e > 0)) for t in optimal)
        assert aligned == 4 * int(e > 0)
        complement_cases += 1
    # Root+tail retained-topic conservation is a pointwise identity.
    conservation_cases = 0
    for t, *actual in product((0, 1), repeat=5):
        k = sum(actual)
        assert t - share(t, t + k) == t * share(k, 1 + k)
        conservation_cases += 1
    print(json.dumps({
        'status': 'exact coefficient consequence, not Q-CAG-HALF proof',
        'alpha': str(ALPHA), 'uniform_root_loss_credit': str(C),
        'rho_cases': all_types, 'table': table,
        'uniform_credit_equality_eta': witnesses,
        'aligned_complement_membership_cases': complement_cases,
        'root_tail_conservation_cases': conservation_cases,
    }, indent=2))


if __name__ == '__main__':
    main()
