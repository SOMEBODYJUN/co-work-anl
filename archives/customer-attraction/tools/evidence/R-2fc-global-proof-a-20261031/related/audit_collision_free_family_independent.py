"""Independent ordered-tree audit of the collision-free family, k=1,2,3.

Generation uses type-load formulas; a separate pass expands unit clients.
All unstructured subtrees use backward induction. No game package is used.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def audit(k):
    p, m = 3 * k + 1, k + 1
    b, d = 3 * k, 3 * k + 1
    topics = []
    for i in range(k):
        core = {2 * i, 2 * i + 1}
        topics.extend((core | {2 * k + i}, core | {b}, core))
    topics.append({b, d})

    def formula(path, index):
        q = [path.count(a) for a in range(p)]
        action = path[index]
        bload = q[-1] + sum(q[3 * i + 1] for i in range(k))
        if action == p - 1:
            return F(1, bload) + F(1, q[-1])
        i, kind = divmod(action, 3)
        value = F(2, sum(q[3 * i:3 * i + 3]))
        if kind == 0:
            value += F(1, q[action])
        if kind == 1:
            value += F(1, bload)
        return value

    def prescribed(history):
        if p - 1 in history:
            return None
        groups = [a // 3 for a in history]
        if len(set(groups)) != len(groups):
            return None
        bs = [a // 3 for a in history if a % 3 == 1]
        if len(bs) > 1:
            return None
        fresh = [i for i in range(k) if i not in groups]
        if bs:
            return 3 * fresh[0] if fresh else 3 * bs[0]
        if fresh:
            return 3 * fresh[0] + 2
        opened = [a // 3 for a in history if a % 3 == 0]
        return 3 * opened[-1] + 1 if opened else p - 1

    sigma = {}
    leaves = {}

    def build(history):
        if len(history) == m:
            return history
        children = [build(history + (a,)) for a in range(p)]
        values = [formula(child, len(history)) for child in children]
        selected = prescribed(history)
        if selected is None:
            selected = min(a for a in range(p) if values[a] == max(values))
        assert values[selected] == max(values), (k, history, selected, values)
        sigma[history] = selected
        leaves[history] = children[selected]
        return children[selected]

    actual = build(())
    assert actual == tuple(3 * i + 2 for i in range(k)) + (p - 1,)

    def unit_payoff(path, position):
        return sum((F(1, sum(x in topics[a] for a in path))
                    for x in topics[path[position]]), F())

    def finish(history):
        while len(history) < m:
            history += (sigma[history],)
        return history

    checked = 0
    for depth in range(m):
        for history in product(range(p), repeat=depth):
            terminal = finish(history)
            value = unit_payoff(terminal, depth)
            assert value == formula(terminal, depth)
            for a in range(p):
                alternative = finish(history + (a,))
                assert value >= unit_payoff(alternative, depth), (history, a)
                checked += 1
    loads = [sum(x in topics[a] for a in actual) for x in range(3 * k + 2)]
    assert all(c <= 1 for c in loads)
    assert sum(loads) == 2 * k + 2
    optimum_tuple = tuple(3 * i for i in range(k)) + (p - 1,)
    assert set().union(*(topics[a] for a in optimum_tuple)) == set(range(3 * k + 2))
    assert [unit_payoff(actual, i) for i in range(m)] == [F(2)] * m
    return {"k": k, "m": m, "p": p, "N": 3 * k + 2,
            "actual": actual, "W": 2 * k + 2, "OPT": 3 * k + 2,
            "ratio": str(F(3 * k + 2, 2 * k + 2)),
            "decision_histories": len(sigma), "comparisons_including_self": checked,
            "all_ordered_histories_verified": True, "actual_collision_free": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"identity": "independent finite audit of arbitrary-k symbolic family",
              "cases": [audit(k) for k in range(1, 4)],
              "scope": "finite exact replay; general validity depends on state induction"}
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(payload)
    print(payload)
