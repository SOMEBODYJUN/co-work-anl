"""Bind the sole full-X numerical discovery to its pushed source; no optimizer."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
WS = HERE.parent
COMMIT = "ef43da7b2a1bdf1bdaa06e302586dc4a3748a13a"
REQUEST = "C-six-boss1-maxb-full-lift-22297-01"
ZIP_SHA = "17eae6d1b6d1c89d33baab3434f772893b213fa56584a75419e0320469b13160"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
zpath = HERE / "maxb-full-artifact-13889091562.zip"
assert sha(zpath) == ZIP_SHA
with zipfile.ZipFile(zpath) as z:
    assert z.testzip() is None
    for info in z.infolist():
        p = Path(info.filename)
        assert not p.is_absolute() and ".." not in p.parts
        assert ((info.external_attr >> 16) & 0o170000) != 0o120000
raw = zpath.with_suffix("")
result_path = raw / "validation/compute" / REQUEST / "result.json"
result = read(result_path)
assert result["commit"] == COMMIT and result["request_id"] == REQUEST
assert result["status"] == "completed" and result["exit_code"] == 0
full = WS / "maxb_augmented_lp/full_lift"
request = read(full / "actions_request.json")
expected = {v["path"]: v["sha256"] for v in request["required_inputs"]}
assert len(expected) == 6
assert {v["path"]: v["sha256"] for v in result["input_files"]} == expected
assert result["spec"]["expected_input_sha256"] == expected
for name, digest in expected.items():
    assert sha(ROOT / name) == digest
    blob = subprocess.check_output(["git", "show", COMMIT + ":" + name], cwd=ROOT)
    assert hashlib.sha256(blob).hexdigest() == digest
relout = request["output_directory"]
assert result["output_paths"] == [relout]
src = raw / relout
manifest = read(src / "output_manifest.json")
for item in manifest["files"]:
    p = src / item["name"]
    assert p.stat().st_size == item["bytes"] and sha(p) == item["sha256"]
assert {p.name for p in src.iterdir()} == {v["name"] for v in manifest["files"]} | {"output_manifest.json"}
aim = read(src / "actions_input_manifest.json")
runtime = read(full / "runtime_inputs_manifest.json")
assert aim["runtime_inputs_manifest"] == runtime
assert aim["inputs"] == runtime["inputs"]
assert aim["runtime_inputs_manifest_sha256"] == sha(full / "runtime_inputs_manifest.json")
assert (src / "executed_actions_solve.py").read_bytes() == (full / "actions_solve.py").read_bytes()
execution = read(src / "execution.json")
assert execution["exit_code"] == 0
assert execution["source_sha256"] == sha(full / "actions_solve.py")
assert execution["stdout_sha256"] == sha(src / "solver_stdout.txt")
assert execution["stderr_sha256"] == sha(src / "solver_stderr.txt")
num = read(src / "numerical_result.json")
assert num["matrix_sha256"] == sha(full / "exact_matrix.json.gz")
assert num["floating_problem_sha256"] == sha(full / "floating_problem.npz")
assert num["arrays_sha256"] == sha(src / "floating_solver_arrays.npz")
assert num["optimizer_calls"] == 1 and num["success"] and num["status_code"] == 0
assert num["exact_verified"] is False
with np.load(src / "floating_solver_arrays.npz", allow_pickle=False) as arrays:
    shapes = {k: list(arrays[k].shape) for k in arrays.files}
    assert tuple(arrays["shape"]) == (22297, 21021)
    assert arrays["primal"].shape == (21021,)
    assert arrays["row_multipliers_unscaled"].shape == (22297,)
    assert arrays["equality_marginals"].shape == (1,)
    assert arrays["computed_dual_residual"].shape == (21021,)
    assert int(arrays["optimizer_calls"]) == 1
    for key in ("primal", "row_multipliers_unscaled", "computed_row_slacks", "computed_dual_residual"):
        assert np.isfinite(arrays[key]).all()
dst = ROOT / relout
assert not dst.exists(), "Never overwrite a received immutable discovery."
shutil.copytree(src, dst)
for p in src.iterdir():
    assert p.read_bytes() == (dst / p.name).read_bytes()
audit = {
    "status": "PASS_PROVENANCE_AND_BYTE_IDENTICAL_IMPORT_NOT_EXACT_LP_CERTIFICATE",
    "source_commit": COMMIT, "request_id": REQUEST,
    "run_id": 43091082992, "job_id": 130768110298, "artifact_id": 13889091562,
    "zip_sha256": ZIP_SHA, "result_sha256": sha(result_path),
    "six_input_hashes": expected, "output_manifest_sha256": sha(src / "output_manifest.json"),
    "arrays_sha256": num["arrays_sha256"], "array_shapes": shapes,
    "numerical_W": num["W_float"], "numerical_status": num["message"],
    "numeric_solver_seconds": num["solver_seconds"], "optimizer_calls": 1,
    "exact_verified": False,
    "next": "Original agent restores exact freeW primal, exact dual and independent all-row/all-column verification.",
    "script_sha256": sha(Path(__file__)),
}
out = HERE / "maxb-full-artifact-audit.json"
assert not out.exists()
out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: audit[k] for k in ("status", "source_commit", "artifact_id", "numerical_W", "exact_verified")}, indent=2))
