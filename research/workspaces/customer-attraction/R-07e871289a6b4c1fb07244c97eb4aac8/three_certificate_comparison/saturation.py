#!/usr/bin/env python3
"""Exact independent coefficient audit of the general near-saturation lemma.

No solver or certificate data needed.  Finite enumeration checks the written
pointwise identity; the accompanying analytic cases prove all k>=2,b>=0.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def check(k, b, c, d, l, r):
    w = F(1, b + k)
    q = c + l + r
    share = F(l, b + q) if l else F(0)
    query = F(d, b + c + r + 1)
    ideal = c * d * w + F((1-c)*d, b+1)
    rho = (c + (k-1)*c*(k-q) - F(k*k, 2)*c
           + k*l + F(k*r, 2))*w - ideal - share + query
    if c == 0:
        last = (k*w - F(1, b+l+r)) if l else F(0)
        formula = last + F(k*r, 2)*w - F(d*r, (b+1)*(b+r+1))
        assert last >= 0
        assert F(k*r, 2)*w - F(d*r, (b+1)*(b+r+1)) >= 0
    elif l == 0:
        h = k-q
        formula = F(k-2, 2)*(h-1)*w + d*(F(1, b+q+1)-w)
    elif d == 1:
        formula = F(k-2, 2)*(k-q)*w
    else:
        formula = (k-q)*w*(F(k-2, 2)-F(1, b+q))
    assert rho == formula, (k,b,c,d,l,r,rho,formula)
    assert rho >= 0, (k,b,c,d,l,r,rho)
    # The per-customer deficit/source-gap relation for a total m=b+k.
    if c:
        gap = F(1, b+q) - w
        deficit = (k-q)*w
        assert gap >= deficit/(b+k-1)
    return rho


def main():
    total = zeros = 0
    minima = []
    for k in range(2, 33):
        minimum = None
        for b in range(33):
            for c in (0,1):
                for d in (0,1):
                    for l in (0,1):
                        for r in range(k-1):
                            rho = check(k,b,c,d,l,r)
                            minimum = rho if minimum is None else min(minimum,rho)
                            total += 1
                            zeros += rho == 0
        minima.append({'k':k,'min_residual':str(minimum)})
    # Check the two capacity readouts and exact five-person coefficient match.
    coefficient_checks = 0
    for m in range(2, 65):
        for k in range(2, m+1):
            B = (m-1)*(k-1)
            a = 2*B+k*k
            assert F(a,2) == B+F(k*k,2)
            assert F(a-2,2) == B+F(k*k,2)-1
            if m == 5:
                assert a == 8*(k-1)+k*k
            coefficient_checks += 1
    report = dict(status='EXACT POINTWISE IDENTITIES VERIFIED',
                  k_range=[2,32], background_range=[0,32],
                  coefficient_states=total,zero_residuals=zeros,
                  capacity_readout_checks=coefficient_checks,
                  arithmetic='fractions.Fraction', minima=minima,
                  scope='Local near-saturation lemma only; no whole 44-row certificate run')
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
