# Normalized gated-menu welfare 代码的实际独立审计

2026-10-18。实读完整初版源码及新版末尾增量，独立执行、重构验证当前源码。没有修改研究仓库或 Git。当前审计结论：没有发现所述有限审计合同的 fatal；可保留当前准确范围。

目标：`co-work-anl-boss11-negative/tests/audits/unrelated_machines/normalized_gated_menu_welfare.py`。

- 最初实读版本 SHA256：`11dca801e3ae81aa45042c883a55dedb1bf729fc03152fad75a2575bf0b9084d`。
- 当前实际运行、独立复核且前后重算相同的 SHA256：`31aeb2b57bbf78e0f980f552bd5985e4f0a15b57f98f93f46be1296a19b156f6`。
- 两份本地执行输出 `independent_replay.json`、`independent_replay_v2.json` 都是新版。首次进程实际启动已晚于源码替换；没有声称本人的初次输出是旧版本，也没有把新增覆盖倒填到旧运行。

## 数值提案与精确认证

SciPy/HiGHS 仅产生原始 primal、inequality dual 和 equality dual 提案。它们经 `Fraction(...).limit_denominator(10**8)` 转成候选有理数之后，代码逐式检查非负 primal、全部精确行、ub dual 非正、全部精确 reduced costs 非负，以及 primal/dual 目标精确相等。因此成功返回的 finite LP 最优性是有理证书证明，既不依赖 `result.success` 的数值容差，也不把 float objective 当最优值。

本审者另不使用原矩阵认证过程，直接将序列化 dual 转成 welfare prices：链接价 a>=0、资源价 b>=0、组价 eta；检查每个正 incidence 的 a+b_u>=p，以及每 state 的 eta_g>=sum_u a_gsu。精确 dual value 为 sum b+sum eta，并与精确可行 primal 的福利相等。72 个 general certificates 与 3 个 coin fixtures 的最优值 certificates 全部通过；后者的 supplied nonbasic 点另核可行与目标相同，所以不能误说 certificate 的 basic primal 就是 supplied nonbasic 点。

分母上限的 rationalization 可能拒绝其他合法输入；没有 fallback、任意输入成功保证或一般精确 LP 后端。两例 2^200+1 分母 fixtures 使用给定的精确最优点，完全绕开浮点提案。n=1 由归一化给 LP 上界一；两组同一 unit resource 由该资源列给上界一，故这些点确实最优，不是仅证可行。

## State/coin 条件平均与完整输出

原 `expected_max_sum` 的按高度积分公式正确：对每资源，以阈值层差乘“至少一组提出不低于该层的 offer”的概率。组间独立；同一组的 state 相关性已由其分布合并，未要求不同资源之间独立。先定 state 时只选择正 z，故后续 x/z 不会除零。coin 阶段在全部 state 固定后执行。每步状态平均和 coin 平均均有精确相等断言；比较与 tie breaking 也都是 Fraction。

另用完全枚举 state/coin outcomes 的期望函数替换原高度积分公式，重新驱动 36 support、72 general、3 nonbasic、2 大分母 fixtures 的原 rounding 主体。113 个实例、904 次独立期望评估的全部条件平均和非降断言通过，最终福利与运行记录相同。这不是只用原 `distribution` 自检。

实际 bundle 逐资源仅给最高正 offer 的一组，因而不交。最终允许改用该 bundle 的 attaining state，其值只能增。所有 selector、connector、全部 indexed-state incidence（包括 unselected states 与显式零 jobs）均保留。另逐件重算 113 个实例的 private/root/resource loads 和总 jobs；与源码 schedule 的完整检查及记录 peak 一致。

门控的初始 makespan=2 可直接由全组 inactive 的实际调度达到，所以 `brute_gate_opt` 初始 best=2 是合法 incumbent。非负处理时间保证 partial peak>=incumbent 时剪枝不会丢改善解；它不是宣称访问了每一份完整调度。

## 实际资源与普通任务枚举

独立代码只复用 deterministic input generators 来恢复相同输入流；没有复用目标文件的 `build_gate`、`brute_gate_opt`、`exhaustive_values`、`actual_values` 或 `balanced` 来证明以下最优性。

重新建立普通任务的全部资格，逐项访问十二个小实例的**全部合法完整调度**，无剪枝。合法调度数依次为

    8, 64, 16, 256, 24, 576, 96, 9216, 8, 64, 16, 256

合计 10,600 份。独立对资源所有者分配枚举并逐组取最大 state 值、枚举 top-k 平衡量；十二例均得相同 beta_opt，真实普通 UM 最优值逐例等于 2-beta_opt，且与原搜索结果一致。

这仍是明确十二个小输入的精确核验，不是一般 UM solver 或一般归约定理的计算证明。

## 负控修正及新边界 fixtures

旧版负控的 flat_opt=2、gated_opt=3/2 只是写入报告的常量，没有在该段执行计算；因此旧版该字段不能算自动负控证据。

新版确实枚举 flat 的四份原任务调度，另调用真正 gated 搜索并断言 2 与 3/2。本审者再独立无剪枝枚举 flat 的全部4份与 gated 的全部64份合法调度，分别精确得到 2 与 3/2。门控确实改变原 flat 问题，不能把 gated 保证宣称成原 flat 保证。

新增两大分母 fixtures 实际通过归一化、给定 LP 可行/最优点、Fraction 条件舍入、bundle 值、全部原 jobs 的 loads 及独立资源最优枚举。第一例包含两件零 incidence、n=1 和两 state；第二例两组在同一资源上的 coins 为 tiny 与 1-tiny，真正执行两次非平凡 coin 决策。它们没有挤进旧 summary 的三 coin fixtures/20 次 coin 决策口径。

## 运行、拒覆盖与准确结论

新版实际 main 输出维持：36 support；72 exact-certified general，其中2例含分数 state、0例含非平凡 incidence coin；3 deliberate optimal nonbasic fixtures 共20次非平凡 coin 决策；12个普通 UM 小例。max_observed_ratio=153/130。大分母两例另列。

以同一已存在的 output 路径再次调用新版 CLI，实际 exit=2，stderr 明确拒覆盖，文件 SHA256 前后不变，为 `2b40b0bc6e3b11a3bf1a3b6f678873873d0a12ec6d29e404cbfd8f41b30ebe86`。写入本身另用 exclusive open('x')，因此入口检查之后的竞争也不会覆盖既有文件。

独立附加检查位于 `independent_extra_checks.py`；精确结果为 `extra_checks_result.json`。它们仅是本次代码实审的 scratch 证据，不建立新的研究 Claim。一般常数分析、所有输入 bit-polynomial algorithm 与 source hardness 均不由这些有限程序认证。未发现阻止当前限定资产保存的代码异议。
