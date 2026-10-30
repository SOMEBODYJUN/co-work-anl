"""Decode the saved seven-row dual and pair data; cleanup arithmetic only.

No LP solve and no repeat of the full 2778-row verifier. The upper certificate
is checked as one exact sparse identity, and a single three-topic consistency
failure is extracted from the already verified primal.
"""
from ast import literal_eval
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def add_scaled(out, row, scale):
    for key, value in row.items():
        out[key] = out.get(key, F(0)) + scale * value
        if not out[key]:
            del out[key]
    return out


def coord(q, a):
    return (tuple(q), a)


def count(labels):
    return tuple(labels.count(a) for a in range(6))


def encode(v):
    q, a = v
    return f"U{a}[{''.join(str(b) * q[b] for b in range(6))}]"


def unit(q, a):
    return {coord(q, a): F(1)}


def total(q):
    return {coord(q, a): F(q[a]) for a in range(6) if q[a]}


def third_pair(a, b):
    out = {}
    add_scaled(out, unit(count([a, a, b]), a), F(2))
    add_scaled(out, unit(count([a, b, b]), b), F(2))
    add_scaled(out, unit(count([a, b, b]), a), F(-1))
    add_scaled(out, unit(count([b, b, b]), b), F(-3))
    return out


def main():
    raw = (BASE / "original/complete_pair_v2.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (
        "a6ad7e44fcba37d1c0a1fc0c128ed200b70e7ba34ef3c96b2445f299e1524e32"
    )
    obj = json.loads(raw)
    y = {literal_eval(k): F(v) for k, v in obj["positive_values"].items()}
    actions = {tuple(x["history"]): x["action"] for x in obj["strategy_actions"]}
    z = {}
    for k in range(3, -1, -1):
        for h in product(range(6), repeat=k):
            z[h] = count(h) if k == 3 else z[h + (actions[h],)]
    assert list(z[()]) == obj["root"]
    qs = sorted({count(h) for h in product(range(6), repeat=3)})
    vertices = [(q, a) for q in qs for a in range(6) if q[a]]
    weights = {int(i): F(v) for i, v in obj["dual_nonzero"]}
    selected = {}
    provenance = {}
    for i, (h, a) in enumerate(actions.items()):
        for b in range(6):
            j = i * 6 + b
            if j in weights:
                row = unit(z[h], a)
                add_scaled(row, unit(z[h + (b,)], b), F(-1))
                selected[j] = row
                provenance[j] = {"kind": "true-history-incentive", "history": list(h),
                                 "prescribed": a, "alternative": b}
    j = 258
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            if j in weights:
                kappa = max(
                    F(sum(r[c] for c in range(6) if typ >> c & 1),
                      sum(q[c] for c in range(6) if typ >> c & 1))
                    for typ in range(1, 64) if typ >> a & 1
                )
                row = {}
                add_scaled(row, unit(r, a), kappa)
                add_scaled(row, unit(q, a), F(-1))
                selected[j] = row
                provenance[j] = {"kind": "same-topic-dilution", "topic": a,
                                 "q": list(q), "r": list(r), "kappa": str(kappa)}
            j += 1
    assert j == 2778 and set(selected) == set(weights)
    residual = {}
    add_scaled(residual, total(z[()]), F(2))
    add_scaled(residual, total(count(obj["portfolio"])), F(-1))
    add_scaled(residual, third_pair(1, 4), F(1))
    add_scaled(residual, third_pair(3, 4), F(-1))
    for j, mu in weights.items():
        add_scaled(residual, selected[j], -mu)
    assert residual == {}
    eq = [(i, F(v)) for i, v in enumerate(obj["dual_equalities"]) if F(v)]
    assert eq == [(0, F(2)), (39, F(1)), (54, F(-1))]

    def val(labels, a):
        return y.get(coord(count(labels), a), F(0))

    def C(labels):
        q = count(labels)
        return sum((q[a] * y[coord(q, a)] for a in range(6) if q[a]), F(0))

    pairs = []
    for a, b in combinations(range(6), 2):
        ca, cb, cab = C([a, a, a]), C([b, b, b]), C([a, a, b])
        masses = [cab - cb, cab - ca, ca + cb - cab]
        assert min(masses) >= 0
        pairs.append({
            "pair": [a, b], "Ca": str(ca), "Cb": str(cb), "Cab": str(cab),
            "a_only": str(masses[0]), "b_only": str(masses[1]), "both": str(masses[2]),
        })
    lhs = val([0, 3, 4], 0) - val([0, 3, 4], 3)
    rhs = (C([0, 0, 0]) - C([3, 3, 3]) + C([0, 0, 4]) - C([3, 3, 4])) / 2
    assert lhs == -F(1, 27) and rhs == -F(1, 9)
    coverage_gap = C([0, 0, 3]) + C([0, 0, 4]) - C([0, 0, 0]) - C([3, 3, 4])
    assert coverage_gap == -F(2, 9)
    records = [
        {"index": j, "multiplier": str(weights[j]), **provenance[j],
         "row": {encode(v): str(c) for v, c in selected[j].items()}}
        for j in sorted(selected)
    ]
    report = {
        "scope": "cleanup extraction of a sparse exact upper identity and explicit non-gluing witness; no optimizer/full-tree recheck",
        "upper_identity": "2*C(root)-C(T)+E3(1,4)-E3(3,4)=sum(mu_j*row_j)",
        "all_126_sparse_identity_coordinates_zero": True,
        "nonnegative_inequality_rows": records,
        "equality_nonzero_multipliers": [[i, str(v)] for i, v in eq],
        "pair_customer_masses": pairs,
        "pairwise_common_total": "2; add empty pair-type mass 2-Cab to each local table",
        "nonnegative_coverage_separator": {
            "valid_expression": "C03+C04-C0-C34 >= 0 for every nonnegative customer instance",
            "saved_pair_data_value": str(coverage_gap),
        },
        "global_signed_three_topic_failure": {
            "support": [0, 3, 4],
            "U0": str(val([0, 3, 4], 0)), "U3": str(val([0, 3, 4], 3)),
            "C0": str(C([0, 0, 0])), "C3": str(C([3, 3, 3])),
            "C04": str(C([0, 0, 4])), "C34": str(C([3, 3, 4])),
            "left": str(lhs), "required_right": str(rhs), "difference": str(lhs - rhs),
        },
        "pair_scope": "All 15 pair reconstructions are nonnegative, but no one global signed customer representation realizes the full saved array.",
    }
    (BASE / "replay/sparse-upper-identity-and-gluing-gap.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
