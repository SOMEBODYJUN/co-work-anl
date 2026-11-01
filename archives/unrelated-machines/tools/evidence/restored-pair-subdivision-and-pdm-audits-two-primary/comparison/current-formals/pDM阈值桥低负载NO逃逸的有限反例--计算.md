---
id: "unrelated-machines/pdm-threshold-bridge-low-load-no-escape"
kind: "computation"
type_tag: "计算"
title: "pDM阈值桥低负载NO逃逸的有限反例"
status: "finite-exact-counter-observation"
truth_status: "finite-instance-observation; not a general hardness or NO-gap theorem"
review_level: "full-frozen-json-read-and-scope-classification"
scope: "一个d=3、n=2、m=3、b=4的无完美匹配实例及648个整数分配的精确枚举记录"
summary: "精确记录显示无完美匹配时仍可有OPT/T=13/12；它只击破把无匹配直接推成近二NO值的朴素桥接。"
source_refs:
  - "source:2ff9d538ae90f44b6e38:evidence/runs/unrelated_machines/pdm_escape_counterexample_audit.json"
---

# pDM 阈值桥低负载 NO 逃逸的有限反例

## 输入和保存结果

冻结 JSON 使用 `fractions.Fraction exact`，实例参数为 (d=3,n=2,m=3,b=4)，阈值 (T=12)，4 个 dummy jobs，总工作量36。三条超边为

\[
\{a_1,b_1,c_1\},\quad \{a_1,b_2,c_2\},\quad \{a_2,b_1,c_2\}.
\]

记录穷举648个分配，确认 `perfect_matching=false`，但最优峰值为

\[
\mathrm{OPT}=13,qquad (L_1,L_2,L_3)=(12,11,13),qquad
\mathrm{OPT}/T=13/12.
\]

因此不存在峰值恰为 (T) 的调度（`NO_schedule_at_T=false`），但 NO 实例也没有自动产生接近二倍的峰值。这是一个精确的有限反观察，不是一般 NO 上界。

## 量词和处置边界

该记录自己把 claim scope 限为“有限观察；不是一般 NO 上界，也不是 UM-TARGET-v1 的困难性证明”。它只说明：从“没有完美匹配”到“NO 峰值接近 (2T)”之间缺少一个可直接使用的桥。pDM 阈值定理的 YES 阈值和有效 NO 实例的整数下界 `OPT>=T+1` 与本点相容；本点没有否定它们。

保存的原 JSON 在 [pdm_escape_counterexample_audit.json](../../tools/evidence/unrelated-machines/pdm-escape/pdm_escape_counterexample_audit.json)。该证据保存源程序 SHA 和重放命令，但本批未取得源代码正文；故本页不把字段重写为新的算法证明，也不外推所有 gap amplification、所有 (R\|C_{\max}) 算法或 NP 难度。它可作为后续关于阈值桥的反例关系边，不能作为六人半覆盖模型的反例。
