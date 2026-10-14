# 加权多项式拥塞：奇数环下界与剩余缺口

## 精确模型与当前结论

本页采用 [WC-TARGET v1](../weighted_congestion_frontier/MODEL.md)：有限玩家、有限资源、任意正实权，任意非空有限多资源策略族，资源费用为非负系数且次数至多整数 d 的多项式。玩家成本为所用资源费用之和；α-PNE 使用弱不等式 C_i(s)≤αC_i(t_i,s_{−i})。全类阈值 a_*(d) 是所有普遍存在因子的下确界。

本轮独立审查后的下界为：对每个整数 d≥2，存在一个合法有限游戏，**在下列因子本身也没有纯近似均衡**：

\[
 E_d=\frac{d}{(d+1)d^{1/(d+1)}-d}.
\]

因此 a_*(d)≥E_d=(1−o(1))d/ln d。先前冻结的较简形式 a_*(d)≥d/(ln d+2) 对所有 d≥4 仍成立。结合已核对的文献存在保证 a_*(d)≤d，尚有对数因子的缺口；**WC-TARGET 仍 OPEN，增长阶未确定**。

状态是完整一般证明、两项独立重构和定义级精确核验；外部同行评审未记录。文献检索确认与已核对基线的严格比较，但不认证全球优先权。奇数环的抽象反匹配机制已有前例；本页的数学内容是它在正权多项式拥塞模型中的实现、参数闭环和次数预算。

## OC-INTERFACE-v1：资源实现与全部纯状态

取奇数 m≥3，索引模 m。Hub i 权重 u_i>0，有二进制策略 h_i。Cohort i 有 n_i≥1 个独立玩家，每人权 v_i>0，各自选 l_ij∈{0,1}。这里 cohort 玩家可重于其自身 hub。

建立不同资源 A_i^0,A_i^1，费用 a_i z^{k_i}；每个 cohort 玩家有 B_ij^0,B_ij^1，费用 b_i z^d。a_i,b_i>0，整数 1≤k_i≤d。策略精确为

\[
 H_i(h)=\{A_i^h\}\cup\{B_{i-1,j}^{h}:1≤j≤n_{i-1}\},\qquad
 L_{ij}(l)=\{A_i^l,B_{ij}^{1-l}\}.
\]

固定 α>1，记

\[
 x_i=v_i/u_i,\quad t_i=v_i/u_{i+1},\quad
 q_i=a_i u_i^{k_i},\quad p_i=b_i u_{i+1}^d,
\]

\[
 \begin{aligned}
 N_i&=(1+x_i)^{k_i}-α(n_i x_i)^{k_i},&
 M_i&=α(1+n_i x_i)^{k_i}-1,\\
 P_i&=α(1+t_i)^d-t_i^d,&
 Q_i&=(1+t_i)^d-α.
 \end{aligned}
\]

若每个 i 都满足

\[
 \boxed{q_iN_i>p_iP_i,\qquad n_i p_i Q_i>q_{i+1}M_{i+1},}\tag{1}
\]

则所有纯状态均存在严格 α-改善。

**证明。** 若某 cohort 玩家与自己的 hub 同位，其当前主资源负载至少 u_i+v_i，当前侧资源负载至少 v_i。偏离后的主资源负载至多 n_i v_i，侧资源负载至多 u_{i+1}+v_i。于是当前成本减 α 倍偏离成本至少 q_iN_i−p_iP_i>0。n_i v_i 已包含刚迁入的玩家；该比较覆盖部分同位的群组和 n_i=1。

剩下的状态中，所有 cohort 玩家均与自身 hub 反位。奇数环必有 h_i=h_{i+1}。Hub i+1 当前独占其主资源，并与每个 incoming cohort-i 玩家共享侧资源；偏离后与全部自身 cohort 玩家共用主资源、独占 incoming 侧资源。其精确成本差为 n_i p_i Q_i−q_{i+1}M_{i+1}>0。独占侧资源的正基线也已计入，不能把 Q_i 的 −α 换成 −1。两类状态穷尽全部纯状态。∎

## 闭环权重与正系数

正比率 x_i,t_i 可由权重实现，当且仅当 ∏x_i=∏t_i。必要性直接相乘；充分性取 u_0=1，递推 u_{i+1}=u_i x_i/t_i，令 v_i=u_i x_i，乘积恒等式保证闭环。

若 N_i,Q_i>0，则 M_i,P_i>0。此时 (1) 有正系数解，当且仅当

\[
 G=\prod_i\frac{n_iN_iQ_i}{M_iP_i}>1.\tag{2}
\]

证明及显式构造如下。令 K_i=n_iN_iQ_i/(P_iM_{i+1})。消去 p_i 得 q_{i+1}<K_iq_i，相乘证明必要性。反之选择 δ>1 使 δ^{m−1}<G；取 q_0=1，q_{i+1}=K_iq_i/δ，0≤i≤m−2。前 m−1 个比较严格成立，最后一个由 G/δ^{m−1}>1 成立。取

\[
 p_i=\tfrac12\left[\frac{q_{i+1}M_{i+1}}{n_iQ_i}+\frac{q_iN_i}{P_i}\right],
 \quad a_i=q_i/u_i^{k_i},\quad b_i=p_i/u_{i+1}^d.
\]

两个区间端点严格有序，所有系数均为正。若输入为有理数，可从 δ=2 开始反复令 δ←1+(δ−1)/2，直到 δ^{m−1}<G；必有限终止且保持有理。所有构造都是有限游戏，不使用极限游戏、连续策略或数值可行性容差。

## OC-AMPLIFIER-LIMIT-v1：线性重置给出一般下界

对整数 d≥1 和 0<t<1，定义

\[
 H_d(t)=\frac{(1+t)^d+t^{d+1}}{1+t(1+t)^d}.
\]

**Exact Statement。** 对每个满足 1<α<H_d(t) 的 α，存在上述有限游戏没有 α-PNE；若 α,t 有理，权重和费用系数也可全为有理数。因而 d≥2 时 a_*(d)≥sup_{0<t<1}H_d(t)。这不声称上确界处由同一个游戏取得。

令 y=(1+t)^d，P=αy−t^d，Q=y−α，B=Q/P。P>0，且

\[
 α<H_d(t)\iff Q>tP>0\iff B/t>1.
\]

选择有限整数 R≥5、R≡1 mod 4，使

\[
 t^R<1/(4α),\qquad (B/t)^R>8α^2.\tag{3}
\]

这样的 R 存在，因为 0<t<1<B/t。令 m=(R+1)/2，x=t^R，n=⌊1/(2αx)⌋。权重及主资源次数为

\[
 \begin{aligned}
 u_0&=1,&v_0&=t^R,&n_0&=n,&k_0&=1,\\
 u_i&=t^{2(m-i)},&v_i&=t^{2(m-i)-1},&n_i&=1,&k_i&=d\quad(1≤i<m).
 \end{aligned}
\]

因此所有 t_i=t，x_0=t^R，x_i=1/t（i≥1），权重闭环精确成立。除一个线性重置主资源外，所有费用均为次数 d 的正单项式。

由 (3)，1/(2αx)>2，故

\[
 \frac1{4αx}<n≤\frac1{2αx},\quad
 N_0=1+x−αnx>1/2,\quad 0<M_0=α(1+nx)−1<α.
\]

于是 A_0=nN_0/M_0>1/(8α²x)。每个其余节点精确满足 N_i=t^{−d}Q、M_i=t^{−d}P，因此它对 (2) 的贡献为 B²，重置节点贡献为 A_0B。故

\[
 G=A_0B^{2m-1}=A_0B^R>
 \frac{(B/t)^R}{8α^2}>1.
\]

正系数构造和全状态证明遂完成。玩家数 n+m+(m−1) 可非常大，模型没有人数或位长上限；没有多项式时间或小实例承诺。

当 d≥4，取 t=ln d/d。由 ln(1+t)>t−t²/2，且 sup_{d≥1}(ln d)²/(2d)=2/e²<ln2，得 y>d/2。因此

\[
 H_d(t)>\frac1{t+1/y}>\frac{d}{\ln d+2}>1.
\]

这证明先前冻结身份中“每个 d≥4，存在游戏没有 d/(ln d+2)-PNE”的结论，且端点严格被排除。

## OC-AMPLIFIER-ENVELOPE-v1：有限次数的显式强化

这是本轮新 corollary，保留上一节原 claim 的身份。对每个 d≥2，设 t_d=d^{1/(d+1)}−1。函数 g(t)=t+(1+t)^{−d} 的导数为 1−d(1+t)^{−d−1}，二阶导数为正。其在 [0,1] 上的唯一最小点是 t_d∈(0,1)；g'(0)<0 也给 1/g(t_d)>1。

直接代入得

\[
 \frac1{g(t_d)}=E_d=\frac{d}{(d+1)d^{1/(d+1)}-d}.
\]

又

\[
 H_d(t)=\frac1{g(t)}+\frac{t^{d+1}}{1+t(1+t)^d}>\frac1{g(t)},
\]

所以 1<E_d<H_d(t_d)。上一节以 α=E_d 构造游戏，证明不存在 **E_d-PNE**。进一步，第二项小于 (t/(1+t))^d<2^{−d}。H_d 在闭区间 [0,1] 连续，两端值均为 1，最大值在内部取得，故

\[
 E_d<\max_{0<t<1}H_d(t)<E_d+2^{−d}.
\]

Taylor 展开令 L=ln d，得到 (d+1)exp[L/(d+1)]−d=L+1+O(L²/d)，于是 E_d∼d/ln d。这里的 envelope 是 **这项重置放大构造所证明的下界**，不是全类门槛的上界，也不证明该资源拓扑的最优因子。

## 与文献精确参数上确界的严格比较

主来源 [CGGPW, Theorem 1, equation (3)](https://arxiv.org/html/2002.07466v3) 给出两列重轻族的精确参数上确界 F_d。仅与论文展示的 Ω(√d/ln d) 比较不足以排除原参数上确界已更强；以下从原公式独立给一个足够的全域 ceiling。

设原公式两个商的最小值为 f>1，写 x=nw，E=(1+w)^d，p=(1+w)^k，T=(1+x)^k，r=x^k，q=βE，θ=(w/(1+w))^d≤1。w=0 或 β=0 的第一商至多 1，故这里只需 w,β>0。第一商至少 f、第二商至少 f 分别给

\[
 fT−1≤nq,\qquad fr+(f−θ)q≤p.
\]

相乘并用 T≥1、θ≤1 得 (f−1)²≤np/T≤n；第二式又迫 x<1+w，即 (n−1)w<1。第一商至多 E，因此 ln f≤dw。若 f≥4，则

\[
 n−1≥(f−1)^2−1=f(f−2),\qquad f(f−2)\ln f<d.
\]

由 f(f−2)≥f²/2 和 ln f>1，得到 f<√(2d)。因此整个原公式 F_d≤max{4,√(2d)}。这个粗界不声称锐性；它足够独立证实新的 d/ln d 下界严格超过 **原参数全域**，并不依赖公屏中更细的 sharp-envelope 定理。

明确地，对每个 d≥256，d/(ln d+2)>√(2d)≥4。证明：√(d/2)−ln d−2 在 d>8 严格增加；d=256 时 √128>11、ln256<8，差为正。故新旧下界在所有这些次数严格分离。更细的有限次数与全球优先权另行审查。

## OC-LIGHT-FORCING-EXACT-v1：失败边的真实均衡

本轮独立 reviewer 进一步证明：**给定所有 q_iN_i>p_iP_i，游戏没有 α-PNE 当且仅当每个 n_i p_iQ_i>q_{i+1}M_{i+1}。**

必要性如下。所有 cohort 反位时，同 hub 边上的 cohort 当前成本 C_0=q_i(n_ix_i)^{k_i}+p_i(1+t_i)^d，偏离成本 C_1=q_i(1+x_i)^{k_i}+p_it_i^d。light 条件恰为 C_1>αC_0，所以反位 light 稳定；若相邻 hubs 反位，其当前侧费用更低、偏离侧费用更高，仍稳定。相邻 hubs 反位的 hub 偏离差为 −q_{i+1}M_{i+1}+n_i p_i[1−α(1+t_i)^d]<0。若某 hub 条件失败，则把这条边设为奇数环唯一同位边，其余边交替，令全部 cohort 反位；该状态所有偏离均满足均衡弱不等式，包括失败边恰为等号的情况。充分性就是全状态证明。

这给一个严格失败机制，但 **未证明无 light-forcing 前提的整个拓扑上界**。

## OC-INTERFACE-BARRIER-v1：机制的次数限制

在 (1) 的证书范围，允许侧次数 D_i 也在 1,…,d 变化。令 z=α^{1/d}，L=z−1。N_i>0 给 n_ix_i<(1+x_i)/z，因此 x_i<1/L；Q_i>0 给 t_i>L。权重闭环推出

\[
 \prod_i n_i<\frac{\prod_i(1+x_i)}{z^m\prod_i x_i}<L^{−2m}.
\]

又 M_i≥(α−1)(1+x_i)^{k_i}，N_i<(1+x_i)^{k_i}，且 P_i−(α−1)Q_i=(1+t_i)^{D_i}−t_i^{D_i}+α(α−1)>0。因此

\[
 G<\frac{\prod_i n_i}{(α−1)^{2m}}<[(α−1)(α^{1/d}−1)]^{−2m}.
\]

G>1 必须满足 (α−1)(α^{1/d}−1)<1，进而 (α−1)lnα<d。所以同一证书机制最多达到 (1+o(1))d/ln d；本构造达到相同 leading constant。结合上一节，light-forcing 前提下超过该机制边界会产生真实 α-PNE。该 barrier 不是 a_*(d) 上界。

## 来源、证据与接续

原证明和程序从远端 `wcg/work/R1/e18ff3b3e4` 的冻结 commit `a3f0c7aa977a6e2036df08afb7b66225cf372d42` 逐字节恢复于 [odd_cycle/](../weighted_congestion_frontier/assets/R1/odd_cycle/README.md)。原文件的 pending 标签记录当时阶段；本页记录随后完成的审查，不改写冻结原文。

- [独立状态重构](../weighted_congestion_frontier/assets/R1/odd_ring_audit/state_review.md)：先从策略定义攻击，再读原证明；核查所有混合 group、闭环、strict 边界，并建立失败边均衡 lemma。
- [独立次数和参数审查](../weighted_congestion_frontier/assets/R1/odd_ring_audit/asymptotic_review.md)：重构原增长族、线性重置、显式 E_d 及原文 ceiling。
- [实际文献审查](../weighted_congestion_frontier/assets/R1/odd_ring_audit/literature_review.md)：一手陈述、范围、后续线索和检索限制；未认证世界首次。
- [独立精确程序](../weighted_congestion_frontier/assets/R1/odd_ring_audit/verify_linear_reset.py)与 [实际输出](../weighted_congestion_frontier/assets/R1/odd_ring_audit/linear_reset_verification.json)：七组有理增长参数、六组端点拒绝、原公式有限回归；Decimal 数值仅诊断。
- [定义级状态程序](../weighted_congestion_frontier/assets/R1/odd_ring_audit/verify_state_review.py)与 [输出](../weighted_congestion_frontier/assets/R1/odd_ring_audit/state_verification.json)保存独立资源枚举与实际参数。

一般证明决定无限族结论，有限计算核查实现和索引。零费用和空策略属于 WC-TARGET 的普遍类，但本下界只需其中正成本、两策略子类；无需把所有游戏变成该构造。Truth：上述范围完整内部证明；Value：新无限下界和严格可复用接口；Novelty：未认证全球首次；Mechanism：线性重置累积人数，权重递增 buffer 传输成本差，奇数 parity 保证全状态矛盾；Ambition：全类下界推进，普遍上界与增长阶仍开放。

最有信息价值的下一义务是全类 O(d/ln d) 存在性，或绕开 light-forcing 限制的更强非存在族。同资源多 dense 尺度和跨权重 gluing 的现有势机制障碍只限制相应方法；不能把本页 barrier 当成方法白名单或全类结论。
