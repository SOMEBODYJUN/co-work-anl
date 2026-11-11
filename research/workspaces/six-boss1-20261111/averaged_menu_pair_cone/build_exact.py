#!/usr/bin/env python3
"""Exact 144-type, 11-weight cone certificate; no optimizer is used.

The only output directory is this new package. The audited local query
parameter is theta = 1/6; literal one-membership menus realize this block.
The manuscript separately explains its interface to union-weakened budgets.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import csv
import hashlib
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
THETA = F(1, 6)
NAMES = ["alpha", "sY", "sZ", "sT", "aY", "aZ", "aT", "delta", "eta1", "eta2", "eta3"]
COST = [F(1)] * 4 + [F(0)] * 7
PRIMAL = [F(15), F(0), F(0), F(4), F(7, 6), F(7, 6), F(0), F(1), F(0), F(0), F(0)]
DUAL_SUPPORT = {0: F(160), 15: F(36), 33: F(24), 110: F(30)}
SOURCES = [
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md",
    "research/workspaces/six-boss1-20261111/early3_pair_cone.md",
]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def record(typ):
    n, k, x, y, z, t = typ
    D = n + 3
    d = n + x + y
    psi = F(z, d + t) + F(t, d + z) + F(z, d * (d + 1))
    tp = [
        psi - (THETA + x) / d + THETA * x / (d * (d + 1)),
        psi - 2 * THETA / d + THETA / (d * (d + 1)),
        psi - F(2 * x, d) + F(x, d * (d + 1)),
    ]
    G = [
        F(x, n + y + z + t) - F(x, D),
        F(y - x, D), F(z - x, D), F(t - x, D),
        F(y - x, n + k), F(z - x, n + k), F(t - x, n + k),
        (THETA - t) / (n + x + y + z),
        *[-v for v in tp],
    ]
    h = THETA * (F(x, D) + F(1 - x, n)) - F(x, D)
    return {"type": list(typ), "d": d, "psi": psi, "TP": tp, "G": G, "h": h, "E_star": dot(G, PRIMAL) - h}


def reduced(x, n, a, t):
    if x == 0:
        return F(4 * t, n + 3) + F(7 * a, 6 * (n + 2)) - F(t, n + a) - F(a, 6 * n * (n + a))
    return F(15, n + a + t) + F(24 * t - 109, 6 * (n + 3)) - F(7 * (2 - a), 6 * n) - F(6 * t - 1, 6 * (n + 1 + a))


def convert(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [convert(v) for v in obj]
    return obj


def save(name, obj):
    (HERE / name).write_text(json.dumps(convert(obj), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    rows = [record(typ) for typ in product((1, 2, 3), (0, 1, 2), (0, 1), (0, 1), (0, 1), (0, 1))]
    assert len(rows) == 144
    lam = [DUAL_SUPPORT.get(i, F(0)) for i in range(144)]
    GTlam = [sum((lam[i] * rows[i]["G"][j] for i in range(144)), F(0)) for j in range(11)]
    rc = [COST[j] - GTlam[j] for j in range(11)]
    p_obj = dot(COST, PRIMAL)
    d_obj = sum((lam[i] * rows[i]["h"] for i in range(144)), F(0))
    assert p_obj == d_obj == 19
    assert min(PRIMAL) >= 0 and min(lam) >= 0 and min(rc) >= 0
    assert all(r["E_star"] >= 0 for r in rows)
    assert rc == [F(0), F(1), F(1), F(0), F(0), F(0), F(2), F(0), F(1), F(2, 3), F(20)]
    assert all(lam[i] * rows[i]["E_star"] == 0 for i in range(144))
    assert all(rc[j] * PRIMAL[j] == 0 for j in range(11))

    compact = []
    for x, n, a, t in product((0, 1), (1, 2, 3), (0, 1, 2), (0, 1)):
        v = reduced(x, n, a, t)
        assert v >= 0
        compact.append({"x": x, "n": n, "a": a, "t": t, "H": v})
    for row in rows:
        n, k, x, y, z, t = row["type"]
        a = y + z
        correction = F(7 * a, 6) * (F(1, n + k) - F(1, n + 2)) if x == 0 else F(7 * (2 - a), 6) * (F(1, n) - F(1, n + k))
        assert correction >= 0
        assert row["E_star"] == reduced(x, n, a, t) + correction

    positive = [r["E_star"] for r in rows if r["E_star"] > 0]
    stats = {"types": 144, "variables": 11, "matrix_entries": 1584, "zero_residuals": sum(r["E_star"] == 0 for r in rows), "positive_residuals": len(positive), "negative_residuals": sum(r["E_star"] < 0 for r in rows), "minimum_positive_residual": min(positive)}
    save("local_table_144.json", {"theta": THETA, "row_order": ["n", "k", "x", "y", "z", "t"], "index_base": 0, "variable_order": NAMES, "rows": [{"index": i, **r} for i, r in enumerate(rows)]})
    with (HERE / "local_table_144.csv").open("w", encoding="utf-8", newline="") as f:
        out = csv.writer(f)
        out.writerow(["index", "n", "k", "x", "y", "z", "t", "d", "psi", "TP1", "TP2", "TP3", *NAMES, "h", "E_star"])
        for i, row in enumerate(rows):
            out.writerow([i, *row["type"], row["d"], row["psi"], *row["TP"], *row["G"], row["h"], row["E_star"]])
    save("reduced_36_table.json", {"meaning": "A display-only reduction for the exhibited eta=0 symmetric primal certificate, not a symmetry reduction of the 11-weight cone.", "rows": compact})
    save("exact_certificate.json", {
        "scope": "Fixed theta=1/6 block of six-query average budgets; literal dmenu=1 realization or valid union-weakened budgets. Mixed theta=0/1/6 global closure is outside this audit; complete ordered-history pure SPE is retained.",
        "variable_order": NAMES, "cost": COST, "primal": PRIMAL,
        "primal_objective": p_obj, "dual_objective": d_obj, "exact_gap": p_obj - d_obj,
        "dual_support": [{"index": i, "type": rows[i]["type"], "lambda": v, "TP": rows[i]["TP"], "h": rows[i]["h"]} for i, v in DUAL_SUPPORT.items()],
        "GT_lambda": GTlam, "reduced_cost": rc, "statistics": stats,
        "lower_bound_identity": "C-19 = 160 E_0 + 36 E_15 + 24 E_33 + 30 E_110 + sY + sZ + 2 aT + eta1 + (2/3) eta2 + 20 eta3",
        "all_optima_have_eta_zero": True,
        "all_optima_zero_coordinates": ["sY", "sZ", "aT", "eta1", "eta2", "eta3"],
        "not_claimed": ["SPE sharpness", "realization of the dual as a game", "unrestricted d>1 theorem", "six-player half-welfare theorem", "uniqueness of aY and aZ"],
    })
    save("optimization_log.json", {"optimizer_invocations": 0, "reason": "An exact four-support dual is obtained algebraically; the permitted one tiny local LP was unnecessary.", "old_optimizer_reruns": 0, "external_search": False, "numeric_discovery_input": None, "numeric_discovery_output": None})
    manifest = []
    for rel in SOURCES:
        data = (REPO / rel).read_bytes()
        manifest.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    save("source_manifest.json", {"read_only_sources": manifest, "source_contents_not_modified": True})
    print(json.dumps(convert({"result": "PASS", "objective": p_obj, "statistics": stats, "dual_support": DUAL_SUPPORT, "reduced_cost": rc, "optimizer_invocations": 0}), ensure_ascii=False))


if __name__ == "__main__":
    main()
