---
id: "customer-attraction/root-tax-upload-transport-20261030-review"
kind: "review"
type_tag: "审查"
title: "四人根税独立上传与传输接口增量审计"
status: "complete"
truth_status: "exact-full-tree-replay-and-interface-regression"
review_level: "source-read-independent-Fraction-audit-no-universal-half-claim"
scope: "2026-10-10 四人根税单位客户独立上传审计的七个CSV/JSON输出，加同日传输接口整合报告；固定61客户完整SPE、有限接口回归与既有证书"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/all_deviations.csv"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/all_nodes.csv"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/comparison_21_pairs.csv"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/last_replies.csv"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/numeric_claims.csv"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/static_safety_56_multisets.csv"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/root_tax_upload_independent/summary.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-10/transport_integration_checks.json"
evidence_dir: "archives/customer-attraction/tools/evidence/root-tax-upload-20261030"
---

# 1. 来源与完整读取

本批认领八个冻结源。七个来自 `root_tax_upload_independent/`：六个 CSV（节点、偏离、21 个无序前缀对、216 个末位回复、74 项数值断言、56 个静态竞争多重集）和一个 `summary.json`；第八个是同日的 `transport_integration_checks.json`。所有源均用 `clean show` 导出，原始字节保存在 `tools/evidence/root-tax-upload-20261030/`，manifest 记录源 ID、字节数和 SHA-256。

CSV 已逐行解析而非只取首尾：偏离表 1,295 行、节点表 259 行、比较表 21 行、末位表 216 行、数值断言 74 行、静态安全表 56 行；Fraction 字段逐项转成有理数并检查计数与布尔断言。两个 JSON 被完整遍历所有顶层字段、嵌套数组和审计运行记录。相关稳定正文 `四人实际根总税--反例.md` 与 `税接口精确审计--计算.md` 已全文比较。

# 2. 61 客户四人完整 SPE 的独立单位客户重放

`summary.json` 的顶层结论为 `verdict=PASS, independent=true`。输入包含 61 个单位客户、六个共同主题，策略实际终局为 `AAAF`，全部 1,296 个终局配置和 259 个非终局节点均已生成。数值字段为

\[
W=38,\qquad \operatorname{OPT}_4=61,\qquad \tau=45/2,
\qquad \operatorname{OPT}_4-(W+\tau)=1/2.
\]

因此它重放的是既有“实际根总税”反例：若 \(b_x\) 只计前三位实际覆盖的负载，则 \(\operatorname{OPT}_4\le W+\sum_x b_x/(b_x+1)\) 在本实例严格失败半单位。该数学对象不是新反例 ID，而是旧完整正文的独立单位客户实现证据。

## 2.1 全部历史与偏离

节点表按历史长度给出 `1+6+36+216=259` 个有序节点，分别属于四位玩家 1、6、36、216 个节点。每个节点保存实际行动、实际终局、六个候选行动收益。偏离表逐节点枚举五个非自身行动，共 1,295 行；所有行 `passes=True`，没有盈利偏离，严格更差 1,230 行，平局 65 行。因此这是完整纯 SPE 证书，但不是严格 SPE；平局保持在定义内，不能被摘要的 `PASS` 掩盖。

21 个无序前缀对的比较表逐项与原稿一致，最大非 A 行动的 margin 从 0 到 4；AA 行唯一 margin=0，其他行均有正边际。末位 216 个历史的选行动计数为 A:200、E:3、F:13；每行 `best_actions` 是该节点的最优行动集合，三路平局长度为 3 或 5 的记录保留，没有把任意平局改写成唯一响应。

74 项 `numeric_claims` 全部通过，包含客户数、主题大小 `(30,10,11,10,20,20)`、A/B/C/D 分割、259 节点、1,295 偏离、1,296 终局、`AAAF` 实际收益 `(9,9,9,11)`、`W=38`、`OPT=61`、根税 `45/2`、RT 缺口 `1/2`、`FAAE` 第一位偏离续局、末位回复表、静态安全值和五个边界测试。它是机器重放的断言清单，不替代正文中对策略量词和客户分割的数学说明。

## 2.2 静态安全值的独有表格

56 个竞争主题多重集的完整表逐行保存六个查询收益、混合值和原始 margin。最小混合值为 9，等号恰有 5 个多重集；其余 margin 非负。对偶纯列 `AAF` 的六个查询值为 `(9,9,9,9,9,7)`，所以和既有正文相同，得到指定静态不观察安全值 `v_4=9`。本实例满足每个实际玩家收益至少 9，且

\[
W-4v_4=2>0,
\qquad 2W-\operatorname{OPT}_4=15>0.
\]

这部分只保留“静态安全桥在该实例兼容”的证据；它不能把实际根税失败升级成聚合安全反例，也不能替代顺序隐藏回复的动态证明。

## 2.3 负向与边界控制

摘要保留 5 类边界：单人非空、四人唯一空主题、重复覆盖不同标签、两人不交单例和全空标签。负向控制包含 3 个应当产生盈利偏离的错误策略；它们被检测到，不是 SPE 候选。边界记录用于确认实现对空主题、零客户、重复标签和离轨历史的处理，没有改变 61 客户主实例。

# 3. 传输接口整合报告的范围

`transport_integration_checks.json` 不是新的全称定理，而是将同日 CAG 审计、源 SHA、结构检查和测试回归放在一个整合包中。其声明 scope 是“exact general interfaces and local or specified-cone boundaries; arbitrary-n half coverage and global compensation remain unproved”。结构检查 `build_map --check`、`build_crosswalk --check`、`check_assets` 与 11 个 `unittest` 全部退出 0；58 个源 SHA 均有登记。

十个审计运行中，与本批对象直接相关的边界如下：

* dynamic iid 主审计与独立审计都重放五人七主题、60 客户、2,801 历史、19,607 比较，`OPT_5=60,W=58`；实际路径 `[6,6,0,3,4]`，收益 `[12,12,10,12,12]`，局部弱漂移缺口 `1/5`，旧尾债总和 `-5/3`，但全局弱 iid 桥保底余量为 4。报告明确 `root_Z_exactly_computed=false`、`unrestricted_global_iid_bridge_proved=false`。
* 五人 86 客户逐人安全独立审计保持 `OPT=86,W=85,v=2262/139`，首位安全缺口 `51/695`，half margin 84；这与本批四人 61 客户的静态安全表是不同输入、不同对象，不能合并为一个反例。
* 新策略安全锥运行再次报告 21 棵、95,349 历史、709,573 比较；其固定策略量词已在本批另一份“新策略安全锥与半顶点候选增量审计”单独登记。
* security-chain、stationary-pair、terminal-transport 的运行均为 PASS，但分别标注“局部归纳失败而聚合/half 仍成立”“指定 Q 失败而非全局桥反例”“给定 canonical certificate 的条件提升”。它们是接口边界，不能从整合报告中抽取一般补偿定理。

报告的三条 limitations 明确写出：这是内部审查、无外部新颖性或同行评审；局部负债和指定核失败不是全局安全或 half 反例；21 棵完整策略锥不是 universal catalog theorem。故整合报告的用途是关系证据和回归水位，不是为四人 RT 反例之外的命题背书。

# 4. 与既有正文的比较及处置

1. 与 `四人实际根总税--反例.md`：全部核心数值、21 对前缀比较、216 末位回复和 56 个静态背景逐项一致；本批独有的是独立单位客户实现的完整 CSV 输出、74 项断言清单和负向控制。处置为集成到既有反例，保留独立字节，不另造同实例反例。
2. 与 `税接口精确审计--计算.md`：transport integration 的测试与审计边界复核了“固定完整策略证书而非一般所有 SPE”的总量词；本批补齐同日上传文件的逐源登记。处置为增量审查，不把结构检查字段当成数学证明。
3. 与 `逐人安全与全树流增量审查--审查.md`：同一整合包中的 60/86 客户流、安全锥与本批 61 客户根税分开保留；没有把局部弱漂移或逐人安全失败误连到 RT 或当前六人 half 目标。
4. 与当前 Q-CAG-HALF-6：本批实例只有四名提供者、六主题、61 单位客户，证明的是一个四人全历史纯 SPE 的根税失败和静态安全兼容性。它既不是六人目录覆盖反例，也没有检验“每份完整历史纯 SPE 至少达到六个目录主题最大覆盖人数一半”。

# 5. 后续接续

* 若第三阶段引用 RT 缺口，使用 `summary.json` 的 `OPT4=61,W=38,tau=45/2,RT_gap=1/2` 与 1,295 行全偏离表；不要只引用摘要中的 `PASS`。
* 若需要复核静态安全值，使用 56 行完整表和 `AAF` 对偶列；若需要复核 SPE，使用 259 节点和 1,295 偏离，而非只看 21 行合并比较。
* transport integration 的 58 个 SHA 和十个 audit run 只作为关系/回归证据。任何新的一般税、聚合安全或六人 half 说法仍须独立领取并实读相应来源。

结论等级：本批是“既有四人实际根总税反例的独立完整单位客户复核 + 传输接口边界审计”；反例本身保持完整证明层级，整合报告保持有限接口/回归层级，没有新增一般 SPE、全局补偿或六人 half 结论。
