"""Exact finite checks for the local Shapley proof; not a universal proof.

Run from any working directory. Compares the frozen verification.json.
--generate NEW_PATH writes a new record and refuses to overwrite one.
Only fractions, factorials, and seeded integer/rational samples are used.
"""

from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb, factorial
from pathlib import Path
from random import Random
import hashlib
import json
import argparse


if not __debug__:
    raise RuntimeError('Run without -O: exact verification requires assertions')


def polynomial(x, coefficients):
    return sum((coefficient * x**degree
                for degree, coefficient in enumerate(coefficients)), Q(0))


def coalition_value(weights, coefficients, mask):
    load = sum((weight for j, weight in enumerate(weights)
                if mask & (1 << j)), Q(0))
    return load * polynomial(load, coefficients)


def potential(weights, coefficients, mask):
    n = mask.bit_count()
    if not n:
        return Q(0)
    answer = Q(0)
    subset = mask
    while subset:
        t = subset.bit_count()
        answer += Q(factorial(t-1)*factorial(n-t), factorial(n)) * \
                  coalition_value(weights, coefficients, subset)
        subset = (subset - 1) & mask
    return answer


def share(weights, coefficients, mask, player):
    assert mask & (1 << player)
    n = mask.bit_count()
    remainder = mask ^ (1 << player)
    answer = Q(0)
    subset = remainder
    while True:
        t = subset.bit_count()
        answer += Q(factorial(t)*factorial(n-t-1), factorial(n)) * \
                  (coalition_value(weights, coefficients, subset | (1 << player))
                   - coalition_value(weights, coefficients, subset))
        if not subset:
            return answer
        subset = (subset - 1) & remainder


def verify_share_case(weights, coefficients):
    mask = (1 << len(weights)) - 1
    shares = [share(weights, coefficients, mask, i)
              for i in range(len(weights))]
    load = sum(weights, Q(0))
    cost = polynomial(load, coefficients)
    assert sum(shares, Q(0)) == load * cost
    h = potential(weights, coefficients, mask)
    for i, value in enumerate(shares):
        assert h - potential(weights, coefficients, mask ^ (1 << i)) == value
        assert min(weights) * cost <= value <= max(weights) * cost
    pair_count = 0
    for i in range(len(weights)):
        for j in range(i + 1, len(weights)):
            if weights[i] <= weights[j]:
                assert shares[i] <= shares[j]
                assert shares[i] / weights[i] >= shares[j] / weights[j]
            else:
                assert shares[j] <= shares[i]
                assert shares[j] / weights[j] >= shares[i] / weights[i]
            pair_count += 1
    return pair_count


def compositions(total, parts):
    if not parts:
        if total == 0:
            yield ()
        return
    if parts == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in compositions(total-head, parts-1):
            yield (head,) + tail


def verify_identity(weights, q, i, j):
    a, b = weights[i], weights[j]
    assert a <= b
    others = [weight for index, weight in enumerate(weights)
              if index not in (i, j)]
    positive_expansion = Q(0)
    for beta_total in range(q):
        h = q - beta_total
        if h < 2:
            continue
        for beta in compositions(beta_total, len(others)):
            m = sum(exponent > 0 for exponent in beta)
            B = Q(factorial(q), factorial(h))
            for weight, exponent in zip(others, beta):
                B *= Q(weight**exponent, factorial(exponent))
            for r in range(h - 1):
                coefficient = Q(comb(h, r+1), m+2) - Q(1, m+1)
                assert coefficient >= 0
                positive_expansion += B * (b-a) * coefficient * a**r * b**(h-2-r)
    coefficients = [Q(0)] * (q-1) + [Q(1)]
    mask = (1 << len(weights)) - 1
    actual = (share(weights, coefficients, mask, i) / a
              - share(weights, coefficients, mask, j) / b)
    assert positive_expansion == actual


def exact_game_check(rng):
    # Arbitrary strategy sets, including empty and multiple resources.
    weights = (Q(1), Q(5, 4), Q(3, 2), Q(7, 4))
    strategies = (
        ((), (0,), (0, 1), (1, 2)),
        ((), (1,), (0, 2)),
        ((0,), (2,), (0, 1, 2)),
        ((1,), (0, 2), (1, 2)),
    )
    resources = range(3)
    coefficients = (
        (Q(0), Q(0), Q(1), Q(2)),
        (Q(0),),  # Entirely zero resource.
        (Q(2), Q(1), Q(0), Q(3)),
    )
    potential_users = [
        [i for i in range(len(weights))
         if any(e in strategy for strategy in strategies[i])]
        for e in resources
    ]
    minima = [min(weights[i] for i in users) for users in potential_users]
    R = max(max(weights[i] for i in users) / minima[e]
            for e, users in enumerate(potential_users))

    def masks(state):
        return [sum(1 << i for i, index in enumerate(state)
                    if e in strategies[i][index]) for e in resources]

    def values(state):
        user_masks = masks(state)
        phi = sum((potential(weights, coefficients[e], user_masks[e]) / minima[e]
                   for e in resources), Q(0))
        costs, modified = [], []
        for i, index in enumerate(state):
            costs.append(sum((polynomial(
                sum((weights[j] for j in range(len(weights))
                     if user_masks[e] & (1 << j)), Q(0)), coefficients[e])
                for e in strategies[i][index]), Q(0)))
            modified.append(sum((share(weights, coefficients[e], user_masks[e], i)
                                 / minima[e] for e in strategies[i][index]), Q(0)))
            assert costs[i] <= modified[i] <= R * costs[i]
        return phi, costs, modified

    states = list(product(*(range(len(choices)) for choices in strategies)))
    cached = {state: values(state) for state in states}
    minimum = min(cached[state][0] for state in states)
    minimizers = [state for state in states if cached[state][0] == minimum]
    checks = 0
    for state in states:
        phi, costs, modified = cached[state]
        for i, choices in enumerate(strategies):
            for alternative in range(len(choices)):
                deviation = state[:i] + (alternative,) + state[i+1:]
                new_phi, new_costs, new_modified = cached[deviation]
                assert new_phi - phi == new_modified[i] - modified[i]
                if state in minimizers:
                    assert costs[i] <= R * new_costs[i]
                checks += 1
    return {"states": len(states), "deviation_checks": checks,
            "minimizers": minimizers, "R": str(R)}


def verify_dense_augmentation():
    d, M, L = 7, 49, 3
    delta = Q(1 + (M+1)**(d+1) - M**(d+1), 2*(M+1)**d)
    rho = delta/2
    weights = (Q(1), Q(M)) + (Q(1), Q(M))*L
    coefficients = (Q(0),)*d + (Q(1, (M+1)**d),)
    # Player 1 stays on A. Player 0 chooses A or B. New players choose A or empty.
    choices = [i for i in range(len(weights)) if i != 1]
    phis = {}
    for bits in range(1 << len(choices)):
        mask = (1 << 1) | sum(1 << i for j, i in enumerate(choices) if bits & (1 << j))
        phis[mask] = potential(weights, coefficients, mask) + (rho if not mask & 1 else 0)
    minimum = min(phis.values())
    minimizers = [mask for mask, phi in phis.items() if phi == minimum]
    assert minimizers == [1 << 1]
    assert rho >= Q(d, 6) and rho > 1
    return {"d": d, "M": M, "L": L, "states": len(phis),
            "potential_A_users_per_band": L+1,
            "unique_minimum_A_users_mask": minimizers[0],
            "rho": str(rho), "rho_decimal_display_only": float(rho)}


def main():
    rng = Random(20261014)
    pool = (Q(1, 3), Q(1), Q(5, 4), Q(2), Q(5))
    share_cases = pair_checks = 0
    for n in range(1, 6):
        for weights in combinations_with_replacement(pool, n):
            for degree in range(7):
                coefficients = [Q(0)] * degree + [Q(1)]
                pair_checks += verify_share_case(weights, coefficients)
                share_cases += 1
    for sample in range(100):
        n = rng.randrange(1, 7)
        weights = tuple(Q(rng.randrange(1, 20), rng.randrange(1, 9))
                        for _ in range(n))
        coefficients = tuple(Q(rng.randrange(0, 6), rng.randrange(1, 8))
                             for _ in range(rng.randrange(1, 9)))
        pair_checks += verify_share_case(weights, coefficients)
        share_cases += 1
    # Explicit all-zero polynomial.
    pair_checks += verify_share_case((Q(1), Q(9)), (Q(0),))
    share_cases += 1
    identity_cases = 0
    for n in range(2, 6):
        for q in range(1, 8):
            for sample in range(8):
                weights = sorted(Q(rng.randrange(1, 11), rng.randrange(1, 6))
                                 for _ in range(n))
                verify_identity(weights, q, 0, n-1)
                identity_cases += 1

    # Curl identity: singleton bands do not yield an ordinary potential.
    curl_M = Q(13)
    weights = (Q(1), curl_M)
    cubic_total = (Q(0), Q(0), Q(1))
    kappa = potential(weights, cubic_total, 3) \
        - potential(weights, cubic_total, 1) \
        - potential(weights, cubic_total, 2)
    assert kappa == Q(3, 2)*curl_M*(curl_M+1)
    assert kappa != kappa/curl_M

    linear_obstruction = []
    for d in (7, 8, 10, 20, 50, 100):
        M = d*d
        delta = Q(1 + (M+1)**(d+1) - M**(d+1), 2*(M+1)**d)
        rho = delta/2
        assert delta >= Q(d, 3)
        assert rho >= Q(d, 6) and rho > 1 and rho < delta
        linear_obstruction.append({"d": d, "M": M,
                                   "delta": str(delta), "rho": str(rho),
                                   "rho_decimal_display_only": float(rho)})

    sharp_selector = []
    R = Q(2)
    for m in (2, 3, 5, 10, 20):
        d = m*m
        W = m*R+1
        delta = sum(((k*R+1)**(d+1) - (k*R)**(d+1)
                     for k in range(m+1)), Q(0)) / ((m+1)*W**d)
        lower = W/(m+1)*(1-(1-1/W)**(d+1))
        upper = W/(m+1)
        assert lower <= delta <= upper
        rho = delta-Q(1, m)
        if rho > 1:
            assert rho < delta
        sharp_selector.append({"m": m, "d": d, "R": str(R),
                               "delta_decimal_display_only": float(delta),
                               "rho_decimal_display_only": float(rho),
                               "rho_gt_one": rho > 1})

    output = {"seed": 20261014, "arithmetic": "fractions.Fraction only; floats are display only",
              "status": "all assertions passed", "share_cases": share_cases,
              "pair_ordering_checks": pair_checks,
              "positive_identity_checks": identity_cases,
              "exact_multiresource_game": exact_game_check(rng),
              "curl": {"M": str(curl_M), "kappa": str(kappa)},
              "dense_augmentation": verify_dense_augmentation(),
              "linear_obstruction": linear_obstruction,
              "sharp_selector": sharp_selector,
              "scope": "Finite exact verification supplements, but does not prove, the general theorem."}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate', type=Path)
    args = parser.parse_args()
    path = args.generate or Path(__file__).with_name("verification.json")
    if args.generate:
        if path.exists():
            parser.error('refusing to overwrite frozen evidence')
        path.write_text(json.dumps(output, indent=2)+'\n')
    else:
        assert json.loads(path.read_text()) == json.loads(json.dumps(output)), 'frozen evidence mismatch'
    print(json.dumps({key: value for key, value in output.items()
                      if key not in ("linear_obstruction", "sharp_selector")}, indent=2))
    print("verification_sha256=" + hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
