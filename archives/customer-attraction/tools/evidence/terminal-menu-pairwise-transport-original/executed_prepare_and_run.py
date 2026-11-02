"""Copy frozen sources and one archived dependency; execute original main once.

No source mutation, Git operation, optimization, or SPE search occurs here.
"""
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent / "co-work-anl-boss8"
E = BASE / "staging/archives/customer-attraction/tools/evidence/terminal-menu-pairwise-transport-original"
SOURCE_DIR = BASE.parent / "sources"
INPUT = ROOT / "archives/customer-attraction/tools/evidence/R486-same-query-clique-20261101/enhanced_2396_exact_obstruction.json"
PATH_PREFIX = "research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

active = {x["id"]: x for x in json.loads((BASE.parent / "active.json").read_text())}
manifest = []
for sid, suffix in [("a9876e6a3e564fb0b8e1", "py"), ("1df0962f1a3930e8c225", "json")]:
    item = active[sid]
    src = SOURCE_DIR / (sid + "." + suffix)
    dst = E / "original/round3_indexed" / ("transport_bounds." + suffix)
    dst.parent.mkdir(parents=True, exist_ok=True)
    assert src.stat().st_size == item["size"] and sha(src) == item["sha256"]
    shutil.copyfile(src, dst)
    manifest.append({**item, "preserved_path": str(dst.relative_to(E)), "full_file_read": True})
assert INPUT.stat().st_size == 34584
assert sha(INPUT) == "ce1f9d8b1036256b7e40e1eb5c990fdcc4f33c7fed3f2aa796bdf8245b9d0c4f"
for place in ["original", "replay"]:
    folder = E / place / "next_credible"
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(INPUT, folder / INPUT.name)
replay = E / "replay/round3_indexed"
replay.mkdir(parents=True, exist_ok=True)
shutil.copyfile(E / "original/round3_indexed/transport_bounds.py", replay / "transport_bounds.py")
(E / "source-manifest.json").write_text(json.dumps({"primary_sources": manifest,
    "dependency": {"source_id": "667dc37261628075aedc", "source_path": PATH_PREFIX + "next_credible/" + INPUT.name,
    "source_commits": ["68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"],
    "existing_archive_path": str(INPUT.relative_to(ROOT)), "preserved_path": "original/next_credible/" + INPUT.name,
    "size": INPUT.stat().st_size, "sha256": sha(INPUT)}}, ensure_ascii=False, indent=2) + "\n")
before = {str(p.relative_to(E)): sha(p) for p in [E/"original/round3_indexed/transport_bounds.py", E/"original/round3_indexed/transport_bounds.json", E/"original/next_credible"/INPUT.name, replay/"transport_bounds.py", E/"replay/next_credible"/INPUT.name]}
start = time.perf_counter()
proc = subprocess.run([sys.executable, str(replay/"transport_bounds.py")], cwd=replay,
    capture_output=True, text=True, check=False)
elapsed = time.perf_counter() - start
(E / "replay/stdout.txt").write_text(proc.stdout)
(E / "replay/stderr.txt").write_text(proc.stderr)
out = replay / "transport_bounds.json"
assert proc.returncode == 0 and not proc.stderr
same = out.read_bytes() == (E/"original/round3_indexed/transport_bounds.json").read_bytes()
after = {p: sha(E/p) for p in before}
assert before == after
record = {"event": "one normal CLI invocation of unchanged original main", "argv": proc.args,
    "cwd": str(replay), "python": platform.python_version(), "returncode": proc.returncode,
    "elapsed_seconds": elapsed, "original_main_invocations": 1, "stdout_size": len(proc.stdout.encode()),
    "stderr_size": len(proc.stderr.encode()), "report_size": out.stat().st_size,
    "report_sha256": sha(out), "report_equals_frozen_bytes": same,
    "immutable_files_before": before, "immutable_files_after": after,
    "optimization_or_SPE_search_runs": 0}
(E / "replay/execution.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
assert same
print(json.dumps(record, ensure_ascii=False, indent=2))
