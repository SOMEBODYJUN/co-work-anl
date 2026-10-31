"""Author finite whole-row trade check; no global/localizer enumeration.

For four stated (d,k) values, enumerate the actual Qnew and H row marginals,
the proposed legal CONFIG list, and every squarefree monomial of row degree
at most d. Integer common-denominator sums verify all moments exactly.
No earlier audit is relabeled, and this does not prove the arbitrary-d claim.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path


def subset_masks(k, bound):
    for size in range(bound + 1):
        for subset in combinations(range(k), size):
            yield sum(1 << j for j in subset)


def check(d, k):
    s = d - 1
    low = list(subset_masks(k, s))
    z = len(low)
    max_coefficient = comb(k - 1, s)
    ell = 2 * k * k
    count = 1 + 120 * ell * k ** 4 + 4 * k * z * max_coefficient
    a = F(1, count)
    all_home = (1 << k) - 1

    def state(unit, homes):
        return homes | (0 if unit is None else 1 << (k + unit))

    q = defaultdict(F)
    q[state(None, all_home)] += 1 - F(3, 4 * ell)
    for j in range(k):
        q[state(j, 0)] += F(1, 8 * ell * k)
        q[state(None, all_home ^ (1 << j))] += F(1, 8 * ell * k)
    for homes in low:
        q[state(None, homes)] += F(1, 4 * ell * z)
        for j in range(k):
            q[state(j, homes)] += F(1, 4 * ell * k * z)
    assert sum(q.values()) == 1
    raw = defaultdict(F, {key: (1 - a) * value for key, value in q.items()})
    raw[state(None, all_home)] += a * (1 - F(k, ell))
    for j in range(k):
        raw[state(j, all_home)] += a / ell
    legal = defaultdict(F, {key: (1 - a) * value for key, value in q.items()})
    legal[state(None, all_home)] += a
    coefficients = {}
    for homes in low:
        size = homes.bit_count()
        coefficient = (-1) ** (s - size) * comb(k - size - 1, s - size)
        coefficients[homes] = coefficient
        assert abs(coefficient) <= max_coefficient
        for j in range(k):
            legal[state(j, homes)] += a * coefficient / ell
        legal[state(None, homes)] -= a * k * coefficient / ell
    for probe in low:
        assert sum(value for mask, value in coefficients.items()
                   if mask & probe == probe) == 1
    assert sum(raw.values()) == sum(legal.values()) == 1
    for mask, weight in legal.items():
        assert weight >= 0
        assert (mask >> k).bit_count() <= 1
        load_scaled = k * (mask >> k).bit_count() + (mask & all_home).bit_count()
        assert load_scaled <= k + s
    denominator = lcm(*(value.denominator for value in [*raw.values(), *legal.values()]))
    raw_int = {key: value.numerator * (denominator // value.denominator)
               for key, value in raw.items()}
    legal_int = {key: value.numerator * (denominator // value.denominator)
                 for key, value in legal.items()}

    def moment(measure, mask):
        return sum(value for key, value in measure.items() if key & mask == mask)

    checked = 0
    for probe in subset_masks(2 * k, d):
        assert moment(raw_int, probe) == moment(legal_int, probe), (d, k, probe)
        checked += 1
    raw_home = defaultdict(int)
    legal_home = defaultdict(int)
    for key, value in raw_int.items():
        raw_home[key & all_home] += value
    for key, value in legal_int.items():
        legal_home[key & all_home] += value
    assert dict(raw_home) == dict(legal_home)
    next_probe = (1 << k) | ((1 << d) - 1)
    assert F(moment(raw_int, next_probe), denominator) == a / ell
    assert moment(legal_int, next_probe) == 0
    return {
        "d": d, "k": k, "L": ell, "M": count, "Z": z,
        "Amax": max_coefficient, "row_variable_count": 2 * k,
        "checked_all_squarefree_row_monomials_through_degree_d": checked,
        "matched": True, "legal_CONFIG_mass": "1",
        "minimum_CONFIG_mass": str(min(legal.values())),
        "maximum_CONFIG_load": str(F(k + s, k)),
        "pure_home_marginal_exactly_equal": True,
        "natural_law_degree_d_plus_one_witness": str(a / ell),
        "legal_CFG_same_witness": "0",
        "scope": "row trade only, no global M2 or affine-localizer enumeration",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = {
        "status": "finite author audit, not general-d proof or independent review",
        "cases": [check(d, k) for d, k in [(2, 2), (3, 3), (4, 4), (4, 7)]],
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"cases_passed": len(payload["cases"]),
                      "output_sha256": sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
