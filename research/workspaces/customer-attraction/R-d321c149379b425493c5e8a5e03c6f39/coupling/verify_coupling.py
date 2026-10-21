"""Definition-level exact audit; no optimization packages or SPE core imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def compositions(m, p):
    if p == 1:
        return [(m,)]
    return [(a,) + q for a in range(m + 1) for q in compositions(m - a, p - 1)]


def hit(q, B):
    return sum(n for a, n in enumerate(q) if B >> a & 1)


def payoff(q, a, weights):
    return sum((w / hit(q, B) for B, w in weights.items() if B >> a & 1), F(0))


def cover(A, weights):
    return sum((w for B, w in weights.items() if B & A), F(0))


def audit_weights(m, weights):
    qs = compositions(m, 3)
    us = {(q, a): payoff(q, a, weights) for q in qs for a in range(3) if q[a]}
    assert min(us.values()) >= 0
    comparisons = 0
    for a in range(3):
        selected = [q for q in qs if q[a]]
        for q in selected:
            for r in selected:
                kap = max(F(hit(r, B), hit(q, B)) for B in range(1, 8) if B >> a & 1)
                gap = kap * us[r, a] - us[q, a]
                assert gap >= 0, (m, q, r, a, gap)
                comparisons += 1
    cs = {A: cover(A, weights) for A in range(8)}
    monotone = all(cs[A] <= cs[B] for A in range(8) for B in range(8) if A & B == A)
    for a in range(3):
        for b in range(a + 1, 3):
            ca, cb, cab = cs[1 << a], cs[1 << b], cs[(1 << a) | (1 << b)]
            assert ca + cb - cab >= 0
            assert cab - ca >= 0
            assert cab - cb >= 0
    triangle = cs[3] + cs[5] - cs[6] - cs[1]
    return {"m": m, "vertices": len(us), "dilution_comparisons": comparisons,
            "all_payoffs_nonnegative": True, "all_sharp_dilutions": True,
            "local_pair_moments_nonnegative": True, "coverage_monotone": monotone,
            "triangle_gap": str(triangle)}


def audit_strategy(weights, expect_root, expect_welfare):
    n, p = 3, 3
    last = [1, 2, 1, 2, 2, 1, 1, 1, 1]
    actions = {h: a for h, a in zip(product(range(p), repeat=2), last)}
    actions.update({(0,): 1, (1,): 2, (2,): 1, (): 2})
    terminal = {}
    comparisons = 0
    for depth in range(n, -1, -1):
        for h in product(range(p), repeat=depth):
            if depth == n:
                terminal[h] = tuple(h.count(a) for a in range(p))
                continue
            a = actions[h]
            terminal[h] = terminal[h + (a,)]
            actual = payoff(terminal[h], a, weights)
            for b in range(p):
                assert actual >= payoff(terminal[h + (b,)], b, weights), (h, b)
                comparisons += 1
    assert terminal[()] == expect_root
    welfare = sum(payoff(terminal[()], a, weights) * terminal[()][a]
                  for a in range(p) if terminal[()][a])
    assert welfare == expect_welfare
    optimum = max(sum(payoff(q, a, weights) * q[a] for a in range(p) if q[a])
                  for q in compositions(n, p))
    return {"full_history_comparisons": comparisons, "root_counts": terminal[()],
            "root_welfare": str(welfare), "optimum": str(optimum)}


def determinant(matrix):
    a = [[F(x) for x in row] for row in matrix]
    result = F(1)
    for j in range(len(a)):
        pivot = next(k for k in range(j, len(a)) if a[k][j])
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            result = -result
        v = a[j][j]
        result *= v
        for k in range(j + 1, len(a)):
            ratio = a[k][j] / v
            a[k] = [x - ratio * y for x, y in zip(a[k], a[j])]
    return result


def audit_background():
    checked = 0
    for r in range(1, 9):
        for s in range(1, r + 1):
            for k in range(7):
                for z in range(k + 1):
                    for a, b in product(range(2), repeat=2):
                        dq, dp = r * a + s * b + z, s * a + r * b + z
                        ua = F(a, dq) if a else F(0)
                        ubp = F(b, dp) if b else F(0)
                        uap = F(a, dp) if a else F(0)
                        vq = F(z, dq) if z else F(0)
                        vp = F(z, dp) if z else F(0)
                        vb = b * vq
                        tb = F(b * z * (z + (r + s) * a), dq * dp) if b and z else F(0)
                        left = r * s * ua + r * (r - s) * ubp
                        right = s * s * uap + (r - s) * b + s * vp
                        assert 0 <= tb <= vb <= vq
                        assert left + s * vq + (r - s) * tb == right
                        assert left + s * vq <= right <= left + r * vq
                        checked += 1
    modes = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2),
             (1, 0, 0), (1, 0, 1), (1, 0, 2)]
    matrix = []
    val = lambda x, d: F(x, d) if d else F(0)
    for a, b, z in modes:
        q, qp, q0 = 2 * a + b + z, a + 2 * b + z, 3 * b + z
        matrix.append([val(a, q), val(b, qp), val(a, qp), val(b, q0),
                       val(z, q), val(z, qp), val(z, q0)])
    det = determinant(matrix)
    assert det == F(-1, 155520)
    return {"per_type_identity_checks": checked, "seven_slot_minor_determinant": str(det)}


def audit_cut_map():
    checks = 0
    for B in range(1, 16):
        ca = {a: F(bool(B >> a & 1)) for a in range(4)}
        cab = {(a, b): F(bool(B & ((1 << a) | (1 << b))))
               for a in range(4) for b in range(a + 1, 4)}
        for (a, b), c in cab.items():
            assert 2 * c - ca[a] - ca[b] == abs(ca[a] - ca[b])
        for z in product(range(-2, 3), repeat=4):
            length = sum(z[a] * ca[a] for a in range(4))
            row = sum(z[a] * (z[a] - 1) * ca[a] for a in range(4))
            row += 2 * sum(z[a] * z[b] * (ca[a] + ca[b] - c)
                           for (a, b), c in cab.items())
            assert row == length * (length - 1) >= 0
            checks += 1
    return {"integer_quadratic_type_checks": checks}


def main():
    family = []
    for m in range(2, 13):
        M = F(2 * m ** 4)
        weights = {1: F(1), 2: M, 3: M, 4: M, 5: M, 6: F(-2), 7: M}
        result = audit_weights(m, weights)
        assert result["coverage_monotone"] and result["triangle_gap"] == "-1"
        family.append(result)
    small = {1: F(-1, 15), 2: F(1, 3), 3: F(1, 5), 4: F(1, 3),
             5: F(1, 5), 6: F(-1, 5), 7: F(1, 5)}
    small_audit = audit_weights(3, small)
    assert small_audit["triangle_gap"] == "-4/15"
    small_audit["signed_full_strategy"] = audit_strategy(small, (0, 2, 1), F(16, 15))
    small_audit["same_strategy_legal_instance"] = audit_strategy({2: F(1), 4: F(1)}, (0, 2, 1), F(2))
    report = {"status": "exact_checks_passed", "general_claims_proved_in_notes": True,
              "finite_checks_are_not_general_proof": True, "cut_map": audit_cut_map(),
              "arbitrary_background": audit_background(), "signed_family_boundaries": family,
              "small_signed_separation": small_audit}
    target = Path(__file__).with_name("verification.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
