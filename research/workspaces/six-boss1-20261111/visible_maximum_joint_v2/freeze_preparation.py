#!/usr/bin/env python3
"""Freeze the fully checked1003-row preparation; authorizes no optimizer."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sha = lambda p: sha256(p.read_bytes()).hexdigest()
dump = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")
assert not (HERE / "freeze_manifest.json").exists(), "Already frozen; preserve this preparation."
for prohibited in ["solve_once.py", "single_lp_consumed.json", "single_lp_started.txt", "discovery_output.json"]:
    assert not (HERE / prohibited).exists(), prohibited
data = json.loads((HERE / "exact_input.json").read_text())
build = json.loads((HERE / "build_result.json").read_text())
check = json.loads((HERE / "independent_precheck_result.json").read_text())
assert build["optimizer_calls"] == data["optimizer_calls"] == 0
assert data["preparation_only"]["optimization_authorized"] is False
assert build["input_sha256"] == sha(HERE / "exact_input.json")
assert check["new_input_sha256"] == sha(HERE / "exact_input.json")
assert (str(check.get("status", "")) + " " + str(check.get("result", ""))).find("PASS") >= 0
assert check["optimizer_calls"] == 0
assert len(data["raw_rows"]) == 1003 and data["variables"] == 513 and len(data["equalities"]) == 2
sources = json.loads((HERE / "source_pins.json").read_text())["sources"]
for relative, expected in sources.items():
    assert sha(REPO / relative) == expected, (relative, "frozen dependency changed")
dump(HERE / "final_source_verification.json", {"status": "PASS_ALL41_SOURCES_UNCHANGED", "optimizer_calls": 0,
     "source_count": len(sources), "sources": sources})
adjacent = HERE.parent / "visible_maximum_joint_v2.md"
assert adjacent.exists()
artifacts = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size}
             for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in ["freeze_manifest.json", "SHA256SUMS"]}
artifacts["../visible_maximum_joint_v2.md"] = {"sha256": sha(adjacent), "bytes": adjacent.stat().st_size}
manifest = {
    "status": "PREPARED_NO_OPTIMIZER", "frozen_preparation_only": True,
    "owner": "Boss1", "RUN": "six-boss1-20261111", "frozen_utc": datetime.now(timezone.utc).isoformat(),
    "input_sha256": sha(HERE / "exact_input.json"),
    "baseline_input_sha256": "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33",
    "baseline_certificate_sha256": "8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347",
    "new_row_sha256": "a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba",
    "new_source_manifest_sha256": "3bdfeadb2ad2a48a2f9e0452bdb35dc4fe9002ec86d5aa9679950ca49188f269",
    "raw_inequalities": 1003, "nonnegative_columns": 513, "atom_columns": 512, "equalities": 2,
    "old_raw_rows_literal": 1002, "new_raw_rows": 1,
    "new_row": "SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE", "new_raw_index": 1002,
    "new_original_scale": "300u2+K-288B-12M-5N", "new_numerical_positive_divisor": "300",
    "optimizer_calls": 0, "numerical_optimization_authorized": False,
    "independent_precheck": "PASS", "source_count_verified_unchanged": len(sources),
    "literal_hidden_state_checks": 128, "exact_minima": 8, "literal_six_query_membership_checks": 4096,
    "new_full_column_checks": 513,
    "old_face_diagnostic_only": True,
    "old_face_constant": "-15981204499895866953854050884598865236619/86426960107246755980438461555855802597096",
    "artifacts": artifacts,
    "write_scope": ["research/workspaces/six-boss1-20261111/visible_maximum_joint_v2/",
                    "research/workspaces/six-boss1-20261111/visible_maximum_joint_v2.md"],
    "not_performed": ["optimization", "support restriction", "fixed K", "point completion", "new optimum claim", "SPE existence claim"],
    "future_release": "Await Main separate explicit authorization; no next-call token is consumed by this preparation.",
    "half_status": "OPEN"
}
dump(HERE / "freeze_manifest.json", manifest)
entries = [(name, entry["sha256"]) for name, entry in artifacts.items()]
entries.append(("freeze_manifest.json", sha(HERE / "freeze_manifest.json")))
(HERE / "SHA256SUMS").write_text("".join(digest + "  " + name + "\n" for name, digest in sorted(entries)))
print(json.dumps({"status": manifest["status"], "input_sha256": manifest["input_sha256"],
      "freeze_manifest_sha256": sha(HERE / "freeze_manifest.json"), "SHA256SUMS_sha256": sha(HERE / "SHA256SUMS"),
      "optimizer_calls": 0, "artifacts": len(artifacts)}, indent=2))
