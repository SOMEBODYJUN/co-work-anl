"""Read-only verification of recovery 3036; no Git, network, or queue mutations."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "tools"))
import research_runtime as research
import map_tasks

WORK = Path(__file__).resolve().parent
NEW_ID = "boss2-wave22-um-repair-303633f45e196d68"
OLD_ID = "unrelated-machines-3a-3a-3826ce877d049abc"


def read_json(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def finite_cluster_checks():
    """New exact local checks, distinct from every historical whole-tree audit."""
    rows = []
    for k in range(1, 33):
        terminal_weights = []
        for ell in range(1, k + 1):
            weights = [Fraction(1, k), Fraction(ell - 1, k), Fraction(k - ell, k)]
            assert all(w >= 0 for w in weights) and sum(weights) == 1
            terminal_weights.append([str(w) for w in weights])
        for ell in range(1, k):
            assert Fraction(k - ell, k) + Fraction(ell, k) == 1
        assert sum(Fraction(1, k) for _ in range(k)) == 1
        rows.append({"k": k, "all_terminal_probabilities_and_blocker_coverages_valid": True})

    path_rows = []
    for k in range(1, 13):
        injective = []
        for bits in product((0, 1), repeat=k - 1):
            loads = [0] * k
            for ell, side in enumerate(bits):
                loads[ell + side] += 1
            if max(loads) <= 1:
                injective.append(loads.index(0))
        assert len(injective) == k and set(injective) == set(range(k))
        path_rows.append({"k": k, "injective_path_orientations": len(injective), "free_terminal_count": 1})

    opt_rows = []
    for k in range(4, 9):
        # Incoming job is fixed at parent with time 1. Each star has parent
        # time 1/k or own terminal time 1; each path blocker has two unit ends.
        best = None
        count = 0
        for bits in product((0, 1), repeat=2 * k - 1):
            loads = [0] * (k + 1)
            loads[0] = k  # all loads are integer multiples of 1/k
            for ell in range(k):
                loads[ell + 1 if bits[ell] else 0] += k if bits[ell] else 1
            for ell, side in enumerate(bits[k:]):
                loads[ell + 1 + side] += k
            peak = max(loads)
            best = peak if best is None else min(best, peak)
            count += 1
        assert Fraction(best, k) == 2 - Fraction(1, k)
        assert 2 - Fraction(1, k) > 1 + Fraction(1, k)
        # Local machine graph: parent, k terminals, k star edges, k-1 path edges.
        cycle_rank = (2 * k - 1) - (k + 1) + 1
        assert cycle_rank == k - 1 and cycle_rank > 1
        opt_rows.append({"k": k, "assignments": count, "local_forced_incoming_optimum": str(Fraction(best, k)), "cycle_rank": cycle_rank})

    escape_rows = []
    for k in range(4, 33):
        ratio = Fraction(k, k - 1)
        alpha = Fraction(1, k - 1)
        height = 1
        while alpha < Fraction(1, 2):
            alpha *= ratio
            height += 1
        assert height >= 3
        lower = Fraction(2 ** (height - 1), 2)
        theta = 2 - Fraction(1, k)
        assert lower >= 2 > theta
        assert theta / (1 + Fraction(1, k)) == 2 - Fraction(3, k + 1)
        escape_rows.append({"k": k, "height": height, "four_or_more_active_clusters": True, "z_load_lower_bound": str(lower)})
    return {"terminal_configuration_checks": rows, "path_occupancy_checks": path_rows, "local_assignment_enumerations": opt_rows, "escape_formula_checks": escape_rows,
            "limits": "Only new local path/star-cluster enumerations and exact formula checks. No historical CLI, full original tree, source-hardness proof, or generic scheduling solver was rerun."}


def main():
    new = read_json(f"research/operations/map-v2/tasks/{NEW_ID}.json")
    old = read_json(f"research/operations/map-v2/tasks/{OLD_ID}.json")
    definition = new["definition"]
    assert new["state"] == "claimed" and new["owner"] == "Boss6"
    registry, objects = research.load(ROOT, verify=False)
    ids = definition["object_ids"] + definition["read_object_ids"]
    assert len(ids) == len(set(ids))
    for oid in ids:
        assert research.pin(objects[oid]) == definition["input_pins"][oid]
        research.ref_bytes(ROOT, objects[oid]["body"])
        for ref in objects[oid]["evidence"]:
            research.ref_bytes(ROOT, ref)
    for ref in definition["context_plan"]["reading_refs"]:
        research.ref_bytes(ROOT, ref)

    changed = [oid for oid in ids if old["definition"]["input_pins"].get(oid) != definition["input_pins"][oid]]
    assert changed == ["UM-SIMPLE-SUPPORT-GAP-v1"]
    old_object = next(o for o in read_json("research/registration/batches/register-ab98f323ad-0101.json")["objects"] if o["object_id"] == changed[0])
    current = objects[changed[0]]
    assert research.pin(old_object) == old["definition"]["input_pins"][changed[0]]
    fields = sorted(k for k in set(old_object) | set(current) if old_object.get(k) != current.get(k))
    assert fields == ["evidence", "objections", "version"]
    assert old_object["body"] == current["body"]
    for key in ("title", "kind", "truth_status", "model", "statement", "quantifiers", "assumptions", "scope", "sources"):
        assert old_object[key] == current[key]

    prior = read_json(f"map/receipts/{OLD_ID}.json")
    assert old["receipt"] == prior
    assert prior["assets"] == definition["context_plan"]["prior_assets"]
    checks = []
    for asset in prior["assets"]:
        assert sha(asset["path"]) == asset["sha256"]
        assert asset["path"] in registry["edge_files"]
        result = research.check_edge(ROOT, asset["path"])
        edge = read_json(asset["path"])
        assert changed[0] not in edge["source_ids"] + edge["target_ids"]
        assert all(ref["path"] != current["evidence"][1]["path"] for ref in edge["evidence"])
        checks.append({**asset, **result})

    report = {
        "task_id": NEW_ID,
        "predecessor_task_id": OLD_ID,
        "owner_snapshot": {"state": new["state"], "owner": new["owner"], "task_sha256": sha(f"research/operations/map-v2/tasks/{NEW_ID}.json")},
        "current_registration_inputs_verified": len(ids),
        "current_reading_ref_bindings_verified": len(definition["context_plan"]["reading_refs"]),
        "changed_objects": changed,
        "changed_registration_fields": fields,
        "old_registration_pin": research.pin(old_object),
        "current_registration_pin": research.pin(current),
        "old_source_bytes_retrieved": False,
        "old_source_literal_diff_claimed": False,
        "native_edge_checks": checks,
        "finite_checks": finite_cluster_checks(),
        "preservation_pins": {f"research/operations/map-v2/tasks/{OLD_ID}.json": sha(f"research/operations/map-v2/tasks/{OLD_ID}.json"), f"map/receipts/{OLD_ID}.json": sha(f"map/receipts/{OLD_ID}.json"), **{a["path"]: a["sha256"] for a in prior["assets"]}},
    }
    receipt_path = ROOT / f"map/receipts/{NEW_ID}.json"
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text())
        relations = research.edges(ROOT, {"edge_files": [a["path"] for a in receipt["assets"]]}, objects)
        map_tasks._map_receipt_coverage(definition, receipt, objects, relations)
        research.validate_map_follow_ups(definition, receipt, [old], objects)
        map_tasks._supersession(ROOT, definition, receipt, [old], "map")
        assert receipt["assets"] == prior["assets"]
        assert receipt["closed_overlaps"] == [] and receipt["follow_up_tasks"] == []
        report["receipt_validation"] = {"status": "passed", "path": receipt_path.relative_to(ROOT).as_posix(), "sha256": sha(receipt_path.relative_to(ROOT)), "coverage_count": len(receipt["coverage"]), "retained_asset_count": len(receipt["assets"])}
    (WORK / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "passed", "objects": len(ids), "changed_objects": changed, "native_edge_checks": len(checks), "receipt_validation": report.get("receipt_validation"), "report": str(WORK / "verification.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
