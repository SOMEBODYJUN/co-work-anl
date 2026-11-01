"""Independent exact audit, limited to the already-used n=3 and n=5 checks.

The all-n statement is proved analytically in new_general_mechanisms.md.
The same all-big obstruction was independently published in commit 8c4fbfd2
by R-e05f01e191354b028004b433016ae1c9; this audit is concurrent verification,
not a separate novelty claim. No discovery code or canonical game solver is
imported. All customers are represented separately and all ordered histories
are replayed, including histories that prescribe actions never taken on path.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def sf(value):
    return str(F(value))


def audit(n):
    assert n in (3, 5), "This audit must not expand the finite sample."
    topics = [frozenset(range(n))] + [
        frozenset({n + j}) for j in range(n - 1)
    ]

    def union(actions):
        return frozenset().union(*(topics[a] for a in actions))

    def payoff(action, terminal, restrict=None):
        clients = topics[action] if restrict is None else topics[action] & restrict
        return sum(
            (F(1, sum(x in topics[b] for b in terminal)) for x in clients), F()
        )

    @lru_cache(None)
    def completion(past, remaining):
        return max(
            len(frozenset(past) | union(tail))
            for tail in product(range(n), repeat=remaining)
        )

    # sigma prescribes the big topic, action 0, at every ordered history.
    comparisons = 0
    minimum_slack = None
    for depth in range(n):
        for history in product(range(n), repeat=depth):
            terminal = history + (0,) * (n - depth)
            chosen = payoff(0, terminal)
            for action in range(n):
                forced = history + (action,) + (0,) * (n - depth - 1)
                slack = chosen - payoff(action, forced)
                assert slack >= 0
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                comparisons += 1

    position_rows = []
    local_identity_checks = 0
    local_weakened_bound_checks = 0
    alpha = F(1, 2)  # illustrates the sign issue; not tuned to seek a proof.
    actual = (0,) * n
    covered = union(actual)
    all_clients = union(range(n))
    omitted = all_clients - covered

    # A matching primal/dual certificate for the owner-cost LP on this input.
    owner_cost = F()
    owner_overcover = F()
    owner_slack = F()
    owner_outside = F()
    a_counts = {x: F() for x in omitted}
    dual_row_max_restricted_payoffs = []

    for i in range(n):
        remaining = n - i
        history = (0,) * i
        past = union(history)
        prescribed = topics[0]
        g = completion(tuple(sorted(past)), remaining)
        h = completion(tuple(sorted(past | prescribed)), remaining - 1)
        delta = g - h
        utility = payoff(0, actual)
        action_rows = []
        for action, query in enumerate(topics):
            ga = completion(tuple(sorted(past | query)), remaining - 1)
            if ga != g:
                continue
            tail = union((0,) * (remaining - 1))
            forced = history + (action,) + (0,) * (remaining - 1)
            d = payoff(action, forced)
            rho = g - len(past | query | tail)
            m_new = len(query - (past | prescribed))
            exclusive = len(query - (past | prescribed | tail))
            f_old = len(prescribed - (past | query | tail))
            theta = m_new - delta
            xi = h - len(past | prescribed | tail)
            eta = remaining * d - m_new - (remaining - 1) * exclusive
            gamma = utility - d
            assert min(rho, m_new, exclusive, f_old, theta, xi, eta, gamma) >= 0
            coef = F(remaining - 1, remaining)
            full_rhs = (
                coef * rho - F(theta, remaining) - coef * (f_old + xi)
                - eta / remaining - gamma
            )
            assert full_rhs == delta - utility
            local_identity_checks += 1

            # Reducing a coefficient on a SUBTRACTED nonnegative term relaxes
            # an upper bound. It cannot invalidate that upper bound.
            weakened_rhs = (
                coef * rho - F(theta, remaining) - coef * f_old
                - alpha * coef * xi - eta / remaining - gamma
            )
            assert weakened_rhs == full_rhs + (1 - alpha) * coef * xi
            assert delta - utility <= weakened_rhs
            local_weakened_bound_checks += 1
            discarded_rhs = coef * rho - F(theta, remaining) - coef * f_old - gamma
            discounted_drop_eta_rhs = (
                coef * rho - F(theta, remaining) - coef * f_old
                - alpha * coef * xi - gamma
            )
            action_rows.append({
                "action": action,
                "rho": rho,
                "theta": theta,
                "f": f_old,
                "xi": xi,
                "eta": sf(eta),
                "Gamma": sf(gamma),
                "full_rhs": sf(full_rhs),
                "discarded_11_rhs": sf(discarded_rhs),
                "half_xi_drop_eta_rhs": sf(discounted_drop_eta_rhs),
                "half_xi_keep_eta_upper_bound": sf(weakened_rhs),
            })
        row_min = min(F(row["discarded_11_rhs"]) for row in action_rows)
        discounted_min = min(F(row["half_xi_drop_eta_rhs"]) for row in action_rows)
        position_rows.append({
            "position": i + 1,
            "remaining": remaining,
            "delta": delta,
            "utility": sf(utility),
            "actions": action_rows,
            "minimum_discarded_11_rhs": sf(row_min),
            "minimum_half_xi_drop_eta_rhs": sf(discounted_min),
        })

        # n-1 singleton queries, followed by one actual big-topic query.
        owner_action = i + 1 if i < n - 1 else 0
        owner_forced = history + (owner_action,) + (0,) * (remaining - 1)
        d_owner = payoff(owner_action, owner_forced)
        d_j = payoff(owner_action, owner_forced, all_clients)
        d_e = d_owner - d_j
        q = F(len(omitted & topics[owner_action])) - d_owner + d_e
        owner_cost += q
        owner_slack += utility - d_owner
        owner_outside += d_e
        for x in omitted & topics[owner_action]:
            a_counts[x] += 1
        restricted_values = [
            payoff(a, history + (a,) + (0,) * (remaining - 1), all_clients)
            for a in range(n)
        ]
        assert max(restricted_values) == utility
        dual_row_max_restricted_payoffs.append(sf(max(restricted_values)))

    owner_overcover = sum((count - 1 for count in a_counts.values()), F())
    assert min(a_counts.values()) >= 1
    w = len(covered)
    optimum = completion((), n)
    assert (w, optimum) == (n, 2 * n - 1)
    assert owner_cost == len(omitted) - w + owner_overcover + owner_slack + owner_outside
    assert owner_cost == -1 and owner_overcover == owner_slack == owner_outside == 0

    min_bad = sum((F(row["minimum_discarded_11_rhs"]) for row in position_rows), F())
    harmonic = sum((F(1, k) for k in range(1, n + 1)), F())
    all_n_formula = F(n * n - 3 * n - 2, 2) + harmonic
    assert min_bad == all_n_formula
    capacity = min_bad + 1
    min_discounted = sum((F(row["minimum_half_xi_drop_eta_rhs"]) for row in position_rows), F())
    assert min_discounted == -1 + (1 - alpha) * capacity
    return {
        "n": n,
        "customers": len(all_clients),
        "W": w,
        "OPT": optimum,
        "half_slack": 2 * w - optimum,
        "all_history_IC_comparisons_including_self": comparisons,
        "minimum_IC_slack": sf(minimum_slack),
        "local_identity_checks": local_identity_checks,
        "weakened_negative_xi_upper_bound_checks": local_weakened_bound_checks,
        "minimum_11_deficit": sf(min_bad),
        "all_n_formula_value": sf(all_n_formula),
        "xi_capacity_C_n": sf(capacity),
        "half_xi_drop_eta_budget_deficit": sf(min_discounted),
        "owner_LP_matching_primal_and_beta_one_dual_value": sf(owner_cost),
        "owner_overcover": sf(owner_overcover),
        "owner_IC_slack": sf(owner_slack),
        "owner_outside_query": sf(owner_outside),
        "dual_row_max_restricted_payoffs": dual_row_max_restricted_payoffs,
        "positions": position_rows,
    }


def main():
    report = {
        "status": "PASS",
        "scope": "Only n=3,5 exact regression; all-n theorem rests on the accompanying analytic proof.",
        "source_status": "Independent concurrent verification of the obstruction published as 8c4fbfd2; not a separate discovery claim.",
        "published_commit": "8c4fbfd2334c621273308dca7f8179536d1dc928",
        "published_actor": "R-e05f01e191354b028004b433016ae1c9",
        "tested_claim": "Slack-discarded global budget (11?), not half/H4/Mpath/owner LP.",
        "coefficient_correction": "Reducing a subtracted nonnegative xi term relaxes an upper bound; it can break a separate claim that its RHS is nonpositive.",
        "runs": [audit(n) for n in (3, 5)],
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "runs": [
            {key: row[key] for key in (
                "n", "W", "OPT", "all_history_IC_comparisons_including_self",
                "minimum_11_deficit", "half_xi_drop_eta_budget_deficit",
                "owner_LP_matching_primal_and_beta_one_dual_value",
            )}
            for row in report["runs"]
        ],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
