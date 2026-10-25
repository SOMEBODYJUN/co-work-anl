"""Exact diagnostic for the valid commuting-prefix tool; not an SPE audit."""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
CERT = ROOT / "evidence/certificates/customer_attraction/five_player_indexed_bound.json"
THIRD = list(itertools.product((0, 1), repeat=3))
SECOND = list(itertools.product((0, 1), repeat=4))
KNOTS = (F(0), F(1, 3), F(1, 2), F(1))


def share(n, d):
    return F(n, d) if n else F(0)


def lower(p, q, lam):
    return min(share(q, p), share(q + 2 * lam, p + 2)) if q else F(0)


def indexed(atom, family, q_index, lam):
    bits = list(map(int, atom["bits"]))
    a, q = bits[0], bits[q_index]
    ans = F(0)
    for cnt, (t, h, i, j) in zip(atom["second_hist"], SECOND):
        ans += cnt * share(h, a + t + h + i + j)
    for cnt, (t, r, s) in zip(atom[family + "_hist"], THIRD):
        p = a + q + t
        h_tail = share(r + s, p + r + s) + share(r, (p + 1) * (p + 2))
        ans += cnt * (lam * h_tail - lower(p, q, lam))
    return ans


def nonindexed(atom, lam):
    a, b, _, _, e, u, v, w, x, y = map(int, atom["bits"])
    p = a + b + e
    h_tail = share(x + y, p + x + y) + share(x, (p + 1) * (p + 2))
    return share(u, a + e + u + v + w) + lam * h_tail - lower(p, b, lam)


def main():
    cert = json.loads(CERT.read_text())["primal"]
    denominator = int(cert["denominator"])
    rows = []
    for name, evaluator in (
        ("AB", lambda atom, lam: indexed(atom, "AB", 1, lam)),
        ("AE", lambda atom, lam: indexed(atom, "AE", 4, lam)),
        ("nonindexed_B", nonindexed),
    ):
        for lam in KNOTS:
            slack = sum(
                (F(int(atom["mass_numerator"]), denominator) * evaluator(atom, lam)
                 for atom in cert["atoms"]), F(0)
            )
            assert slack > 0
            rows.append({"family": name, "lambda": str(lam), "slack": str(slack), "approx": float(slack)})
    out = {"status": "TOOL ONLY; none excludes historical primal", "rows": rows}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
