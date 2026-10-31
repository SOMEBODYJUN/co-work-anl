---
id: "customer-attraction/beta-clone-single-use-gains-collision-debt-and-multiplicity-upper-tails"
kind: "lemma"
type_tag: "引理"
title: "Beta克隆的单次增益与复用上尾债务"
status: "proved-static-all-terminal-relations; no-cross-tree-lift"
summary: "任意含重复终局的单次clone玩家获益、复用总债D+G、所有multiplicity上尾与非降权比较完整保；标签商统计依提升，静态同叶账不控制另一真偏离叶。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/background_salvage_next/clone_collision_debt_and_credible_gap.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/background_salvage_next/clone_collision_debt_and_credible_gap.md"]
source_ids: ["56eb68b10bd80ec8a1ee"]
review_status: "原五Markdown全文与全仓正式对象比较；知情解析清洗，原先手算/后读稿与两实现scope保真，数学CLI0"
truth_status: "静态表示/固定策略lift反例/同叶碰撞债已证；更弱可信lift与背景半利润未由这些源解决"
---

# 任意重复终局与统一单位口径

用[非负Beta静态表示](../等价/Beta克隆对背景利润的非负静态表示--等价.md)，原背景b_x整数，q≥r，b≥1时P_x密度b(1−p)^(b−1)，b0时P1。记号是有限有理兴趣型，清共同整数M后为确定单位客户；以下全部除M。

任意r槽clone终局z允许重复，πz为原主题投影。玩家i的实际clone收益U_i^c，原投影背景收益

\[
U_i^b=\sum_{x\in\pi(z_i)}\frac1{b_x+K_x},
\quad K_x=\sum_{j=1}^{d_x}n_{x,j},
\]

d_x为相关**不同clone标签数**，n_(x,j)为其使用次数。全局同clone使用次数不依客户，x只列相关标签。S为完整clone标签恰出现一次的玩家，R为其余，不按原主题重复划分。无相关玩家时各项0，b=K=d0的比例定义0。

若同覆盖标签商掉，可任取标签提升应用；S、R、H_t依提升而变，不能说是商目录内在统计。实际经济收益和相应静态比较仍正确。

# 单次clone玩家逐客户不吃亏

**命题1。** 每i∈S有U_i^c≥U_i^b，逐原客户成立。

固定其喜欢的x、条件P=p且该i标签被含，考虑别人一个n≥2重复标签的拥挤nI，I~Ber(p)，其余负载Z固定。拆成n个不同fresh标签后负载Y~Bin(n,p)。g(s)=1/(1+Z+s)凸，在[0,n]有

\[
g(y)\le(1-y/n)g(0)+(y/n)g(n),\quad
E g(Y)\le(1-p)g(0)+pg(n)=E g(nI).
\]

乘i被含概率p，对Z/P平均，说明拆开别人的重复标签不会提高i份额。依次拆完全部其他重复，i本身单次，相关K标签全鲜，静态表示份额恰1/(b+K)。原重复终局给i至少此值；b0时P1各步取等。单次玩家因**别人复用**而获益，不能误推所有玩家都同向。

# 覆盖损失与全部复用者的精确债

clone覆盖只依不同标签d，原投影利润依带复用K：

\[
W_c=\sum_x\frac{d_x}{b_x+d_x},\qquad
P_b=\sum_iU_i^b=\sum_x\frac{K_x}{b_x+K_x}.
\]

故

\[
D=P_b-W_c=\sum_{x:b_x>0}\frac{b_x(K_x-d_x)}{(b_x+K_x)(b_x+d_x)}\ge0,
\quad G=\sum_{i\in S}(U_i^c-U_i^b)\ge0.
\]

分母b>0自动正；K0项0。实际clone份额守恒Σ_iU_i^c=W_c，移S项即精确逐客户/全局恒等式

\[
\boxed{\sum_{i\in R}(U_i^b-U_i^c)=D+G\ge0.}
\]

若全终局只有一个重复标签、其n≥2使用者选同一clone，则其Uc相同、Ub亦相同，故每位Uc≤Ub。多个重复标签只给总和，不可把同一D+G逐组重复分摊。

# 每个复用次数上尾都折扣

令n_i为i完整clone在z的全局次数，H_t={i:n_i≥t}，整数t≥1。**命题2。** Σ_(H_t)U_i^c≤Σ_(H_t)U_i^b，任意t。

固定客户x/P=p，两个相关标签j,l的次数n_j,n_l，其他负载Z。两标签都含或都不含时份额差0，仅一含给

\[
v_j(p)-v_l(p)=p(1-p)E\left[\frac1{n_j+Z}-\frac1{n_l+Z}\right].
\]

所以n_j≥n_l⇒v_j≤v_l，积分亦保。相关上尾J_t={j:n_j≥t}按n_j加权的平均份额≤全相关组加权平均；令C_t=Σ_(J_t)n_j，K=Σn_j。C_t>0时

\[
\sum_{j\in J_t}n_jv_j
\le\frac{C_t}{K}\sum_jn_jv_j
=\frac{C_t}{K}\frac d{b+d}
\le\frac{C_t}{b+K}.
\]

最后一式等价bd≤bK；C_t0两侧0，K0客户无贡献。右端正是H_t玩家背景投影从x所得份额，对x求和即结论。它包含t1总覆盖≤总背景利润，t>r空集平凡，不要求给出所有无穷阈值计算。

任意f:{1,…,r}→R_≥0非降，写f(n)=f(1)+Σ_(t=2)^r[f(t)−f(t−1)]1_(n≥t)，各系数非负，故

\[
\sum_i f(n_i)U_i^c\le\sum_i f(n_i)U_i^b.
\]

使用**全局最大复用次数**标签的每位也逐人Uc≤Ub：逐客户其份额≤所有相关组加权平均，再用d/[K(b+d)]≤1/(b+K)。不是任意复用组的逐人声明。原§4为作者独立逐式强化，当时尚未独审，当前知情解析核其证明，不倒填原父方已全审该加节。

# 静态同叶账为何仍不产生可信lift

原完整σ当前规定利润u，改原主题T后真叶t_σ(T)只给u≥u_i^b(t_σ(T))。clone重复后真SPE可能产生另一叶z，πz未必是该叶，甚至未必是原背景该孩子某SPE叶。最有利单组折扣也仅Uc_i(z)≤Ub_i(πz)，并无Ub_i(πz)≤Ub_i(t_σ(T))。

原反例精确为重复后clone25≤投影AAC背景27，但要求保留的fresh AAB只有24；同叶折扣完全成立却动态偏离盈利。同一叶D+G转给其他玩家不允许把互斥子树收益移去规定叶，也不使规定原后继在重复孩子仍最优。

仍未证明/未被本稿反驳的两较弱接口：其一，存在无约束clone完整SPE全鲜实际叶投影为原σ实际叶，但其他fresh历史可重选；其二，只需某clone完整SPE τ有W_c(τ)≤P_σ，不要求叶/计数。第一蕴含第二，第二若普遍成立结合根half与OPT_clone=F_r(b)才推背景半利润。静态各式既未选τ、未保真实后继最优，也未控所需跨叶福利方向。

原单客户b2、复用(1,2,4)的Fraction核对报告：每用户份额236/1575、41/420、803/12600，Ub每人1/9，D8/45、G61/1575、复用总债341/1575=D+G，t1…4上尾全过。这只是原MD有限公式核对；本批没读跑其程序/日志，不据一个例替代上述全参数解析证明。
