from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from math import comb


def harmonic_prefix(m):
    values = [Fraction(0)]
    for j in range(1, m + 1):
        values.append(values[-1] + Fraction(1, j))
    return values


def coefficient(m, d, q, h):
    t = m - q
    return t + Fraction(d + 2, d + 1) * (t * (h[m] - h[t]) - Fraction((d - q) * q, m))


def forward_difference(m, d, q, h):
    return -1 + Fraction(d + 2, d + 1) * (1 - h[m] + h[m-q-1] + Fraction(2*q + 1 - d, m))


def minimum(m, d, h):
    if d == 0:
        return Fraction(m)
    pivot = min(d - 1, m // 2)
    lo, hi = 0, pivot + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if forward_difference(m, d, mid, h) < 0:
            lo = mid + 1
        else:
            hi = mid
    return min(coefficient(m, d, q, h) for q in {0, d, pivot + 1, lo})


def largest_certified(m, h):
    lo, hi = 0, m
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if minimum(m, mid, h) >= m - 1:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    for m in range(1, 106):
        h = harmonic_prefix(m)
        previous = Fraction(m)
        cutoff = 0
        for d in range(m):
            values = [coefficient(m, d, q, h) for q in range(d + 1)]
            assert minimum(m, d, h) == min(values) <= previous
            previous = min(values)
            if previous >= m - 1:
                cutoff = d
            for q, value in enumerate(values):
                if q < d:
                    assert values[q+1] - value == forward_difference(m, d, q, h)
                if d+1 < m:
                    base = (m-q)*(h[m]-h[m-q]) + Fraction(q*q, m)
                    c = Fraction(q, m)
                    assert value - coefficient(m,d+1,q,h) == c + (base+c)/((d+1)*(d+2))
        assert cutoff == largest_certified(m, h)
    assert largest_certified(6, harmonic_prefix(6)) == 3
    assert largest_certified(100, harmonic_prefix(100)) == 17
    registry = json.loads(Path('research/registry.json').read_text())
    source = next(o for o in registry['objects'] if o['object_id'] == 'B2-REPEATED-LAST-ABSENCE-v1')
    ref = next(e for e in source['evidence'] if e['path'].endswith('new-definition-check.json'))
    original = Path(ref['path']).read_bytes()
    assert sha256(original).hexdigest() == ref['sha256']
    old = json.loads(original)['all_m_k_cases']
    assert len(old) == 5050
    for item in old:
        m, d = item['m'], item['d']
        h = harmonic_prefix(m)
        gamma = minimum(m, d, h)
        assert gamma == Fraction(item['gamma'])
        assert [m-q for q in reversed(range(d+1)) if coefficient(m,d,q,h) == gamma] == item['argmin_t']
    print(comb(107, 3), 'exact coefficient grid cases and', len(old), 'historical minima matched')


if __name__ == '__main__':
    main()
