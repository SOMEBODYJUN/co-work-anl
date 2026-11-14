"""Verify the extra fixed-policy average-cone results over exact rationals."""

import json
from fractions import Fraction
from itertools import combinations, product


LABELS = tuple(range(5))
HISTORIES = tuple(h for depth in range(4) for h in product(LABELS, repeat=depth))
MASKS = tuple(range(1, 32))
NINTH_ACTIONS = (
    "2",
    "00202",
    "0000020022022200002020022",
    "000020002002200220000200002022222000000222202020020200220202022202"
    "22220220222202020020222020200020200022222022000220202222220",
)
NINTH_POINT = {2: 1, 4: 20, 5: 12, 8: 1, 9: 21, 17: 1}
SIXTEENTH_POINT = {1: 11, 5: 5, 6: 13, 12: 11, 20: 12}


def member(mask, action):
    return bool(mask & (1 << action))


def value(column, customers):
    return sum(column[mask - 1] * mass for mask, mass in customers.items())


def coverage(actions):
    return tuple(int(any(member(mask, a) for a in actions)) for mask in MASKS)


def evaluate(actions, J):
    tau = {h: h for h in product(LABELS, repeat=4)}
    for h in reversed(HISTORIES):
        tau[h] = tau[h + (actions[h],)]

    def payoff(mask, a, ending):
        if member(mask, a):
            return Fraction(1, sum(member(mask, b) for b in ending))
        return Fraction(0)

    def row(h, a):
        return tuple(
            payoff(mask, actions[h], tau[h]) - payoff(mask, a, tau[h + (a,)])
            for mask in MASKS
        )

    def mean(h, alternatives):
        return tuple(sum(column) / len(alternatives) for column in zip(
            *(row(h, a) for a in alternatives), strict=True
        ))

    retained = {h: tuple(a for a in J if a not in h)
                for h in HISTORIES if len(set(h)) == len(h) and set(h) <= set(J)}
    full = {h: mean(h, J) for h in HISTORIES}
    filtered = {h: mean(h, alternatives) for h, alternatives in retained.items()}
    individual = {(h, a): row(h, a) for h, alternatives in retained.items() for a in alternatives}
    assert (len(full), len(filtered), len(individual)) == (156, 41, 64)
    return tau, full, filtered, individual


def prove_bound(family, dual_history, weight, ratio, tau, J, customers, expected_coverage):
    w, o = coverage(tau[()]), coverage(J)
    W, O = value(w, customers), value(o, customers)
    all_group_coverages = {
        ",".join(map(str, group)): value(coverage(group), customers)
        for group in combinations(LABELS, 4)
    }
    OPT = max(all_group_coverages.values())
    assert (W, O, OPT) == expected_coverage
    assert Fraction(O, W) == ratio and ratio * W == O == sum(customers.values())
    topics = tuple(frozenset(m for m in customers if member(m, a)) for a in LABELS)
    assert all(topics) and len(set(topics)) == 5
    coefficients = family[dual_history]
    residual = tuple(
        ratio * wm - om - weight * rm for wm, om, rm in zip(w, o, coefficients, strict=True)
    )
    assert min(residual) == 0 and all(residual[m - 1] == 0 for m in customers)
    slacks = {h: value(column, customers) for h, column in family.items()}
    assert min(slacks.values()) == slacks[dual_history] == 0
    return {
        "J": J,
        "root_terminal": tau[()],
        "customers": customers,
        "topic_membership_masks": [sorted(s) for s in topics],
        "W": W,
        "O_J": O,
        "OPT4": OPT,
        "all_group_coverages": all_group_coverages,
        "sharp_ratio": str(ratio),
        "dual": {
            "history": dual_history, "weight": weight,
            "columns": [{"mask": mask, "coefficient": str(rm), "residual": str(rho)}
                        for mask, rm, rho in zip(MASKS, coefficients, residual, strict=True)],
        },
        "slack_minima_by_depth": [str(min(v for h, v in slacks.items() if len(h) == d)) for d in range(4)],
        "zero_histories": [h for h, v in slacks.items() if not v],
        "all_retained_slacks": [{"history": h, "slack": str(v)} for h, v in slacks.items()],
    }


def check():
    assert tuple(map(len, NINTH_ACTIONS)) == (1, 5, 25, 125)
    actions9 = dict(zip(HISTORIES, map(int, "".join(NINTH_ACTIONS)), strict=True))
    actions16 = {h: 2 if any(h) else 0 for h in HISTORIES}

    j9 = (1, 2, 3, 4)
    tau9, full9, filtered9, _ = evaluate(actions9, j9)
    assert tau9[()] == (2, 2, 2, 2)
    assert [tau9[(2, 2, 2, a)] for a in j9] == [(2, 2, 2, a) for a in j9]
    result9 = prove_bound(full9, (2, 2, 2), 4, Fraction(7, 4), tau9, j9, NINTH_POINT, (32, 56, 56))
    assert value(filtered9[(1,)], NINTH_POINT) == Fraction(-1, 2)
    result9["filtered_average_separator"] = {"history": [1], "slack": "-1/2"}

    j16 = (0, 1, 3, 4)
    tau16, full16, filtered16, individual16 = evaluate(actions16, j16)
    assert tau16[()] == tau16[(0,)] == (0, 0, 0, 0)
    alternatives = (1, 3, 4)
    assert [tau16[(0, a)] for a in alternatives] == [(0, a, 2, 2) for a in alternatives]
    result16 = prove_bound(
        filtered16, (0,), 9, Fraction(13, 4), tau16, j16, SIXTEENTH_POINT, (16, 52, 52)
    )
    for record in result16["dual"]["columns"]:
        mask = record["mask"]
        a0, c = int(member(mask, 0)), int(member(mask, 2))
        q = sum(member(mask, a) for a in alternatives)
        denominator = a0 + 1 + 2 * c
        average = Fraction(record["coefficient"])
        assert average == Fraction(a0, 4) - Fraction(q, 3 * denominator)
        assert 9 * average == 3 * sum(individual16[(0,), a][mask - 1] for a in alternatives)
        assert Fraction(record["residual"]) == a0 + Fraction(3 * q, denominator) - int(a0 + q > 0)
    individual_negatives = {(h, a): value(row, SIXTEENTH_POINT)
                            for (h, a), row in individual16.items() if value(row, SIXTEENTH_POINT) < 0}
    assert individual_negatives == {((0,), 1): Fraction(-1, 3), ((1,), 0): Fraction(-1, 12)}
    assert value(full16[(0, 0)], SIXTEENTH_POINT) == Fraction(-3, 2)
    assert value(full16[(0, 0, 0)], SIXTEENTH_POINT) == -6
    result16["filtered_individual_separators"] = [
        {"history": h, "action": a, "slack": str(v)} for (h, a), v in individual_negatives.items()
    ]
    result16["full_history_average_separators"] = [
        {"history": [0, 0], "slack": "-3/2"}, {"history": [0, 0, 0], "slack": "-6"},
    ]
    return {"policy_9_full_history_average": result9, "policy_16_filtered_average": result16}


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
