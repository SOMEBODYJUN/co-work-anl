"""Exhaust the abstract coverage-type prefixes of lengths 0 through 3.

Aliases of a coverage share a type solely for this combinatorial classification;
no continuation strategies are identified. A label with empty coverage has type E.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path

symbols = tuple("T" + str(i) for i in range(6)) + tuple("B" + str(i) for i in range(5)) + ("E",)
totals = Counter()
by_length = {}
for p in range(4):
    rows = Counter()
    for h in product(symbols, repeat=p):
        a = len({x for x in h if x.startswith("T")})
        s = 6 - a
        bs = [x for x in h if x.startswith("B")]
        M, d = len(bs), len(set(bs))
        if M == d:
            if s >= 5:
                case = "paid:no-extra-repeat-and-s>=5"
            elif s == 3:
                assert p == 3 and a == 3 and M == 0
                case = "paid:three-distinct-anchors"
            elif s == 4:
                if p == 2:
                    assert M == 0 and len(set(h)) == 2
                    case = "A"
                elif p == 3 and M == 1:
                    assert a == 2
                    case = "B"
                else:
                    assert p == 3 and M == 0 and a == 2
                    case = "paid:two-anchors-and-empty-or-anchor-repeat"
            else:
                raise AssertionError(h)
        elif s == 6:
            assert M <= 3 and d >= 1
            case = "paid:extra-repeat-and-s=6"
        elif s == 5:
            assert p == 3 and a == 1 and M == 2 and d == 1
            case = "C"
        else:
            raise AssertionError(h)
        rows[case] += 1
    by_length[p] = dict(rows)
    totals.update(rows)
result = {"symbols": symbols, "checked_prefixes": sum(totals.values()),
          "by_length": by_length, "totals": dict(totals),
          "scope": "Finite exhaustion of abstract equality/anchor/empty types; analytic proof supplies all coverage geometries and arbitrary ordered-label continuations"}
Path(__file__).with_name("prefix-types-results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
