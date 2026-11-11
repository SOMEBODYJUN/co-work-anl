"""Freeze the verified union certificate and write the substantive result note."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT/"peer_augmented_lp"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE/name).read_text())


def write(name, value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")


def main():
    report, execution, status = read("certificate_verification.json"), read("execution_manifest.json"), read("status.json")
    assert report["exact_primal_verified"] and report["exact_dual_verified"]
    assert report["rows"] == 19662 and report["columns"] == 15593
    assert {record["step"] for record in execution["executions"]} == {"solve","recover","dual_repair","dual_repair2","verify"}
    assert status["exact_dual_failure_resolved"] is True
    for record in execution["executions"]:
        assert record["status"] == "finished"
        assert record["exit_code"] == (1 if record["step"] in ("recover","dual_repair") else 0)
        assert digest(HERE/record["executed_source"]) == record["source_sha256"]
        assert digest(HERE/record["source_snapshot"]) == record["source_sha256"]
        assert digest(HERE/record["stdout"]) == record["stdout_sha256"]
        assert digest(HERE/record["stderr"]) == record["stderr_sha256"]
        assert ((HERE/record["stderr"]).stat().st_size == 0) == (record["step"] not in ("recover","dual_repair"))
    for name in ("executed_repair_sources.json","executed_repair2_sources.json"):
        for record in read(name):
            assert digest(HERE/record["source"]) == record["sha256"]
            assert digest(HERE/record["snapshot"]) == record["sha256"]
    for filename in ("recovery_repair_inputs.json","recovery_repair2_inputs.json"):
        for name, expected in read(filename)["sha256"].items():
            assert digest(HERE/name) == expected
    with gzip.open(HERE/"exact_matrix.json.gz","rt",encoding="utf-8") as stream:
        matrix = json.load(stream)
    primal, dual, audit = read("augmented_lp_exact.json"), read("exact_dual_certificate.json"), read("primal_exact_audit.json")
    old_dual = json.loads((BASE/"exact_dual_certificate.json").read_text())
    old_weights = {i:F(value) for i,value in old_dual["row_multipliers"]}
    weights = {i:F(value) for i,value in dual["row_multipliers"]}
    changes = [{"row":i,"name":matrix["row_names"][i],"old_dual_weight":str(old_weights.get(i,F(0))),
                "new_dual_weight":str(weights.get(i,F(0))),"new_primal_slack":audit["row_slacks"][i],
                "new_row":i>=19621} for i in sorted(set(old_weights)|set(weights))]
    write("dual_activity_changes.json",{"old_positive_dual_rows":len(old_weights),"new_positive_dual_rows":len(weights),
          "old_active_retained":len(set(old_weights)&set(weights)),
          "old_active_no_longer_positive":len(set(old_weights)-set(weights)),
          "previously_zero_now_positive":len(set(weights)-set(old_weights)),"rows":changes})
    new_rows = read("new_row_results.json")
    active = [row for row in new_rows if row["positive_dual_weight"]]
    signs = Counter("zero" if F(row["exact_slack"]) == 0 else "positive" for row in new_rows)
    W = F(primal["W"])
    old_W = F(json.loads((BASE/"augmented_lp_exact.json").read_text())["W"])
    peer_W = F(report["peer_exact_optimum"])
    assert W == F(dual["normalization_multiplier"]) and peer_W <= W < F(1,2)
    write("frozen_result.json",{"status":"FROZEN; exact finite LP obligation complete and releasable",
          "original_obligation":"six-player common-catalog full-history pureSPE half remains OPEN",
          "rows":19662,"columns":15593,"appended_rows":41,"W":str(W),"O":"1",
          "strict_half_gap":str(1-2*W),"baseline_W":str(old_W),"peer5799_W":str(peer_W),
          "exact_increase_from_baseline":str(W-old_W),"exact_difference_from_peer5799":str(W-peer_W),
          "new_row_slack_signs":dict(signs),"new_positive_dual_rows":len(active),
          "point_sha256":digest(HERE/"augmented_lp_exact.json"),"matrix_sha256":digest(HERE/"exact_matrix.json.gz"),
          "dual_sha256":digest(HERE/"exact_dual_certificate.json"),
          "independent_verification_sha256":digest(HERE/"certificate_verification.json"),
          "execution_manifest_sha256":digest(HERE/"execution_manifest.json")})
    active_table = "\n".join(f"| {r['row']} | `{r['name']}` | `{r['dual_weight']}` | {float(F(r['dual_weight'])):.17g} |" for r in active)
    if not active_table:
        active_table = "| — | 无 | `0` | 0 |"
    free_table = "\n".join(f"| {j} | {audit['recovery']['support'][j]} | `{value}` |" for j,value in audit["recovery"]["free_values"])
    if not free_table:
        free_table = "| — | — | 无自由变量 |"
    hashes = "\n".join(f"| `{name}` | `{digest(HERE/name)}` |" for name in [
        "append_plan.json","inputs.json","exact_matrix.json.gz","augmented_lp_exact.json",
        "exact_dual_certificate.json","certificate_verification.json","whole_peer_coverage.json",
        "inherited_peer_dual_lower_bound.json","new_row_results.json","execution_manifest.json"])
    reverse = new_rows[-1]
    text = f"""# 完整同行归并与 reverse624 增补有限 LP：冻结结果

- 执行代理：`/root/union_augmented_lp`；SameBoss1。
- RUN：`six-boss1-20261111`；只写本文件及 `union_augmented_lp/`。
- 状态：19662×15593一次数值求解、精确primal恢复、对偶互补修复及独立标准库全行全列核验完成；求解、最终修复、最终核验均退出0。两次对偶恢复候选的退出1及实际stderr完整保留，最终仅用同一数值数组与精确primal修复；本有限计算义务已冻结，可释放。
- 原六人、共同菜单、全历史 pureSPE 的 half 义务仍为 **OPEN**。

## 精确结论

本轮固定16hist必要LP的精确最优值为

`W = {W}`，`O = 1`，约 **{float(W):.17g}**。

`1 - 2W = {1-2*W}`。该量为严格正数。低于half的必要LP可行点没有补齐全历史策略、共同菜单与SPE一致性，因而不构成原题反例，也不构成全域下界。

| 系统 | 精确最优值 | 近似值 | 本轮差值 |
| --- | --- | ---: | ---: |
| 保留的19621行系统 | `{old_W}` | {float(old_W):.17g} | +{float(W-old_W):.17g} |
| 同行5799行系统 | `{peer_W}` | {float(peer_W):.17g} | +{float(W-peer_W):.17g} |
| 本轮19662行系统 | `{W}` | {float(W):.17g} | 0 |

相对19621行旧系统的精确提高为 `{W-old_W}`；相对同行5799行系统的精确差值为 `{W-peer_W}`。独立核验器重新证明同行5799行精确 primal/dual，再把其非负对偶权按正比例行映射嵌入本系统；因此本轮不低于同行值具有完整可复核的有理证书。

## 输入与完整保留

基准为 `peer_augmented_lp/` 的19621×15593系统，原点SHA为 `d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f`，矩阵SHA为 `6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9`。

全部19621条旧行的编码、15593列描述、目标、归一化、7954个canonical max辅助变量、2790个canonical min辅助变量均逐项原样保留。新增41行只作用于原4849列，10744个辅助坐标系数全部为0；正比例去重后41行与基准及彼此均不重合。最终954669个非零系数。

| 输入包 | SHA256 | 新行 | 原点负 / 零 / 正 |
| --- | --- | ---: | --- |
| `peer_union_transfer/all_missing_rows_19621.json` | `bdbf86be287f748de895161471cf24c366f933d4486ca5df34af33041b9b4b57` | 40 | 5 / 0 / 35 |
| `peer_union_transfer/reverse624_reviewed_19621.json` | `ae2b87e64a38a13d5b475420985e39cf7fb428b13b2897ef460268f69957e4d2` | 1 | 0 / 0 / 1 |

40条同行行的来源矩阵SHA为 `0b4bd0a81097b022a638fdc44324c731768255579a5bf07618e12c35c9342bec`。全部5799条同行行都有正比例对应行，全部4849原始描述符、目标和归一化一致，前5692条行已在旧基准中；逐行对应因子及新点余量冻结于 `whole_peer_coverage.json`。其中13条neighbor行只作为已审阅合同的保留行，不声称为本轮新数学机制。

额外reverse624行位于19661（0-based），来源为 `joint_requery/reverse_terminal_5799_one_v1.json`，Main按真实末节点的 `v/(p4+r+1) - z/(p4+r+z)` 独立逐4992字面隐藏态、全部4849原始系数重构并审阅合同。本轮绑定原始来源、Main源码与审核SHA，再独立核对转入完整向量；没有新增钱包。Main审阅的数学合法性与本轮固定输入的代入及优化是不同职责。

## 精确证书与独立核验

标准库 `verify_certificates.py` 不导入装配、恢复、数值优化或切面生成代码。它核验所有19662行primal余量、15593列非负性与dual残差、两套canonical辅助变量、全旧系统保留、41条新向量、源SHA、恢复支持和自由值、互补性、同行全系统包含及同行对偶嵌入。独立核验耗时 {report['seconds']:.3f} 秒。

证书身份为 `objective = W * normalization + sum_i lambda_i row_i + residual`，所有lambda与residual非负，primal实现同一W。最小primal余量与最小dual残差均为0，因此是精确最优值而非浮点候选。原19621行对偶的零扩展也重新核验通过。

| 核验项目 | 数量 |
| --- | ---: |
| 正原始列 | {report['positive_original_columns']} |
| 正max辅助列 | {report['positive_max_auxiliaries']} |
| 正min辅助列 | {report['positive_min_auxiliaries']} |
| primal恢复变量 / 秩 / 自由变量 | {audit['recovery']['variables']} / {audit['recovery']['rank']} / {len(audit['recovery']['free_variables'])} |
| 正dual行 | {report['positive_dual_rows']} |
| dual恢复变量 / 秩 / 自由变量 | {dual['recovery'].get('variables')} / {dual['recovery'].get('rank')} / {len(dual['recovery'].get('free_variables',[]))} |
| 新行精确零 / 严格正余量 | {signs['zero']} / {signs['positive']} |
| 新行严格正dual权 | {len(active)} |

## 新活动对偶权

下表完整列出41条新行中严格正的对偶权；这些行在新点均精确取零。零对偶权不等于数学冗余，存在旧对偶权变化也不等于产生了新机制。旧、新所有正对偶支持及精确权变化另存 `dual_activity_changes.json`。

| 行号（0-based） | 名称 | 精确dual权 | 近似值 |
| ---: | --- | --- | ---: |
{active_table}

额外reverse624行的新点余量为 `{reverse['exact_slack']}`，约 {reverse['slack_float']:.17g}；dual权为 `{reverse['dual_weight']}`。全部41行的原点余量、新点余量、完整向量SHA、来源、矩阵行号与dual权都在 `new_row_results.json`，全系数保留于输入包及完整新矩阵。

## 恢复与实际执行

SciPy HiGHS仅用于选择活动面，唯一一次数值求解耗时 {status['solver_seconds']:.3f} 秒、{status['solver_iterations']} 次迭代；随后使用精确Fraction稀疏消元完成全部原始列支持恢复及canonical辅助填充。源码、输入散列、数值原始数组、活动方程、自由值与全行余量均冻结。

初次对偶恢复的`1e-9`筛选漏掉行1894（`overlap-upper:907`）约`3.8493180648e-10`的正乘子，又把列907同量级的正reduced cost强制为0，因而产生不相容精确等式。第一修复保留原优化与原精确点，候选行阈值改为`1e-12`并按精确primal余量裁剪，仅在严格正primal列强制对偶残差为0；这留下自由方向，数值自由值有理化后列2737出现约`-5.1e-14`的严格负残差，该候选也被拒绝。

最终修复额外使用数值reduced cost绝对值小于`1e-12`的列等式，避开列907真实的微小正残差；每条精确等式、全部15593列非负残差及互补性最终通过。两次修复均未调用优化器。两次失败stdout/stderr、原执行源码、故障文件，以及`dual_repair_diagnostics.json`、`dual_repair2_diagnostics.json`、修复输入和源码均保留，不能把失败尝试描述为成功。

| primal局部自由变量 | 原始列 | 采用的精确值 |
| ---: | ---: | --- |
{free_table}

`execution_manifest.json` 记录五个真实命令、工作目录、实际源码SHA、退出码与逐字stdout/stderr的SHA。驱动命令依次为 `python -u run_step.py solve`、`python -u run_step.py recover`、`python -u run_repair.py dual_repair`、`python -u run_repair2.py dual_repair2`、`python -u run_step.py verify`；驱动以参数数组运行各数学脚本。`source_snapshots/` 保存借鉴的旧脚本及Main输入重构源码，`executed_sources/` 保存实际执行脚本的逐SHA快照，`artifact_manifest.json` 给出最终产物清单。哈希绑定输入仍位于原冻结工作区。

## 核心SHA256

下表路径均相对 `union_augmented_lp/`。

| 文件 | SHA256 |
| --- | --- |
{hashes}

## 接续接口

Main可直接使用 `union_augmented_lp/augmented_lp_exact.json` 与 `union_augmented_lp/exact_matrix.json.gz` 接续分离；后续增补须保留本轮19662行与两套辅助结构。当前任务冻结并可释放；原full-history pureSPE half义务仍OPEN。
"""
    (ROOT/"union_augmented_lp.md").write_text(text)
    artifacts = []
    for path in sorted(HERE.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.name != "artifact_manifest.json":
            artifacts.append({"path":str(path.relative_to(HERE)),"bytes":path.stat().st_size,"sha256":digest(path)})
    write("artifact_manifest.json",{"scope":"frozen union certificate, exact sources, bound inputs, commands and raw outputs",
          "report":{"path":"../union_augmented_lp.md","sha256":digest(ROOT/"union_augmented_lp.md")},
          "artifacts":artifacts})
    print(json.dumps({"frozen":True,"W":str(W),"W_float":float(W),"new_positive_dual_rows":len(active),
          "report_sha256":digest(ROOT/"union_augmented_lp.md"),"artifact_manifest_sha256":digest(HERE/"artifact_manifest.json")},ensure_ascii=False))


if __name__ == "__main__":
    main()
