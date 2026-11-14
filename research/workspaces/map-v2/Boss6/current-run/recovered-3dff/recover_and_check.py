"""Rebuild only the authorized repair receipt; validate without Git or queue writes."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "work.py").is_file())
sys.path.insert(0, str(ROOT / "tools"))
import research_runtime as research
import map_tasks

TASK = "boss2-wave22-um-repair-3dff15adda4a5b83"
OLD = "unrelated-machines-3a-3a-7670a89f413f26a6"
CHANGED = "unrelated-machines/arbitrary-sink-price-cover-final-audit"
PROOF = "archives/unrelated-machines/tools/evidence/um-next-four-audit-primary/comparison/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md"
PROOF_SHA = "6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580"
RECEIPT = f"map/receipts/{TASK}.json"


def read(name):
    return json.loads((ROOT / name).read_text())


def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


task_path = f"research/operations/map-v2/tasks/{TASK}.json"
old_path = f"research/operations/map-v2/tasks/{OLD}.json"
task, predecessor = read(task_path), read(old_path)
d, od = task["definition"], predecessor["definition"]
assert task["state"] == "claimed" and task["owner"] == "Boss6"
assert predecessor["state"] == "done" and d["supersedes"] == [OLD]
old_receipt_path = f"map/receipts/{OLD}.json"
prior = read(old_receipt_path)
assert prior == predecessor["receipt"]
registry = read(d["registry"])
objects = {o["object_id"]: o for o in registry["objects"]}
assert set(d["object_ids"]) == set(od["object_ids"]) == set(prior["coverage"])
assert set(d["input_pins"]) == set(d["object_ids"] + d["read_object_ids"])
assert all(research.pin(objects[i]) == p for i, p in d["input_pins"].items())
changes = [i for i, p in od["input_pins"].items() if d["input_pins"][i] != p]
assert changes == [CHANGED]

# The exact predecessor registration is recoverable from the old pinned record,
# without pretending that the old review-source bytes were retrieved.
previous_record = copy.deepcopy(objects[CHANGED])
previous_record["version"] = 2
previous_record["objections"] = previous_record["objections"].removesuffix(
    " Boss3已据完整证明订正引用页的转述错误，本登记数学结论及条件保持。"
)
previous_record["evidence"][0]["sha256"] = "3a3edde0a48bb34fbb0dccda407d271b43ee322156ecaab6205cb251b75cf026"
assert research.pin(previous_record) == od["input_pins"][CHANGED]
delta_fields = sorted(k for k in objects[CHANGED] if objects[CHANGED][k] != previous_record[k])
assert delta_fields == ["evidence", "objections", "version"]
assert sha(PROOF) == PROOF_SHA

# These checks load complete bytes and verify exact headings. They do not mean
# that all unchanged historical source proofs have been freshly re-read.
refs = d["context_plan"]["reading_refs"][:]
for i in d["input_pins"]:
    refs += [objects[i]["body"], *objects[i]["evidence"]]
unique_refs = {json.dumps(r, sort_keys=True, ensure_ascii=False): r for r in refs}
for r in unique_refs.values():
    research.ref_bytes(ROOT, r)

scopes = {
    "unrelated-machines/li-nearly-linear-scheduling-lp-and-rounding": "沿用前任务的Li整体算法/小槽/BGW比较；本轮实读当前v1登记、Li§2–3、BGW§5及保留边，区分MPC、列归一化、匹配与搜索的不同义务。",
    "M-3fcaea74cca845be8c00c0f2e9d089f5": "沿用前任务的小槽中心恢复比较；本轮实读当前v2登记、Li§2–3、BGW§5和保留边，核Hall扩张、前槽收费及CONGEST边界。",
    "UM-SINGLE-LAYER-QUOTA-VALUE-v1": "沿用前任务已发布的单层配额/两状态/行列池/EXACT COVER比较；本轮核当前v3登记及完整body/evidence字节绑定。未重新全文审查这些不变来源或复跑旧枚举。",
    "M-ddb8ee6a112145848ec4170ede09001b": "沿用前任务的完整Karp来源归约链；本轮实读当前v1登记、语言/编码及§2、§3.4、§5.1、§5.4，复核两条共享保留边的exact-one与无进位映射。",
    "unrelated-machines/cumulative-path-proof-aware-correction-and-statement-first-certificate": "沿用前任务已发布的累计路径/完整leaf正规形/PCSP比较；本轮核当前v3登记及完整body/evidence字节绑定。不把前worker的全文读取或旧Fraction检查计成本轮执行。",
    "UM-CACTUS-HIGH-GIRTH-CONFIG-GAP-v1": "沿用前任务的cactus/双树CONFIG gap比较；本轮实读当前v4登记及主审查的任意围长间隙族和逐块精确算法两节，复核b=1保留边的局部范围。",
    "M-0fbec72103194febba64cdb960f46091": "沿用前任务的Karp有向/无向Hamilton比较；本轮实读当前v1登记、Karp§1、§2、§3.4和保留边，核三点路径双向解码及极小图预处理。",
    "UM-UNIT-READOUT-HALF-DENSITY-THREE-HALVES-v1": "沿用前任务的半密度/包络/纯叶hitting比较；本轮实读当前v2登记、半片共同匹配及真实森林节、包络单行节与保留边。不把纯叶数量当外部共同容量。",
    "M-d9e5cebbc2d04007aea7542b91397ad6": "沿用前任务的完整有向Hamilton来源链；本轮实读当前v1登记、Karp§1、§2、§3.4和三点路径保留边；Cook起点继续作为已声明外部输入。",
    "UM-HALL-GROUP-PROMISE-APPROX-v1": "沿用前任务Hall/失真组/任意sink/TARGET比较；本轮核当前v3登记、完整body/evidence绑定，并以任意sink最终原证明§1–9重核两种OPT承诺接口的差别。其余Hall成熟推导复用前任务审查。",
    "UM-ST-ENVELOPE-CONFIG-IDENTITY-v1": "沿用前任务的固定B凸化/CONFIG/半密度比较；本轮实读当前v1登记、包络单行定义/可提取性、半片共同匹配节及保留边，保留非凸最优化未给算法的边界。",
    CHANGED: "本轮全文实读当前v3登记、主内部审计、改后最终冻结读后审查、共同占位联合舍入审查和最终原证明§1–9；原证明SHA=6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580。由反向重建记录命中旧pin，准确确认v2→v3仅version/objections/一项审查evidence SHA变化；未取得旧审查页字节，不声称其逐字diff。比较Hall、distorted及一般可靠阈值→TARGET。",
    "UM-NEAR-UNIT-PHYSICAL-COPY-OPEN": "沿用前任务的PCSP/物理复制/ring/cumulative比较；本轮核当前v1登记及完整body/evidence绑定，并由任意sink原证明重核该受限结构算法不能支付一般物理编译义务。没有把旧worker完整审查计为本轮读取。",
    "UM-UNPRUNED-ASSIGNMENT-LP-KRONECKER-v1": "沿用前任务的LP/actual Kronecker比较；本轮实读当前v1登记及同一正文§7.1–7.4，复核非负原初/对偶乘积、完整100任务平方、十五件同时交换和偶幂范围。旧任务的follow-up处置保留在本coverage；本修复定义无overlap，不另填closed_overlaps。",
    "UM-TARGET-v1": "沿用前任务的一般目标/可靠阈值/CONFIG gap比较；本轮实读当前v4登记、一般问题的阈值及缺口节、可靠阈值接口节、任意sink最终原证明和保留条件边。接受集合非单调的网格搜索另作本轮有限穷举检验。",
    "M-76983feebdc44edca5da3feb68582355": "沿用前任务的r份uniform-I/两份actual异权比较；本轮实读当前v1登记、共同流正文§3、§5、§6、版本审查§3及保留边；核两见证半半流桥与两套任意S回填。",
    "UM-DISTORTED-GROUP-PROMISE-APPROX-v1": "沿用前任务的distorted/Hall/price-cover比较；本轮核当前v3登记及完整body/evidence绑定，实读任意sink最终原证明§1–9，保留distorted的共同资格/双侧包络与该接口逐件资格/上界的区别。不声称复跑其旧审计。",
    "UM-CONF-GAP-v1": "沿用前任务的双树/cactus/CONFIG/TARGET比较；本轮实读当前v2登记、双树正文的排除范围、一般问题缺口、cactus主审查两节及动机边。CONFIG相对T障碍继续仅作语境覆盖。",
    "M-c7afd458b546466b96676d45b76ebe79": "沿用前任务已发布的m2最小负平方/CONFIG/一般目标比较；本轮核当前v1登记和完整body/evidence绑定。未复跑旧Bareiss程序，未把该边界反例扩大到m≥3或调度困难性。",
    "M-53bb17e3dfb142718bc8fb965bb20b4e": "沿用前任务的两见证异权/uniform-I子域比较；本轮实读当前v1登记、共同流§3及双回填§5–6、版本边界§3与保留边。全异权成本配对及固定同端细界保持原独立义务。",
    "UM-COMPACT-MULTIROW-EXTENSION-v1": "沿用前任务已发布的多行真实容量/单机CONFIG探针比较；本轮核当前v2登记、共享probe v2登记及完整body/evidence绑定，保留不同查询可换见证和剩余行仅计数的量词区别。旧in-packet比较已在前任务实质处置，不虚构新follow-up。",
}
assert set(scopes) == set(d["object_ids"])
receipt = {
    "coverage": copy.deepcopy(prior["coverage"]),
    "assets": copy.deepcopy(prior["assets"]),
    "follow_up_tasks": [],
    "closed_overlaps": [],
    "reviewed_by": "Boss6",
    "review_note": "运行环境重置后重建；旧任务、旧收据和9条边原字节保全。成熟未变数学复用已发布前任务，comparison_scope区分本轮实际读取与沿用审查；旧程序/有限运行不冒称新run。新做的字节、原生结构检查与有限算术/搜索核验见recovered-3dff工作区。",
    "supersession": {
        OLD: {
            "reason": "唯一变化输入为arbitrary-sink-price-cover-final-audit v2→v3；精确旧pin重建确认数学陈述、域、量词、假设及主证明均未变。重核改后审查及原证明§7的未知OPT语义，刷新21核心coverage，9资产的端点/evidence/review绑定和原SHA全部保留。",
            "assets": {},
        }
    },
}
for i, row in receipt["coverage"].items():
    row["object_pin"] = d["input_pins"][i]
    row["comparison_scope"] = scopes[i]
receipt["coverage"][CHANGED]["reason"] = (
    "三个合同仍限唯一home、不交私有组、合法逐件sink资格、统一rho/delta及共同宏占位。"
    "未知OPT版本只取消宏边>当前T/2的检查，仍剪p_hb>T，并检查W_h≤T和a_j≤delta*T。"
    "在真实OPT承诺内且T≥OPT时，原最优调度每home至多一宏；所用宏端≤OPT≤T未被剪，"
    "私有留量<OPT/2≤tau*T，且W_h≤OPT≤T、a_j≤delta*OPT≤delta*T，故同一原最优调度"
    "给共同macro/home/出口见证，最小覆盖、价格FPTAS和共同宏匹配不会FAIL。成功时只用实际宏≤T、"
    "保留的W/a界及真实cover的b0*T列预算，经MW和单侧+b0*T舍入得home≤(1+tau)T、"
    "sink≤(1+eta+b0)T，故仍为alpha*T；无须当前T宏下界。FAIL⇒T<OPT只在承诺域内，"
    "低于OPT可非单调接受，保存成功见证的分母网格二分仍给alpha*OPT。满秩非空模式home覆盖B、"
    "home容量1及原任务回溯不可省；复杂度poly(L,1/eta)，非poly(L,log(1/eta))。"
    "没有一般矩阵角色/承诺提取器或生产LP后端，不能接成UM-TARGET的无条件支持。"
)
for a in receipt["assets"]:
    assert sha(a["path"]) == a["sha256"]
    assert a["path"] in registry["edge_files"]
    edge = read(a["path"])
    assert CHANGED not in edge["source_ids"] + edge["target_ids"]
    assert all(r["path"] != objects[CHANGED]["evidence"][0]["path"] for r in edge["evidence"])
    receipt["supersession"][OLD]["assets"][a["path"]] = {
        "disposition": "retained",
        "reason": f"本轮重读边的实际数学关系并核当前端点、完整evidence字节及review绑定；该边不依赖唯一改版对象或改动审查页，保原SHA及原scope：{edge['scope']}",
    }
write(ROOT / RECEIPT, receipt)


def native_edge_check(a):
    command = [sys.executable, "work.py", "research", "edge-check", a["path"]]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
    return {"command": command[1:], "asset": a, "result": json.loads(proc.stdout)}


with ThreadPoolExecutor(max_workers=3) as pool:
    edge_checks = list(pool.map(native_edge_check, receipt["assets"]))
relations = research.edges(ROOT, {"edge_files": [a["path"] for a in receipt["assets"]]}, objects)
map_tasks._map_receipt_coverage(d, receipt, objects, relations)
assert map_tasks._supersession(ROOT, d, receipt, [predecessor], "map") == set()
research.validate_map_follow_ups(d, receipt, [predecessor, task], objects)
assert receipt["assets"] == prior["assets"] == d["context_plan"]["prior_assets"]

# Independent finite sanity checks, explicitly distinct from the historical
# price-cover/LP audits and from the general arguments in the cited proof.
balanced = 0
for rho in [F(1), F(3, 2), F(2), F(10), F(1000)]:
    for delta in [F(0), F(1, 10000), F(1, 10), F(1, 4), F(1, 2)]:
        for eta in [F(1, 10000), F(1, 100), F(1, 4), F(1, 2), F(1)]:
            if rho * delta + eta >= 1:
                continue
            tau = (rho * (1 + delta) + eta) / (1 + rho)
            b0 = rho * (1 - tau + delta)
            alpha = 2 - (1 - rho * delta - eta) / (1 + rho)
            assert F(1, 2) <= tau < 1 and 0 <= b0 <= 1
            assert b0 == tau - eta and alpha == 1 + tau == 1 + eta + b0 < 2
            # Back substitution recovers the exact defining balance.
            assert (1 + rho) * tau == rho * (1 + delta) + eta
            balanced += 1
mw_checks = 0
for denominator in range(1, 25):
    for numerator in range(1, denominator + 1):
        eta = F(numerator, denominator)
        assert (1 + eta / 2) / (1 - eta / 4) <= 1 + eta
        assert (1 + eta) * (1 - eta / 4) - (1 + eta / 2) == eta * (1 - eta) / 4
        mw_checks += 1

search_cases = 0
for optimum in range(1, 11):
    for upper in range(optimum, 13):
        # Every low-threshold pattern is allowed; T>=OPT always succeeds.
        for mask in range(1 << optimum):
            accepted = lambda t: t >= optimum or bool(mask & (1 << t))
            lo, hi = 0, upper
            while hi > lo + 1:
                mid = (lo + hi) // 2
                if accepted(mid):
                    hi = mid
                else:
                    lo = mid
                assert lo < optimum and accepted(hi)
            assert hi <= optimum and accepted(hi)
            a, b = 0, upper
            while a < b:
                mid = (a + b) // 2
                if accepted(mid):
                    b = mid
                else:
                    a = mid + 1
                assert a <= optimum and accepted(b)
            assert b <= optimum and accepted(b)
            search_cases += 1

# Two dedicated homes; each has a unit macro and two private 1/4 jobs.
# No sinks. Exact OPT=3/2. The current macro-lower check fails at T>=2,
# although the retained W/a checks, joint macro matching and decoder work.
rho, delta, eta = F(1), F(1, 2), F(1, 4)
tau = (rho * (1 + delta) + eta) / (1 + rho)
alpha = 1 + tau
regression = []
for threshold in [F(1), F(3, 2), F(2), F(3)]:
    assert F(1, 2) <= threshold and F(1, 4) <= delta * threshold
    assert 1 <= threshold and F(1, 2) <= tau * threshold
    assert F(3, 2) <= alpha * threshold
    regression.append({"T": str(threshold), "old_macro_lower": bool(1 > threshold / 2), "actual_peak": "3/2", "alpha_T": str(alpha * threshold)})
assert F(1) > F(3, 2) / 2
assert not (F(1) <= F(1, 2))  # Macro pruning soundly rejects this low T.
assert not (F(4) <= F(1))     # W<=T is a real check, even when B is empty.
assert not (F(1, 4) <= F(0))  # delta=0 uses multiplication, not division.

report = {
    "status": "passed-local-review-not-published",
    "task": TASK,
    "task_sha256": sha(task_path),
    "predecessor_task_sha256": sha(old_path),
    "predecessor_receipt_sha256": sha(old_receipt_path),
    "local_registry_sha256": sha(d["registry"]),
    "receipt": {"path": RECEIPT, "sha256": sha(RECEIPT)},
    "current_input_pins_checked": len(d["input_pins"]),
    "changed_inputs": changes,
    "exact_predecessor_registration_pin_reconstructed": research.pin(previous_record),
    "registration_delta_fields": delta_fields,
    "old_review_source_bytes_retrieved": False,
    "literal_before_after_source_diff_claimed": False,
    "unchanged_final_proof": {"path": PROOF, "sha256": PROOF_SHA},
    "unique_reference_bindings_checked": len(unique_refs),
    "unique_reference_files_checked": len({r["path"] for r in unique_refs.values()}),
    "reference_check_means_full_math_reread": False,
    "coverage_counts": dict(Counter(row["state"] for row in receipt["coverage"].values())),
    "retained_asset_count": len(receipt["assets"]),
    "new_asset_count": 0,
    "native_edge_checks": edge_checks,
    "native_receipt_checks": ["_map_receipt_coverage", "_supersession", "validate_map_follow_ups"],
    "finite_sanity": {"exact_balance_cases": balanced, "exact_mw_cases": mw_checks, "all_low_threshold_acceptance_patterns_cases": search_cases, "unknown_opt_regression": regression, "empty_zero_and_delta_zero_branches": "checked algebraic guards only; no historical audit rerun"},
    "limits": "Native checks are structural, finite sanity is not a general proof, inherited mathematical reviews are not fresh executions. No Git, queue, registry, coverage, integration, old task, old receipt or old edge was written.",
}
write(HERE / "validation.json", report)
print(json.dumps({k: report[k] for k in ["status", "receipt", "current_input_pins_checked", "changed_inputs", "registration_delta_fields", "unique_reference_bindings_checked", "coverage_counts", "retained_asset_count", "new_asset_count", "finite_sanity"]}, ensure_ascii=False, indent=2))
