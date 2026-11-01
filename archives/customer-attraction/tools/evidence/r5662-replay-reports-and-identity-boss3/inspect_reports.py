"""Check frozen report bindings and already saved evidence; no math entry run."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent


def read(relative):
    return json.loads((HERE / relative).read_text())


def main():
    manifest = read("source-manifest.json")
    for entry in manifest:
        path = HERE / entry["evidence_path"]
        assert path.stat().st_size == entry["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    tail = read("original/tail3_B_projection_review.json")
    old_stdout = read("related/tail3-parent-stdout.json")
    independent = read("related/tail3-independent-audit.json")
    mapping = {"raw_states_with_overlap": "states", "visible_types": "visible_types",
               "old_point_value": "point_value", "old_point_sha256": "old_sha256"}
    for saved, output in mapping.items():
        assert tail[saved] == old_stdout[output]
    assert tail["status"] == "passed"
    assert tail["raw_states_with_overlap"] == independent["raw_overlap_states"] == 64 * 4 * math.comb(9, 3)
    assert tail["visible_types"] == independent["visible_cells"] == 64 * 7
    assert F(tail["old_point_value"]) == F(independent["old_point_value"]) < 0
    old_raw = (HERE / "related/old-full-new-reply-point.json").read_bytes()
    assert hashlib.sha256(old_raw).hexdigest() == tail["old_point_sha256"] == independent["old_point_sha256"]
    terminal = read("original/terminal_closure_replay.json")
    pair_raw = (HERE / "related/pair_closure_exact.json").read_bytes()
    pair = json.loads(pair_raw)
    assert hashlib.sha256(pair_raw).hexdigest() == terminal["point_sha256"]
    assert terminal["rows"] == pair["rows"] == 7931
    assert F(terminal["W"]) == F(pair["W"]) < F(1, 2)
    assert terminal["minimum_slack"] == pair["minimum_slack"] == "0"
    assert len(pair["variables"]) == pair["original_Z_variables"] == 275
    assert pair["overlap_variables"] == 1903
    assert 3945 + 60 + 120 + 2 * 1903 == 7931
    current_code_sha = hashlib.sha256((HERE / "related/pair_closure_current_frozen.py").read_bytes()).hexdigest()
    assert current_code_sha == "bf72caf986685f6db6ae22106cf531d2314f19cf636621136804d685ed524f91"
    assert current_code_sha != terminal["source_sha256"]
    identity = read("original/workspace.json")
    assert identity == {"schema": 1, "save": "customer-attraction",
                        "actor": "R-5662d5cb0e5845a980ed10a3b3224cb1",
                        "instance": "d124437d66d446b1a5e007751f19b149"}
    result = {"status": "passed-report-binding-and-existing-evidence-comparison",
              "primary_count": 3,
              "tail_report_field_mapping": mapping,
              "tail_report_all_four_math_fields_equal_existing_stdout": True,
              "tail_report_all_four_math_fields_equal_existing_independent_report": True,
              "terminal_report_point_sha_and_header_equal": True,
              "terminal_point_header_only_review": {key: pair[key] for key in pair if key != "variables"},
              "terminal_reported_source_sha": terminal["source_sha256"],
              "current_frozen_pair_program_sha": current_code_sha,
              "same_code_version": False,
              "original_research_entries_run": 0,
              "new_hidden_state_enumerations": 0,
              "new_matrix_replays": 0,
              "new_point_full_coordinate_audits": 0,
              "identity": identity}
    (HERE / "inspection.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "primary_count": 3, "same_code_version": False}))


if __name__ == "__main__":
    main()
