"""Exact count-level checks of INSERT and direct matching-query half credit.

This checks new all-input identities, not a new special SPE instance.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def H(k):
    return sum((F(1, j) for j in range(1, k+1)), F())


def f(c, s):
    return F(1) if s else F(c, c+1)


def main():
    profile_checks = query_checks = 0
    for k in range(9):
        for s in (0, 1):
            c = k+s
            assert H(c) == f(c, s)+H(k+1)-1
            error_sum = F()
            if s:
                owner_margin = f(c, s)-f(c-1, 0)
                assert owner_margin == F(1, c)
            if k:
                nonowner_margin = f(c, s)-f(c-1, s)
                e = F(1, c)-nonowner_margin
                assert e == F(1, k+1)
                assert 0 < e <= F(1, 2)
                assert (H(k+1)-1)-(H(k)-1) == e
                error_sum += k*e
            assert error_sum == F(k, k+1)
            profile_checks += 1
    # Any query matching has one owner query and a-1 nonowner queries.
    # Their leaves may have unrelated loads, so each is checked independently.
    for a in range(1, 9):
        maxima = []
        for is_owner in (False, True):
            credits = []
            for c in range(1, 10):
                if is_owner:
                    credit = F(1, c)-(f(c, 1)-f(c-1, 0))
                    assert credit == 0
                    credits.append(credit)
                else:
                    for s in (0, 1):
                        if s and c < 2:
                            continue
                        credit = F(1, c)-(f(c, s)-f(c-1, s))
                        assert 0 <= credit <= F(1, 2)
                        credits.append(credit)
                query_checks += 1
            maxima.append(max(credits))
        assert maxima == [F(1, 2), F()]
        assert maxima[1]+(a-1)*maxima[0] == F(a-1, 2)
    result = dict(status='PASS', profile_count_identity_checks=profile_checks,
                  independent_query_count_checks=query_checks,
                  direct_matching_credit='sum query rebate(x) <= (a_x-1)/2; separate R and I sums',
                  insertion_potential='harmonic potential = F_Q + sum_O(H_(1+k_nonowner)-1)',
                  scope='New all-input formula boundary checks only; universal proof is in the component note.',
                  limitations='No cross-branch budget or HALF conclusion.')
    with (HERE / 'owner_insertion_identity_audit.json').open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
