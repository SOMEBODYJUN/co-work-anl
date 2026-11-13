"""Recompute the two saved S3 cuts from the point, with no original imports.

This checks the two fixed-point evaluations and the finite local identities.
It does not verify old 1146-row feasibility, optimizer optimality, or an SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "archives/customer-attraction/tools/evidence/middle-safe-and-zz-resume-primary"
POINT = EVIDENCE / "dependencies/research/workspaces/customer-attraction/R-a241704002304c95bca9ef95d516b61f/solo_six/source_requery_exact.json"
PARAMETERS = EVIDENCE / "original/research/workspaces/customer-attraction/R-68a6ffab8681474aa2228b770a56e263/attack/source_middle/cut_source3_B-off.json"
AUDIT = EVIDENCE / "saved-cuts-audit.json"


def load(path, expected):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected
    return json.loads(raw)


def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)


point = load(POINT, "480f7a96c21bad34f01192f179306d2da05f84ae47dfd0c36c1cd79acd9c6a27")
parameters = load(PARAMETERS, "1e6fd7ace44de69e5ed07a75234b872cad19716d816bb76c7ba091507ffb71fb")
audit = load(AUDIT, "9fb2ff3ba8d32a56b54779b699e0ed879ad4a2caa36745a77fe6bf73a2cdc7c9")
assert len(point["atoms"]) == 28
assert len(point["histograms"]) == len(point["groups"]) == 16
assert sum(map(len, point["groups"])) == 194
words = tuple(product((0, 1), repeat=3))
tails = tuple(product((0, 1), repeat=3))
literal_indices = [(i, j) for i in range(6) for j in range(6) if i != j]
hist_data = []
for hist, groups in zip(point["histograms"], point["groups"]):
    a = tuple(map(int, hist["actual_bits"]))
    assert len(a) == 6 and set(a) <= {0, 1}
    assert len(hist["hist"]) == 8 and all(isinstance(n, int) and n >= 0 for n in hist["hist"])
    expanded = [word for word, n in zip(words, hist["hist"]) for _ in range(n)]
    assert len(expanded) == 6
    assert hist["d"] == sum(word[0] for word in expanded)
    group_map = {(f, diag, tuple(wi), tuple(wj)): index for index, (f, diag, wi, wj) in enumerate(groups)}
    assert len(group_map) == len(groups)
    hist_data.append((a, expanded, group_map))

payoffs = [F(0)] * 6
coverage = F(0)
for atom in point["atoms"]:
    hist_index = atom["hist_index"]
    assert isinstance(hist_index, int) and 0 <= hist_index < 16
    assert F(atom["weight"]) > 0
    assert len(atom["R"]) == len(atom["Z"]) == len(point["groups"][hist_index])
    assert set(atom["R"]) <= {0, 1} and set(atom["Z"]) <= {0, 1}
    a, _, _ = hist_data[hist_index]
    mass = F(atom["weight"])
    coverage += mass * bool(sum(a))
    for player in range(6):
        payoffs[player] += mass * share(a[player], sum(a))
assert payoffs == list(map(F, audit["payoffs"]))
assert coverage == sum(payoffs) == F(point["W"])
assert F(point["O"]) - 2 * coverage == F(point["strict_half_gap"])

report = {
    "scope": "two fixed S3 parameter evaluations and finite local identities; no 1146-row feasibility, optimization, SPE or half claim",
    "audit_sha256": hashlib.sha256(AUDIT.read_bytes()).hexdigest(),
    "point_sha256": hashlib.sha256(POINT.read_bytes()).hexdigest(),
    "parameters_sha256": hashlib.sha256(PARAMETERS.read_bytes()).hexdigest(),
    "point_shapes_checked": {"atoms": 28, "histograms": 16, "groups": 194},
    "actual_payoffs_match": True,
    "cuts": {},
}
integer_formula_checks = 0
for a in product((0, 1), repeat=6):
    b, ell = sum(a[:2]), sum(a[:5])
    for t, ti, ci, yj in product((0, 1), repeat=4):
        for p, q, z in tails:
            den = b + t + p + q + z
            last_den = b + t + p + q + 1
            raw_rows = (share(285 * t, den) + 5 * p + share(15 * p, ell + 1)
                        + q + share(96 * q, b + 4) + share(120 * z, b + 4)
                        - 15 * (share(q, den) - share(ci, b + t + p + 2))
                        - 10 * (share(z, den) - share(ti, last_den))
                        - 10 * (share(z, den) - share(ci, last_den))
                        - 10 * (share(z, den) - share(yj, last_den)))
            combined = (share(285 * t - 15 * q - 30 * z, den) + 5 * p + q
                        + share(15 * p, ell + 1) + share(96 * q + 120 * z, b + 4)
                        + share(15 * ci, b + t + p + 2)
                        + share(10 * (ti + ci + yj), last_den))
            assert raw_rows == combined
            integer_formula_checks += 1
assert integer_formula_checks == audit["integer_formula_checks"] == 8192
zz_checks = 0
for a in range(7):
    for re, ze, zf in product((0, 1), repeat=3):
        assert F(ze - zf, a + re + 1) == F(ze - zf, a + 1) - F(re * (ze - zf), (a + 1) * (a + 2))
        zz_checks += 1
assert zz_checks == audit["zz_identity_checks"] == 56
for coefficient in (1, 2):
    def value(bits):
        r0, z0, r1, z1 = bits
        return int(r0 != z0) + int(r1 != z1) + coefficient * (r0 * r1 + z0 * z1)
    assert audit["four_bit_example_check"][str(coefficient)] == {
        "all_bits_max": max(value(bits) for bits in product((0, 1), repeat=4)),
        "fully_constant_max": max(value((bit,) * 4) for bit in (0, 1)),
    }
report["local_identity_crosschecks"] = {
    "S3_integer_formula_checks": integer_formula_checks,
    "ZZ_identity_checks": zz_checks,
    "four_bit_examples_match": True,
    "role": "S3 expansion supports this edge; ZZ and four-bit checks only confirm otherwise unused audit metadata",
}
for label in ("with_middle", "terminal_only"):
    cut = parameters[label]
    saved = audit["cuts"][label]
    assert cut["source"] == 3 and cut["family"] == "B-off"
    assert F(cut["lambda_source"]) == 1
    assert all(0 <= F(row["weight"]) <= cut["parameter_bound"] for row in cut["parameters"])
    assert len(saved["terms"]) == 28 * 30
    lhs_per_query = payoffs[2]
    for row in cut["parameters"]:
        if row["kind"] == "capacity":
            lhs_per_query += F(row["weight"]) * F(point["K"])
        elif row["kind"] == "price":
            lhs_per_query += F(row["weight"]) * payoffs[row["query"] - 1]
        else:
            assert row["kind"] == "safe"
    rhs = F(0)
    configurations = set()
    checked_values = 0
    per_atom = []
    for atom_index, atom in enumerate(point["atoms"]):
        a, expanded, group_map = hist_data[atom["hist_index"]]
        b = sum(a[:2])
        mass = F(atom["weight"])
        atom_rhs = F(0)
        for ij, (i, j) in enumerate(literal_indices):
            ti, bi, ci = expanded[i]
            _, yj, _ = expanded[j]
            t = atom["R"][group_map[(0, 0, expanded[i], expanded[j])]]
            # The saved 44-config key also retains unused Bi, as the input does.
            configurations.add((a, ti, bi, ci, yj, t))
            values = []
            for p, q, z in tails:
                tail = (p, q, z)
                denominator = b + t + p + q + z
                value = share(t, denominator)
                for row in cut["parameters"]:
                    weight = F(row["weight"])
                    l = row["tail_position"]
                    bit = tail[l - 1]
                    if row["kind"] == "capacity":
                        value += weight * bit
                    elif row["kind"] == "price":
                        player = row["query"]
                        value += weight * share(bit, sum(a[:player - 1]) + 7 - player)
                    else:
                        query_bit = {"Ti": ti, "Ci": ci, "Yj": yj}[row["query"]]
                        safe_denominator = b + t + sum(tail[:l - 1]) + 4 - l
                        value -= weight * (share(bit, denominator) - share(query_bit, safe_denominator))
                if label == "with_middle":
                    # Independently compare the combined G/285 printed in the lemma.
                    combined = (share(285 * t - 15 * q - 30 * z, denominator)
                                + 5 * p + q + share(15 * p, sum(a[:5]) + 1)
                                + share(96 * q + 120 * z, b + 4)
                                + share(15 * ci, b + t + p + 2)
                                + share(10 * (ti + ci + yj), b + t + p + q + 1)) / 285
                    assert value == combined
                values.append(value)
            term = saved["terms"][30 * atom_index + ij]
            assert set(term) == {"atom", "i", "j", "values", "mass", "minimum"}
            assert (term["atom"], term["i"], term["j"]) == (atom_index, i, j)
            assert F(term["mass"]) == mass
            assert list(map(F, term["values"])) == values
            assert F(term["minimum"]) == min(values)
            checked_values += len(values)
            atom_rhs += mass * min(values)
        rhs += atom_rhs
        per_atom.append({"atom": atom_index, "terms": 30, "values": 240, "rhs": str(atom_rhs)})
    lhs = 30 * lhs_per_query
    slack = lhs - rhs
    assert len(configurations) == 44
    for key, value in (("lhs", lhs), ("rhs", rhs), ("slack", slack)):
        assert F(saved[key]) == F(cut[key]) == value
    assert slack < 0
    report["cuts"][label] = {
        "terms_checked": 840, "tail_values_checked": checked_values,
        "distinct_configurations": len(configurations),
        "lhs": str(lhs), "rhs": str(rhs), "slack": str(slack),
        "per_atom": per_atom,
    }
out = Path(__file__).with_name("exact-review.json")
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": "PASS", "report": str(out.relative_to(ROOT)),
                  "cuts": {label: {k: v for k, v in cut.items() if k != "per_atom"}
                           for label, cut in report["cuts"].items()}}, indent=2))
