#!/usr/bin/env python3
"""Audit this frozen four-point discovery, without invoking a numerical LP.

The raw audit below reconstructs n=6 rows with integer arithmetic independently
of the frozen verifier. It does not run discovery, recovery, or that verifier.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "evidence"
PATHS = [[0, 1, 2, 3, 4, 5], [0, 5, 6, 7, 8, 9],
         [0, 1, 5, 10, 11, 12], [0, 1, 2, 5, 13, 14],
         [0, 1, 2, 3, 5, 15]]
L = 120


def guard(c):
    assert c["n"] == 6 and c["copies"] == 4
    assert c["bits"] == 16 and c["paths"] == PATHS
    assert F(c["B"]) > 0
    for key, value in c["multipliers"].items():
        assert F(value) > 0
        z = key.split(":")
        if z[0] == "CAP":
            assert len(z) == 2 and 1 <= int(z[1]) < 16
        elif z[0] == "COPY":
            assert len(z) == 2 and 1 <= int(z[1]) <= 4
        elif z[0] == "FLOOR":
            k, i, j = map(int, z[1:])
            assert 0 <= k <= 4 and (1 if k == 0 else k + 1) <= i < 6
            assert 0 <= j < 16 and j != PATHS[k][i]
        elif z[0] == "PAIR":
            assert len(z) == 2 and 0 <= int(z[1]) <= 3
        elif z[0] == "LAST":
            assert len(z) == 2 and 0 <= int(z[1]) <= 4
        else:
            raise AssertionError(key)


def exact_rows(mask, keys):
    """Integer coefficients 120*G(mask,0), derived from the displayed formulas."""
    b = [(mask >> j) & 1 for j in range(16)]
    loads = [sum(b[j] for j in path) for path in PATHS]
    def share(k, i):
        return L // loads[k] if b[PATHS[k][i]] else 0
    rows = []
    for key in keys:
        z = key.split(":")
        kind = z[0]
        if kind == "CAP":
            rows.append(L * (b[0] - b[int(z[1])]))
        elif kind == "COPY":
            i = int(z[1])
            rows.append(share(0, i) - share(i, i))
        elif kind == "FLOOR":
            k, i, j = map(int, z[1:])
            prefix = sum(b[h] for h in PATHS[k][:i])
            den = prefix + 6 - i
            assert L % den == 0
            rows.append(share(k, i) - (L // den if b[j] else 0))
        elif kind == "PAIR":
            k = int(z[1])
            prefix = sum(b[h] for h in PATHS[k][:4])
            den = (prefix + 1) * (prefix + 2)
            assert L % den == 0 and L % (prefix + 1) == 0
            tax = L // den if b[PATHS[k][4]] else 0
            rows.append(3 * (share(k, 4) + share(k, 5) + tax)
                        + L * prefix // (prefix + 1))
        elif kind == "LAST":
            k = int(z[1])
            prefix = sum(b[h] for h in PATHS[k][:5])
            assert L % (prefix + 1) == 0
            rows.append(6 * share(k, 5) + L * prefix // (prefix + 1))
        else:
            raise AssertionError(key)
    return b[0], share(0, 0), rows


def raw_audit(c):
    guard(c)
    lam = {k: F(v) for k, v in c["multipliers"].items()}
    B, C = F(c["B"]), F(c["C"])
    S = sum((v for k, v in lam.items() if k.startswith(("PAIR:", "LAST:"))), F(0))
    D = math.lcm(B.denominator, C.denominator, *(v.denominator for v in lam.values()))
    weights = [int(v * D) for v in lam.values()]
    bn, cn, sn = int(B * D), int(C * D), int(S * D)
    minima = [None, None]
    witnesses = [None, None]
    negatives = [0, 0]
    for mask in range(1 << 16):
        root, v, rows = exact_rows(mask, lam)
        r0 = bn * v + cn * L * root - sum(w * g for w, g in zip(weights, rows))
        for o in (0, 1):
            residual = r0 + (sn - D) * L * o
            negatives[o] += residual < 0
            if minima[o] is None or residual < minima[o]:
                minima[o] = residual
                witnesses[o] = mask
    def witness(o):
        mask = witnesses[o]
        return {"o": o, "mask": mask,
                "member_labels": [j for j in range(16) if mask & (1 << j)],
                "residual": str(F(minima[o], D * L)),
                "residual_float": float(F(minima[o], D * L)),
                "negative_type_count": negatives[o]}
    return {"C": str(C), "B": str(B), "B_float": c["B_float"],
            "nonzero_multiplier_count": len(lam),
            "family_counts": {t: sum(k.startswith(t + ":") for k in lam)
                              for t in ["CAP", "COPY", "FLOOR", "PAIR", "LAST"]},
            "opt_multiplier_sum": str(S), "opt_sum_minus_one": str(S - 1),
            "opt_sum_minus_one_float": float(S - 1),
            "exact_normalization": S == 1,
            "legal_active_rows": True,
            "raw_pointwise_identity_nonnegative": not any(negatives),
            "checked_membership_types": 65536,
            "checked_o_values_per_type": 2,
            "minima": [witness(0), witness(1)],
            "solver_status_as_recorded": c["status"]}


def main():
    raw = json.loads((EVIDENCE / "discovery_n6_c4.json").read_text())
    raw_report = [raw_audit(c) for c in raw]
    (HERE / "raw-discovery-exact-audit.json").write_text(json.dumps(raw_report, indent=2) + "\n")
    summary = {"numerical_lp_run": False,
               "recovery_run": False,
               "frozen_verifier_run": False,
               "raw_row_reconstruction": "new fixed-n=6 integer formulas in audit_discovery.py",
               "raw_audit": raw_report,
               "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(EVIDENCE.iterdir()) if p.is_file()}}
    (HERE / "audit-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"raw_normalizations_exact": [r["exact_normalization"] for r in raw_report],
                      "raw_pointwise_nonnegative": [r["raw_pointwise_identity_nonnegative"] for r in raw_report]}, indent=2), flush=True)


if __name__ == "__main__":
    main()
