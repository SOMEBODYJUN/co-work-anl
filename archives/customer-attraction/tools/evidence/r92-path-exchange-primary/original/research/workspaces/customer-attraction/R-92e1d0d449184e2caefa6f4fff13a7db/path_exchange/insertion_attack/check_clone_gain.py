"""Definition-level exact check of all histories, without the SPE solver."""
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


def check():
    path = Path(__file__).with_name("clone_gain_m4.json")
    obj = json.loads(path.read_text())
    actions = {tuple(row["history"]): row["action"]
               for row in obj["certificate"]["actions"]}
    expected = {h for d in range(4) for h in product(range(2), repeat=d)}
    assert set(actions) == expected

    def follow(h):
        while len(h) < 4:
            h += (actions[h],)
        return h

    def payoff(h, player):
        a = h[player]
        return Fraction((3, 2)[a], h.count(a))

    rows = []
    for h in sorted(expected, key=lambda t: (len(t), t)):
        chosen = follow(h)
        player = len(h)
        p = payoff(chosen, player)
        comparisons = []
        for a in range(2):
            alt = follow(h + (a,))
            q = payoff(alt, player)
            assert p >= q, (h, chosen, alt, p, q)
            comparisons.append(str(q))
        rows.append({"history": h, "prescribed": actions[h],
                     "payoff_if_A_or_B": comparisons})
    actual, clone = follow(()), follow((0, 0))
    assert actual == (0, 1, 0, 0)
    assert clone == (0, 0, 1, 1)
    assert payoff(actual, 0) == 1
    assert payoff(clone, 0) == Fraction(3, 2)
    assert Fraction(3, 2) - 1 == -Fraction(1, 4) + Fraction(3, 4)
    return {"valid": True, "histories": len(expected), "rows": rows,
            "actual": actual, "clone": clone,
            "incumbent_before": "1", "incumbent_after": "3/2"}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
