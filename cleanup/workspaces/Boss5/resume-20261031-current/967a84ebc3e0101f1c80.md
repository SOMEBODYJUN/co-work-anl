# 七态原作业星：只据 Exact 独立重构全局二次检验

2026-10-18，scratch 冻结前完整重构记录。审查对象为 `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-EXACT-v1`。结论限于所给局部星，不是递归定理、实际 near-two gap 或复杂性困难性。

## 1. 阅读边界与审查身份

本轮只实际全文读了 statement-only 文件：

`sol_seven_state_star_global_quadratic_exact_v1.md`

SHA256 `939a9b12b0dc8d74aa9809f816140b8569d6c6d091ee6fd809492256d1a0b477`；5586 bytes，106 lines。读取时逐字节计算并核对该 hash。

在以下重构完成和冻结前，没有打开作者 Proof、代码、JSON，也没有读取作者此前的七态数学 Proof 或五点评估插值消息，没有向 global 索取机制。root 已告知它是 actual OPT=1 的局部构件，并要求攻击任意全局 degree-two q。

已有背景必须披露：我已知并实际研究 raw SH3 条件流、原 unit-row pair 零向量、共同 M2、diluted raw K2 真 law 及其升阶障碍；也刚审过另一个 growing-depth 候选给定 first 表的零支撑阻断。因此这是对这个新 Exact 的独立重构，不是对整个研究方向的盲审。

以下没有依赖任何未释放作者推导。没有程序执行证据，也不认证作者软件；全部结论由本文显式计算给出。

## 2. 完整原输入与参数合法性

整数 d、s 均为正偶数，2≤s≤d/2。记

\[
\eta=s/d,\quad h=s/2,\quad T=1+\eta,\quad
p=\eta^3/1000,\quad u_0=4p(1-\eta),\quad
e=4/5-p-u_0.
\]

所以 d≥4，0<η≤1/2，h 是整数。机器为 u,v,z_1,…,z_d。原 unit job R 只能放 u 或 v，两个时间均为一；每枚不同原 job j_l 只能在 v 用时 1/d 或在自己的 z_l 用时一。其余端为无穷。总共 d+2 台机器、d+1 枚原 jobs、2(d+1) 个有限条目，无拆分、无附加约束。

R 的所有资格时间均为一，故实际 OPT≥1。把 R 放 u，全部 j_l 放 v，得到两个负载一、其余负载零，因此实际 OPT=1。

定义 C=1_{R→v}、Y_l=1_{j_l→v}、H=Σ_lY_l。四类原端点正好为 C、1−C、Y_l、1−Y_l；不存在漏排的原 job。

P 取下列七个 (C,H) 类别，然后在每类均匀抽 H 个不同索引置 Y_l=1：

| (C,H) | 质量 |
|---|---:|
| (1,d) | p |
| (1,0) | 1/20 |
| (1,h) | 1/20 |
| (0,0) | 1/20 |
| (0,h) | 1/20 |
| (0,d/2) | u_0 |
| (0,d) | e |

由于 p≤1/8000，u_0≤4p，故 e≥4/5−5/8000=0.799375>0.79。所有质量严格正，总和为一。每个样本指定每枚原 job 的恰一个有限端，是一个真实完整 assignment。

负载是 load_u=1−C、load_v=C+H/d、load_zl=1−Y_l。唯独 (C,H)=(1,d) 时负载 v 为二，概率为 p>0；其余六类负载 v 均≤T。

## 3. 全部原变量上的共同矩与 M3

对全部有限原端点变量定义 L(f)=E_P f。真实完整 assignment 上 Boolean、每 job one-hot 及全部有定义的乘子等式逐样本成立。

对任意次数≤3 的多项式 r，L(r²)=E_P r²≥0。因此以全部原次数≤3 单项式为标签的一个共同 M3 PSD。这里不要求有效支持枚举，也没有调用 SDP finder；这是显式概率 law 的直接 Gram 证明。

## 4. 任意全局 degree-two q 的严格降维

取系数任意实数、在全部原有限端点上的总次数≤2 多项式 q。将互补端点代成 1−C、1−Y_l，并用 Boolean identities 化简，必可写成

\[
q(C,Y)=a+bC+\sum_l u_lY_l+\sum_l v_lCY_l
          +\sum_{l<j}w_{lj}Y_lY_j.\tag{1}
\]

这一步包含 u、v、所有 z_l 的变量；没有把 q 限于 v 行，也没有假设 q 本身对称。

令 U=Σ_lu_l，V=Σ_lv_l，W=Σ_{l<j}w_lj。固定 (C,H) 并令 x=H/d，由均匀子集得到

\[
\mathbb E[Y_l\mid H]=x,\qquad
\mathbb E[Y_lY_j\mid H]
=\frac{d x^2-x}{d-1}\quad(l\ne j).
\]

因此条件均值 f_C(x)=E[q|C,H] 具有形式

\[
f_C(x)=A+BC+Dx+ECx+Fx^2.\tag{2}
\]

其中 f_0、f_1 的二次项系数 F 完全相同。这是原次数二的关键限制：式 (1) 中没有 CY_lY_j 这种次数三项。

对每个 (C,H) 类别，Jensen 给 E[q²|C,H]≥f_C(H/d)²。在唯一负余量类别 C=1,H=d，所有 Y_l 都为一，没有剩余随机性，所以 q 的值恰为 f_1(1)。非对称部分在这个坏类别不会留下额外负项。

## 5. 独立得到的五点评估恒等式

置 τ=h/d=η/2，B_*=1/τ=2/η，A_*=B_*−1。由式 (2) 中两支共享相同二次项，直接展开可得

\[
f_1(1)= -A_*f_1(0)+B_*f_1(\tau)
       +A_*f_0(0)-B_*f_0(\tau)+f_0(1).\tag{3}
\]

例如先以 f_1(0)、f_1(τ) 外推到一，余项为 F(1−τ)；用 f_0 的三点评估消去同一个 F，就得到式 (3)。这只是我从 Exact 独立推出的恒等式，不是读取作者五点消息后的复述。

上述五个状态在 P 下都有严格正质量及严格正负载余量。相应的“质量乘余量”权重为：

| 取值 | 权重 w_i | 插值系数 |
|---|---:|---:|
| f_1(0) | η/20 | −A_* |
| f_1(τ) | η/40 | B_* |
| f_0(0) | (1+η)/20 | A_* |
| f_0(τ) | (1+η/2)/20 | −B_* |
| f_0(1) | eη | 1 |

令 E_+(q) 是 P 的六个正余量类别对 E[(T−load_v)q²] 的全部贡献。Jensen 保证这五项的 Σ_i w_i f_i²≤E_+(q)；第六个 C=0,H=d/2 类别只会增加 E_+。

加权 Cauchy 给

\[
f_1(1)^2\le S\sum_iw_if_i^2\le S E_+(q),\tag{4}
\]

其中

\[
S=A_*^2\left(\frac{20}{\eta}+\frac{20}{1+\eta}\right)
 +B_*^2\left(\frac{40}{\eta}+\frac{20}{1+\eta/2}\right)
 +\frac1{e\eta}.
\]

利用 A_*≤B_*=2/η、e>79/100、η≤1/2，逐项估计

\[
S\le\frac{240}{\eta^3}+\frac{160}{\eta^2}
       +\frac{100}{79\eta}
\le \frac{320+25/79}{\eta^3}
<\frac{321}{\eta^3}.\tag{5}
\]

所有常数均不依赖 d、s、全局 q 的非零系数个数或 monomial 维数。

## 6. 全局二次负载矩阵 PSD

坏类别的余量为 T−2=−(1−η)，故由 (4)–(5) 及 p=η³/1000，

\[
\begin{aligned}
L[(T-\operatorname{load}_v)q^2]
 &=E_+(q)-p(1-\eta)f_1(1)^2\\
 &\ge\left(1-\frac{321}{1000}\right)E_+(q)
 =\frac{679}{1000}E_+(q)\ge0.\tag{6}
\end{aligned}
\]

这是相对于正余量能量的 dimension-free 控制，不声称在有 Boolean/one-hot 零向量的原 monomial 基上有常数最小特征值。

其他原机器更直接：逐样本 T−load_u=η+C>0、T−load_zl=η+Y_l>0。故它们对同一个任意全局 q 都有非负期望。

因此全部机器以全部原次数≤2 monomials 为标签的负载局部化矩阵都 PSD，且用的是同一个 L。式 (6) 同时处理跨机器、跨 jobs、任意实系数和非对称 q，没有仅检对称子块后遗漏其他块的问题。

## 7. K_v 是合法 CONFIG(T) 分布

给定 Exact 的 K_v 六类是

\[
\begin{array}{c|c}
(C,H)&\text{质量}\\\hline
(1,s)&p/\eta\\
(1,0)&1/20+p-p/\eta\\
(1,h)&1/20\\
(0,0)&1/20+u_0/2\\
(0,h)&1/20\\
(0,d)&e+u_0/2.
\end{array}
\]

p/η=η²/1000≤1/4000，所以第二个质量至少 1/20−1/4000>0。其余质量都正，六项之和为 1/5+p+u_0+e=1。

当 C=1，H 仅取 s、0、h，负载分别是 T、1、1+η/2；当 C=0，H≤d，负载≤1。故每个支持集合都是真正由原 jobs 组成的合法行配置。

## 8. K_v 的全部原 first/pair 一致性

P 与 K_v 都对 j_l 交换对称。其 v 行原 first/pair 完全由四个统计量

\[
E(C),\quad E(H),\quad E(CH),\quad E[H(H-1)]\tag{7}
\]

决定：EY_l=EH/d，ECY_l=ECH/d，EY_lY_j=E[H(H−1)]/[d(d−1)]（l≠j），对角 pair 由 Boolean first 决定。

从 P 到 K_v 的变化只有两组：先以 C=1 将质量 p 的 H=d 换为质量 p/η 的 H=s，并把质量差补在 H=0；再以 C=0 将质量 u_0 的 H=d/2 换为 H=0、d 各质量 u_0/2。

前一组保持 E(C)，因为质量差被补在相同的 C=1。又 (p/η)s=pd，所以它保持 E(H)、E(CH)。后一组也保持 E(H)，并不改变 E(C)、E(CH)。

对最后一个统计量，K_v−P 的精确差为

\[
\begin{aligned}
&\frac p\eta s(s-1)-pd(d-1)
 +\frac{u_0}{2}d(d-1)
 -u_0\frac d2\left(\frac d2-1\right)\\
&=-p d^2(1-\eta)+\frac{u_0d^2}{4}=0.\tag{8}
\end{aligned}
\]

最后用了 u_0=4p(1−η)。因此 (7) 全部相同，覆盖 v 行所有原端点的一阶、所有二阶与对角。

u 行只有原 R 端点，z_l 行只有原 j_l 端点。它们的真实 Bernoulli 边际支持空配置/单个 unit job，因 T>1 全合法，并自动匹配各自行 first/pair。这里只建立逐行配置 law 与 L 的 first/pair agreement，不声称这些 K_i 的支持能共同实现一个全局 T 调度 law。

## 9. 全部矩的显式有理生成与总位复杂度

每个给定原 endpoint monomial 先去重复。如果它对同一原 job 同时要求两个互补端点，则矩为零。否则它指定可选的 C 值、a 个不同 Y_l=1 及 b 个不同 Y_l=0。给定某个七态类别 (C,H)，该事件的精确条件概率为

\[
\frac{(H)_a(d-H)_b}{(d)_{a+b}},\tag{9}
\]

其中 (x)_r 为下降阶乘；不可能事件取零，空乘积取一。类别的 C 若不匹配则贡献零。对七类加权即得 L 矩。对 K_v 用其六类同样生成；其他 K_i 是 Bernoulli。

对固定次数 D，式 (9) 的阶乘长度≤D，概率参数及结果的 numerator/denominator 位长均为 O_D(log d)，每项可用确定性整数运算精确得到。原变量数是 2(d+1)，全部次数≤D monomials 个数为 O_D(d^D)。因此完整生成共同 degree≤D 矩、特别是 M3 的 degree≤6 entries，具有显式原输入位长的多项式总运行时间、输出规模与位长。

负载二次局部化条目为 L[(T−load_i)ab]，deg a、deg b≤2，总次数至多五。负载是至多 d+1 个原指标的有理线性组合，所以可直接用已生成的矩作多项式多个有理运算。所有行 first/pair 的生成也同样为多项式规模。

这里的时间下界已支付 d 枚显式原 jobs；不声称关于 log d 的多项式时间。均匀子集的指数支持无需展开，也未在复杂度论证中隐含做此展开。没有优化、未知调度、精确 SDP 可行性或条件 oracle。

## 10. 结论与保留边界

Exact 的全部陈述均获得上述自足重构，未发现 fatal。尤其同一真实 assignment law 的共同 M3、所有全局 degree-two q 负载检验、全部原行 CONFIG(T) first/pair 与总位复杂度兼容；P 的坏样本概率 p>0 不会被这些条件切掉。

这只是实际 OPT=1 的明确局部噪声构件。u 没有额外 payload，z_l 没有内部 jobs；把它们接入更大共享网络会改变负载与全局 q，本文没有为这些新增约束付款。没有递归接线证明、共同全局预算、真实 near-two gap、sound decoder、一般算法或一般困难性结论。

审查状态：本记录是只据所列 Exact 的独立证明/攻击，具有已披露的相关旧背景；未读作者 Proof，未读或运行作者软件，未外审。冻结后的作者读后比较须另记，不能回写本记录的阅读顺序。
