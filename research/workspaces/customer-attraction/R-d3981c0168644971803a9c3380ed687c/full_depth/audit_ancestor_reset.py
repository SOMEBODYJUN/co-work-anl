"""Exact, self-contained audit of branch-local ancestor promises.

Only expands unit customers and applies the literal finite game definition.
Does not import the repository solver, a previous audit, or optimization code.
"""

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def show(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): show(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [show(v) for v in value]
    return value


TOPICS = ({0}, {0, 1}, {1, 2})
LABELS = "ABC"
STRATEGY = {
    (): 2,
    (0,): 2, (1,): 1, (2,): 0,
    (0, 0): 2, (0, 1): 2, (0, 2): 1,
    (1, 0): 2, (1, 1): 2, (1, 2): 2,
    (2, 0): 2, (2, 1): 1, (2, 2): 1,
}


def reward(terminal, actor):
    own = TOPICS[terminal[actor]]
    return sum((Q(1, sum(x in TOPICS[a] for a in terminal))
                for x in own), Q())


def text_path(path):
    return "".join(LABELS[a] for a in path)


def replay(history):
    history = tuple(history)
    while len(history) < 3:
        history += (STRATEGY[history],)
    return history


def terminal_set(history):
    """Literal set-valued BI on the ordered tree, with all pure ties."""
    history = tuple(history)
    if len(history) == 3:
        return {history}
    actor = len(history)
    children = {a: terminal_set(history + (a,)) for a in range(3)}
    floors = {a: min(reward(z, actor) for z in terminals)
              for a, terminals in children.items()}
    floor = max(floors.values())
    return {z for terminals in children.values() for z in terminals
            if reward(z, actor) >= floor}


def main():
    expected_keys = {h for depth in range(3)
                     for h in product(range(3), repeat=depth)}
    assert set(STRATEGY) == expected_keys
    comparisons = []
    for history in sorted(expected_keys, key=lambda h: (len(h), h)):
        actor = len(history)
        actual = replay(history)
        actual_value = reward(actual, actor)
        for alternative in range(3):
            terminal = replay(history + (alternative,))
            other_value = reward(terminal, actor)
            assert actual_value >= other_value
            comparisons.append({
                "history": text_path(history), "actual": text_path(actual),
                "alternative": LABELS[alternative],
                "terminal": text_path(terminal),
                "actual_payoff": actual_value, "alternative_payoff": other_value,
            })
    assert replay(()) == (2, 0, 2)
    assert [reward(replay(()), i) for i in range(3)] == [Q(1)] * 3

    cap = Q(1)
    child_tables = []
    for alternative in range(3):
        terminals = terminal_set((2, alternative))
        accepted = {z for z in terminals if reward(z, 0) <= cap}
        assert accepted
        child_tables.append({
            "action": LABELS[alternative],
            "outcomes": [{"terminal": text_path(z),
                          "ancestor": reward(z, 0),
                          "current": reward(z, 1)} for z in sorted(terminals)],
            "unrestricted_floor": min(reward(z, 1) for z in terminals),
            "cap_floor": min(reward(z, 1) for z in accepted),
        })
    assert [row["unrestricted_floor"] for row in child_tables] == [Q(1, 2), Q(5, 6), Q(5, 6)]
    assert [row["cap_floor"] for row in child_tables] == [Q(1), Q(4, 3), Q(5, 6)]
    assert max(row["unrestricted_floor"] for row in child_tables) == Q(5, 6)
    assert max(row["cap_floor"] for row in child_tables) == Q(4, 3)
    assert reward((2, 0, 2), 1) == Q(1)
    assert reward((2, 1, 1), 1) == Q(5, 6)
    assert reward((2, 1, 1), 0) == Q(4, 3)

    # Exact intersection of the real SPE continuation set is different from
    # restricting all sibling witnesses before computing the current floor.
    true_capped = {z for z in terminal_set((2,)) if reward(z, 0) <= cap}
    assert (2, 0, 2) in true_capped
    inherited_floor = max(row["cap_floor"] for row in child_tables)
    hereditary_cap_outcomes = {
        z for a in range(3) for z in terminal_set((2, a))
        if reward(z, 0) <= cap and reward(z, 1) >= inherited_floor
    }
    assert (2, 0, 2) not in hereditary_cap_outcomes

    # An all-large-theme SPE has no uniform multiplicative hereditary cap.
    # |L|=m, |B|=1, disjoint. At arbitrary prefix with k old L choices and
    # r remaining players, strategy all-L gives current payoff m/(k+r)>=1;
    # deviating to B gives <=1. This formula covers every ordered history.
    family = []
    for m in range(3, 31):
        checked_states = 0
        for depth in range(m):
            for old_large in range(depth + 1):
                old_small = depth - old_large
                remaining = m - depth
                actual = Q(m, old_large + remaining)
                deviation = Q(1, old_small + 1)
                assert actual >= deviation
                checked_states += 1
        descendant_ancestor = Q(m, 2)  # history L B^(m-2), then prescribed L
        assert descendant_ancestor > 1
        family.append({"m": m, "actual_root": Q(1),
                       "descendant_ancestor": descendant_ancestor,
                       "ratio": descendant_ancestor,
                       "count_states_checked": checked_states})

    result = {
        "status": "exact checks passed; no half theorem or half counterexample",
        "unit_customers": 3,
        "topics": {LABELS[a]: sorted(t) for a, t in enumerate(TOPICS)},
        "strategy_nodes": len(STRATEGY),
        "deviation_comparisons_including_self": len(comparisons),
        "actual": "CAC", "payoffs": [Q(1)] * 3,
        "all_comparisons": comparisons,
        "prefix_C_tables": child_tables,
        "correct_floor": Q(5, 6), "hereditary_cap_floor": Q(4, 3),
        "action_B_reset_premium": Q(1, 2),
        "true_capped_outcomes": [text_path(z) for z in sorted(true_capped)],
        "hereditary_cap_outcomes": [text_path(z) for z in sorted(hereditary_cap_outcomes)],
        "unbounded_cap_family_formula": "descendant root reward / actual root reward = m/2",
        "family_finite_regression": family,
    }
    output = Path(__file__).with_name("ancestor_reset_exact.json")
    output.write_text(json.dumps(show(result), indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(output),
                      "status": result["status"],
                      "nodes": len(STRATEGY), "comparisons": len(comparisons),
                      "correct_floor": "5/6", "incorrect_floor": "4/3"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
