"""Apply the verified one-line audit transcription correction, once, serially.

The ordinary full-menu state label ell is arbitrary. Only the separately
selected witness uses ell_i(g)=g_(i+1). Original frozen evidence is retained.
"""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

ROOT = Path.cwd()
OUT = ROOT / "research/workspaces/map-v2/Boss7/final-review-20261116"
sys.path.insert(0, str(ROOT / "tools"))
import research_runtime as rr


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


path = "archives/unrelated-machines/state/审查/裸Cartesian张量反向放大独立实际稀疏审计--审查.md"
original_path = "archives/unrelated-machines/tools/evidence/tensor-reverse-actual-audit-20261031/original/tensor_reverse_actual_audit_review.md"
old_sha = "fc69adc5dbbdbd9073b8501ec41462c3a52f198487f6dffa7db271732dedfe3f"
original_sha = "55041afcaa86bf12918f76085449b881a08bad0814cbcd1ba4173069f62508f4"
oid = "UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1"
source = ROOT / path
original = ROOT / original_path
old_literal = r"b_i+g_i a_i=\ell_i(g_i)\pmod 2"
new_literal = r"b_i+g_i a_i=\ell_i\pmod 2"
assert sha(source) == old_sha
assert sha(original) == original_sha
assert "b_i+g_i a_i=ell_i (mod 2)" in original.read_text()
text = source.read_text()
assert text.count(old_literal) == 1

registry_path = ROOT / "research/registry.json"
registry = read(registry_path)
old_registry_sha = sha(registry_path)
old_baseline = copy.deepcopy(registry["baseline"])
baseline_path = ROOT / old_baseline["path"]
assert sha(baseline_path) == old_baseline["sha256"]
baseline = read(baseline_path)
affected = [obj for obj in registry["objects"]
            if any(ref["path"] == path for ref in [obj["body"], *obj.get("evidence", [])])]
assert len(affected) == 1 and affected[0]["object_id"] == oid
obj = affected[0]
before = copy.deepcopy(obj)
assert before["version"] == 2
assert before["body"]["path"] != path
for rows in (registry["materials"], baseline["materials"]):
    hits = [row for row in rows if row["path"] == path]
    assert len(hits) == 1 and hits[0]["sha256"] == old_sha

source.write_text(text.replace(old_literal, new_literal))
new_sha = sha(source)
assert source.read_text().replace(new_literal, old_literal) == text
for ref in obj["evidence"]:
    if ref["path"] == path:
        assert ref["sha256"] == old_sha
        ref["sha256"] = new_sha
obj["version"] = 3
obj["objections"] += (
    " 2026-11-16仅按冻结独立审计原文修正附件中一般完整菜单支持的坐标记号"
    "ell_i(g_i)为ell_i；循环见证ell_i(g)=g_(i+1)及所有冻结计算保留。"
    "本对象的一般反向放大陈述、证明、量词和数学状态不变。"
)
for key in ("title", "kind", "truth_status", "model", "statement", "quantifiers",
            "assumptions", "scope", "body", "sources"):
    assert obj[key] == before[key], key
for rows in (registry["materials"], baseline["materials"]):
    next(row for row in rows if row["path"] == path)["sha256"] = new_sha

new_baseline_path = ROOT / "research/registration/baseline-boss7-tensor-audit-notation-20261116.json"
assert not new_baseline_path.exists()
baseline["coverage_note"] = baseline.get("coverage_note", "") + (
    "；Boss7按冻结独立审计原文，仅更正一般完整菜单支持的ell_i坐标转录；"
    "保全部材料分母、主数学陈述、原证明和有限计算字节。"
)
baseline["commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
save(new_baseline_path, baseline)
registry["baseline"] = {"path": new_baseline_path.relative_to(ROOT).as_posix(),
                        "sha256": sha(new_baseline_path)}
proposal = OUT / "tensor-audit-notation-registry-proposed.json"
save(proposal, registry)
result = subprocess.run([sys.executable, "work.py", "research", "register", "--record-file",
                         proposal.relative_to(ROOT).as_posix()], capture_output=True, text=True)
print(result.stdout, end="", flush=True)
print(result.stderr, end="", flush=True)
if result.returncode:
    raise SystemExit(result.returncode)
proposal.unlink()

audit = {
    "status": "registered-local-not-pushed", "reviewer": "Boss7",
    "path": path, "old_sha256": old_sha, "new_sha256": new_sha,
    "old_literal": old_literal, "new_literal": new_literal,
    "source": {"path": original_path, "sha256": original_sha},
    "object_id": oid, "before_object": before, "after_object": obj,
    "old_object_pin": rr.pin(before), "new_object_pin": rr.pin(obj),
    "old_baseline": old_baseline, "new_baseline": registry["baseline"],
    "old_registry_sha256": old_registry_sha, "new_registry_sha256": sha(registry_path),
    "mathematical_contract_changed": False,
    "required_repair_tasks": [
        "boss2-6405-source-repair-74d84ac2223f267e",
        "boss2-wave22-um-repair-b52d66a972227003",
        "boss2-wave10-repair-094b299464e358ff",
        "boss3-sourcefix-repair-8d806bdc7cc35ff1",
    ],
    "next": "Checkpoint source, new baseline and registry together; publish targeted replacements for the four effective done tasks, bind/check their current edges, push, done, assemble and run final gates.",
}
save(OUT / "tensor-audit-notation-erratum.json", audit)
print(json.dumps({k: audit[k] for k in ("status", "object_id", "old_object_pin", "new_object_pin",
                                      "old_sha256", "new_sha256", "required_repair_tasks")},
                 ensure_ascii=False), flush=True)
