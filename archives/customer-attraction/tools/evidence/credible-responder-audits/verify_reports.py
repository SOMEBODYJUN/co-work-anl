"""Check both frozen reports from customer loads and explicit branch paths."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def payoff(topic, others):
    loads = Counter(customer for other in others for customer in other)
    return sum((Fraction(1, 1 + loads[customer]) for customer in topic), Fraction())


def terminal_pair_gain(middle, query, reply, actual_last):
    return (
        payoff(reply, [*middle, query])
        - payoff(query, [*middle, reply])
        - payoff(actual_last, [*middle, query])
    )


def piecewise_kernel(load, t, r, d):
    if t == r:
        return -Fraction(d, load + t + 1)
    if t == 0:
        return Fraction(1 - d, load + 1)
    return -Fraction(1, load + 1) - Fraction(d, load + 2)


def verify_exchange(terminal, defect):
    membership_rows = []
    identity_rows = 0
    customer = {0}
    for location, t, r in product(("A", "H", "D", "outside"), range(2), range(2)):
        actual, other, last = (customer if location == label else set() for label in "AHD")
        query = customer if t else set()
        reply = customer if r else set()
        charge = Fraction(t, 2) if location in ("H", "D") else Fraction(t)
        target = Fraction(3 * len(actual), 2) - charge
        fixed_gain = terminal_pair_gain([other], query, reply, last)
        fixed_part = len(actual) + len(last) - payoff(reply, [actual, other])
        uncovered_part = Fraction(len(actual - reply), 2)
        assert target == fixed_part + fixed_gain + uncovered_part
        membership_rows.append({"location": location, "T": t, "R": r, "both_sides": str(target)})
        for new_load in range(8):
            branch_gain = terminal_pair_gain([customer] * new_load, query, reply, last)
            defect_gain = (
                piecewise_kernel(new_load, t, r, len(last))
                - piecewise_kernel(len(other), t, r, len(last))
            )
            assert defect_gain == branch_gain - fixed_gain
            assert target == fixed_part + branch_gain + uncovered_part - defect_gain
            identity_rows += 1
    assert membership_rows == terminal["membership_rows"]
    assert identity_rows == defect["identity_rows"] == 128

    convex_checks = []
    for k in range(1, 101):
        early_budget = (Fraction(2 * k + 1, k), Fraction(1, 2))
        last_budget = (Fraction(1, 2), Fraction(k + 1))
        early_difference = early_budget[0] - early_budget[1]
        last_difference = last_budget[1] - last_budget[0]
        weight = last_difference / (early_difference + last_difference)
        mixed = [weight * a + (1 - weight) * b for a, b in zip(early_budget, last_budget)]
        assert 0 < weight < 1 and mixed[0] == mixed[1] < 2
        assert 2 - mixed[0] == Fraction(5 * k + 4, 4 * (k + 1) ** 2)
        convex_checks.append({"k": k, "lambda": str(weight), "beta": str(mixed[0])})
    assert convex_checks == terminal["convex_checks"]


def verify_family_case(k, saved):
    group = [{(index, 0), (index, 1)} for index in range(k)]
    private = [core | {(index, 2)} for index, core in enumerate(group)]
    b, d = (-1, 0), (-1, 1)
    shared = [core | {b} for core in group]
    last = {b, d}
    comparison = [*private, last]
    catalog = [*comparison, *shared, *group]
    assert payoff(last, group) == max(payoff(topic, group) for topic in catalog) == 2
    assert all(payoff(core, [*group[:i], *group[i + 1 :], last]) == 2 for i, core in enumerate(group))
    assert set().union(*comparison) == set().union(*catalog)

    rows = []
    total = Fraction()
    terminal_comparisons = 0
    for i in range(k):
        actual_middle = [*group[:i], *group[i + 1 :]]
        for j, query in enumerate(comparison):
            if i <= j < k:
                future = [group[g] for g in range(i, k) if g != j]
                reply = shared[j]
            else:
                future = private[i:-1]
                reply = private[-1]
            middle = [*group[:i], *future]
            preterminal = [*middle, query]
            assert len(middle) == k - 1
            assert payoff(query, [*middle, reply]) == 2
            assert payoff(reply, preterminal) == max(payoff(topic, preterminal) for topic in catalog)
            terminal_comparisons += len(catalog)
            if not i <= j < k:
                terminal = [*preterminal, reply]
                assert all(payoff(topic, [*terminal[:g], *terminal[g + 1 :]]) == 3
                           for g, topic in enumerate(terminal) if i <= g < k - 1)
                assert payoff(reply, preterminal) == 3
            delta = (
                terminal_pair_gain(middle, query, reply, last)
                - terminal_pair_gain(actual_middle, query, reply, last)
            )
            assert delta == int(i < k - 1 and (j < i or j == k))
            rows.append({"i": i + 1, "query": f"A{j + 1}" if j < k else "D", "delta": str(delta)})
            total += delta

    welfare = len(set().union(*group, last))
    opt = len(set().union(*comparison))
    beta = Fraction(8 * k * k + 11 * k + 4, 4 * (k + 1) ** 2)
    coefficient = Fraction(2 * k + 1, 2 * (k + 1) ** 2)
    budget = (2 - beta) * welfare / coefficient
    assert total == k * (k - 1) // 2 and opt <= beta * welfare + coefficient * total
    assert (total > budget) == (k >= 7)
    assert saved == {
        "k": k, "m": k + 1, "W": welfare, "OPT": opt, "delta_total": str(total),
        "sufficient_budget": str(budget), "budget_violated": total > budget, "queries": rows,
    }
    return len(rows), terminal_comparisons


def main():
    root = Path(__file__).resolve().parent
    terminal = json.loads((root / "audit_terminal_responder_exchange.json").read_text())
    defect = json.loads((root / "audit_response_defect.json").read_text())
    assert terminal["scope"] == (
        "16 exact customer membership identities; 100 exact coefficient checks; "
        "general claim relies on symbolic proof"
    )
    assert defect["scope"] == (
        "exact finite formula audit; arbitrary-k complete-SPE existence relies on written symbolic gluing"
    )
    verify_exchange(terminal, defect)
    counts = [verify_family_case(k, case) for k, case in zip(range(2, 21), defect["family_cases"], strict=True)]
    print(json.dumps({
        "membership_rows": len(terminal["membership_rows"]),
        "convex_checks": len(terminal["convex_checks"]),
        "identity_rows": defect["identity_rows"],
        "family_cases": len(counts),
        "query_rows": sum(rows for rows, _ in counts),
        "query_terminal_actions_compared_including_selected": sum(checks for _, checks in counts),
    }))


if __name__ == "__main__":
    main()
