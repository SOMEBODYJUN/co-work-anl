#!/usr/bin/env python3
"""Independent Fraction audit of the exact all-proper-restrictions obstruction."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def target(r, T, anchor=0):
    assert 1 <= len(T) <= 2
    if anchor in T:
        return Q(1)
    if len(T) == 1:
        return Q(1, 2)
    return Q(3*r-1, 2*(2*r-1))


def all_moment_sets(labels):
    return [(i,) for i in labels] + list(combinations(labels, 2))


def model_moments(labels, components):
    """Each component is (total rational mass, explicit equally weighted types)."""
    result = {T: Q(0) for T in all_moment_sets(labels)}
    for mass, types in components:
        if not mass:
            continue
        assert types and all(types)
        for T in result:
            count = sum(any(a in B for a in T) for B in types)
            result[T] += mass*Q(count, len(types))
    return result


def audit_r(r):
    n = 2*r+1
    variables = tuple(range(1, n+1))
    anchor = 0
    labels = (anchor,) + variables
    type_count = 0
    nonnegative_min = None
    zero_types = 0
    # Reconstruct the dual from coverage columns, separately from its k-formula.
    for mask in range(1, 1 << len(labels)):
        B = {a for a in labels if mask >> a & 1}
        coverage = lambda T: int(any(a in B for a in T))
        value = r*(r+1)*coverage((anchor,))
        value -= sum(2*coverage((i, j))-coverage((i,))-coverage((j,))
                     for i, j in combinations(variables, 2))
        value += 2*r*sum(coverage((anchor, i))-coverage((anchor,)) for i in variables)
        k = len(B.intersection(variables))
        expected = ((k-r)*(k-r-1) if anchor in B else k*(k-1))
        assert value == expected and value >= 0
        nonnegative_min = value if nonnegative_min is None else min(nonnegative_min, value)
        zero_types += value == 0
        type_count += 1

    # Maximal proper restriction: remove variable n, keeping anchor and 2r variables.
    local_vars = tuple(range(1, 2*r+1))
    anchored_types = [frozenset((anchor,)+T) for T in combinations(local_vars, r)]
    anchored = model_moments((anchor,)+local_vars, [(Q(1), anchored_types)])
    assert all(value == target(r, T) for T, value in anchored.items())

    # Other maximal proper restriction: delete anchor, retaining n variables.
    alpha = Q(n, 2*(2*r-1))
    beta = Q(n*(r-1), 2*(r+1)*(2*r-1))
    first = [frozenset(T) for T in combinations(variables, r)]
    second = [frozenset(T) for T in combinations(variables, r+1)]
    unanchored = model_moments(variables, [(alpha, first), (beta, second)])
    assert all(value == target(r, T) for T, value in unanchored.items())
    assert alpha >= 0 and beta >= 0

    fake = {T: target(r, T) for T in all_moment_sets(labels)}
    dual_value = r*(r+1)*fake[(anchor,)]
    dual_value -= sum(2*fake[(i, j)]-fake[(i,)]-fake[(j,)]
                      for i, j in combinations(variables, 2))
    dual_value += 2*r*sum(fake[(anchor, i)]-fake[(anchor,)] for i in variables)
    assert dual_value == -Q(r, 2*r-1) < 0

    anchored_unit_weight = Q(1, len(anchored_types))
    first_unit_weight = alpha/len(first)
    second_unit_weight = beta/len(second)
    scale = lcm(anchored_unit_weight.denominator, first_unit_weight.denominator,
                second_unit_weight.denominator)
    assert all((x*scale).denominator == 1 for x in
               [anchored_unit_weight, first_unit_weight, second_unit_weight])
    return dict(r=r, variables=n, all_labels=n+1,
                full_nonempty_types_checked=type_count,
                minimum_dual_column=nonnegative_min, zero_dual_columns=zero_types,
                anchored_model_types=len(anchored_types),
                unanchored_first_types=len(first), unanchored_second_types=len(second),
                alpha=str(alpha), beta=str(beta), unanchored_total_mass=str(alpha+beta),
                local_single_pair_moments_checked=len(anchored)+len(unanchored),
                all_maximal_proper_restriction_classes_realizable=True,
                dual_value_at_fake_data=str(dual_value), common_integer_scale=scale)


def main():
    report = dict(
        identity="PM-1/PM-2/PM-3 exact positive-moment locality audit; not a CAG counterexample",
        arithmetic="standard-library Fraction, explicit type enumeration and local customer models",
        scope="m=2; one representative of each maximal proper restriction under variable-label symmetry",
        cases=[audit_r(r) for r in range(1, 7)],
        limitations="finite checks support the separate universal proofs; no general half payment is constructed",
    )
    target_path = HERE / 'positive_moment_locality_audit.json'
    target_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(output=str(target_path), all_checks_passed=True,
                          cases=len(report['cases']),
                          full_types=sum(r['full_nonempty_types_checked'] for r in report['cases']),
                          local_moments=sum(r['local_single_pair_moments_checked'] for r in report['cases']))))


if __name__ == '__main__':
    main()
