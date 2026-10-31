---
source_id: 46d4c496affb2362c2ac
source_path: history/research_operations/customer_attraction_transition/original/research/weighted_congestion_frontier/prompts/PAPER_WRITER.md
source_sha256: 2e1b577ed8df9b08e10f7e7f705a930c80ef6fabb22129cfd1f708d4dc17f17
source_blob: 6b341822c348540384a905733f1ceabd5908f555
source_size: 4941
source_commits:
  - 68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup)
  - aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)
proposed_disposition: integrated
proposed_target: archives/weighted-congestion/state/资料/历史角色提示词三件套--资料.md
---

# 语义清洗草稿：历史 PAPER_WRITER 提示词

## 实际读取

通过 `python3 work.py clean show 46d4c496affb2362c2ac --out ...` 完整读取 4941 字节 Markdown，并核对两个冻结提交、blob、SHA-256 和大小。两个提交中的正文逐字节相同。全文由标题、一个 `~~~text` 角色提示词块组成，没有代码、输入、运行输出或数学证书。

提示词把角色定义为“论文者”，要求从已有成果中挑选可成文的精确主张，核对最接近文献，区分已知机制、直接推论、新增内容和局限，完整重建承重证明/依赖，并按准确输入与复杂度写出可复现稿件。它要求不以改标题制造贡献、保留重要缺口，并将 proof、implementation、internal review、external review 和 novelty 分轴。

## 实际内容和量词

源中固定的历史主目标是迁移时点的 `UM-TARGET-v1`：一般不相关并行机 `R||C_max`，机器数 `m>=1`、任务数 `n>=0`，每个 `p_ij` 是二进制非负有理数或 `infinity`，任务必须分配到恰一台可用机器，目标是统一 `epsilon` 和确定性总位多项式时间算法，输出实际分配并满足 `(2-epsilon) OPT`，含 `OPT=0` 和空任务。源明确标为 `OPEN`，特殊输入、估值、准多项式结果和单个松弛 gap 不替代全量目标。

其余段落是历史仓库与写作流程：旧仓库 `main`、`unrelated-machines` save、随机 `W-<uuid>` 身份、旧 `research/weighted_congestion_frontier/tools/work.py`、旧 `board`/通信入口、旧 token 文件路径和独立 clone 合同；要求先读根/账本/失败路线/文献/模型，再把正文、问题、审查、代码、证据和个人桌面分层保存，执行旧 catalog/map/check 脚本并在 checkpoint 后才称远端保存。

## 全仓比较

- `archives/weighted-congestion/state/资料/历史角色提示词三件套--资料.md` 已完整处置 `CLEANER.md`、`EXTRACTOR.md` 和 `MODELS.md`，明确这些提示词是历史角色/模型路由材料，不是 weighted-congestion 定理；本源的 PAPER_WRITER 与三件套互补，补充论文成稿角色、文献核对和证明/实现/审查/新颖性分轴。
- 现行 `archives/weighted-congestion/README.md`、`prompts/README.md` 和 `cleanup/OBJECTS.md` 仍要求把数学对象按定义、定理、反例、审查、计算和证据分开保存；这一证据纪律与源的成稿原则相容，但当前结果分支、Boss 编号、`rebuild/research-v2`、`clean claim/done` 和根 `work.py` 已替代旧 `main`/随机 W-uuid/旧工具路径。
- 现行 `archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md` 承载 UM-TARGET-v1 的精确输入、四项承重义务及 OPEN 状态；源中的目标文本可作为历史版本路由 provenance，但不能用它推出近二算法、困难性、P≠NP 或外部文献优先权。
- 源没有新的证明、反例、程序、输入、运行或外部文献核验。它的独有价值是历史“论文者”职责、成稿门槛和旧模型全量目标措辞，而不是一个需要写入 `state/定理` 的数学对象。

## 处置建议和边界

建议处置为 `integrated`，并入现有 `历史角色提示词三件套--资料.md`，补充：

1. `PAPER_WRITER` 要求从已存在成果中挑选精确贡献、重建证明并核最近文献；没有成果时推进证明/提炼，不靠改标题。
2. 旧 `UM-TARGET-v1` 的完整输入量词及 `OPEN` 状态只作为历史路由版本，数学真值回到当前 unrelated-machines canonical 对象；不能迁移成 CAG 半覆盖结论。
3. 论文成稿与研究/清洗角色不同：写作提示词本身不授权新认领、不会替代 `clean show`/`checkpoint pushed`/`clean done`，也不替代第三阶段关系图。
4. 旧构建检查命令、随机角色身份、main 分支、旧 token 路径和旧通信命令保留为历史上下文，不作为当前执行指令。

原字节应在现有 `archives/weighted-congestion/tools/evidence/history-transition-prompts-20261031/` 证据包中增加本源条目（或另建同批 manifest），保留两个冻结提交、SHA、blob 和“未运行写作/构建命令”的边界。不建议标 `duplicate`：三件套没有涵盖论文者成稿职责和完整目标文字；也不应标数学 `retired`，因为它仍是可复核的历史协作材料。

第三阶段若建关系，只能是“历史 PAPER_WRITER 角色提示词 → 当前论文/对象入口”的资料关系；不能从提示词到 UM 定理、设施结果或客户吸引 half 目标建立 `derives` 边。

## 回执字段建议

```json
{
  "id": "46d4c496affb2362c2ac",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "完整读取4941字节历史PAPER_WRITER提示词，核对两个冻结提交、blob、SHA和全部角色/目标/保存段落。",
  "comparison_note": "与历史CLEANER/EXTRACTOR/MODELS三件套、现行weighted-congestion对象规范、unrelated-machines入口和cleanup协议比较；确认本源是论文成稿角色与历史UM目标路由，不含数学证明或运行证据。",
  "decision_note": "独有内容是论文者的贡献筛选、证明重建、文献核对和五轴状态纪律；整合到历史角色资料并保留原字节，旧main/W-uuid/旧命令只作版本边界。",
  "disposition": "integrated",
  "targets": [
    "archives/weighted-congestion/state/资料/历史角色提示词三件套--资料.md",
    "archives/weighted-congestion/tools/evidence/history-transition-prompts-20261031/source-manifest.json",
    "archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md"
  ]
}
```
