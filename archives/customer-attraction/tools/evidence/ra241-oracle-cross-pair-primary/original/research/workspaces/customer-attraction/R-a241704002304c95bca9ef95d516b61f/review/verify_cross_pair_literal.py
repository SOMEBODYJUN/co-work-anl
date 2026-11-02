"""Independent literal audit of proposed cross-branch comparisons.

Reads the frozen 27 joint atoms only; imports no research row generator.
Each orbit sum is the common S6 symmetrization of literal IC comparisons.
This is an audit of necessary inequalities, never a six-player SPE proof.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "work.py").exists())
SOURCE = ROOT / "research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms_exact.json"


def partition(indices):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in indices)


def main():
    data = json.loads(SOURCE.read_text())
    slacks = defaultdict(F)
    comparisons = 0
    for atom in data["atoms"]:
        hi = atom["hist_index"]
        h = data["histograms"][hi]
        a = tuple(map(int, h["actual_bits"]))
        b = sum(a[:3])
        last_background = sum(a[:4])
        words = [w for w, n in zip(product((0, 1), repeat=3), h["hist"]) for _ in range(n)]
        groups = {
            (g[0], g[1], tuple(g[2]), tuple(g[3])): j
            for j, g in enumerate(data["groups"][hi])
        }
        mass = F(atom["weight"])
        for fam, j, k in product(range(2), range(6), range(6)):
            if fam == 0 and j == k:
                continue
            gi = groups[fam, int(j == k), words[j], words[k]]
            r, z = atom["R"][gi], atom["Z"][gi]
            for i in range(6):
                t, p, q = words[i]
                # Last player in the true child (g,T_i,P_i,Q_i) may choose Z_e.
                key = ("old-C-Z", fam, partition((i, j, k)))
                slacks[key] += mass * F(q - z, b + t + p + 1)
                comparisons += 1
                # Last player after the actual four-prefix and R_e may choose
                # each old T_i, P_i, Q_i; its actual topic is Z_e.
                for coord in range(3):
                    key = ("Z-old", fam, coord, partition((j, k, i)))
                    slacks[key] += mass * F(z - words[i][coord], last_background + r + 1)
                    comparisons += 1
                base = b + t
                H = F(p + q, base + p + q) if p + q else F()
                H += F(p, (base + 1) * (base + 2))

                def pair_slack(x):
                    return H - F(x + z, base + 1) + F(x * z, (base + 1) * (base + 2))

                # True two-player child (P_i,Q_i), with either an actual theme
                # or another old branch theme paired with the same Z_e.
                for coord in range(6):
                    key = ("branch-pair-actual-Z", fam, coord, partition((i, j, k)))
                    slacks[key] += mass * pair_slack(a[coord])
                    comparisons += 1
                for l in range(6):
                    for coord in range(3):
                        key = ("branch-pair-old-Z", fam, coord, partition((i, j, k, l)))
                        slacks[key] += mass * pair_slack(words[l][coord])
                        comparisons += 1
    violations = [{"name": str(k), "slack": str(v)} for k, v in sorted(slacks.items()) if v < 0]
    report = {
        "status": "independent literal evaluation; not a proof of half or an SPE counterexample",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "literal_comparisons": comparisons,
        "orbit_families": len(slacks),
        "violations": violations,
        "minimum_slack": str(min(slacks.values())),
        "all_slacks": [{"name": str(k), "slack": str(v)} for k, v in sorted(slacks.items())],
    }
    candidate = HERE.parent / "solo_six/cross_pair_frozen_violations.json"
    if candidate.exists():
        authored = json.loads(candidate.read_text())
        expected = {v["name"]: v["slack"] for v in authored["violations"]}
        observed = {v["name"]: v["slack"] for v in violations}
        assert expected == observed, "Independent literal evaluation disagrees with the proposed rows"
        report["agrees_with_author_negative_rows"] = True
    (HERE / "cross_pair_literal_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "all_slacks"}, indent=2))


if __name__ == "__main__":
    main()
