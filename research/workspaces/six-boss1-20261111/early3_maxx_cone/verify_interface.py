#!/usr/bin/env python3
"""Independent point-free 17-row check from raw hist and marginal descriptors.

No builder import. No optimizer. No point weights. Literal query averaging is
reconstructed from raw A bits, T/B/C words, R/Z joint states and H role bits.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]


def recursive_tuple(value):
    return tuple(map(recursive_tuple, value)) if isinstance(value, list) else value


def unpack(row):
    result = {i: F(a) for i, a in row}
    assert len(result) == len(row) and all(result.values())
    assert row == [[i, str(a)] for i, a in sorted(result.items())]
    return result


def add(row, index, amount):
    row[index] = row.get(index, F(0)) + amount
    if row[index] == 0:
        del row[index]


packet = json.loads((HERE / "rows_17.json").read_text())
old_path = WORK / "early_x_anchor_queries/rows_51.json"
columns_path = WORK / "early_x_anchor_queries/columns_21021.json.gz"
old = json.loads(old_path.read_text())
columns = json.loads(gzip.decompress(columns_path.read_bytes()))
assert sha256(old_path.read_bytes()).hexdigest() == packet["source_sha256"]["old_rows_51"]
assert sha256(columns_path.read_bytes()).hexdigest() == packet["source_sha256"]["columns_21021"]
assert len(columns) == packet["full_dimension"] == 21021 and packet["new_columns"] == 0
hist, joint, hidden, current, old_mapping = {}, defaultdict(dict), defaultdict(list), None, {}
for j, descriptor in enumerate(columns[:4849]):
    if descriptor["kind"] == "hist":
        current = j
        hist[j] = descriptor
    elif descriptor["kind"] == "joint-reply":
        assert current is not None
        origin = descriptor["hist_column_old"]
        assert old_mapping.setdefault(origin, current) == current
        joint[current, recursive_tuple(descriptor["group"])][tuple(descriptor["state"])] = j
    elif descriptor["kind"] == "actual-B-family-state" and descriptor["source"] == 4:
        hidden[descriptor["hist_column"]].append((j, tuple(descriptor["hidden"])))
assert len(hist) == len(old_mapping) == 16
assert len(joint) == 194 and all(set(states) == {(0, 1), (1, 0), (1, 1)} for states in joint.values())
assert set(hidden) == set(hist) and all(len(states) == 8 for states in hidden.values())
xcolumns = {descriptor["hist_column"]: j for j, descriptor in enumerate(columns) if descriptor["kind"] == "common-X-mass"}
upper_columns = {(descriptor["hist_column"], recursive_tuple(descriptor["query_token"])): j
                 for j, descriptor in enumerate(columns) if descriptor["kind"] == "X-query-overlap-upper"}
assert set(hist) == set(xcolumns) and len(upper_columns) == 420
words = {}
for h, descriptor in hist.items():
    words[h] = [tuple(map(int, f"{word:03b}")) for word, count in enumerate(descriptor["hist"]) for _ in range(count)]
    assert len(words[h]) == 6


def token(h, label):
    kind = label[0]
    if kind == "A":
        return ("bit", int(hist[h]["actual_bits"][label[1]]))
    if kind in ("T", "B", "C"):
        return ("bit", words[h][label[1]][("T", "B", "C").index(kind)])
    if kind == "H":
        return tuple(label)
    assert kind in ("R", "Z")
    _, family, left, right = label
    return (kind, (family, int(left == right), words[h][left], words[h][right]))


def marginal(h, query_token):
    if query_token[0] == "bit":
        return {h: F(1)} if query_token[1] else {}
    if query_token[0] == "H":
        return {j: F(1) for j, state in hidden[h] if state[query_token[1]]}
    axis = int(query_token[0] == "Z")
    return {j: F(1) for state, j in joint[h, query_token[1]].items() if state[axis]}


for (h, query_token), index in upper_columns.items():
    assert marginal(h, query_token) == unpack(columns[index]["query_marginal"])

income, safe, hist_records = {}, {}, []
for h, descriptor in sorted(hist.items()):
    bits = tuple(map(int, descriptor["actual_bits"]))
    b = bits[0] + bits[1]
    income_coefficient = F(1, sum(bits)) if bits[2] else F(0)
    if income_coefficient:
        income[h] = safe[h] = income_coefficient
    safe[xcolumns[h]] = -F(1, b + 4)
    hist_records.append({"hist_column": h, "actual_bits": descriptor["actual_bits"], "b": b,
                         "actual_player3_income_coefficient": str(income_coefficient),
                         "X_column": xcolumns[h], "kappa_X_coefficient": str(F(1, b + 4))})
saved_safe = json.loads((HERE / "safe3_from_actual_bits.json").read_text())
assert safe == unpack(saved_safe["row"]) and hist_records == saved_safe["histograms"]
lift = json.loads((WORK / "terminal_response_cycles/max_b_symbolic_lift.json").read_text())
lift_safe = next(record for record in lift["rows"] if record["name"] == ["actual-safe-X", 3])
mapped_safe = {index if index < 4849 else index + 15736: value for index, value in unpack(lift_safe["row"]).items()}
assert safe == mapped_safe
assert income == unpack(lift["incomes"][2])
zeros = {1, 59, 366, 449, 524, 574}
assert zeros == set(lift["zero_histograms"]) == set(packet["all_zero_histograms_retained"]) <= set(hist)

all_labels = [("A", j) for j in range(6)]
all_labels += [(kind, j) for kind in ("T", "B", "C") for j in range(6)]
nodes = [(family, left, right) for family, left, right in product(range(2), range(6), range(6)) if family or left != right]
all_labels += [(kind, *node) for kind in ("R", "Z") for node in nodes]
all_labels += [("H", j) for j in range(2)]
assert len(set(all_labels)) == len(all_labels) == 158


def move(label, permutation):
    if label[0] in ("A", "H"):
        return label
    if label[0] in ("T", "B", "C"):
        return (label[0], permutation[label[1]])
    return (label[0], label[1], permutation[label[2]], permutation[label[3]])


perms = list(permutations(range(6)))
assert len(packet["rows"]) == 17
seen_labels, upper_used, orbit_records = set(), Counter(), []
direct_checks = 0
for record in packet["rows"]:
    members = list(map(tuple, record["query_members"]))
    assert set(members).issubset(all_labels) and not seen_labels.intersection(members)
    seen_labels.update(members)
    images = Counter(move(members[0], permutation) for permutation in perms)
    assert set(images) == set(members) and set(images.values()) == {720 // len(members)}
    assert record["orbit_size"] == len(members) and record["C"] == "61/3"
    direct = {index: F(61, 3) * value for index, value in income.items()}
    frequencies = []
    for h, descriptor in hist.items():
        b = sum(map(int, descriptor["actual_bits"][:2]))
        add(direct, xcolumns[h], -F(58, 3 * (b + 4)))
        counts = Counter(token(h, label) for label in members)
        images_by_token = Counter()
        for label, count in images.items():
            images_by_token[token(h, label)] += count
        assert images_by_token == {query_token: count * 720 // len(members) for query_token, count in counts.items()}
        frequencies.append({"hist_column": h, "frequencies": [[query_token, count] for query_token, count in sorted(counts.items(), key=repr)]})
        for label in members:
            query_token = token(h, label)
            for index, value in marginal(h, query_token).items():
                add(direct, index, -value / F((b + 1) * len(members)))
            overlap_coefficient = F(3, (b + 1) * (b + 4) * len(members))
            if query_token[0] == "bit":
                if query_token[1]:
                    add(direct, xcolumns[h], overlap_coefficient)
            else:
                add(direct, upper_columns[h, query_token], overlap_coefficient)
            direct_checks += 1
    assert json.loads(json.dumps(frequencies)) == record["histogram_frequencies"]
    assert direct == unpack(record["row"])
    source = old["rows"][record["old_row_index"]]
    assert source["actual_player"] == 3 and source["C"] == "23"
    assert source["query_members"] == record["query_members"]
    transformed = unpack(source["row"])
    for index, value in safe.items():
        add(transformed, index, -F(8, 3) * value)
    assert transformed == direct
    assert all(direct.get(index, 0) < 0 for index in xcolumns.values())
    for index in set(upper_columns.values()).intersection(direct):
        assert direct[index] > 0 and direct[index] == unpack(source["row"])[index]
        upper_used[index] += 1
    orbit_records.append({"orbit_id": record["orbit_id"], "name": record["name"], "orbit_size": len(members),
                          "nonzeros": len(direct), "direct_formula_equals_affine_update": True})
assert seen_labels == set(all_labels)
assert set(upper_used) == set(upper_columns.values()) and set(upper_used.values()) == {1}
assert direct_checks == 16 * 158
assert sum(record["nonzeros"] for record in orbit_records) == packet["nonzero_count"]
for asset in json.loads((HERE / "math_freeze_manifest.json").read_text())["files"]:
    assert sha256((REPO / asset["path"]).read_bytes()).hexdigest() == asset["sha256"]
report = {"status": "PASS", "constructor_imported": False, "optimizer_called": False, "point_weights_read": False,
    "rows": 17, "columns": 21021, "new_columns": 0, "nonzero_count": packet["nonzero_count"],
    "all_16_histograms_retained": True, "all_zero_histograms_retained": sorted(zeros),
    "actual_income_rebuilt_from_raw_bits": True, "SAFE3_rebuilt_from_raw_bits_and_X_columns": True,
    "SAFE3_matches_existing_symbolic_lift": True, "raw_joint_groups": len(joint),
    "all_420_marginals_rebuilt_from_raw_descriptors": True,
    "all_420_upper_variables_used_once_with_unchanged_positive_coefficient": True,
    "direct_new_formula_equals_old_row_minus_8_over_3_SAFE3": True,
    "literal_query_labels": 158, "S6_orbits": 17, "literal_hist_query_checks": direct_checks,
    "S6_representative_hist_image_checks": 16 * 17 * 720,
    "mathematical_certificate_unchanged": True, "old_rows_unchanged": True,
    "scope": "New general lemma interface only; no fixed-point evaluation yet.", "orbits": orbit_records}
(HERE / "interface_verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "orbits"}, indent=2, ensure_ascii=False))
