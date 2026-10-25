"""Independent direct ordered-history audit of the reviewed menu witnesses.

No canonical SPE solver, author audit, or equilibrium-menu recursion is imported.
Finite checks validate explicit child strategies, not the arbitrary-m proof.
"""

from fractions import Fraction as F
from itertools import product
import json


def audit(m, a, b):
    actions = tuple(product(range(m), range(m - 1)))
    # Expand blocks into different unit customers; no weighted providers.
    assert a.denominator == b.denominator == 1
    customers = [((0, e), j) for e in range(m) for j in range(int(a))]
    customers += [((1, bank), j) for bank in range(m - 1) for j in range(int(b))]
    cover = {
        action: frozenset(i for i, ((coordinate, label), _) in enumerate(customers)
                          if label == action[coordinate])
        for action in actions
    }

    def payoff(terminal, index):
        own = cover[terminal[index]]
        return sum((F(1, sum(x in cover[action] for action in terminal))
                    for x in own), F(0))

    def repeated_bank(history):
        banks = [action[1] for action in history]
        return len(set(banks)) < len(banks)

    def fresh(history, coordinate, count):
        used = {action[coordinate] for action in history}
        return min(label for label in range(count) if label not in used)

    nodes = comparisons = exact_lower_witnesses = 0
    for i in range(2, m):
        prefix = tuple((0, bank) for bank in range(i - 1))
        for forced in actions:
            start = prefix + (forced,)
            target_bank = forced[1]

            def prescribed(history):
                economic = fresh(history, 0, m)
                if repeated_bank(history):
                    bank = fresh(history, 1, m - 1)
                elif len(history) == m - 1:
                    bank = target_bank
                else:
                    bank = fresh(history, 1, m - 1)
                return economic, bank

            def finish(history):
                while len(history) < m:
                    history = history + (prescribed(history),)
                return history

            def check(history):
                nonlocal nodes, comparisons
                if len(history) == m:
                    return
                nodes += 1
                current = len(history)
                actual = finish(history)
                value = payoff(actual, current)
                for action in actions:
                    alternative = finish(history + (action,))
                    assert value >= payoff(alternative, current), (
                        m, a, b, i, forced, history, action, value,
                        payoff(alternative, current))
                    comparisons += 1
                    check(history + (action,))

            check(start)
            current_value = payoff(finish(start), i - 1)
            assert current_value <= a + b / 2
            if forced[0] != 0 and forced[1] < i - 1:
                # Fresh economic plus a used singleton bank. Every true
                # continuation is handled analytically by fresh sufficiency;
                # this explicit continuation also realizes the lower witness.
                assert current_value == a + b / 2
                exact_lower_witnesses += 1

    target = tuple((0, bank) for bank in range(m - 1)) + ((1, 0),)
    utilities = [payoff(target, i) for i in range(m)]
    union = frozenset().union(*(cover[action] for action in target))
    assert utilities[0] == a / (m - 1) + b / 2
    assert all(x == a / (m - 1) + b for x in utilities[1:-1])
    assert utilities[-1] == a + b / 2
    assert len(union) == 2 * a + (m - 1) * b == sum(utilities)
    t = a * F(m - 2, m - 1) - b / 2
    balance = (4 - m) * a + (m - 1) * b
    whole_nodes = whole_comparisons = 0
    if t <= 0:
        def whole_prescribed(history):
            if not history:
                return 0, 0
            anchor_e, anchor_bank = history[0]
            mode, target_bank = "BASE", None
            # Reconstruct the mode from every observed ordered action.
            for position in range(1, len(history)):
                past = history[:position]
                observed = history[position]
                used_banks = {action[1] for action in past}
                if mode == "BASE":
                    expected = (anchor_e, fresh(past, 1, m - 1))
                    if observed != expected:
                        if observed[1] in used_banks:
                            mode = "EXIT"
                        else:
                            mode, target_bank = "PUNISH", observed[1]
                elif mode == "PUNISH" and observed[1] in used_banks:
                    mode = "EXIT"
            if mode == "EXIT":
                return fresh(history, 0, m), fresh(history, 1, m - 1)
            if len(history) == m - 1:
                return (fresh(history, 0, m),
                        anchor_bank if mode == "BASE" else target_bank)
            if mode == "BASE":
                return anchor_e, fresh(history, 1, m - 1)
            return fresh(history, 0, m), fresh(history, 1, m - 1)

        def whole_finish(history):
            while len(history) < m:
                history = history + (whole_prescribed(history),)
            return history

        def whole_check(history):
            nonlocal whole_nodes, whole_comparisons
            if len(history) == m:
                return
            whole_nodes += 1
            current = len(history)
            actual_value = payoff(whole_finish(history), current)
            for action in actions:
                alternative = whole_finish(history + (action,))
                assert actual_value >= payoff(alternative, current), (
                    "whole", m, a, b, history, action)
                whole_comparisons += 1
                whole_check(history + (action,))

        whole_check(())
        assert whole_finish(()) == target
        for root_action in actions:
            assert payoff(whole_finish((root_action,)), 0) == utilities[0]

    if t >= 0:
        lower = balance + (2 * m - 3) * t
        assert lower == a * (m - 1 + F(1, m - 1)) + b / 2 > 0
    else:
        lower = balance + (m - 3) * t
        assert lower == F(m + 1, 2) * b + 2 * a / (m - 1) > 0
    return {
        "m": m, "a": str(a), "b": str(b), "ordered_nodes": nodes,
        "full_action_comparisons": comparisons,
        "exact_lower_witnesses": exact_lower_witnesses,
        "credible_root_ordered_nodes": whole_nodes,
        "credible_root_full_action_comparisons": whole_comparisons,
        "t": str(t), "checked_budget_bound": str(lower),
    }


if __name__ == "__main__":
    cases = [(3, F(2), F(1)), (3, F(1), F(2)),
             (4, F(1), F(1)), (4, F(1), F(2))]
    print(json.dumps({"status": "passed", "cases": [audit(*case) for case in cases]},
                     ensure_ascii=False, indent=2))
