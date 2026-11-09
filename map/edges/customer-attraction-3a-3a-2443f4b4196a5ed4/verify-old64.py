"""Replay exact frozen-row witnesses with no numerical solver or in-place output."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from hashlib import sha256
import json
from pathlib import Path

parser = ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, default=Path.cwd())
ROOT = parser.parse_args().repo.resolve()
EVIDENCE = ROOT / "archives/customer-attraction/tools/evidence/credible-feedback-and-alignment-primary"
ORIGINAL = EVIDENCE / "original"
CERTIFICATE = EVIDENCE / "dependencies/five_player_indexed_bound.json"


INPUT_HASHES = {
    "five_player_indexed_bound.json": "18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1",
    "joint_alignment_proposal.json": "bfddb4b67fcd5e7e76107beb4b047bdf3d0db8c1dd2099cfe40cf7c08ac439af",
    "best_alignment_proposal.json": "2cfff70e22d0bcab8d4766d38b28af6a44692000dda598c645897cd17a59b44f",
    "max_topic_security_proposal.json": "79be592181684096419c1a4c1385924b2904ec3cd1bc5011028b36772a3cde71",
    "universal_punisher_exact.json": "f8ce8b07418db1f151cb5382c7c27358ad61ec5b79a30408ec530161bd6fd542",
}


def read(path):
    data = path.read_bytes()
    assert sha256(data).hexdigest() == INPUT_HASHES[path.name]
    return json.loads(data)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


primal = read(CERTIFICATE)["primal"]
atoms = primal["atoms"]
r = [F(a["mass_numerator"], int(primal["denominator"])) for a in atoms]
bits = [tuple(map(int, a["bits"])) for a in atoms]
assert len(r) == 64 and min(r) > 0
assert all(sum(a[h][len(a[h]) // 2:]) == 1 for a in atoms
           for h in ("AB_hist", "AE_hist", "second_hist"))
p = [sum(b[:3]) for b in bits]
u = [sum(m / sum(b[:5]) for m, b in zip(r, bits) if b[i]) for i in range(5)]
residual = [m / (q + 1) for m, q in zip(r, p)]
copy = [m / (q + 2) for m, q in zip(r, p)]
G = sum(residual)
fixed = [
    (sum(m / (q + 1) for m, q, b in zip(r, p, bits) if b[j]),
     [-m * b[j] / ((q + 1) * (q + 2)) for m, q, b in zip(r, p, bits)])
    for j in range(10)
]
average = (G / 4, [-v / 4 for v in residual])
t0 = (F(0), copy)


def difference(test, prescribed):
    a, x = test
    b, y = prescribed
    return ([v - w for v, w in zip(x, y)], b - a)


def shared_rows():
    rows = {}
    for i in range(5):
        g = [m / (sum(b[:i]) + 5 - i) for m, b in zip(r, bits)]
        rows[f"T0_path_floor_{i}"] = (g, u[i])
        rows[f"Tother_path_floor_{i}"] = ([-v / 4 for v in g], u[i] - sum(g) / 4)
    for dev in (4, 6, 7, 8, 9):
        load = [q + b[dev] for q, b in zip(p, bits)]
        g = [m / (ll + 1) for m, ll in zip(r, load)]
        best = max(sum(v * b[j] for v, b in zip(g, bits)) for j in range(10))
        base = sum(m / ll for m, ll, b in zip(r, load, bits) if b[dev])
        loss = [-m / (ll * (ll + 1)) if b[dev] else F(0)
                for m, ll, b in zip(r, load, bits)]
        rows[f"fixeddev_{dev}_replyT0_BR_fixed"] = ([-v for v in g], -best)
        rows[f"fixeddev_{dev}_replyT0_BR_other_T"] = ([-5 * v / 4 for v in g], -sum(g) / 4)
        rows[f"fixeddev_{dev}_penultimate_IC"] = (loss, u[3] - base)
    assert len(rows) == 25
    return rows


def own_rows(last):
    reply = fixed[last] if last < 10 else t0
    rows = {f"last_BR_fixed_{j}": difference(option, reply) for j, option in enumerate(fixed)}
    rows["last_BR_T0_copy"] = difference(t0, reply)
    rows["last_BR_other_T"] = difference(average, reply)
    own = [m / (q + 1 + b[last]) for m, q, b in zip(r, p, bits)] if last < 10 else copy
    return rows, own


def solve_basis(coefficients, rhs):
    """Gauss–Jordan over Q. Return None if the proposed square basis is singular."""
    n = len(rhs)
    rows = [list(a) + [b] for a, b in zip(coefficients, rhs)]
    for j in range(n):
        k = next((i for i in range(j, n) if rows[i][j]), None)
        if k is None:
            return None
        rows[j], rows[k] = rows[k], rows[j]
        pivot = rows[j][j]
        rows[j] = [v / pivot for v in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                coefficient = rows[i][j]
                rows[i] = [v - coefficient * w for v, w in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def reconstruct_point(rows, candidate, lower, upper):
    x = [F(lo) if abs(float(lo) - v) < 1e-8
         else F(hi) if abs(float(hi) - v) < 1e-8 else F(0)
         for v, lo, hi in zip(candidate, lower, upper)]
    unknown = [j for j, v in enumerate(candidate)
               if float(lower[j]) + 1e-8 < v < float(upper[j]) - 1e-8]
    tight = [name for name, (a, b) in rows.items()
             if abs(float(b) - dot(list(map(float, a)), candidate)) < 1e-8]
    for names in combinations(tight, len(unknown)):
        equations = [rows[name] for name in names]
        matrix = [[a[j] for j in unknown] for a, _ in equations]
        v = solve_basis(matrix, [b - dot(a, x) for a, b in equations])
        if v is None:
            continue
        exact = x.copy()
        for j, value in zip(unknown, v):
            exact[j] = value
        if (all(lo <= v <= hi for v, lo, hi in zip(exact, lower, upper))
            and all(dot(a, exact) <= b for a, b in rows.values())):
            return names, exact
    raise AssertionError((unknown, tight))


result = {"input_sha256": INPUT_HASHES}
shared = shared_rows()
joint = read(ORIGINAL / "joint_alignment_proposal.json")
best = read(ORIGINAL / "best_alignment_proposal.json")
assert joint["branches"] == [4, 6, 7, 8, 9] and best["partition"] == [0] * 5
counts = Counter(
    "no_certificate" if "minimum_common_IC_violation" not in rec else
    "negative" if rec["minimum_common_IC_violation"] < 0 else "positive"
    for rec in joint["results"]
)
assert counts == {"negative": 1, "positive": 41, "no_certificate": 10}
assert {tuple(record["partition"]) for record in joint["results"]} == {
    part for part in product(range(5), repeat=5)
    if all(v <= max(part[:i], default=-1) + 1 for i, v in enumerate(part))
}
result["historical_joint_floating_statuses"] = dict(counts)
joint_rows = {name: (a + [F(-name.endswith("_IC"))], b) for name, (a, b) in shared.items()}
basis, z = reconstruct_point(joint_rows, best["x"][:-1:5] + [best["delta"]], [0] * 64 + [-2], [1] * 64 + [2])
assert z[-1] < 0
result["joint_all_T0_exact_feasible"] = {
    "symmetry_lift": "Set x[k,0]=x[k] and each x[k,j]=(1-x[k])/4 for j=1,2,3,4.",
    "basis": basis,
    "x_T0": [str(v) for v in z[:-1]],
    "delta": str(z[-1]),
    "delta_decimal": float(z[-1]),
    "scope": "Feasibility of this partition; no exact optimum claim and no other partition upgraded.",
}

proposals = read(ORIGINAL / "max_topic_security_proposal.json")
certificates = read(ORIGINAL / "universal_punisher_exact.json")
result["max_topic_exact_feasible"] = {}
result["punisher"] = {}
for last, certificate in enumerate(certificates["fixed_last_reply_certificates"]):
    last_rows, own = own_rows(last)
    label = ("ABCDEUVWXY" + "T")[last] if last < 10 else "T0"
    assert label == certificate["last_reply"] == proposals[last]["last_reply"]
    rows = {**shared, **last_rows, "T0_penultimate_IC": (own, u[3])}
    mu = {name: F(value) for name, value in certificate["multipliers"].items()}
    assert len(rows) == 38 and min(mu.values()) > 0 and sum(mu.values()) == 1
    aa = [sum(value * rows[name][0][j] for name, value in mu.items()) for j in range(64)]
    beta = sum(value * rows[name][1] for name, value in mu.items())
    kappa = sum(min(F(0), v) for v in aa) - beta
    assert kappa > 0 and str(kappa) == certificate["minimum_common_violation_at_least"]
    assert [str(v) for v in aa] == certificate["linear_coefficients"]
    assert str(beta) == certificate["weighted_rhs"]
    result["punisher"][label] = str(kappa)
    if "x" not in proposals[last]:
        continue
    common_floors = {name: data for name, data in shared.items() if "_path_floor_" in name}
    max_rows = {**common_floors, **last_rows, "T0_has_largest_residual": ([-v for v in residual], -G / 5)}
    assert len(max_rows) == 23 and len(set(max_rows).intersection(rows)) == 22
    basis, x = reconstruct_point(max_rows, proposals[last]["x"], [0] * 64, [1] * 64)
    margin = dot(own, x) - u[3]
    result["max_topic_exact_feasible"][label] = {
        "basis": basis,
        "x_T0": [str(v) for v in x],
        "T0_payoff": str(dot(own, x)),
        "margin_to_D": str(margin),
        "margin_to_D_decimal": float(margin),
        "violated_shared_rows": [name for name, (a, b) in rows.items() if dot(a, x) > b],
        "scope": "Exact feasible vector for the 23-row LP; no optimality claim.",
    }

other_T = sum(m * b[7] / (q + b[6] + 1) for m, b, q in zip(r, bits, p)) - u[3]
assert other_T > 0 and str(other_T) == certificates["other_T_last_reply_margin"]
result["other_T_margin"] = str(other_T)
assert all(F(result["max_topic_exact_feasible"][label]["margin_to_D"]) < 0 for label in ("V", "X"))
print(json.dumps(result, indent=2))
