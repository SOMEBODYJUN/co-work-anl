# 终局冻结钱包与最优fresh自留预算的原件及执行证据

本目录支持四份自足对象：[末对钱包](../../../state/引理/实际末对冻结查询的选择性钱包--引理.md)、[开放自留预算](../../../state/想法/最优覆盖查询的自留份额预算--想法.md)、[笛卡尔缺陷和根修复](../../../state/引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md)、[原程序完整策略复跑](../../../state/计算/终局冻结钱包原程序及完整策略复跑--计算.md)。

## 五个正式主源与三个运行依赖

正式认领已由 Boss4 确认 pushed `b6c14c398ab92125a2a9e07e41c6f6f374f3541e`、synced。本批只写 external 独立 staging，未做 Git 写、claim 或 done。五个主源合计 30,133 字节，均在正式确认后重新完整读取、核 inventory SHA，并从两个冻结提交逐字节核对相同。完整路径、blob、大小、SHA 与双定位见 [source-manifest.json](source-manifest.json)。

|ID|原源文件|字节|处置|
|---|---|---:|---|
|30449824f9a39ec251e2|round8/matching/terminal_frozen_regret_wallet.md|7443|全部三真实IC、选择性钱包、利润锚定和EARLY开放接口进自足引理|
|3beb17d5735520b90e84|round8/matching/audit_terminal_wallet.py|7269|精确原源码及全部输入保全，本批一次隔离主入口|
|53c66ec7d069d0a166ab|round8/matching/terminal_wallet_exact_audit.json|7401|冻结报告原字节保全，两例全部12行语义进计算页|
|86f3b77f8de039cb76be|round8/matching/README.md|1124|三入口合同与剩余义务合并进引理/计算页，无导航代读|
|9da7c5510bd045b3d059|round11/geometry/optimal_fresh_self_reserve_working.md|6896|完整S?、静态式、去重、有限范围及Cartesian/修复进想法与引理|

主源都来自 `R-cd789330fc7141299ac491bbb3ffa420/`。`original/` 下保留原始仓库相对路径与原字节。三个运行依赖 ID `a7579960b289fff40c97`、`ff1a437e39e730d230eb`、`be317a14860bf5650dfe` 合计 39,475 字节：旧52的完整实例/动作 JSON，1953的实例与完整动作 JSON。依赖曾逐字段和全部动作表全文读，本批核同SHA并由真实入口实际读取。它们只标 runtime-dependency-only，不重复登记完成。

## 一次真实主入口与历史区别

`replay-tree/` 中保持原相对路径，只有原主程序及三个输入和它生成的报告。原 `ROOT=parents[6]` 不改，环境只禁写 pyc。真实执行次数一、exit0、约0.833秒、stderr空；所有代码/输入SHA执行前后相同。[执行记录](replay/execution.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[本次输出](replay/terminal_wallet_exact_audit.json)与原冻结报告分开保存。本次输出SHA `8ee168a14bf717e5e39a33b9048dbc97122a7394dfc67a7c55d91b2f3724fd7c`，逐字节等原7401B报告。[运行依赖清单](runtime-input-manifest.json)记录实际放入树的四个代码/输入文件。

本入口确实展开单位客户，核完整有序历史键集/合法动作、302个决策历史、1812个含自身IC及12条末对查询。它不计算OPT或min Q，不生成均衡。上批跨角色程序只是import该模块并调用load_*，未执行audit/main；本次新增完整执行不回填上批历史，也不冒称独立实现或盲审。两例利润失衡均零，非零失衡项一般正确性来自解析证明。

`cleanup/workspaces/Boss4/r3-terminal-wallet-fresh-reserve/run_original_once.py` 是本次实际运行器；不要为包结构核查再次运行它。该工作区的 `check_package.py` 只读冻结字节、核链接/receipt/已经存在的执行记录，不运行数学原程序。[结构核查](verification.json)与人的数学自查分别保留。

## 全文比较及后续状态

另保全十份 comparison-only 原件：round9调和末对钱包；旧调和弱匹配主稿及独立review；credible11前缀核去重；m块padded保险修复；13人36客户算术；fresh精确审计代码和16行报告；65目标浮点报告；旧13人安全最优query攻击状态。它们均全文比较，但不额外done。本批没有运行fresh审计、LP攻击、padded保险或旧13人程序。

现行全文对象核了共同目录模型、末两人安全查询税、循环污染调和付款、回复循环静态运输、两主题根修复、Cartesian银行族、强静态指派失败及两个证书资源、跨角色门与positive-loss停界。五人定理/六人问题仅核模型与状态段，未重审其全证书。全仓state及原round9–14按钱包、fresh候选、K0与强/弱Q检索后续，不把旧README多数意见当证明。

三个需保留的纠正或证据边界：

1. fresh主源的“十三客户”实指13名提供者和36个客户；其 $37/66$ 余量反驳任意重复单query加强，不反驳min费用覆盖最优元组。
2. 原稿“最优 $K_0\le W$ 已失败”未给定位；本批未核到该min-fresh强桥的有效完整证书，不用强冻结 $Q$ 反例冒充。原尾注弱聚合 $\theta_m$ 路线停止亦只保历史身份，不擅改成真正minimax的新断言。
3. fresh审计代码用整个目录最便宜主题补齐m槽，保重复元组；浮点四锥共65目标、57可行，不是精确dual或全策略证明。

正确静态关系、正平方、零损失门、局部钱包和编译器均不填早期冻结税或S?一般付款缺口。当前五人half另证、六人仍开放；本批不作升级、外审或新颖性认证。
