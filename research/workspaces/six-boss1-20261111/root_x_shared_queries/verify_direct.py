#!/usr/bin/env python3
"""Independent exact audit of the shared-X 42-row append interface.

Only standard-library modules are used.  The row builder is never imported.
Only descriptors/equalities are taken from the previous symbolic root matrix;
no previous point file, point weights, optimizer, or solver is accessed.
Direct coefficients are reconstructed by evaluating literal residuals at X=0
and X=1, then taking their exact affine difference.  This differs from the
builder's expanded coefficient construction.

This program writes exactly direct_verification.json next to this script.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import gzip
import json


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
INTERFACE = HERE / "direct_interface_exact.json.gz"
OWN = BASE / "root_x_joint_contract/own_blocks.json"
ROOT = BASE / "root_sorting_20910/symbolic_matrix_exact.json.gz"
OUT = HERE / "direct_verification.json"
PARTS = ("old", "mu", "eta")


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def bits(value, width=5):
    return tuple(int(x) for x in format(value, "0%db" % width))


def fraction(value):
    assert isinstance(value, str), ("coefficient must be an exact string", value)
    result = F(value)
    assert str(result) == value, ("coefficient is not canonical", value)
    return result


def sparse(row):
    result = {}
    for part in PARTS:
        entries = row.get(part, [])
        ids = [item[0] for item in entries]
        assert ids == sorted(set(ids)), ("noncanonical sparse indices", row.get("name"), part)
        for index, value in entries:
            assert isinstance(index, int) and index >= 0
            assert index < (21021 if part == "old" else 1216)
            q = fraction(value)
            assert q, ("explicit sparse zero", row.get("name"), part, index)
            result[part, index] = q
    return result


def cleaned(row):
    return {key: value for key, value in row.items() if value}


def share(member, load):
    return F(member, load) if member else F()


def pair_price(background, first, second):
    """Literal union/intersection price, including equal/repeated queries."""
    return F(first | second, background + 1) + F(first & second, background + 2)


def row_names():
    names = [("RX", k) for k in range(1, 6)]
    names += [("RPQ", q) for q in range(6)] + [("RXX",)]
    names += [("XM", k) for k in range(1, 6)]
    names += [("XC", k) for k in range(1, 6)]
    names += [("RC-SAME", l, m) for l, m in combinations_with_replacement(range(6), 2)
              if (l, m) != (0, 0)]
    assert len(names) == 42 and len(set(names)) == 42
    return names


def literal_residual(name, actual, t, e, z):
    """One-customer true payoff/PAIR expression before affine expansion."""
    kind = name[0]
    N = t + sum(e)
    P = sum(actual[:4])
    a = share(actual[4], sum(actual))
    C = F(z, P + 1)
    if kind == "RX":
        k = name[1] - 1
        prefix = t + sum(e[:k])
        remaining_after_query = 4 - k
        return share(e[k], N) - F(z, prefix + 1 + remaining_after_query)
    if kind in ("RPQ", "RXX"):
        p = t + sum(e[:3])
        wallet = F(e[3], p + 1 + e[4]) + F(e[4], p + 1 + e[3])
        wallet += F(e[3], (p + 1) * (p + 2))
        query = z if kind == "RXX" else ((t,) + e)[name[1]]
        return wallet - pair_price(p, z, query)
    if kind == "XM":
        return C - F(e[name[1] - 1], P + 1)
    if kind == "XC":
        return a + C - pair_price(P, z, e[name[1] - 1])
    assert kind == "RC-SAME"
    v = (t,) + e
    return a + C - pair_price(P, v[name[1]], v[name[2]])


def old_wallet(name, actual, z):
    """The actual-source terms retained in original coordinates."""
    P = sum(actual[:4])
    value = F()
    if name[0] in ("XC", "RC-SAME"):
        value += share(actual[4], sum(actual))
    if name[0] in ("XM", "RC-SAME"):
        value += F(z, P + 1)
    return value


def verify_direct_rows(data, hist, xmap, lookup):
    expected = {name: defaultdict(F) for name in row_names()}
    literal_checks = Counter()
    for h, desc in hist.items():
        actual = tuple(map(int, desc["actual_bits"]))
        P = sum(actual[:4])
        a = share(actual[4], sum(actual))
        for name, row in expected.items():
            if name[0] in ("XC", "RC-SAME"):
                row["old", h] += a
            if name[0] in ("XM", "RC-SAME"):
                row["old", xmap[h]] += F(1, P + 1)
        for w, multiplicity in enumerate(desc["hist"]):
            if not multiplicity:
                continue
            t, factor = w >> 2, F(multiplicity, 6)
            for state in range(32):
                e = bits(state)
                j = lookup[h, w, state]
                for name, row in expected.items():
                    local = [literal_residual(name, actual, t, e, z) - old_wallet(name, actual, z)
                             for z in (0, 1)]
                    mu_coefficient = local[0]
                    eta_coefficient = local[1] - local[0]
                    row["mu", j] += factor * mu_coefficient
                    row["eta", j] += factor * eta_coefficient
                    for z in (0, 1):
                        assert (old_wallet(name, actual, z) + mu_coefficient + z * eta_coefficient
                                == literal_residual(name, actual, t, e, z))
                        literal_checks[name[0]] += 1
    actual_rows = {tuple(row["name"]): row for row in data["rows"]}
    assert len(actual_rows) == len(data["rows"]) == 42
    assert set(actual_rows) == set(expected)
    coefficient_checks = 0
    for name, row in expected.items():
        want, got = cleaned(row), sparse(actual_rows[name])
        assert want == got, ("direct row coefficient mismatch", name,
                             sorted(set(want.items()) ^ set(got.items()))[:8])
        coefficient_checks += len(want)
    assert sum(literal_checks.values()) == 102144
    return {"row_count": 42, "assembled_nonzero_coefficients_checked": coefficient_checks,
            "literal_affine_identities": dict(literal_checks),
            "literal_affine_identity_count": sum(literal_checks.values())}


def verify_mass_contract(data, root, hist, xmap, lookup):
    # The underlying mu mass equations are independently checked by content.
    expected_mu = {}
    expected_eta = {}
    for h, desc in hist.items():
        for w, n in enumerate(desc["hist"]):
            if not n:
                continue
            expected_mu[h, w] = {("old", h): F(-1)}
            expected_eta[h, w] = {("old", xmap[h]): F(-1)}
            for state in range(32):
                j = lookup[h, w, state]
                expected_mu[h, w]["mu", j] = F(1)
                expected_eta[h, w]["eta", j] = F(1)
    assert len(expected_mu) == len(expected_eta) == 38
    mu_actual = {tuple(row["name"])[1:]: sparse(row) for row in root["equalities"]
                 if row["name"][0] == "mass"}
    assert mu_actual == expected_mu
    eta_actual = [sparse(row) for row in data["eta_equalities"]]
    assert len(eta_actual) == 38
    encode = lambda row: tuple(sorted(row.items()))
    assert Counter(map(encode, eta_actual)) == Counter(map(encode, expected_eta.values()))
    upper_actual = [sparse(row) for row in data["eta_upper_rows"]]
    upper_expected = [{("mu", j): F(1), ("eta", j): F(-1)} for j in range(1216)]
    assert len(upper_actual) == 1216
    assert Counter(map(encode, upper_actual)) == Counter(map(encode, upper_expected))

    # Ambient lower bounds must be declared, rather than inferred from a name.
    declared = data.get("nonnegative_variables")
    if isinstance(declared, dict):
        eta_decl = declared.get("eta")
        assert eta_decl == "all" or eta_decl is True or eta_decl == list(range(1216)), declared
    elif isinstance(declared, list):
        assert any(item in ("eta", "all eta", "all eta; mu inherited") for item in declared), declared
    else:
        raise AssertionError("missing explicit eta nonnegativity declaration")

    # All hist X bounds follow symbolically from each group's two mass maps.
    # eta >= 0 sums to x; (mu-eta) >= 0 sums to H-x.  This simultaneously
    # checks the per-word normalization and covers x=0,H and zero hist mass.
    implied_bound_checks = 0
    for (h, w), eta_eq in expected_eta.items():
        mu_eq = expected_mu[h, w]
        lower_sum = defaultdict(F)
        upper_sum = defaultdict(F)
        for state in range(32):
            j = lookup[h, w, state]
            lower_sum["eta", j] += 1
            upper_sum["mu", j] += 1
            upper_sum["eta", j] -= 1
        for key, value in eta_eq.items():
            lower_sum[key] -= value
            upper_sum[key] += value
        for key, value in mu_eq.items():
            upper_sum[key] -= value
        assert cleaned(lower_sum) == {("old", xmap[h]): F(1)}
        assert cleaned(upper_sum) == {("old", h): F(1), ("old", xmap[h]): F(-1)}
        implied_bound_checks += 2

    explicit_bound_count = 0
    if "hist_x_bounds" in data:
        bound_rows = data["hist_x_bounds"]
        if isinstance(bound_rows, dict):
            bound_rows = list(bound_rows.values())
        bounds = [sparse(row) for row in bound_rows]
        wanted = [{("old", xmap[h]): F(1)} for h in hist]
        wanted += [{("old", h): F(1), ("old", xmap[h]): F(-1)} for h in hist]
        assert Counter(map(encode, bounds)) == Counter(map(encode, wanted))
        explicit_bound_count = len(bounds)
    return {"eta_upper_rows": 1216, "eta_mass_equalities": 38,
            "inherited_mu_mass_equalities": 38, "eta_nonnegative_coordinates": 1216,
            "implied_hist_x_bound_identities": implied_bound_checks,
            "explicit_hist_x_bound_rows_checked": explicit_bound_count}


def rename(expr, names):
    kind = expr[0]
    if kind in ("A", "H", "X"):
        return expr
    if kind in ("T", "B", "C"):
        return kind, names.setdefault(expr[1], len(names))
    if kind == "Y":
        return kind, names.setdefault(expr[1], len(names)), expr[2]
    return (kind, expr[1], names.setdefault(expr[2], len(names)),
            names.setdefault(expr[3], len(names)))


def pair_canonical(a, b):
    names = {}
    return rename(a, names), rename(b, names)


def verify_orbits(hist):
    old = [("A", i) for i in range(6)]
    old += [(kind, i) for kind in ("T", "B", "C") for i in range(6)]
    old += [(kind, f, i, j) for kind in ("R", "Z") for f in range(2)
            for i in range(6) for j in range(6) if f or i != j]
    old += [("H", i) for i in range(2)]
    new = [("Y", i, k) for i in range(6) for k in range(5)]
    catalog = old + [("X",)] + new
    assert len(old) == 158 and len(catalog) == 189
    legacy = {pair_canonical(a, b) for a in old for b in old}
    ordered = Counter(pair_canonical(a, b) for a in catalog for b in catalog
                      if a[0] == "Y" or b[0] == "Y")
    unordered = Counter(min(pair_canonical(a, b), pair_canonical(b, a))
                        for i, a in enumerate(catalog) for b in catalog[i:]
                        if a[0] == "Y" or b[0] == "Y")
    root_pair = Counter()
    for i in range(6):
        for expr in catalog:
            root_pair[rename(expr, {i: 0})] += 1
    assert len(legacy) == 490
    assert len(ordered) == 360 and sum(ordered.values()) == 10440
    assert len(unordered) == 185 and sum(unordered.values()) == 5235
    assert len(root_pair) == 41 and sum(root_pair.values()) == 1134
    assert Counter(ordered.values()) == {6: 165, 30: 155, 120: 40}
    assert Counter(unordered.values()) == {6: 85, 15: 5, 30: 75, 120: 20}
    assert Counter(root_pair.values()) == {6: 19, 30: 18, 120: 4}

    pair_count_checks = 0
    permutation_checks = 0
    for h, desc in hist.items():
        words = [w for w, n in enumerate(desc["hist"]) for _ in range(n)]
        same = Counter((words[i], words[i]) for i in range(6))
        off = Counter((words[i], words[j]) for i in range(6) for j in range(6) if i != j)
        for w, v in product(range(8), repeat=2):
            assert same[w, v] == desc["hist"][w] * int(w == v)
            assert off[w, v] == desc["hist"][w] * (desc["hist"][v] - int(w == v))
            pair_count_checks += 2
        # A deliberately nonconstant root-state assignment is carried with its
        # root index, while X is kept unindexed under all 720 permutations.
        root_states = tuple((7 * i + w) % 32 for i, w in enumerate(words))
        word_images = Counter()
        endpoint_images = Counter()
        for perm in permutations(range(6)):
            image = tuple(words[perm[i]] for i in range(6))
            word_images[image] += 1
            for z in (0, 1):
                endpoint_images[z, words[perm[0]], root_states[perm[0]]] += 1
                permutation_checks += 1
        assert len(set(word_images.values())) == 1
        for z in (0, 1):
            for w in range(8):
                for state in range(32):
                    count = sum(words[i] == w and root_states[i] == state for i in range(6))
                    assert endpoint_images[z, w, state] == 120 * count
    assert pair_count_checks == 2048 and permutation_checks == 23040
    return {"old_label_count": 158, "extended_label_count": 189,
            "old_ordered_pair_orbits": 490,
            "new_ordered_pair_literals": 10440, "new_ordered_pair_orbits": 360,
            "new_unordered_pair_literals": 5235, "new_unordered_pair_orbits": 185,
            "root_X_pair_orbits": 41,
            "ordered_orbit_size_distribution": dict(Counter(ordered.values())),
            "unordered_orbit_size_distribution": dict(Counter(unordered.values())),
            "root_X_pair_orbit_size_distribution": dict(Counter(root_pair.values())),
            "same_off_frequency_checks": pair_count_checks,
            "S6_images_with_X_held_fixed": permutation_checks}


def verify_true_source_kernel():
    count = 0
    for p in range(5):
        D = (p + 1) * (p + 2)
        pay = lambda a, b: F(a, p + 1 + b)
        tax = lambda a, b: F(a * b, D)
        for A, B, X, Q, R in product((0, 1), repeat=5):
            first = pay(A, B) - pay(X, R)
            second = pay(R, X) - pay(Q, X)
            third = pay(B, A) - pay(R, A)
            remainder = tax(A, A) - tax(A, R)
            target = pay(A, B) + pay(B, A) + tax(A, A) - pair_price(p, X, Q)
            assert first + second + third + remainder == target and remainder >= 0
            count += 1
    assert count == 160
    safe_count = 0
    for t in (0, 1):
        for e in product((0, 1), repeat=5):
            for k in range(5):
                prefix = t + sum(e[:k])
                for after in product((0, 1), repeat=4 - k):
                    assert F(1, prefix + 1 + sum(after)) >= F(1, prefix + 5 - k)
                    safe_count += 1
    assert safe_count == 1984
    return {"three_true_IC_PAIR_identities": count,
            "SAFE_prices_against_every_off_path_suffix": safe_count}


def verify_gluing(hist):
    cases = 0
    recovered_marginals = 0
    positive_atom_checks = 0
    for h, desc in hist.items():
        words = tuple(w for w, n in enumerate(desc["hist"]) for _ in range(n))
        occupied = sorted(set(words))
        for H, x in ((F(0), F(0)), (F(1), F(0)), (F(1), F(1, 3)), (F(1), F(1))):
            target_mu, target_eta = defaultdict(F), defaultdict(F)
            recovered_mu, recovered_eta = defaultdict(F), defaultdict(F)
            z_totals = defaultdict(F)
            for z in (0, 1):
                Hz = x if z else H - x
                probabilities = {w: F(w + 1 + z, w + 4) for w in occupied}
                for w in occupied:
                    for selected in (0, 1):
                        state = (w + 1) if selected else 0
                        nu = Hz * (probabilities[w] if selected else 1 - probabilities[w])
                        target_mu[w, state] += nu
                        if z:
                            target_eta[w, state] += nu
                # Two arbitrary old-hidden states sharing exactly the same
                # (U,z) mass. Their distribution can depend on the whole U,z.
                old_probability = F(1 + (sum((i + 1) * w for i, w in enumerate(words)) + z) % 5, 7)
                old_masses = (Hz * old_probability, Hz * (1 - old_probability))
                recovered_old = [F(), F()]
                for selected_roots in product((0, 1), repeat=6):
                    probability = F(1)
                    for w, selected in zip(words, selected_roots):
                        probability *= probabilities[w] if selected else 1 - probabilities[w]
                    root_mass = Hz * probability
                    glued = [old_mass * root_mass / Hz if Hz else F() for old_mass in old_masses]
                    assert sum(glued) == root_mass
                    for i, value in enumerate(glued):
                        recovered_old[i] += value
                    z_totals[z] += root_mass
                    for w, selected in zip(words, selected_roots):
                        state = (w + 1) if selected else 0
                        recovered_mu[w, state] += root_mass / desc["hist"][w]
                        if z:
                            recovered_eta[w, state] += root_mass / desc["hist"][w]
                    positive_atom_checks += int(bool(Hz))
                assert recovered_old == list(old_masses)
            assert z_totals[0] == H - x and z_totals[1] == x
            for w in occupied:
                assert sum(target_mu[w, state] for state in range(32)) == H
                assert sum(target_eta[w, state] for state in range(32)) == x
                for state in range(32):
                    assert 0 <= target_eta[w, state] <= target_mu[w, state]
                    assert recovered_mu[w, state] == target_mu[w, state]
                    assert recovered_eta[w, state] == target_eta[w, state]
                    recovered_marginals += 2
            cases += 1
    assert cases == 64
    return {"root_and_old_gluing_cases": cases,
            "exact_root_marginals_recovered": recovered_marginals,
            "positive_root_atom_gluing_identities": positive_atom_checks,
            "boundary_cases": ["H=0", "x=0", "0<x<H", "x=H"],
            "scope": "Preserves supplied laws only when full (h,U,X) marginals agree; does not certify all cross-query transports."}


def verify_local_global_gaps():
    # Two separate local own blocks pass. The fixed old law additionally says
    # Q1 and Q2 partition the population, making their requested X overlaps
    # impossible to realize simultaneously.
    m00, m10, m01, m11 = F(1, 2), F(1, 2), F(0), F(0)
    x, yQ, yR = F(1, 2), F(1, 2), F(0)
    lower = max(F(0), yQ - m10, yR - m01, yQ + yR - x)
    upper = min(m11, yQ, yR, m00 - x + yQ + yR)
    facets = [yQ + yR - x + m00, m10 - yQ + yR, m01 + yQ - yR,
              m00 + m10 - x + yR, m00 + m01 - x + yQ, x + m11 - yQ - yR]
    assert lower == upper == 0 and all(value >= 0 for value in facets)
    requested_overlap_sum = 2 * yQ
    assert requested_overlap_sum - x == F(1, 2)
    # Each signed-query requirement is feasible alone but not with shared eta.
    assert F(3, 8) <= F(1, 2)
    assert 2 * F(3, 8) - F(1, 2) == F(1, 4)
    # Weighted group averaging cannot replace a per-word eta mass map.
    assert F(1, 6) * 1 + F(5, 6) * F(2, 5) == F(1, 2)
    assert F(1) != F(1, 2) and F(2, 5) != F(1, 2)
    return {"own_local_tables_pass": 2,
            "own_facets": list(map(str, facets)),
            "fixed_old_partition_global_obstruction": "1/2",
            "independent_eta_query_envelope_obstruction": "1/4",
            "weighted_only_eta_mass_counterexample_checked": True}


def main():
    data, own, root = map(read_json, (INTERFACE, OWN, ROOT))
    hist = dict(own["hist_records"])
    assert len(hist) == 16 and data["hist_records"] == own["hist_records"]
    assert all("weight" not in desc for desc in root["original_columns"])
    for h, desc in hist.items():
        assert root["original_columns"][h] == desc
        assert sum(desc["hist"]) == 6
    xmap = {}
    for block in own["blocks"]:
        h, x = block["H_column"], block["X_column"]
        assert xmap.setdefault(h, x) == x
    assert set(xmap) == set(hist) and sorted(xmap.values()) == list(range(20585, 20601))
    expected_columns = [dict(hist=h, old_word=w, state=s)
                        for h, desc in hist.items() for w, n in enumerate(desc["hist"])
                        if n for s in range(32)]
    assert len(expected_columns) == 1216
    assert root["mu_columns"] == data["mu_columns"] == expected_columns
    # Descriptive kind tags are allowed; coordinate identities must match.
    eta_identities = [{k: col[k] for k in ("hist", "old_word", "state")}
                      for col in data["eta_columns"]]
    assert eta_identities == expected_columns
    lookup = {(col["hist"], col["old_word"], col["state"]): j
              for j, col in enumerate(expected_columns)}
    result = {
        "status": "INDEPENDENT_EXACT_SHARED_X_DIRECT_INTERFACE_PASS",
        "sources": [{"path": str(path.relative_to(BASE)), "sha256": sha256(path.read_bytes()).hexdigest()}
                    for path in (INTERFACE, OWN, ROOT, Path(__file__).resolve())],
        "coordinate_audit": {"hist_count": 16, "root_groups": 38,
                             "mu_coordinates": 1216, "shared_eta_coordinates": 1216,
                             "hist_X_coordinates": 16, "original_coordinate_count": 21021},
        "direct_rows": verify_direct_rows(data, hist, xmap, lookup),
        "mass_contract": verify_mass_contract(data, root, hist, xmap, lookup),
        "orbits": verify_orbits(hist),
        "true_source_kernel": verify_true_source_kernel(),
        "gluing": verify_gluing(hist),
        "global_law_limitations": verify_local_global_gaps(),
        "builder_imported": False,
        "point_weight_files_read": 0,
        "optimizer_calls": 0,
        "scope": "Exact symbolic append interface and stated finite kernel only; no game-point feasibility or complete SPE claim.",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "direct_rows": result["direct_rows"],
                      "mass_contract": result["mass_contract"],
                      "output": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
