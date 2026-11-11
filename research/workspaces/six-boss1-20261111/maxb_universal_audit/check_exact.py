"""Independent arithmetic audit of MP/MC6; no optimizer or project imports.

The analytic proof is in ../maxb_universal_audit.md.  This checker reads the
raw cb45 customer histograms, builds six literal (B,C) menu memberships,
evaluates the five budget contributions directly by terminal payoffs, and
only then compares its projected row with the frozen certificate.
All writes stay in this audit directory.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


AUDIT = Path(__file__).resolve().parent
RUN = AUDIT.parent
REPO = RUN.parents[2]
POINT = RUN / "full624_augmented_lp/recovery/augmented_lp_exact.json"
CERT = RUN / "terminal_response_cycles/max_b_exact_certificate.json"
EXPECTED_POINT_HASH = "cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932"
EXPECTED_CERT_HASH = "f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664"
PARAMS = tuple(map(F, (12, 36, 24, 1, 16)))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(p, own, other):
    # The denominator is needed only when this player covers the customer.
    return F(1, p + 1 + other) if own else F(0)


def f(p, q):
    return F(q, p + 1)


def g(p, q, r):
    return F(q * r, (p + 1) * (p + 2))


def average(values):
    return sum(values, F(0)) / len(values)


def evaluate(p, a, b, z, pairs, params):
    """Return five local budgets, bare MP part and the coefficient of z.

    These are algebraic customer contributions.  Individual customer IC
    contributions are NOT asserted to be nonnegative.  The global +delta*K
    is carried separately when evaluating the actual necessary row.
    """
    lam, beta, gamma, delta, eps = params
    u = share(p, a, b)
    v = share(p, b, a)
    mean_fq = average([f(p, q) for q, r in pairs])
    mean_fr = average([f(p, r) for q, r in pairs])
    mean_g = average([g(p, q, r) for q, r in pairs])
    budgets = (
        u - share(p, b, z),
        u - average([share(p, r, z) for q, r in pairs]),
        v - share(p, z, a),
        -F(z),
        u + f(p, z) - mean_fq - mean_fr + mean_g,
    )
    bare = ((lam + beta + eps) * u + gamma * v - lam * f(p, b)
            - eps * mean_fq - (beta + eps) * mean_fr + eps * mean_g)
    mean_r = average([F(r) for q, r in pairs])
    k = ((lam * b + beta * mean_r) / ((p + 1) * (p + 2))
         + eps / (p + 1) - gamma / (p + a + 1) - delta)
    combined = sum((weight * budget for weight, budget in zip(params, budgets)), F(0))
    assert combined == bare + k * z
    assert max(k, F(0)) - k * z >= 0
    return bare, k, combined


def six_pair_menus():
    # Each quadruple is the multiset of six literal (B_i,C_i) memberships.
    for n00 in range(7):
        for n01 in range(7 - n00):
            for n10 in range(7 - n00 - n01):
                n11 = 6 - n00 - n01 - n10
                yield ([(0, 0)] * n00 + [(0, 1)] * n01
                       + [(1, 0)] * n10 + [(1, 1)] * n11)


menus = list(six_pair_menus())
assert len(menus) == 84
mc6_cases = 0
for p, a, b, z in product(range(5), (0, 1), (0, 1), (0, 1)):
    for pairs in menus:
        bare, k, combined = evaluate(p, a, b, z, pairs, PARAMS)
        dc = sum(r for q, r in pairs)
        simplified = F(12 * b + 24 * a + 6 * dc - (p + 2) * (p + 9),
                       (p + 1) * (p + 2))
        assert k == simplified
        mc6_cases += 1
assert mc6_cases == 3360

# Independent small checks for arbitrary menu length/background, parameter
# coordinate faces, the all-zero face, and one mixed rational parameter.
parameter_vectors = [tuple(F(i == j) for i in range(5)) for j in range(5)]
parameter_vectors += [(F(0),) * 5, (F(2, 3), F(5, 7), F(11, 13), F(17, 19), F(23, 29))]
generic_inputs = [
    (0, 0, 0, 0, [(0, 0)]),
    (0, 1, 1, 1, [(1, 1)]),
    (4, 1, 0, 0, [(0, 1), (1, 0), (1, 1)]),
    (17, 0, 1, 1, [(1, 0), (1, 0)]),
    (29, 1, 1, 0, [(0, 0), (1, 1), (0, 1), (1, 1), (1, 0)]),
]
for case in generic_inputs:
    for params in parameter_vectors:
        evaluate(*case, params)

assert digest(POINT) == EXPECTED_POINT_HASH
assert digest(CERT) == EXPECTED_CERT_HASH
point = json.loads(POINT.read_text())
assert len(point["columns"]) == 20585
assert point["columns"][0]["kind"] == "K"
row = {0: F(1)}
table = []
component_values = {key: F(0) for key in ("u5", "u6", "f_A6", "mean_f_B", "mean_f_C", "mean_g_BC", "positive_part")}
for j, col in enumerate(point["columns"]):
    if col["kind"] != "hist":
        continue
    bits = tuple(map(int, col["actual_bits"]))
    p, a, b = sum(bits[:4]), bits[4], bits[5]
    pairs = []
    for word, count in enumerate(col["hist"]):
        pairs.extend([((word >> 1) & 1, word & 1)] * count)
    assert len(pairs) == 6
    bare, k, _ = evaluate(p, a, b, 0, pairs, PARAMS)
    # Membership one gives the same coefficient without relying on (7).
    _, _, at_one = evaluate(p, a, b, 1, pairs, PARAMS)
    assert at_one - bare == k
    coefficient = bare + max(k, F(0))
    if coefficient:
        row[j] = coefficient
    weight = F(col["weight"])
    contributions = {
        "u5": share(p, a, b),
        "u6": share(p, b, a),
        "f_A6": f(p, b),
        "mean_f_B": average([f(p, q) for q, r in pairs]),
        "mean_f_C": average([f(p, r) for q, r in pairs]),
        "mean_g_BC": average([g(p, q, r) for q, r in pairs]),
        "positive_part": max(k, F(0)),
    }
    for name, value in contributions.items():
        component_values[name] += weight * value
    table.append({
        "column": j, "actual_bits": col["actual_bits"], "P": p,
        "d_B": sum(q for q, r in pairs), "d_C": sum(r for q, r in pairs),
        "d_BC": sum(q * r for q, r in pairs), "kappa": str(k),
        "positive_part": str(max(k, F(0))), "coefficient": str(coefficient),
        "point_mass_is_zero": weight == 0,
    })
assert len(table) == 16 and len(row) == 17

# Read the certificate only after the independent row has been assembled.
cert = json.loads(CERT.read_text())
assert row == {j: F(c) for j, c in cert["sparse_original4849_row_K_normalized"]}
positive_hist = {h["column"]: 3 * F(h["kappa"]) for h in table if F(h["kappa"]) > 0}
negative_hist = {h["column"]: -3 * F(h["kappa"]) for h in table if F(h["kappa"]) < 0}
assert positive_hist == {
    item["name"][1]: F(item["multiplier"]) for item in cert["row_multipliers"]
    if item["name"][0] == "X-at-most-hist"
}
assert negative_hist == {
    item["descriptor"]["hist_column"]: F(item["multiplier"])
    for item in cert["new_nonnegativity_multipliers"]
}
assert {
    tuple(item["name"]): F(item["multiplier"]) for item in cert["row_multipliers"]
    if item["name"][0] != "X-at-most-hist"
} == {
    ("X-caps-query", "A", 5): F(36),
    ("X-caps-query", "C"): F(108),
    ("actual-safe-X", 6): F(72),
    ("capacity-X",): F(3),
    ("common-B-pair", 142): F(48),
}
value = sum((c * F(point["columns"][j]["weight"]) for j, c in row.items()), F(0))
K = F(point["columns"][0]["weight"])
cv = component_values
value_from_components = (64 * cv["u5"] + 24 * cv["u6"] + K - 12 * cv["f_A6"]
                         - 16 * cv["mean_f_B"] - 52 * cv["mean_f_C"]
                         + 16 * cv["mean_g_BC"] + cv["positive_part"])
expected = F(-4426145324455836398818752701603934797071201573118130939132148836781341509474,
             37610930738552016886760210756472139042422876797320439967207958074168853634165)
assert value == value_from_components == expected == F(cert["K_normalized_point_value"]) < 0
assert 3 * value == F(cert["exact_point_value"])

source_files = [
    REPO / "archives/customer-attraction/state/引理/共同最大潜力主题的末两位容量投影--引理.md",
    REPO / "archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md",
    REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
]
report = {
    "status": "PASS_INDEPENDENT_MP_MC6_AND_CB45_ARITHMETIC",
    "source_hashes": {str(p.relative_to(REPO)): digest(p) for p in source_files},
    "point_sha256": digest(POINT), "certificate_sha256": digest(CERT),
    "checker_sha256": digest(Path(__file__)),
    "mc6_atomic_expansion_cases": mc6_cases,
    "generic_menu_and_parameter_face_cases": len(generic_inputs) * len(parameter_vectors),
    "three_times_kappa_matches_all_ten_box_multipliers": True,
    "histograms": table,
    "row": [[j, str(c)] for j, c in sorted(row.items())],
    "K": str(K),
    "exact_components": {name: str(value) for name, value in component_values.items()},
    "decimal_components": {name: float(value) for name, value in component_values.items()},
    "exact_value": str(value), "decimal_value": float(value),
    "proof_scope": "Analytic MP is universal; these calculations check identities and a fixed-point evaluation only.",
    "old_LP_optimality_reaudited": False,
    "no_optimizer": True,
    "no_project_code_imported": True,
    "writes_only_this_audit_directory": True,
}
(AUDIT / "check_exact.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k not in
                  ("histograms", "row", "exact_components", "decimal_components", "source_hashes")},
                 ensure_ascii=False, indent=2))
