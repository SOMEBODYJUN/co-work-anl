"""Exact definition-level audit of the full-menu potential-rise obstruction.

No optimization or canonical CAG implementation is imported.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import json


COUNTS_791 = {
    1: 12, 2: 109, 4: 3, 9: 86, 12: 60, 16: 109,
    19: 18, 21: 27, 22: 3, 26: 27, 29: 36, 33: 48,
    36: 82, 42: 36, 43: 36, 45: 9, 46: 36, 51: 9, 53: 45,
}
COUNTS_24 = {
    2: 3, 9: 3, 12: 2, 16: 3, 21: 1, 23: 1, 29: 1, 33: 2,
    36: 2, 42: 1, 43: 1, 46: 1, 53: 1, 54: 1, 58: 1,
}
TOPICS = ("X0", "X1", "X2", "Y0", "Y1", "Y2", "Empty")


def strategy(history):
    if not history:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    first, second = history
    nonempty = [a for a in history if a != 6]
    if not nonempty:
        return 0
    if len(nonempty) == 1:
        return (1, 0, 0, 4, 3, 3)[nonempty[0]]
    group = range(3) if second < 3 else range(3, 6)
    return next(a for a in group if a not in history)


def main(case):
    counts = COUNTS_24 if case == 24 else COUNTS_791
    interests = []
    for mask, count in counts.items():
        interests.extend([frozenset(a for a in range(7) if mask >> a & 1)] * count)
    topic_sets = [{x for x, labels in enumerate(interests) if a in labels} for a in range(7)]

    def terminal(history):
        history = tuple(history)
        while len(history) < 3:
            history += (strategy(history),)
        return history

    def utility(a, profile, extra=0):
        return sum((Fraction(1, extra + sum(x in topic_sets[b] for b in profile))
                    for x in topic_sets[a]), Fraction(0))

    def potential(profile):
        return sum((sum((Fraction(1, j) for j in
                         range(1, 1 + sum(x in topic_sets[b] for b in profile))), Fraction(0))
                    for x in range(len(interests))), Fraction(0))

    def welfare(profile):
        return len(set().union(*(topic_sets[a] for a in profile)))

    actions = []
    slacks = []
    for depth in range(3):
        for history in product(range(7), repeat=depth):
            actions.append({"history": list(history), "action": strategy(history)})
            original = terminal(history)
            original_u = utility(original[depth], original)
            for deviation in range(7):
                changed = terminal(history + (deviation,))
                slack = original_u - utility(deviation, changed)
                assert slack >= 0, (history, deviation, slack)
                slacks.append({"history": list(history), "deviation": deviation, "slack": str(slack)})

    root = terminal(())
    root_u = utility(root[0], root)
    menu = []
    for b in range(7):
        profile = terminal((b,))
        menu.append({"first_action": b, "terminal": list(profile),
                     "owner_payoff": str(utility(b, profile)),
                     "potential": str(potential(profile)), "welfare": welfare(profile),
                     "query_cap_values": [str(utility(a, profile, extra=1)) for a in range(7)]})

    a, b = 2, 4
    za, zb = terminal((a,)), terminal((b,))
    cap = utility(a, zb, extra=1)
    maximum_potential = max(Fraction(row["potential"]) for row in menu)
    assert len(interests) == case
    assert len({frozenset(s) for s in topic_sets}) == 7
    assert not topic_sets[6]
    assert len(actions) == 57 and len(slacks) == 399
    assert root == (0, 3, 4)
    if case == 24:
        assert [utility(c, root) for c in root] == [Fraction(35, 6), Fraction(41, 6), Fraction(19, 3)]
        assert welfare(root) == 19
        assert potential(za) == potential(zb) == maximum_potential == Fraction(143, 6)
        assert cap == Fraction(73, 12) > root_u == Fraction(35, 6)
        assert cap - root_u == Fraction(1, 4)
        assert max(utility(a, root, extra=1) for a in range(7)) == Fraction(11, 2) < root_u
    else:
        assert [utility(c, root) for c in root] == [187, 223, 187]
        assert welfare(root) == 597
        assert potential(za) == potential(zb) == maximum_potential == Fraction(1511, 2)
        assert cap == Fraction(409, 2) > root_u == 187
        assert cap - root_u == Fraction(35, 2)
        assert max(utility(a, root, extra=1) for a in range(7)) == Fraction(353, 2) < root_u
        # Stronger failure of even weak nondecrease: the profitable query's
        # forced-root terminal has strictly lower harmonic potential.
        assert utility(5, terminal((1,)), extra=1) == 196 > root_u
        assert potential(terminal((5,))) - potential(terminal((1,))) == -3

    report = {
        "status": "EXACT PASS", "customers": len(interests), "topics": list(TOPICS),
        "integer_types": counts, "actions": actions,
        "comparisons_checked": len(slacks), "minimum_slack": min(Fraction(s["slack"]) for s in slacks).__str__(),
        "comparison_slacks": slacks, "root": list(root), "root_u": str(root_u),
        "root_utilities": [str(utility(c, root)) for c in root], "root_welfare": welfare(root),
        "root_menu": menu, "query_a": a, "column_b": b,
        "cap": str(cap), "cap_minus_root_u": str(cap - root_u),
        "potential_a": str(potential(za)), "potential_b": str(potential(zb)),
        "maximum_menu_potential": str(maximum_potential),
        "scope": "Refutes K_ab>u=>Phi(Z(a))>Phi(Z(b)) and every-max-Phi-column blocker; not existence of a good max-Phi column, pure blocker, mixed full menu, extra-one, or half.",
    }
    output = Path(__file__).with_name("phi_rise_24_exact.json" if case == 24 else "phi_rise_exact.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in (
        "status", "customers", "comparisons_checked", "root_u", "root_welfare",
        "cap", "potential_a", "potential_b")}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=(24, 791), default=24)
    main(parser.parse_args().case)
