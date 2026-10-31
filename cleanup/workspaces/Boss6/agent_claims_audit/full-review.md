---
source_id: "984a73cedc8b69b63593"
source_sha256: "f71b0a42197aa4a8ad6c680c8c525fae26f667355bf5313a85da5ace04dc3ddc"
source_path: "research/unrelated_machines/CLAIMS.md"
source_bytes: 586921
source_lines: 3702
frozen_commits:
  - "68fad804ec5946cb296f77dc5b336308a66abf12"
  - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
review_status: "full-byte-read; semantic-ledger-review; integration-pending"
recommended_disposition: "needs-decision"
---

# CLAIMS 账本完整复核（Boss6 本地审查）

## 复核证据

本地冻结副本 `cleanup/workspaces/Boss6/CLAIMS.md` 已完整读取，字节数为 586,921、行数为 3,702，SHA-256 为 `f71b0a42197aa4a8ad6c680c8c525fae26f667355bf5313a85da5ace04dc3ddc`。逐行索引和章节边界保存在 `section-index.json`；不是只搜索关键词或只读开头/目录。全文共有 320 个二级/三级章节标题，其中 306 个带 `UM-...` 身份（306 个唯一身份）。

账本不是一篇单一证明，而是主目标、已知工具、条件构造、有限审计、方法障碍、反例和候选的状态账。全文交叉检查了每节的精确命题、对象/域、量词、结论、依赖、证据、反面意见、状态和相关文件字段；结构统计如下：

- 306 个 UM 身份中，303 个有独立 `Status` 字段；3 个把状态并入 `Scope / Status` 或 `Counterevidence / Status`，需要后续 schema 修正。
- 260 个章节有 `Exact Statement`，245 个有 `Objects`、`Assumptions`、`Dependencies`、`Counterevidence` 四类承重字段，160 个有单独 `Conclusion` 字段。
- 275 个章节同时列出 `Evidence` 和 `Related Files`；另有 4 个章节缺 `Related Files`，不能仅靠账本字段证明目标文件已入库。
- 152 个章节仍写明主目标 OPEN、候选或待内部攻击；136 个是已声明范围内的结果/接口，4 个是限范围障碍，3 个明确标为已反驳接口。任何这些状态都没有把 `UM-TARGET-v1` 升级为已解或一般困难性定理。

## 数学内容的整体处置

`UM-TARGET-v1` 的量词仍是一般 unrelated parallel machines、非负二进制有理处理时间、禁用边、必须完整分配、输出实际调度、统一与规模和精度无关的 `2-epsilon` 余量。全文反复区分：

1. 给定分数/配置/共同见证的条件舍入，与从任意输入寻找见证的算法；
2. 估值、有限枚举、局部搜索终止，与实际整数输出及输入位长多项式复杂度；
3. 配置或固定层松弛的间隙，与相对真实 `OPT` 的一般近似下界；
4. 方法合同的反例/失败步骤，与对所有算法的近二困难性；
5. 一般 UM 模型，与 restricted assignment、Santa Claus、图平衡、客户 SPE 等保持独立身份的模型。

账本中可复用的独有内容主要是状态和边界组织：给定共同容量的 ST 舍入接口、配置/联合投影/矩与复制的精确反例、未知目标搜索与共同见证选择的复杂度缺口、物理 decoder 与 sound `FAIL` 的必要义务、固定字母表的 gcd 正面障碍、以及多条已纠正的旧路线。它们应由各自数学对象、审查和证据承重；账本本身不应被第三阶段当作一张自动关系图。

## 与当前结果树的交叉核对

按 306 个身份在当前 `archives/unrelated-machines` 全树（Markdown、JSON、Python）查找：255 个身份至少在一份现有证据/历史/对象文件中出现，51 个身份没有任何当前树命中。这 51 个身份列在 `unreferenced-claim-ids.txt`，包括若干 `UM-3DM-DEMAND-FLOOR-OBSTRUCTION-v1`、`UM-ANCHOR-DEFICIENCY-*`、`UM-CONFIG-FINITE-COVER-v1`、`UM-DILUTED-SHARED-TERMINAL-*`、`UM-NORMALIZED-*`、`UM-SEVEN-STATE-*`、`UM-SMALL-DENSITY-FLOW-BARRIER-v1`、`UM-TREE-MARKOV-COMPLETION-NO-v1` 等。它们不能仅凭本账本的摘要算作已入库数学对象。

当前正式对象 frontmatter 直接声明 `legacy_ids` 的身份约 139 个；其余身份即使可在证据历史或正文引用中找到，也缺少稳定对象映射，需由后续清洗者逐一决定是合并到已有对象、建立新对象，还是保留为账本级历史导航。旧 `research/current/...` 和 `research/reviews/...` 路径在结果分支中多数不以同名文件存在，属于冻结来源/证据路径，不能把链接存在性当作数学真值。

## 推荐处置

建议暂保持该源为 `needs-decision`，理由不是全文未读，而是全文已读后仍有真实入库缺口：

- 51 个身份没有当前树中的对象/证据命中；
- 3 个实际命题章节缺独立 `Status` 字段，4 个缺 `Related Files`，另有多节缺对象/假设/依赖/反面字段；
- 账本记录了大量候选、条件结果和开放失败边界，不能把它们批量标为 `integrated`；
- 现有总览对象可以吸收已核实的共同义务和失败机制，但不能替代逐身份对象正文。

下一步应按 `unreferenced-claim-ids.txt` 逐一查找冻结原文、现有证据和后续纠错，先把自足正文/证据 checkpoint 到结果分支，再为该源提交 `integrated`、`retained` 或 `duplicate` 记录。只有所有身份都有准确去向后，才可把本账本源从 `needs-decision` 改为完成处置。此本地审查未执行 `claim`、`done` 或远端 `push`。
