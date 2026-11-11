"""Create a compact handoff and hash manifest after independent verification."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
BASE=RUN/"zz_closure_lp"/"round2"


def read(name):
    return json.loads((HERE/name).read_text())


def main():
    point=read("augmented_lp_exact.json")
    dual=read("exact_dual_certificate.json")
    audit=read("primal_exact_audit.json")
    verification=read("certificate_verification.json")
    status=read("status.json")
    baseline=json.loads((BASE/"augmented_lp_exact.json").read_text())
    W,old_W=F(point["W"]),F(baseline["W"])
    assert verification["exact_primal_verified"] and verification["exact_dual_verified"]
    assert verification["W"]==dual["normalization_multiplier"]==point["W"]
    changes=[]
    for j,(a,b) in enumerate(zip(baseline["columns"][:4849],point["columns"][:4849])):
        if F(a["weight"])!=F(b["weight"]):
            changes.append({"column":j,"descriptor":{k:v for k,v in a.items() if k!="weight"},
                            "old_weight":a["weight"],"new_weight":b["weight"],
                            "difference":str(F(b["weight"])-F(a["weight"]))})
    (HERE/"original_coordinate_changes.json").write_text(json.dumps(changes,indent=2)+"\n")
    rec=audit["recovery"]
    dr=dual["recovery"]
    summary={"run":"six-boss1-20261111","rows":19578,"columns":15593,
             "original_columns":4849,"unchanged_baseline_rows":19556,"appended_rows":22,
             "scope":"exact optimum only of the frozen finite necessary system; no SPE counterexample and no universal lower bound",
             "W":str(W),"W_float":float(W),"O":"1","below_half":W<F(1,2),
             "strict_half_gap":str(1-2*W),"half_minus_W":str(F(1,2)-W),
             "half_minus_W_float":float(F(1,2)-W),"old_W":str(old_W),"old_W_float":float(old_W),
             "exact_increase":str(W-old_W),"increase_float":float(W-old_W),
             "point_path":str(HERE/"augmented_lp_exact.json"),"point_sha256":verification["point_sha256"],
             "matrix_path":str(HERE/"exact_matrix.json.gz"),"matrix_sha256":verification["matrix_sha256"],
             "dual_path":str(HERE/"exact_dual_certificate.json"),"dual_sha256":verification["dual_sha256"],
             "all_rows_fraction_verified":verification["primal_rows_checked"],
             "all_columns_fraction_verified":verification["dual_columns_checked"],
             "canonical_max_auxiliaries_verified":7954,"canonical_min_auxiliaries_verified":2790,
             "positive_original_columns":rec["original_positive_columns"],
             "positive_max_auxiliaries":rec["old_max_positive_columns"],
             "positive_min_auxiliaries":rec["new_min_positive_columns"],
             "primal_rank":rec["rank"],"primal_variables":rec["variables"],
             "primal_free_variables":rec["free_variables"],"primal_free_values":rec["free_values"],
             "dual_rank":dr.get("rank"),"dual_variables":dr.get("variables"),
             "dual_free_variables":dr.get("free_variables",[]),"dual_free_values":dr.get("free_values",[]),
             "positive_dual_rows":verification["positive_dual_rows"],
             "positive_dual_new_rows":verification["positive_dual_new_rows"],
             "changed_original_coordinates":len(changes),"exact_optimum_verified":True,
             "solver_seconds":status["solver_seconds"],"solver_iterations":status["solver_iterations"]}
    (HERE/"result_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    cut_records=read("cut_records.json")
    new_slack={i:(name,F(value)) for i,name,value in verification["new_row_slacks"]}
    new_dual={i:F(v) for i,v in verification["positive_dual_new_rows"]}
    exact_cut_table=[{**record,"new_point_slack":str(new_slack[record["row"]][1]),
                      "new_point_slack_float":float(new_slack[record["row"]][1]),
                      "binding":new_slack[record["row"]][1]==0,
                      "exact_dual_multiplier":str(new_dual.get(record["row"],F())),
                      "positive_dual_multiplier":new_dual.get(record["row"],F())>0}
                     for record in cut_records]
    usage={"total_positive_dual_rows":verification["positive_dual_rows"],
           "new_positive_dual_rows":len(new_dual),
           "new_positive_dual_rows_theta_zero":sum(record["theta"]=="0" and record["row"] in new_dual for record in cut_records),
           "new_positive_dual_rows_theta_positive":sum(F(record["theta"])>0 and record["row"] in new_dual for record in cut_records),
           "claim":"This exact optimal dual uses four positive-discount new rows, and no zero-discount new row; this is certificate usage only, with no ablation or indispensability claim."}
    (HERE/"new_cut_exact_slacks.json").write_text(json.dumps({"point_sha256":verification["point_sha256"],
           "dual_sha256":verification["dual_sha256"],"usage":usage,"rows":exact_cut_table},indent=2)+"\n")
    summary["new_row_certificate_usage"]=usage
    (HERE/"result_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    lines=["# 22 条具名同源折扣行后的精确 LP",
           "", "RUN：`six-boss1-20261111`。本次只更新本页与 `discounted_augmented_lp/`。", "",
           "## 认证结果", "",
           "原 19556 行、15593 列的冻结必要系统追加 22 条互异原列不等式，得到 **19578 行、15593 列**。原 4849 列、7954 个正部辅助量、2790 个最小值辅助量、目标和归一化均保持。", "",
           f"精确有限系统最优值为 `{W}`，约 **{float(W):.16f}**。旧值约 `{float(old_W):.16f}`，增加约 `{float(W-old_W):.16g}`；距 1/2 仍有 `{F(1,2)-W}`，约 `{float(F(1,2)-W):.16g}`。", "",
           "该结论只属于这个有限必要系统：低于 1/2 不构成完整历史纯 SPE 反例，也不是原题的通用下界。六人一般共同目录半覆盖命题仍 OPEN。", "",
           "|文件|SHA-256|", "|---|---|",
           f"|`augmented_lp_exact.json`|`{verification['point_sha256']}`|",
           f"|`exact_matrix.json.gz`|`{verification['matrix_sha256']}`|",
           f"|`exact_dual_certificate.json`|`{verification['dual_sha256']}`|", "",
           "以上均在 `discounted_augmented_lp/`。新点可直接供后续分离；不得搬用旧点的行符号。", "",
           "## 恢复与独立认证", "",
           f"原变量精确恢复采用 {rec['variables']} 个正支持原列、秩 {rec['rank']} 的稀疏有理消元，剩余 {len(rec['free_variables'])} 个自由变量用保存的有理值确定。恢复之后重新计算全部辅助量。正质量原列 {rec['original_positive_columns']} 个，正 max 辅助量 {rec['old_max_positive_columns']} 个，正 min 辅助量 {rec['new_min_positive_columns']} 个。", "",
           f"对偶采用辅助列方程优先的稀疏有理消元：变量 {dr.get('variables')} 个、秩 {dr.get('rank')}、自由变量 {len(dr.get('free_variables',[]))} 个，最终正行乘子 {verification['positive_dual_rows']} 个。原始支持、零约化成本列、所有自由变量及其取值分别保存于 `primal_exact_audit.json` 和 `exact_dual_certificate.json`。", "",
           "独立核验器只用 Python 标准库与 Fraction，不导入构造器、恢复器或数值求解器。它核对输入与源码 SHA、全部 19556 条旧行逐系数不变、22 条新增全向量及去重、全部 19578 条 primal 行、15593 个变量非负性、全部 15593 条 dual 列、归一化、目标、原有 max/min 语义及互补性。primal 与 dual 目标精确相等。", "",
           "## 新行在新点的状态", "",
           "下表序号为零基矩阵行号；`actual_source_zero_based` 和 H 名称采用源包记法，不改写下标。", "",
           "|行号|源包名称|新点精确余量|精确对偶乘子|", "|---:|---|---|---|"]
    for record in cut_records:
        i=record["row"]
        lines.append(f"|{i}|`{record['name']}`|`{new_slack[i][1]}`|`{new_dual.get(i,F())}`|")
    lines += ["", "22 条精确余量、精确乘子、取等标志与源包字段另合并保存在 `new_cut_exact_slacks.json`。22 行包含 11 条 θ=0 的自由 portfolio、10 条二状态 θ=1/4、1 条四状态 θ=1/4；不重复添加已在旧点非负的 4906 条旧固定向量。", "",
              "**此最优证书实际使用的新增行均有正折扣。** 127 个正行乘子中恰有 4 个来自新增行，即 19569、19571、19574、19576，均为二状态 θ=1/4、actual 第 3 源。所有 11 条 θ=0 行以及新增四状态行，在此证书中的乘子均为 0。其余 123 个正乘子使用旧系统行。因此此证书将精确最优值的提高归于旧系统与这 4 条正折扣新行的组合；没有运行消融，不推断这些行各自不可或缺，也不推断零折扣机制的一般能力。", "",
              "## 输入、执行与复现", "",
              "三个冻结输入的 SHA：", "",
              "- 旧点：`bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3`。",
              "- 旧矩阵：`353b1978b6c2ad46d28dc33a03b5ff8c3f71f273d9bf4d71cc15f5a9cf223f0c`。",
              "- `selected_all_named_19556.json`：`3b373504be8593d6737433ea8341aac5eba67a153243392d173631e05f02e130`。", "",
              "依次执行本目录的 `python -B run_stage.py solve`、`python -B run_stage.py recover`、`python -B run_stage.py verify`、`python -B summarize.py`。前三阶段的实际执行脚本按 SHA 留在 `executed_sources/`，源参考脚本与包在 `source_snapshots/`。`inputs.json`、`recovery_inputs.json`、`execution_records.json`、各阶段 stdout/stderr 与 `final_manifest.json` 保存来源、依赖、命令、运行输出及产物哈希。", "",
              "数值求解只用于发现候选支持；最后结论来自保存的有理证书及独立精确回代。有限单位客户、共同非空标签目录、完整有序历史纯 SPE、任意平局、空主题、重复标签和零客户边界的原模型均未作改变。", ""]
    note=RUN/"discounted_augmented_lp.md"
    note.write_text("\n".join(lines))
    files=[]
    for path in sorted(HERE.rglob("*")):
        if path.is_file() and path.name!="final_manifest.json" and "__pycache__" not in path.parts:
            files.append({"path":str(path.relative_to(RUN)),"bytes":path.stat().st_size,
                          "sha256":sha256(path.read_bytes()).hexdigest()})
    files.append({"path":str(note.relative_to(RUN)),"bytes":note.stat().st_size,
                  "sha256":sha256(note.read_bytes()).hexdigest()})
    manifest={"created_utc":datetime.now(timezone.utc).isoformat(),
              "scope":"final artifact manifest for the certified ZZ19578 finite LP extension",
              "files":files,"file_count":len(files)}
    (HERE/"final_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("primal_free_values","dual_free_values","positive_dual_new_rows")},indent=2))


if __name__=="__main__":
    main()
