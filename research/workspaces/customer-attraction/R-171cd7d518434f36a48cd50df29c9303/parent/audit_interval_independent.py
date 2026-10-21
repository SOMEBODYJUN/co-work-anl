"""Definition-level independent reconstruction; imports no author implementation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random


def verify(bits, lengths, theta, rho):
    m = len(bits)
    c = sum(bits)
    hit_slots = [t for t, bit in enumerate(bits, 1) if bit]
    raw = F(0)
    allocated = F(0)
    congestion = [F(0)] * m
    for j, length in enumerate(lengths, 1):
        b = sum(bits[:j])
        q = sum(bits[j:j + length])
        raw += theta[j - 1] * b * (1 / (rho + b) - 1 / (rho + b + q))
        for t in range(j + 1, j + length + 1):
            congestion[t - 1] += j * theta[j - 1]
    for rank, t in enumerate(hit_slots, 1):
        assigned = sum((theta[j - 1] * sum(bits[:j])
                        for j, length in enumerate(lengths, 1)
                        if j < t <= j + length), F(0))
        allocated += assigned / ((rho + rank - 1) * (rho + rank))
    gamma = max(congestion, default=F(0))
    cap = gamma * (1 / (rho + 1) - 1 / (rho + c)) if c else F(0)
    assert raw == allocated
    assert 0 <= raw <= cap <= gamma * int(c > 0) / (rho + 1)
    return raw, cap


def main():
    cases = 0
    # Exhaustive binary paths, all interval choices at small m, noninteger reserve.
    for m in range(1, 7):
        intervals = list(product(*(range(m - j + 1) for j in range(1, m))))
        for bits in product((0, 1), repeat=m):
            for lengths in intervals:
                for rho in (F(1, 3), F(1), F(5, 2)):
                    theta = [F(1, j) if j % 2 else F(2, 3 * j)
                             for j in range(1, m)]
                    verify(bits, lengths, theta, rho)
                    cases += 1
    rng = random.Random(171021)
    for _ in range(500):
        m = rng.randrange(2, 45)
        bits = [rng.randrange(2) for _ in range(m)]
        lengths = [rng.randrange(m - j + 1) for j in range(1, m)]
        theta = [F(rng.randrange(6), rng.randrange(1, 7)) for _ in lengths]
        verify(bits, lengths, theta, F(rng.randrange(1, 9), rng.randrange(1, 7)))
        cases += 1
    # Sparse future windows, one use per slot, violate the proposed interval cap.
    sparse = []
    for q in (1, 2, 3, 8, 64):
        bits = [1] + [0] * (q - 1) + [1] * q
        harmonic = sum((F(1, j) for j in range(1, q + 1)), F(0))
        raw = sum((F(sum(bits[:j]), j) *
                   (F(1, 1 + sum(bits[:j])) -
                    F(1, 1 + sum(bits[:j]) + bits[q + j - 1]))
                   for j in range(1, q + 1)), F(0))
        assert raw == harmonic / 6
        cap = F(1, 2) - F(1, q + 2)
        sparse.append({'q': q, 'cost': str(raw), 'interval_cap': str(cap),
                       'difference': str(raw - cap)})
    assert sparse[2]['difference'] == '1/180'
    # Rank2 can appear in two adjacent windows: prevents a tempting false sharpening.
    raw, cap = verify([1, 0, 1, 0], [2, 2, 0], [F(1), F(1, 2), F(0)], F(1))
    assert raw == F(1, 4) and cap == F(1, 3)
    out = {'status': 'independent exact finite audit; universal proof in review',
           'cases': cases, 'seed': 171021, 'sparse_future_boundary': sparse,
           'rank2_cost': str(raw)}
    Path(__file__).with_name('interval_independent_audit.json').write_text(
        json.dumps(out, indent=2) + '\n')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
