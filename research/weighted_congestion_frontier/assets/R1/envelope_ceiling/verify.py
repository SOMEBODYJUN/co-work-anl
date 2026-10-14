#!/usr/bin/env python3
"""Reproducible sanity checks; exact algebra and non-interval Decimal numerics."""
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import platform
import random


def exact_checks():
    rng = random.Random(314159)
    count = active = 0
    boundary = []
    cases = [(1, 1, 1, Fraction(1), Fraction(0)),
             (2, 1, 1, Fraction(1, 2), Fraction(1)),
             (4, 1, 2, Fraction(1, 10**12), Fraction(1, 3)),
             (8, 20, 3, Fraction(1), Fraction(1, 10**12))]
    for d in (2, 4, 8, 16, 32):
        for n in (1, 2, 3, 5):
            for w in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 10)):
                for beta in (Fraction(1, 4), Fraction(1, 8), Fraction(1, 32), Fraction(1, 128)):
                    cases.append((d, n, max(1, d//3), w, beta))
    for _ in range(240):
        d = rng.randint(1, 32)
        cases.append((d, rng.randint(1, 40), rng.randint(1, d),
                      Fraction(rng.randint(1, 100), 100),
                      Fraction(rng.randint(0, 100), 100)))
    for d, n, k, w, beta in cases:
        E, A, B = (1+w)**d, (1+n*w)**k, (1+w)**k
        Q = beta*E
        R_h = (1+n*Q)/(A+n*beta)
        R_l = (B+beta*w**d)/((n*w)**k+Q)
        R = min(R_h, R_l)
        z, y = w/(1+w), n*w/(1+w)
        assert A/B == (1+(n-1)*z)**k
        assert E == (1-z)**(-d)
        if R > 1:
            active += 1
            assert 0 < y < 1
            assert y**k <= 1/R
            assert Q <= B/(R-1)
            assert E > R
            assert n*B/A >= (R-1)*(R-1/A) >= (R-1)**2
            assert R*(n*w)**k + (R-(w/(1+w))**d)*Q <= B
        if beta == 0:
            assert R_h <= 1
            boundary.append('beta=0')
        count += 1
    return {'seed': 314159, 'cases': count, 'R_above_one': active,
            'boundary_checks': boundary}


def decimal_checks():
    samples = []
    for exponent in (6, 12, 24, 48, 96, 192, 384):
        with localcontext() as ctx:
            ctx.prec = exponent + 80
            d = Decimal(10)**exponent
            D, H = d.ln(), d.ln().ln()
            w = D/(2*d)
            n = int(4*d*H/(D*D))
            k = int((D/(2*(H-(2*H).ln()))).to_integral_value(rounding='ROUND_CEILING'))
            E = (d*(1+w).ln()).exp()
            S = (d*H).sqrt()/D
            Q = Decimal(1).exp().sqrt()/2/S
            beta = Q/E
            A, B = (1+Decimal(n)*w)**k, (1+w)**k
            heavy = (1+Decimal(n)*Q)/(A+Decimal(n)*beta)
            # Omitting beta*w**d gives a lower ratio. Here w<1/2,
            # beta<=1, so the omitted numerator is at most 2**(-d).
            assert 0 < w < Decimal('0.5') and 0 < beta <= 1
            light_lower = B/((Decimal(n)*w)**k+Q)
            R = min(heavy, light_lower)
            sample = {'degree': '10^'+str(exponent), 'precision': ctx.prec,
                      'k': k, 'heavy_over_S': str(heavy/S)[:24],
                      'light_lower_over_S': str(light_lower/S)[:24]}
            if R >= Decimal(2).exp():
                h = R.ln()
                bound = 8*d*h.ln()/(h*h)
                # The first proof also applies to any common lower bound
                # of the ratios, so the omitted term causes no issue here.
                assert R*R <= bound
                sample['R_squared_over_ceiling'] = str(R*R/bound)[:24]
            samples.append(sample)
    scalar_count = 0
    with localcontext() as ctx:
        ctx.prec = 80
        for h in map(Decimal, (2, 3, 4, 10, 100, 1000)):
            for j in range(1, 1000):
                y = Decimal(j)/1000
                scalar = y*(-h*y/(4*(1/y).ln())).exp()
                assert scalar <= 2*h.ln()/h
                scalar_count += 1
        D = Decimal(16)
        assert D*(-D/4).exp()/D.ln().sqrt() < 1
        assert (D/2).exp()*D.ln().sqrt()/D > Decimal(2).exp()
        assert 4/Decimal(1).exp() < 2
    return {'samples': samples, 'scalar_grid_cases': scalar_count}


def main():
    report = {'claim': 'WC-ENVELOPE-CEILING v1',
              'python': platform.python_version(),
              'method': 'Fraction exact algebra; Decimal non-interval sanity checks',
              'exact': exact_checks(), 'decimal': decimal_checks(),
              'limitations': ['Finite checks do not prove a universal inequality.',
                              'Decimal output has no certified interval error bound.',
                              'The written analytic proof carries the claim.'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target = Path(__file__).with_name('verification.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'exact_cases': report['exact']['cases'],
                      'scalar_cases': report['decimal']['scalar_grid_cases'],
                      'degree_samples': len(report['decimal']['samples'])}))


if __name__ == '__main__':
    main()
