#!/usr/bin/env python3
"""Exact unit-client audit of the copy-tax naive-induction boundary."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


themes = range(3)
clients = [(1,), (1, 2), (1, 2), (0,), (0,), (0, 2)]
strategy = {
    (): 0,
    (0,): 0, (1,): 1, (2,): 0,
    (0, 0): 1, (0, 1): 1, (0, 2): 1,
    (1, 0): 0, (1, 1): 0, (1, 2): 0,
    (2, 0): 1, (2, 1): 0, (2, 2): 0,
}


def finish(prefix):
    z = tuple(prefix)
    while len(z) < 3:
        z += (strategy[z],)
    return z


def payoff(terminal, player):
    a = terminal[player]
    ans = F(0)
    for interest in clients:
        if a in interest:
            ans += F(1, sum(int(s in interest) for s in terminal))
    return ans


def welfare(terminal):
    return sum(any(s in interest for s in terminal) for interest in clients)


def copy_tax(terminal, start=0):
    ans = F(0)
    for i in range(start, 3):
        remaining = 3 - i
        for interest in clients:
            if terminal[i] not in interest:
                continue
            past = sum(int(terminal[j] in interest) for j in range(i))
            ans += F(1, past + 1) - F(1, past + remaining)
    return ans


def harmonic(k):
    return sum((F(1, j) for j in range(1, k + 1)), F(0))


comparisons = 0
minimum_slack = None
for history, prescribed in strategy.items():
    i = len(history)
    actual = finish(history + (prescribed,))
    for a in themes:
        deviation = finish(history + (a,))
        slack = payoff(actual, i) - payoff(deviation, i)
        assert slack >= 0, (history, prescribed, a, slack)
        comparisons += 1
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)

actual = finish(())
off = finish((2,))
assert actual == (0, 0, 1) and off == (2, 0, 1)
actual_budget = F(welfare(actual)) + copy_tax(actual)
off_tail_utility = payoff(off, 1) + payoff(off, 2)
off_demand = F(sum(2 in interest for interest in clients)) + off_tail_utility + copy_tax(off, start=1)
assert actual_budget == F(17, 2)
assert off_demand == F(26, 3)
assert off_demand - actual_budget == F(1, 6)

max_potential = F(0)
argmax_counts = []
for q0 in range(4):
    for q1 in range(4 - q0):
        q2 = 3 - q0 - q1
        terminal = (0,) * q0 + (1,) * q1 + (2,) * q2
        phi = sum(harmonic(sum(int(a in interest) for a in terminal)) for interest in clients)
        if phi > max_potential:
            max_potential, argmax_counts = phi, [(q0, q1, q2)]
        elif phi == max_potential:
            argmax_counts.append((q0, q1, q2))
assert max_potential <= actual_budget

report = {
    "status": "PASS",
    "scope": "complete unit-client SPE; refutes only BRANCH-MONO",
    "decision_histories": len(strategy),
    "action_comparisons": comparisons,
    "minimum_ic_slack": str(minimum_slack),
    "actual_terminal": actual,
    "off_terminal_after_root_2": off,
    "actual_root_payoff": str(payoff(actual, 0)),
    "off_root_payoff": str(payoff(off, 0)),
    "actual_W_plus_C": str(actual_budget),
    "off_branch_demand": str(off_demand),
    "branch_mono_gap": str(off_demand - actual_budget),
    "maximum_three_slot_harmonic_potential": str(max_potential),
    "maximizing_count_vectors": argmax_counts,
    "potential_candidate_slack": str(actual_budget - max_potential),
}
target = Path(__file__).with_name("copy_tax_induction_boundary_audit.json")
target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False))
