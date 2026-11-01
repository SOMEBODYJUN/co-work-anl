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
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/tree/audit_compact_strongA.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/tree/compact_strongA_independent.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/parent/audit_compact_adjacent_literal.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/parent/compact_adjacent_root_literal_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/compact_exchange_independent_review.json
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


## 原五源主清洗补充：精确字节与执行端点

本节在原4722作者一次成功事件之后补读/绑定五个主源，不改变上方已自足的十客户数学、原5868冻结报告或任何旧执行记录。当前3492/3075/2520/832/670共10589B全部正常show核size/SHA/blob后全文读；其中tree码/报告和root码/报告这四件，与先前comparison-only原件逐字节同SHA。此前“已读相关”没有被误当“已经正式处置本五源”，也没有变成这两独立程序的新run。

两原实现都**没有main guard**，其核验和写报告均在顶层；导入同样执行全部数学。tree3492最后直接write_text到同目录compact_strongA_independent.json，会覆盖已有文件；root2520在全部收益/IC/OPT/匹配计算和assert之后，才以open('x')写compact_adjacent_root_literal_audit.json。后者排他写保护文件，**不会**阻止此前数学执行；不能把“输出已存在会拒写”误作安全导入。当前只AST/文义读码，没import、CLI、调用函数或开关断言模式运行。两码的数学认证依assert，禁用断言时没有相同核验合同。

运行输入都为源码内置十个不同单位客户及根/second/terminal的21节点完整动作；零外部JSON、零项目模块或求解器依赖，只有标准库Fraction/product/Path/json。程序按每个原有序h的真后继finish(h+a)比较当前利润，不按计数合并h。尤其(A,B)后选B、(B,A)后选A的平局分别保；提供的四元收益向量给全ties，不能把max数值误作唯一最佳主题或替换另一张统一平局策略。这里是这一个具体合法输入，未把两码授为任意共同目录/全模型解析器或搜例工具。

|原实现|实际核验、字段与未测部分|
|---|---|
|tree3492|从21条字面policy遍历每h三个非规定动作，63个真实非自身IC；assert节点数/非负min/actual/u、M、两C、W/OPT及StrongA差。OPT枚全部64有序三元组。3075报告同时保存根4格、第二层4×4格、末层4×4×4格，共84个真实强制收益数；含自身**数据**不把其63个assert比较改记84。冻结矩阵3×4和全部客户/动作常量明列；weaker_optimal_assignment_tested=false准确，因为代码没有遍历最优指派成本。|
|root2520|按depth0/1/2全h和四动作assert84个含自身IC，并显式assert四主题覆盖两两不同；重算同矩阵/C_adj1/J_base7/2，assert坏最优(A,A,D)价11。枚64有序tuple求OPT并对全部最优tuple求minQ6，显式达到者(D,D,A)。原832不存全部84收益/63非self单表，不能把tree的完整字段借成root输出。|

当前将tree全部21×4真实收益字段按层形状展开，与原作者5868完整21表逐字段同值；客户列表、动作表、actual、利润、冻结矩阵、各预算与gap也作JSON值比较。这只是既有输出和内置输入的值/排版对应，不是新SPE或镜像收益实现。原作者4722实际一次exit0/new5868同字节仍只属于原作者入口；3492和2520本批都0执行，不借共同结果制造第二/第三个原生成功。

## credible侧670B独审记录的准确身份

此独立记录scope为“从 supplied exact strategy 直接重构exchange10 compact”，是作者明确构造之后的内部结果陈述；代码无作者导入之类的独立实现事实，只能对实际已读的3492/2520说，不能因这句scope便给670补一份未见程序或心理先验。五源没有它的生产者码、输入/代码SHA、argv、环境、stdout/stderr或exit记录；它也不是本次执行产物。

其所有字段实读：m3、unit_customers10、histories21、nonself_IC63、minimum_IC="0"、actual=(0,0,3)、W9、OPT10、profits=(3,3,3)、frozen_rows为前两行(3,4,7/2,3/2)/末行(2,3,3,3)、Q="11"、Csum="1"、StrongA_gap="1"、best_optimal_assignment=(3,3,1)、best_optimal_Q="6"、weak_gap="-4"。这里索引0/1/2/3对应(C,A,B,D)，所以good指派正是(D,D,A)，弱差6−9−1=−4；min/Q字段的“最佳”是原记录声明，原root全64枚举及原作者四多重集最小表另给独立数学支撑。

它的63非自身计数与tree相同，但tree3075明确weaker_optimal_assignment_tested=false且不输出best/minQ，不能将670误认tree写出的报告；root832使用84含自身且schema不同，也不把它当该程序原生输出。三个结果数值相容，各自输入先验/实现/执行字段的缺口仍保，不将同一份点上结果数凑成三次盲审、外审或新颖性。

ROWMAX、COMMON-ALL和OPT-ALL的严格失败、存在版本例min6可逃以及后继m≥7反族，均已由上方完整矩阵/覆盖/全指派论证及正式反例页承担，本五源不另授一个新十客户反例。670无新数学命题，但有独立内部记录的来源身份；两个旧报告的完整数学与数据早已吸收，按重复内容处置仍保全原字节。两实施代码则保留其顶层/写端点合同和具体检查差异。

原件、五逐源处置和两码0运行范围见[本五源证据](../../tools/evidence/compact-strongA-original-audit-five-primary/README.md)。本批15XD实际claim pushedaaa6b5e5ca5bd4ab2f4e2ec30473b4fd5bea8f5f，raw needs-attention原样；独立38untracked/2tracked同字节、无missing/different/unmerged、stash保留与原回执并列，不伪synced。稳定页仅本次窄追加，旧before快照及原作者一次事件保全，Root按expected_beforeSHA串行guard复制后checkpoint/done，本线程0共享R写入或Git操作。
