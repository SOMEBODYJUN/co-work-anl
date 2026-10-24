#!/usr/bin/env python3
"""Reproduce the bounded independent audit reported in delete_repair.md.

Standard library only. No repository solver or author's audit is imported.
The fixed scopes are the 18-client repair witness and the two plans at
m=2,...,6 with q=0. These finite checks do not prove the arbitrary-m claims.

Without --output, print JSON. With --output, create a new JSON file and refuse
to overwrite an existing file. No frozen source evidence is changed.
"""

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


SOURCE = Path(
    "research/workspaces/customer-attraction/"
    "R-105f776c3e6d4a22bb7c380c5df8edc7/"
    "new_cross_branch/zero_regret_repair_witness.json"
)


def repo_root():
    return next(p for p in Path(__file__).resolve().parents if (p / "AGENTS.md").is_file())


def audit_repair_witness(path):
    raw = path.read_bytes()
    witness = json.loads(raw)
    labels = witness["topics"]
    actions = range(len(labels))
    clients = [
        frozenset(c["topics"])
        for c in witness["customers"]
        for _ in range(c["multiplicity"])
    ]
    assert len(clients) == 18

    def payoff(leaf, player, background=()):
        return sum(
            (
                F(1, sum(a in client for a in background + tuple(leaf)))
                for client in clients
                if leaf[player] in client
            ),
            F(0),
        )

    def welfare(leaf):
        return sum(any(a in client for a in leaf) for client in clients)

    def all_complete_spe(background):
        # A complete two-player policy has one root action and four last
        # actions: exactly 4**5=1024 policies. Check every last history,
        # then all true root deviations using that same menu.
        terminal = [[payoff((a, t), 1, background) for t in actions] for a in actions]
        first = [[payoff((a, t), 0, background) for t in actions] for a in actions]
        found = []
        examined = 0
        for root_action in actions:
            for menu in product(actions, repeat=len(labels)):
                examined += 1
                if not all(terminal[a][menu[a]] == max(terminal[a]) for a in actions):
                    continue
                root_payoffs = [first[a][menu[a]] for a in actions]
                if root_payoffs[root_action] == max(root_payoffs):
                    found.append((root_action, menu))
        assert examined == 1024
        return found, terminal, examined

    def encode_policy(policy):
        root_action, menu = policy
        return {
            "first_action": labels[root_action],
            "last_after_first": [labels[a] for a in menu],
            "actual_leaf": [labels[root_action], labels[menu[root_action]]],
            "tail_coverage": welfare((root_action, menu[root_action])),
        }

    old_spe, old_terminal, old_count = all_complete_spe((0,))
    new_spe, new_terminal, new_count = all_complete_spe(())
    assert old_spe == [(2, (2, 2, 1, 2))]
    assert new_spe == [(3, (2, 3, 1, 1))]
    assert [welfare((a, menu[a])) for a, menu in old_spe] == [17]
    assert [welfare((a, menu[a])) for a, menu in new_spe] == [16]

    old_plan = witness["old_tail_strategy"]
    root_action = old_plan["first_action"]
    menu = old_plan["last_after_first"]
    assert (root_action, tuple(menu)) == old_spe[0]
    retained_root_payoffs = [payoff((a, menu[a]), 0) for a in actions]
    retained_last_payoffs = [payoff((root_action, a), 1) for a in actions]
    actual_regrets = [
        max(retained_root_payoffs) - retained_root_payoffs[root_action],
        max(retained_last_payoffs) - retained_last_payoffs[menu[root_action]],
    ]
    assert actual_regrets == [F(0), F(0)]
    assert max(welfare(leaf) for leaf in product(actions, repeat=2)) == 17

    root_probe = []
    expected_leaves = [(2, 1), (3, 2), (1, 3), (1, 2)]
    expected_payoffs = [F(5), F(13, 2), F(11, 2), F(6)]
    expected_policy_counts = [1, 2, 1, 1]
    for a in actions:
        suffix_spe, _, count = all_complete_spe((a,))
        leaves = {(b, mm[b]) for b, mm in suffix_spe}
        root_payoffs = {payoff((a, b, mm[b]), 0) for b, mm in suffix_spe}
        assert leaves == {expected_leaves[a]}
        assert root_payoffs == {expected_payoffs[a]}
        assert len(suffix_spe) == expected_policy_counts[a]
        root_probe.append({
            "root_action": labels[a],
            "policies_examined": count,
            "complete_suffix_spe_count": len(suffix_spe),
            "distinct_suffix_terminal_count": len(leaves),
            "suffix_policies": [encode_policy(p) for p in suffix_spe],
            "root_payoff": str(expected_payoffs[a]),
        })
    assert expected_payoffs.index(max(expected_payoffs)) == 1

    return {
        "source": SOURCE.as_posix(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "unit_client_count": len(clients),
        "old_background_A": {
            "policies_examined": old_count,
            "complete_spe_count": len(old_spe),
            "distinct_spe_terminal_count": len({(a, mm[a]) for a, mm in old_spe}),
            "policies": [encode_policy(p) for p in old_spe],
            "last_payoff_table": [[str(v) for v in row] for row in old_terminal],
        },
        "new_empty_background": {
            "policies_examined": new_count,
            "complete_spe_count": len(new_spe),
            "distinct_spe_terminal_count": len({(a, mm[a]) for a, mm in new_spe}),
            "policies": [encode_policy(p) for p in new_spe],
            "last_payoff_table": [[str(v) for v in row] for row in new_terminal],
        },
        "retained_old_plan": {
            "root_payoff_menu": list(map(str, retained_root_payoffs)),
            "actual_last_payoff_menu": list(map(str, retained_last_payoffs)),
            "actual_regrets": list(map(str, actual_regrets)),
            "projected_coverage": welfare((root_action, menu[root_action])),
        },
        "empty_background_OPT_2": 17,
        "three_player_root_probe": root_probe,
        "unique_actual_three_player_root_action": "B",
    }


def audit_plan(m, factor_two=False):
    # Identical fixed finite scope to the first inline run: q=0 only.
    q = 0
    L = m // 2  # ceil((m-1)/2), with integer arithmetic.

    def theme_size(a):
        return L if a == 0 else 1

    def prescribed(history):
        if len(history) == m - 1:
            if not factor_two:
                return next(a for a in range(m) if a not in history)
            values = [F(theme_size(a), history.count(a) + 1) for a in range(m)]
            best = max(values)
            return next((a for a in range(1, m) if values[a] == best), 0)
        return 0 if factor_two or not history else history[-1]

    def replay(history):
        history = tuple(history)
        while len(history) < m:
            history += (prescribed(history),)
        return history

    def income(leaf, i):
        if factor_two:
            return F(theme_size(leaf[i]), leaf.count(leaf[i]))
        return F(q, m) + F(1, leaf.count(leaf[i]))

    defects = []
    max_ratio = F(1)
    histories_examined = 0
    forced_actions_examined = 0
    for i in range(m):
        depth_defect = F(0)
        for history in product(range(m), repeat=i):
            histories_examined += 1
            prescribed_leaf = replay(history)
            prescribed_income = income(prescribed_leaf, i)
            forced_incomes = [income(replay(history + (a,)), i) for a in range(m)]
            forced_actions_examined += m
            best = max(forced_incomes)
            depth_defect = max(depth_defect, best - prescribed_income)
            max_ratio = max(max_ratio, best / prescribed_income)
        defects.append(depth_defect)
    actual_leaf = replay(())
    if factor_two:
        assert defects == [F(m - 1 - L, m - 1)] * (m - 1) + [F(0)]
        assert max_ratio <= 2
        W = sum(theme_size(a) for a in set(actual_leaf))
        OPT = L + m - 1  # All m pairwise disjoint themes can be selected once.
        assert W == L + 1
        assert OPT - 2 * W == sum(defects) - 2
    else:
        assert defects == [F(1, m - i - 1) - F(1, m - 1) for i in range(m - 1)] + [F(0)]
        assert sum(defects) == sum((F(1, k) for k in range(1, m)), F(0)) - 1
        W = q + len(set(actual_leaf))
        OPT = q + m  # The m distinct petals and the common core.
        assert W == q + 2
    return {
        "m": m, "q": q, "L": L if factor_two else None,
        "all_histories_examined": histories_examined,
        "forced_actions_examined": forced_actions_examined,
        "actual_leaf": list(actual_leaf),
        "depth_max_regrets": list(map(str, defects)),
        "B": str(sum(defects)), "W": W, "OPT": OPT,
        "maximum_forced_to_prescribed_ratio": str(max_ratio),
    }


def audit_products():
    products = []
    for m in [4, 5]:
        complement = F(1)
        for r in range(1, m + 1):
            complement *= 1 - F(1, r * m)
        coverage_fraction = 1 - complement
        products.append({"m": m, "F_m(m)": str(coverage_fraction),
                         "inverse": str(1 / coverage_fraction)})
    assert products == [
        {"m": 4, "F_m(m)": "893/2048", "inverse": "2048/893"},
        {"m": 5, "F_m(m)": "6049/15625", "inverse": "15625/6049"},
    ]
    prefix_profit = F(0)
    profits = []
    for r in range(5, 0, -1):
        profit = (1 - prefix_profit) / (5 * r)
        assert prefix_profit + 5 * r * profit == 1
        profits.append(profit)
        prefix_profit += profit
    assert profits == [F(n, 15625) for n in [625, 750, 950, 1330, 2394]]
    assert prefix_profit == F(6049, 15625) < F(1, 2)
    return {
        "products": products,
        "five_player_scalar_relaxation": {
            "O": "1", "kappa": "5", "rho": ["0"] * 5,
            "u": list(map(str, profits)), "W": str(prefix_profit),
            "all_five_scalar_rows_are_equalities": True,
            "W_below_one_half": True,
            "interpretation": "Feasible scalar relaxation only; no SPE realization claimed.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Create JSON here; existing files are refused.")
    args = parser.parse_args()
    result = {
        "audit": "delete_repair_independent_v1",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "18-client witness; m=2,...,6,q=0 plans; products m=4,5; no expanded scan.",
        "finite_checks_are_not_general_proofs": True,
        "repair_witness": audit_repair_witness(repo_root() / SOURCE),
        "petal_plans": [audit_plan(m) for m in range(2, 7)],
        "factor_two_plans": [audit_plan(m, factor_two=True) for m in range(2, 7)],
        "products_and_scalar_relaxation": audit_products(),
        "all_assertions_passed": True,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as output:
            output.write(rendered)
        print(json.dumps({"output": str(args.output), "all_assertions_passed": True}, ensure_ascii=False))
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
