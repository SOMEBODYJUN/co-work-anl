"""Read-only pin, byte, exact-section and finite interface identity checks.

This does not run a tail/root IC loop, a solver, BI, LP or policy generation.
Every write is to the explicitly supplied output file outside the input repo.
Run with python -B so importing the native reader creates no repo cache files.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys


TASK = "boss1-wave8-source-repair-repair-5d5ca1e70347ad05"
OLD = "customer-attraction-3a-3a-0bb4847cebdb22cd"
EDGE = f"map/edges/{OLD}/legal-family-to-finite-tail-contribution.json"
P1 = "customer-attraction/actual-prefix-fresh-coverage-global-counterexample"
CHANGED = "archives/customer-attraction/state/障碍/R-2fc背景遗憾探针与无碰撞五客户负载桥--障碍.md"
CORRECTION = "b03a23a02e828a6c920d35db9e315d21da5cd732"
EXPECTED_DEFINITION_PIN = "f7176ff87884881d37dbb7bda50d9cd53ef939c696deaa490d16c2a5a777ea67"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    assert not args.output.resolve().is_relative_to(repo), "Output must be outside the read-only repo"
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repo / "tools"))
    import research_runtime as native

    def read_json(relative):
        return json.loads((repo / relative).read_text())

    task_path = f"research/operations/map-v2/tasks/{TASK}.json"
    old_task_path = f"research/operations/map-v2/tasks/{OLD}.json"
    task, old_task = read_json(task_path), read_json(old_task_path)
    definition = task["definition"]
    assert native.pin(definition) == EXPECTED_DEFINITION_PIN
    assert task["state"] == "claimed" and task["owner"] == "Boss1"
    assert definition["supersedes"] == [OLD] and old_task["state"] == "done"
    registry, objects = native.load(repo, verify=False)
    pin_checks = []
    registered_refs = {}
    for oid, expected in definition["input_pins"].items():
        obj = objects[oid]
        assert native.pin(obj) == expected
        pin_checks.append({"object_id": oid, "version": obj["version"],
                           "old_pin": old_task["definition"]["input_pins"][oid],
                           "current_pin": expected, "matches_task": True})
        for ref in [obj["body"], *obj["evidence"]]:
            raw = native.ref_bytes(repo, ref)
            entry = registered_refs.setdefault(ref["path"], {
                "path": ref["path"], "sha256": digest(raw), "bytes": len(raw),
                "owners": [], "unique_sections_verified": []})
            if oid not in entry["owners"]:
                entry["owners"].append(oid)
            if ref.get("section") and ref["section"] not in entry["unique_sections_verified"]:
                entry["unique_sections_verified"].append(ref["section"])

    old_receipt = read_json(f"map/receipts/{OLD}.json")
    assert old_receipt == old_task["receipt"]
    assert old_receipt["assets"] == definition["context_plan"]["prior_assets"]
    prior_checks = []
    for ref in old_receipt["assets"]:
        raw = native.ref_bytes(repo, ref)
        prior_checks.append(dict(ref, bytes=len(raw), current_bytes_match_old_receipt=True))

    edge = read_json(EDGE)
    assert EDGE in registry["edge_files"]
    native.require_edge_result(edge)
    native.verify_endpoints(repo, edge, objects)
    bindings = native.edge_bindings(repo, edge, objects)
    assert all(edge[key] == value for key, value in bindings.items())
    check = native.check_edge(repo, EDGE)
    assert check["proof_scope"] == "step"
    copies = []
    for name in registry["edge_files"]:
        data = read_json(name)
        if data.get("edge_id") == edge["edge_id"]:
            copies.append(name)
    assert copies == [EDGE]

    base = "archives/customer-attraction/tools/evidence/global-actual-prefix/replay/finite-parameters"
    policy_checks = []
    for p in (2, 3):
        audit = read_json(f"{base}/full-root-p{p}-audit.json")
        raw = (repo / base / audit["policy_file"]).read_bytes()
        n = 2 * p + 2
        assert digest(raw) == audit["policy_sha256"]
        assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
        digits = raw[:-1].decode("ascii")
        assert len(digits) == sum(6 ** i for i in range(n)) == audit["ordered_nodes"]
        assert set(digits) <= set("012345")

        def action(history):
            ordinal = 0
            for label in history:
                ordinal = 6 * ordinal + label
            return int(digits[(6 ** len(history) - 1) // 5 + ordinal])

        actual = ()
        while len(actual) < n:
            actual += (action(actual),)
        prefix = (0,) * p + (1,) * p
        replies = tuple(action(prefix + (label,)) for label in range(6))
        assert actual == prefix + (0, 1) == tuple(audit["actual_path"])
        assert action(prefix) == 0 and replies == (1, 5, 5, 5, 5, 4)
        weights = {1: (p+1)*(p+4), 2: (p+1)*(p+5), 4: 2*p+3, 8: 2*p+3,
                   20: 2, 24: 2, 36: 2, 40: 2, 49: (p+1)*(p+2), 50: (p+1)*(p+2)}
        assert weights == {int(k): v for k, v in audit["weights"].items()}
        assert sum(weights.values()) == 4*p*p+21*p+27 == audit["unit_customers"]
        assert (p+1)*(4*p+13) == audit["root_W"]
        assert audit["root_OPT"] == sum(weights.values())
        policy_checks.append({"p": p, "policy_sha256": digest(raw), "bytes": len(raw),
            "encoding_bytes_checked": True, "actual_path_decoded": list(actual),
            "tail_first_decoded": action(prefix), "tail_replies_decoded": list(replies),
            "family_type_identity": True,
            "mature_audit_ordered_nodes": audit["ordered_nodes"],
            "mature_audit_IC_comparisons": audit["comparisons_including_self"],
            "IC_comparisons_executed_this_round": 0,
            "patched_encoding_generated_this_round": False})

    previous_source = subprocess.check_output(["git", "show", f"{CORRECTION}^:{CHANGED}"], cwd=repo)
    current_source = (repo / CHANGED).read_bytes()
    assert digest(previous_source) == "f7fd1bc59bbfc1090203a9909274ea2b1704f9eaf382fac37272f371cd0c4d07"
    assert previous_source.replace("四个客户的主题集合".encode(), "四个主题的客户集合".encode()) == current_source
    probe_title = "`background_regret_probe.py`：有限 Markov 锥探针"
    assert native.section(previous_source.decode(), probe_title) == native.section(current_source.decode(), probe_title)
    old_registry = json.loads(subprocess.check_output(["git", "show", f"{CORRECTION}^:research/registry.json"], cwd=repo))
    previous_p1 = next(obj for obj in old_registry["objects"] if obj["object_id"] == P1)
    current_p1 = objects[P1]
    assert native.pin(previous_p1) == old_task["definition"]["input_pins"][P1]
    changed_fields = sorted(key for key in set(previous_p1) | set(current_p1)
                            if previous_p1.get(key) != current_p1.get(key))
    assert changed_fields == ["evidence", "objections", "version"]
    assert previous_p1["body"] == current_p1["body"]

    result = {"task_id": TASK, "owner": "Boss1", "worker_marker": "FINITE2-CURRENT",
        "task_definition_pin": native.pin(definition), "request_id": task["request_id"],
        "observed_local_HEAD": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip(),
        "local_state_checked": {"state": task["state"], "owner": task["owner"]},
        "pushed_authorization_provenance": "Parent Boss confirmed pushed before dispatch; no remote query/authentication by worker.",
        "input_pin_checks": pin_checks, "all_six_input_pins_current": True,
        "registered_reference_checks": sorted(registered_refs.values(), key=lambda row: row["path"]),
        "all_registered_reference_bytes_and_unique_sections_match": True,
        "prior_asset_checks": prior_checks,
        "reviewed_edge_id": edge["edge_id"], "canonical_edge_path": EDGE,
        "canonical_edge_sha256": digest((repo / EDGE).read_bytes()),
        "canonical_same_id_paths": copies, "edge_binding_fields_unchanged_current": True,
        "native_readonly_edge_check": check,
        "policy_identity_and_selective_decode": policy_checks,
        "p1_read_input_refresh": {"old_version": previous_p1["version"], "current_version": current_p1["version"],
            "old_pin": native.pin(previous_p1), "current_pin": native.pin(current_p1),
            "changed_record_fields": changed_fields, "primary_body_reference_unchanged": True,
            "changed_source_path": CHANGED, "old_source_sha256": digest(previous_source),
            "current_source_sha256": digest(current_source), "Markov_probe_section_byte_identical": True,
            "source_diff": list(difflib.unified_diff(previous_source.decode().splitlines(), current_source.decode().splitlines(), lineterm="")),
            "mathematical_statement_model_quantifiers_unchanged": True},
        "formal_overlap_comparisons": definition["context_plan"].get("overlap_comparisons", []),
        "execution_boundary": {"tail_IC": 0, "root_IC": 0, "BI": 0, "LP": 0,
            "large_scan": 0, "new_policy_generation": 0, "queue_writes": 0, "git_writes": 0,
            "shared_clone_writes": 0, "native_edge_bind_write": 0,
            "new_native_readonly_edge_check": 1,
            "note": "Full policy SHA/alphabet/length/newline identity plus selected path/reply decode; no all-node semantic or IC rerun."}}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
