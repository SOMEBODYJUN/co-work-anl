# 有限组交互加权菜单：canonical 实际全文读后

审查对象 ID：`UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`。

实际读后日期：2026-10-18。本记录是在此前 Exact-only 独立推导、作者 Proof_v2 实际全文读后均冻结之后，首次实际通读下列 root canonical 所得。旧记录和 repo 均不修改。

## 实际读取的固定版本

路径：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md`

实际读取字节数：`10,422`。

实际核对 SHA256：

`d305cf8e2dd5c70dc30e7811c3ed71787eba179d30171bfdeb794468a25e56d1`

本结论仅认证该实际读取版本，不预先认证未来改写版本、未来 embedding 文件或其它导航文件。

## 结论

**PASS；没有发现数学 fatal。** canonical 完整落地了此前独立推导及作者 Proof_v2 的准确输入域、两分支证明、归一化和实际原任务调度。它未把失败分支的 relative guarantee 改写为所有输入的 absolute guarantee，也未把该结构类结果提升为一般 UM 算法或困难性定理。

root 明示后续另建的 `degree_three_weighted_menu_cube_embedding.md` 为 pending 导航。此项不影响本文自足的算法定理和证明，不按数学 fatal 处理；本记录也不因此认证那个尚待建立的 embedding 结论。

## 完整落地逐项核对

| 项目 | canonical 实际落地位置与核对结果 |
|---|---|
| 完整原 ordinary-UM 域 | §1 列明全部 selector、全部 indexed-state incidence jobs、仅有的两类机器/有限时间；所有其它时间为 infinity，无额外任务、预载、拒绝或 side constraints。结构标签明示为输入的一部分，未免费分解一般 UM。 |
| state 内资源无重 | §1 明写每个 `S_gs` 是资源集合且标识互异；不同 indexed states 可以重复，同组多个 states 可以复用同一资源。§5 的右度 Hall 计数正确使用该限制。§6 保留了非单射反例，但没有声称它否定扩大域中的所有比 1 算法。 |
| 全部菜单交互参数 | §1 的 `U_g=union_s S_gs` 包括全部 states 和零 private 权 incidence。M 是完整交互图上界，Delta 是跨组资源度上界，均不是某个未知选态的局部度。 |
| 空 state、零权和未选 states | §1 允许；§2 为每个 deficient indexed state 加 bonus；§6 明确保留所有 states 的其它 jobs，零时间 job 仍是真实原 job。未选 state 不被删掉或免费释放。 |
| 精确保 OPT 的归一化 | §2 同时给出删除 bonus 的投影以及向每个 indexed state 的独占资源导出 bonus 的反向扩展。扩展包括未选 states，利用原 schedule 峰至少 1，得到精确 optimum equality。 |
| heavy failure | §3 对任意峰小于 `1+beta` 的真实调度，从 selector 实际选中的 state 强制一个 heavy export；资源时间 1 及峰严格小于 2 给覆盖 H 的 matching。失败据此获得真实 OPT 下界，而非未知 witness 假设。 |
| failure 的 relative guarantee | §1 与 §3 均明确：失败输出全 private 峰至多 2，结合 `OPT>=1+beta` 得 `2/(1+beta)<=2-beta`；不主张此分支实际峰总小于等于 `2-beta`。 |
| heavy success 的 M beta 损失 | §4 按每个 heavy group 只预留一个资源、完整菜单交互图至多 M 个邻组逐项收费。零权项不改变质量下界，无虚设“任意 heavy 选择保住 diffuse LP”。 |
| 单个共同 full-slot matching | §5 每个 full slot 有 Delta 个互异原资源邻点，资源至多属于 Delta 个组、每组只属一个块，因此 Hall 一次覆盖全部完整 slots。没有分别匹配后再假定互不冲突。 |
| 精确尾项计账 | §5 的式(6)正确。计账用区间从 `t Delta` 起，真实匹配块则从 `(t-1)Delta+1` 起，正文明确区分。最后计账区间不要求完整。 |
| 完整实际输出 | §6 为每个 selector 给出所选 private state，为 H/L 的指定 incidence 给出 export，其余所有 states 的全部 incidence 留在原 private 机器；逐台负载和每 job 恰一次均覆盖。§2 最终删除的只有 bonus。 |
| endpoint beta=1 | §6 明确等价于 `Delta=1,M=0`，归一化后 H 空、所有块为单资源，所有所选 incidence 导出，真实 OPT 和返回峰均为 1。 |
| binary 大参数 | §6 不复制 Delta 或 M 数值份对象，只按实际列表长度分块；精确有理运算与参数分母编码长度均多项式。 |
| dense processing matrix 与 schedule 输出 | §6 明给 a、u、g、l 计数以及 bonus 后 dense 矩阵的多项式项数上界，并明确输出全部原 jobs 的 machine identifiers。不是只输出一个分数目标值或局部分配。 |
| cube 的 q 是 union | §7 加粗要求每组完整变量并集至多 q。明确若仅逐 state 至多 q、而所有菜单变量并集增长，不能沿用 `M<=q(d-1)`。 |

## 四个边界的实际再核

1. **空尾与不满尾。** 若 `n=m Delta`，最后计账区间只有 index `m Delta`，仍在“至多 Delta 项”的界内；若余数为 r，则最后区间有 `r+1<=Delta` 项。若 `n<Delta`，没有 full slot，所有 n 项可归前 Delta-1 项。式(6)对空 sampled sum 仍成立；success 中式(7)的正下界排除真实 L 组只有空 sampled sum 的情况。

2. **正权和零权。** 排序可有零权及 ties，区间上界和资源匹配仍适用。一个 zero-private job 的外部时间依然是 1；未 export 时它合法留在 private 0，而没有从任务集消失。度数按资源身份列入零权 incidence，因此不会低估完整交互上界。

3. **大 binary Delta。** 即使 supplied Delta 是极大的宽松有效上界，`floor(n/Delta)` 可直接由二进制整除得到。无 full block 时不构造任何该组 slot。由 `W'>=(2 Delta-1)beta` 与 diffuse 最大单权 beta，这种无 full block 情形不可能是 success 中需获得正质量的 L 组；没有数值规模循环或隐式复制。

4. **dense 输出域。** 归一化每 state 至多一个 bonus，故新增机器/job 各至多 a。完整 dense 矩阵上界 `(a+u+a)(g+l+a)` 是计数上的真实多项式，不依赖 beta 分母的数值。最终返回原 jobs 的单机器标识，未返回 bonus 或丢失未选 state jobs。

## 一个措辞澄清建议，不列为 standing fatal

§3 的“原资源”、§5 的“原resource”应按 §2 所作“在 N(P) 上运行下述算法；以下先设所有 W=1”的约定，解释为**当前归一化实例中的真实资源，包含新加的 bonus resources**。在该正确解释下，证明与源 Exact/Proof 一致。

若误解释为 heavy graph 或 slot graph 只能使用原 P、不得使用 bonus resources，则结论不成立：例如原空 state 在归一化后可能以 bonus 形成唯一 heavy edge，不能删掉该边。因此可在最终文本中加一句“以下所有 state/resource 均指当前归一化实例，包含 bonus”，以避免读者误读。现有 §2 已建立该工作实例转换，故此建议是文字澄清，不是对当前数学论证的 fatal objection，也不要求改变 theorem 的输入域或常数。

## 状态边界

本次审查认证了固定 hash canonical 的完整数学重构与先前独立/作者证明结论一致。有限算术核验仅为辅助；没有新增实现或运行性能认证，没有外审、新颖性、因子锐性认证，也没有把后文 pending embedding 当成定理依赖。未改 repo、Git、Work 或此前冻结文件。
