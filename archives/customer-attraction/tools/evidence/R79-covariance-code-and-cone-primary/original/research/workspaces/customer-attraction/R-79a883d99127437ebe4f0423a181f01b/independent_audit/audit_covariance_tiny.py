"""Independent definition-level audit; imports no peer or canonical solver."""
from fractions import Fraction as F
from itertools import product
import json

TOPICS = ("A", "B", "D", "E")
SETS = {"A": frozenset("xz"), "B": frozenset("y"),
        "D": frozenset("xy"), "E": frozenset("zw")}
REPLY = {"A": "D", "B": "E", "D": "E", "E": "D"}
P = {"A": F(1, 2), "B": F(1, 2)}


def utility(path, player):
    return sum((F(1, sum(x in SETS[a] for a in path))
                for x in SETS[path[player]]), F())


def continuation(history):
    if not history:
        history = ("D",)
    if len(history) == 1:
        history += (REPLY[history[0]],)
    return history


def main():
    comparisons = 0
    tables = {}
    for depth in range(2):
        for h in product(TOPICS, repeat=depth):
            path = continuation(h)
            prescribed = utility(path, depth)
            alternatives = [utility(continuation(h + (a,)), depth) for a in TOPICS]
            assert all(prescribed >= value for value in alternatives)
            comparisons += len(alternatives)
            tables["root" if not h else h[0]] = [str(v) for v in alternatives]
    assert comparisons == 20
    rows = {}
    for x in "xyzw":
        q = sum((prob for a, prob in P.items() if x in SETS[a]), F())
        d = c = F()
        conditional = {0: F(), 1: F()}
        for a, prob in P.items():
            path = continuation((a,))
            indicator = int(x in SETS[a])
            load = sum(x in SETS[t] for t in path)
            h = load - indicator
            d += prob * indicator / (h + 1)
            c += prob * q / (1 + load)
            conditional[indicator] += prob / (h + 1)
        h0 = conditional[0] / (1-q) if q != 1 else None
        h1 = conditional[1] / q if q else None
        rows[x] = {"q": str(q), "D": str(d), "C": str(c),
                   "C_minus_D": str(c-d),
                   "H0": None if h0 is None else str(h0),
                   "H1": None if h1 is None else str(h1)}
    assert rows["x"] == {"q": "1/2", "D": "1/4", "C": "1/3",
                          "C_minus_D": "1/12", "H0": "1", "H1": "1/2"}
    total_d = sum((F(row["D"]) for row in rows.values()), F())
    total_c = sum((F(row["C"]) for row in rows.values()), F())
    assert total_d == F(5, 4) and total_c == F(5, 6)
    assert total_d-total_c == F(5, 12)
    actual = continuation(())
    welfare = len(set().union(*(SETS[a] for a in actual)))
    assert actual == ("D", "E") and welfare == 4
    root = utility(actual, 0)
    assert root == 2
    e = root-total_d
    kappa = total_d-total_c
    assert root-total_c == e+kappa == F(7, 6)
    print(json.dumps({"nodes": 5, "IC_comparisons_including_self": comparisons,
        "alternative_payoff_rows_A_B_D_E": tables,
        "actual_path": actual, "actual_utilities": [str(utility(actual, i)) for i in range(2)],
        "W": welfare, "OPT": 4, "clients": rows,
        "D_total": str(total_d), "C_total": str(total_c),
        "D_minus_C": str(kappa), "node_slack": str(e),
        "u_minus_C": str(root-total_c)}, indent=2))


if __name__ == "__main__":
    main()
