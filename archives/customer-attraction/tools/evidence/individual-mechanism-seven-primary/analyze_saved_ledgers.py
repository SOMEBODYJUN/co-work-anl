"""Read every field of all 1171 saved records; no solver or discovery import.

The compact F/G ledger is losslessly reversible, including record order,
original fraction strings, exact_dual flags and all metadata. It certifies
what the reports contain, not the absent primal/dual numerical certificates.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import groupby, combinations
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
WORK = BASE / "original/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/independent_mechanism"


def dump(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


floor = json.loads((WORK / "individual_floor_scan.json").read_text())
gap = json.loads((WORK / "individual_gap_scan.json").read_text())
missed = json.loads((WORK / "missed_union_scan.json").read_text())
assert len(floor) == len(gap) == 490 and len(missed) == 171
common = ("source", "m", "p", "root", "action")
sources = list(dict.fromkeys(row["source"] for row in floor))
for f, g in zip(floor, gap):
    assert set(f) == set(common) | {"ratio", "threshold", "exact_dual"}
    assert set(g) == set(common) | {"gap_over_payoff", "threshold"}
    assert all(f[key] == g[key] for key in common)
    assert type(f["m"]) is int and type(f["p"]) is int
    assert len(f["root"]) == f["m"] and all(type(a) is int and 0 <= a < f["p"] for a in f["root"])
    assert f["action"] in f["root"] and type(f["exact_dual"]) is bool
    assert f["threshold"] == 2 * f["m"] - 1 and g["threshold"] == g["m"]
    assert 0 <= F(f["ratio"]) <= f["threshold"] and 0 <= F(g["gap_over_payoff"]) <= g["threshold"]

encoded = []
decoded_f, decoded_g = [], []
for _, group in groupby(enumerate(floor), key=lambda item: tuple(json.dumps(item[1][key]) for key in common)):
    rows = list(group)
    first = rows[0][1]
    triples = [(f["ratio"], gap[i]["gap_over_payoff"], f["exact_dual"]) for i, f in rows]
    runs = [{"floor_ratio": key[0], "gap_ratio": key[1], "exact_dual": key[2], "repeat": len(list(values))}
            for key, values in groupby(triples)]
    record = {key: first[key] for key in common}
    encoded.append({"metadata": record, "runs": runs, "records": len(rows)})
    for run in runs:
        for _ in range(run["repeat"]):
            decoded_f.append(record | {"ratio": run["floor_ratio"], "threshold": 2 * record["m"] - 1, "exact_dual": run["exact_dual"]})
            decoded_g.append(record | {"gap_over_payoff": run["gap_ratio"], "threshold": record["m"]})
assert decoded_f == floor and decoded_g == gap

missed_encoded = []
decoded_m = []
for key, group in groupby(missed, key=lambda r: (r["source"], r["m"], r["p"], tuple(r["root_counts"]))):
    rows = list(group)
    source, m, p, root = key
    assert len(root) == p and sum(root) == m and all(type(c) is int and c >= 0 for c in root)
    for row in rows:
        assert set(row) == {"source", "m", "p", "root_counts", "missed_over_W", "threshold", "portfolio"}
        assert row["threshold"] == 1 and 0 <= F(row["missed_over_W"]) <= 1
        assert row["portfolio"] == sorted(set(row["portfolio"])) and len(row["portfolio"]) == min(m, p)
        assert all(type(a) is int and 0 <= a < p for a in row["portfolio"])
    portfolios = [r["portfolio"] for r in rows]
    assert portfolios == list(map(list, combinations(range(p), min(m, p))))
    pair_rows = [[r["portfolio"], r["missed_over_W"]] for r in rows]
    missed_encoded.append({"source": source, "m": m, "p": p, "root_counts": root, "pairs": pair_rows})
    decoded_m.extend({"source": source, "m": m, "p": p, "root_counts": list(root), "portfolio": portfolio, "missed_over_W": value, "threshold": 1} for portfolio, value in pair_rows)
assert decoded_m == missed

by_m = []
for m in sorted({r["m"] for r in floor}):
    f = [r for r in floor if r["m"] == m]
    g = [r for r in gap if r["m"] == m]
    z = [r for r in missed if r["m"] == m]
    by_m.append({"m": m, "floor_records": len(f), "gap_records": len(g), "missed_records": len(z),
                 "floor_max": str(max(F(r["ratio"]) for r in f)), "gap_max": str(max(F(r["gap_over_payoff"]) for r in g)),
                 "missed_max": str(max(F(r["missed_over_W"]) for r in z)), "floor_exact_dual_true": sum(r["exact_dual"] for r in f)})
by_source = []
for source in sources:
    f = [r for r in floor if r["source"] == source]
    g = [r for r in gap if r["source"] == source]
    z = [r for r in missed if r["source"] == source]
    by_source.append({"source": source, "m_p": sorted(set((r["m"], r["p"]) for r in f)),
                      "floor_records": len(f), "gap_records": len(g), "missed_records": len(z),
                      "floor_exact_dual_true": sum(r["exact_dual"] for r in f),
                      "floor_max": str(max(F(r["ratio"]) for r in f)), "gap_max": str(max(F(r["gap_over_payoff"]) for r in g)),
                      "missed_max": str(max(F(r["missed_over_W"]) for r in z))})
summary = {"status": "all-saved-record-fields-parsed-and-losslessly-roundtripped",
           "floor_records": len(floor), "gap_records": len(gap), "missed_records": len(missed), "total_records": 1171,
           "source_path_strings": len(sources), "source_and_root_groups_in_missed": len(missed_encoded),
           "floor_exact_dual_true": sum(r["exact_dual"] for r in floor), "floor_exact_dual_false": sum(not r["exact_dual"] for r in floor),
           "floor_gap_metadata_positionwise_equal": True, "all_saved_objectives_at_or_below_threshold": True,
           "missed_portfolios_complete_within_each_saved_source_root_group": True,
           "floor_gap_portfolios_stored": False, "primal_weights_stored": False, "dual_vectors_stored": False,
           "new_LP_or_game_solver_executed": False, "new_original_scan_replay_executed": False,
           "by_m": by_m, "by_source": by_source,
           "raw_json_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (WORK / "individual_floor_scan.json", WORK / "individual_gap_scan.json", WORK / "missed_union_scan.json")}}
dump("full-lossless-ledger.json", {"field_schema": {"floor_threshold": "2*m-1", "gap_threshold": "m", "missed_threshold": 1}, "paired_floor_gap_runs": encoded, "missed_groups": missed_encoded})
dump("ledger-analysis.json", summary)
print(json.dumps({key: summary[key] for key in ("status", "total_records", "floor_exact_dual_true", "floor_exact_dual_false", "source_path_strings", "source_and_root_groups_in_missed", "by_m")}, indent=2))
