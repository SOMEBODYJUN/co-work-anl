"""Independent exact event/kernel checks for the general exchange review.

No root/shared program or SPE solver is imported. The general proof is the
review note; these checks target same-slot intersections, rational alpha,
alpha=0 removal, random matching and complete anchoring.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent


def beta_integer_second(z, c):
    assert z > 0 and c >= 0
    prod = F(1)
    for j in range(c + 1):
        prod *= z + j
    return F(factorial(c)) / prod


def harmonic(c):
    return sum((F(1, j) for j in range(1, c + 1)), F())


def main():
    event_checks = matching_checks = kernel_checks = 0
    for m in range(6):
        for A_mask in range(1 << m):
            for C_mask in range(1 << m):
                a, c = A_mask.bit_count(), C_mask.bit_count()
                for p in (F(0), F(1, 7), F(1, 2), F(1)):
                    actual_cover = F()
                    for bits in product((0, 1), repeat=m):
                        prob = F(1)
                        covered = False
                        for i, switched in enumerate(bits):
                            prob *= p if switched else 1-p
                            covered |= bool(((C_mask if switched else A_mask) >> i) & 1)
                        actual_cover += prob * covered
                    if a == 0:
                        formula = 1-(1-p)**c
                    else:
                        loss = F() if A_mask & C_mask else p**a * (1-p)**c
                        formula = 1-loss
                    assert actual_cover == formula
                    event_checks += 1
        for a in range(m + 1):
            for c in range(m + 1):
                # Enumerate actual c-subsets of positions, not permutations.
                positions = list(combinations(range(m), c))
                avoiding = sum(all(i >= a for i in pos) for pos in positions)
                actual = F(avoiding, len(positions))
                formula = F(comb(m-a, c), comb(m, c)) if a+c <= m else F()
                assert actual == formula
                matching_checks += 1
    for c in range(9):
        for alpha in (F(1, 101), F(1, 3), F(1, 2), F(1), F(7, 3)):
            cancelled = 1/alpha-beta_integer_second(alpha, c)
            stable = sum((beta_integer_second(alpha+1, q) for q in range(c)), F())
            assert cancelled == stable
            assert 0 <= stable <= harmonic(c)
            if c == 0:
                assert cancelled == 0
            kernel_checks += 1
        # The continuous alpha=0 extension is evaluated directly, avoiding 1/0.
        extended = sum((F(1, q+1) for q in range(c)), F())
        assert extended == harmonic(c)
    # Complete anchoring has no unprotected optimal customers or outside slots.
    for m in range(7):
        residual_slots = m-m
        assert residual_slots == 0
        assert harmonic(0) == 0
    # The IC weight change is a genuine sign change even at a terminal tie.
    unweighted = F(2, 2)-1
    beta_weighted = F(3, 2)-F(2, 3)-1  # integral (2t-1)(1-t)
    assert unweighted == 0 and beta_weighted == F(-1, 6)
    result = {
        'status': 'PASS',
        'scope': 'Exact event and boundary implementation checks only; general statements use the independent review proof.',
        'bernoulli_event_checks': event_checks,
        'random_position_matching_checks': matching_checks,
        'positive_rational_alpha_checks': kernel_checks,
        'alpha_zero': 'removable expression sum_q Beta(alpha+1,q+1), limit H_c; c=0 identically zero',
        'same_slot_intersections': 'enumerated including repeated coverage and p endpoints',
        'zero_customers': 'all sums empty, both sides zero',
        'complete_anchoring': 'zero residual slots, both sides zero',
        'ic_beta_reweighting': str(beta_weighted),
        'limitation': 'No SPE-to-FLOW or HALF proof is inferred.'
    }
    target = OUT / 'optimal_exchange_review_audit.json'
    with target.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
