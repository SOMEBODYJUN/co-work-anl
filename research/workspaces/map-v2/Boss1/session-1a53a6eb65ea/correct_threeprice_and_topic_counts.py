"""Apply two exact source-count errata without changing mathematical claims.

Run after preserving and handing off the two affected unfinished Boss1 tasks.
Original scientific programs and frozen outputs remain byte-identical.
"""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

ROOT = Path.cwd()
OUT = ROOT / "research/workspaces/map-v2/Boss1/session-1a53a6eb65ea"
sys.path.insert(0, str(ROOT / "tools"))
import research_runtime as rr


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


changes = [
    {
        "path": "archives/customer-attraction/state/障碍/R-373d背景支撑分支缺口与三价模板精确障碍--障碍.md",
        "old_sha": "cf49f19e387bfde165b976c0133613424b5ff10a26bb03944b4de12bda96d39e",
        "old_text": "输出给出 700 个整数类型的 multiplicity",
        "new_text": "候选域共有 192 型；冻结输出给出其中 9 个正支撑整数类型的 multiplicity",
        "reason": "The original loop has 2^5 binary choices, three d choices and two ell choices; the frozen JSON contains nine strictly positive multiplicities.",
    },
    {
        "path": "archives/customer-attraction/state/障碍/R-2fc背景遗憾探针与无碰撞五客户负载桥--障碍.md",
        "old_sha": "f7fd1bc59bbfc1090203a9909274ea2b1704f9eaf382fac37272f371cd0c4d07",
        "old_text": "源报告对应四个客户的主题集合",
        "new_text": "源报告对应四个主题的客户集合",
        "reason": "The frozen input has four topic sets on five unit clients; only the nouns in this sentence were transposed.",
    },
]
expected = {
    "M-de2542fe4dcc45b59d358b5d2f899baa": 1,
    "M-837fb8766b1f4b77ad33225a292f0d27": 2,
    "CA-COLLISION-FREE-LOAD-PAYMENT-NO": 3,
    "customer-attraction/actual-prefix-fresh-coverage-global-counterexample": 4,
}
for tid in [
    "customer-attraction-3a-3a-e3998ab1da2cfd7d",
    "customer-attraction-3a-3a-dfb07ef8d1f88657",
]:
    task = json.loads((ROOT / "research/operations/map-v2/tasks" / (tid + ".json")).read_text())
    assert task["state"] == "handoff" and task.get("owner") is None, tid

regpath = ROOT / "research/registry.json"
old_registry_sha = sha(regpath)
reg = json.loads(regpath.read_text())
old_baseline_ref = copy.deepcopy(reg["baseline"])
basepath = ROOT / old_baseline_ref["path"]
assert sha(basepath) == old_baseline_ref["sha256"]
baseline = json.loads(basepath.read_text())
objects = {o["object_id"]: o for o in reg["objects"]}
before = {oid: copy.deepcopy(objects[oid]) for oid in expected}
for oid, version in expected.items():
    assert objects[oid]["version"] == version, oid

sources_before = {}
for change in changes:
    p = ROOT / change["path"]
    assert sha(p) == change["old_sha"], change["path"]
    sources_before[change["path"]] = p.read_text()
    assert sources_before[change["path"]].count(change["old_text"]) == 1
    for rows in [reg["materials"], baseline["materials"]]:
        hits = [x for x in rows if x["path"] == change["path"]]
        assert len(hits) == 1 and hits[0]["sha256"] == change["old_sha"]

changed_refs = []
for change in changes:
    p = ROOT / change["path"]
    p.write_text(sources_before[change["path"]].replace(change["old_text"], change["new_text"]))
    change["new_sha"] = sha(p)
    for obj in reg["objects"]:
        for ref in [obj["body"], *obj["evidence"]]:
            if ref["path"] == change["path"]:
                assert obj["object_id"] in expected, obj["object_id"]
                assert ref["sha256"] == change["old_sha"]
                changed_refs.append({"object_id": obj["object_id"], "reference_before": copy.deepcopy(ref)})
                ref["sha256"] = change["new_sha"]
    for rows in [reg["materials"], baseline["materials"]]:
        next(x for x in rows if x["path"] == change["path"])["sha256"] = change["new_sha"]

notes = {
    "M-de2542fe4dcc45b59d358b5d2f899baa": "本次将原正文的700计数最小勘误为192候选型、9个正支撑整数型；登记原数学陈述、十一列余量与目标−1399均不变，没有重跑LP或科学核验。",
    "M-837fb8766b1f4b77ad33225a292f0d27": "本次仅同步所引同页另一节三价模板计数勘误后的全文SHA；本对象所用“精确代数审计”节、主证明、全部数学陈述和原报告均未改变。",
    "CA-COLLISION-FREE-LOAD-PAYMENT-NO": "本次仅将所引障碍页的一句“四个客户的主题集合”纠正为“四个主题的客户集合”；原五客户输入、完整策略、矩阵、负载及全称f反例均未改变。",
    "customer-attraction/actual-prefix-fresh-coverage-global-counterexample": "本次仅同步同页另一节四主题/五客户词序勘误后的全文SHA；本对象所用Markov探针节、52客户正文、259节点证据与量词完全未改变。",
}
for oid, version in expected.items():
    obj = objects[oid]
    obj["version"] = version + 1
    obj["objections"] += " " + notes[oid]
    for key in ["statement", "model", "quantifiers", "assumptions", "scope", "truth_status"]:
        assert obj[key] == before[oid][key], (oid, key)

newbase = ROOT / "research/registration/baseline-boss1-threeprice-topic-counts-20261112.json"
assert not newbase.exists()
baseline["coverage_note"] = baseline.get("coverage_note", "") + "；Boss1最小修正三价候选型/正支撑计数及四主题五客户词序，保全部数学命题与冻结科学证据。"
baseline["commit"] = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
write(newbase, baseline)
reg["baseline"] = {"path": str(newbase.relative_to(ROOT)), "sha256": sha(newbase)}
proposal = OUT / "threeprice-topic-counts-proposed.json"
write(proposal, reg)
result = subprocess.run(["python", "work.py", "research", "register", "--record-file", str(proposal.relative_to(ROOT))], capture_output=True, text=True)
print(result.stdout, end="")
print(result.stderr, end="")
if result.returncode:
    raise SystemExit(result.returncode)
proposal.unlink()

audit = {
    "status": "registered-local-not-pushed",
    "reviewed_by": "Boss1 and fresh TAX-MODEL-20 worker",
    "old_registry_sha256": old_registry_sha,
    "new_registry_sha256": sha(regpath),
    "old_baseline": old_baseline_ref,
    "new_baseline": reg["baseline"],
    "changes": changes,
    "changed_refs": changed_refs,
    "before_objects": before,
    "after_objects": {oid: objects[oid] for oid in expected},
    "new_input_pins": {oid: rr.pin(objects[oid]) for oid in expected},
    "scope": "Two source sentences only; four versions increment solely for exact byte references. No new object, no altered theorem, no scientific execution, and no old task/edge is silently retired.",
    "pending_repair": "Refresh the two preserved unfinished Boss1 tasks; refresh Boss5's read-only endpoint without taking its core ownership; publish directed successors of affected effective done batches.",
}
write(OUT / "threeprice-topic-counts-correction.json", audit)
print(json.dumps({"status": audit["status"], "objects": audit["new_input_pins"], "baseline": reg["baseline"]}, ensure_ascii=False))
