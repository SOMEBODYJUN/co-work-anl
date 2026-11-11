"""Exact all-type arithmetic for Main's prefix SAFE/MAX-X analytic family."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

PARAMS = {4: (F(15), F(2, 3), F(1)),
          5: (F(20), F(7, 4), F(3, 5)),
          6: (F(25), F(51, 20), F(3, 8))}
def kernel(r, n, k, x, ys, t, q):
    alpha, s, a = PARAMS[r]
    C = alpha + (r - 2) * s + r
    j, D = sum(ys), n + r - 1
    direct = (alpha * F(x, n + j + t)
              + (s * j + r * t) / D - (C - 1) * x / D
              - q * (F(x, D) + F(1 - x, n))
              - a * F((r - 2) * x - j, n + k)
              - F(t - q, n + x + j))
    # Sum individual member budgets rather than the aggregated count formula.
    split = alpha * F(x, n + sum(ys) + t) - (C - 1) * F(x, D)
    split -= F(q * x, D) + F(q * (1 - x), n)
    for y in ys:
        split += s * F(y, D) - a * F(x - y, n + k)
    split += F(r * t, D) - F(t - q, n + x + sum(ys))
    assert direct == split
    return direct

all_atoms = []
summaries = []
for r, (alpha, s, a) in PARAMS.items():
    C = alpha + (r - 2) * s + r
    assert s / r + a / (r - 1) == F(1, 2)
    assert alpha == 5 * (r - 1)
    vals = []
    for n in range(1, 8 - r):
        d, D = n + r - 2, n + r - 1
        G = d * (s + a * D / n)
        assert G <= alpha - 1 and alpha >= (r - 1) * d
        assert (r - 1) * n * (n + 1) >= 2 * (n + r - 2)
        for k in range(r - 1):
            for bits in product((0, 1), repeat=r + 1):
                x, *ys, t, q = bits
                assert len(ys) == r - 2
                e = kernel(r, n, k, x, ys, t, q)
                corner = kernel(r, n, 0 if x else r - 2, x, ys, t, 0 if x else 1)
                assert e >= corner >= 0
                vals.append(e)
                all_atoms.append({"r": r, "b": n - 1, "k": k, "bits": list(bits),
                                  "remainder": str(e), "corner_remainder": str(corner)})
    summaries.append({"r": r, "actual_player": 7 - r,
                      "alpha": str(alpha), "s_middle": str(s), "a_middle": str(a),
                      "s_terminal": str(r), "a_terminal": "0", "BR_weight": "1",
                      "C": str(C), "old_C": str(F(5 * (r - 1)) + F(r * r, 2)),
                      "types": len(vals), "negative": sum(v < 0 for v in vals),
                      "zero": sum(v == 0 for v in vals), "positive": sum(v > 0 for v in vals),
                      "min_positive": str(min(v for v in vals if v > 0)),
                      "G_endpoints": [str((n + r - 2) * (s + a * (n + r - 1) / n))
                                      for n in (1, 7 - r)]})
assert len(all_atoms) == 1440
here = Path(__file__).resolve()
out = {"status": "PASS_ALL1440_TYPES_PREFIX_SAFE_MAX_X_FAMILY",
       "summaries": summaries, "atoms": all_atoms, "optimizer_calls": 0,
       "point_reads": 0, "script_sha256": hashlib.sha256(here.read_bytes()).hexdigest()}
dest = here.with_suffix(".json")
assert not dest.exists()
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": out["status"], "summaries": summaries}, ensure_ascii=False, indent=2))
