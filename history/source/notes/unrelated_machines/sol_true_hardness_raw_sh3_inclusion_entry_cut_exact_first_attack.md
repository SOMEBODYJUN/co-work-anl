# 包含图原端三阶矩入口切：独立 Exact-first 攻击记录

日期：2026-10-18。审者：sol_true_hardness（6.1sol max）。仅 scratch；不改仓库。

## 1. 实际读取范围与判断

本轮实际全文读取且核 hash 的唯一候选材料是
`sol_raw_sh3_inclusion_entry_cut_exact_v1.md`，SHA256
`0b8815af7ded08ed5fd85efdf06c10691b683aa54c66ed1caa4b61377b77c41d`。
冻结本记录前没有读取该候选作者 Proof、作者 audit/code/output 或 global 后续推导。此前本审者审过另一份 ancestry 必要系统；这里不将其结论或辅助变量当作依赖，而从本候选的原 assignment endpoints 重新给出全部推导。没有核对外部论文、原文 hierarchy 定理或新颖性。

**结论：在所列完整原矩阵和 raw SH3 假设下，未发现核心数学 fatal。**
入口切、CONFIG(1) 证书、全原 jobs 上界、固定多项式 shrink 的渐近以及显式输入的位复杂度都可独立重构。下文给自足证明。需要保留的措辞边界是：系统在 §2 首先对有理 T 定义；§4 固定实数 delta 的数值结论成立，若要直接谈实数 T 的同一系统，应作自然的实参数定义，或用较大的有理阈值和单调性解释。此为参数表述澄清，不破坏算法或任何实际 OPT 结论。

## 2. 原输入与全部计数

沿用 Exact 的 q,m,N,C,K,G,d1,d2。q 是正的四倍数，故 q>=4；m>=100q。
每个 q 集 S 有 C 个 2q 超集，每个 2q 集 W 有 K 个 q 子集，所以双计数给 NC=GK。
原机器数为 2N+G。selector h、全部 Nd1 枚 f、全部 Gd2 枚 e 均存在。
每枚 f 有一 home 加 C 个 unit heads，每枚 e 有一 home 加 K 个 unit heads，故原有限条目数恰为

    N + Nd1(1+C) + Gd2(1+K).

d1,d2 是真实 job 数，不是二进制需求的免费展开。后续证明从未删去未选 U/B 的原 jobs，也没有要求 inactive rows 不外送。

## 3. raw M3 中可合法使用的 unit 容量提升

以下所有变量均是原 job 的实际有限 assignment endpoints。Boolean/one-hot 等式按 Exact 允许的次数使用。

任意同一物理行的两个不同 unit endpoints x,y，在 T<2 的合法 CONFIG 中不能同时出现。因此同一行 CONFIG first/second compatibility 给

    L(xy)=0.

M3 的索引含次数至多三的单项式；Boolean 约化给 L((xy)^2)=L(xy)=0。PSD 的零范数列性质于是给

    L(xy p)=0  (deg p<=3).

下面实际只需 deg p<=2；没有把无条件二阶零值免费当成任意阶条件零值。

若 t 是次数至多二的正 Boolean 单项式，V 是同一物理行若干 unit endpoints 的和，则

    0 <= L(tV) <= L(t).                                      (3.1)

左边逐项使用 deg(tx)<=3 和 M3：L(tx)=L((tx)^2)>=0。
右边取次数至多三的多项式 p=t(1-V)。展开平方、用 t^2=t，以及上一零范数性质消掉 V^2 中所有不同 unit-pair 后，得到

    0 <= L(p^2) = L(t)-L(tV).

因此 (3.1) 是本 raw 系统的后果，未添加 canonical activity、ancestor 或 export<=activity 约束。它也适用于只取某个 incoming-unit 子族的 V。

## 4. 从原负载平方 localizers 重建两层质量

固定一个 S，记 A=h→U_S，a=L(A)>0。令

    X_jW = [f_S,j 在 B_W],
    F_SW = sum_j X_jW,
    alpha_W = L(A F_SW)               (W⊃S),
    Y_WlR = [e_W,l 在 Z_R],
    E_WR = sum_l Y_WlR,
    beta_WR = L(A F_SW E_WR)          (W⊃S,R⊂W).

F/E 是端点和，不另造变量。alpha、beta 非负：展开后分别是二次、三次正单项式的 L 值。

U_S 的原 one-hot 身份给

    load_U = A + 1 - (sum_W F_SW)/d1.

在负载 localizer 中取 p=A（deg 1），用 A^2=A，得到

    sum_W alpha_W >= delta d1 a.                            (4.1)

对任意 B_W，令 F_W 为该行全部 incoming f unit endpoints 的和，D_W 为该行全部 e 的所有 Z-export endpoints 的和。完整原 e-one-hot 给

    load_BW = F_W + 1 - D_W/d2.

对每个 X_jW，在其 B_W 负载 localizer 中取 p=A X_jW（deg 2）。原始乘积最高次数五，处于合同内。约化平方后，因 X_jW 是 F_W 的一个 unit endpoint，§3 的零范数性质给

    L(A X_jW F_W)=L(A X_jW).

所以 L(A X_jW D_W)>=delta d2 L(A X_jW)。累加该 S 的全部原 f jobs，得到

    sum_(R⊂W) beta_WR >= delta d2 alpha_W.                  (4.2)

同一 U_S 可以向多个 W 外送；这里恰是对所有这些不同原 f endpoints 求和，未把它们误当一条祖先路径或另设 one-hot。

## 5. bad 计数和所有 good terminals 的联合容量

对 W⊃S，将 R⊂W 按 |R∩S|<q/4 与否分类。
由于 |S|=|W\S|=q，该 W 的 bad R 数恰为

    sum_(j=0)^(q/4-1) binom(q,j) binom(q,q-j)
    = sum_(j=0)^(q/4-1) binom(q,j)^2 = M.                    (5.1)

对每个 j，用 (3.1) 取 t=A X_jW、V=E_WR，再累加 j，得

    beta_WR <= alpha_W.

故 (4.2) 给

    sum_(good R⊂W) beta_WR >= (delta d2-M) alpha_W.           (5.2)

全局 good q 集是 |R∩S|>=q/4 的全部 R⊂[m]，其数恰为 H。关键是每个这样的物理 Z_R 只能付一次预算。
固定一个 R 和它的一枚原 incoming e endpoint y=Y_WlR。用 (3.1) 取 t=A y、V=F_SW，给

    sum_j L(A X_jW y) <= L(A y).

对所有 W⊃S、R⊂W 及 l 求和，再扩展到 Z_R 的全部 incoming e endpoints，并用 (3.1) 取 t=A，可得

    sum_(W⊃S,R⊂W) beta_WR <= L(A) = a.                     (5.3)

这是共同原 terminal 行的容量，包含不同 W、同一祖先 S 的全部项；没有按 W 重复收取 terminal 预算。若若干项实际上不可达，它们没有对应原 endpoint，根本不进入和式。

若 c=delta d2-M<=0，则目标切左边非正而 H>=0，立即成立。
若 c>0，合并 (4.1)、(5.2)、(5.3)，得

    delta d1 c a <= c sum_W alpha_W
                 <= sum_(good R,W) beta_WR <= H a.

除以 a>0，正是 delta d1(delta d2-M)<=H。这里必须先分 c 的符号，不能把 (4.1) 直接乘负数后保持方向。

所有 selector masses 非负且由原 h-one-hot 求和为一，故至少一个 a>0。严格反向数值不等式因此确实切掉整个指定 raw SH3 系统。每个实际完整 T-schedule 的 Dirac functional 满足这些条件，故同样推出 OPT>T。

## 6. CONFIG(1) 与完整实际上界的独立核验

给 U_S 的行分布：概率 1/N 取单件 h，概率 1-1/N 取该行全部 d1 枚 home f。每枚 f 的每个 B-head marginal 设为 1/(NC)。
定义

    b = K d1/(NC).

每个 B_W 的 Kd1 个 incoming f endpoints 各取 singleton 配置概率 1/(NC)，余下概率 1-b 取该行全部 d2 枚 home e。
每枚 e 的每个 Z-head marginal 为 b/K。于是每个 Z_R 全部 incoming e 的质量和为

    C d2 b/K = d1 d2/N <= C/(N s1 s2) <= 1.

Z_R 对每枚 incoming e 取其 singleton 配置对应 marginal，剩余概率取空配置。又 b<=1/(Ns1)<=1。所有这些行配置负载均<=1；全部原 job 的 home/head marginals 求和恰一：f 是 (1-1/N)+C/(NC)，e 是 (1-b)+K b/K，h 是 N/N。因此这是完整 CONFIG(1) 证书。T<1 没有任何行配置能覆盖 h，故 CONFIG optimum 恰为一。

实际完整上界则选任意 S、一个 W⊃S、一个 R⊂W。只把一枚 f_S,j 放 W、一枚 e_W,l 放 R，h 放 S，其余每枚原 f/e 均留原 home。三类特殊行峰为 2-1/d1、2-1/d2、1；其余 home 行为一。这精确核回 Exact 所列上界，不是假定强端有完整 branching forest。

## 7. 四个有限二项式界与 floor payment

对 H/C 的第 j 项，有

    binom(m-q,q-j)/binom(m-q,q)
    = product_(i=0)^(j-1) (q-i)/(m-2q+1+i) < (1/98)^j.

H 中 j>=q/4>=1，所以用 sum_j binom(q,j)=2^q，得

    H/C < 2^q (1/98)^(q/4) = (8/49)^(q/4).

binom(q,j) 在 j<=q/4 不减，且二项分布的单项质量<=1 给
binom(q,q/4)<=4^q/3^(3q/4)。结合中心项 K>=4^q/(2q+1)，得

    M/K <= (q+1)(2q+1)(256/729)^(q/4).

另外 binom(n,q)>= (n/q)^q，n=m-q>=99q，且 K<=4^q，给 K/C<=(4/99)^q；中心项为整行最大项直接给 K>=4^q/(2q+1)。四界均成立。

固定 a0,b0>=0（避免和 selector mass a 混名）、delta>0，统一考虑 s1<=q^a0、s2<=q^b0。指数增长保证充分大 q 时两次 floor 的原商都>=2，因此

    d1 >= C/(2K s1),       d2 >= K/(2s2).

再取 q 大到 M/K<=delta/(4q^b0)，则

    delta d2-M >= delta K/(4s2),
    delta d1(delta d2-M) >= delta^2 C/(8s1s2)
                            >= delta^2 C/(8q^(a0+b0)) > H.

最后严格号由第一条指数界得到。所有选择均对允许的 s1,s2 同时成立，并对所有 m>=100q 成立。d1,d2 一起趋无穷；实际峰<=2 且对每个固定 delta 最终>2-delta，故实际 OPT 趋二。CONFIG 仍恰一，而这里指定的 raw SH3 在每个固定 T<2 最终不再可行；三个不同结论没有混用。

本轮另用独立 Python 整数/Fraction 临时表达式检查 q=4,8,16,32,64、m=100q、s1=s2=1：四界都成立，T=3/2 的严格切都触发。只计算了这些二项式整数，没有构建那些巨大的原矩阵、求 SDP、读取作者代码或跑作者软件；此有限算术不是上述一般证明的前提。

## 8. 位复杂度、实参数与 attachment 范围

验证完整显式矩阵的行、job 身份、集合菜单、1/d 时间和全部条目，耗时可按实际输入列表/矩阵长度计。binomial、H、M 的运算仅需 O(poly(m,q)) 次标准整数运算；m<=N 已被显式机器数支付，q<=m，整数位数也由显式输入规模支付。严格切可清分母作整数比较，依赖 T 的位长，不按 1/delta 的数值循环。d1,d2 的原 job 数已显式列出。故所述纯数值 FAIL/UNKNOWN 检查是总位多项式，并不需要 exact SDP feasibility 后端。若验证不在承诺类，不能仅凭该式对任意矩阵报 FAIL。

固定实数 delta 的不等式渐近证明只用实数比较。若严格遵守系统最初仅定义有理 T 的写法，可选有理 T' 满足 2-delta<T'<2：最终在 T' 已不行，实际 OPT>T'>2-delta。自然把系统定义扩展到实 T 后，可行性也随 T 单调：负载 localizers 增加非负的 (T'-T)L(p^2)，CONFIG(T) 包含于 CONFIG(T')，因此同样不行。算法输入仍只承诺有理 T。

在可实现的固定 rho=q/m>0、rho<=1/100 的整数序列上，m/q 是常数，binomial 计数的对数与 q 同阶，所以显式 inclusion graph 大小的对数为 Theta(q)。m/q 无界时不能升级成这个结论；polylog shrink 也只有已核到固定 q 次幂的部分被 §7 覆盖。

若外接 source 仅增加进入 U 的原 unit arrivals，保留本 f/e home jobs 及原菜单，则可把 §4 的 A 换成任意一枚有正 mass 的该类原 unit endpoint。U 的其他 unit-arrival 项在相应正单项式条件下非负，丢掉只弱化入口需求；B/Z 的证明不变。必须另证正 mass 及 source 全 jobs 完成。这里既没有给任意 source 免费找到正入口，也没有给一般 decoder、近二计算困难性或 native hierarchy 反例。

冻结判断：上述限定合同数学上可重构，无 standing fatal；实 T 的定义域措辞宜明确。作者 Proof/code 尚未释放给本审者，本记录不代签其内容或运行。
