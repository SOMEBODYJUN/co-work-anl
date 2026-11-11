# TWO-MINIMAL-SOURCE-ERRATA：Root审查候选

本目录仅为本地 staging。只读 co-work-anl-boss6；没有执行 Git、work、queue、registry 注册、bind 或任何 clone 写入。全部候选由现行精确源字节作最小替换；没有运行冻结数学 driver，也没有新建数学对象或正式审查对象。

## 交付范围

- `bodies/`：两个正文的完整候选字节。
- `two-source-errata.patch`：两正文统一 diff。Root 可直接采用完整正文；CAG候选与此前两段勘误完全同字节。
- `registry-batch.candidate.json`：schema 2，精确6个既有对象、2个材料、空edge_files；不含完整registry，也不捕获原registry的edge_files。
- `materials-update.candidate.json`：同batch中2个材料条目的独立查看副本。
- `manifest.json`：源SHA、六对象前后canonical pins、字段差异、全current-owner扫描与本地任务/边影响清单。

集成时必须以Root届时的latest registry为base，保留全部最新边和其它owner。manifest内旧registry SHA仅是观察快照，不能当作登记base。任务/owner记录也是只读本地快照；ca44扫描期间已从claimed改为handoff，未把旧记录当作最新远端归属。

| 正文 | 旧SHA256 | 候选SHA256 |
|---|---|---|
| archives/customer-attraction/state/计算/实际末主题单枝与三枝条件联合的精确点--计算.md | `99f93e2a6bd7d52a71b60e93f1b187b2fd08d2cb3271f93c4c2c3143244a5406` | `17d527b0a34cf42c66d8cd2a13b30570b3bb2a62a2a0b040292552fa7cbe160a` |
| archives/unrelated-machines/state/文献/结构参数下的指派限制调度--文献.md | `a2c918daef8cb6711a97a56fbdca355f2e72fd1136ff6dbc1216f393d577aaa1` | `113ed833ea9443fe2166793c19b5fe2b1b6bfb3b789e6f617372120d1c90375e` |

## CAG：失败driver与历史成功记录的边界

原正文只替换原L86和L88两段。现存verify_fixed_point.py与replay/failed-type-comparison/verifier.py确为相同SHA256 152200c7426a02563be1b6cbc930f9b1bcb9da6f1694ec8ca02fde0ef30175e7；直接检查第25行可见tuple/list直接比较，第69行字段仍无JSON规范化后缀。

历史single/families summary确含`all_saved_column_descriptors_equal_builder_after_JSON_tuple_array_normalization`，报告原行有理非负；对应execution的exit_code确为0。execution记录外部stage脚本路径，但没有成功driver的源码字节或SHA绑定。总账保存失败与成功事件。它们支持历史记录的身份，不能给当前失败driver追认成功复现。未猜测或恢复成功driver。

以下三路径当前registry.materials均不存在，当前registry也无既有evidence owner；因此本候选不追加它们到CAG objects的evidence/sources，两个原列表逐字保留。它们只在正文/本review与manifest中作为已冻结历史溯源记录列明，不产生新增材料登记。

| 历史记录 | SHA256 | 有限作用 |
|---|---|---|
| archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/replay/attempt-ledger.json | `e99b65c800c831db73161b1b78a0c2a4eb415276b638b75979ad9ac003014356` | 区分保存失败、容器比较失败和历史规范化成功事件 |
| archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/replay/single.execution.json | `2353f4da8dfd674bfb202c7346b1f46e80c094987bd929f1fc914cc1f94b430a` | 单枝历史外部命令exit0；无成功driver SHA |
| archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/replay/families.execution.json | `7fdea1a8a9f743458e74a730530a8bda8c74562aaa49dcbb463fcd25887f9696` | 三枝历史外部命令exit0；无成功driver SHA |
| archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/replay/single/summary.json | `183aa54cb4f1973f5c450d2888c8703158354d5c8a90b38bba90320a4bb67212` | 已保存历史成功summary；现有object evidence原已绑定 |
| archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/replay/families/summary.json | `33c07c3ba338f52bf067da0ad987f1f44d3c72cfde5565e918641283d6f5b11d` | 已保存历史成功summary；现有object evidence原已绑定 |

两CAG对象仅v1→v2、body SHA与objections变化。原statement、全部数学数字、truth_status、原evidence和sources完全不变。原脚本、PDF、向量、成功/失败输出均冻结。

## UM：m²费用与端点的独立核验

直接查看已有worker渲染的原PDF页17图，Results原式确为O(m² n^{O(d2^k)})；上标2属于m。并读取同一source的页5提取文本：分解树内部节点全为3度，所以常规分解有O(n+m)节点；固定k的分解构造在总图顶点数上为三次多项式。其外引构造定理未在本次独立重证。

令q=2^k。非空可行分支n,m≥1，实际尺寸种类d≥1，故dq≥1。一个计数坐标的0..φ有φ+1种，单方向表大小≤(n+1)^{dq}，常数方向和常数份枚举仍为(n+1)^{O(dq)}。类型处理的多项式因子可吸收入该界。

显式资格矩阵的读入O(nm)。对每条cut，以精确二进制签名/字典整理连接类型并限制代表签名得到translation；朴素逐cut扫描可用O((n+m)nm)基本资格操作。因为n+m≤m(n+1)，有

\[ (n+m)nm\le m^2n(n+1)\le m^2(n+1)^2. \]

DP总费用O((n+m)(n+1)^{O(dq)})≤O(m(n+1)^{O(dq)})，合并为安全O(m²(n+1)^{O(d2^k)})。dq≥1支付常数指数2；n≥2时n+1≤n²，与论文n^{O(d2^k)}形式一致，n=1仍由n+1安全处理。

空任务峰值0；有任务无机器或有任务无任何资格端时不可行，先行处理。n,m≥1时总图至少两个顶点，分解定义不产生单顶点例外。k=0且仍有任务的无边情况同样由资格检查处理。已有分解的DP/预处理界与未附分解的f(k)(n+m)^3构造费用分列；数值位长按输入编码计费。没有把线性m界作为本轮新结论。

四UM对象v4→v5，全部数学合同保持，只有M-3452046f3bdd47c48b17a0a3038ba4b2的runtime statement准确更新。另三条仅body来源和objections刷新。此前正确的treewidth join、计数+1、x≥0和机器叶资格完全未改。

## 影响与验证

全current registry对象中，以两个body路径/SHA及driver路径/SHA检索，owner并集恰为6；没有遗漏的第7个owner。扫描结果与每个匹配字段保存在manifest。

当前注册边受影响的2条为：

- `um-constant-tw-exact-load-dp-contributes-fptas-join-v4-7c26`：M247→M14，需Root按最新对象/共享body重绑或交原任务复核；该数学关系未在本候选重审。
- `um-controlled-incidence-dp-implies-primal-single-exponential-effd`：M247→M232，同上；本次没有凭复杂度旁段更正去重证该完整transfer。

另有5条未在当前registry.edge_files的draft/历史边：CAG single/three普通价局部边2条、rankwidth LST/ST舍入局部边1条、850a/c739已被后续修复替代的历史FPTAS边2条。逐路径、SHA和endpoint清单在manifest，不对历史边执行重复登记。

任务直接输入命中8项：ca44、d97、UM777(Boss2 read M14)、UM9a(Boss5 core M247/read M14)，以及done的850a/c739/7c26/effd。另4个CAG任务仅在候选/比较/历史文字提及两固定点，没有本轮直接input_pin，不应自动当作6对象变版的必须重做任务。具体JSON位置均保存；未写队列、未发跨Boss指令。

只读overlay调用仓库`registration.validate_batch`通过：6对象、2材料、无外部owner复用；14个去重body/evidence/material引用的实际SHA全部匹配（两body读staging，其余只读clone）。字段断言确认只有M345变statement，6对象truth_status全部保持；两CAG evidence/sources精确保持。

本次准备者直接审读范围是CAG勘误相关正文与driver指定行、保存summary/总账/execution的身份字段，以及UM目标rankwidth段、保全的完整worker review、PDF页17图和页5提取文本。完整候选正文中的其它部分作字节保全，原对象既有审读历史按旧objections保留；不声称本次重审整份源PDF或全部数学证明。

## 各角色审读范围的明确分界

本候选准备者的直接读取范围见上一段；读取原worker的完整review不等于本人重新逐页阅读原PDF。原CAG worker的范围以既有staging的source-erratum.md、input-audit.json和reading-ledger.json为准；本次只复核其中与两段来源更正直接相关的字节、字段和记录，不增补其未记录的阅读。原UM worker的完整rankwidth数学审查以其既有rankwidth-review.md及reading-ledger.json为准；本候选保全并引用该已完成审查，不修改其历史阅读范围。

Root在本次派工明确已经亲看原PDF页17，并在后续消息明确已审两正文diff与六对象delta、接受m²计费和语义。这些是Root在当前任务明确给出的实际范围；本候选不据此推断Root新读了其它PDF页面或重跑了CAG数学driver。
