"""Exact check and 17-row interface for the common-X H3 bridge.

Reads frozen descriptors and the already-built common-X lift.  It does not
evaluate an old feasible point, solve an LP, modify a frozen matrix, or claim
that independent overlap upper bounds have a common customer realization.
All output is confined to this directory.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
WORK = HERE.parent
SOURCES = {
    "lift": WORK / "terminal_response_cycles/max_b_symbolic_lift.json",
    "orbits": WORK / "terminal_response_cycles/max_b_preflight.json",
    "descriptor_container": WORK / "full624_augmented_lp/recovery/augmented_lp_exact.json",
}
WORDS = tuple(product((0, 1), repeat=3))


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def save(name, value):
    (HERE / name).write_text(json.dumps(serial(value), ensure_ascii=False,
                                        indent=2) + "\n")


def frozen(value):
    return tuple(frozen(v) for v in value) if isinstance(value, list) else value


def add(row, column, value):
    if value:
        row[column] = row.get(column, F()) + value
        if not row[column]:
            del row[column]


def sparse(row):
    return [[j, str(v)] for j, v in sorted(row.items())]


def check_atoms():
    records = []
    table = []
    for b, a, x, y, z, q in product(range(4), (0, 1), (0, 1),
                                   (0, 1), (0, 1), (0, 1)):
        n = b + 1
        vx = F(x, n + y + z)
        kappa = F(x, n + 2)
        ell = F(q * x, n + 2) + F(q * (1 - x), n)
        max_y = F(x - y, n + a)
        max_z = F(x - z, n + a)
        last = F(z - q, n + x + y)
        slack = 10 * vx - 9 * kappa - ell - max_y - 2 * max_z - last
        if not x:
            closed = F(y + 2 * z, n + a) - F(z, n + y) - F(q * y, n * (n + 1))
        elif y == z == 0:
            closed = F(10, n) - F(9, n + 2) - F(3, n + a) + F(q, (n + 1) * (n + 2))
        elif y == 0 and z == 1:
            closed = F(9 + q, (n + 1) * (n + 2)) - F(1, n + a)
        elif y == 1 and z == 0:
            closed = F(10, n + 1) - F(9, n + 2) - F(2, n + a)
        else:
            closed = F()
        assert slack == closed and slack >= 0
        # Exact membership form of the row used in the 17-orbit adapter.
        expanded = 10 * vx - F(9 * x, b + 3) - F(q, b + 1) + F(2 * x * q, (b + 1) * (b + 3))
        assert expanded == 10 * vx - 9 * kappa - ell
        records.append({"b": b, "a": a, "x": x, "y": y, "z": z, "q": q,
                        "deviation_pay": vx, "kappa": kappa, "target_L": ell,
                        "maximum_Y_atom": max_y, "maximum_Z_atom": max_z,
                        "last_BR_atom": last, "remainder": slack,
                        "closed_form_remainder": closed})
        table.append(f"| {b} | {a} | {x} | {y} | {z} | {q} | {slack} |")
    assert len(records) == 128
    counts = Counter(str(r["remainder"]) for r in records)
    result = {"scope": "All 4 * 2^5 coefficient types; not 128 games or SPE tests.",
              "formula": "10*u4 - 9*kappa - L = 10*(u4-vX) + M_Y + 2*M_Z + BR_Z(Q) + sum(remainder)",
              "case_count": len(records), "all_nonnegative": True,
              "minimum": min(r["remainder"] for r in records),
              "zero_count": counts["0"], "records": records}
    save("atom_audit.json", result)
    (HERE / "atom_table.md").write_text(
        "# 完整 128 型有理余项表\n\n"
        "b 是前三位负载；a 是 actual A4 位；x,y,z,q 分别是同一 X、真实 Y、真实 Z、查询 Q 位。\n"
        "表中逐客户余项非负；各条激励/最大性只在全客户求和后非负。\n\n"
        "| b | a | x | y | z | q | 精确余项 |\n"
        "|---:|---:|---:|---:|---:|---:|---:|\n" + "\n".join(table) + "\n")
    return result


def build_rows():
    lift = json.loads(SOURCES["lift"].read_bytes())
    preflight = json.loads(SOURCES["orbits"].read_bytes())
    container = json.loads(SOURCES["descriptor_container"].read_bytes())
    old_core = lift["original_columns"]
    # Strip all weights at once.  No evaluation at the excluded cb45 point.
    desc = [{k: v for k, v in c.items() if k != "weight"}
            for c in container["columns"][:old_core]]
    full_start = len(container["columns"])
    del container
    assert old_core == 4849 and full_start == 20585
    hist = {j: c for j, c in enumerate(desc) if c["kind"] == "hist"}
    xcols = {}
    overlap = {}
    for index, c in enumerate(lift["new_columns"]):
        full = full_start + index
        h = c["hist_column"]
        if c["kind"] == "common-X-mass":
            xcols[h] = full
        else:
            assert c["kind"] == "X-query-overlap-upper"
            overlap[h, frozen(c["query_token"])] = (
                full, {int(j): F(v) for j, v in c["query_marginal"]})
    assert len(hist) == len(xcols) == 16 and len(overlap) == 420
    income4 = {}
    for h, c in hist.items():
        bits = tuple(map(int, c["actual_bits"]))
        if bits[3]:
            income4[h] = F(1, sum(bits))
    assert income4 == {int(j): F(v) for j, v in lift["incomes"][3]}
    orbits = preflight["all_17_orbits"]
    assert len(orbits) == 17 and sum(o["size"] for o in orbits) == 158
    rows = []
    used_overlap = set()
    for orbit in orbits:
        key = frozen(orbit["orbit"])
        members = [frozen(q) for q in orbit["members"]]
        assert len(members) == orbit["size"]
        row = {j: 10 * v for j, v in income4.items()}
        histogram_frequencies = []
        for h, c in hist.items():
            bits = tuple(map(int, c["actual_bits"]))
            b = sum(bits[:3])
            add(row, xcols[h], -F(9, b + 3))
            words = tuple(w for w, n in zip(WORDS, c["hist"]) for _ in range(n))
            assert len(words) == 6
            tokens = []
            for q in members:
                if q[0] == "A":
                    token = ("bit", bits[q[1]])
                elif q[0] in ("T", "B", "C"):
                    token = ("bit", words[q[1]][("T", "B", "C").index(q[0])])
                elif q[0] == "H":
                    token = q
                else:
                    kind, family, i, j = q
                    token = (kind, (family, int(i == j), words[i], words[j]))
                tokens.append(token)
            frequency = Counter(tokens)
            histogram_frequencies.append({"hist_column": h,
                                          "frequencies": [[t, n] for t, n in frequency.items()]})
            for token, multiplicity in frequency.items():
                average = F(multiplicity, len(members))
                if token[0] == "bit":
                    if token[1]:
                        add(row, h, -average / (b + 1))
                        add(row, xcols[h], 2 * average / ((b + 1) * (b + 3)))
                else:
                    auxiliary, marginal = overlap[h, token]
                    for j, v in marginal.items():
                        add(row, j, -average * v / (b + 1))
                    add(row, auxiliary, 2 * average / ((b + 1) * (b + 3)))
                    used_overlap.add(auxiliary)
        assert all(row.get(j, F()) >= 0 for j, _ in overlap.values())
        assert all(0 <= j < 21021 for j in row)
        rows.append({"name": ["common-X-H3-bridge", *key],
                     "orbit_size": len(members), "query_members": members,
                     "row": sparse(row), "rhs": "0",
                     "histogram_frequencies": histogram_frequencies})
    assert len(used_overlap) == 420
    result = {"scope": "17 homogeneous necessary rows. Append only after separate authorization; this file changes no frozen input.",
              "formula": "10*u4 - 9*sum(X/(p3+3)) - avg_Q sum(Q/(p3+1)) + avg_Q sum(2*XQ/((p3+1)*(p3+3))) >= 0",
              "full_dimension": 21021, "new_columns": 0,
              "row_count": len(rows), "nonzero_count": sum(len(r["row"]) for r in rows),
              "reuses_existing_X_columns": list(sorted(xcols.values())),
              "reuses_existing_overlap_upper_columns_count": len(used_overlap),
              "all_overlap_coefficients_nonnegative": True,
              "canonical_min_preserved": True,
              "fixed_point_evaluated": False, "optimizer_called": False,
              "input_sha256": {k: sha256(p.read_bytes()).hexdigest() for k, p in SOURCES.items()},
              "rows": rows}
    save("rows_17.json", result)
    return result


if __name__ == "__main__":
    atoms = check_atoms()
    rows = build_rows()
    print(json.dumps({"status": "PASS", "atomic_types": atoms["case_count"],
                      "zero_remainders": atoms["zero_count"],
                      "rows": rows["row_count"], "nonzero_count": rows["nonzero_count"],
                      "columns": rows["full_dimension"], "new_columns": 0,
                      "existing_overlap_columns_reused": 420,
                      "fixed_point_evaluated": False, "optimizer_called": False},
                     ensure_ascii=False))
