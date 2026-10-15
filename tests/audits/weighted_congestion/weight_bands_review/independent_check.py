"""Independent exact bound check using the original subset Shapley definition.

Default is read-only: recompute and compare independent_verification.json.
--generate NEW_PATH writes one new output and refuses to overwrite a file.
This finite calculation is evidence only, never a proof of the general lemma.
"""

from fractions import Fraction
from itertools import combinations, product
from math import factorial
from pathlib import Path
import argparse
import hashlib
import json


if not __debug__:
    raise RuntimeError('Run without -O: exact verification requires assertions')


def monomial_share(weights, player, exponent):
    n = len(weights)
    others = [j for j in range(n) if j != player]
    answer = Fraction(0)
    for cardinality in range(n):
        coefficient = Fraction(
            factorial(cardinality) * factorial(n-cardinality-1), factorial(n))
        for coalition in combinations(others, cardinality):
            load = sum(weights[j] for j in coalition)
            answer += coefficient * ((load + weights[player])**exponent
                                     - load**exponent)
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', type=Path)
    args = parser.parse_args()
    target = args.generate or Path(__file__).with_name('independent_verification.json')
    if args.generate and target.exists():
        parser.error('refusing to overwrite frozen evidence')

    by_n = []
    for n in range(2, 6):
        cases = checks = 0
        for weights in product(range(1, 5), repeat=n):
            load = sum(weights)
            minimum, maximum = min(weights), max(weights)
            for exponent in range(1, 13):
                shares = [monomial_share(weights, i, exponent) for i in range(n)]
                for share in shares:
                    assert minimum * load**(exponent-1) <= share
                    assert share <= maximum * load**(exponent-1)
                    checks += 1
                assert sum(shares, Fraction(0)) == load**exponent
                cases += 1
        by_n.append({'n': n, 'ordered_weight_vectors': 4**n,
                     'monomial_cases': cases, 'share_bound_checks': checks})

    output = {
        'arithmetic': 'fractions.Fraction; no floats',
        'definition': 'original coalition/subset Shapley marginal formula',
        'weight_domain': [1, 2, 3, 4],
        'weight_vectors': 'all ordered vectors, not only multisets',
        'monomial_total_cost_exponents': list(range(1, 13)),
        'by_n': by_n,
        'monomial_cases': sum(row['monomial_cases'] for row in by_n),
        'share_bound_checks': sum(row['share_bound_checks'] for row in by_n),
        'efficiency_checks': sum(row['monomial_cases'] for row in by_n),
        'status': 'all assertions passed',
        'scope': 'Finite supporting evidence; independent general proof is in independent_review.md.',
    }
    if args.generate:
        target.write_text(json.dumps(output, indent=2) + '\n')
    else:
        assert json.loads(target.read_text()) == output, 'frozen evidence mismatch'
    print(json.dumps(output, indent=2))
    print('verification_sha256=' + hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
