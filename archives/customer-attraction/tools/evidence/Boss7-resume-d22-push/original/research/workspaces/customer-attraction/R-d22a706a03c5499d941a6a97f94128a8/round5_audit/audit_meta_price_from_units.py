"""Independent definition-level check; no repository or discovery imports.

All clients are separate unit clients and all arithmetic is rational.
The finite run checks the analytic arbitrary-(m,r,L) proof, not its converse.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def action(history, m):
    return "B" if len(history) == m - 1 and all(a == "A" for a in history) else "A"


def finish(history, m):
    history = tuple(history)
    while len(history) < m:
        history += (action(history, m),)
    return history


def client_topics(m, L):
    return [frozenset("A") for _ in range(m * L)] + [frozenset("B") for _ in range(L)]


def own_pay(terminal, player, clients):
    return sum((F(1, sum(a in topic for a in terminal))
                for topic in clients if terminal[player] in topic), F(0))


def extra_pay(query, prefix, terminal, clients):
    # The additional query contributes the explicit +1 in every used denominator.
    return sum((F(1, 1 + sum(a in topic for a in prefix + terminal))
                for topic in clients if query in topic), F(0))


def encoded(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encoded(v) for v in value]
    return value


def audit(m, L):
    clients = client_topics(m, L)
    node_count, comparison_count, minimum = 0, 0, None
    for i in range(m):
        for h in product("AB", repeat=i):
            node_count += 1
            actual = finish(h, m)
            actual_pay = own_pay(actual, i, clients)
            for alternate in "AB":
                terminal = finish(h + (alternate,), m)
                margin = actual_pay - own_pay(terminal, i, clients)
                assert margin >= 0, (m, L, h, alternate, margin)
                comparison_count += 1
                minimum = margin if minimum is None else min(minimum, margin)
    assert node_count == 2**m - 1
    real = finish((), m)
    assert real == ("A",) * (m - 1) + ("B",)
    covered = sum(any(a in t for a in real) for t in clients)
    assert covered == len(clients) == (m + 1) * L

    residuals = []
    for r in range(2, m + 1):
        prefix = ("A",) * (m - r)
        columns = {a: finish(prefix + (a,), m)[len(prefix):] for a in "AB"}
        K = {a: {b: extra_pay(a, prefix, columns[b], clients) for b in "AB"}
             for a in "AB"}
        assert K == {"A": {"A": F(L), "B": F(L)},
                     "B": {"A": F(L, 2), "B": F(L, 2)}}
        d = {a: own_pay(prefix + columns[a], len(prefix), clients) for a in "AB"}
        assert d == {"A": F(m * L, m - 1), "B": F(L)}
        C = K["A"]["A"]
        D = d["A"]
        v_full = sum((K[a]["A"] for a in columns["A"]), F(0)) / r
        v_tail = sum((K[a]["A"] for a in columns["A"][1:]), F(0)) / (r - 1)
        assert v_full == F(L) * (1 - F(1, 2 * r))
        assert v_tail == F(L) * (1 - F(1, 2 * (r - 1)))
        assert (D - C) / (C - v_full) == F(2 * r, m - 1)
        assert (D - C) / (C - v_tail) == F(2 * (r - 1), m - 1)
        assert K["A"]["A"] > K["B"]["A"]  # strict meta-Nash
        assert max(K[a][b] for a in "AB" for b in "AB") < d["A"]
        residuals.append({"r": r, "prefix_A_count": m - r,
                          "D": D, "C": C, "v_full": v_full, "v_tail": v_tail,
                          "full_price_ratio": (D - C) / (C - v_full),
                          "tail_price_ratio": (D - C) / (C - v_tail),
                          "full_alpha1_margin": D + v_full - 2 * C,
                          "tail_alpha1_margin": D + v_tail - 2 * C})
    return {"m": m, "L": L, "unit_clients": len(clients),
            "all_ordered_nodes": node_count,
            "comparisons_including_same_action": comparison_count,
            "minimum_SPE_margin": minimum,
            "W_equals_OPT": covered, "residual_checks": residuals}


if __name__ == "__main__":
    results = [audit(m, L) for m in range(2, 10) for L in (1, 2)]
    output = {"status": "pass", "definition": "separate unit clients; exact Fraction arithmetic",
              "scope": "finite checks of an independently proved all-m,r,L family",
              "cases": results,
              "total_ordered_nodes": sum(x["all_ordered_nodes"] for x in results),
              "total_comparisons_including_same_action": sum(
                  x["comparisons_including_same_action"] for x in results)}
    path = Path(__file__).with_name("meta_price_unit_audit.json")
    path.write_text(json.dumps(encoded(output), indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("status", "total_ordered_nodes",
                                           "total_comparisons_including_same_action")}))
