"""Exact independent-from-solver replay of the complete-policy NE witness."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

SIZES = (12, 15, 20, 30, 60, 60, 60, 60, 60, 60)
NAMES = tuple(f"A{i}" for i in range(1, 6)) + tuple(f"O{i}" for i in range(1, 6))
ACTUAL = tuple(range(5))


def policy(history):
    """One rule supplies the prescribed action at every ordered history."""
    assert len(history) < 5
    for k, theme in enumerate(history):
        if theme != ACTUAL[k]:
            return theme
    return ACTUAL[len(history)]


def finish(history):
    history = tuple(history)
    while len(history) < 5:
        history += (policy(history),)
    return history


def utility(terminal, i):
    # Topics are pairwise disjoint blocks of distinct unit customers.
    counts = Counter(terminal)
    return F(SIZES[terminal[i]], counts[terminal[i]])


def welfare(terminal):
    return sum(SIZES[t] for t in set(terminal))


actual = finish(())
assert actual == ACTUAL
payoffs = tuple(utility(actual, i) for i in range(5))
assert payoffs == tuple(map(F, (12, 15, 20, 30, 60)))
assert welfare(actual) == 137
assert sum(SIZES) == 437

# All full-policy unilateral deviations have one of these realized choices.
deviations = []
for i in range(5):
    for theme in range(10):
        terminal = finish(ACTUAL[:i] + (theme,))
        value = utility(terminal, i)
        assert value <= payoffs[i]
        deviations.append({"player": i + 1, "theme": NAMES[theme],
                           "terminal": [NAMES[t] for t in terminal],
                           "utility": str(value), "slack": str(payoffs[i] - value)})

opt = max(welfare(profile) for profile in combinations(range(10), 5))
assert opt == 300
# With repeated topics a union uses <=5 distinct themes; adding disjoint nonempty
# themes increases welfare, so 5-subsets suffice for the exact optimum.
assert opt > 2 * welfare(actual)

ordered_nodes = sum(10 ** depth for depth in range(5))
for depth in range(5):
    for history in product(range(10), repeat=depth):
        assert policy(history) in range(10)
assert ordered_nodes == 11111

history = (5,)  # O1
prescribed = finish(history)
alternative = finish(history + (6,))  # second player switches to O2
assert utility(prescribed, 1) == 12
assert utility(alternative, 1) == 60

# Exact dynamic/static smoothness residual for comparator (O1,...,O5).
true_queries = []
static_queries = []
for i in range(5):
    t = 5 + i
    true_queries.append(utility(finish(ACTUAL[:i] + (t,)), i))
    frozen = list(ACTUAL)
    frozen[i] = t
    static_queries.append(utility(tuple(frozen), i))
Gamma = sum(payoffs) - sum(true_queries)
Delta = sum(static_queries) - sum(true_queries)
static_slack = F(137) + sum(static_queries) - opt
assert Gamma == 0 and Delta == 163 and static_slack == 137
assert Gamma + static_slack - Delta == 2 * F(137) - opt == -26

report = {
    "status": "exact replay passed; pure policy-normal-form NE, explicitly not SPE",
    "customer_count": 437, "topic_count": 10, "decision_histories_defined": ordered_nodes,
    "normal_form_deviation_realizations_checked": len(deviations),
    "actual_terminal": [NAMES[t] for t in actual], "actual_payoffs": list(map(str, payoffs)),
    "W": 137, "OPT5": opt, "ratio": str(F(opt, 137)),
    "non_SPE": {"history": ["O1"], "player": 2,
                "prescribed_terminal": [NAMES[t] for t in prescribed],
                "alternative_terminal": [NAMES[t] for t in alternative],
                "prescribed_utility": "12", "alternative_utility": "60", "slack": "-48"},
    "residual": {"true_queries": list(map(str, true_queries)),
                 "static_queries": list(map(str, static_queries)),
                 "Gamma_sum": str(Gamma), "Delta_sum": str(Delta),
                 "static_slack_sum": str(static_slack), "2W_minus_OPT": "-26"},
    "deviations": deviations,
}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "deviations"}, ensure_ascii=False, indent=2))
