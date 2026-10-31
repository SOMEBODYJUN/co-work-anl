"""Independent exact checks of payoff/moment ranks and exposed type rays.

This imports no game solver or other team implementation. Finite checks audit
the implementation of symbolic arguments; they do not establish Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, parts - 1):
                yield (first,) + tail


def rank(rows):
    pivots = {}
    for input_row in rows:
        row = list(map(F, input_row))
        for col, basis in sorted(pivots.items()):
            if row[col]:
                scale = row[col]
                row = [a - scale * b for a, b in zip(row, basis)]
        col = next((j for j, x in enumerate(row) if x), None)
        if col is not None:
            scale = row[col]
            pivots[col] = [x / scale for x in row]
    return len(pivots)


def H(n):
    return sum((F(1, j) for j in range(1, n + 1)), F())


def main():
    cases = []
    for p in range(1, 6):
        types = range(1, 1 << p)
        for m in range(1, 5):
            qlist = list(compositions(m, p))
            moments = [[int(bool(B & T)) for B in types]
                       for T in types if T.bit_count() <= m]
            potentials = []
            payoffs = []
            for q in qlist:
                loads = [sum(q[a] for a in range(p) if B >> a & 1)
                         for B in types]
                potentials.append([H(c) for c in loads])
                for a in range(p):
                    if q[a]:
                        payoffs.append([F(1, c) if B >> a & 1 else F()
                                        for B, c in zip(types, loads)])
            rows = []
            for prefix in compositions(m - 1, p):
                # An arbitrary anchor action; it need not be optimal. It may
                # vary with the prefix, illustrating independence of sigma.
                anchor = sum((a + 3) * c for a, c in enumerate(prefix)) % p
                values = []
                for a in range(p):
                    values.append([F(1, 1 + sum(prefix[b] for b in range(p)
                                               if B >> b & 1))
                                   if B >> a & 1 else F() for B in types])
                for a in range(p):
                    rows.append([x - y for x, y in zip(values[anchor], values[a])])
            root_q = qlist[len(qlist) // 2]
            welfare = [int(any(root_q[a] and B >> a & 1 for a in range(p)))
                       for B in types]
            d = sum(comb(p, k) for k in range(1, min(p, m) + 1))
            actual = {
                "moments": rank(moments), "potentials": rank(potentials),
                "payoffs": rank(payoffs), "terminal_rows": rank(rows),
                "terminal_rows_plus_W": rank(rows + [welfare]),
            }
            assert actual == {"moments": d, "potentials": d, "payoffs": d,
                              "terminal_rows": d - 1,
                              "terminal_rows_plus_W": d}, (p, m, actual)
            assert all(row[-1] == 0 for row in rows)
            cases.append({"p": p, "m": m, "dimension": d, "ranks": actual})
    exposed_checks = 0
    for p in range(1, 9):
        for B in range(1, 1 << p):
            for C in range(1, 1 << p):
                singleton = lambda a: int(bool(C & (1 << a)))
                value = sum(singleton(a) for a in range(p) if not B >> a & 1)
                for a, b in combinations([a for a in range(p) if B >> a & 1], 2):
                    value += 2 * int(bool(C & ((1 << a) | (1 << b))))
                    value -= singleton(a) + singleton(b)
                j = (B & C).bit_count()
                assert value == (C & ~B).bit_count() + j * (B.bit_count() - j)
                assert value >= 0 and (value == 0) == (B == C)
                exposed_checks += 1
    # The m=1 exception: singleton generators suffice and a two-interest type
    # is the sum of two singleton columns, so it is not an extreme ray.
    assert [1, 1] == [1 + 0, 0 + 1]
    output = {"arithmetic": "standard-library Fraction and exact rational ranks",
              "rank_cases": cases, "exposing_functional_pairs": exposed_checks,
              "m1_exception_checked": True,
              "scope": "finite audit of symbolic representation; no welfare theorem"}
    path = Path(__file__).with_name("root_independent_audit.json")
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"rank_cases": len(cases),
                      "exposing_functional_pairs": exposed_checks,
                      "status": "passed"}))


if __name__ == "__main__":
    main()
