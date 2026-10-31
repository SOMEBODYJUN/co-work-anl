# tex_safe_polishing_zh 比较记录

- **Claim ID**：`eeea779c1adaeba50eb9`
- **源路径**：`research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing_zh.md`
- **源 blob**：`1ed0763b4ebdb651a98f9f0c630b21529092fe14`
- **源 SHA-256**：`615388149cd14b9d464044eb97cea64017f847a18d3f92c6454f0a6edb7b0f1c`
- **源大小**：19,517 B / 374 行

## 比较范围

本源中文指南逐节实读，并与以下已保存对象比较：

- companion `paper-polisher/SKILL.md`（source `a384c9cdb4e4cf198fd7`）：模式优先级、verification/consistency/approved-normalization 权限、共享 coverage/result 协议、完整稿件门槛、checker 调用与输出字段；
- 英文 `tex_safe_polishing.md`（source `08507e794b6ed17a804f`）：逐字节保护、结构 key、术语/记号/数值 ledger、full-manuscript gate、五模式、dash policy、保全脚本的语法边界；
- 归档的中文/英文 artifact verification、论文论证重构、反防御审计和 genre-profiles 资料；
- weighted-congestion `linear-article-assets` 的 build、pdf-reading、replay-comparison、self-check 和 provenance 证据层。

## 独有增量

中文指南把英文参考中的保护规则和审计协议改写成中文工作流，并新增/强调：

1. 明确四个必须分开的回答：候选是否保留 protected source、源内术语是否一致、源内记号是否一致、同一数值/单位/正负号是否一致；
2. 用完整的中文表格和例子解释裸 `\label{tab}`、错误的 `\cite`/`\ref` 重命名、caption 不能重复自动编号，以及 figure asset signature 的保护；
3. 将“不要自动猜修数字”扩展到单位换算、表格趋势、预期结果和作者姓名顺序，并给出 91.2%/92.1% 的 `NUM-* ISSUE REPORTED` 例子；
4. 细化中文 workflow 的 local/full/verification/consistency-only/approved mapping 五种模式、逐步骤 checker 调用和输出示例；
5. 明确自动数字扫描只是语法覆盖，不能替代数量到单位的语义审计或不可识别 macro/figure 的人工复核；
6. 以中文说明破折号风格规则与 lexical hyphen、URL/DOI、数学减号、signed value、`\pm` 的保护差异。

这些是用户-facing 解释和操作例，不新增数学对象或 TeX 工具权限。英文 SKILL 的 source-of-truth 仍优先决定模式和不变内容；中文 companion 不能放宽其保护规则。

## 与当前存档的边界

- 相对 artifact verification：本指南专门细化 TeX source-to-output preservation、symbol/number/asset ledger；artifact 资料负责 Text/Source/Execution/Render 层级和 freshness/hash。checker 通过最多是语法级静态证据，不是数学正确或 PDF 渲染成功。
- 相对论文论证重构：重构负责需求→瓶颈→能力→机制→证据的故事线；本指南不进行 broad storyline redesign，而是最终 faithful language/consistency pass。
- 相对 innovation/novelty 资料：那些资料审查 gap、危险 baseline、reviewer attack 和可防守 claim；本指南不宣称 novelty、priority 或外部 related-work 覆盖。
- 相对反防御审计：反防御资料决定句子功能的 Keep/Rewrite/Compress/Delete/Flag；本指南提供更硬的 TeX/math/number/key/literal 保护，不能把“语言更好”当作删除数学限定的许可。
- 相对 genre-profiles：genre 资料按文类安排论证责任；本指南保留各文类所需的 protected structures、结果和证据字段，不把统计/视觉文类迁移成 UM 数学模型。
- 相对 weighted-congestion build 证据：现有 build/pdf/replay/self-check 可展示编译、PDF 抽取和回放的分层保存；本次没有运行这些脚本，也不把现成论文的成功状态迁移到任意新稿件。

## 处置

本源保留为中文 TeX 安全编辑和审计资源，原字节置于 `original/`，本比较记录置于 `comparisons/`。本批未运行 `check_preservation.py`、未编译新 TeX、未检查任何完整论文的 figure/macro、未执行外部文献核验，也没有新增或修改数学结论。任何数字、单位、结构 key 或 theorem condition 的修改都必须在技能外得到作者确认的新 baseline。
