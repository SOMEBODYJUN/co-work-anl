# 静态中间分母：真实 off-IC 的覆盖拥挤分解

2026-10-24，Boss10/global。任意有限共同目录、任意人数、任意完整有序历史纯 SPE。**Q-CAG-HALF 及共同容量仍 OPEN。** 本稿给出一条未冻结真实后继的 off-IC 恒等式：把 actual 收益与 off-history 收益之差拆为同一 B 叶的背景拥挤、以及真实返回分支 W 的后继响应。它允许在初始单 reset 叶上合法使用过去的 B 规定利润；迭代后出现的强制未来利润必须另外投影，不能假称自然规定利润。

coupling 在未读本证明、仅收到精确合同后独立重构了恒等式与利润支配，并给出额外 query-projection；见 [独立重构](../coupling/static_denominator_and_query_projection_review.md)。没有福利结论或外审认证。

## 1. 对象

固定完整 SPE σ，实际叶 Z=(S_1,…,S_m)，实际收益 u_i，客户实际负载 c_Z(x)。下标从 1 开始。

取任意自然 context t=(g,i)，g 长度 i−1。置

\[
B=\operatorname{finish}_\sigma(g),\qquad a=B_i=\sigma_i(g),\qquad
W=\operatorname{finish}_\sigma(g,S_i).
\]

记 v=u_i(B)、z=u_i(W)、ℓ=v−z≥0。最后一个不等式是 **同一真实 g 节点上返回实际主题 S_i 的原完整 IC**，并不是 actual-prefix IC。

对每个 x∈S_i，定义

\[
d_x=c_B(x)+1-\mathbf1_{x\in a}
    =1+\sum_{j\ne i}\mathbf1_{x\in B_j},\qquad
\theta=\sum_{x\in S_i}\frac1{d_x}.
\]

d 是只替换 i 自己的行动、暂不改变 B 其他行动时的静态分母。它只用于代数中间层；**没有将该静态叶当作 σ 的真实偏离完成叶**。总有 d_x≥1，且 d_x≥c_B(x)。x∈S_i 保证 c_Z(x)、c_W(x)≥1，即使 c_B(x)=0 也无分母问题。

定义

\[
T_B=\sum_{x\in S_i}\sum_{j\ne i}
\frac{\mathbf1_{x\in B_j}-\mathbf1_{x\in S_j}}{c_Z(x)d_x},
\]

\[
T_W=\sum_{x\in S_i}\sum_{j>i}
\frac{\mathbf1_{x\in W_j}-\mathbf1_{x\in B_j}}{d_xc_W(x)}.
\]

按原标签分别写 T_B=P_B−N_B、T_W=P_W−N_W，正负项均非负。

## 2. 精确 off-IC 分解

\[
\boxed{u_i=v-\ell+T_B+T_W.}\tag{SD}
\]

因此真正 off-IC 给出

\[
u_i\le v+P_B+P_W-N_B-N_W.\tag{SD-IC}
\]

对任何 β≥0，gross actual 行相对当前 prescribed 流入的超额满足

\[
\boxed{\beta(u_i-v)
 =\beta(P_B+P_W-N_B-N_W-\ell).}\tag{EXCESS}
\]

**证明。** 直接数覆盖者，得到

\[
u_i-\theta
 =\sum_{x\in S_i}\frac{d_x-c_Z(x)}{c_Z(x)d_x}=T_B.
\]

W 与静态中间层在 i 之前行动相同、i 都选择 S_i，故

\[
\theta-z
 =\sum_{x\in S_i}\frac{c_W(x)-d_x}{d_xc_W(x)}=T_W.
\]

将 u_i−θ、θ−z 与 z=v−ℓ 相加即得。全过程保留 W 的原真实历史依赖后继，允许重复/空主题、任意平局及零客户。□

## 3. 每个正项究竟由哪份利润支配

第一类正项的标签为 (j,x)，j≠i，x∈S_i∩B_j、x∉S_j，其原价

\[
q^B_{ij}(x)=\frac1{c_Z(x)d_x}.
\]

既然 x∈B_j，c_B(x)>0。由于 d_x≥c_B(x)，

\[
q^B_{ij}(x)
 =\frac{c_B(x)}{c_Z(x)d_x}\frac1{c_B(x)}
 \le\frac1{c_Z(x)}\frac1{c_B(x)}.
\tag{B-SHARE}
\]

所以 q^B_{ij}=Σ_x q^B_{ij}(x)≤u_j(B)。这笔钱支配于 **B 中 j 的利润**，不是 W 中 j 的利润，也不是 actual u_j。

第二类正项的标签为 (j,x)，j>i，x∈S_i∩W_j、x∉B_j，原价

\[
q^W_{ij}(x)=\frac1{d_xc_W(x)}
            =\frac1{d_x}\frac1{c_W(x)}.
\tag{W-SHARE}
\]

因此 q^W_{ij}≤u_j(W)。j>i 保证 W_<j 之后完全按 σ，故它是 **真实自然 context (W_<j,j) 的 prescribed 利润**。

上面是逐项利润支配；不同来源相加不保证整行系数≤1。B-SHARE/W-SHARE 也不自动使 SD 的联合正出口成为 sub-Markov 行。

## 4. 单 reset 初始域及迭代域的区别

若 B 来自初始或原前向图的一个 actual-prefix query

\[
B=\operatorname{finish}_\sigma(Z_{<k},A_k),\qquad k<i,
\]

则第一类正项 j<k 不存在，因为 B_j=S_j。j=k 的 B 利润是该 actual-prefix query 的当前利润，可由原 actual IC 支配于 u_k。每个 j>k 都是在历史 B_<j 上真正规定、之后也全部按 σ 的自然 context，规定叶正好 B。这包括 k<j<i 的过去角色；此处没有未来强制动作污染其 B 利润。

**不能把这一单 reset 域无证迭代。** SD 的第二类正项会进入 W 上未来自然 context。W 含原 k 位 query 和后来 i 位返回 S_i 的第二次强制动作。若从该新节点再次使用 SD，其第一类正项在 k≤j<i 可能带有 j 之后 i 位的强制动作。此时 u_j(W) 不是 j 节点的 prescribed 利润，不能直接调用 j 的 IC。

一般地，对叶 F 定义强制位置集

\[
\mathcal F(F)=\{j:F_j\ne\sigma_j(F_{<j})\}.
\]

令 r=max F(F)。对 j>r，finish(F_<j)=F，故自然域合法。对 j=r，F 是该历史上的真实强制 query 完成叶，可由同历史的完整当前 IC 支配于 prescribed 利润。对 j<r 则可能有强制未来，必须保留为 synthetic profit，或使用下一节的额外投影。

## 5. 强制未来利润的合法 query-projection

此修复由 coupling 独立给出并写成 [自足审查 §3](../coupling/static_denominator_and_query_projection_review.md)。这里记录接合，不把 synthetic 利润直接当成 IC 左边。

给任意 synthetic 叶 F、角色 j 及其行动 a=F_j，置 h=F_<j，

\[
R=\operatorname{finish}_\sigma(h,a),\quad
H=\operatorname{finish}_\sigma(h),\quad
f=u_j(F),\quad d=u_j(R),\quad V=u_j(H).
\]

R 是 h 上强制 a 后的 **真实** 完成叶，所以 V≥d。F 与 R 的过去及当前行动相同，覆盖者差异只在 l>j。按当前 a 的客户定义

\[
q_l=\sum_{x\in a:\,x\in R_l,\,x\notin F_l}
\frac1{c_F(x)c_R(x)},\quad
N=\sum_{x\in a}\frac{|\{l>j:x\in F_l\setminus R_l\}|}{c_F(x)c_R(x)}.
\]

则

\[
f=d+\sum_lq_l-N,
\qquad d-N=\sum_{x\in a}\frac{1+\#\text{共同其他覆盖者}}{c_F(x)c_R(x)}\ge0.
\]

当 f>0 时 d−N>0。于是

\[
\boxed{f=\alpha V+\sum_{l>j}q_l,
\qquad \alpha=(d-N)/V\in[0,1].}\tag{PROJ}
\]

零利润行用 α=0。第一项进入真实自然 context (h,j)，其 prescribed 利润 V；每个 q_l 进入真实自然 context (R_<l,l)，其规定叶 R，并且 q_l≤u_l(R)。把任意金额 z≤f 的 synthetic 请求按 z/f 等比例拆分即可。该步是守恒、非负、有限次的合法利润分解，不是过去角色的伪 IC。

PROJ 的单次投影把未来强制问题消掉，但再用 SD 仍可返回已有角色/context。**联合 SD+PROJ 图可能有环；没有证明终止、瞬时性、谱半径<1、共同容量或同时可行。** 也不能把每次 α≤1 相加当 cap1。

## 6. 当前确实新增什么、还缺什么

SD 把原来只以口头描述存在的压力写成精确一般关系：v 小于 actual u_i 的那部分，除了真正 IC 松弛 ℓ 的有利减项，必须来自明确的 B 背景拥挤或 W 真实后继响应。静态中间分母 d≥c_B 让初始单 reset 的过去拥挤有合法 B prescribed 收款人；PROJ 给迭代后 synthetic 利润一个额外合法出口层。

仍需证明一个 **真正全局不等式**，例如存在与原 source/CLIP 使用同一资金的 SD+PROJ 非负权，使全部拥挤债与负项/真实 slack 共同结算，实际各钱包总费用≤2u_j（或净遗漏源总费用≤W）。目前没有这条不等式。恒等式、逐边合法域及单节点 sub-Markov 投影均不等于福利付款。

可接续的精确问题是：在初始化与原前向 reset 图固定后，是否可为 SD+PROJ 环图选择流，使每个源的总期望访问成本有限，并用 source 客户互不重计控制实际出口。若不能，必须另给支付机制；不能把无穷流或未付 synthetic 项丢掉。

## 7. 与共同客户出口兼容的一条容量不等式

下面给一条局部真实容量界，不声称可跨 whole-profit 重采样相加。它扩展 credible 的 prefix→parent 联合投影：共同未来客户券可以和过去券**一起**进入同一个投影，而不是另外占一次 parent 券。

固定任意两叶 F、R 和客户 x。令 C_x 为两叶共同的覆盖者角色集，r_x=|C_x|，令 D_x 为 R 新增覆盖者角色集，即 cover(R,x)\cover(F,x)。对 j∈C_x 给任意请求密度 0≤λ_j(x)≤L_x，其金额是 λ_j(x)/c_F(x)。将它拆为

\[
\text{同角色 }j:\quad
\frac{\lambda_j(x)r_x}{c_F(x)c_R(x)},\qquad
\text{每个 }l\in D_x:\quad
\frac{\lambda_j(x)}{c_F(x)c_R(x)}.
\tag{COMMON-PROJ}
\]

若 r_x=0 没有请求。因为 r_x+|D_x|=c_R(x)，每份请求守恒。以 R 中每个实际份额 1/c_R(x) 计券，目标负载满足

\[
\Lambda_{j,x}=\lambda_j(x)\frac{r_x}{c_F(x)}
\le L_x\frac{r_x}{c_F(x)}\quad(j\in C_x),
\]

\[
\Lambda_{l,x}=\frac{\sum_{j\in C_x}\lambda_j(x)}{c_F(x)}
\le L_x\frac{r_x}{c_F(x)}\quad(l\in D_x).
\]

所以

\[
\boxed{\max_{j\in\operatorname{cover}(R,x)}\Lambda_{j,x}
\le L_x\frac{r_x}{c_F(x)}\le L_x.}\tag{COMMON-CAP}
\]

该不等式逐客户成立，不需要 IC。对同客户的 parent 共同覆盖者与新增覆盖者，输出支持不重叠；把所有 common F-incidence 请求先合成 λ 再投影，即同时支付 prefix 与共同 future 请求。不能先运行 prefix 投影，又让同一 future common 请求全额独立占 R 券。

**精确限制。** F 的 exclusive future incidences（x∈F_j、x∉R_j）不属于输入域；它们可含 R 未覆盖的新客户。COMMON-CAP 没有支付这些请求，也没有证明后续 whole-profit IC 重采样仍保留 λ≤L 或共同客户支持。角色 j 在 R 中是否为自然 prescribed 角色仍须独立核验；本节不把任何 R 利润自动当成真实 IC。

## 8. 固定 B 的全部静态正拥挤共同容量

coupling 和 credible 随后分别提出同一固定叶联合界，root 亦独立重构；自足主证明见 [STATIC-COLUMN](../coupling/fixed_parent_static_column_capacity.md)。本节记录我补出的精确密度与它的支付接口，不把跨 B 的容量免费相加。

固定 B、Z，同时取全部角色 i 的 SD 第一类正项。对任意 0≤θ_i≤L、每个 recipient j，有

\[
\boxed{\sum_i\theta_i q^B_{ij}
\le L\,u_j(B;(C\cap B_j)\setminus S_j).}\tag{STATIC-CAP}
\]

其中 C 是实际覆盖；x∉C 没有发送行，不定义 1/c_Z(x)。这是 **同一 B 上跨全部角色、可有不同 off-return W_i 的联合容量不等式**，不是逐行上界求和。

精确地，对 x∈C，设 z=c_Z(x)、b=c_B(x)、r=|cover(Z,x)∩cover(B,x)|。对每个新增 B 角色 j∈cover(B,x)\cover(Z,x)，收到的 B 份额券密度恰为

\[
\Lambda_{j,x}
 =\frac{\sum_{i\in cover(Z,x)\cap cover(B,x)}\theta_i
       +\frac b{b+1}\sum_{i\in cover(Z,x)\setminus cover(B,x)}\theta_i}{z}
\le L\left(1-\frac{z-r}{z(b+1)}\right)\le L.
\tag{STATIC-EXACT}
\]

因为 common 行 d_i=b，而 actual-only 行 d_i=b+1；新增 recipient j 不属于实际覆盖者，i≠j 自动满足。若 B 丢失至少一个实际覆盖者，则有上述定量严格缺额。

一个直接接合是：若同一 B 的既有 recipient j 请求保留逐客户密度≤L，且其支持只在 fresh 客户 B_j\C 及 own-intersection 客户 B_j∩S_j，则它与 STATIC-CAP 输出的 actual-new 客户支持互不重叠；两者共同费用仍≤L u_j(B)。**这给同一叶的 fresh / own-intersection / static-new 请求一份共同钱包。**

尚未证明的是原初始化和所有 whole-profit 重采样能持续维持这个支持合同。若已有请求已经占用 actual-new 份额，便可能与 STATIC-CAP 冲突；不能再领一次同一列容量。各个 B 的上界也没有相同实际钱包的共同总和控制。
