#!/usr/bin/env python3
"""Exact diagnostic for marked real-history clocks, without history merging.

General statements are proved by telescoping in signed_history_exchange.md.
This script independently reconstructs that page's full-history example and
checks branch clocks, signed incidence flow and legitimate terminal grouping.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json


THEMES = {"A": frozenset({0, 1}), "B": frozenset({2, 3}),
          "C": frozenset({4})}
CLIENTS = tuple(range(5))
SIGMA = {(): "B", ("A",): "B", ("B",): "A", ("C",): "A"}
SIGMA.update({tuple(h): a for h, a in {
    "AA": "B", "AB": "A", "AC": "B", "BA": "C", "BB": "A",
    "BC": "A", "CA": "B", "CB": "A", "CC": "A"}.items()})


def counts(path):
    return tuple(sum(x in THEMES[a] for a in path) for x in CLIENTS)


def terminal(history):
    history = tuple(history)
    while len(history) < 3:
        history += (SIGMA[history],)
    return history


def topic_mark(topic):
    return tuple(int(x in THEMES[topic]) for x in CLIENTS)


def rent(mark, load, rho):
    return sum((F(a, rho + b) for a, b in zip(mark, load) if a), F(0))


def real_clock(history, mark, rho):
    path = terminal(history)
    before = counts(history)
    result = F(0)
    for topic in path[len(history):]:
        after = tuple(b + int(x in THEMES[topic])
                      for x, b in zip(CLIENTS, before))
        result += sum((F(a, (rho + b) * (rho + c))
                       for x, a, b, c in zip(CLIENTS, mark, before, after)
                       if a and x in THEMES[topic]), F(0))
        before = after
    return result


def terminal_rent(history, mark, rho):
    return rent(mark, counts(terminal(history)), rho)


def graph_audit(edges, rho):
    d = defaultdict(lambda: [F(0)] * len(CLIENTS))
    direct = F(0)
    for source, target, mark, weight in edges:
        assert counts(source) == counts(target)
        direct += weight * (terminal_rent(target, mark, rho)
                            - terminal_rent(source, mark, rho))
        for x in CLIENTS:
            d[target][x] += weight * mark[x]
            d[source][x] -= weight * mark[x]
    endpoints = sum((terminal_rent(h, mark, rho) for h, mark in d.items()), F(0))
    clock_endpoints = -sum((real_clock(h, mark, rho) for h, mark in d.items()), F(0))
    grouped = defaultdict(lambda: [F(0)] * len(CLIENTS))
    for h, mark in d.items():
        for x in CLIENTS:
            grouped[counts(terminal(h))][x] += mark[x]
    compressed = sum((rent(mark, load, rho) for load, mark in grouped.items()), F(0))
    assert direct == endpoints == clock_endpoints == compressed
    return {
        "direct": str(direct),
        "nonzero_history_incidence": sum(any(mark) for mark in d.values()),
        "nonzero_terminal_incidence": sum(any(mark) for mark in grouped.values()),
    }


def main():
    # Independently check all actual decision nodes before any coalescence.
    comparisons = 0
    for depth in range(3):
        for h in product(THEMES, repeat=depth):
            actual = terminal(h)
            actual_topic = actual[depth]
            actual_value = terminal_rent(actual, topic_mark(actual_topic), 0)
            for action in THEMES:
                branch = terminal(h + (action,))
                deviation_value = terminal_rent(branch, topic_mark(action), 0)
                assert actual_value >= deviation_value, (h, action)
                comparisons += 1
    assert comparisons == 39

    reports = []
    checked_clocks = 0
    for rho in (0, 1, 2):
        for depth in range(1, 4):
            for h in product(THEMES, repeat=depth):
                load = counts(h)
                # All subsets of the actual prefix players as fixed marks.
                for selected in product((0, 1), repeat=depth):
                    mark = tuple(sum(chosen and x in THEMES[topic]
                                     for chosen, topic in zip(selected, h))
                                 for x in CLIENTS)
                    before = rent(mark, load, rho)
                    after = terminal_rent(h, mark, rho)
                    assert before - after == real_clock(h, mark, rho)
                    assert before >= after
                    checked_clocks += 1

        old_group = counts(tuple("BA"))
        actual_clock = real_clock(tuple("BA"), old_group, rho)
        other_clock = real_clock(tuple("AB"), old_group, rho)
        expected = F(2, (rho + 1) * (rho + 2))
        assert actual_clock == 0 and other_clock == expected

        # A coherent marked two-cycle cancels exactly.
        coherent = graph_audit([
            (tuple("BA"), tuple("AB"), old_group, F(3, 2)),
            (tuple("AB"), tuple("BA"), old_group, F(3, 2))], rho)
        assert coherent["direct"] == "0"

        # Scalar conservation fails when the two arrows carry different marks.
        scalar = graph_audit([
            (tuple("BA"), tuple("AB"), topic_mark("A"), F(1)),
            (tuple("AB"), tuple("BA"), topic_mark("B"), F(1))], rho)
        assert F(scalar["direct"]) == -expected

        # Ordered histories stay distinct; terminal coalescence is legitimate.
        terminal_group = graph_audit([
            (tuple("AC"), tuple("CA"), topic_mark("A"), F(1)),
            (tuple("CA"), tuple("AC"), topic_mark("C"), F(1))], rho)
        assert terminal_group["nonzero_history_incidence"] == 2
        assert terminal_group["nonzero_terminal_incidence"] == 0
        assert terminal_group["direct"] == "0"
        reports.append({"reserve": rho, "actual_BA_clock": str(actual_clock),
                        "exchanged_AB_clock": str(other_clock),
                        "coherent_cancellation": coherent,
                        "scalar_balance_failure": scalar,
                        "legitimate_terminal_grouping": terminal_group})
    print(json.dumps({"status": "pass", "spe_comparisons": comparisons,
                      "clock_identity_checks": checked_clocks,
                      "reports": reports}, indent=2))


if __name__ == "__main__":
    main()
