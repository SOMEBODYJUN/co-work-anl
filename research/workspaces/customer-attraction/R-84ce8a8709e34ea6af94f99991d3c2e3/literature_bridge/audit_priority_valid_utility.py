#!/usr/bin/env python3
"""Definition-level audit of a priority allocation outer-class counterexample.

This does not implement equal-sharing CAG. Integer masks represent unit clients.
All histories are ordered; every available action is checked at every history.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def covered(actions):
    union = 0
    for action in actions:
        union |= action
    return union


def outcome_payoffs(profile, client_count):
    # Later owners overwrite earlier owners, independently of the stated formula.
    owner = [None] * client_count
    for player, action in enumerate(profile):
        for client in range(client_count):
            if action & (1 << client):
                owner[client] = player
    payoff = [0] * len(profile)
    for player in owner:
        if player is not None:
            payoff[player] += 1
    return tuple(payoff)


def copy_policy(history, catalog):
    return history[-1] if history else catalog[0]


def continue_policy(prefix, player_count, catalog):
    actions = list(prefix)
    while len(actions) < player_count:
        actions.append(copy_policy(tuple(actions), catalog))
    return tuple(actions)


def audit(player_count, zero_clients=False):
    m = player_count
    client_count = 0 if zero_clients else m
    catalog = (0,) if zero_clients else tuple(1 << j for j in range(m))

    profiles = tuple(itertools.product(catalog, repeat=m))
    optimum = 0
    marginal_slacks = []
    for profile in profiles:
        welfare = covered(profile).bit_count()
        payoff = outcome_payoffs(profile, client_count)
        assert sum(payoff) == welfare, (m, profile, payoff, "budget")
        for i in range(m):
            without_i = covered(profile[:i] + profile[i + 1:]).bit_count()
            slack = payoff[i] - (welfare - without_i)
            assert slack >= 0, (m, profile, i, "marginal")
            marginal_slacks.append(slack)
        optimum = max(optimum, welfare)

    # Coverage as a function of collections of catalog actions. Its lift to
    # player-labelled action atoms is the same union function with duplicate labels.
    catalog_collections = tuple(
        frozenset(j for j in range(len(catalog)) if mask & (1 << j))
        for mask in range(1 << len(catalog))
    )
    def collection_value(indices):
        return covered(catalog[j] for j in indices).bit_count()
    submodular_pairs = 0
    for left, right in itertools.product(catalog_collections, repeat=2):
        assert collection_value(left) + collection_value(right) >= (
            collection_value(left | right) + collection_value(left & right)
        ), (m, left, right, "submodular")
        if left <= right:
            assert collection_value(left) <= collection_value(right)
        submodular_pairs += 1

    history_count = 0
    deviation_count = 0
    minimum_spe_slack = None
    for i in range(m):
        for history in itertools.product(catalog, repeat=i):
            history_count += 1
            policy_outcome = continue_policy(history, m, catalog)
            policy_payoff = outcome_payoffs(policy_outcome, client_count)[i]
            for action in catalog:
                deviation_count += 1
                deviation_outcome = continue_policy(history + (action,), m, catalog)
                deviation_payoff = outcome_payoffs(deviation_outcome, client_count)[i]
                slack = policy_payoff - deviation_payoff
                assert slack >= 0, (m, history, action, "SPE", slack)
                minimum_spe_slack = slack if minimum_spe_slack is None else min(
                    minimum_spe_slack, slack
                )

    equilibrium_outcome = continue_policy((), m, catalog)
    equilibrium_welfare = covered(equilibrium_outcome).bit_count()
    equilibrium_payoffs = outcome_payoffs(equilibrium_outcome, client_count)
    if zero_clients:
        assert equilibrium_welfare == optimum == 0
        assert equilibrium_payoffs == (0,) * m
    else:
        assert equilibrium_welfare == 1 and optimum == m
        assert equilibrium_payoffs == (0,) * (m - 1) + (1,)
        assert (2 * equilibrium_welfare >= optimum) == (m <= 2)

    return {
        "players": m,
        "clients": client_count,
        "catalog_masks": list(catalog),
        "terminal_profiles_checked": len(profiles),
        "ordered_histories_checked": history_count,
        "history_action_deviations_checked": deviation_count,
        "coverage_submodular_pairs_checked": submodular_pairs,
        "minimum_marginal_slack": min(marginal_slacks),
        "minimum_SPE_slack": minimum_spe_slack,
        "equilibrium_outcome_masks": list(equilibrium_outcome),
        "equilibrium_payoffs": list(equilibrium_payoffs),
        "equilibrium_welfare": equilibrium_welfare,
        "optimum": optimum,
        "half_coverage_holds": 2 * equilibrium_welfare >= optimum,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "candidate": "LB-PRIORITY-VALID-UTILITY-SPE",
        "allocation": "full value to highest-index covering player; not equal sharing",
        "all_assertions_passed": True,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "positive_client_instances": [audit(m) for m in range(1, 5)],
        "zero_client_instances": [audit(m, True) for m in range(1, 5)],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
