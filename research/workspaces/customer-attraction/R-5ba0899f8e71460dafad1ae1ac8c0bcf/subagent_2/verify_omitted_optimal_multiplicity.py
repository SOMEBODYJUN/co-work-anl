"""Exact arithmetic audit of the analytic omitted-comparator multiplicity lemma.

No equilibrium solver or LP is imported. This audits coefficients/identities;
the accompanying proof supplies the all-input SPE quantifiers.
"""

from fractions import Fraction as F
from itertools import product
import json
from math import prod


def factor(m, tau):
    return 1 - prod(1 - 1 / (r * tau) for r in range(1, m + 1))


def main():
    recursive_cases = 0
    for m in range(1, 13):
        for tau in (F(1), F(3, 2), F(m)):
            value = F(0)
            for r in range(m, 0, -1):
                value = (1 - 1 / (r * tau)) * value + 1 / (r * tau)
            assert value == factor(m, tau)
            assert 0 < value <= 1
            recursive_cases += 1

    n = 6
    integer_column_checks = 0
    fractional_column_checks = 0
    for actual in product((0, 1), repeat=n):
        covered = any(actual)
        final_load = sum(actual)
        for i in range(n):
            b = sum(actual[:i])
            r = n - i
            assert final_load <= b + r
            for d in range(n + 1):
                if not d:
                    continue
                lhs = F(b + r * d, b + r)
                demand = F(1) if covered else F(d)
                assert lhs >= demand
                if not covered:
                    assert b == 0 and lhs == d
                # Old actual players are paid within this same terminal.
                for j in range(i):
                    if actual[j]:
                        assert F(1, b + r) <= F(1, final_load)
                integer_column_checks += 1
            for a in (F(0), F(1, 6), F(1, 2), F(1), F(7, 6), F(2), F(6)):
                demand = min(F(1), a) if covered else a
                assert F(b, b + r) + F(r, b + r) * a >= demand
                fractional_column_checks += 1

    f = factor(6, F(6))
    assert f == F(2352949, 6718464)
    beta = 1 / f
    assert beta == F(6718464, 2352949)
    assert beta - 1 == F(4365515, 2352949)
    assert beta - 2 == F(2012566, 2352949)
    assert 3 - beta == F(340383, 2352949) > 0
    assert (beta + 1) / 2 == F(9071413, 4705898) < 2
    report = {
        "status": "passed",
        "scope": "exact coefficient and recurrence audit, not a search over games",
        "recurrence_cases": recursive_cases,
        "six_player_integer_column_checks": integer_column_checks,
        "six_player_fractional_column_checks": fractional_column_checks,
        "F6_6": str(f),
        "beta6": str(beta),
        "all_omissions_at_least_two_bound": str((beta + 1) / 2),
        "strict_counterexample_unique_optimal_occurrence_floor": str(3 - beta),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
