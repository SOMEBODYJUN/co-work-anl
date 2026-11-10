"""Fresh six-type Fraction check; no solver, scan, or repository mutation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

LABELS = tuple("ABCDQ")
ACTUAL = tuple("ABCD")
TYPES = {"Q": 18, "D": 18, "C": 9, "BC": 3, "AB": 5, "ABC": 6}


def profit(action, choices):
    return sum((F(w, sum(a in bits for a in choices))
                for bits, w in TYPES.items() if action in bits), F(0))


def remaining(prefix, choices):
    result = F(0)
    for bits, w in TYPES.items():
        old = sum(a in bits for a in prefix)
        new = sum(a in bits for a in choices)
        if new:
            result += F(w * new, old + new)
    return result


def f(prefix, action):
    return sum((F(w, 1 + sum(a in bits for a in prefix))
                for bits, w in TYPES.items() if action in bits), F(0))


def g(prefix, first, second):
    return sum((F(w, (1 + sum(a in bits for a in prefix)) *
                       (2 + sum(a in bits for a in prefix)))
                for bits, w in TYPES.items() if first in bits and second in bits), F(0))


payoffs = [profit(a, ACTUAL) for a in ACTUAL]
W = remaining((), ACTUAL)
safe = {}
for index in range(4):
    for action in LABELS:
        floor = sum((F(w, 4 - index + sum(a in bits for a in ACTUAL[:index]))
                     for bits, w in TYPES.items() if action in bits), F(0))
        safe[f"{index + 1}:{action}"] = payoffs[index] - floor

tail_prefix = tuple("AB")
tax = {}
for first, second in product(LABELS, repeat=2):
    tax[first + second] = (payoffs[2] + payoffs[3] + g(tail_prefix, "C", "C")
                           - f(tail_prefix, first) - f(tail_prefix, second)
                           + g(tail_prefix, first, second))

V3 = remaining(("A",), tuple("BCD"))
three_rows = {"".join(c): F(5, 3) * V3 - remaining(("A",), c)
              for c in product(LABELS, repeat=3)}
four_rows = {"".join(c): F(1499, 750) * W - remaining((), c)
             for c in product(LABELS, repeat=4)}

prices = {}
for action in LABELS:
    prices[action] = sum((F(4 * w, 4 + 3 * sum(a in bits for a in ACTUAL))
                          for bits, w in TYPES.items() if action in bits), F(0))
background = sum((F(3 * sum(a in bits for a in ACTUAL) * w,
                    4 + 3 * sum(a in bits for a in ACTUAL))
                  for bits, w in TYPES.items()), F(0))
J = 4 * max(prices.values()) + background

off_prefix = tuple("ABQ")
off_payoffs = {a: profit(a, off_prefix + (a,)) for a in LABELS}
max_off = max(off_payoffs.values())
best_replies = [a for a in LABELS if off_payoffs[a] == max_off]
H = "D"
deviation_choices = tuple("ABQ") + (H,)
current_IC = payoffs[2] - profit("Q", deviation_choices)
off_reply_IC = profit(H, deviation_choices) - profit("D", tuple("ABQD"))
actual_reply_IC = payoffs[3] - profit(H, ACTUAL)
discarded_tax = g(tail_prefix, "C", "C") - g(tail_prefix, "C", H)

assert payoffs == [F(9, 2), F(6), F(25, 2), F(18)]
assert W == 41
assert min(safe.values()) == 0 and len(safe) == 20
assert min(tax.values()) == 0 and len(tax) == 25
assert min(three_rows.values()) == F(59, 6)
assert min(four_rows.values()) == F(17209, 750)
assert prices["Q"] == 18 and max(prices.values()) == 18
assert background == F(9339, 455)
assert J - 2 * W == F(4789, 455)
assert list(off_payoffs.values()) == [F(11, 3), F(31, 6), F(25, 2), F(18), F(9)]
assert best_replies == ["D"]
assert current_IC == F(-11, 2)
assert (off_reply_IC, actual_reply_IC, discarded_tax) == (0, 0, F(11, 2))
assert tax["QD"] == current_IC + off_reply_IC + actual_reply_IC + discarded_tax == 0


def encoded(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encoded(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [encoded(item) for item in value]
    return value


def summary(rows):
    least = min(rows.values())
    return {"number": len(rows), "min_slack": least,
            "minimizers": [label for label, value in rows.items() if value == least]}


result = {
    "scope": "six positive customer types, 20 safety rows, 25 one-sided tax rows, 125/625 comparison tuples; no SPE search",
    "types": TYPES,
    "actual_payoffs": payoffs,
    "W": W,
    "safe_rows": safe,
    "single_sided_tax_rows": tax,
    "background_three_profit": {"actual_tail_profit": V3, **summary(three_rows)},
    "background_four_profit": summary(four_rows),
    "prices_at_L0": prices,
    "T_at_L0": background,
    "J_at_L0": J,
    "J_minus_2W": J - 2 * W,
    "off_prefix": "ABQ",
    "last_position_payoffs": off_payoffs,
    "unique_last_best_reply": best_replies,
    "missing_current_IC_slack": current_IC,
    "E_QD_decomposition": {
        "current_IC": current_IC,
        "off_last_compares_D": off_reply_IC,
        "actual_last_compares_off_reply": actual_reply_IC,
        "discarded_tax_residual": discarded_tax,
        "E_QD": tax["QD"],
    },
}
destination = Path(__file__).with_name("exact-check.json")
destination.write_text(json.dumps(encoded(result), ensure_ascii=False, indent=2) + "\n")
print(json.dumps(encoded({key: result[key] for key in (
    "W", "actual_payoffs", "background_three_profit", "background_four_profit",
    "T_at_L0", "J_at_L0", "J_minus_2W", "last_position_payoffs",
    "E_QD_decomposition")}), ensure_ascii=False, indent=2))
