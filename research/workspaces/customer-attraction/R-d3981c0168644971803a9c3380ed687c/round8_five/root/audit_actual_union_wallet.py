"""Independent pointwise reconstruction of the five-player actual-union wallet.

No author code, game solver, LP, or numerical library is imported.  This proves
the finite coefficient identity, whose SPE semantics are stated in the review.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def main():
    weights = (F(5, 4), F(19, 9), F(11, 3), F(4))
    records = []
    for bits in product((0, 1), repeat=6):
        actual, query = bits[:5], bits[5]
        total = sum(actual)
        utilities = tuple(F(a, total) if total else F(0) for a in actual)
        rows = tuple(utilities[i] - F(query, sum(actual[:i]) + 5 - i)
                     for i in range(1, 5))
        # Strong version: the comparison theme need not contain / dominate A1.
        target = 4 * bool(total) - 5 * utilities[0] - 4 * query + actual[0]
        residue = target - sum(w * row for w, row in zip(weights, rows))
        assert residue >= 0, (bits, residue)
        # Adding |C|-|A1| gives the maximum-theme projection.
        projected = 4 * bool(total) - 5 * utilities[0] - 3 * query
        assert projected == target + query - actual[0]
        records.append({"actual": list(actual), "query": query,
                        "residue": str(residue)})
    out = {"status": "PASS", "scope": "all 64 coefficient states, arbitrary legal C",
           "weights": list(map(str, weights)), "states": records,
           "zero_residues": sum(r["residue"] == "0" for r in records),
           "disclaimer": "SPE semantics and catalogue legitimacy require the accompanying proof; no target HALF(5) proof."}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": out["status"], "states": len(records),
                      "zero_residues": out["zero_residues"]}))


if __name__ == "__main__":
    main()
