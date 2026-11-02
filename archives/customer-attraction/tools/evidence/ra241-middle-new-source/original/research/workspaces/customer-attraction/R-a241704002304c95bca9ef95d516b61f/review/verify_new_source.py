"""Literal independent audit of the fourth-source -> old R query cut.

Imports only standard library and reads only frozen complete R/Z atoms.
The hidden P,Q minimum is computed independently with Fraction arithmetic.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "work.py").exists())
# Keep the exact source identifier explicit rather than discovering a witness.
SOURCE = ROOT / "research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms_exact.json"


def phi(b, r, ti, ci, bj):
    vals = []
    for p, q in product((0, 1), repeat=2):
        v = F(r, b + r + p + q) if r else F()
        v += F(3, 4) * F(q, b + 3) + F(5, 48) * p
        if q:
            v -= F(1, 4) * F(q, b + r + p + q)
        v += (F(ti + ci, 24) + F(bj, 6)) / (b + r + p + 1)
        vals.append(v)
    return min(vals)


def main():
    data = json.loads(SOURCE.read_text())
    u4 = F()
    rhs = F()
    terms = 0
    for atom in data["atoms"]:
        hi = atom["hist_index"]
        h = data["histograms"][hi]
        a = tuple(map(int, h["actual_bits"]))
        b = sum(a[:3])
        weight = F(atom["weight"])
        if a[3]:
            u4 += weight / sum(a)
        words = [w for w, n in zip(product((0, 1), repeat=3), h["hist"]) for _ in range(n)]
        groups = {
            (g[0], g[1], tuple(g[2]), tuple(g[3])): k
            for k, g in enumerate(data["groups"][hi])
        }
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            k = groups[0, 0, words[i], words[j]]
            r = atom["R"][k]
            rhs += weight * phi(b, r, words[i][0], words[i][2], words[j][1])
            terms += 1
    lhs = 30 * (F(7, 4) * u4 + F(5, 48) * F(data["K"]))
    slack = lhs - rhs
    assert slack < 0, "The announced new-source cut does not separate the frozen witness"
    report = {
        "scope": "independent exact projection at a necessary-condition witness; not an SPE counterexample or a half proof",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "hidden_assignments_per_type": 4,
        "literal_index_terms": terms,
        "u4": str(u4),
        "K": data["K"],
        "orbit_size": 30,
        "lhs": str(lhs),
        "rhs": str(rhs),
        "slack": str(slack),
        "slack_float": float(slack),
    }
    (HERE / "new_source_cut_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
