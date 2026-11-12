"""Apply source-count errata and an exact two-player scope clarification.

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
    {
        "path": "archives/customer-attraction/state/计算/R373二元局部响应与残差覆盖的71整数证书--计算.md",
        "old_sha": "f57616eeb55e7fa2b9eb368faf1827033937b864012618749dc3a45040e7f8c2",
        "old_text": "这是一个二阶段分支比较，不是完整SPE的根到叶验证。",
        "new_text": "与上述36行合在一起，这是根动作0及固定ρ的恰两人完整纯SPE在全部7个决策历史的42项IC验证；它不是六人完整SPE的根到叶验证。",
        "extra_replacements": [
            [
                "它没有给出更长历史、六位提供者或所有子博弈的动作表。",
                "这36行遍历恰两名提供者的全部长度1历史和全部末位偏离；它没有给出三位或更多提供者的更长历史动作表。"
            ],
            [
                "因此该表确实满足这份**两阶段编码**的局部最佳回应行；这些等号是平局，不能被写成唯一最佳回应或完整树中的可信续局。",
                "因此该表给出这份**恰两人完整策略**的全部最佳回应比较；这些等号允许弱平局，不能被写成唯一最佳回应，也不提供六人完整树的可信续局。"
            ],
            [
                "也没有检查所有离轨历史、任意平局的后继、终局均分网络或",
                "这42行已覆盖恰两人的全部有序决策历史、两个槽均分及弱平局；它没有检查六人模型中的"
            ],
            [
                "其余求解器输出、有限搜索或相关工作不得把该数值升级成一般人数、一般目录或完整SPE结论。空主题、零客户、重复标签和离轨历史未被该脚本建模，不能从本证书默认为已处理。",
                "其余求解器输出、有限搜索或相关工作不得把该数值升级成一般人数或一般目录的普遍SPE结论。六个原标签、含重复的两个行动槽及全部六个长度1前缀均在此固定模型中；71最优值只针对所列63行含严格正缺口的系统，不是零客户或任意目录的普遍结论。"
            ],
        ],
        "reason": "The source lists all 36 terminal comparisons and all six root comparisons for two players and six labels. These are all seven ordered decision histories, including repeated slots and off-path one-action histories. The fixed 63-row minimum-71 statement does not assert any six-player guarantee.",
    },
]
expected = {
    "M-de2542fe4dcc45b59d358b5d2f899baa": 1,
    "M-837fb8766b1f4b77ad33225a292f0d27": 2,
    "CA-COLLISION-FREE-LOAD-PAYMENT-NO": 3,
    "customer-attraction/actual-prefix-fresh-coverage-global-counterexample": 4,
    "customer-attraction/r373-binary-local-response-residual-coverage-71-certificate": 1,
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
    for old_text, _ in change.get("extra_replacements", []):
        assert sources_before[change["path"]].count(old_text) == 1
    for rows in [reg["materials"], baseline["materials"]]:
        hits = [x for x in rows if x["path"] == change["path"]]
        assert len(hits) == 1 and hits[0]["sha256"] == change["old_sha"]

changed_refs = []
for change in changes:
    p = ROOT / change["path"]
    text = sources_before[change["path"]].replace(change["old_text"], change["new_text"])
    for old_text, new_text in change.get("extra_replacements", []):
        text = text.replace(old_text, new_text)
    p.write_text(text)
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
    "customer-attraction/r373-binary-local-response-residual-coverage-71-certificate": "本次澄清正文范围：36末位行和6根行确为给定两人策略的全部7历史42IC，允许重复槽及弱平局；未编码的是六人完整策略。原63行系统、71原对偶最优值、固定ρ和登记陈述均不变，没有重跑MILP或原验证器。",
}
for oid, version in expected.items():
    obj = objects[oid]
    obj["version"] = version + 1
    obj["objections"] += " " + notes[oid]
    for key in ["statement", "model", "quantifiers", "assumptions", "scope", "truth_status"]:
        assert obj[key] == before[oid][key], (oid, key)

newbase = ROOT / "research/registration/baseline-boss1-threeprice-topic-counts-20261112.json"
assert not newbase.exists()
baseline["coverage_note"] = baseline.get("coverage_note", "") + "；Boss1最小修正三价候选型/正支撑计数、四主题五客户词序及71证书恰两人完整IC/六人未编码范围，保全部登记数学命题与冻结科学证据。"
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
    "scope": "Three source pages: two count/wording sentences and precise two-player versus six-player scope. Five versions increment for exact byte references and scope clarification; registered mathematical statements are unchanged. No new object, no scientific execution, and no old task/edge is silently retired.",
    "pending_repair": "Refresh the two preserved unfinished Boss1 tasks; refresh Boss5's read-only endpoint without taking its core ownership; publish directed successors of affected effective done batches.",
}
write(OUT / "threeprice-topic-counts-correction.json", audit)
print(json.dumps({"status": audit["status"], "objects": audit["new_input_pins"], "baseline": reg["baseline"]}, ensure_ascii=False))
