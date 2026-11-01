"""Exact definition-level audit; no equilibrium solver or floating point."""
from fractions import Fraction
from itertools import product

TOPICS = {"A": frozenset((1, 2, 3)), "C": frozenset((4,))}
POLICY = {(): "A", ("A",): "A", ("C",): "A"}


def complete(h):
    h = tuple(h)
    while len(h) < 2:
        h += (POLICY[h],)
    return h


def profit(z, i):
    return sum((Fraction(1, sum(x in TOPICS[a] for a in z))
                for x in TOPICS[z[i]]), Fraction())


def welfare(z):
    return len(set().union(*(TOPICS[a] for a in z)))


for depth in range(2):
    for h in product(TOPICS, repeat=depth):
        prescribed = complete(h)
        for a in TOPICS:
            forced = complete(h + (a,))
            assert profit(prescribed, depth) >= profit(forced, depth)
            if a != POLICY[h]:
                assert profit(prescribed, depth) > profit(forced, depth)

actual, forced = complete(("A",)), complete(("A", "C"))
assert actual == ("A", "A") and forced == ("A", "C")
delta_w = welfare(forced) - welfare(actual)
delta_b = profit(forced, 0) - profit(actual, 0)
slack = profit(actual, 1) - profit(forced, 1)
assert delta_w == 1 and delta_b == Fraction(3, 2)
assert delta_w == delta_b - slack
opt = max(welfare(z) for z in product(TOPICS, repeat=2))
assert opt == 4 and 2 * welfare(actual) >= opt
print("PASS: all 3 histories / 6 comparisons; all 3 nontrivial IC strict.")
print(f"Old R1 false: delta W={delta_w}, delta tail=0.")
print(f"Correct C1: {delta_w} = {delta_b} - {slack}; OPT={opt}.")
