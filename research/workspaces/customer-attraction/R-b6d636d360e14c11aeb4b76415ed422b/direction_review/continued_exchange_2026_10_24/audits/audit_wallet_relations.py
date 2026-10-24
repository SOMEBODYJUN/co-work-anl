#!/usr/bin/env python3
"""Reproduce the wallet review's original finite Fraction calibrations.

No author implementation, solver, cached result, random sample, or optimizer is
imported. The finite domains are unchanged from the original inline execution.
These checks calibrate algebra and boundary handling; they do not certify an SPE,
prove a universal theorem, or furnish a new small-player welfare result.

Run from any directory. By default print JSON; optionally persist the same JSON:
    python3 audit_wallet_relations.py --output audit_wallet_relations.json
"""

import argparse
import json
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path


def fs(value):
    """Exact JSON representation, including integers as rational strings."""
    return str(value)


def check_prefix():
    m = 5
    values = []
    prefix = F(0)
    for i in range(1, m + 1):
        remaining = m - i + 1
        values.append((1 - prefix) / (remaining * m))
        prefix += values[-1]
    fraction = F(1) - prod(F(r * m - 1, r * m) for r in range(1, m + 1))
    assert prefix == fraction == F(6049, 15625)
    return {
        "domain": {"m": 5, "tau": 5, "comparison_coverage_normalization": 1},
        "tight_profits": list(map(fs, values)),
        "W_over_OPT": fs(fraction),
        "OPT_over_W": fs(1 / fraction),
        "passed": True,
    }


def check_all_A_calibration():
    rows = []
    for m in [1, 2, 5, 17]:
        n = F(7)
        actual = [n / m] * m
        if m > 1:
            branch = [n / (m - 1)] * (m - 1) + [F(0)]
            q = n / (m * (m - 1))
            received = (m - 1) * q
            assert received == actual[-1]
            assert all(branch[j] > actual[j] for j in range(m - 1))
            assert sum(branch[:-1]) == n
            rows.append({
                "m": m,
                "actual_sender_profit": fs(actual[0]),
                "branch_sender_profit": fs(branch[0]),
                "q_per_sender_to_last": fs(q),
                "total_received_by_last": fs(received),
                "all_old_pushback_coefficients": "1",
                "AMOUNT_overrun_factor_at_lambda_1": fs(F(m, m - 1)),
            })
        else:
            rows.append({"m": 1, "sender_count": 0, "q_sum": "0"})
    return {
        "domain": {
            "m_values": [1, 2, 5, 17],
            "A_client_count": 7,
            "catalogue": ["A", "empty"],
            "actual_leaf": "A repeated m times",
            "forced_branch": "A repeated m-1 times, then empty",
        },
        "rows": rows,
        "passed": True,
    }


def check_coordinates():
    count = 0
    by_m = {}
    H_count = 0
    for m in range(1, 7):
        local_count = 0
        # One tagged client: B and T are its membership bits in the actual
        # and comparison actions, respectively. All 2^m choices are retained.
        for B in product([0, 1], repeat=m):
            b = sum(B)
            for T in product([0, 1], repeat=m):
                t = sum(T)
                if not t:
                    continue
                # H is independent of the forced-completion tail.
                for l in range(m):
                    hl = (
                        sum((F(1, t * (b + 1 - B[i]))
                             for i in range(m) if T[i]), F(0))
                        if B[l] and not T[l] else F(0)
                    )
                    if b:
                        assert hl <= F(1, b)
                    else:
                        assert hl == 0
                    H_count += 1
                for i in range(m):
                    if not T[i]:
                        continue
                    d = b + 1 - B[i]
                    p = F(1, t)
                    PB = F(sum(B[j] * (1 - T[j]) for j in range(m)), t * d)
                    r = p - PB
                    assert r >= 0
                    # The forced action contains this client (T_i=1).
                    # Earlier actual membership is fixed; every binary future
                    # tail is allowed. No SPE property is assumed here.
                    for tail in product([0, 1], repeat=m - i - 1):
                        W = B[:i] + (1,) + tail
                        w = sum(W)
                        n = sum(W[j] * (1 - B[j]) for j in range(i + 1, m))
                        q = F(n, d * w)
                        qhat = F(n, w) * min(p, F(1, d))
                        assert max(r - q, 0) <= F(1, w)
                        assert max(r - qhat, 0) <= F(1, w)
                        if n:
                            assert qhat / n <= p / w
                        count += 1
                        local_count += 1
        by_m[str(m)] = local_count
    assert count == 147066
    return {
        "domain": {
            "m_min": 1,
            "m_max": 6,
            "client_count_per_coordinate": 1,
            "B": "all binary membership vectors of length m",
            "T": "all nonzero binary membership vectors of length m",
            "i": "each position with T_i=1",
            "W": "B before i; forced membership 1 at i; every binary tail after i",
            "case_unit": "one (m, B, T, i, W-tail) tuple",
            "SPE_assumed": False,
        },
        "coordinate_cases": count,
        "coordinate_cases_by_m": by_m,
        "H_pointwise_columns_checked": H_count,
        "checks": [
            "r >= 0",
            "positive_part(r - raw_q) <= 1/c_W",
            "positive_part(r - strengthened_q) <= 1/c_W",
            "each strengthened future edge <= p/c_W",
            "H_lx <= 1/c_B when c_B>0; H_lx=0 when c_B=0",
        ],
        "passed": True,
    }


def check_terminal():
    count = 0
    by_m = {}
    topics = [frozenset(x for x in range(3) if mask >> x & 1)
              for mask in range(8)]
    for m in range(1, 5):
        local_count = 0
        for B in product(topics, repeat=m):
            c = {x: sum(x in action for action in B) for x in range(3)}
            p = [sum((F(1, c[x]) for x in action), F(0)) for action in B]
            worst = F(0)
            for j in range(m - 1):
                ratios = []
                # Every possible last replacement is included simultaneously
                # in the independent sender AMOUNT maximization.
                for T in topics:
                    W = B[:-1] + (T,)
                    d = {x: sum(x in action for action in W) for x in range(3)}
                    pj = sum((F(1, d[x]) for x in B[j]), F(0))
                    q = sum((F(1, c[x] * d[x])
                             for x in B[j] & (B[-1] - T)), F(0))
                    if pj:
                        ratios.append(q / pj)
                    else:
                        assert q == 0
                worst += p[j] * max(ratios, default=F(0))
            assert worst <= 2 * p[-1]
            count += 1
            local_count += 1
        by_m[str(m)] = local_count
    assert count == 4680
    return {
        "domain": {
            "m_min": 1,
            "m_max": 4,
            "labelled_unit_clients": [0, 1, 2],
            "catalogue": "all 8 subsets of {0,1,2}, including empty",
            "B": "every ordered length-m tuple over the 8 subsets",
            "last_replacements_per_B": 8,
            "case_unit": "one actual-leaf tuple B, with all replacement actions included",
            "SPE_assumed": False,
            "client_count_note": "3 labels fixed; any or all may have zero actual coverage",
        },
        "B_leaves": count,
        "B_leaves_by_m": by_m,
        "count_identity": "8^1 + 8^2 + 8^3 + 8^4 = 4680",
        "checks": [
            "zero branch sender profit implies q=0",
            "sum_j p_j(B) max_T q_jm(T)/p_j(W(T)) <= 2 p_m(B)",
        ],
        "passed": True,
    }


def check_sharp_family():
    rows = []
    for n in [3, 4, 10, 1000]:
        sender = 2 * n - 1
        branch = n + 1
        recipient = n
        lam = F(sender, branch)
        output = n * lam
        assert lam * branch == sender
        assert output / recipient == F(2 * n - 1, n + 1) < 2
        rows.append({
            "n": n,
            "m": n + 1,
            "sender_actual_profit": fs(F(sender)),
            "sender_branch_profit": fs(F(branch)),
            "lambda": fs(lam),
            "column_ratio": fs(output / recipient),
            "gap_to_2": fs(2 - output / recipient),
        })
    return {
        "domain": {"n_values": [3, 4, 10, 1000]},
        "scope": "arithmetic calibration of the supplied general-family formulas, not SPE replay",
        "rows": rows,
        "passed": True,
    }


def check_I_complement():
    count = 0
    for b in range(1, 8):
        shares = [F(1, b)] * b
        for Hnum in range(5):
            Hmass = F(Hnum, 4)
            H = [Hmass * s for s in shares]
            for anum in range(5):
                Amass = (1 - Hmass) * F(anum, 4)
                J = [Amass * (s - h) / (1 - Hmass) if Hmass < 1 else F(0)
                     for s, h in zip(shares, H)]
                assert sum(J) == Amass
                assert all(h + j <= s for s, h, j in zip(shares, H, J))
                count += 1
    return {
        "domain": {
            "actual_coverer_count_b": list(range(1, 8)),
            "w_lx": "1/b for each of the b actual coverers",
            "H_mass": ["0", "1/4", "1/2", "3/4", "1"],
            "H_lx": "H_mass * w_lx",
            "A_mass": "(1-H_mass) * a/4 for a in {0,1,2,3,4}",
        },
        "cases": count,
        "checks": ["sum_l J_lx = A_mass", "H_lx + J_lx <= w_lx", "H_mass=1 uses J=0"],
        "passed": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the JSON receipt to this path")
    args = parser.parse_args()
    receipt = {
        "audit": "wallet_relations",
        "date": "2026-10-24",
        "arithmetic": "fractions.Fraction; exact rational comparisons",
        "author_solver_or_cached_results_imported": False,
        "parameter_domain_expanded_from_original_inline_run": False,
        "scope": "Finite algebra/boundary calibrations only; no universal SPE or welfare certification.",
        "prefix": check_prefix(),
        "all_A_empty_calibration": check_all_A_calibration(),
        "coordinates": check_coordinates(),
        "terminal_multi_child_amount": check_terminal(),
        "sharp_family_formulas": check_sharp_family(),
        "I_complement": check_I_complement(),
        "all_passed": True,
    }
    result = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    print(result, end="")


if __name__ == "__main__":
    main()
