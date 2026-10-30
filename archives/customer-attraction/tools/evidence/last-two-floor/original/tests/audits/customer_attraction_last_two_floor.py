"""Independent exact audit of the last-two payoff floor and all-n welfare bound.

The proof is in research/current/customer_attraction/last_two_floor.md. This
script checks its algebra and listed finite games; finite enumeration is not
the universal proof. No canonical or uploaded SPE implementation is imported.
Customer multiplicities are numbers of distinct unit clients.
"""

from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random
import subprocess


def utility(path, player, weights):
    action = path[player]
    return sum((F(count, sum(bool(mask & (1 << a)) for a in path))
                for mask, count in weights.items()
                if mask & (1 << action)), F(0))


def marginal(history, action, weights):
    return sum((F(count, 1 + sum(bool(mask & (1 << a)) for a in history))
                for mask, count in weights.items()
                if mask & (1 << action)), F(0))


def welfare(path, weights):
    return sum(count for mask, count in weights.items()
               if any(mask & (1 << a) for a in path))


def parameters(m, n, weights):
    largest = max(sum(count for mask, count in weights.items()
                      if mask & (1 << a)) for a in range(m))
    optimum = max(welfare(path, weights) for path in product(range(m), repeat=n))
    theta = min(max(marginal(h, a, weights) for a in range(m))
                for h in product(range(m), repeat=n - 1))
    histories_checked = 0
    for h in product(range(m), repeat=n - 1):
        b = max(marginal(h, a, weights) for a in range(m))
        budget = sum((F(count * load, load + 1)
                      for mask, count in weights.items()
                      if (load := sum(bool(mask & (1 << a)) for a in h))), F(0))
        assert budget == sum((marginal(h, a, weights) for a in h), F(0))
        assert optimum <= n * b + budget
        assert budget <= (n - 1) * b
        assert budget <= F((n - 1) * largest, 2)
        histories_checked += 1
    assert theta >= F(optimum, 2 * n - 1)
    assert theta >= F(2 * optimum - (n - 1) * largest, 2 * n)
    return largest, optimum, theta, histories_checked


def verify_policy(policy, m, n, weights):
    """Return the independently verified path, or None for a non-SPE policy."""
    histories = tuple(h for depth in range(n)
                      for h in product(range(m), repeat=depth))
    assert set(policy) == set(histories)
    assert all(0 <= a < m for a in policy.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == n else terminal(h + (policy[h],))

    for h in histories:
        depth = len(h)
        own = utility(terminal(h), depth, weights)
        if any(own < utility(terminal(h + (a,)), depth, weights)
               for a in range(m)):
            return None
    return terminal(()), terminal


def check_spe(policy, m, n, weights, params):
    verified = verify_policy(policy, m, n, weights)
    if verified is None:
        return None
    path, terminal = verified
    largest, optimum, theta, _ = params
    tail_histories = 0
    for p in product(range(m), repeat=n - 2):
        local_theta = min(max(utility(p + (a, b), n - 1, weights)
                              for b in range(m)) for a in range(m))
        assert local_theta >= theta
        actual = terminal(p)
        assert utility(actual, n - 2, weights) >= local_theta
        assert utility(actual, n - 1, weights) >= local_theta
        best_increment = max(marginal(p, a, weights) for a in range(m))
        for a in range(m):
            if marginal(p, a, weights) != best_increment:
                continue
            best_reply = max(utility(p + (a, b), n - 1, weights)
                             for b in range(m))
            for b in range(m):
                follower = utility(p + (a, b), n - 1, weights)
                if follower == best_reply:
                    assert utility(p + (a, b), n - 2, weights) >= follower
                    assert follower >= local_theta
        tail_histories += 1
    for depth in range(n):
        for h in product(range(m), repeat=depth):
            assert utility(terminal(h), depth, weights) >= F(largest, n)
    covered = welfare(path, weights)
    payoffs = tuple(utility(path, i, weights) for i in range(n))
    assert sum(payoffs, F(0)) == covered
    assert covered >= F((n - 2) * largest, n) + 2 * theta
    assert covered * n * (2 * n - 1) >= 4 * (n - 1) * optimum
    return path, tail_histories


def construct_policy(m, n, weights):
    """Ordinary full ordered-tree backward induction, with history-based ties."""
    policy = {}

    def visit(h):
        if len(h) == n:
            return h
        children = tuple(visit(h + (a,)) for a in range(m))
        values = tuple(utility(child, len(h), weights) for child in children)
        candidates = tuple(a for a in range(m) if values[a] == max(values))
        history_bit = (len(h) + sum((i + 1) * a for i, a in enumerate(h))) % 2
        chosen = candidates[-1] if history_bit else candidates[0]
        policy[h] = chosen
        return children[chosen]

    visit(())
    return policy


def run():
    if not __debug__:
        raise RuntimeError("Run without -O: this audit requires assertions.")
    atom_checks = 0
    for background in (0, 1, 2, 10, 1000, 10**40):
        for a, b in product((0, 1), repeat=2):
            denominator = background + a + b
            difference = F(a - b, denominator) if a + b else F(0)
            assert difference == F(a - b, background + 1)
            atom_checks += 1
    scalar_checks = 0
    for n in tuple(range(2, 31)) + (10**6,):
        wa, wb = F(1, n - 1), F(n - 2, n - 1)
        assert wa >= 0 and wb >= 0 and wa + wb == 1
        assert wa * F(n - 2, n) - wb / n == 0
        assert wa * F(2, 2 * n - 1) + wb * F(2, n) == F(4 * (n - 1), n * (2 * n - 1))
        for h in range(7):
            assert F(h, h + 1) <= F(h, 2)
            for d in range(n + 1) if n < 31 else (0, 1, n):
                assert F(h + d, h + 1) >= int(d > 0)
                scalar_checks += 1
    games = policies = valid = tail_histories = last_histories = 0
    observed_ordered_tie = False
    # Every complete policy, rather than terminal-count recurrence, is checked.
    # Two topics / three players: 27 clone-inputs, 128 policies per input.
    # Three topics / two players: 128 binary clone-inputs, 81 policies each.
    for m, n, alphabet in ((2, 3, range(3)), (3, 2, range(2))):
        histories = tuple(h for depth in range(n)
                          for h in product(range(m), repeat=depth))
        for values in product(alphabet, repeat=(1 << m) - 1):
            weights = {mask: value for mask, value in enumerate(values, 1) if value}
            params = parameters(m, n, weights)
            last_histories += params[-1]
            games += 1
            for actions in product(range(m), repeat=len(histories)):
                policy = dict(zip(histories, actions))
                result = check_spe(policy, m, n, weights, params)
                policies += 1
                if result is not None:
                    valid += 1
                    tail_histories += result[1]
                    if n == 3 and policy[(0, 1)] != policy[(1, 0)]:
                        observed_ordered_tie = True
    assert observed_ordered_tie
    # Explicit catalog boundaries: zero clients, duplicate coverage, empty
    # coverage labels, uninterested clients and a single available topic.
    selected = [
        (3, 5, {}), (3, 5, {3: 7, 0: 11}),
        (3, 5, {1: 4, 2: 2}), (1, 7, {1: 13, 0: 11}),
        (2, 6, {1: 2, 2: 2}),
    ]
    selected_seed = 20261010
    rng = random.Random(selected_seed)
    for index in range(40):
        m = 2 if index % 2 else 3
        n = rng.randrange(2, 8 if m == 2 else 6)
        selected.append((m, n, {mask: rng.randrange(21)
                                for mask in range(1 << m)}))
    selected_checks = 0
    for m, n, weights in selected:
        params = parameters(m, n, weights)
        policy = construct_policy(m, n, weights)
        checked = check_spe(policy, m, n, weights, params)
        assert checked is not None
        selected_checks += 1
        tail_histories += checked[1]
        last_histories += params[-1]
    # n=1 and n=0 are separate boundaries, not applications of theta_n.
    assert welfare((0,), {1: 3}) == utility((0,), 0, {1: 3}) == 3
    assert welfare((), {1: 3}) == 0
    root = Path(__file__).resolve().parents[2]
    return {
        "audit": "customer_attraction_last_two_floor",
        "scope": "exact formula checks and listed finite full-policy checks; universal proof in Markdown",
        "arithmetic": "fractions.Fraction",
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "python_version": platform.python_version(),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "replay_commands": ["python3 tests/audits/customer_attraction_last_two_floor.py"],
        "selected_rng_seed": selected_seed,
        "exhaustive_input_parameters": [
            {"topics": 2, "players": 3, "multiplicities": [0, 1, 2],
             "nonempty_interest_masks": [1, 2, 3]},
            {"topics": 3, "players": 2, "multiplicities": [0, 1],
             "nonempty_interest_masks": [1, 2, 3, 4, 5, 6, 7]},
        ],
        "selected_input_parameters": {
            "explicit_boundary_games": 5, "random_games": 40,
            "random_multiplicities_inclusive": [0, 20],
            "two_topic_player_range_inclusive": [2, 7],
            "three_topic_player_range_inclusive": [2, 5],
            "zero_interest_mask_included": True,
        },
        "atomwise_potential_difference_checks": atom_checks,
        "scalar_checks": scalar_checks,
        "complete_policy_enumeration_games": games,
        "complete_policies_checked": policies,
        "valid_complete_spe_policies_checked": valid,
        "selected_full_history_spe_checks": selected_checks,
        "last_node_numerical_histories_checked": last_histories,
        "last_two_ordered_histories_checked": tail_histories,
        "same_counts_different_replies_observed": observed_ordered_tie,
        "coefficient_n2": str(F(4, 6)),
        "coefficient_n3": str(F(8, 15)),
        "coefficient_n4": str(F(12, 28)),
        "all_checks_pass": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
