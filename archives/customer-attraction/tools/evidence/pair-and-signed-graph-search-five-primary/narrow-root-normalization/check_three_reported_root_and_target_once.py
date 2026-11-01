"""Only reported root path and two coverage fields; no IC, BI, or optimizer."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib
import json
import sys

manifest_path, output_path = map(Path, sys.argv[1:])
if output_path.exists():
    raise SystemExit("refuse to overwrite a previous result")
manifest = json.loads(manifest_path.read_text())
results = []
for source in manifest["rows"]:
    if not source["path"].endswith(".json"):
        continue
    raw = Path(source["local_path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == source["sha256"]
    packet = json.loads(raw)
    n, p = packet["n"], packet["p"]
    entries = packet["strategy_actions"]
    policy = {tuple(e["history"]): e["action"] for e in entries}
    histories = {h for k in range(n) for h in product(range(p), repeat=k)}
    assert len(policy) == len(entries) and set(policy) == histories
    assert all(type(a) is int and 0 <= a < p for a in policy.values())
    assert [tuple(e["history"]) for e in entries] == sorted(histories)
    path = ()
    steps = []
    for _ in range(n):
        a = policy[path]
        steps.append({"history": list(path), "action": a})
        path += (a,)
    root_mask = sum(1 << a for a in set(path))
    target_mask = sum(1 << a for a in packet["target"])
    actual = packet["actual_customer_weights"]
    assert len(actual) == (1 << p) - 1
    assert all(type(w) is int and w >= 0 for w in actual)
    saved = packet["signed_customer_weights"]
    assert len({e["mask"] for e in saved}) == len(saved)
    rational = {e["mask"]: Fraction(e["weight"]) for e in saved}
    assert all(1 <= b < (1 << p) for b in rational)
    coverage = lambda mask: sum((w for b, w in rational.items() if b & mask), Fraction())
    root, target = coverage(root_mask), coverage(target_mask)
    results.append({
        "source_id": source["id"], "source_sha256": source["sha256"],
        "n": n, "p": p, "seed": packet["seed"], "trial": packet["trial"],
        "all_report_fields": list(packet), "complete_policy_entries": len(policy),
        "all_policy_keys_unique_complete_and_sorted": True,
        "root_path_steps": steps, "root_path": list(path),
        "root_count": [path.count(a) for a in range(p)], "root_support_mask": root_mask,
        "target": packet["target"], "target_mask": target_mask,
        "reported_float_value": packet["value"],
        "all_saved_signed_weights": saved,
        "saved_weight_count": len(saved),
        "negative_saved_weights": sum(w < 0 for w in rational.values()),
        "source_actual_customer_total": sum(actual),
        "source_actual_root_coverage": sum(w for b, w in enumerate(actual, 1) if b & root_mask),
        "source_actual_target_coverage": sum(w for b, w in enumerate(actual, 1) if b & target_mask),
        "exact_saved_root_coverage": str(root), "exact_saved_root_minus_one": str(root - 1),
        "saved_root_exactly_one": root == 1,
        "float_saved_root_minus_one": float(root - 1),
        "exact_saved_target_coverage": str(target),
        "exact_saved_target_over_root": str(target / root),
        "float_saved_target_over_root": float(target / root),
        "scope": "only root trajectory, saved coverage normalization and fixed-target field arithmetic; no IC, dilution, BI, solver, or feasibility certificate",
    })
assert len(results) == 3
output_path.write_text(json.dumps({"one_narrow_check": True, "packets": results}, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
print(json.dumps([{"id": r["source_id"], "path": r["root_path"], "root_exactly_one": r["saved_root_exactly_one"], "root_minus_one": r["exact_saved_root_minus_one"], "target": r["exact_saved_target_coverage"], "reported": r["reported_float_value"]} for r in results], ensure_ascii=False))
