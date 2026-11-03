#!/usr/bin/env python3
"""Read all saved records; pack their complete semantics and audit fixed policies.

No discovery imports, LP, BI, or RNG. Policy strings encode all ordered histories
by increasing depth, then lexicographic order. Inputs remain read-only.
"""
import argparse
import collections
import hashlib
import itertools
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ("full_bi_m5k7.json", "full_m5k7.json")
NAMES = ("decimal", "binary64", "rounded_1000000")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def histories(k, m):
    return [h for d in range(m) for h in itertools.product(range(k), repeat=d)]


def unpack(entry):
    """Reverse the compact encoding, including the original action-list order."""
    k, m = entry["parameters"]["topics"], entry["parameters"]["players"]
    hs = histories(k, m)
    records = []
    for rec in entry["records"]:
        actions = dict(zip(hs, map(int, rec["action_digits"])))
        order = hs if rec["original_action_order"] == "increasing-depth-lexicographic" else [
            h for d in reversed(range(m)) for h in itertools.product(range(k), repeat=d)]
        item = {a:b for a,b in rec.items() if a not in ("certificate_key", "terminal_counts",
                "action_digits", "original_action_order")}
        item[rec["certificate_key"]] = {"terminal_counts": rec["terminal_counts"],
                "actions": [{"history": list(h), "action": actions[h]} for h in order]}
        records.append(item)
    return {"scope": entry["scope"], "parameters": entry["parameters"], "records": records}


def pack(source_dir):
    out = {"format": "ordered-policy-digits-v1", "policy_order":
           "increasing depth then lexicographic history; one base-10 action digit per history",
           "files": []}
    for name in FILES:
        raw = (source_dir / name).read_bytes()
        obj = json.loads(raw)
        assert set(obj) == {"scope", "parameters", "records"}
        entry = {"name": name, "source_size": len(raw), "source_sha256": sha(raw),
                 "scope": obj["scope"], "parameters": obj["parameters"], "records": []}
        k, m = obj["parameters"]["topics"], obj["parameters"]["players"]
        hs = histories(k, m)
        for rec in obj["records"]:
            key = "certificate" if "certificate" in rec else "cert"
            cert = rec[key]
            assert set(cert) == {"terminal_counts", "actions"}
            assert all(set(a) == {"history", "action"} for a in cert["actions"])
            actions = {tuple(a["history"]): a["action"] for a in cert["actions"]}
            assert len(actions) == len(cert["actions"]) == len(hs)
            assert set(actions) == set(hs)
            assert all(type(a) is int and 0 <= a < k for a in actions.values())
            assert cert["terminal_counts"] == rec["root"]
            # Every record field, mass coordinate, and complete action survives.
            item = {a: b for a, b in rec.items() if a != key}
            item["certificate_key"] = key
            item["terminal_counts"] = cert["terminal_counts"]
            item["action_digits"] = "".join(str(actions[h]) for h in hs)
            item["original_action_order"] = ("decreasing-depth-lexicographic" if
                [tuple(a["history"]) for a in cert["actions"]] ==
                [h for d in reversed(range(m)) for h in itertools.product(range(k), repeat=d)]
                else "increasing-depth-lexicographic")
            if item["original_action_order"] == "increasing-depth-lexicographic":
                assert [tuple(a["history"]) for a in cert["actions"]] == hs
            entry["records"].append(item)
        assert unpack(entry) == obj
        entry["parsed_JSON_roundtrip_equal"] = True
        out["files"].append(entry)
    return out


def scaled_masses(weights, interpretation):
    vals = [F(str(v)) if interpretation == "decimal" else F.from_float(v)
            for v in weights.values()]
    if interpretation == "rounded_1000000":
        vals = [F(str(v)).limit_denominator(1000000) for v in weights.values()]
    den = math.lcm(*(v.denominator for v in vals))
    return [int(mask) for mask in weights], [v.numerator * (den // v.denominator) for v in vals], den


def audit_record(rec, k, m):
    hs = histories(k, m)
    assert len(rec["action_digits"]) == len(hs)
    actions = dict(zip(hs, map(int, rec["action_digits"])))
    terminal = {}
    for h in itertools.product(range(k), repeat=m):
        terminal[h] = tuple(h.count(a) for a in range(k))
    for h in reversed(hs):
        terminal[h] = terminal[h + (actions[h],)]
    root = terminal[()]
    assert list(root) == rec["root"] == rec["terminal_counts"]
    path, h = [], ()
    while h in actions:
        a = actions[h]
        path.append(a)
        h += (a,)
    if "path" in rec:
        assert path == rec["path"]
    assert rec["target_action"] in path
    comp = rec["comparison"]
    assert len(comp) == min(k, m) and len(set(comp)) == len(comp)
    assert all(0 <= a < k for a in comp)
    L = math.lcm(*range(1, m + 1))
    all_masks = range(1, 1 << k)
    coefficient_cache = {}

    def coefficients(q, a):
        key = q, a
        if key not in coefficient_cache:
            row = tuple((L // sum(q[b] for b in range(k) if mask >> b & 1))
                        if mask >> a & 1 else 0 for mask in all_masks)
            coefficient_cache[key] = row
        return coefficient_cache[key]

    rows, locations = [], []
    for h in hs:
        a = actions[h]
        chosen = coefficients(terminal[h], a)
        for b in range(k):
            if b == a:
                continue
            other = coefficients(terminal[h + (b,)], b)
            rows.append(tuple(x - y for x, y in zip(chosen, other)))
            locations.append((h, a, b))
    # Compare the exact row count against every stored BI unique-row count.
    unique_count = len(set(rows))
    if "unique_rows" in rec:
        assert unique_count == rec["unique_rows"]
    result = {a: b for a, b in rec.items() if a not in
              ("action_digits", "weights", "certificate_key", "terminal_counts", "original_action_order")}
    result.update({"ordered_nodes_checked": len(hs), "nonself_IC_checked": len(rows),
                   "unique_rows_rebuilt": unique_count, "root_path_rebuilt": path,
                   "policy_sha256": sha(rec["action_digits"].encode()),
                   "fresh_at_all_nodes": all(a not in h for h, a in actions.items()),
                   "support_size": len(rec["weights"]), "interpretations": {}})
    cover = lambda q, masks: [int(any(q[a] and mask >> a & 1 for a in range(k))) for mask in masks]
    for name in NAMES:
        masks, mass, D = scaled_masses(rec["weights"], name)
        assert all(1 <= b < 1 << k for b in masks) and min(mass) >= 0
        projected = [tuple(row[b-1] for b in masks) for row in rows]
        slacks = [sum(c*v for c, v in zip(row, mass)) for row in projected]
        low = min(slacks)
        pos = slacks.index(low)
        uh = [sum(coefficients(root, a)[b-1]*v for b, v in zip(masks, mass)) for a in path]
        W = sum(c*v for c, v in zip(cover(root, masks), mass))
        covers = [(sum(v for b, v in zip(masks, mass) if any(b >> a & 1 for a in J)), J)
                  for J in itertools.combinations(range(k), min(k, m))]
        opt, optJ = max(covers)
        ccomp = sum(v for b, v in zip(masks, mass) if any(b >> a & 1 for a in comp))
        target_u = sum(coefficients(root, rec["target_action"])[b-1]*v for b, v in zip(masks, mass))
        fh, fa, fb = locations[pos]
        result["interpretations"][name] = {
            "mass_sum": str(F(sum(mass), D)), "valid_complete_policy": low >= 0,
            "negative_nonself_IC": sum(s < 0 for s in slacks),
            "min_IC_slack": str(F(low, L*D)), "min_IC_slack_float": float(F(low, L*D)),
            "min_slack_at": {"history": fh, "chosen": fa, "deviation": fb},
            "W": str(F(W, D)), "OPT": str(F(opt, D)), "OPT_support": optJ,
            "saved_comparison_coverage": str(F(ccomp, D)),
            "root_payoffs": [str(F(u, L*D)) for u in uh],
            "saved_target_value_recomputed": str(F(L*(ccomp-W)-m*target_u, L*D)),
            "half_margin_2W_minus_OPT": str(F(2*W-opt, D)),
        }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", type=Path)
    ap.add_argument("--out", type=Path, default=HERE / "fixed-policy-audit.json")
    args = ap.parse_args()
    started = time.monotonic()
    if args.source_dir:
        data = pack(args.source_dir)
        (HERE / "saved-policy-semantics.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")
    else:
        data = json.loads((HERE / "saved-policy-semantics.json").read_text())
    out = {"scope": "fixed stored support and complete ordered policies only; no LP-optimality assertion",
           "interpretations": {"decimal": "Fraction(str(JSON float))", "binary64":
             "Fraction.from_float(JSON float)", "rounded_1000000":
             "Fraction(str(JSON float)).limit_denominator(1000000); a separately defined input"},
           "files": []}
    for entry in data["files"]:
        k, m = entry["parameters"]["topics"], entry["parameters"]["players"]
        records = [audit_record(r, k, m) for r in entry["records"]]
        summary = {"name": entry["name"], "source_sha256": entry["source_sha256"],
                   "source_size": entry["source_size"], "parameters": entry["parameters"],
                   "parsed_JSON_roundtrip_equal": entry.get("parsed_JSON_roundtrip_equal", False),
                   "saved_records": len(records), "ordered_nodes_checked": sum(r["ordered_nodes_checked"] for r in records),
                   "nonself_IC_checked_per_interpretation": sum(r["nonself_IC_checked"] for r in records),
                   "saved_value_min": min(r["value"] for r in records),
                   "saved_value_max": max(r["value"] for r in records),
                   "valid_complete_policy_counts": {name: sum(r["interpretations"][name]["valid_complete_policy"] for r in records) for name in NAMES},
                   "fresh_policy_count": sum(r["fresh_at_all_nodes"] for r in records),
                   "record_audits": records}
        out["files"].append(summary)
        print(json.dumps({a:b for a,b in summary.items() if a != "record_audits"}), flush=True)
    out["elapsed_seconds"] = time.monotonic() - started
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__":
    main()
