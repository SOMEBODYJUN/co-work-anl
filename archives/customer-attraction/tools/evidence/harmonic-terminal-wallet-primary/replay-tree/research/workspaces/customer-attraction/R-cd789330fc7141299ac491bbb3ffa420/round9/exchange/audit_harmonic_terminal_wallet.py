"""Definition-level audit of HW on two already certified complete policies.

No instance generation or equilibrium search.  The full IC audit from round8
is rerun before the new per-customer and same-W identities are checked.
"""

from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parents[1] / "round8" / "matching" / "audit_terminal_wallet.py"
spec = importlib.util.spec_from_file_location("previous_wallet_audit", PREVIOUS)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def audit(loader):
    previous = old.audit(loader)
    instance, policy, sources = loader()
    m = instance["players"]
    customers = [
        frozenset(row["topics"])
        for row in instance["customers"]
        for _ in range(row["multiplicity"])
    ]
    actual = ()
    while len(actual) < m:
        actual += (policy[actual],)
    A, B = actual[-2:]
    u = list(map(F, previous["actual_profits"]))
    a, v = u[-2:]
    W = sum(u, F(0))
    H = sum((F(1, r) for r in range(1, m + 1)), F(0))
    q = [F(0) for _ in range(m - 2)]
    L = C = customer_refund = F(0)
    for customer in customers:
        if A not in customer:
            continue
        k = sum(action in customer for action in actual[:-2])
        Fx = F(0)
        for i in range(m - 2):
            b = sum(action in customer for action in actual[:i])
            r = m - i
            assert b + r <= (k + 1) * r
            value = F(1, b + r)
            q[i] += value
            Fx += value
        assert Fx >= (H - F(3, 2)) / (k + 1)
        lx = F(1, k + 2)
        cx = F(1, (k + 1) * (k + 2))
        slack = Fx + 2 * lx - (2 * H - 1) * cx
        assert slack >= F(k) * (H + F(1, 2)) / ((k + 1) * (k + 2)) >= 0
        L += lx
        if B not in customer:
            C += cx
            customer_refund += slack
        else:
            customer_refund += Fx + 2 * lx
    assert all(ui >= qi for ui, qi in zip(u[:-2], q))
    Fsum = sum(q, F(0))
    t = min(a, v)
    Cp = t - L
    R = sum((ui - qi for ui, qi in zip(u[:-2], q)), F(0))
    J = Fsum + 2 * L - (2 * H - 1) * C
    assert C == a - L >= Cp >= 0
    assert J == customer_refund >= 0
    assert W >= Fsum + 2 * t
    assert W >= (2 * H + 1) * Cp
    assert W - (2 * H + 1) * Cp == R + abs(a - v) + J + (2 * H - 1) * max(a - v, F(0))
    return {
        "sources": sources,
        "players": m,
        "all_true_ic_including_self": previous["all_true_ic_including_self"],
        "actual": list(actual),
        "actual_profits": list(map(str, u)),
        "welfare": str(W),
        "harmonic_number": str(H),
        "copy_rows_q": list(map(str, q)),
        "copy_row_slack_R": str(R),
        "copy_floor_L": str(L),
        "unreduced_wallet_C": str(C),
        "reduced_wallet_C_prime": str(Cp),
        "customer_refund_J": str(J),
        "same_welfare_refund": str(W - (2 * H + 1) * Cp),
        "all_copy_client_and_refund_identities": True,
    }


def main():
    result = {
        "status": "exact_existing_certificate_implementation_check_only",
        "general_half": "OPEN",
        "weak_optimal_assignment": "OPEN",
        "cases": {
            "old_52_unit_strong_assignment_counterexample": audit(old.load_old52),
            "independent_1953_unit_strong_assignment_counterexample": audit(old.load_new1953),
        },
        "m5_analytic_substitution": {
            "H_5": str(sum((F(1, r) for r in range(1, 6)), F(0))),
            "C_prime_over_W_upper_bound": str(F(30, 167)),
            "remaining_W_over_5_minus_C_prime_lower_coefficient": str(F(17, 835)),
            "proves_general_m5_half": False,
        },
    }
    output = HERE / "harmonic_terminal_wallet_exact_audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({label: {key: value[key] for key in (
        "players", "all_true_ic_including_self", "reduced_wallet_C_prime",
        "same_welfare_refund",
    )} for label, value in result["cases"].items()}, indent=2))


if __name__ == "__main__":
    main()
