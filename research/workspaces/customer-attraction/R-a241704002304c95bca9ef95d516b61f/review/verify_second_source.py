"""Independent literal check of the capacity-free second source cut."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
POINT = HERE.parent / "solo_six/source_requery_exact.json"


def phi(a, r, cj):
    b, ell = sum(a[:3]), sum(a[:5])
    vals = []
    for p, q in product((0, 1), repeat=2):
        v = F(r, b + r + p + q) if r else F()
        v += F(4, 7) * F(q, sum(a[:2]) + 4)
        v += F(9, 35) * F(q, ell + 1) + F(1, 5) * F(p, ell + 1)
        if q:
            v -= F(2, 5) * F(q, b + r + p + q)
        v += F(2, 5) * F(cj, b + r + p + 1)
        vals.append(v)
    return min(vals)


def main():
    data = json.loads(POINT.read_text())
    u3 = u4 = u6 = rhs = F()
    terms = 0
    for atom in data["atoms"]:
        hi = atom["hist_index"]
        h = data["histograms"][hi]
        a = tuple(map(int, h["actual_bits"]))
        weight = F(atom["weight"])
        if sum(a):
            u3 += weight * F(a[2], sum(a))
            u4 += weight * F(a[3], sum(a))
            u6 += weight * F(a[5], sum(a))
        words = [w for w, n in zip(product((0, 1), repeat=3), h["hist"]) for _ in range(n)]
        groups = {
            (g[0], g[1], tuple(g[2]), tuple(g[3])): k
            for k, g in enumerate(data["groups"][hi])
        }
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            k = groups[1, 0, words[i], words[j]]
            rhs += weight * phi(a, atom["R"][k], words[j][2])
            terms += 1
    lhs = 30 * (u4 + F(4, 7) * u3 + F(16, 35) * u6)
    slack = lhs - rhs
    assert slack < 0, "Announced second cut does not separate the supplied first-cut witness"
    report = {
        "scope": "independent exact necessary-row separation; not an SPE or half proof",
        "point_sha256": hashlib.sha256(POINT.read_bytes()).hexdigest(),
        "point": str(POINT.relative_to(HERE.parent)),
        "literal_index_terms": terms,
        "u3": str(u3), "u4": str(u4), "u6": str(u6),
        "lhs": str(lhs), "rhs": str(rhs),
        "slack": str(slack), "slack_float": float(slack),
    }
    (HERE / "second_source_cut_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
