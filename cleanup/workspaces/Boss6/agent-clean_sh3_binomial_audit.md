---
agent: Boss6/clean_sh3_binomial_audit
source_id: "0100c3dab772bd7bb80c"
source_sha256: "a6bd7ba669aa21108a8495e4cc02b0eaa969b20a76d542875f13b85378bf065b"
source_path: "history/source/notes/unrelated_machines/sol_raw_sh3_inclusion_entry_cut_binomial_audit_v1.py"
review_status: "full-source-read-and-exact-replay"
recommended_disposition: "integrated"
---

# 来源处置：SH3 包含切口二项式有限审计增量

## 实际读取与运行

已用 `work.py clean show` 完整导出并逐段读取 6569 字节源程序；源为整数/`Fraction` 的有限审计，不是 SDP 求解器或完整矩阵生成器。源定义 120 个二项式参数案例：`q` 为 4、8、16、32、64，`m` 为 `100q`/`104q`，四组 `(a,b)` 与四个 `delta`。每行检查四个边界不等式、计算 `strict_reverse_cut` 与精确切口余量，并记录巨大参数计数。

源还独立构造 `q=2,m=6` 小矩阵：45 台机器、106 个原作业、750 个有限端；检查 690 个 CONFIG1 支持项、106 条覆盖等式、750 个端点边际和 106 个完整路径分配，精确峰值为 `11/6`。

源固定绝对输出路径；本轮未改源字节，而在内存替换 `OUT` 后运行一次。输出 `binomial_cases=120`、`strict_reverse_cut_cases=85`，小矩阵字段与源审计一致。回放 JSON SHA-256 为 `116d696240e103c3c3203612eb03fae40e407530188e7a7ea559cf3be80d53b8`。

## 比较与处置

仓库已有 `archives/unrelated-machines/state/审查/SH3包含切口二项式有限审计--审查.md`，保留同一有限审计的 120/85/11/6 结论和非一般边界；已有 `rawSH3条件子树流与集合包含切--资料.md`、`原作业SH3子树流与包含容量双源续审查--审查.md` 和历史 evidence 解释该审计与条件流对象的关系。当前来源的独有内容是可执行源程序本身和本轮重定向后的精确 JSON 回放，不是新的数学定理。

建议把源与回放作为 `integrated-finite-audit-increment` 并入现有 SH3 审查对象，保留原程序、输出与 manifest 的 SHA；不新建第二个 SH3 身份。严格区分：120 个参数行是有限精确检查，`strict_reverse_cut` 只有 85 行为真；q=64 字段不构成全称失败；小矩阵不在 `m>=100q` 渐近域。没有物化大矩阵、SDP、所有完整指派或未知 source decoder，因此不升级为一般切口定理、近二算法、hardness 或 UM-TARGET-v1 结论。

## 证据位置

- 原程序：`archives/unrelated-machines/tools/evidence/raw-sh3-inclusion-cut-binomial-audit-20261031/original/sol_raw_sh3_inclusion_entry_cut_binomial_audit_v1.py`
- 回放：`archives/unrelated-machines/tools/evidence/raw-sh3-inclusion-cut-binomial-audit-20261031/runs/0100c3-replay.json`
- manifest：`archives/unrelated-machines/tools/evidence/raw-sh3-inclusion-cut-binomial-audit-20261031/manifest.json`
- 正式目标：`archives/unrelated-machines/state/审查/SH3包含切口二项式有限审计--审查.md`

## 建议 receipt

```json
{
  "id": "0100c3dab772bd7bb80c",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "完整读取6569字节有限二项式审计程序；核对120案例、四个Fraction边界、strict_reverse_cut、q=2,m=6完整小矩阵和11/6路径峰值。",
  "comparison_note": "与既有SH3包含切口审查、raw SH3条件流资料、历史evidence和相关CLAIMS对照；确认源程序是已有有限审计的可执行原件，独有增量是本轮重定向回放。",
  "decision_note": "整合为有限审计增量，保存源/回放/manifest与哈希；不物化大矩阵、不宣称一般切口定理、SDP、hardness、近二算法或UM-TARGET-v1结论。",
  "disposition": "integrated",
  "targets": ["archives/unrelated-machines/state/审查/SH3包含切口二项式有限审计--审查.md"]
}
```
