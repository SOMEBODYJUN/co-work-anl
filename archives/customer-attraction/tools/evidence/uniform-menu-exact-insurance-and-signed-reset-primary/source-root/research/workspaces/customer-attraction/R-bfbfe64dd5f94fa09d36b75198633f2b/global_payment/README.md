# 跨真实分支直接付款：本轮准确停止点

2026-10-25。任意有限共同目录、任意人数、任意完整有序历史纯 SPE；原 **Q-CAG-HALF 仍 OPEN**。本目录未得到新增的一般福利不等式、辅助反例或完整证明。没有作有限阴性扩样，也没有使用已失败的逐人 floor。

本轮独立推导了“多后继循环遗憾 → 更深真实 IC + 删槽重置”的展开，随后发现它与下列既存资产重复。因此只留下一个接续所需的总式及准确未付量，不另建新 Claim，不把等价重排算作正向推进。

## 可以直接续写的精确总账

固定原完整 SPE 的实际路径，实际位置 i 的前缀为 h_i，收益为 u_i。强制当前主题 A 后沿**同一原策略**产生的完整 m 槽终局记为 Z_i(A)，当前以后真实尾序列为 Y_i(A)。任取同一个主题分布 p，令 A,T 独立服从 p，并定义

\[
C_i(p)=\mathbb E_{A,T}\sum_{x\in T}\frac1{1+c_x(Z_i(A))},\qquad
e_i=u_i-\mathbb E_Au_i(Z_i(A))\ge0.
\]

固定实际前缀负载 b_i，并对**完整** profile 用总调和势 \(\Phi(Z)=\sum_xH_{c_x(Z)}\)。从根 A 的真实叶开始，按时间顺序逐一强制尾部改成目标序列 Y_i(T) 的对应主题，每一步以后仍沿原策略。第 j 步当前角色为 \(\ell=i+j\)，前后完整 rollout 为 \(Z^{j-1},Z^j\)。置

\[
\gamma_{i,j}(A,T)=u_\ell(Z^{j-1})-u_\ell(Z^j)\ge0,
\]

\[
d_{i,j}(A,T)=\Phi((Z^j)^{-\ell})-
\Phi((Z^{j-1})^{-\ell}),
\]

其中删槽只是形式势运算，删槽后的后继**未被断言为 SPE**。再置原完整列的额外槽折扣

\[
J_i=\mathbb E_{A,T}\sum_{x\in A\cap T}
\frac1{[b_i(x)+1+c_x(Y_i(A))]
[b_i(x)+2+c_x(Y_i(A))]}\ge0.
\]

调和势单槽边际等于该玩家利润，逐步相消并交换独立 A,T 后，得到

\[
\boxed{
W-\sum_iC_i(p)=
\sum_i(e_i+J_i)+
\mathbb E\sum_{i,j}\gamma_{i,j}
-\mathbb E\sum_{i,j}d_{i,j}.}
\tag{*}
\]

这是下列旧展开在全部实际位置的合写，不认领新机制。每条 \(\gamma\) 都是原树真实合法 IC；不同 rollout 的 \(d\) 没有自动符号。

末位 i=m 的尾和为空，且有**精确**而非仅下界的式子

\[
u_m-C_m(p)=e_m+
\sum_x\frac{q_x^2}{(b_m(x)+1)(b_m(x)+2)},
\quad q_x=\Pr_{A\sim p}(x\in A).
\tag{LAST}
\]

倒二位置的唯一尾部改动也是末位改动，删掉末位后两叶完全相同，故该位置所有 d 均为零；在 LAST 型折扣外再有真实末位 BR 松弛。一般位置中，任何最后一步的 d 也为零。真正剩下的是 i<ℓ<m 的中间角色删槽 reset。

## 没有支付的准确义务

若采用已有的全分布弱额外槽桥 \(\sum_iC_i(p)\le W\)，则 (*) 需要同一次耦合满足

\[
\mathbb E\sum_{i,j}d_{i,j}\le
\sum_i(e_i+J_i)+\mathbb E\sum_{i,j}\gamma_{i,j}.
\tag{未证付款}
\]

本轮没有得到此式，甚至没有得到可由最后两人二次税共同支付左边的新 Cauchy 界。\(1/k\) 的凸性、末位对角折扣和逐条真实 IC 都成立；它们尚未把互斥历史中的正 reset 变成同一终局的一份信用。不能逐客户加权原 IC，也不能把多位后继当作一个联合最佳回复者。

这条全 p 桥仅为充分候选；可另选安全最优 p，或自由菜单列，或完全绕开额外槽。五人压力代入仍含六类可能的中间 reset 对 \(i<\ell<5\)，没有无条件推出 \(\operatorname{OPT}_5\le2W\)。没有在五人专用模板调系数。

## 已读且应复用的旧资产

- `research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/early_price/harmonic_tail_menu_debt.md`：任意后继数量的循环调和势身份；已有完整 SPE 的负循环遗憾及组合债边界。
- `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/global/full_depth_substitution.md`：上述逐历史 \(\gamma,d\) 展开、删槽信号的可信性问题；本轮展开与其重复。
- `research/workspaces/customer-attraction/R-059140e622784d85a4e3a4dd6554f506/menu_covariance/last_successor_peeling.md`：先付款真实末位 BR，再留下中间背景漂移的 PATH-PEEL；与 (*) 同一缺口的另一表示。
- `research/workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/menus/optimal_union_meta_regret.md`：可放弃全 p 加强，选择内生 meta-Nash，并保留共同负载分散税与最优并集税；其 TREE-PAY 仍未证。
- `research/current/customer_attraction/general_half_proof.md` §§5、7、8：真正聚合安全值、全树非负 IC 支付与自由完整路径菜单三条准确 OPEN 接口。

## 接续条件与审查义务

值得接续的是一条**此前没有的真实跨历史容量或共同付款关系**，能够控制 (*) 的正 reset；仅进一步展开、改名、换调和势端点或复查旧有限样本不会增加资金。本轮在这里停止，没有证明所有可能的循环单调、Cauchy 或全树耦合方法不可能。

若后续找到付款式，须独立重构：所有系数是否非负且使用整条 IC、两边是否采用同一个原策略与同一个源耦合、过去玩家是否仍被计入、删槽对象是否被误用为 SPE、同份税是否跨分支重复付款。当前文件只作父方汇总的准确停止记录，不作为经过独立审查的新数学结果。
