---
id: retired-topic-selection/cross-field-battle-candidate-registry
kind: resource
type_tag: 资料
title: 跨域工具迁移候选注册表与处置边界
status: candidate-index-integrated-by-model; no-universal-result
truth_status: structured-candidate-map-only; finite-toy-boundaries-retained
review_level: full-source-read-cross-archive-comparison
summary: "完整读取跨域工具迁移候选注册表 candidates.json（6847 bytes）；保留 CB01–CB07 的精确模型、量词、首个证明义务、致命风险、玩具状态、母文献位置和 web_ref。各数学切口分别映射既有 BMKP、fair-goods、fair-chores、local-potential-games 或 atomic-games 对象；注册表本身的机器可读字段是独有来源。未把 OPEN、有限穷举或候选报告升级为定理或新颖性认证。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/cross_field_battle/candidates.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/cross_field_battle/candidates.json"
source_ids:
  - 7bc9c5f4dfe9e519fa51
source_blob: de1b84c58b2c6785465e9d1d80044c2547b1b787
source_sha256: cd49947436ec90cbe2d53fbbde4c89b4a886bb09977a5352fc397c77d4376c15
source_size: 6847
source_commits:
  - 68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup)
  - aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)
recommended_evidence_path: archives/retired-topic-selection/tools/evidence/cross-field-battle-20261031/candidates.json
---

# 来源身份与读取边界

冻结源为 `history/retired_topic_selection/independent_review/research/topic_selection/cross_field_battle/candidates.json`，源 ID `7bc9c5f4dfe9e519fa51`，blob `de1b84c58b2c6785465e9d1d80044c2547b1b787`，SHA-256 `cd49947436ec90cbe2d53fbbde4c89b4a886bb09977a5352fc397c77d4376c15`，大小 6847 bytes。源内容经 `work.py clean show` 导出后由 JSON 解析器完整读取；字段包括：

- `date=2026-10-20`、`task=cross_field_battle`；
- `guidance_fully_read=true`；
- `configuration_note` 明确说明继承父配置、没有独立的 model-identification 覆盖；
- 七条 `candidates` 记录，每条均有 `id/title/depth/status/paper_type/precise_model/mother_url/original_position/web_ref/our_idea/first_proof_obligation/fatal_risk/toy_and_evidence/novelty_certified`。

这是一个跨子线的选题索引，不是七个证明文件，也不是外部文献的逐字副本。`mother_url`、`original_position` 和 `web_ref` 是来源内的文献定位线索；本次清洗没有把它们当成独立的文献复核或新颖性证明。

# 七个候选的精确内容与当前映射

| ID | 源中精确模型/目标 | 源中状态与首义务 | 全仓比较、建议去向 |
|---|---|---|---|
| **CB01** | 两种硬容量：`m1` 个容量 1、`m2` 个容量 `C≥1`；公共有理 weights/profits；物品至多一次、可 unused；每个固定 ε 求位长多项式 `(2/3−ε)` 近似。 | `OPEN`, `deep`；证明联合 labels 数常数、两容量 rounded feasibility 同时成立，并让 matching 与 cheap LP 共享同一见证。风险是共享 item supply、高利润预处理/short 损失和条件交换不能自动组成总算法；1/2 容量、4–8 项整数枚举尚未完成算法实验。 | 数学内容已进入 `archives/bottleneck-knapsack/state/资料/双容量BMKP候选的三模块与完整目标--资料.md` 与 `state/审查/两容量BMKP候选的独立反方审查与量词边界--审查.md`；有限联合类型审计另见 `archives/fair-allocation/state/审查/两容量联合类型与有限舍入审计--审查.md`。本注册表新增的是 CB01 的机器可读候选索引和 `web_ref`/深度/玩具字段，不新增总算法或保证。候选总算法仍 open，源级建议 `integrated` 到跨域注册表并保留上述对象链接。 |
| **CB02** | `n=3`，每型 `c_g∈{1,2}`，每人每型至多一件，完整 SD-EF1；任意型数。 | `OPEN`, `deep`；要证明三人所有型数的 prefix constraints 交换/增广，或给最小反例。风险是异质多序 discrepancy；一般 partition 负例不能移植到 identical copies。`n=3,t=4` 归一化 9216 个 strict profiles、每 profile 81 个 allocation 全存在，但这是计算而非证明。 | 与 `archives/fair-allocation/state/审查/退役公平商品copies穷举结果--审查.md` 和 `state/审查/退役公平商品有限玩具结果--审查.md` 对齐；候选报告/注册表的有限结果和更大随机样本保持独立。注册表的四字段 scope/状态/母文献定位是独有索引信息；不把 9216 或更大随机样本写成任意类型数定理。候选内容建议 `integrated` 到 fair-goods 既有对象的“候选地图/有限证据”关系。 |
| **CB03** | 四人 additive 非负估值；K8 类大小 `(3,3,2)`，每类 cap1、总 cap2；K12 四类各3、每类 cap1、总 cap3；目标 EF1 且给定 `i<j` 时 `i` 不 envy `j`。 | `OPEN`, `reserve`；先给 K8 完整 chamber 覆盖或 exact infeasibility certificate。风险是值域 32 维、值序不决定 bundle sums、K8 解不足以覆盖全部四人 laminar；864 个可行 allocation，seed 20261020 的值域 `0..20` 随机 1000 profiles 全有解。 | 与 `archives/fair-allocation/state/审查/退役公平商品有限玩具结果--审查.md`、`archives/weighted-congestion/tools/evidence/retired-fair-goods-20261031/candidate_report.md` 和 `candidates.json` 对齐。有限 profile、K8/K12 allocation 数和旧 top-separation 失败边界已在 fair-goods 对象保留；注册表只补机器可读的 reserve/status/URL/obligation 字段。不要把有限样本升级为连续估值 universal theorem。 |
| **CB04** | 无 loops 的 rank-2 matroid chores，成本 `min(2,触达平行类数)`；先每人三平行类；目标完整 EFX。 | `OPEN_WITH_LOCAL_LEMMA`, `high`；在三平行类中找 Hall 替代或最小反例；一般 rank-2 没有证明。风险是二元补词不保 owner-pure，且 loops 不能遗漏；三人 3–8 项全部 12825 word multisets 构造 EF witness 并逐对核验成功。 | 与 `archives/fair-allocation/state/审查/退役公平家务有限证据三源处置--审查.md`、`state/审查/公平家务生成器三源审查--审查.md` 和 `archives/weighted-congestion/tools/evidence/retired-fair-chores-20261031/candidate_report.md`/`rank2_two_classes_lemma.md` 对齐。二平行类局部引理和 12825 有限回归已独立归档；CB04 仍只支持工具苗头，不能扩成一般 rank-2 EFX。 |
| **CB05** | 任意长度 ladder graphic matroid、任意边序，`x` 在 spanning-tree base polytope、`w≥0`；所有 prefix weighted discrepancy `≤C max w`，`C` 与图长无关。 | `OPEN`, `reserve`；证明不随路径分解高度累积的 weighted prefix invariant。风险是任意边序抹掉图优势，且 `2610.16079` block-TU 近邻需排重；3–5 格 ladder Fraction toy 只建议、尚未执行。 | 当前全仓没有同一 ladder graphic candidate 的正式对象；保留为独立 reserve candidate，建议新证据目录仅复制该注册表行并链接母文献线索。不能用固定 rank/corank 的平凡总权界或 cactus/partition 特例冒充 ladder 结果。 |
| **CB06** | 两人二元 identical-interest game；bounded multilinear potential；无偏、方差有界 utility-vector 全信息估计；标准 simultaneous clipped RM+。 | `OPEN`, `reserve`；在二元协调中证明 stochastic drift 或构造反例。风险是 generic SGD 换符号无价值，且 `2608.17417` 撤稿 claim 只能保留为背景、不可作定理依赖；二元 ±noise 的 regret/势/last-gap toy 尚未执行。 | 与 `archives/local-potential-games/state/资料/Nash候选报告与近期排雷边界--资料.md` 的 NASH-02 有模型近邻，但 CB06 的“同时 clipped RM+、两人二元 identical-interest、全信息无偏有界方差”应作为独立限制版本；不能把同时/交替、确定/随机或 expected gap/high-probability 量词混写。当前无正面定理，建议 `retained` candidate map。 |
| **CB07** | 非加权 atomic congestion；每策略资源数 `≤2`、显式策略表；nonnegative monotone latencies；先二元策略 affine。目标是 PNE 局部优化边界。 | `OPEN`, `reserve`；精确表征可表示 `Q,h` 并排查既有低度局部优化。风险是不能嵌任意 PSD QUBO，可能撞长期 degree-4 边界；2–5 人、size2 整数 affine flipgraph toy 尚未执行。 | 与 `archives/weighted-congestion/tools/evidence/atomic-games/candidate_report.md` 的 AG-01 高度近邻；后者已说明 size-2 全局势最小化 NP-hard 不等于 PNE 搜索困难。CB07 的资源数 `≤2`、显式策略和 affine-first 量词保留为精确别名/受限版本，建议 `retained`/near-duplicate，不能把全局势硬度移植成 PLS-hard。 |

# 注册表独有内容与重复边界

与已归档的单模型候选页相比，本源独有的是一张可机器读取的统一索引：七个 CB ID 的 `depth/status/paper_type`，每条母文献 URL/原文位置/搜索 ref，具体 `precise_model` 字符串，`our_idea`，首个承重义务，`fatal_risk`，玩具状态以及统一的 `novelty_certified=false`。它还记录 `guidance_fully_read=true` 和“继承父配置、没有独立模型识别字段”的配置边界。

`cross_report`（同目录的 `candidate_report.md`）是另一冻结源（源 ID `17d0fbd6edf5d1477682`），包含更长的逐候选解释。两源不可互相替代：本 JSON 是结构化索引；报告是语义展开。若后续整合两者，应保留本 JSON 原字节和 SHA，并在报告中引用本注册表，不把同一候选重复算作两条数学对象。

与现有对象的关系是“候选地图/有限证据/近邻映射”，不是“候选→定理”。第三阶段可建立带解释的 `来源/候选/有限验证/迁移` 边：

- CB01 → 双容量 BMKP 三模块资料：候选目标与条件模块一致，但总算法仍未闭合；
- CB02/CB03 → fair-goods 的 copies/K8/K12 有限审查：有限支持或障碍，不足以支撑一般量词；
- CB04 → fair-chores rank-2 二类局部引理：局部工具支持三类开放边界；
- CB05 → graphic-matroid prefix discrepancy 预候选：当前没有有限执行结果；
- CB06 → NASH-02 噪声/同时 RM+ 近邻：需保持 clipping 与随机量词；
- CB07 → AG-01 size-2 congestion 复杂度候选：全局势与 PNE 搜索保持分离。

不得建立以下无证边：有限玩具→普遍存在/算法；母文献选题位置→新颖性；跨模型（fair-goods、fair-chores、local-potential-games、atomic congestion）直接迁移结论；一个候选报告→已解决。

# 处置建议与接续

建议源级 disposition 为 `integrated`：把原 JSON 复制到 `archives/retired-topic-selection/tools/evidence/cross-field-battle-20261031/candidates.json`（或由 Boss 选择保持在对应模型的 evidence 目录），并以本文作为结构化注册表的自足资料对象。四个已有对象（CB01–CB04）只需补 source_refs/registry 交叉链接；CB05–CB07 保持候选地图/近邻边界，不强建新定理。

可提交的语义回执应说明：

1. 用 `clean show` 完整导出并读取 JSON，核验 6847 bytes、SHA-256、JSON 合法性和七条记录；
2. 对照全仓相关对象，说明每条 CB 记录的独有字段去向和模型边界；
3. 保留 `novelty_certified=false`、OPEN/OPEN_WITH_LOCAL_LEMMA、未执行 toy 状态和完整量词；
4. 注册表正文与必要证据先 checkpoint pushed，再以源 ID `7bc9c5f4dfe9e519fa51` 提交 `integrated`，不把 JSON 的存在或“全候选已读”写成数学结论。

本草稿没有 Git 提交、外部消息或 clean done；它等待 Boss 审阅并在统一 checkpoint 中与其他五源成果一起推送。
