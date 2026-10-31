---
id: ten-customer-adjacent-wallet-original-audit-and-scope
kind: computation
type_tag: 计算
title: 十客户相邻钱包的原审计与失败层级
status: original-self-contained-audit-replayed-once-exactly
summary: 原标准库程序内置十单位客户及完整三人策略，一次复跑核21有序历史84含自身IC、全部64比较元组和四种最优多重集指派，输出5868B同冻结；后修正与独立审计范围分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/exchange/audit_compact_adjacent_counterexample.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/exchange/compact_adjacent_counterexample_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/exchange/compact_adjacent_wallet_counterexample.md
---

本资源核验[十客户相邻钱包反例](../反例/十客户重复实际行的相邻钱包失败--反例.md)，并与[静态松弛吸收](../引理/静态覆盖松弛吸收末对钱包的直接缺额式--引理.md)区分。实际构造严格满足原单位客户共同目录与完整有序历史纯SPE；被否定的是精确辅助钱包断言，原half未被否定。

## 无外部输入的原入口

4722B原 `audit_compact_adjacent_counterexample.py` 只使用标准库 `Fraction`、`product`、`permutations`、`json`、`Path`。所有输入都是源码常量：三名玩家，标签顺序 $(C,A,B,D)$，六个核心单位客户偏好\{C,A,B\}、一个只喜A、一个喜B/D、两个只喜D；`SECOND=(C,A,B,A)`，16格 `LAST` 如反例完整表。没有外部JSON运行依赖，没有导入发现代码、规范模型、SPE求解器或优化器。

`action(h)` 定义根、四个第二节点和16个末节点；`finish(h)` 从任意给定有序前缀按同一原表完成。`utility(z,i)` 直接对每个显式单位客户找全部最终覆盖者，按人数均分。对长度0、1、2的每个历史和每个合法动作（含自身），程序比较真实当前利润，逐项assert非负，保存全部21行四行动收益和所选动作。反例正文的21行表直接从此原报告完整字段排版，未用摘要替代原节点内容。

随后计算实际叶、全部3×4冻结利润矩阵、行最大值、两条相邻退出钱包及严格ROWMAX差。枚举全部 $4^3=64$ 个有序比较元组求OPT，取其排序去重得到四种最优多重集；对每种全部不同排列算静态Q并取最小。四种共18个最优有序指派，重复主题保留。它不生成新实例/策略、不作无反例扫描，也不使用三人福利定理代替SPE检查。

## 原报告全部字段的数学归属

|字段组|冻结值及解释|
|---|---|
|labels/unit_customers/players|四标签、十个不同单位客户的完整偏好列表、m=3；全部内置原输入|
|actual/actual_profits/W/OPT|(C,C,D)、(3,3,3)、9、10|
|full_ordered_decision_histories/all_true_IC_including_self/minimum_IC_slack|21、84、0|
|frozen_payoff_matrix|前两行(3,4,7/2,3/2)，末行(2,3,3,3)|
|frozen_row_maxima/sum_static_row_regrets|(4,4,3)、2|
|adjacent_wallets/total_adjacent_wallet/strict_candidate_violation|(0,1)、1、1|
|optimal_assignments|四多重集的最佳成本15/2、17/2、8、6；完整指派见反例表|
|complete_strategy_true_payoffs|21个完整历史、规定动作、四行动真实收益向量，全部进反例正文|

报告 `status=exact_counterexample_to_strong_adjacent_rowmax_only` 是原入口主要assert的身份，不表示它的完整矩阵不能推出另外两条原稿已说明的强断言失败：共同query A给总11、坏最优指派(A,A,D)也给11。两条失败由精确矩阵与覆盖见证直接得出；作者代码没有另外单立这两个assert，不能把“源报告没有专字段”误当未获数学证据。

原 `general_half: OPEN` 是历史总体状态，当前五人已另证；`weak_optimal_assignment_adjacent_budget: not_refuted` 准确指本十客户见证，不是当前全人数存在性桥仍开放。原JSON逐字节保留；原稿首段后修正与root一般族已说明m≥7存在性失败。本批未把这种状态更新写回冻结JSON，也不据m7族否定六人或原half。

## 当前唯一新增原审计执行

2026-10-31先检查新stage不存在，之后仅在新原路径树放入原码，执行该main一次。Python3.12.14，exit0、0.047476768493652344秒、stderr空，源码SHA前后不变。新5868B JSON与冻结报告逐字节相同，SHA-256为
`4249c114f4ae5abb8994bc604a5834610e70829100a5dd139d7a0b778e51afe3`。
[执行记录](../../tools/evidence/direct-surplus-compact-wallet-primary/replay/execution.json)、原样stdout/stderr、新JSON和原码树与 `original/` 冻结源分开保存。[运行输入清单](../../tools/evidence/direct-surplus-compact-wallet-primary/runtime-input-manifest.json)明确外部输入数为零并列内置客户/动作常量。

这次复现没有运行独立tree或root程序，也没有运行后续一般族审计；同作者原实现重放不是新增盲实现。当前原程序的84比较包含21自身行，与旧独立实现的63非自身行一致。

## 独立实现与后续数学的实际比较

本批全文读了tree的3778B审查、3492B独立代码与3075B输出：其输入来自作者明确客户/策略/结论陈述，代码另写且无作者/模型/求解器导入，历史结果为21节点、63非自身IC、最小松弛零，重算全部三层真实收益、冻结矩阵、C_adj、OPT。其输出 `weaker_optimal_assignment_tested: false` 保留：审查指出一个好的D,D,A指派，并没有运行全部弱式优化。

另全文读root的2520B字面程序和832B输出：无作者导入，历史核21节点、84含自身IC、主题确实两两不同，明确assert坏最优Q11、全64元组中最优minQ6、J_base7/2。该程序使用排他写入模式保存旧输出；本批未执行，不凭已有JSON虚构新run或新独立先验。

tree的direct审查（本批3418B主源）与tree的compact独立审查是不同文件。前者已知作者精确逐客户公式而未先读证明，重构ABSORB和DIRECT符号；后者只见明确构造陈述，手算并独立实现全部节点。认可的数学范围、先验和执行历史分别说明，不合并为未知命题全盲审、外审或最小性认证。

后续root全人数族全文比较得 $C_{\rm adj}=1,\min Q-W=(m-4)/2$，故全人数存在性/任意固定倍数相邻钱包桥都失败，但本族half成立；本批不额外done它。相反，direct的静态吸收等式无需另领调和HW资金，仍需实际EARLY上界。两个旧suffix势稿只解释删除势差/联合遗憾未付，不把固定点或终端已消去当早期已付。

必要运行没有缺失来源，全部主源及比较源用本地冻结字节核两commit；没有重试先前非必要远端扫描或认证。原代码、完整报告、后修正及当前模型/状态比较见[证据目录](../../tools/evidence/direct-surplus-compact-wallet-primary/README.md)。
