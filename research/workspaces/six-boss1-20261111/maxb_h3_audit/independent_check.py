#!/usr/bin/env python3
"""Independent Fraction-only audit.  No constructor import, optimizer, or point value.

Inputs are the frozen full matrix, the old symbolic lift, the literal 158-label
catalogue, and the proposed 17 rows.  Outputs stay in this audit directory.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
FILES = {
    "bridge": BASE / "maxb_h3_bridge.md",
    "proposed_rows": BASE / "maxb_h3_bridge/rows_17.json",
    "matrix": BASE / "maxb_augmented_lp/full_lift/exact_matrix.json.gz",
    "lift": BASE / "terminal_response_cycles/max_b_symbolic_lift.json",
    "labels": BASE / "actual_pair_20910/labels_and_orbits.json",
    "bridge_orbit_source": BASE / "terminal_response_cycles/max_b_preflight.json",
}


def digest(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def frozen(a):
    return tuple(map(frozen, a)) if isinstance(a, list) else a


def sparse(a):
    assert len({i for i, _ in a}) == len(a), "duplicate sparse column"
    r = {i: F(v) for i, v in a}
    assert all(r.values()), "stored zero sparse coefficient"
    return r


def serialized(r):
    return [[i, str(v)] for i, v in sorted(r.items()) if v]


def add(r, s, scale=F(1)):
    for i, v in s.items():
        r[i] += scale * v


class Stream:
    """Read a single JSON value at a time, keeping the matrix rows out of memory."""
    def __init__(self, file):
        self.file, self.buf, self.pos = file, "", 0
        self.decoder = json.JSONDecoder()

    def fill(self):
        self.buf = self.buf[self.pos:] + self.file.read(131072)
        self.pos = 0

    def peek(self):
        while True:
            while self.pos < len(self.buf) and self.buf[self.pos].isspace():
                self.pos += 1
            if self.pos < len(self.buf):
                return self.buf[self.pos]
            self.fill()
            assert self.buf, "unexpected JSON end"

    def take(self, symbol):
        assert self.peek() == symbol, (symbol, self.buf[self.pos:self.pos+50])
        self.pos += 1

    def value(self):
        self.peek()
        while True:
            try:
                obj, end = self.decoder.raw_decode(self.buf, self.pos)
                self.pos = end
                return obj
            except json.JSONDecodeError:
                old = len(self.buf) - self.pos
                self.fill()
                assert len(self.buf) > old, "incomplete JSON value"


hashes_before = {k: digest(p) for k, p in FILES.items()}
proposed = json.loads(FILES["proposed_rows"].read_text())
lift = json.loads(FILES["lift"].read_text())
catalogue = json.loads(FILES["labels"].read_text())
assert proposed["input_sha256"]["lift"] == hashes_before["lift"]
assert proposed["input_sha256"]["orbits"] == hashes_before["bridge_orbit_source"]
assert proposed["input_sha256"]["descriptor_container"] == lift["point_sha256"]
assert proposed["fixed_point_evaluated"] is False
assert proposed["optimizer_called"] is False

# Atom arithmetic is reconstructed directly from the four budget definitions.
atoms = []
zero_by_xyz = Counter()
for b, a, x, y, z, q in product(range(4), *([range(2)] * 5)):
    n = b + 1
    target_without_u = -F(9*x, n+2) - F(q*x, n+2) - F(q*(1-x), n)
    budgets_without_u = -F(10*x, n+y+z) + F(x-y, n+a) + F(2*(x-z), n+a) + F(z-q, n+x+y)
    residual = target_without_u - budgets_without_u
    forms = {
        (0, 0, 0): F(0),
        (0, 0, 1): F(2, n+a) - F(1, n),
        (0, 1, 0): F(1, n+a) - F(q, n*(n+1)),
        (0, 1, 1): F(3, n+a) - F(1, n+1) - F(q, n*(n+1)),
        (1, 0, 0): F(10, n) - F(9, n+2) - F(3, n+a) + F(q, (n+1)*(n+2)),
        (1, 0, 1): F(9+q, (n+1)*(n+2)) - F(1, n+a),
        (1, 1, 0): F(10, n+1) - F(9, n+2) - F(2, n+a),
        (1, 1, 1): F(0),
    }
    assert residual == forms[x, y, z] >= 0
    if not residual:
        zero_by_xyz[x, y, z] += 1
    atoms.append({"b": b, "a": a, "x": x, "y": y, "z": z, "q": q, "E": str(residual)})
assert len(atoms) == 128 and sum(zero_by_xyz.values()) == 39

# General certificate residual has affine coordinates [constant,C,alpha,beta,gamma].
def affine_atom(b, a, x, y, z, q):
    n = b+1
    return [F(x, n+2)-F(q*x, n+2)-F(q*(1-x), n),
            F(x, n+y+z)-F(x, n+2),
            -F(x-y, n+a), -F(x-z, n+a), -F(z-q, n+x+y)]


lower_bound_atoms = [
    ((0, 0, 0, 0, 0, 1), [F(-1), F(0), F(0), F(0), F(1)]),
    ((0, 1, 0, 0, 1, 0), [F(0), F(0), F(0), F(1, 2), F(-1)]),
    ((0, 0, 1, 1, 0, 0), [F(1, 3), F(1, 6), F(0), F(-1), F(0)]),
]
for atom, expected in lower_bound_atoms:
    assert affine_atom(*atom) == expected
# Elimination weights (12,12,6) cancel beta and gamma and give C-10.
assert [sum(w*v[i] for w, (_, v) in zip((12, 12, 6), lower_bound_atoms)) for i in range(5)] == [F(-10), F(1), F(0), F(0), F(0)]

# Supplementary TP decomposition, including its self-tax and both real terminal ICs.
tp_checks = 0
for m, y, z, q, r, j in product(range(5), *([range(2)]*5)):
    def U(t, s):
        return F(t, m+1) - F(t*s, (m+1)*(m+2))
    def g(t, s):
        return F(t*s, (m+1)*(m+2))
    s, t = U(y, z), U(z, y)
    lhs = s+t+g(y,y)-F(q+r,m+1)+g(q,r)
    rhs = (s-U(q,j))+(U(j,q)-U(r,q))+(t-U(j,y))+g(y,y)-g(y,j)
    assert lhs == rhs and g(y,y)-g(y,j) >= 0
    tp_checks += 1

# Read every frozen matrix row, compare all 1387 remapped lift rows, and audit
# every old/new occurrence of the 420 min variables.  No matrix/point product.
full_metadata = {}
matrix_row_count = 0
negative_usage = Counter()
positive_usage = Counter()
with gzip.open(FILES["matrix"], "rt") as file:
    stream = Stream(file)
    stream.take("{")
    while stream.peek() != "}":
        key = stream.value()
        stream.take(":")
        if key == "columns":
            columns = stream.value()
            assert len(columns) == 21021
            assert columns[20585:] == lift["new_columns"]
            overlap_indices = {i for i, d in enumerate(columns) if d["kind"] == "X-query-overlap-upper"}
            assert len(overlap_indices) == 420
        elif key == "row_names":
            matrix_names = stream.value()
        elif key == "rows":
            stream.take("[")
            while stream.peek() != "]":
                row = sparse(stream.value())
                index = matrix_row_count
                if index >= 20910:
                    original = sparse(lift["rows"][index-20910]["row"])
                    mapped = {i if i < 4849 else i+15736: v for i, v in original.items()}
                    assert row == mapped, ("full lift row mismatch", index)
                for i in overlap_indices.intersection(row):
                    assert index >= 20910, "new min variable leaked into baseline"
                    if row[i] < 0:
                        negative_usage[i] += 1
                        assert lift["rows"][index-20910]["name"][0] in ("overlap-at-most-X", "overlap-at-most-query")
                        assert row[i] == -1
                    else:
                        positive_usage[i] += 1
                matrix_row_count += 1
                if stream.peek() == ",":
                    stream.take(",")
            stream.take("]")
        else:
            full_metadata[key] = stream.value()
        if stream.peek() == ",":
            stream.take(",")
    stream.take("}")
assert matrix_row_count == len(matrix_names) == 22297
assert all(negative_usage[i] == 2 for i in overlap_indices)
assert full_metadata["all_columns_nonnegative"] is True
assert full_metadata["baseline_rows"] == 20910
assert full_metadata["maxb_lift_sha256"] == hashes_before["lift"]

# Hist ownership is read from the actual descriptor block boundaries.  The old
# hist_column_old field is checked as a bijection, never used as a current index.
hist = {}
old_to_current = {}
joint = defaultdict(dict)
b4 = defaultdict(list)
current_hist = None
for i, d in enumerate(columns[:4849]):
    if d["kind"] == "hist":
        current_hist = i
        hist[i] = d
    elif d["kind"] == "joint-reply":
        old = d["hist_column_old"]
        assert old_to_current.setdefault(old, current_hist) == current_hist
        joint[current_hist, frozen(d["group"])][tuple(d["state"])] = i
    elif d["kind"] == "actual-B-family-state" and d["source"] == 4:
        b4[d["hist_column"]].append((i, tuple(d["hidden"]), d["ell"]))
assert len(hist) == len(old_to_current) == len(set(old_to_current.values())) == 16
assert len(joint) == 194 and all(set(v) == {(0,1),(1,0),(1,1)} for v in joint.values())
assert set(b4) == set(hist) and all(len(v) == 8 for v in b4.values())
x_column = {d["hist_column"]: i for i, d in enumerate(columns) if d["kind"] == "common-X-mass"}
upper = {(columns[i]["hist_column"], frozen(columns[i]["query_token"])): i for i in overlap_indices}
assert len(upper) == 420 and set(x_column) == set(hist)


def marginal(h, token):
    if token[0] == "bit":
        return {h: F(1)} if token[1] else {}
    if token[0] in ("R", "Z"):
        axis = 0 if token[0] == "R" else 1
        return {i: F(1) for state, i in joint[h, token[1]].items() if state[axis]}
    assert token[0] == "H"
    return {i: F(1) for i, hidden, ell in b4[h] if hidden[token[1]]}


lift_rows = {frozen(r["name"]): sparse(r["row"]) for r in lift["rows"]}
for (h, token), full_i in upper.items():
    rebuilt = marginal(h, token)
    assert rebuilt == sparse(columns[full_i]["query_marginal"])
    compressed_i = full_i - 15736
    compressed_x = x_column[h] - 15736
    assert lift_rows["overlap-at-most-X", compressed_i] == {compressed_x:F(1), compressed_i:F(-1)}
    expected = dict(rebuilt)
    expected[compressed_i] = F(-1)
    assert lift_rows["overlap-at-most-query", compressed_i] == expected
for h in hist:
    assert lift_rows["X-at-most-hist", h] == {h:F(1), x_column[h]-15736:F(-1)}

# Rebuild the 158 literal labels from their original data, then derive their
# 17 orbits by all 720 S6 permutations (without reading any saved orbit table).
def literal(d):
    if "actual_position" in d:
        return ("A", d["actual_position"])
    if d["kind"] in ("T", "B", "C"):
        assert d["word_slot"] == ("T", "B", "C").index(d["kind"])
        return (d["kind"], *d["indices"])
    if "own_coordinate" in d:
        kind = "R" if d["own_coordinate"] == 0 else "Z"
        assert d["node"] == [d["family"], *d["indices"]]
        return (kind, d["family"], *d["indices"])
    return ("H", d["B4_coordinate"])


labels = [literal(d) for d in catalogue["labels"]]
assert len(labels) == len(set(labels)) == 158
assert Counter(t[0] for t in labels) == {"A":6,"T":6,"B":6,"C":6,"R":66,"Z":66,"H":2}
assert not any(t[0] in ("R","Z") and t[1] == 0 and t[2] == t[3] for t in labels)
perms = list(permutations(range(6)))


def moved(label, pi):
    kind = label[0]
    if kind in ("A", "H"):
        return label
    if kind in ("T", "B", "C"):
        return (kind, pi[label[1]])
    return (kind, label[1], pi[label[2]], pi[label[3]])


remaining = set(labels)
orbits = []
for label in labels:
    if label not in remaining:
        continue
    images = Counter(moved(label, pi) for pi in perms)
    assert set(images) <= remaining
    assert all(n == 720//len(images) for n in images.values())
    orbit = sorted(images)
    orbits.append((label, orbit, images))
    remaining -= set(images)
assert not remaining and len(orbits) == 17

words = {}
for h, d in hist.items():
    assert sum(d["hist"]) == 6
    words[h] = [tuple(map(int, f"{k:03b}")) for k, count in enumerate(d["hist"]) for _ in range(count)]


def token_of(h, label):
    kind = label[0]
    if kind == "A":
        return ("bit", int(hist[h]["actual_bits"][label[1]]))
    if kind in ("T", "B", "C"):
        return ("bit", words[h][label[1]][("T", "B", "C").index(kind)])
    if kind == "H":
        return label
    _, family, i, j = label
    return (kind, (family, int(i == j), words[h][i], words[h][j]))


proposed_by_members = {frozenset(map(tuple, r["query_members"])): r for r in proposed["rows"]}
assert len(proposed_by_members) == 17
rebuilt_rows = []
new_overlap_usage = Counter()
frequency_checks = 0
literal_hist_queries = 0
zero_hist = set(lift["zero_histograms"])
assert zero_hist == {1,59,366,449,524,574} <= set(hist)
zero_hist_row_counts = Counter()
for representative, orbit, images in orbits:
    proposed_row = proposed_by_members[frozenset(orbit)]
    assert proposed_row["orbit_size"] == len(orbit)
    expected_name = ["common-X-H3-bridge", representative[0]]
    if representative[0] in ("A", "H"):
        expected_name.append(representative[1])
    elif representative[0] in ("R", "Z"):
        expected_name += [representative[1], int(representative[2] == representative[3])]
    assert proposed_row["name"] == expected_name
    stored_freqs = {d["hist_column"]: {frozen(t):n for t,n in d["frequencies"]} for d in proposed_row["histogram_frequencies"]}
    assert set(stored_freqs) == set(hist)
    row = defaultdict(F)
    frequencies = []
    for h, d in hist.items():
        bits = tuple(map(int, d["actual_bits"]))
        b, a = sum(bits[:3]), bits[3]
        if a:
            row[h] += F(10, sum(bits))
        row[x_column[h]] -= F(9, b+3)
        counts = Counter(token_of(h, label) for label in orbit)
        literal_hist_queries += len(orbit)
        assert counts == stored_freqs[h], ("hist frequency", h, representative)
        projected_images = Counter()
        for label, multiplicity in images.items():
            projected_images[token_of(h, label)] += multiplicity
        assert projected_images == {t: n*720//len(orbit) for t,n in counts.items()}
        frequency_checks += 720
        for token, count in counts.items():
            weight = F(count, len(orbit))
            add(row, marginal(h, token), -weight/F(b+1))
            if token[0] == "bit":
                if token[1]:
                    row[x_column[h]] += weight*F(2, (b+1)*(b+3))
            else:
                row[upper[h,token]] += weight*F(2, (b+1)*(b+3))
        frequencies.append({"hist_column":h, "frequencies":[[t,n] for t,n in sorted(counts.items(), key=repr)]})
        if h in zero_hist:
            zero_hist_row_counts[h] += 1
    row = {i:v for i,v in row.items() if v}
    assert proposed_row["rhs"] == "0"
    assert row == sparse(proposed_row["row"]), ("row coefficient mismatch", representative)
    assert all(i < 21021 for i in row)
    assert all(row[x_column[h]] < 0 for h in hist)
    for i in overlap_indices.intersection(row):
        assert row[i] > 0
        new_overlap_usage[i] += 1
    rebuilt_rows.append({"name":expected_name,"orbit_size":len(orbit),"row":serialized(row),"rhs":"0","histogram_frequencies":frequencies})
assert literal_hist_queries == 2528 and frequency_checks == 195840
assert set(new_overlap_usage) == overlap_indices and all(v == 1 for v in new_overlap_usage.values())
assert all(zero_hist_row_counts[h] == 17 for h in zero_hist)
assert sum(len(r["row"]) for r in rebuilt_rows) == proposed["nonzero_count"] == 1731
assert proposed["new_columns"] == 0 and proposed["full_dimension"] == 21021
assert proposed["reuses_existing_X_columns"] == sorted(x_column.values())

hashes_after = {k:digest(p) for k,p in FILES.items()}
assert hashes_before == hashes_after, "an input changed during independent audit"
report = {
    "status":"PASS",
    "scope":"Independent full-type proof arithmetic and exact 17-row interface audit; no optimization or fixed-point evaluation.",
    "input_sha256":hashes_before,
    "matrix_rows":matrix_row_count,
    "matrix_columns":len(columns),
    "matrix_lift_rows_matched_exactly":1387,
    "atom_cases":len(atoms),
    "zero_atom_cases":sum(zero_by_xyz.values()),
    "positive_atom_cases":sum(F(t["E"]) > 0 for t in atoms),
    "minimum_positive_residual":str(min(F(t["E"]) for t in atoms if F(t["E"]) > 0)),
    "zeros_by_xyz":{str(k):v for k,v in sorted(zero_by_xyz.items())},
    "certificate_family_C_lower_bound":"10; weights (12,12,6) of the three atom conditions give C-10 >= 0",
    "true_SPE_sharpness_claimed":False,
    "supplementary_TP_identity_cases":tp_checks,
    "literal_label_count":len(labels),
    "single_label_orbit_count":len(orbits),
    "literal_hist_query_count":literal_hist_queries,
    "S6_hist_representative_frequency_checks":frequency_checks,
    "own_descriptor_groups":len(joint),
    "X_columns":sorted(x_column.values()),
    "overlap_upper_columns":len(overlap_indices),
    "all_420_marginals_rebuilt_from_raw_descriptors":True,
    "all_840_min_upper_bounds_matched":True,
    "negative_occurrences_in_existing_matrix":"exactly the two expected upper bounds per min variable",
    "all_other_existing_occurrences_nonnegative":True,
    "all_new_overlap_coefficients_strictly_positive":True,
    "new_overlap_occurrences":sum(new_overlap_usage.values()),
    "zero_histograms_retained_in_each_of_17_rows":sorted(zero_hist),
    "zero_histogram_X_bounds_retained":True,
    "rows_rebuilt":len(rebuilt_rows),
    "nonzero_coefficients_rebuilt":sum(len(r["row"]) for r in rebuilt_rows),
    "new_columns":0,
    "imported_constructors":False,
    "optimizer_called":False,
    "point_weights_read":False,
    "fixed_point_evaluated":False,
    "frozen_inputs_unchanged_during_audit":True,
}
for name, data in [("audit_result.json",report),("atoms_128.json",atoms),("independent_rows_17.json",rebuilt_rows)]:
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(report,ensure_ascii=False,indent=2))
