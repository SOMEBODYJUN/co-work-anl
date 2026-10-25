# 优先权表示、未曝光随机化与可支付的整行上包络

2026-10-25，round7/fresh。研究对象保持任意 m、任意有限共同目录、所有完整历史纯 SPE。一般 Q-CAG-HALF 仍 OPEN。本文没有新的无条件福利界或目标反例；没有复算 round6 随机留存核。

## 1. Primary 来源重新核查

本轮直接联网读 [Deng 等 arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2) 的 §2、§5 Definition 4 和 Theorem 5.2。其顺序 SPE 要求所有有序前缀上的真实后继比较。两人上界为 3/2；一般人数给出 2-1/m 下界，并未给一般上界2。两人证明使用真实末位 BR 对同一静态势的最大化。多名后继的 SPE 不自动最大化该势，因此本轮不把这一行当归纳假设。

上述为重新核过的文献事实；下文是本轮自己的概率付款探索，不是文献综述。原论文不提供下文多 context 合并结论。

## 2. 优先权表示保留全部真实完成叶

固定原完整 SPE σ、实际叶 z、实际位置 i 和合法查询 A，记 y_(i,A)=finish_σ(z_<i,A)。抽一个均匀全局玩家排列 π，不让玩家观察。对任意固定叶 y，把每名客户分给其覆盖者中 π 最早者；记 i 获得的客户数为 V_i(y;π)。则

\[
\mathbb E_\pi V_i(y;\pi)=u_i(y),\quad
D_i(A):=\mathbb E V_i(y_{i,A};\pi)\le u_i(z).
\tag{1}
\]

对 missed source x∈O\C，实际前缀不覆盖 x。因此在实际位置 i 查询一个含 x 的主题时，若 winner 不是 i，它必是未来 j>i。把 x 转交给该 winner 在真实查询叶中所选的主题，再在 j 的实际前缀重新查询，角色严格增加，至多 m 次终止。若同一 π 保持不变，优先权也严格提前，但角色递增已经足以终止。

这段只构造无循环的客户来源路径。它不保证多名客户在某角色触发同一个查询，也不保证使用原 IC 的行系数合法。

## 3. 条件 IC 不能免费使用

写固定原行的 winner 差

\[
G_{i,A}(\pi)=V_i(z;\pi)-V_i(y_{i,A};\pi),\quad
\mathbb E G_{i,A}=\Gamma_{i,A}\ge0.
\]

如果路线根据 π 选择随机行系数 λ(π)，真正加权项是 E[λG]，一般不等于 (Eλ)Γ。只证明每角色访问一次或 π rank 下降，都没有消除这一差别。

root 已给完整两人、同目录反例并独立核查：不交主题 A 大小1、B 大小2，根选 A，末位在两种根行动后都选 B，是全历史 SPE。根实际与偏离期望收益均1；但条件根 priority 早于末位，winner 差为1-2=-1，反序为1-0=1。所以 λ=1{根先} 给 E[λG]=-1/2，尽管 Γ=0。这是旧底层游戏的本轮 IC-conditioning 诊断，不是新的 half 反例；本分支不再扩张同机制例。

## 4. 一个可以直接支付的整行上包络

下面的付款不需要条件 IC 非负。它对任意 m、目录、完整 SPE 和任意共同 winner 耦合成立，只要求每个固定查询叶的 winner 边际满足 (1)。

给实际位置 i、各合法 A 任意非负随机系数 λ_(i,A)(ω)。若有**确定常数** c_(i,A)>=0，使对所有 ω 有 λ_(i,A)(ω)<=c_(i,A)，则非负性给

\[
\boxed{\mathbb E\sum_A\lambda_{i,A}(\omega)
 V_i(y_{i,A};\omega)
\le\sum_Ac_{i,A}D_i(A)
\le u_i(z)\sum_Ac_{i,A}.}
\tag{ENV}
\]

所以 Σ_A c_(i,A)<=1 时，i 的整份实际利润已支付该角色所有这类随机查询收入。只要有一个固定查询 A、0<=λ<=1，便可支付一份完整 u_i；不必证明 E[λG]>=0。条件 IC 反例否定的是按 Eλ·u_i 缩减后的钱包，并不否定完整 u_i 可支付一个固定查询。

同样，允许客户来源系数 q_(i,A,x)(ω) 各不相同，只要对 x∈A 都有 0<=q_(i,A,x)<=c_(i,A)，则先逐客户支配、再求完整行，得到

\[
\mathbb E\sum_{A,x}q_{i,A,x}(\omega)
1\{x\text{ 在 }y_{i,A}\text{ 分给 }i\}
\le\sum_Ac_{i,A}D_i(A).
\tag{ENV-SOURCE}
\]

这没有按客户重权原 IC：客户支配在使用 IC 之前已合并成常数乘以整行利润。

**精确限制。** 只有每个 ω 下 Σ_A λ_(i,A)(ω)<=1 不够。不同 ω 可以选择不同查询而专选实现 winner 收益较高的查询。ENV 需要一份确定上包络，例如 c_(i,A)=sup_ω λ_(i,A)(ω)，并控制其和；或直接控制更细的 Σ_A c_(i,A)D_i(A)。本轮未证明 priority 路由自动供应该包络。

ENV 是一个实际可付合同，但不作为新的 half 推进：它仍未把全覆盖来源流放进这一行质量条件。后续来源核查已确认其付款步骤是旧 whole-query COVER/PAY 的概率支配特例，详见 §9；不是新增资金关系。

## 5. 未曝光的每角色彩票可以保留原 IC，但回到既有流

另一种修正是预先独立抽每角色的一份排列 π_i。同角色所有查询共享 π_i；在处理角色 i 时，只曝光 π_<i。先根据过去确定整行系数 λ_(i,A)，再揭 π_i。条件期望给

\[
\mathbb E\left[\sum_A\lambda_{i,A}G_{i,A}(\pi_i)
\mid\mathcal F_{<i}\right]
=\sum_A\lambda_{i,A}\Gamma_{i,A}\ge0.
\tag{FRESH}
\]

missed 客户仍只能转给未来角色，故无需保持同一全局 priority 来终止。FRESH 修正条件化债，不修复多 context 的行质量。若按每客户均匀分给当前/未来覆盖者取条件均值，就回到仓库既有 increasing-role capture kernel。因此本轮没有把此表示认领成新的共享付款机制。

## 6. 独立客户彩票只局限 conditioning 债，不支付它

令 C 为实际覆盖、R=O\C。可以给不同客户独立排列，仅用 R 客户的 lottery 决定路线和 λ；C 彩票完全不曝光。对一个固定 i,A 行，λ 与该行全部 C winner 独立，原实际 R 贡献为零。于是精确有

\[
\boxed{\mathbb E[\lambda G_{i,A}]
=(\mathbb E\lambda)\Gamma_{i,A}
-\sum_{x\in A\cap R}\operatorname{Cov}
\left(\lambda,1\{i\text{ 在 }y_{i,A}\text{ 赢得 }x\}\right).}
\tag{COV-R}
\]

因此该耦合可把 conditioning 债局限到 missed 来源，不污染 actual-C 客户。共同一个玩家排序通常没有这份独立性。

但 COV-R 的协方差正是源吸收因条件早优先权而放大的部分，本轮没有从真实后继 IC 得到它的共同上界。把它直接删掉仍是不合法付款；用新彩票恢复均匀分享则退回 FRESH/旧捕获核。

## 7. 真正未完成的一般桥与 m=5 压力

写 I=|O∩C|、G=|C\O|、R=|O\C|，则 OPT_m=W+R-G。若选定一次最优主题 owner、在 R 上取消总质量 G（R<=G 时目标已直接成立），并把剩余 R-G 来源质量安排成守恒吸收流；同时其各角色随机来源系数满足 ENV-SOURCE 的一份确定包络 Σ_A c_(i,A)<=1，则 R-G<=Σ_i u_i=W，从而 half。该段说明 ENV 合同的真实接点，没有证明这样的 owner、取消、路线与包络同时存在。

同样必须付清：若选择 COV-R 而不用确定包络，则正协方差减去偏离叶 old-C 利润，还须与未使用的整行实际容量、G 信用共同结算。本轮没有可行构造，不能把这一句话或其代数形式当作覆盖分解。

同一推导代入 m=5，ENV 仍逐角色只付一份 u_i，FRESH 与 COV-R 仍成立。但没有为任意目录、任意完整 SPE 生成五组可兼容的 c_(i,A)；故不能推出 OPT_5<=2W。没有五人专用系数、扫描或目录限制。

## 8. 状态与来源

- Primary 事实已实际读取原论文，未将一般下界当上界，未将双人静态势最大化推广给多后继。
- 本轮 winner 路由方向与 root 并行探索；conditioning 风险及完整两人诊断由 root 提供，本分支另独立识别同类条件化问题，不重复认领游戏。
- ENV/FRESH/COV-R 是本分支一般推导，均有上文直接证明；简单非负支配、条件期望、协方差公式和随机优先权表示不认领数学新颖性。
- 既有 capture-flow 的 source 标量化/净库存限制已读，不把 FRESH 当作新机制。确定包络并未消除已知多 context 容量缺口。
- 未做新有限扫描，无目标反例，无新无条件福利界；内部独立审查未完成，无外审或新颖性认证。

## 9. ENV 来源核查与身份降级

root 指出可能重复后，本分支实际读了以下旧正文：

- [NEW-CAP、全图客户密度及 ONE-WHOLE-IC](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md)，特别 §3-4。其来源保持与单 context 密度保证已经证明；本轮没有新增该结论。
- [同一角色完整 query 的 COVER/PAY 与 ACTION-GROUP](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/credible/joint_query_compression.md)，§3-4。
- [同 action uniform-reset 去重](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/common_action_reset_deduplication.md)，已明确同 action 的来源先合并再花一次 whole IC；底层均分流追溯至 round3 increasing-role capture。

ENV-SOURCE 在旧 COVER 中令

\[
g_i(x)=\mathbb E\sum_A q_{i,A,x}(\omega)
1\{i\text{ 赢得 }x\text{ in }y_{i,A}\},\quad
z_{i,A,x}=\mathbb E1\{i\text{ 赢得 }x\text{ in }y_{i,A}\}
\]

即可得到 g_i(x)<=Σ_A c_(i,A)z_(i,A,x)，然后逐字使用旧 COVER/PAY。因此它是概率实现下的旧向量支配合同，不是新 cap、新源保持、新钱或新 half 组件。它的用途仅是纠正“weighted IC 为负就连完整 u_i 钱包也不能使用”的过强判断。

最终交接仍是旧跨 action/context 共同系数预算未付。FRESH、COV-R 和优先权终止也没有给出新的共同金额。parent 的 A2/B1 完整 SPE 自适应末位例进一步区分了 pointwise rowmass1 与确定上包络，相关反例由 parent 保存，本分支不重复构造或认领。
