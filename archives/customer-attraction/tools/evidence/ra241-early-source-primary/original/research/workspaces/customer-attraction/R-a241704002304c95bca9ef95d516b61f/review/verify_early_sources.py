"""Literal, unsorted hidden-bit audit of the second/third-source cuts."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
POINT = HERE.parent / "solo_six/source_requery_exact.json"


def phi(a, r, ti, source):
    b, ell = sum(a[:source-1]), sum(a[:5])
    middle = 5-source
    if source == 2:
        cP, cQ, mu = F(1, 64) + F(1, 32*(ell+1)), F(1, 16), F(1, 16)
    else:
        cP, cQ, mu = F(1, 18), F(1, 9), F(1, 9)
    vals = []
    # Deliberately enumerate every ordered tuple of middle membership bits;
    # no sorted-count projection from the author's implementation is reused.
    for bits in product((0, 1), repeat=middle+1):
        s, q = sum(bits[:-1]), bits[-1]
        v = F(r, b+r+s+q) if r else F()
        v += cP*s + cQ*q
        if q:
            v -= mu * F(q, b+r+s+q)
        v += mu * F(ti, b+r+s+1)
        vals.append(v)
    return min(vals)


def main():
    data = json.loads(POINT.read_text())
    u = [F() for _ in range(6)]
    rhs = {2: F(), 3: F()}
    terms = 0
    for atom in data["atoms"]:
        hi = atom["hist_index"]
        h = data["histograms"][hi]
        a = tuple(map(int, h["actual_bits"]))
        weight = F(atom["weight"])
        if sum(a):
            for i in range(6):
                u[i] += weight * F(a[i], sum(a))
        words = [w for w, n in zip(product((0, 1), repeat=3), h["hist"]) for _ in range(n)]
        groups = {
            (g[0], g[1], tuple(g[2]), tuple(g[3])): k
            for k, g in enumerate(data["groups"][hi])
        }
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            k = groups[0, 0, words[i], words[j]]
            for source in (2, 3):
                rhs[source] += weight * phi(a, atom["R"][k], words[i][0], source)
            terms += 1
    K = F(data["K"])
    lhs = {2: 30*(u[1]+F(3, 32)*u[5]+F(7, 64)*K), 3: 30*(u[2]+F(2, 9)*K)}
    report = {
        "scope": "independent exact early-source projection separation; no six-player half or SPE claim",
        "point_sha256": hashlib.sha256(POINT.read_bytes()).hexdigest(),
        "literal_index_terms_per_source": terms,
        "ordered_hidden_assignments_per_type": {"2": 16, "3": 8},
        "rows": [],
    }
    for source in (2, 3):
        slack = lhs[source]-rhs[source]
        assert slack < 0
        report["rows"].append({"source": source, "lhs": str(lhs[source]), "rhs": str(rhs[source]), "slack": str(slack), "slack_float": float(slack)})
    (HERE / "early_source_cuts_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
