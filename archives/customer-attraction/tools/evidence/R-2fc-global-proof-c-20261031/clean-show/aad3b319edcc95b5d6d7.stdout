"""Boss independent replay of harmonic-potential obstructions.

No policy JSON, game solver, or discoverer's audit implementation is imported.
Prints a fresh report without overwriting the frozen independent report.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json

WEIGHTS = {1: 7, 3: 3, 4: 12, 6: 3, 9: 5, 18: 3,
           19: 6, 22: 1, 30: 5, 32: 15, 56: 18}
CLIENTS = [mask for mask, n in WEIGHTS.items() for _ in range(n)]


def choose(history):
    if not history:
        return 1
    if len(history) == 1:
        return 1 if history[0] == 5 else 5
    return {(0, 5): 4, (2, 5): 4, (3, 5): 1,
            (4, 5): 2, (5, 5): 1}.get(tuple(sorted(history)), 5)


def terminal(history):
    while len(history) < 3:
        history += (choose(history),)
    return history


def utility(history, player):
    return sum((F(1, sum(mask >> a & 1 for a in history))
                for mask in CLIENTS if mask >> history[player] & 1), F())


def welfare(history):
    return sum(any(mask >> a & 1 for a in history) for mask in CLIENTS)


def main():
    slacks = []
    for depth in range(3):
        for history in product(range(6), repeat=depth):
            actual = utility(terminal(history), depth)
            for action in range(6):
                slack = actual - utility(terminal(history + (action,)), depth)
                assert slack >= 0, (history, action, slack)
                slacks.append(slack)
    history = terminal(())
    loads = Counter(sum(mask >> a & 1 for a in history) for mask in CLIENTS)
    harmonic = lambda c: sum((F(1, j) for j in range(1, c + 1)), F())
    phi = sum((n * harmonic(c) for c, n in loads.items()), F())
    psi = sum((n * min(F(2), harmonic(c)) for c, n in loads.items()), F())
    opt = max(welfare(t) for t in product(range(6), repeat=3))
    assert history == (1, 5, 5)
    assert welfare(history) == 54 and opt == 75 and phi == psi == F(141, 2)
    assert len(slacks) == 258 and 2 * welfare(history) - opt == 33
    print(json.dumps({"N": len(CLIENTS), "terminal": history,
                      "payoffs": [str(utility(history, i)) for i in range(3)],
                      "W": welfare(history), "OPT": opt, "Phi": str(phi),
                      "Psi": str(psi), "comparisons_including_self": len(slacks),
                      "nonself_comparisons": len(slacks) // 6 * 5,
                      "minimum_slack": str(min(slacks)), "loads": dict(loads)},
                     indent=2))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--minimized":
        WEIGHTS = {1: 2, 6: 1, 12: 1, 19: 1, 22: 1, 32: 2, 56: 3}
        CLIENTS = [mask for mask, n in WEIGHTS.items() for _ in range(n)]
        slacks = []
        for depth in range(3):
            for history in product(range(6), repeat=depth):
                value = utility(terminal(history), depth)
                for action in range(6):
                    slack = value - utility(terminal(history + (action,)), depth)
                    assert slack >= 0, (history, action, slack)
                    slacks.append(slack)
        history = terminal(())
        loads = Counter(sum(mask >> a & 1 for a in history) for mask in CLIENTS)
        harmonic = lambda c: sum((F(1, j) for j in range(1, c + 1)), F())
        phi = sum((n * harmonic(c) for c, n in loads.items()), F())
        opt = max(welfare(t) for t in product(range(6), repeat=3))
        values = [utility(history, i) for i in range(3)]
        assert len(CLIENTS) == 11 and history == (1, 5, 5)
        assert values == [F(3), F(5, 2), F(5, 2)]
        assert welfare(history) == 8 and opt == 11 and phi == F(21, 2)
        assert phi < opt and 2 * welfare(history) >= opt
        print(json.dumps({"status": "passed", "N": len(CLIENTS),
                          "terminal": history, "payoffs": list(map(str, values)),
                          "W": welfare(history), "OPT": opt, "Phi": str(phi),
                          "comparisons": len(slacks), "min_slack": str(min(slacks)),
                          "loads": dict(loads)}, indent=2))
    else:
        main()
