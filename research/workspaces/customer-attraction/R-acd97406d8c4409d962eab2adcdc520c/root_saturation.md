# 根保底近饱和时的真实末位交换

状态：本轮解析推导，coverage_exchange 已独立重构核验；尚未完成共享资产入库、外审或新颖性核对。一般 Q-CAG-HALF 仍 OPEN。

## 精确 Claim：B6-ROOT-NEAR-SATURATION-v1

**Objects / Domain / Quantifiers.** CAG-MODEL 的任意有限单位客户、有限非空共同目录、任意整数 m≥2，以及任意完整历史依赖纯 SPE。重复主题、空主题、零客户、所有离轨平局都保留。令 r 为实际根玩家最终收益，W 为实际根福利，K=max_{D∈S}|D|，E=mr−K。对每个最大主题 C（|C|=K）和每个合法主题 D，

\[
E\ge0,\qquad
m|D\setminus C|+|D\cap C|\le K+(m-1)^2E.\tag{1}
\]

因此

\[
\operatorname{OPT}_m\le(2-1/m)K+(m-1)^2E.\tag{2}
\]

**Dependencies.** 仅用根的真实偏离、该偏离分支末玩家的真实最佳回复、全目录大小上界 K，以及整数负载的均分收益；不冻结根偏离后的后继，不假定匿名平局，不使用未证明的全局桥。

**Evidence.** 下方完整解析证明；`root_saturation_audit.py` 另枚举有限客户分支作实现检查，有限枚举不是一般证明。coverage_exchange 独立重构了任意 D 版本；独立审查文件待写。

**Counterevidence / objections.** 未知致命异议。系数锐性未证明；(2) 在 E 大时可很弱，不能宣称一般半覆盖已证。

## 证明

在根实际改选 C，随后全部玩家沿给定原策略继续。记这个真实分支的行动为 A₁=C,A₂,…,Aₘ=L，客户最终负载 c_x，首人分支收益 v=Σ_{x∈C}1/c_x。根最优性给

\[
K/m\le v\le r.
\]

令 ε=r−K/m=E/m，定义 C 上的总覆盖席位缺额

\[
d=\sum_{x\in C}(m-c_x)
=\sum_{j=2}^m|C\setminus A_j|,
\quad d_L=|C\setminus L|.
\]

对 x∈C，若 c_x<m，则 c_x≤m−1，故

\[
v-K/m
=\sum_{x\in C}\frac{m-c_x}{mc_x}
\ge\frac{d}{m(m-1)},
\quad d\le m(m-1)\varepsilon.\tag{3}
\]

每个 |A_j|≤K=|C|，所以 |A_j\C|≤|C\A_j|。因此末行动的外部客户数≤d_L；前 m−1 个行动在 C 外的总关联数≤d−d_L。记末玩家在这个分支的真实收益为 t。比较 t 与首人分支收益 v 时，C∩L 的项相消。C\L 的负载≤m−1，得到

\[
t\le v+|L\setminus C|-\frac{|C\setminus L|}{m-1}
\le v+\frac{m-2}{m-1}d_L.\tag{4}
\]

在该真实末节点改选任意 D。对 D∩C 的每位客户，最终负载至多 m，收益至少 1/m。对 D\C，记前 m−1 人负载为 k_x。整数 k≥0 满足 k/(k+1)≤k/2，故

\[
\sum_{x\in D\setminus C}\frac1{1+k_x}
\ge|D\setminus C|-\frac12\sum_{x\in D\setminus C}k_x
\ge|D\setminus C|-\frac{d-d_L}{2}.
\]

末位最佳回复与 (4) 给

\[
|D\setminus C|+\frac{|D\cap C|}{m}
\le v+\frac d2+\frac{m-3}{2(m-1)}d_L.\tag{5}
\]

若 m≥3，d_L≤d 和 (3) 将右侧控制为

\[
v+\frac{m-2}{m-1}d
\le\frac Km+\bigl[1+m(m-2)\bigr]\varepsilon
=\frac Km+(m-1)^2\varepsilon.
\]

若 m=2，前缀只有 C，d=d_L；(5) 右侧恰为 v≤K/2+ε，同样等于所需表达式。乘以 m 即得 (1)。

对任意 m 个比较主题 D₁,…,Dₘ，令 I=C∩(∪D_j)，R=(∪D_j)\C。对 (1) 求和并使用 |R|≤Σ|D_j\C|、|I|≤Σ|D_j∩C|，得

\[
m|R|+|I|\le mK+m(m-1)^2E.
\]

于是

\[
|R|+|I|\le K+(1-1/m)|I|+(m-1)^2E
\le(2-1/m)K+(m-1)^2E.
\]

取最优比较元组即得 (2)。K=0 时所有量为零；证明无需除以 K 或 W。

## 后果与真实范围

1. **等大主题分离。** 若 D 也是最大主题，则
   |D\C|≤(m−1)E=m(m−1)(r−K/m)。因而不同最大主题迫使根保底严格松弛。
2. **根饱和刚性。** E=0 时所有最大主题具有相同覆盖；真实根改选 C 后所有后继都选覆盖 C（因为 (3) 的 d=0 且主题大小≤K）。末位比较给每个 D 的 m|D\C|+|D∩C|≤K。
3. **一个无人数/目录上界的条件半覆盖区。** 每名实际玩家在自己的真实节点改选最大主题均能保证 K/m，故 W≥K。若
   E≤K/[m(m−1)^2]，则 (2) 给 OPT_m≤2K≤2W。更一般可直接检查 (2) 的右侧是否≤2W。这是新增条件版本，不替代 Q-CAG-HALF。
4. **m=1。** 原半覆盖直接由根最优性得到 W=K=OPT₁；(1) 不用于此情形。

## 剩余研究义务

本机制只使用一个根偏离分支及其末位。一般情形的 E 没有足够小的上界；需要让更多真实分支共同支付 E，或找到完全不同的全局机制。不能把排除旧437行坏点等同于该松弛已被加强到半覆盖，更不能当作原一般命题已证。
