"""Independent exact checks of continuation shortcuts, not a universal proof.

The supplied JSON certificate is checked directly on the complete ordered tree.
This audit does not import the canonical solver, model, or certificate verifier.
Compressed multiplicities are expanded into distinct unit customers.
"""

from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def payoff(preferences, action, path):
    return sum((Fraction(1, sum(chosen in liked for chosen in path))
                for liked in preferences if action in liked), Fraction(0))


def welfare(preferences, path):
    return sum(any(chosen in liked for chosen in path) for liked in preferences)


def verify(preferences, topics, players, actions):
    expected = {history for depth in range(players)
                for history in product(range(topics), repeat=depth)}
    assert set(actions) == expected
    paths = {path: path for path in product(range(topics), repeat=players)}
    deviations = 0
    for depth in range(players - 1, -1, -1):
        for history in product(range(topics), repeat=depth):
            action = actions[history]
            actual = paths[history + (action,)]
            actual_payoff = payoff(preferences, action, actual)
            for alternative in range(topics):
                if alternative == action:
                    continue
                deviations += 1
                alternate = paths[history + (alternative,)]
                assert actual_payoff >= payoff(preferences, alternative, alternate)
            paths[history] = actual
    return paths[()], len(expected), deviations


def residual(preferences, path, topic):
    return sum(topic in liked and not any(chosen in liked for chosen in path)
               for liked in preferences)


def run():
    input_path = ROOT / "examples/customer_attraction/residual_counterexample.json"
    certificate_path = ROOT / "evidence/certificates/customer_attraction/residual_counterexample.json"
    instance = json.loads(input_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    preferences = tuple(frozenset(item["topics"]) for item in instance["customers"]
                        for _ in range(item["multiplicity"]))
    actions = {tuple(item["history"]): item["action"] for item in certificate["actions"]}
    topics, players = len(instance["topics"]), instance["players"]
    path, histories, deviations = verify(preferences, topics, players, actions)
    assert tuple(path.count(action) for action in range(topics)) == tuple(certificate["terminal_counts"])
    pay = tuple(payoff(preferences, action, path) for action in path)
    branch_pay = tuple(payoff(preferences, action, (action, actions[(action,)]))
                       for action in range(topics))
    follower_pay = tuple(payoff(preferences, actions[(action,)], (action, actions[(action,)]))
                         for action in range(topics))
    q = max(residual(preferences, path, action) for action in range(topics))
    covered = welfare(preferences, path)
    optimum = max(welfare(preferences, terminal)
                  for terminal in product(range(topics), repeat=players))
    assert path == (0, 1) and pay == (4, 5)
    assert branch_pay == (4,) * 5 and follower_pay == (5, 5, 5, 4, 4)
    assert q == 5 and covered == 9 and optimum == 10
    assert pay[0] < q and covered < players * q
    assert 2 * covered >= optimum

    # A complete m=3 history-dependent tie certificate. Both ordered histories
    # AB and BA have counts (1,1), but prescribe different terminal actions.
    singletons = (frozenset({0}), frozenset({1}))
    tie_actions = {(): 0, (0,): 1, (1,): 0,
                   (0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 0}
    tie_path, tie_histories, tie_deviations = verify(singletons, 2, 3, tie_actions)
    tie_pay = tuple(payoff(singletons, action, tie_path) for action in tie_path)
    assert tie_path == (0, 1, 0) and tie_pay == (Fraction(1, 2), 1, Fraction(1, 2))
    assert tie_actions[(0, 1)] != tie_actions[(1, 0)]
    assert tie_pay[0] < tie_pay[1] and tie_pay[1] > tie_pay[2]

    # A separate three-unit-customer non-PNE SPE. This retains the complete
    # history certificate independently of the smaller-player literature example.
    nonpne_preferences = (frozenset({0, 1}), frozenset({1, 2}), frozenset({2}))
    nonpne_actions = {(): 2, (0,): 2, (1,): 1, (2,): 0,
                     (0, 0): 2, (0, 1): 2, (0, 2): 1,
                     (1, 0): 2, (1, 1): 2, (1, 2): 2,
                     (2, 0): 2, (2, 1): 1, (2, 2): 1}
    nonpne_path, nonpne_histories, nonpne_deviations = verify(nonpne_preferences, 3, 3, nonpne_actions)
    nonpne_pay = tuple(payoff(nonpne_preferences, action, nonpne_path) for action in nonpne_path)
    static_deviation = payoff(nonpne_preferences, 1, (2, 1, 2))
    assert nonpne_path == (2, 0, 2) and nonpne_pay == (1, 1, 1)
    assert static_deviation == Fraction(4, 3) > nonpne_pay[1]

    return {
        "audit": "customer_attraction_continuations", "arithmetic": "fractions.Fraction",
        "scope": "Three supplied complete SPE certificates; no universal bound or all-SPE optimum inferred",
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "residual_counterexample": {
            "unit_customers": len(preferences), "path": list(path),
            "payoffs": [str(value) for value in pay],
            "root_branch_payoffs": [str(value) for value in branch_pay],
            "follower_branch_payoffs": [str(value) for value in follower_pay],
            "checked_histories": histories, "checked_deviations": deviations,
            "welfare": covered, "optimal_welfare": optimum, "max_residual": q,
            "refutes_per_agent_floor": True, "refutes_aggregate_floor": True,
            "half_coverage_holds_on_specified_path": True,
        },
        "history_ties": {
            "path": list(tie_path), "payoffs": [str(value) for value in tie_pay],
            "actions_at_AB_and_BA": [tie_actions[(0, 1)], tie_actions[(1, 0)]],
            "checked_histories": tie_histories, "checked_deviations": tie_deviations,
            "refutes_both_payoff_monotonicities": True,
        },
        "non_pne": {
            "path": list(nonpne_path), "payoffs": [str(value) for value in nonpne_pay],
            "middle_player_static_deviation": str(static_deviation),
            "checked_histories": nonpne_histories, "checked_deviations": nonpne_deviations,
        },
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        if args.output.exists():
            raise SystemExit("Refusing to overwrite frozen audit output")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    print(result, end="")
