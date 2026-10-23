"""Independent exact audit: no solver or author's proof imported."""
from fractions import Fraction as F
from itertools import product
import json

LABELS = "ABC"
TYPES = [("A", 1), ("AB", 1), ("BC", 3), ("ABC", 2)]
CUSTOMERS = tuple(frozenset(labels) for labels, count in TYPES for _ in range(count))

def utilities(path):
    return tuple(sum((F(1, sum(a in x for a in path))
                      for x in CUSTOMERS if chosen in x), F())
                 for chosen in path)

def action(history):
    if not history:
        return "C"
    if len(history) == 1:
        return {"A": "B", "B": "B", "C": "C"}[history[0]]
    return "A" if history == ("C", "C") else "B"

def continuation(history):
    history = tuple(history)
    while len(history) < 3:
        history += (action(history),)
    return history

node_rows = []
for depth in range(3):
    for history in product(LABELS, repeat=depth):
        payoffs = {a: utilities(continuation(history + (a,)))[depth]
                   for a in LABELS}
        assert payoffs[action(history)] == max(payoffs.values()), (history, payoffs)
        node_rows.append({"history": "".join(history), "chosen": action(history),
                          "deviation_payoffs": {a: str(v) for a, v in payoffs.items()}})

def rent(query, response_to):
    suffix = continuation((response_to,))[1:]
    return sum((F(1, 1 + sum(a in x for a in suffix))
                for x in CUSTOMERS if query in x), F())

rents = {q: {s: str(rent(q, s)) for s in LABELS} for q in LABELS}
diagonal = rent("B", "B") + rent("C", "C")
cross = rent("B", "C") + rent("C", "B")
assert diagonal == F(25, 6) < F(26, 6) == cross
actual = continuation(())
assert actual == ("C", "C", "A")
assert sum(utilities(actual)) == 7
assert sum(any(a in x for a in actual) for x in CUSTOMERS) == 7

print(json.dumps({"customers": len(CUSTOMERS), "nodes": node_rows,
                  "rents": rents, "diagonal": str(diagonal), "cross": str(cross),
                  "actual": "".join(actual),
                  "actual_payoffs": list(map(str, utilities(actual))),
                  "actual_welfare": 7}, indent=2))
