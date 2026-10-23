#!/usr/bin/env python3
"""Exact arithmetic audit; the universal proof is in the companion note."""
from fractions import Fraction as F
import json
from pathlib import Path


def profit(num, den):
    return F(num, den) if num else F(0)


def terms(b, e, l, d):
    j = F(d + e, b + e + 1) - profit(d, b + d)
    k = profit(e, b + e + l) - F(e, b + e + 1)
    jc = (F(b * e + d * (d - 1), (b + e + 1) * (b + d))
          if b + d else F(e, e + 1))
    kc = F(e, (b + e) * (b + e + 1)) if e and not l else F(0)
    assert j == jc and k == kc and j >= 0 and k >= 0
    # The local identity before imposing the terminal BR sum.
    p = profit(e + l, b + e + l)
    v = F(l, b + e + 1)
    assert p - v - profit(d, b + d) == -F(d, b + e + 1) + k + j
    return k, j


checks = 0
for b in range(13):
    for e in range(13):
        for l in (0, 1):
            for d in range(13):
                terms(b, e, l, d)
                checks += 1

customers = [({0}, 30), ({1}, 7), ({2}, 5), ({3}, 7), ({2, 4}, 2),
             ({2, 5}, 2), ({1, 4, 5}, 6), ({2, 4, 5}, 4), ({3, 4, 5}, 6)]
actual = (0, 0, 0, 5)
compare = (0, 1, 2, 3)
pay = []
for a in actual:
    pay.append(sum((F(w, sum(t in s for t in actual))
                    for s, w in customers if a in s), F(0)))
p = sum(pay, F(0)); v = pay[-1]
terminal = [sum((F(w, 1 + sum(t in s for t in actual[:-1]))
                 for s, w in customers if a in s), F(0)) for a in range(6)]
assert terminal[actual[-1]] == max(terminal)
L = sum((v - terminal[a] for a in compare), F(0))
K = J = R = F(0)
for s, w in customers:
    e = sum(a in s for a in actual[:-1]); l = int(actual[-1] in s)
    d = sum(a in s for a in compare)
    k, j = terms(0, e, l, d)
    K += w * k; J += w * j; R += w * profit(d, d)
assert (p, v, R, L, K, J) == (48, 18, 69, F(51, 2), F(15, 2), 0)
assert p + 3 * v - R == L + K + J == 33
result = {
    "universal_proof": "companion note; finite checks do not prove generality",
    "local_identity_exact_checks": checks,
    "existing_69_customer_scalar_example": {
        "actual": actual, "comparison": compare,
        "payoffs": list(map(str, pay)), "P": str(p), "v": str(v),
        "comparison_profit": str(R), "terminal_action_values": list(map(str, terminal)),
        "L": str(L), "K": str(K), "J": str(J), "total_remainder": str(L + K + J),
        "full_SPE_reaudit": False,
    },
}
print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == "__main__" and len(__import__('sys').argv) > 1:
    Path(__import__('sys').argv[1]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
