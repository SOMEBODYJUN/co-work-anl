#!/usr/bin/env python3
"""Independent all-atom source/column audit; standard library, no optimizer.

Rebuild 217 rows from literal shares and literal Cartesian menu pairs.  Do not
import or execute either builder or its checker.  Only this directory is written.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
PACKAGE = WORK / "universal_union_wallet_lp"
D = 571565195660569935844
N = 243427385229576983115
L = {
    "SAFE_2_5": 53860460613903177735,
    "SAFE_2_6": 160156075815106272705,
    "SAFE_6_8": 628154063268874822080,
    "UP_2": 6731669434550885946,
    "UP_3": 20553399971568254160,
    "UP_4": 41987372506647246540,
    "MX_8": 346687085980026716220,
    "RC_8_8": 213927321397462708320,
    "ROOT_NEAR": 1070559033998408244,
    "ROOT_RIG_4_5": 1353144016427082948,
    "ROOT_RIG_4_7": 185475750857642747,
    "ROOT_RIG_5_6": 3756945420254355679,
    "ROOT_RIG_6_5": 2971529575004182288,
}
ATOMS = tuple(product((0, 1), repeat=8))


def insertion(member, earlier):
    return F(1, earlier + 1) if member else F(0)


def actual_payoff(a, i):
    return F(1, sum(a)) if a[i - 1] else F(0)


def menu(role, atom):
    """A pure role, or literal six-slot one-hit representative after union reduction.

    For the mean the true d>=o reduction is separately proved and checked below;
    this representative computes the already weakened coefficient, not an action.
    """
    if role < 8:
        return (atom[role - 1],)
    return (atom[7], 0, 0, 0, 0, 0)


def query_average(role, atom, earlier):
    q = menu(role, atom)
    return sum((insertion(t, earlier) for t in q), F()) / len(q)


def potential(p, q, r):
    # The harmonic insertion sum, reconstructed directly from two ordered bits.
    return insertion(q, p) + insertion(r, p + q)


def pair_average(left, right, atom, p):
    q, r = menu(left, atom), menu(right, atom)
    return sum((potential(p, v, w) for v in q for w in r), F()) / (len(q) * len(r))


def rebuild(name):
    parts = name.split("_")
    out = []
    for atom in ATOMS:
        a, x, o = atom[:6], atom[6], atom[7]
        p = sum(a[:4])
        u = [actual_payoff(a, i) for i in range(1, 7)]
        if parts[0] == "SAFE":
            i, role = map(int, parts[1:])
            b = sum(a[:i - 1])
            value = u[i - 1] - query_average(role, atom, b + 6 - i)
        elif parts[0] == "UP":
            i = int(parts[1])
            b, r = sum(a[:i - 1]), 7 - i
            C = (31, 25, 19, 10)[i - 1]
            kappa = insertion(x, b + r - 1)
            exposure = F(1, b + r) if x else F(1, b + 1)
            value = C * u[i - 1] - (C - 1) * kappa - F(o, 6) * exposure
        elif parts[0] == "FMAX":
            value = insertion(x, p) - query_average(int(parts[1]), atom, p)
        elif parts[0] == "MX":
            value = u[4] - query_average(int(parts[1]), atom, p + x)
        elif parts[0] in ("RC", "PAIR"):
            left, right = map(int, parts[1:])
            wallet = u[4] + insertion(x, p)
            if parts[0] == "PAIR":
                self_tax = insertion(a[4], p) - insertion(a[4], p + a[4])
                wallet = u[4] + u[5] + self_tax
            value = wallet - pair_average(left, right, atom, p)
        elif parts[0] == "OPT6":
            omit = int(parts[2])
            visible = a + (x,)
            value = -F(any(v for j, v in enumerate(visible, 1) if j != omit))
        elif name.startswith("K_ge_size_"):
            value = -F(atom[int(parts[-1]) - 1])
        elif name == "K_le_1":
            value = F(0)
        elif name.startswith("SIZE_FLOOR_"):
            value = u[int(parts[-1]) - 1]
        elif name == "W_le_1":
            value = -F(any(a))
        elif name == "ROOT_NEAR":
            value = 150 * u[0] - o
        elif name.startswith("ROOT_RIG_"):
            anchor, query = map(int, parts[-2:])
            t = atom[anchor - 1]
            value = 25 * u[0] - 7 * t - query_average(query, atom, 5 * t)
        else:
            raise AssertionError(("unknown row", name))
        out.append(F(value))
    K = F(0)
    rhs = F(0)
    if name.startswith("K_ge_size_"):
        K = F(1)
    elif name == "K_le_1":
        K, rhs = F(-1), F(-1)
    elif name.startswith("SIZE_FLOOR_"):
        K = -F(1, 6)
    elif name == "ROOT_NEAR":
        K = -F(139, 6)
    elif name.startswith("ROOT_RIG_"):
        K = F(3)
    elif name.startswith("OPT6_") or name == "W_le_1":
        rhs = F(-1)
    return tuple(out + [K]), rhs


def source_residual_checks():
    result = {}
    # Source-X deviation, own-terminal SAFE, middle MAX and terminal union BR.
    for i, r in ((1, 6), (2, 5), (3, 4)):
        m, alpha, C = r - 2, 5 * (r - 1), 6 * r - 5
        beta = F(5 * r - 6, r * (r - 1))
        values = []
        for n, k, x, j, t, o in product(range(1, 8 - r), range(m + 1),
                                        (0, 1), range(m + 1), (0, 1), (0, 1)):
            den, theta = n + r - 1, F(o, 6)
            target_without_u = -(C - 1) * F(x, den) - theta * (
                F(1, den) if x else F(1, n))
            # Build paid contribution from actual per-customer source shares.
            source_paid = -alpha * insertion(x, n - 1 + j + t)
            safe_paid = -r * F(t, den)
            maxima_paid = beta * F(m * x - j, n + k)
            terminal_paid = F(t - theta, n + x + j)
            residual = target_without_u - source_paid - safe_paid - maxima_paid - terminal_paid
            assert residual >= 0, ("UP residual", i, n, k, x, j, t, o, residual)
            values.append(residual)
        result[f"UP_{i}"] = {"states": len(values), "minimum": str(min(values)),
                                "positive_states": sum(v > 0 for v in values)}
    # UP4 uses a different valid budget: 10 source IC + MAX(Y)+2MAX(T)+BR.
    values = []
    for b, a4, x, y, t, o in product(range(4), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)):
        theta, den = F(o, 6), b + 3
        target_without_u = -9 * F(x, den) - theta * (F(1, den) if x else F(1, b + 1))
        paid = (-10 * insertion(x, b + y + t) + F(x - y, b + a4 + 1)
                + 2 * F(x - t, b + a4 + 1) + F(t - theta, b + x + y + 1))
        residual = target_without_u - paid
        assert residual >= 0
        values.append(residual)
    result["UP_4"] = {"states": len(values), "minimum": str(min(values)),
                       "positive_states": sum(v > 0 for v in values)}
    # The all-integer root transfer proof at m=6, including zero total load.
    values = []
    for p, z, q, n in product((0, 1), (0, 1), (0, 1), range(5)):
        first = insertion(p, n + z)
        last = insertion(z, p + n)
        lhs = insertion(q, 5 * p) - insertion(q, p + n) + last - first
        rhs = F(n - 4 * p, 2) + z - p + 24 * (first - F(p, 6))
        assert rhs - lhs >= 0
        values.append(rhs - lhs)
    result["root_transfer_m6"] = {"states": len(values), "minimum": str(min(values))}
    # Literal full-pair means, followed by d>=o reduction; no independence.
    full_pair = mixed = 0
    for p, d in product(range(5), range(7)):
        menu_d = (1,) * d + (0,) * (6 - d)
        o = int(d > 0)
        menu_o = (o, 0, 0, 0, 0, 0)
        exact = sum((potential(p, q, r) for q in menu_d for r in menu_d), F()) / 36
        weak = sum((potential(p, q, r) for q in menu_o for r in menu_o), F()) / 36
        assert weak == F(o, 3 * (p + 1)) - F(o, 36 * (p + 1) * (p + 2))
        assert exact - weak >= 0
        full_pair += 1
        for q in (0, 1):
            exact_q = sum((potential(p, q, r) for r in menu_d), F()) / 6
            weak_q = sum((potential(p, q, r) for r in menu_o), F()) / 6
            assert exact_q - weak_q >= 0
            mixed += 1
    result["union_query_reductions"] = {"literal_full36_cases": full_pair,
                                         "literal_pure_mean_cases": mixed}
    return result


def main():
    inputs = {name: PACKAGE / name for name in (
        "source_derivations.md", "exact_input.json", "exact_certificate.json", "checker_output.json", "proof.md")}
    data = json.loads(inputs["exact_input.json"].read_text())
    cert = json.loads(inputs["exact_certificate.json"].read_text())
    assert sha256(inputs["exact_input.json"].read_bytes()).hexdigest() == cert["input_sha256"]
    assert len(data["atom_columns"]) == 256 and data["K_column"] == 256
    for j, (atom, desc) in enumerate(zip(ATOMS, data["atom_columns"])):
        assert desc == {"index": j, "a": list(atom[:6]), "x": atom[6], "o": atom[7]}
    assert data["nonnegative_columns"] == list(range(257))
    obj = tuple(F(any(v[:6])) for v in ATOMS) + (F(0),)
    norm = tuple(F(v[7]) for v in ATOMS) + (F(0),)
    sparse = lambda row: {str(j): str(v) for j, v in enumerate(row) if v}
    assert data["objective"] == sparse(obj)
    assert data["equality"]["a"] == sparse(norm) and F(data["equality"]["rhs"]) == 1

    rows = {}
    groups = defaultdict(list)
    family_counts = Counter()
    for raw in data["raw_rows"]:
        name = raw["name"]
        assert name not in rows
        vector, rhs = rebuild(name)
        assert sparse(vector) == raw["a"] and rhs == F(raw["rhs"]), name
        rows[name] = (vector, rhs)
        family_counts[raw["family"]] += 1
        groups[(vector, rhs)].append(name)
    assert len(rows) == 217
    zero = groups.pop(((F(0),) * 257, F(0)))
    assert zero == ["SAFE_6_6"] == data["removed_zero_rows"]
    assert len(groups) == len(data["unique_rows"]) == 205
    for row in data["unique_rows"]:
        key = rebuild(row["name"])
        assert set(row["aliases"]) == set(groups[key])
        assert row["a"] == sparse(key[0]) and F(row["rhs"]) == key[1]

    primal = [F(0)] * 257
    for j, value in cert["primal"].items():
        assert 0 <= int(j) <= 256
        primal[int(j)] = F(value)
    assert min(primal) >= 0
    dot = lambda r: sum((v * q for v, q in zip(r, primal)), F())
    slacks = {name: dot(vector) - rhs for name, (vector, rhs) in rows.items()}
    assert min(slacks.values()) >= 0
    assert {k: str(v) for k, v in slacks.items()} == cert["raw_row_slacks"]
    assert dot(norm) == 1 and dot(obj) == F(N, D) == F(cert["objective"])
    assert primal[256] == F(cert["K"])
    assert F(1, 2) - dot(obj) == F(42355212600707984807, D) == F(cert["half_gap"])

    weights = {name: F(n, D) for name, n in L.items()}
    assert {k: F(v) for k, v in cert["dual"]["row_weights"].items()} == weights
    assert F(cert["dual"]["normalization_multiplier"]) == F(N, D)
    assert all(rows[name][1] == 0 and L[name] > 0 for name in L)
    residuals = [D * obj[j] - N * norm[j] - sum(
        (L[name] * rows[name][0][j] for name in L), F()) for j in range(257)]
    assert min(residuals) >= 0 and residuals[256] == 0
    assert {str(j): str(v / D) for j, v in enumerate(residuals) if v} == cert["dual"]["nonnegative_column_residual"]
    assert all(v * primal[j] == 0 for j, v in enumerate(residuals))
    assert all(F(L[name], D) * slacks[name] == 0 for name in L)
    assert 3 * sum(L[name] for name in L if name.startswith("ROOT_RIG")) == F(139, 6) * L["ROOT_NEAR"]
    assert all((30 * v).denominator == 1 for v in residuals)

    source_checks = source_residual_checks()
    source_paths = [REPO / path for path in data["source_sha256"]]
    source_paths += [WORK / "main_union_comparison.md", WORK / "maxb_h3_bridge.md",
                     WORK / "universal_union_wallet_lp.md"]
    for path, pin in data["source_sha256"].items():
        assert sha256((REPO / path).read_bytes()).hexdigest() == pin
    pinned = list(inputs.values()) + source_paths
    source_hashes = {str(p.relative_to(REPO)): sha256(p.read_bytes()).hexdigest() for p in pinned}
    result = {
        "status": "PASS_INDEPENDENT_UNIVERSAL_SOURCE_AND_EXACT_COLUMN_AUDIT",
        "N": str(N), "D": str(D), "universal_bound": str(F(N, D)),
        "proof_scope": "Every finite unit-customer common-label-catalog complete ordered-history pure SPE with six players; OPT6=0 handled separately.",
        "system_sharpness_scope": "Only the explicitly specified necessary budget family, not complete SPE realizability or best-known-bound comparison.",
        "source_sha256": source_hashes,
        "raw_rows_rebuilt": 217, "unique_rows_verified": 205,
        "coefficient_equalities": 217 * 257,
        "all_boolean_atoms": 256, "nonnegative_variables_checked": 257,
        "family_counts": dict(family_counts),
        "positive_integer_budget_weights": {k: str(v) for k, v in L.items()},
        "positive_budget_rhs_all_zero": True,
        "normalization_multiplier": str(F(N, D)),
        "all_257_column_identities_exact": True,
        "K_column_residual": "0",
        "zero_atom_residuals": [j for j, v in enumerate(residuals[:256]) if not v],
        "positive_atom_residual_count": sum(v > 0 for v in residuals[:256]),
        "minimum_positive_unnormalized_residual": str(min(v for v in residuals if v > 0)),
        "thirty_times_unnormalized_residuals": [str(int(30 * v)) for v in residuals],
        "primal_nonzero_atoms": sum(v > 0 for v in primal[:256]),
        "primal_objective": str(dot(obj)), "dual_objective": str(F(N, D)),
        "primal_all_217_row_slacks": {k: str(v) for k, v in slacks.items()},
        "normalization": str(dot(norm)), "half_gap": str(F(1, 2) - dot(obj)),
        "all_complementarity_identities_exact": True,
        "source_all_domain_checks": source_checks,
        "generator_or_builder_checker_imported": False,
        "optimizer_imported_or_called": False,
        "old_numeric_points_read": False,
        "outstanding_errors": [],
    }
    destination = HERE / "audit_result.json"
    assert not destination.exists(), "refuse to overwrite frozen audit"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "raw_rows_rebuilt", "coefficient_equalities", "all_boolean_atoms",
        "positive_atom_residual_count", "minimum_positive_unnormalized_residual",
        "K_column_residual", "primal_objective", "dual_objective", "source_all_domain_checks")},
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
