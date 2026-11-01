"""Independent ten-unit-customer full-history StrongA countercheck.

Literal data transcribed from exchange10's statement; no source programs,
model libraries, or solver imports. One explicit auxiliary counterexample.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

names = ("C", "A", "B", "D")
# Six distinct core customers, one private A, one common B/D, two private D.
units = [frozenset((0, 1, 2)) for _ in range(6)]
units += [frozenset((1,)), frozenset((2, 3))]
units += [frozenset((3,)), frozenset((3,))]
second = (0, 1, 2, 1)
terminal = ((3, 2, 1, 1), (2, 2, 2, 2),
            (1, 1, 1, 1), (1, 2, 1, 1))
policy = {(): 0}
policy.update({(a,): second[a] for a in range(4)})
policy.update({(a, b): terminal[a][b] for a, b in product(range(4), repeat=2)})

def finish(h):
    while len(h) < 3:
        h += (policy[h],)
    return h

def pay(profile, i):
    return sum((F(1, sum(a in customer for a in profile))
                for customer in units if profile[i] in customer), F(0))

def cover(profile):
    return sum(bool(set(profile) & customer) for customer in units)

slacks = []
for h, chosen in policy.items():
    i = len(h)
    for a in range(4):
        if a != chosen:
            slacks.append(pay(finish(h), i) - pay(finish(h+(a,)), i))
assert len(policy) == 21 and len(slacks) == 63 and min(slacks) >= 0
actual = finish(())
u = [pay(actual, i) for i in range(3)]
frozen = [[pay(actual[:i]+(a,)+actual[i+1:], i) for a in range(4)]
          for i in range(3)]
M = list(map(max, frozen))
adjacent = []
for j in range(2):
    adjacent.append(sum((F(1, c*(c+1)) for customer in units
                        if actual[j] in customer and actual[j+1] not in customer
                        for c in [sum(a in customer for a in actual)]), F(0)))
W = cover(actual)
OPT = max(map(cover, product(range(4), repeat=3)))
assert actual == (0, 0, 3) and u == [3, 3, 3]
assert M == [4, 4, 3] and adjacent == [0, 1]
assert W == 9 and OPT == 10 and sum(M)-W-sum(adjacent) == 1
report = dict(
    scope="One explicit 10-unit-customer StrongA refutation; HALF not refuted.",
    input_origin="Literal exchange10 statement; independent code/no author imports",
    topic_order=names, customers=[sorted(c) for c in units],
    root=names[policy[()]], second=[names[a] for a in second],
    terminal=[[names[a] for a in row] for row in terminal],
    histories=len(policy), nonself_IC=len(slacks), minimum_IC_slack=str(min(slacks)),
    actual=[names[a] for a in actual], actual_payoffs=list(map(str, u)),
    root_query_payoffs=[str(pay(finish((a,)), 0)) for a in range(4)],
    second_query_payoffs=[[str(pay(finish((a,b)), 1)) for b in range(4)]
                          for a in range(4)],
    terminal_query_payoffs=[[[str(pay((a,b,t), 2)) for t in range(4)]
                             for b in range(4)] for a in range(4)],
    frozen_query_payoffs=[[str(v) for v in row] for row in frozen],
    frozen_maxima=list(map(str, M)), adjacent_Cs=list(map(str, adjacent)),
    W=W, OPT=OPT, StrongA_gap=str(sum(M)-W-sum(adjacent)),
    StrongA_refuted=True, HALF_refuted=False,
    weaker_optimal_assignment_tested=False)
dest = Path(__file__).with_name("compact_strongA_independent.json")
dest.write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({k: report[k] for k in ["histories", "nonself_IC", "actual", "W", "OPT",
                                       "frozen_maxima", "adjacent_Cs", "StrongA_gap"]}, indent=2))
