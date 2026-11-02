"""Independent exact checks of the degree-two family's analytic mechanism.

Expands unit clients, enumerates all ordered distinct-prefix histories, and
uses the analytic duplicate upper bound instead of author/canonical BI code.
Static theta is checked over multisets, not ordered competitor prefixes.
"""

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations
from math import comb
from pathlib import Path
import json


def audit(q, inner, cross):
    assert q >= 2 and 0 <= inner <= cross and cross >= 1
    p, m = 2*q, q+1
    clients = []
    for left, right in combinations(range(p), 2):
        multiplicity = inner if left//q == right//q else cross
        clients.extend([frozenset((left, right))] * multiplicity)
    topics = [frozenset(i for i, c in enumerate(clients) if v in c)
              for v in range(p)]
    assert all(not topics[v] <= topics[w] for v in range(p)
               for w in range(p) if v != w)

    @lru_cache(None)
    def utilities(terminal_counts):
        return tuple(sum((F(1, sum(terminal_counts[w] for w in c))
                          for c in clients if v in c), F())
                     if terminal_counts[v] else F() for v in range(p))

    def count(path):
        return tuple(path.count(v) for v in range(p))

    def value(path, actor):
        return utilities(count(path))[path[actor]]

    def choice(history):
        assert len(set(history)) == len(history)
        if not history:
            return 0
        if len(history) == 1:
            group = 1-history[0]//q
        else:
            totals = [sum(v//q == group for v in history) for group in range(2)]
            # Important review correction: use the most recent group's tie.
            group = history[-1]//q if totals[0] == totals[1] else totals.index(max(totals))
            if totals[group] == q:
                group = 1-group
        return next(v for v in range(group*q, (group+1)*q) if v not in history)

    def distinct_replay(history):
        while len(history) < m:
            history += (choice(history),)
        return history

    S = q*cross+(q-1)*inner
    L = F(q*cross, 2)+(q-1)*inner
    H = F((2*q-1)*cross+(q-1)*inner, 2)
    fresh_comparisons = 0
    distinct_nodes = 0
    for depth in range(m):
        for history in permutations(range(p), depth):
            distinct_nodes += 1
            selected = distinct_replay(history)
            actual = value(selected, depth)
            assert actual >= F(S, 2)  # bounds every repeated-action branch
            for alternative in range(p):
                if alternative not in history:
                    alternative_terminal = distinct_replay(history+(alternative,))
                    assert actual >= value(alternative_terminal, depth), (q, inner, cross, history, alternative)
                    fresh_comparisons += 1

    actual = distinct_replay(())
    root_paths = [distinct_replay((v,)) for v in range(p)]
    for v, terminal in enumerate(root_paths):
        assert terminal[0] == v
        assert set(terminal[1:]) == {w for w in range(p) if w//q != v//q}
        assert value(terminal, 0) == L
        assert all(value(terminal, j) == H for j in range(1, m))

    theta = None
    static_combinations = 0
    for prefix in combinations_with_replacement(range(p), q):
        response = max(value(prefix+(v,), q) for v in range(p))
        theta = response if theta is None else min(theta, response)
        static_combinations += 1
    assert theta == L

    covered = lambda path: {i for i, client in enumerate(clients)
                            if client.intersection(path)}
    welfare = len(covered(actual))
    optimum = max(len(covered(support)) for support in combinations(range(p), m))
    expected_welfare = q*q*cross+inner*(q-1)*(q+2)//2
    assert welfare == optimum == expected_welfare
    comparison = tuple(range(q))+(q,)
    D = covered(comparison)-covered(actual)
    G = covered(actual)-covered(comparison)
    assert len(D) == len(G) == inner*comb(q-1, 2)
    assert all(len(clients[x]) == 2 for x in D | G)

    coefficients = []
    for client in clients:
        coefficient = F()
        for v, terminal in enumerate(root_paths):
            I = int(v in client)
            K = sum(w in client for w in terminal[1:])
            if I+K:
                coefficient += F(q*I-K, p*q*(I+K))
        endpoint = sorted(client)
        expected = F(1, 2*q) if endpoint[0]//q == endpoint[1]//q else -F(q-1, 2*q*q)
        assert coefficient == expected
        coefficients.append(coefficient)
    flux = sum(coefficients, F())
    assert flux == L-H == -F((q-1)*(cross-inner), 2)
    return {"q": q, "a": inner, "b": cross, "unit_clients": len(clients),
            "distinct_ordered_nodes": distinct_nodes,
            "fresh_action_comparisons": fresh_comparisons,
            "theta_multisets": static_combinations,
            "theta": str(theta), "root_L": str(L), "tail_H": str(H),
            "stationary_flux": str(flux), "W": welfare, "OPT": optimum,
            "shared_D": len(D), "shared_G": len(G)}


def main():
    rows = [audit(*parameters) for parameters in
            [(2, 0, 1), (3, 0, 1), (4, 0, 1),
             (2, 1, 2), (3, 1, 2), (4, 1, 2), (3, 1, 1)]]
    report = {"status": "independent exact checks passed with most-recent-group tie rule",
              "cases": rows,
              "total_distinct_ordered_nodes": sum(row["distinct_ordered_nodes"] for row in rows),
              "total_fresh_action_comparisons": sum(row["fresh_action_comparisons"] for row in rows),
              "scope": "Full SPE existence follows analytically from fresh comparisons, duplicate S/2 bound, and finite BI on repeated-prefix subtrees."}
    path = Path(__file__).with_name("degree_two_independent_exact.json")
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
    print(json.dumps({"status": report["status"], "output": str(path),
                      "distinct_nodes": report["total_distinct_ordered_nodes"],
                      "fresh_comparisons": report["total_fresh_action_comparisons"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
