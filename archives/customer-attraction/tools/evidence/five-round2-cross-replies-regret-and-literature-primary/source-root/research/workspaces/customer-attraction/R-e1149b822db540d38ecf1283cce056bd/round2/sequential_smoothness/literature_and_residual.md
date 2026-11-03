# 一手顺序拍卖机制与 CAG 的真实外部性残差

2026-10-25，Q-CAG-HALF-5 专项。原论文事实与本稿解释、直接推导分开。没有找到可直接导入五人半覆盖的定理；这个检索记录不证明世界上不存在相应结果。完整历史依赖与全部任意平局始终保留。

## 1. 已实际搜索、打开的原论文

| 一手来源 | 原文精确位置 | Paper Fact（原论文事实） |
|---|---|---|
| Paes Leme–Syrgkanis–Tardos, [Sequential Auctions and Externalities, arXiv:1108.2452v2](https://arxiv.org/pdf/1108.2452) | §3.2 Theorem 3.2，PDF第6–7页；§3.3 Theorem 3.4，第8页起 | 单位需求者的逐项顺序第一价格拍卖，纯 SPE 的福利比上界2；混合情形上界4。证明用目标物品在实际历史的价格支付差额。其一般次模估值版本可以有无界福利损失。 |
| Syrgkanis–Tardos, [Bayesian Sequential Auctions, arXiv:1206.4771](https://arxiv.org/pdf/1206.4771) | §3.1 Theorem 3.1及其证明，PDF第8–10页，尤其第9页的随机类型 w 与 bluffing 偏离 | 单位需求者的 Bayesian 顺序第一价格拍卖，所核版本给 `2e/(e-1)` 上界。偏离者抽类型样本 w，在目标物品之前按样本自己的类型 w_i 行动，再在目标物品处改变报价；期望消去历史与真实类型的相关性。原文首页注明修正旧版 Theorem 3.1 中的错误，界由3改为约3.16。 |
| Syrgkanis–Tardos, [Composable and Efficient Mechanisms, arXiv:1211.1325v1](https://arxiv.org/pdf/1211.1325) | §5 Theorem 5.2，PDF第7页；Appendix C.3证明，PDF第26页 | 若各机制 `(lambda,mu)` smooth，且玩家对跨机制配置的估值为各机制估值的最大值，顺序组合的完整策略正规式为 `(lambda,mu+1)` smooth。证明沿用原策略直至目标机制，再作该机制的 smooth 偏离；到该时刻的历史与原策略相同。 |
| Paes Leme–Syrgkanis–Tardos, [The Curse of Simultaneity，作者论文页PDF](https://www.renatoppl.com/papers/spoa-itcs.pdf) | §3 Theorem 1和Observation 2，PDF第4页；§5 Theorem 6，第5页 | machine cost-sharing 中每人只选一个机器，成本 `c_r/k`，玩家最小化成本；通过有利规模效应与倒推匹配 greedy，得对数界。另对二色 cut games 给顺序PoA上界4；该证明仅利用已经到达的边所给的不可被未来删除的收益保证。 |
| Vetta, [Nash Equilibria in Competitive Societies](https://web.mit.edu/6.454/www/www_fall_2004/gametheory/VettaNashEquilibria.pdf) | §2.3，PDF第3页式(1)–(4)；§3 Theorem 3，PDF第4页，单调情形后续推论 | valid utility 要求个人效用至少其退出的社会边际、效用总和至多社会效用；对单调次模福利的静态 NE 得半覆盖。它比较的是保持他人动作不变的偏离。 |

这里只依赖上表原论文；搜索结果中的二手摘要没有作为定理依据。

## 2. Interpretation：可迁移的想法和不能迁移的承重步骤

可以保留“直到目标时刻才偏离”的设计：在 CAG 玩家 i 的实际有序历史 h_i，只改变 i 此时选的主题，之后**同一原策略**真实执行。这样的偏离对任意完整 SPE 都合法，完全不需要指定平局规则。

但第一价格拍卖的目标配置在目标拍卖完成后已归偏离者所有。偏离者能停止后续参与，保持所得物品，故后续陌生行为不破坏其价值下界。在 CAG，选择主题后每个客户的最终份额仍会被后继覆盖者稀释；没有“获得一次后退出但保留原份额”的合法行动。把终局客户份额当作前期已经确定的配置，违反组合机制的局部配置结构。若改把配置说成“主题所有权”，效用又不是该局部配置的固定价值。

Bayesian bluffing 的样本只用于选择自己的早期行为，并保证目标机制前的历史仍来自同一均衡策略族。CAG 一人只行动一次：玩家 i 改写自己的完整映射不能改变 i 之前由别人形成的历史；它也不能隐藏已经公开选择的主题，让尾部不响应。抽样主题后再令后继不观察样本，是改动信息结构。因此原文的独立类型平均不能自动去掉这里真实后继与被抽主题的相关性。

cost sharing 的 `c/k` 是越拥挤成本越低，CAG 的 `1/k` 是越拥挤收益越低；直接改符号还会改变社会目标及比值。cut game 的过去跨色边不可被后来者夺走，而 CAG 的过去份额可被降低。两者的贪心/过去收益证明都不能在本模型原样使用。

更强的精确边界见同目录 `normal_form_obstruction.md`：五人全策略正规式本身存在 `OPT5/W=300/137>2` 的纯 NE。所以一般组合定理若对这个正规式的全部 NE 宣称因子二，就必然失败；SPE 专用顺序 smoothness 仍可成立，且必须使用真正的离轨理性。

## 3. Direct derivation：可信偏离的精确稀释价

固定任意合法有序历史 h，旧负载为 b_x；当前选择任意合法主题 T，随后原策略给出真实尾部主题，令其客户负载 d_x。当前偏离收益为

\[
Q_h(T)=\sum_{x\in T}\frac1{b_x+1+d_x}.
\]

主题的即时份额价值、稀释价分别为

\[
g_h(T)=\sum_{x\in T}\frac1{b_x+1},\qquad
\tau_h(T)=\sum_{x\in T}\frac{d_x}{(b_x+1)(b_x+1+d_x)}.
\]

逐客户有精确恒等式

\[
\boxed{Q_h(T)=g_h(T)-\tau_h(T).}\tag{1}
\]

若把该真实偏离叶中尾部在客户 x 上的总收益记为 `v_tail,x=d_x/(b_x+1+d_x)`，则

\[
\boxed{\tau_h(T)=\sum_{x\in T}\frac{v_{\mathrm{tail},x}}{b_x+1}.}\tag{2}
\]

特别地，T 中 h 尚未覆盖的客户贡献的稀释价恰为这条**同一真实分支**的尾部收益。它不是原实际叶的价格，更不能在不同 T 的互斥续局之间免费相加。非根式(1)完整保留 b_x，未把旧玩家利润变化当零。

## 4. Direct derivation：静态 smoothness 的准确动态残差

固定一份完整形式策略 sigma（暂不要求 SPE），实际主题 `a=(A1,...,A5)`。取任意五个合法比较主题 `T1,...,T5`，允许空主题、重复。对客户 x 设：

- `z_i=1_{x in Ai}`，`c=sum_i z_i`；`b_i=sum_(j<i) z_j`，`e_i=sum_(j>i) z_j`。
- `t_i=1_{x in Ti}`，`o=1_{sum_i t_i>0}`，`w=1_{c>0}`。
- 在玩家 i 的**实际历史**改选 Ti，之后沿原 sigma 得到真实尾部，其负载为 `d_i`。

冻结其余实际动作的静态查询贡献与真实查询贡献分别为

\[
f_{i,x}=\frac{t_i}{b_i+1+e_i},\qquad
q_{i,x}=\frac{t_i}{b_i+1+d_i}.
\]

其差额精确为

\[
\boxed{\Delta_{i,x}=f_{i,x}-q_{i,x}
=\frac{t_i(d_i-e_i)}{(b_i+1+e_i)(b_i+1+d_i)}.}\tag{3}
\]

该项可正可负，不删任何符号。定义静态逐客户 slack

\[
s_x=w+\sum_i f_{i,x}-o\ge0.\tag{4}
\]

证明：若 c=0，则每个分母均1且 `sum t_i>=o`；若 c>0，则 `w-o>=0`，其余项非负。这只是覆盖的静态 smoothness，未假定终局是静态 NE。

再记

\[
\Gamma_i=u_i(a)-\sum_xq_{i,x},\qquad
D=\sum_{i,x}\Delta_{i,x},\qquad S=\sum_xs_x.
\]

sigma 若为完整 SPE，则每个 Gamma_i>=0，由玩家 i 的精确实际历史 IC 给出。纯代数给

\[
\boxed{2W(a)-\left|\bigcup_iT_i\right|=\sum_i\Gamma_i+S-D.}\tag{5}
\]

验证：`sum Gamma=W-sum q`，`S=W+sum f-|union T|`，`D=sum f-sum q`，相减即得。没有将两条互斥偏离叶的利润当成同一个预算。

若 T 是最优五主题，则一个**尚未证明的充分加强**是允许选其排列后有 `D<=S`，即 `sum_i Q_(h_i)(Ti)>=OPT5-W`。结合实际 IC 会给 half。更弱的精确缺口是支付 `D-S` 到实际 IC slack `sum Gamma`；式(5)本身只重写目标，不是证明。旧最优匹配反例否定的是更强的纯遗漏收费，不能据此判定这个净需求版本；本稿也没有证明它。

## 5. 反事实正规式 NE 对该残差的定量测试

对同目录437客户策略取比较主题 `(O1,...,O5)`，有

\[
(\sum_xq_{i,x})_{i=1}^5=(12,15,20,30,60),\quad
(\sum_xf_{i,x})_{i=1}^5=(60,60,60,60,60),
\]

故 `sum Gamma=0`, `D=163`, `S=137`，式(5)精确为 `274-300=0+137-163=-26`。

这说明只有实际路径 IC 的证明还缺至少26单位的真实离轨约束效力；那些 IC 在此策略中全部成立，而 O1 后第二位有48单位盈利偏离。这个例子不保证简单把48乘某个系数就能产生普适逐客户证书。真正后继 IC 的效力还须连到根 W；一个离轨叶的负 slack 或整条枝利润并非根可花预算。

## 6. 边界和剩余义务

式(1)–(5)允许零客户、空主题、重复比较主题、任意有序历史和任意平局。所有出现的查询分母至少1；实际个人份额只在其选中客户上计算，不出现0/0。零客户时全部数值为0。

本轮新增的是可复核的普适代数接口，以及一个准确排除全策略正规式因子二 smoothness 导入的有限构造；没有得到五人所有完整 SPE 的 `D<=S+sum Gamma` 新付款，也没有构造真实 SPE 的越二反例。顺序拍卖文献提供“保留目标时刻前的实际历史”的偏离设计，但不可撤销配置/局部价格这个承重性质在 CAG 缺失，须由新的离轨 IC 运输机制补齐。
