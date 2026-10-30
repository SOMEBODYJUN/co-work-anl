"""Independent exact audit of the actual-root-tail-menu security barrier.

Expands 36 individual unit customers. Imports no canonical model, SPE solver,
previous audit, floating optimizer, or symbolic package. The universal menu
failure is the two-row affine identity checked below, rather than a grid of
sampled distributions. Existing frozen reports are never overwritten.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "examples/customer_attraction/aggregate_theta_failure.json"
CERT = ROOT / "evidence/certificates/customer_attraction/aggregate_theta_failure.json"
X, Y = tuple(range(3)), tuple(range(3, 6))
LABELS = X + Y


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run():
    customers = [frozenset((x, y)) for x in X for y in Y]
    customers += [frozenset(i + j) for i in combinations(X, 2)
                  for j in combinations(Y, 2) for _ in range(3)]
    require(len(customers) == 36, "unit customer count")
    themes = {a: frozenset(i for i, likes in enumerate(customers) if a in likes)
              for a in LABELS}

    def payoff(action, competitors):
        return sum((F(1, 1 + sum(customer in themes[b] for b in competitors))
                    for customer in themes[action]), F(0))

    def policy(history):
        if not history:
            return X[0]
        if len(history) == 1:
            return Y[0] if history[0] in X else X[0]
        group = X if history[1] in X else Y
        return next(a for a in group if a not in history)

    def terminal(history):
        while len(history) < 3:
            history += (policy(history),)
        return history

    raw = json.loads(INPUT.read_text())
    expected = [frozenset(row["topics"]) for row in raw["customers"]
                for _ in range(row["multiplicity"])]
    require(raw["players"] == 3 and len(raw["topics"]) == 6, "input dimensions")
    require(sorted(map(sorted, customers)) == sorted(map(sorted, expected)), "input unit expansion")
    cert = json.loads(CERT.read_text())
    rows = cert["strategy"]["actions"]
    saved = {tuple(row["history"]): row["action"] for row in rows}
    expected_actions = {h: policy(h) for depth in range(3)
                        for h in product(LABELS, repeat=depth)}
    require(len(saved) == len(rows) == 43 and saved == expected_actions, "complete stored strategy")

    slacks = []
    for history in expected_actions:
        depth = len(history)
        outcome = terminal(history)
        own = payoff(outcome[depth], outcome[:depth] + outcome[depth + 1:])
        for a in LABELS:
            off = terminal(history + (a,))
            alternate = payoff(a, off[:depth] + off[depth + 1:])
            require(own >= alternate, ("non-SPE", history, a, own, alternate))
            slacks.append(own - alternate)

    root = terminal(())
    root_values = [payoff(a, root[:i] + root[i + 1:]) for i, a in enumerate(root)]
    coverage = lambda actions: len(set().union(*(themes[a] for a in actions)))
    welfare = coverage(root)
    optimum = max(coverage(actions) for actions in product(LABELS, repeat=3))
    require(root == (0, 3, 4) and root_values == [10, 12, 12], "root path/payoffs")
    require((welfare, optimum) == (34, 36), "coverage and optimum")

    menus = {a: terminal((a,))[1:] for a in LABELS}
    require(set(menus.values()) == {(0, 1), (3, 4)}, "real root continuation menu")
    require(all(menus[a] == ((3, 4) if a in X else (0, 1)) for a in LABELS), "root action reply map")
    menu = ((0, 1), (3, 4))
    matrix = tuple(tuple(payoff(a, competitors) for competitors in menu) for a in LABELS)
    require(matrix == ((9, 10), (9, 10), (12, 10), (10, 9), (10, 9), (10, 12)), "exact menu matrix")
    # Both omitted rows are affine in lambda. Their coefficient sum is zero
    # and constant sum is 22; hence max >= 11 at every legal lambda.
    omitted = tuple((row[1], row[0] - row[1]) for row in (matrix[2], matrix[5]))
    require(omitted == ((10, 2), (12, -2)), "affine omitted-label rows")
    require(tuple(sum(pair[j] for pair in omitted) for j in range(2)) == (22, 0), "universal menu lower bound")
    half_values = tuple(sum(row, F(0)) / 2 for row in matrix)
    require(max(half_values) == 11, "matching menu dual upper bound")
    require(all(payoff(a, menus[a]) == 10 for a in LABELS), "all adaptive root deviations")

    # Uniform six-theme primal, against every ordered competitor pair.
    primal = {pair: sum((payoff(a, pair) for a in LABELS), F(0)) / 6
              for pair in product(LABELS, repeat=2)}
    require(min(primal.values()) == 10, "unrestricted safety primal >= 10")
    for pair, val in primal.items():
        category = "repeat" if pair[0] == pair[1] else "same" if (pair[0] in X) == (pair[1] in X) else "cross"
        require(val == {"repeat": F(37, 3), "same": F(10), "cross": F(97, 9)}[category], "all competitor category values")
    dual_menu = tuple(combinations(X, 2)) + tuple(combinations(Y, 2))
    dual = tuple(sum((payoff(a, pair) for pair in dual_menu), F(0)) / 6 for a in LABELS)
    require(dual == (10,) * 6, "unrestricted safety dual <= 10")

    # Stationary kernel of uniformly sampling one real follower action.
    kernel = tuple(tuple(F(menus[a].count(b), 2) for b in LABELS) for a in LABELS)
    stationary = (F(1, 4), F(1, 4), F(0), F(1, 4), F(1, 4), F(0))
    require(tuple(sum((stationary[a] * kernel[a][b] for a in LABELS), F(0)) for b in LABELS) == stationary, "exact stationarity")
    push = tuple(sum((stationary[a] for a in LABELS if menus[a] == pair), F(0)) for pair in menu)
    require(push == (F(1, 2), F(1, 2)), "stationary real-menu weights")

    return {
        "scope": "actual root continuation-menu dual fails; general security and halfcoverage remain open",
        "input_unit_customers": len(customers),
        "all_ordered_decision_histories": len(expected_actions),
        "exact_SPE_action_comparisons": len(slacks),
        "minimum_SPE_slack": str(min(slacks)),
        "root_path": root,
        "root_payoffs": list(map(str, root_values)),
        "root_deviation_payoffs": [str(payoff(a, menus[a])) for a in LABELS],
        "actual_root_reply_pairs": menu,
        "menu_matrix": [[str(x) for x in row] for row in matrix],
        "all_probability_menu_minimax_value": "11",
        "unrestricted_safety_value": "10",
        "primal_ordered_competitor_pairs_checked": len(primal),
        "unrestricted_dual_pairs": dual_menu,
        "unrestricted_dual_row_values": list(map(str, dual)),
        "stationary_root_theme_distribution": list(map(str, stationary)),
        "stationary_actual_menu_distribution": list(map(str, push)),
        "stationary_cap": "11",
        "welfare": welfare,
        "optimum": optimum,
        "two_welfare_minus_optimum": 2 * welfare - optimum,
        "positive_compiled_family_menu_regressions": [compiled_menu(n) for n in range(3, 7)],
        "sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in (INPUT, CERT, Path(__file__).resolve())},
    }


def compiled_menu(n):
    """Direct positive-menu arithmetic; full-history existence uses M2's proof.

    These finite menu regressions do not claim to enumerate every full ordered
    history of the larger instances. The complete-family SPE proof is in the
    canonical manuscript and explicitly uses CA-MOBIUS-FULL-HISTORY-EMBED.
    """
    p = 2 * n
    size = 1 << p
    left = (1 << n) - 1
    potential = []
    for mask in range(size):
        count = mask.bit_count()
        own = (mask & left).bit_count()
        pure = own in (0, count)
        potential.append(int(pure) if count == n else -int(not pure) if count == n - 1 else 0)
    coefficients = potential.copy()
    for bit in range(p):
        for mask in range(size):
            if mask & (1 << bit):
                coefficients[mask] -= coefficients[mask ^ (1 << bit)]
    signed = [(-1) ** (mask.bit_count() + 1) * mask.bit_count() * coefficient
              for mask, coefficient in enumerate(coefficients)]
    for bit in range(p):
        for mask in range(size):
            if not mask & (1 << bit):
                signed[mask] -= signed[mask | (1 << bit)]
    mass = sum(abs(x) for x in signed[1:])
    bias = 4 * mass + 1
    weights = [0] + [x + bias for x in signed[1:]]
    require(min(weights[1:]) >= 1, "positive unit-customer multiplicities")
    baseline = F(size - (1 << n), n)
    root_payoff = bias * baseline
    x_tail = tuple(range(n - 1))
    y_tail = tuple(range(n, 2 * n - 1))

    def direct(action, competitors):
        return sum((F(weight, 1 + sum(bool(mask & (1 << b)) for b in competitors))
                    for mask, weight in enumerate(weights) if mask & (1 << action)), F(0))

    rows = [tuple(direct(a, tail) for tail in (x_tail, y_tail)) for a in range(p)]
    require(rows[n - 1] == (root_payoff + 1, root_payoff), "omitted X label")
    require(rows[p - 1] == (root_payoff, root_payoff + 1), "omitted Y label")
    require(all(rows[a][1 if a < n else 0] == root_payoff for a in range(p)), "all real root branch payoffs")
    for a in list(x_tail) + list(y_tail):
        own_column = 0 if a < n else 1
        require(rows[a][own_column] <= root_payoff - mass - F(1, 2), "old static query cap")
    half_rows = [sum(row, F(0)) / 2 for row in rows]
    require(max(half_rows) == root_payoff + F(1, 2), "exact actual-menu cap")

    expanded = tuple(combinations(range(n), n - 1)) + tuple(combinations(range(n, p), n - 1))
    expanded_values = [sum((direct(a, tail) for tail in expanded), F(0)) / (2 * n) for a in range(p)]
    cap_bound = root_payoff + F(1 - (n - 1) * (mass + F(1, 2)), 2 * n)
    require(max(expanded_values) <= cap_bound <= root_payoff, "expanded static dual remains below root")
    return {
        "players": n, "topics": p, "signed_absolute_mass": mass,
        "uniform_positive_bias": bias, "smallest_positive_type_count": min(weights[1:]),
        "unit_bias_fresh_payoff": str(baseline), "root_payoff": str(root_payoff),
        "omitted_X_query_row": list(map(str, rows[n - 1])),
        "omitted_Y_query_row": list(map(str, rows[p - 1])),
        "actual_root_menu_minimax_value": str(root_payoff + F(1, 2)),
        "actual_root_menu_minus_root": "1/2",
        "expanded_nonactual_dual_columns": len(expanded),
        "expanded_nonactual_dual_cap": str(max(expanded_values)),
        "expanded_nonactual_dual_upper_bound": str(cap_bound),
        "scope": "positive input and exact root-menu arithmetic; full-history SPE existence follows from the manuscript's M2-based proof, not this finite regression",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(run(), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x") as handle:
            handle.write(report)
    print(report, end="")


if __name__ == "__main__":
    main()
