"""Definition-level exact checks for the round5_global examples and formulas."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def utilities(topics, profile):
    clients = set().union(*topics)
    load = {x: sum(x in topics[a] for a in profile) for x in clients}
    return [sum((F(1, load[x]) for x in topics[a]), F()) for a in profile]


def audit_dominance_counterexample():
    B, C, D = {0, 1, 2, 3}, {2, 3, 4}, {0, 1}
    topics = [B, C, D]
    response = [0, 0, 1]
    rows = [[utilities(topics, (first, last))[1] for last in range(3)]
            for first in range(3)]
    root = [utilities(topics, (first, response[first]))[0] for first in range(3)]
    assert rows == [[F(2), F(2), F(1)], [F(3), F(3, 2), F(2)], [F(3), F(3), F(1)]]
    assert root == [F(2)] * 3
    assert all(rows[i][response[i]] == max(rows[i]) for i in range(3))
    for c, other in product(range(3), repeat=2):
        assert utilities(topics, (0, other))[0] >= utilities(topics, (c, other))[0]
    return {"last_payoff_rows": [[str(x) for x in row] for row in rows],
            "root_true_payoffs": list(map(str, root)), "potential_actual": "5", "potential_BB": "6"}


def audit_diagnostic():
    # Four rows of compressed unit customers, explicitly expanded to five.
    A, B, T, Y1, Y2 = {4}, {1, 2, 3}, {0, 4}, {0, 3}, {1, 2, 4}
    topics = [A, B, T, Y1, Y2]
    all_actions = range(5)
    branch = (2, 3, 4)
    actual = (0, 1, 1)
    uA = utilities(topics, actual)[0]
    tau = F(len(A - B), 2)
    query = sum((F(1, 1 + 2 * (x in B)) for x in T), F())
    assert (uA, tau, query) == (F(1), F(1, 2), F(2))
    assert utilities(topics, branch) == [F(1), F(3, 2), F(5, 2)]

    # Compute all pure SPE outcomes of the two-player subgame after root B.
    last_br = {}
    for first in all_actions:
        vals = [utilities(topics, (1, first, last))[2] for last in all_actions]
        last_br[first] = [last for last in all_actions if vals[last] == max(vals)]
    floor = max(min(utilities(topics, (1, first, last))[1] for last in last_br[first])
                for first in all_actions)
    supported = [(first, last) for first in all_actions for last in last_br[first]
                 if utilities(topics, (1, first, last))[1] >= floor]
    root_B_payoffs = [utilities(topics, (1, first, last))[0] for first, last in supported]
    assert min(root_B_payoffs) == F(3, 2)
    return {"u_A": str(uA), "tau_A": str(tau), "q_T": str(query),
            "root_B_subgame_floor": str(floor), "supported_suffixes": supported,
            "minimum_root_B_payoff": str(min(root_B_payoffs))}


def audit_static_localization():
    # For each customer pattern the q(T)-q(B) difference minus tau and
    # B-outside tax equals minus the actual terminal BR slack.
    count = 0
    for bg, r, a, b, t in product((0, 1, 3, 17), (1, 2, 3, 7, 31), (0, 1), (0, 1), (0, 1)):
        qdiff = F(t - b, bg + 1 + r * b)  # If b=1, t-b is 0 or -1.
        # When b=0, denominator bg+1 is also exactly the desired denominator.
        tau = F(a * t * (1 - b), (bg + 1) * (bg + 2))
        residual = F(b * (1 - a) * (1 - t), (bg + r) * (bg + r + 1))
        br_slack = F(b * (1 - t), bg + r + a) - F(t * (1 - b), bg + 1 + a)
        assert qdiff == tau + residual - br_slack
        count += 1
    return {"pointwise_identity_cases": count, "note": "Formula proof in Markdown is for all b>=0,r>=1."}


if __name__ == "__main__":
    report = {"status": "passed", "dominance_counterexample": audit_dominance_counterexample(),
              "diagnostic_only": audit_diagnostic(), "localization": audit_static_localization()}
    output = Path(__file__).with_name("local_findings_audit.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
