# RA11 对抗审计报告（独立第一轮，初步）

审计者：`/root/ra11_adversarial_audit`
对象：`RA11`（仅此篇）
时间：2026-11-25
方法：独立读取当前 ledger/manifest/current、审计证据与正文索引；未读取其他两个核心恢复者的结论。

## 当前硬门槛状态

- `source_units=14`，`target_units=690`，`old_units=0`，`recoveries=0`，`issues=2`，`page_checks=28`，`region_checks=168`，`final_rounds=0`。
- 两个 issue 仍为 `open`：`RA11-ISSUE-01`（p0001 二进网格分层下标）和 `RA11-ISSUE-02`（p0005 Egoroff 尾集页边省写）。两者的 `resolution` 均为空。
- 两个相关 source unit（`RA11-P001-U01`、`RA11-P005-U01`）状态却已是 `resolved`，且没有任何 recovery 记录。这是当前最直接的假解决风险：source 状态不能覆盖 issue 的未决语义。
- 全部 page/region 检查只有 pass 1/2，未有内容快照后的三轮独立终审；`final_rounds=0`，所以当前审计不可能满足冻结门槛。
- `autonomous-recovery/recovery-plan.json` 仍仅记录上述两个 issue；没有候选、原图裁图证据、前向/反向检验或解决后哈希，不能将“疑点已登记”当成恢复完成。

## 映射与覆盖的红旗

- 14 个 source unit 各自挂载同一组 259 个 `study_target_ids`（共 3,626 条链接而仅 259 个唯一 ID），而 `transcription_target_ids` 为 401 个唯一逐页目标。这种全篇重复挂载使 study source→target 反向关系无法证明；必须逐 target 核验其真实 page/source 证据，不能以 source unit `resolved` 掩盖。
- p0001 source unit 有 32 个 transcription targets、p0005 有 33 个；两者的 source/target 具体对应和页边疑点尚未以 recovery 记录固定。应检查每个相关 target 的 `source_ids`、`region_ids`、文本片段和颜色标签是否与原图一致。
- `old_units=0` 与当前 run 的 previous-markdown 约束一致，但仍应验证正文/映射无幽灵旧稿 ID；不可用空 old_units 代替旧稿去向审计。

## 证据/哈希风险

- 当前 artifact 清单含正文、审计和第二遍视觉文件，但没有 RA11 核心三人盲读/候选/对抗文件（本文件为首次补齐）。`manifest_sha256` 和正文 artifact 哈希必须在任何实质修订后重新计算。
- `audit-report.json` 的结构错误至少包含最终三轮缺失；在 issues 未关闭、recoveries=0 时，不能把当前报告改写成 pass。
- 需逐一比对 source transcript/study notes 的红色疑点、ledger issue 状态、target mapping、artifact SHA-256；任何只改正文或只改 ledger 都是假解决。

## 必须继续的对抗动作

1. 回到原 PDF 对 p0001、p0005 做整页定位和 800 dpi 定向裁图（小字/页边必要时 1200 dpi），记录页号、分区、bbox、相邻符号、笔画和版式关系。
2. 为每个 issue 至少记录两个候选，并分别完成原图笔画比对、作者记号习惯比对、前向定义/证明检验、反向结论/条件检验；数学通顺只能列为支持证据。
3. 检查 14 页的 page/region coverage，特别是页边、跨区接续、空白/内容分类；对全篇重复挂载的 study targets 逐 target 做反向 source 检验，发现污染须由 Boss 在整篇同步修订。
4. 修订完成后必须同步 source/target/recovery/issue/page/region/颜色/证据哈希，重新生成 recovery-plan，清空未决，之后再在新快照上完成第二遍视觉复核和三轮独立终审。

## 第一轮结论

RA11 当前不可提交、不可 release、不可切换 RA12。两个疑点仍真实未决；source 已标 `resolved` 而 issue/recovery/证据链未闭合，且 study 映射存在全篇重复挂载的高风险。该报告只记录独立第一轮审计发现，不替代后续原图恢复。

## 后续独立图像与账目复查（仍未读其他 reviewer 结论）

- 直接查看 `pages/p0001.png` 与 `pages/p0005.png` 的整页以及 recovery-plan 指向的原图裁图后，确认两页确有可读内容和边缘/公式区域；原图回查必须再由核心组以 800 dpi（小字 1200 dpi）记录 bbox，不能把当前 400 dpi 全页作为唯一候选证据。
- 直接查看 `pages/p0014.png` 并用像素统计复核：3306×4678 全白，暗像素比例为 0；该页没有正文、公式、页码、边注或跨区接续。可是 `pass1-page-p0014` 和 `pass2-page-p0014` 均错误标为 `assessment: content`，六个区域两遍也用同一套“内容页的一部分”模板，且都指向 `RA11-P014-U01`。这是已核实的 page/region 假解决，必须改为 blank，清除该 source unit 的 source/target 挂载，并只保留编辑性页序说明。
- `source-transcript.md` 第 471–475 行把空白第 14 页写成 heading/正文 targets（T-0472、T-0474、T-0475），其证据哈希仍指向 `image:p0014`；这些 targets 与空白原图不相容，须改为无 source 的 editorial 记录或删除，且同步 study notes、mapping、artifact 哈希。
- `audit/unresolved.md` 还列出 Q001–Q008（p0001、p0003、p0004、p0007、p0008、p0010、p0013），而 ledger.issues 只有两个 RA11 issue；这八条不能静默丢弃。应逐条回原图复核并去重：若已解决，保留候选、排除项及证据；若仍有歧义，转成 recovery/issue，直到未决数为零。
- `audit/mapping.json` 的 71 个行级 ID（如 `RA11-P001-01`）与 ledger 的 14 个页级 source IDs（如 `RA11-P001-U01`）完全不重合。该文件不能直接证明 ledger 的双向 source/target 映射；整合时要明确行级 map 与页级 source 的桥接，或者同步重建 map。当前 14 个 source unit 各挂 259 study targets 的重复挂载进一步放大了这个缺口。

这些新发现使 RA11 当前仍明确不可提交；p0014 空白页错判和 Q001–Q008 遗漏必须先由 Boss 与核心恢复组处理。

## 三人盲读解锁后的对抗合并提示（不替代 Boss 决断）

在本报告第一轮盲审文件写入后，才读取视觉恢复者与数学上下文恢复者的独立记录。两组对 P001 行末上界出现实质分歧：

- 视觉记录的 800 dpi 局部把行末读成 `j=1,\ldots,2^k`（末端可见独立 `2^k`，置信度 0.78）。
- 数学记录把候选首选列为 `j=1,\ldots,k2^k`，理由是必须覆盖 `[0,k)` 才能与 `f\ge k` 截断分支和后续误差界闭合。

这不是可投票消除的差异；在选定前必须追加 1200 dpi 原图裁图、扩大同页公式/作者字形上下文，并把被排除候选及其前向/反向失败写入 recovery。不得仅以标准教材写法覆盖原笔画。

P005 也有独立记录差异：视觉记录暂选带上横线的 `\bar E_n(\varepsilon)`，数学记录暂选普通 `E_n(\varepsilon)` 并把横线视作页边省写。需回图确认横线是否与主体相连、是否在后续同页重复，并同步颜色标签与正文。两个分歧解决前，RA11 仍不得冻结。

## 更细的反向映射计数

逐 target 计算发现每个页级 source unit 的 `transcription_target_ids` 均有反向链接，但另外多挂了完整 259 个 study target；例如 P001 为 32 个声明转写目标、291 个反向总目标、额外 259 个 study 链接，P014 为 3、262、259。该污染同时存在于 14 页，不是单页偶发项。修订时应按真实页/段证据重建 study source→target 关系，不能保留全篇复制列表后宣称双向验证通过。

当前 404 个 transcription targets 与 source-transcript 行哈希、286 个 study targets 与 study-notes 行哈希在未修订快照上均一致；这只说明记录未被意外改写，不证明内容正确。任何空白页清理、候选定稿或链接重建都必须重新计算受影响 target、artifact、manifest 与 snapshot 哈希。
