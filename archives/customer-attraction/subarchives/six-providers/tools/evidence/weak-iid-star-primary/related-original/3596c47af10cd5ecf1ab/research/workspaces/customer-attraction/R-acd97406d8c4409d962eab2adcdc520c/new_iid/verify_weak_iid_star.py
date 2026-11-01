"""Exact endpoint and exhaustive history-type audit for the weak iid star.

The analytic proof in weak_iid_star_counterexample.md carries the universal
history quantifier. This program independently computes all relevant finite
payoff classes and Fraction inequalities; Decimal/float is display only.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import sys

N = 30
K = 100
PRIVATE_B = 2 * (N - 1)


def g(t):
    return sum(((1 - t) ** j for j in range(N)), Q(0)) / N


def action(prefix):
    if not prefix:
        return 0  # A
    if len(prefix) < N - 1:
        return 1  # B
    non_b = [a for a in prefix if a != 1]
    if not non_b:
        return 2
    if len(non_b) == 1 and non_b[0] >= 2:
        return 2 if non_b[0] != 2 else 3
    return 1


def continuation(prefix):
    out = list(prefix)
    while len(out) < N:
        out.append(action(out))
    return out


def payoff(own, terminal):
    if own == 1:
        return Q(PRIVATE_B, terminal.count(1))
    common_load = N - terminal.count(1)
    return Q(2, common_load) + (Q(1, terminal.count(own)) if own >= 2 else 0)


def audit_representatives():
    # All choices below the last node use B regardless of history order.
    # The last action depends on non-B count and, only when count=1, its type.
    # For ell>=2, only the current C's prior multiplicity affects its own payoff.
    # We represent every ell, A count, and current-C multiplicity explicitly.
    checked = 0
    minimum = None
    for depth in range(N):
        for ell in range(depth + 1):
            for a_count in range(ell + 1):
                c_count = ell - a_count
                # For the prospective C2 action: its old multiplicity ranges
                # from 0 through c_count; all other C mass can sit on C3.
                for c2_count in range(c_count + 1):
                    h = [1] * (depth - ell) + [0] * a_count
                    h += [2] * c2_count + [3] * (c_count - c2_count)
                    own = action(h)
                    base = payoff(own, continuation(h))
                    # A, B, C2, C3, and a fresh C exhaust payoff classes.
                    for alt in [0, 1, 2, 3, 4]:
                        value = payoff(alt, continuation(h + [alt]))
                        diff = base - value
                        assert diff >= 0, (h, own, alt, base, value)
                        minimum = diff if minimum is None else min(minimum, diff)
                        checked += 1
    return checked, str(minimum)


def main():
    checked, minimum = audit_representatives()
    s0 = Q(1, 20)
    b = PRIVATE_B * g(1 - s0)
    c = g(s0 / K) + 2 * g(s0)
    c_lower = Q(3971, 4000) + Q(392, 375)
    threshold = Q(120, 59)
    assert 5 * 19 ** 10 < 3 * 20 ** 10
    assert 20 ** 30 > 1711
    assert g(Q(1, 2000)) >= Q(3971, 4000)
    assert 2 * g(Q(1, 20)) > Q(392, 375)
    assert c > c_lower > Q(116, 57) > b > threshold
    assert c_lower - Q(116, 57) == Q(683, 228000)
    terminal = continuation([])
    utilities = [payoff(a, terminal) for a in terminal]
    assert utilities == [Q(2)] * N
    assert 2 + PRIVATE_B + min(K, N - 1) == 89
    # A rational bracket optionally displays a stronger quantitative margin.
    left, right = Q(50342, 1000000), Q(50343, 1000000)
    diff = lambda s: PRIVATE_B * g(1-s) - g(s/K) - 2*g(s)
    assert diff(left) < 0 < diff(right)
    lambda_lo, lambda_hi = PRIVATE_B*g(1-left), PRIVATE_B*g(1-right)
    result = {
        "status": "author_exact_audit_not_independent_review",
        "players": N, "petals": K, "topics": K+2,
        "unit_customers": 2+PRIVATE_B+K,
        "path": ["A"] + ["B"]*(N-1),
        "utilities": [str(u) for u in utilities],
        "W": 60, "OPT": 89,
        "history_class_deviation_checks": checked,
        "minimum_incentive": minimum,
        "s0": str(s0), "B_s0": str(b), "C_s0": str(c),
        "simple_C_lower": str(c_lower),
        "simple_C_lower_minus_116_57": "683/228000",
        "weak_lambda_threshold": str(threshold),
        "s_star_bracket": [str(left), str(right)],
        "lambda_bracket": [str(lambda_lo), str(lambda_hi)],
        "lambda_bracket_decimal": [float(lambda_lo), float(lambda_hi)],
        "weak_gap_bracket_decimal": [float(Q(59,2)*lambda_lo-60),
                                     float(Q(59,2)*lambda_hi-60)],
        "exact_assertions_passed": True,
        "Q_CAG_HALF": "OPEN; this example has 2W=120>OPT=89",
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if len(sys.argv) == 2:
        with Path(sys.argv[1]).open("x") as target:
            target.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
