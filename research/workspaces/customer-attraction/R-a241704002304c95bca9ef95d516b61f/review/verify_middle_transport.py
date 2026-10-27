"""Independent eight-state audit of the integer B-family middle-IC cut."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "work.py").exists())
OLD = ROOT / "research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms_exact.json"
FIRST = HERE.parent / "solo_six/source_requery_exact.json"


def share(x, d):
    return F(x, d) if x else F()


def phi(a, r, z, ti, y):
    b = sum(a[:3])
    vals = []
    for p, q, s in product((0, 1), repeat=3):
        D0, D1 = b+r+p+q, b+r+ti+s
        v = 90783*share(r, D0)
        v += 19980*(share(ti, D1)-share(p, D0))
        v += F(994*p+23194*q+6480*s, sum(a[:2])+4)
        v += F(30434*(p+q), sum(a[:5])+1)
        v += F(3435*(q-r), b+ti+y+1)
        v += F(13500*(s-z), sum(a[:4])+r+1)
        v += F(16545*ti+16545*y+4860*s, b+r+p+1)-37950*share(q, D0)
        v += F(19980*y, b+r+ti+1)-19980*share(s, D1)
        vals.append(v)
    return min(vals)


def evaluate(point):
    data = json.loads(point.read_text())
    u = [F() for _ in range(6)]
    rhs = F()
    terms = 0
    for atom in data["atoms"]:
        hi = atom["hist_index"]
        h = data["histograms"][hi]
        a = tuple(map(int, h["actual_bits"]))
        mass = F(atom["weight"])
        if sum(a):
            for i in range(6):
                u[i] += mass*F(a[i], sum(a))
        words = [w for w, n in zip(product((0, 1), repeat=3), h["hist"]) for _ in range(n)]
        groups = {
            (g[0], g[1], tuple(g[2]), tuple(g[3])): k
            for k, g in enumerate(data["groups"][hi])
        }
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            k = groups[0, 0, words[i], words[j]]
            rhs += mass*phi(a, atom["R"][k], atom["Z"][k], words[i][0], words[j][1])
            terms += 1
    lhs = 30*(90783*u[3]+30668*u[2]+60868*u[5])
    return {
        "point": str(point.relative_to(ROOT)),
        "sha256": hashlib.sha256(point.read_bytes()).hexdigest(),
        "literal_index_terms": terms,
        "lhs": str(lhs), "rhs": str(rhs),
        "slack": str(lhs-rhs), "slack_float": float(lhs-rhs),
    }


def main():
    report = {
        "scope": "independent evaluation of the exact integer middle-IC projection; no SPE or six-player half assertion",
        "joint_hidden_assignments_per_type": 8,
        "nonnegative_source_weight": 90783,
        "nonnegative_middle_weight": 19980,
        "nonnegative_Q_queries_S_weight": 4860,
        "evaluations": [evaluate(p) for p in (OLD, FIRST)],
    }
    (HERE / "middle_transport_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
