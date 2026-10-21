"""Recover and independently check a rational *projection* witness.

This checks necessary rows only; no continuation tree is present.
"""
from pathlib import Path
from fractions import Fraction as F
import json

from actual_ap_projection import build


HERE = Path(__file__).resolve().parent
M = 5
MAXIMA = [[2,3,5], [4,5], [4,5], [5]]


def get_witness():
    data = json.loads((HERE / "actual_bns_projection_m5_symmetric.json").read_text())
    atoms = data["atoms_float"]
    support = [a["mask"] for a in atoms]
    floats = [a["mass"] for a in atoms]
    _, _, _, rows, _ = build(M, MAXIMA)
    # Reconstruct a vertex using exact rational versions of the small fixed
    # coefficients.  The audit below recalculates all rows from definitions.
    def coefficient(row, a):
        return sum(F(float(row[a + (1 << (M+t)) - 1])).limit_denominator(10000)
                   for t in range(M)) / M
    tight = [[F(a != 0) for a in support]]
    rhs = [F(1)]
    for row in rows:
        coefficients = [coefficient(row, a) for a in support]
        if abs(sum(float(c)*v for c,v in zip(coefficients,floats))) < 1e-7:
            tight.append(coefficients)
            rhs.append(F(0))
    augmented = [row + [y] for row,y in zip(tight,rhs)]
    pivot = 0
    for col in range(len(support)):
        chosen = next((j for j in range(pivot,len(augmented)) if augmented[j][col]), None)
        assert chosen is not None
        augmented[pivot],augmented[chosen] = augmented[chosen],augmented[pivot]
        scale = augmented[pivot][col]
        augmented[pivot] = [v/scale for v in augmented[pivot]]
        for j in range(len(augmented)):
            if j != pivot and augmented[j][col]:
                factor = augmented[j][col]
                augmented[j] = [a-factor*b for a,b in zip(augmented[j],augmented[pivot])]
        pivot += 1
    assert all(not any(row[:-1]) and not row[-1] for row in augmented[pivot:])
    return {a:augmented[j][-1] for j,a in enumerate(support)}


def audit(mass):
    # Symmetric comparison topics each get one fifth of every listed group.
    atoms = [(a | (1 << (M+t)), v / M) for a,v in mass.items() for t in range(M)]
    assert all(v >= 0 for _,v in atoms)
    def bit(z,a):
        return (z >> a) & 1
    def dot(fn):
        return sum((v*fn(z) for z,v in atoms), F(0))
    welfare = dot(lambda z:F(bool(z & ((1<<M)-1))))
    opt = dot(lambda z:F(bool(z >> M)))
    assert welfare == 1 and opt > 2
    counts = {"floor":0, "AP":0, "BNS_all_maxima":0}
    records = []
    min_slack = None
    for i in range(M):
        k = M-i
        def b(z):
            return (z & ((1<<i)-1)).bit_count()
        u = dot(lambda z:F(bit(z,i), (z & ((1<<M)-1)).bit_count()) if bit(z,i) else F(0))
        size = [dot(lambda z,c=c:F(bit(z,c), b(z)+k)) for c in range(2*M)]
        maximum = max(size)
        maxima = [c for c,s in enumerate(size) if s == maximum]
        records.append({"i":i, "u":str(u), "K":str(maximum), "delta":str(u-maximum), "maxima":maxima})
        for s in size:
            slack = u-s
            assert slack >= 0
            counts["floor"] += 1
        if k == 1:
            continue
        for c in range(2*M):
            coefficient = F((k-1)*(M-1)) + F(k*k,2)
            for d in range(2*M):
                f = dot(lambda z:F(bit(z,d), b(z)+k) if bit(z,c)
                        else F(bit(z,d),b(z)+1))
                slack = size[c] + coefficient*(u-size[c]) - f
                assert slack >= 0, ("AP",i,c,d,slack)
                counts["AP"] += 1
                min_slack = slack if min_slack is None else min(min_slack,slack)
        for c in maxima:
            max_b = max([b(z) for z,v in atoms if v > 0 and bit(z,c)] + [0])
            coefficient = (k-1)*(k+max_b-1)
            for d in range(2*M):
                f = dot(lambda z:F(bit(z,d), b(z)+k) if bit(z,c)
                        else F(bit(z,d),b(z)+1))
                slack = maximum + coefficient*(u-maximum) - f
                assert slack >= 0, ("BNS-C",i,c,d,slack)
                counts["BNS_all_maxima"] += 1
    return {"scope":"Exact counterexample to summing these necessary rows, NOT an SPE counterexample.",
            "m":M, "W":str(welfare), "comparison_union":str(opt), "excess_over_2W":str(opt-2*welfare),
            "group_mass":{str(a):str(v) for a,v in mass.items()}, "group_interpretation":
            "For each actual-membership mask a and each t=0,...,4, put mass group_mass[a]/5 at a | 2^(5+t).",
            "checked_rows":counts, "actual_nodes":records, "minimum_AP_slack":str(min_slack)}


if __name__ == "__main__":
    report = audit(get_witness())
    (HERE / "exact_projection_witness.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in {"group_mass","actual_nodes","group_interpretation"}}))
