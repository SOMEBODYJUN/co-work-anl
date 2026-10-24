# 多槽最优补全交换与比较关联—真实尾负载矩关系

2026-10-24。范围：Q-CAG-HALF 原模型的全部输入。**工作区身份 EXCHANGE-MULTISLOT-v1；定义级静态组件，已获[独立内部重构](../credible/exchange_review.md)，不主张外审或新颖性。**该重构不是盲审：审查者首次读取整页时证明亦已显示，准确范围见审查正文。

这里给出一族可以严格成立的静态关系，并记录其不能直接支付一般 half 的原因。它们适用于任意有限单位客户、任意有限非空共同目录、任意人数和任意有序历史；对其中任一完整纯 SPE 当然成立。其证明不使用 SPE，故不能声称已经新增了一条动态福利结论。

## 1. 固定背景及最优补全

固定任意合法有序历史，过去覆盖为 P，尚余 r≥1 个单位玩家。记

\[
F_k(Q)=\max_{A_1,\ldots,A_k\in\mathcal S}
 |Q\cup A_1\cup\cdots\cup A_k|,\qquad F_0(Q)=|Q|.
\]

取任意最优 r 元组 \(T_1,\ldots,T_r\)，主题可重复。置

\[
C^*=\bigcup_{j=1}^rT_j,\quad G=|P\cup C^*|=F_r(P).
\]

另取任意合法当前主题 S，特别可以取原完整 SPE 在该精确历史的规定动作。令

\[
H=F_{r-1}(P\cup S),\quad \delta=G-H\ge0,\quad
E=S\setminus(P\cup C^*),\quad e=|E|.
\]

e 是 S 覆盖而比较最优并集不覆盖的真实客户信用；不能删除。已有71客户完整二人反例表明，即使有利重选最优并集，全部遗漏也可能多于实际 W。

对非空槽位子集 \(J\subseteq[r]\)，定义

\[
D(J)=C^*\setminus\left(P\cup\bigcup_{j\notin J}T_j\right).
\]

也即 D(J) 的客户所有比较覆盖槽都属于 J。它包含只由某一个槽覆盖的私有块，也包含由 J 内多个槽共享的客户。重复主题仍照槽位定义。

## 2. 全范围多槽交换关系

**Claim ME。** 对任意非空 \(J\subseteq[r]\)，置 k=|J|；对任意 k−1 个合法主题 \(Y_1,\ldots,Y_{k-1}\)，令 \(Y=\bigcup_\ell Y_\ell\)。则

\[
\boxed{
|D(J)\setminus(S\cup Y)|
\ge e+\delta+
 |Y\setminus(P\cup C^*\cup S)|.
}\tag{ME}
\]

**证明。** \(S,(T_j)_{j\notin J},Y_1,\ldots,Y_{k-1}\) 恰占 r 个槽，且当前槽为 S，因此它的总覆盖至多 H。与最优覆盖 \(P\cup C^*\) 逐客户相比，其精确损失是
\(D(J)\setminus(S\cup Y)\)，精确新获客户是不交的 E 与 \(Y\setminus(P\cup C^*\cup S)\)。所以

\[
\begin{aligned}
H&\ge |P\cup S\cup\bigcup_{j\notin J}T_j\cup Y|\\
 &=G-|D(J)\setminus(S\cup Y)|
 +e+|Y\setminus(P\cup C^*\cup S)|.
\end{aligned}
\]

代入 H=G−δ 即得。没有把 Y 视作 S 孩子的真实 SPE；它只是一个合法静态补全。证毕。

若显式记录松弛

\[
\zeta_{J,Y}=H-
 |P\cup S\cup\bigcup_{j\notin J}T_j\cup Y|\ge0,
\]

则 (ME) 可以写成精确恒等式

\[
|D(J)\setminus(S\cup Y)|
=e+\delta+|Y\setminus(P\cup C^*\cup S)|+\zeta_{J,Y}.
\tag{ME-exact}
\]

边界：k=1 时 Y 为空，给每个比较槽私有块
\(|D(\{j\})\setminus S|\ge e+\delta\)。k=r 时给保留 S、任取 r−1 尾槽的整体补全信用；若所取尾槽达到 H，则该行等号。因此整族包含而不超越最优补全的完整可行性；不能单凭出现了更多交换行，声称获得了新的 half 证明。

## 3. 比较关联数与真实尾负载的联合矩推论

固定任意 r−1 个合法主题 \(B_1,\ldots,B_{r-1}\)。它们可以是原完整 SPE 强制某个当前行动之后的**真实尾元组**，也可以是实际 S 孩子的真实尾元组；无需冻结其他分支。

令

\[
t_x=|\{j\in[r]:x\in T_j\}|,\qquad
q_x=|\{\ell\in[r-1]:x\in B_\ell\}|.
\]

对 k=1,…,r，定义

\[
a_t(k)=\begin{cases}
\binom{r-t}{k-t}/\binom rk,&1\le t\le k,\\
0,&t>k,
\end{cases}
\]

以及（r=1 时单独约定 \(v_0(1)=1\)）

\[
v_q(k)=\frac{\binom{r-1-q}{k-1}}{\binom{r-1}{k-1}},
\]

不可行的二项系数取零。

**Claim MM。** 对每个 k，有

\[
\boxed{
\sum_{x\in C^*\setminus(P\cup S)}a_{t_x}(k)v_{q_x}(k)
\ge e+\delta+
\sum_{x\notin P\cup C^*\cup S}[1-v_{q_x}(k)].
}\tag{MM}
\]

**证明。** 独立均匀抽取 k 个比较槽 J，以及 k−1 个真实尾槽 K。在 (ME) 中取 \(Y=\bigcup_{\ell\in K}B_\ell\)。对 \(x\in C^*\setminus(P\cup S)\)，x 属于 D(J) 的概率是 \(a_{t_x}(k)\)，未被所抽真实尾槽覆盖的概率是 \(v_{q_x}(k)\)；两抽样独立，所以左侧逐客户概率为其乘积。对最优并集及 S 之外客户，被抽尾槽覆盖的概率是 \(1-v_{q_x}(k)\)。取期望即得。证毕。

MM 的 k=1 行是平均比较私有块预算；k=r 行是整个真实尾并集的同尾覆盖信用。中间 k 行把比较共享度与真实尾拥挤度同时保留，并对原模型的任意人数、任意目录成立。这里的两次随机抽样只是证明所用的静态平均，不是把 SPE 换成随机策略，也不假定匿名历史。

## 4. 尝试接入一般证明时的准确义务

已共享的 BG 恒等式将每期 \(\delta-u\) 写成强制最优首动作后的真实孩子损失 ρ，以及 θ、f、ξ、η、Γ 的全部信用。ME/MM 可以合法应用于每个这样的真实尾元组。它们表明：同一孩子不能任意同时吞掉多个比较私有块，吞掉比较外客户还须再留下相应比较缺口。

但仍有两个实质缺口：

1. 对不同强制首动作 \(T_j\)，尾元组是不同的 \(B^{(j)}\)。ME/MM 并未给这些元组提供共同概率耦合；把各孩子的“未覆盖”相加不等于原实际路径的未覆盖。
2. MM 左边仍含实际未覆盖的比较客户，不能仅以尾负载 q 的逐客户函数支付。已有无拥挤完整 SPE 排除了 f(0)=0、f(1)=1 的负载修正；已有纯遗漏反例排除了直接把其总数塞入 W。需要原树后继 IC 的新增付款，而非再删去比较并集外信用。

所以本轮只获得了可用的静态组件，没有获得新的无条件福利下界。它不是一般 half 已完成的证据，也不是 half 为假的证据。

作为未投入证明的想法，曾考虑更弱局部候选 \(\delta\le2u\)，希望先取得非衰减的全人数界；没有找到证明，也没有对它运行扫描，不能列为已证关系。已有负首步余额族令 \(\delta/u\) 趋近2，说明若采用这个候选，任何小于2的固定系数必然失败；这并不证明系数2成立。即使它成立，单独望远镜也仅给 OPT≤3W，仍未达到本题目标。

## 5. 读取及证明边界

本轮已读：根 AGENTS/README/RESEARCH_STATE/CLAIMS/FAILED_ROUTES，CAG-MODEL、general_half_proof，最优首动作 BG、纯遗漏与匹配反例、continuation_lemmas、individual_security_counterexample，以及机会损失/前缀余额及税反例。

这里只写本人分配 exchange 目录，未修改共享 Claim 或状态，未 git 提交、推送或外发。没有有限阴性搜索；ME/MM 的一般性完全来自上述集合恒等与均匀子集计数。
