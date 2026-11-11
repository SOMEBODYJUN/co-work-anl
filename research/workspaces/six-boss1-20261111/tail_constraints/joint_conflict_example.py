"""Exact marginal counterexample to separate single/pair transport closure.

This is a necessary-statistics example, deliberately not a complete SPE.
"""

from fractions import Fraction as F
import json
from pathlib import Path

from transport_separator import STATES, exact_transport, serial


def main():
    # Four-state order is 00, 01, 10, 11.
    rho = (F(), F(3), F(6), F())
    # (mass, preceding load L, prefix theme X member, current last c member).
    states = ((F(6), 5, 1, 0), (F(2), 0, 0, 1), (F(1), 0, 0, 0))
    eta = [s[0] for s in states]
    u_new = sum((mass * F(c, load + 1) for mass, load, x, c in states), F())
    u_old_z = sum((mass * F(z, r + 1) for (r, z), mass in zip(STATES, rho)), F())
    assert (u_new, u_old_z) == (2, 3)

    def transport(cost):
        return exact_transport(rho, eta, [[cost(r, z, load, x, c)
                                          for _, load, x, c in states] for r, z in STATES])

    diagnostics = {
        "new_to_R": (u_new, transport(lambda r, z, load, x, c: F(r, load + 1))),
        "new_to_Z": (u_new, transport(lambda r, z, load, x, c: F(z, load + 1))),
        "new_to_R_plus_Z": (2 * u_new, transport(lambda r, z, load, x, c: F(r + z, load + 1))),
        "old_Z_to_X": (u_old_z, transport(lambda r, z, load, x, c: F(x, r + 1))),
        "old_Z_to_current_last": (u_old_z, transport(lambda r, z, load, x, c: F(c, r + 1))),
    }
    assert all(budget >= result["minimum"] for budget, result in diagnostics.values())
    assert [diagnostics[k][1]["minimum"] for k in diagnostics] == [F(1), F(1, 2), F(4), F(3), F(1)]
    combined = transport(lambda r, z, load, x, c: F(3 * z, load + 1) + F(5 * x, r + 1))
    combined_budget = 3 * u_new + 5 * u_old_z
    assert combined_budget == 21 and combined["minimum"] == 24
    report = {
        "scope": "exact marginal-domain counterexample; not SPE, not a six-player efficiency counterexample",
        "old_prefix_P": 0, "rho_in_00_01_10_11_order": rho,
        "new_states_mass_load_X_current_last": states,
        "new_terminal_profit": u_new, "old_Z_profit": u_old_z,
        "separate_and_RZ_pair": {name: {"budget": budget, "minimum_cost": result["minimum"],
                                         "slack": budget - result["minimum"]}
                                 for name, (budget, result) in diagnostics.items()},
        "joint_weights": {"new_to_Z": 3, "old_Z_to_X": 5},
        "joint_budget": combined_budget, "joint_minimum": combined["minimum"],
        "joint_slack": combined_budget - combined["minimum"],
        "full_transport_certificate": combined,
        "analytic_identity": "For t=mass(Z intersect X), costs are 3-5t/6 and 3+t/2; 3*first+5*second=24 for every coupling."}
    target = Path(__file__).resolve().with_suffix(".json")
    target.write_text(json.dumps(serial(report), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(serial({k: v for k, v in report.items() if k != "full_transport_certificate"}), ensure_ascii=False))


if __name__ == "__main__":
    main()
