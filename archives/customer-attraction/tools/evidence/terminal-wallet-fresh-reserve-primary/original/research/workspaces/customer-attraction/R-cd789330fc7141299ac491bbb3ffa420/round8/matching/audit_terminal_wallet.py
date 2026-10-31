"""Exact replay of the terminal frozen-regret wallet on two existing policies.

This is a targeted implementation check of the all-input analytic inequality
in terminal_frozen_regret_wallet.md.  It generates no instances or policies,
imports no model/solver/verifier, and does not modify its source certificates.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent


def read_json(relative):
    path = ROOT / relative
    raw = path.read_bytes()
    return json.loads(raw), {
        "path": relative,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def load_old52():
    data, source = read_json(
        "research/workspaces/customer-attraction/"
        "R-a0bb57fa24044a8794bc7991918a19c6/"
        "static_matching/static_matching_counterexample.json"
    )
    policy = {
        tuple(row["history"]): row["action"]
        for row in data["certificate"]["actions"]
    }
    return data["instance"], policy, [source]


def load_new1953():
    prefix = (
        "research/workspaces/customer-attraction/"
        "R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/"
    )
    instance, source1 = read_json(prefix + "assignment_instance.json")
    data, source2 = read_json(prefix + "assignment_full_policy.json")
    policy = {
        tuple(map(int, key.split(","))) if key else (): action
        for key, action in data["policy"].items()
    }
    return instance, policy, [source1, source2]


def audit(loader):
    instance, policy, sources = loader()
    m = instance["players"]
    catalog_size = len(instance["topics"])
    topics = range(catalog_size)
    # Expand each multiplicity into distinct unit customers.
    customers = [
        frozenset(row["topics"])
        for row in instance["customers"]
        for _ in range(row["multiplicity"])
    ]
    expected_histories = {
        h for depth in range(m) for h in product(topics, repeat=depth)
    }
    assert set(policy) == expected_histories
    assert all(action in topics for action in policy.values())

    terminal_cache = {}

    def finish(prefix):
        if prefix not in terminal_cache:
            leaf = prefix
            while len(leaf) < m:
                leaf += (policy[leaf],)
            terminal_cache[prefix] = leaf
        return terminal_cache[prefix]

    payoff_cache = {}

    def payoffs(leaf):
        if leaf not in payoff_cache:
            result = [F(0) for _ in leaf]
            for customer in customers:
                coverers = [i for i, action in enumerate(leaf) if action in customer]
                for i in coverers:
                    result[i] += F(1, len(coverers))
            payoff_cache[leaf] = tuple(result)
        return payoff_cache[leaf]

    ic_count = 0
    ic_minimum = None
    for h in sorted(expected_histories, key=lambda value: (len(value), value)):
        current = len(h)
        live = payoffs(finish(h))[current]
        for action in topics:
            deviation = payoffs(finish(h + (action,)))[current]
            slack = live - deviation
            assert slack >= 0
            ic_count += 1
            ic_minimum = slack if ic_minimum is None else min(ic_minimum, slack)

    actual = finish(())
    profits = payoffs(actual)
    actual_past = actual[:-2]
    A, B = actual[-2:]
    background = [sum(action in customer for action in actual_past) for customer in customers]

    def U(X, Y):
        return sum(
            (F(1, b + 1 + (Y in customer))
             for customer, b in zip(customers, background) if X in customer),
            F(0),
        )

    a, v = U(A, B), U(B, A)
    assert (a, v) == profits[-2:]
    L = sum(
        (F(1, b + 2) for customer, b in zip(customers, background) if A in customer),
        F(0),
    )
    C = sum(
        (F(1, (b + 1) * (b + 2))
         for customer, b in zip(customers, background)
         if A in customer and B not in customer),
        F(0),
    )
    assert C == a - L >= 0
    assert v >= L >= a / 2
    assert C <= min(a / 2, v)
    assert 3 * C <= a + v
    imbalance = max(a - v, F(0))
    reduced_wallet = C - imbalance
    assert reduced_wallet == min(a, v) - L >= 0
    assert reduced_wallet <= min(a, v) / 2

    rows = []
    for T in topics:
        R = policy[actual_past + (T,)]
        D = U(T, R)
        e = a - D
        off = U(R, T) - U(B, T)
        act = U(B, A) - U(R, A)
        ell = off + act
        g = U(A, R) - L
        frozen = U(T, B)
        assert min(e, off, act, ell, g) >= 0
        assert D + a - frozen - U(A, R) == ell
        assert frozen == a + C - e - g - ell
        assert frozen <= a + C
        assert frozen - D == C - g - ell
        assert U(T, A) <= v
        assert frozen - U(T, A) <= C
        assert frozen <= min(a, v) + C
        assert e + g + ell >= imbalance
        reduced_credit = e + g + ell - imbalance
        assert frozen == a + reduced_wallet - reduced_credit
        rows.append({
            "topic": T,
            "true_last_reply": R,
            "true_current_profit": str(D),
            "frozen_current_profit": str(frozen),
            "source_ic_slack_e": str(e),
            "last_off_br_slack": str(off),
            "last_actual_br_slack": str(act),
            "copy_floor_credit_g": str(g),
            "reduced_terminal_credit_h": str(reduced_credit),
            "frozen_minus_true": str(frozen - D),
        })

    return {
        "sources": sources,
        "unit_customers": len(customers),
        "players": m,
        "catalog_size": catalog_size,
        "complete_ordered_histories": len(expected_histories),
        "all_true_ic_including_self": ic_count,
        "minimum_true_ic_slack": str(ic_minimum),
        "actual": actual,
        "actual_profits": [str(value) for value in profits],
        "actual_welfare": str(sum(profits, F(0))),
        "actual_penultimate_profit_a": str(a),
        "actual_last_profit_v": str(v),
        "copy_floor_L_A": str(L),
        "selective_wallet_C_p": str(C),
        "reduced_wallet_C_prime_p": str(reduced_wallet),
        "actual_profit_imbalance": str(imbalance),
        "pair_profit_minus_three_wallets": str(a + v - 3 * C),
        "all_terminal_wallet_identities": True,
        "rows": rows,
    }


def main():
    result = {
        "status": "exact_existing_certificate_implementation_check_only",
        "analytic_claim": "terminal pointwise frozen-regret wallet, arbitrary m and catalog",
        "general_half": "OPEN",
        "weak_optimal_assignment_budget": "OPEN",
        "cases": {
            "old_52_unit_strong_assignment_counterexample": audit(load_old52),
            "independent_1953_unit_strong_assignment_counterexample": audit(load_new1953),
        },
    }
    output = HERE / "terminal_wallet_exact_audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        label: {key: value[key] for key in (
            "players", "unit_customers", "complete_ordered_histories",
            "all_true_ic_including_self", "selective_wallet_C_p",
        )}
        for label, value in result["cases"].items()
    }, indent=2))


if __name__ == "__main__":
    main()
