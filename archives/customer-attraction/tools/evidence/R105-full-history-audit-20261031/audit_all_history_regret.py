"""Definition-level audit of the arbitrary-m plan in the accompanying note.

This is an implementation check, not the general proof. No repository game
solver is imported. Output is written only beside this script.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from math import isqrt
from pathlib import Path


def action(m, h):
    if not h:
        return 0
    if len(h) == m - 1:
        return next(a for a in range(m) if a not in h)
    return h[-1]


def complete(m, h):
    z = tuple(h)
    while len(z) < m:
        z += (action(m, z),)
    return z


def payoff(m, q, z, i):
    return F(q, m) + F(1, Counter(z)[z[i]])


def product_factor(m, kappa):
    p = F(1)
    for r in range(1, m + 1):
        p *= 1 - F(1, r * kappa)
    return 1 - p


def audit(m):
    maxima = [F(0) for _ in range(m)]
    history_count = 0
    action_checks = 0
    last_br_checks = 0
    for depth in range(m):
        i = depth
        r = m - depth
        for h in product(range(m), repeat=depth):
            history_count += 1
            z = complete(m, h)
            u = payoff(m, 0, z, i)
            gains = []
            for a in range(m):
                action_checks += 1
                forced = complete(m, h + (a,))
                gains.append(payoff(m, 0, forced, i) - u)
                # Adding q common customers changes all branch payoffs by q/m.
                q = isqrt(m)
                assert payoff(m, q, forced, i) - payoff(m, q, z, i) == gains[-1]
            actual = max(gains)
            maxima[i] = max(maxima[i], actual)
            if depth == 0 or r == 1:
                expected = F(0)
            else:
                t = h.count(h[-1])
                expected = F(1, r - 1) - F(1, t + r - 1)
            assert actual == expected
            if r == 1:
                last_br_checks += m
                assert actual == 0

    expected_max = [F(1, m - i - 1) - F(1, m - 1)
                    for i in range(m - 1)] + [F(0)]
    assert maxima == expected_max
    H = sum((F(1, s) for s in range(1, m)), F(0))
    assert sum(maxima) == H - 1

    # Actual-path errors attain the all-history maxima at every depth.
    z = complete(m, ())
    assert z == (0,) * (m - 1) + (1,)
    W = len(set(z))
    assert W == 2
    errors = []
    for i in range(m):
        h = z[:i]
        gains = [payoff(m, 0, complete(m, h + (a,)), i)
                 - payoff(m, 0, z, i) for a in range(m)]
        errors.append(max(gains))
    assert errors == maxima

    # Definition-level check of the robust prefix and weighted product formulas
    # using C equal to all m petals and cover weight kappa=m.
    P = F(0)
    weighted_error = F(0)
    for i in range(m):
        r = m - i
        ui = payoff(m, 0, z, i)
        assert m <= P + r * m * (ui + errors[i])
        weight = F(1)
        for s in range(1, r):
            weight *= 1 - F(1, s * m)
        weighted_error += weight * errors[i]
        P += ui
    fm = product_factor(m, m)
    assert P == W
    assert W >= m * fm - weighted_error

    # Exact credible exit floors in the petal game: all future SPE moves are
    # fresh by the analytic induction in the note. Test their numerical formula.
    delta = max(F(0), F(1) - F(1, m - 1))
    half_cost = (2 * m - 1) * delta
    assert half_cost >= m - 4

    return {
        "m": m,
        "all_ordered_decision_histories": history_count,
        "true_forced_action_checks": action_checks,
        "last_BR_comparisons": last_br_checks,
        "actual_leaf": list(z),
        "W_at_q0": W,
        "OPT_at_q0": m,
        "depth_max_regrets": list(map(str, maxima)),
        "B": str(sum(maxima)),
        "credible_exit_Delta": str(delta),
        "F_m_m": str(fm),
        "weighted_error": str(weighted_error),
        "q_sqrt": isqrt(m),
        "W_at_q_sqrt": isqrt(m) + 2,
        "OPT_at_q_sqrt": isqrt(m) + m,
    }


def audit_factor_two(m):
    L = m // 2  # ceil((m-1)/2)

    def value(z, i):
        a = z[i]
        return F(L if a == 0 else 1, Counter(z)[a])

    def rule(h):
        if len(h) < m - 1:
            return 0
        counts = Counter(h)
        big = F(L, counts[0] + 1)
        singles = [F(1, counts[a] + 1) for a in range(1, m)]
        best_single = max(singles)
        if big > best_single:
            return 0
        return 1 + singles.index(best_single)

    def leaf(h):
        z = tuple(h)
        while len(z) < m:
            z += (rule(z),)
        return z

    maxima = [F(0)] * m
    checks = 0
    for depth in range(m):
        for h in product(range(m), repeat=depth):
            z = leaf(h)
            u = value(z, depth)
            best = u
            for a in range(m):
                checks += 1
                forced_pay = value(leaf(h + (a,)), depth)
                assert forced_pay <= 2 * u
                assert forced_pay <= F(m - 1, L) * u
                best = max(best, forced_pay)
            maxima[depth] = max(maxima[depth], best - u)
    epsilon = 1 - F(L, m - 1)
    assert maxima == [epsilon] * (m - 1) + [F(0)]
    B = sum(maxima)
    assert B == m - 1 - L
    z = leaf(())
    assert z == (0,) * (m - 1) + (1,)
    W = L + 1
    O = L + m - 1
    assert O - 2 * W == B - 2
    return {
        "m": m,
        "L": L,
        "forced_comparisons_checking_factor_two": checks,
        "actual_leaf": list(z),
        "W": W,
        "OPT": O,
        "depth_sup_regrets": list(map(str, maxima)),
        "B": str(B),
        "half_bad_difference": O - 2 * W,
    }


def main():
    cases = [audit(m) for m in range(2, 7)]
    factor_two_cases = [audit_factor_two(m) for m in range(2, 7)]
    assert cases[3]["depth_max_regrets"] == ["0", "1/12", "1/4", "3/4", "0"]
    assert cases[3]["F_m_m"] == "6049/15625"
    result = {
        "status": "passed",
        "scope": "Definition-level finite audit of a general complete-plan counterfamily; not an SPE or Q-CAG-HALF counterexample.",
        "all_ordered_decision_histories": sum(c["all_ordered_decision_histories"] for c in cases),
        "true_forced_action_checks": sum(c["true_forced_action_checks"] for c in cases),
        "cases": cases,
        "factor_two_contract_scope": "General lower bound C>=1; no counterexample to C=1 or larger. Last BR at every history.",
        "factor_two_forced_action_checks": sum(c["forced_comparisons_checking_factor_two"] for c in factor_two_cases),
        "factor_two_cases": factor_two_cases,
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"cases", "factor_two_cases"}}))


if __name__ == "__main__":
    main()
