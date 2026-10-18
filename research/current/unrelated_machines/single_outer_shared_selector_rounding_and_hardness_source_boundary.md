# 单外层共享选择器的舍入与困难性源边界

本文的用途是排除一种具体的近二困难性源：只有一个外层 group、每个 home 有自己的 singleton helper、所有 fallback 资源共享但与 homes 分离的显式 normalized-flat 结构。在这个结构域内，可以从 typed 菜单本身构造确定性的总位多项式时间 $13/8$ 近似。因此，若一个 NP-hard 源的真实 YES 为 makespan 一、真实 NO 为 $2-\delta>13/8$，它不能在 $P\ne NP$ 下被多项式归约到这个结构域。

这是结构域的反面归约障碍。本文不提供一般 unrelated-machines 算法，也不否定一般 unrelated-machines 的近二困难性。福利舍入工具是经典机制的精确应用，不主张其技术新颖性。

## 1. 两个正式结果及身份字段

本文只保留以下两个正式 ID。后文的物理恒等式、singleton closure、CDF 福利估计和源排除均是证明引理或直接推论，不另立资产。

### `UM-SINGLE-OUTER-PRIMITIVE-SA1-EPS2-4-v1`

| 字段 | 完整内容 |
|---|---|
| Object | 接收给定完整 primitive-SA1 点的条件舍入。 |
| Domain | 第 2 节的显式单外层 typed normalized-flat 菜单及其完整普通 UM 矩阵。 |
| Assumptions | 给定有理数 $0<\epsilon\le1$，以及第 4 节 plain common primitive-SA1 LP 的一个有理可行点。所有原 primitive 和补条件都使用同一对称二阶数组。无需 PSD、unit-FSLP 或真实联合分布。 |
| Quantifiers | 存在一个固定确定性算法，对每个这样的 $Q,\epsilon$ 及每个给定有理可行点，均满足下面的输出保证。 |
| Input | 显式 typed $Q$、$\epsilon$ 和该可行点的完整有理编码；不给 actual optimum。 |
| Output | 所有 groups 的不交实际 allocation，最低质量至少 $\epsilon^2/4$；以及逐一执行全部原 jobs 的完整 schedule，$C_{\max}\le2-\epsilon^2/4$。 |
| Complexity | 对上述全部输入编码的总位多项式时间；不以 $1/\epsilon$、分母数值或隐式状态数为循环界。 |
| Dependencies | 普通 flat allocation/schedule 对应；singleton closure；一次共同条件化；uniform-winner 福利舍入及精确条件期望；home 恢复。本文第 3、5、6 节重构全部分支。 |
| Objections | 不把分别条件化的点拼起来；不声称二阶点有真实联合状态；不丢弃低质量 helpers；零质量/零 marginal 不做除法；所有未选状态 jobs 仍执行。 |
| Status | 数学证明在本文完整重构。作者是旧给定点引理的知情作者，本文不是对该旧引理的独立盲审。本页最终版本的实际复核范围另见审查记录；不据此认证旧审查历史。 |
| Software | None：本文未提供该全流程的端到端程序或运行证书。 |
| External review | 无本文的外部同行评审声明。 |

### `UM-SINGLE-OUTER-TYPED-13-8-v1`

| 字段 | 完整内容 |
|---|---|
| Object | 从 typed $Q$ 本身运行的 $13/8$ 完整普通 UM 近似算法。 |
| Domain | 与上项相同，结构呈现随输入显式给出；不是从任意矩阵中识别该呈现的问题。 |
| Assumptions | 仅第 2 节的结构和 binary-rational 输入；使用标准确定性有理 LP 可行性算法。无需给定 relaxation 点、optimum、精度参数或任何 actual allocation oracle。 |
| Quantifiers | 存在一个固定确定性总位多项式算法，对每个该域的 typed $Q$，输出全部原 jobs 的 assignment，$C_{\max}\le(13/8)\operatorname{OPT}(P(Q))$。 |
| Input | 显式 typed $Q$，等价地生成矩阵与其完整结构呈现。 |
| Output | 一个原机器、原有限端点上的完整 schedule；没有 dropped jobs、逻辑侧约束或未付费辅助组。 |
| Complexity | 恰好 11 次显式 plain rational LP 查询，至多一次有理条件期望舍入；总位多项式，次数不依赖输入分母或支持宽度。 |
| Dependencies | 第 3–5 节的物理恒等式、必要 LP 与共同 fallback 引理；第 7 节的经典 CDF-max 福利后端；第 8 节固定有理余量；第 9 节 11 步搜索。旧 $\epsilon^2/4$ 常数不是新后端常数的证明。 |
| Objections | LP 可行不等于实际 allocation；FAIL 只表示精确不可行；不额外加入不必要的 U/PSD 条件；可行下端点可超过真实 $V$；所有 jobs、零 incidence、重复索引及位成本由第 10 节处理。 |
| Status | 本文知情重构所读的新 Exact 和作者 Proof；不是独立审查。数学证明自足；本页最终版本的独立复核范围另见审查记录。 |
| Software | None：本文没有 11-LP 主算法的端到端实现或运行认证。已有 32-case 小审计只属于 CDF 后端，不能认证 LP 生成、搜索和完整 job 恢复；本文未重跑它。 |
| External review | 无本文的外部同行评审声明。 |

本轮曾有一个较弱的 $7/4$ 导出，保留为 scratch 历史，不在本文重复登记，也不将其算法或软件状态转记给 $13/8$。

## 2. 完整物理 typed 域

外层只有一个 group $M$，有非空有限的 indexed states $a$。状态 $a$ 的正系数 home 集合为

\[
 \{g_{a,j}:j\in J_a\},\qquad
 w_{a,j}>0,\qquad \sum_{j\in J_a}w_{a,j}=1.
\]

所有 $g_{a,j}$ 在不同 $(a,j)$ 间都物理不同。每个 $(a,j)$ 有一个 helper $H_{a,j}$：它的 own state 是系数一的 singleton $g_{a,j}$，其余 indexed states 是在有限资源集 $B$ 上的任意显式 normalized 非负有理向量。$B$ 与全部 homes 不交。不同 helpers、不同 outer states 的 fallback 支持可以任意共享。helper 可以没有 fallback state，但它总有 own state。没有别的 groups，也没有缺少自己 home 的额外 auxiliary core。

所有 groups 的每个 indexed state $s$ 都有系数 $p_{gsu}\ge0$，其总和为一；每个 indexed state/resource 对至多列出一个 incidence。相同 fallback 向量的不同索引仍是不同 states。所有给定零 incidence、重复 state 索引和未使用资源都保留。外层不同 states 的 home 分离假设仍须满足；不能用重复索引消除这项物理要求。

由 $Q$ 生成普通 unrelated-machine 矩阵 $P(Q)$：

| 原对象 | 原机器资格与处理时间 |
|---|---|
| 每个 indexed state $(g,s)$ | 一台不同的 private machine $m_{gs}$。 |
| 每个资源 $u$，包括未使用资源 | 一台资源机器 $R_u$。 |
| 每个 group 的一个 selector $S_g$ | 在该 group 的所有 $m_{gs}$ 上时间一，其余为 $\infty$。 |
| 每个列出的 incidence 的一个 job $J_{gsu}$ | 在 $m_{gs}$ 上时间 $p_{gsu}$，在 $R_u$ 上时间一，其余为 $\infty$。 |

每个 selector 是同一原 job 在其所有状态间选择；不是每个 state 另造一个 selector。每个 incidence 也是一个独立不可拆的原 job。所有 jobs 必须执行，模型中没有额外的资源容量、状态一致性或守卫占位约束。下文的资源不交性来自 allocation 或实际负载 $C<2$，不是附加给原调度问题的逻辑条件。

设 groups 数为 $G$，indexed states 总数为 $S$，列出的 incidences 总数（含零）为 $I$，资源数为 $U$。生成矩阵有 $S+U$ 台机器、$G+I$ 个 jobs、$S+2I$ 个有限资格单元；生成完整矩阵或相应显式有限资格表的成本均为多项式。

## 3. allocation 与全部原 jobs 的精确值恒等式

实际 allocation 为每个 group 给出一个资源 bundle，所有 bundles 两两不交。group $g$ 的值是

\[
 v_g(X)=\max_s\sum_{u\in X_g}p_{gsu},\qquad
 V=\max_X\min_g v_g(X).
\]

有限菜单保证最大值可取到，且 $0\le V\le1$。记 $x=\operatorname{OPT}(P(Q))$，则

\[
 \boxed{1\le x\le2,\qquad x=2-V.} \tag{1}
\]

selector 的单位处理时间给出 $x\ge1$。把所有 incidence jobs 留在其 private machines、每个 selector 放在任一自己的状态机器上，给出 $x\le2$。

若实际 allocation 最低值为 $v$，每个 group 选一个达到其值的 indexed state。将该状态 bundle 中的正 incidence jobs 输出到对应资源机器，其余所有 incidence jobs 留 private，selector 放到该状态的 private machine。选中 private load 为 $2-v_g\le2-v$，每个未选 state 的完整 private load 为一，每台资源机器至多一个单位 job。所有零 incidence jobs 可直接留在其 private 零端点。因此得到完整 schedule $C\le2-v$。

反向，任何完整 schedule 若 $C<2$，同一资源机器不可能容纳两个单位 incidence jobs。每个 group 的 selector 选定唯一状态机器；该状态的 private load 是二减去它向资源端输出的原系数质量，所以这批输出的值至少为 $2-C$。这些选中状态的输出资源两两不交，给出实际 allocation。未选状态的输出 jobs 可全部还原 private，其完整负载仅一。由此在 $x<2$ 时得到恒等式；在 $x=2$ 时，前一方向和 $V\ge0$ 也迫使 $V=0$。

本节没有把 selector 预先固定到某个给定状态，也没有只优化条件 schedule。

## 4. 显式 plain primitive-SA1 LP、必要性与 FAIL

对一个测试阈值 $0<\epsilon\le1$，每个 indexed state 设 binary primitive $A_{gs}$，每个列出的 incidence（含零）设 binary claim primitive $Z_{gsu}$。base rows 为

\[
 \sum_s A_{gs}=1,\qquad
 0\le A_{gs},Z_{gsu}\le1,\qquad Z_{gsu}\le A_{gs}, \tag{2}
\]
\[
 \sum_{g,s}Z_{gsu}\le1\quad(u\in U),\qquad
 \sum_u p_{gsu}Z_{gsu}\ge\epsilon A_{gs}\quad(g,s). \tag{3}
\]

这些是 allocation 的 LP rows，不是改动原 jobs 的调度条件。

设 primitives 总数为 $N=S+I$。建立一个公共数组：一阶矩 $\mu_F$，对称二阶矩 $Y_{FE}=Y_{EF}$，对角 $Y_{FF}=\mu_F$，常数矩为一。对每个 base row $h\ge0$ 及每个同一原 primitive $F$，明确加入

\[
 L(h)\ge0,\qquad L(hF)\ge0,\qquad L(h(1-F))\ge0. \tag{4}
\]

base equality 使用等式。线性化只用 $L(F)=\mu_F$、$L(FE)=Y_{FE}$ 和 binary 对角替换。所有 boxes、非负 rows、gates 都在这个生成过程内。记所得 LP 为 $\mathcal R_\epsilon(Q)$。它有 $O(N^2)$ 个变量，行数是 base rows 数的 $O(N)$ 倍，系数为原有理数、$\epsilon$ 或小整数；不存在隐含的指数状态枚举。

算法调用标准确定性有理 LP 可行性程序，得到一个多项式编码长度的精确有理可行点，或精确报告 **FAIL = LP 不可行**。这里的 FAIL 不是浮点程序超时、数值困难或未找到整数解。

实际 allocation 若最低值至少 $\epsilon$，选择各 group 的见证状态、其正 bundle claims，并将其余 claims（含零）置零。这个零一向量及其 rank-one moments 满足全部 (2)–(4)。因而

\[
 \mathcal R_\epsilon(Q)\text{ FAIL}\quad\Longrightarrow\quad V<\epsilon. \tag{5}
\]

LP 可行绝不被解释为一个实际 allocation。新算法使用的拒绝含义只有 (5)。不加入额外 unit-FSLP、PSD 或更高矩条件；这些额外条件不能从旧给定点结论反推成所有实际阈值的必要证书。

这个 LP 也对阈值单调。quality row 在 base、乘 $F$、乘 $1-F$ 时，被 $\epsilon$ 乘的量分别是 $\mu_A,Y_{AF},\mu_A-Y_{AF}$，它们由同一非负 box rows 均非负。因此降低 $\epsilon$ 保留一个既有可行点。11 步算法不需要在零处取得可行点。

## 5. singleton closure 与一次共同 fallback 条件

先证明一个结构引理。对任意 helper 的 own singleton，记 state primitive 为 $A$，其唯一正 claim 为 $Z$。quality row $Z-\epsilon A\ge0$ 乘 $1-Z$，利用 $Z^2=Z$ 和 $\epsilon>0$，给出 $Y_{AZ}\ge\mu_A$。box $A\le1$ 乘 $Z$，再结合 gate，得到

\[
 \mu_A\le Y_{AZ}\le\mu_Z\le\mu_A.
\]

所以 $\mu_A=\mu_Z=Y_{AZ}$。对任意同一原 primitive $F$，gate $A-Z\ge0$ 分别乘 $F$ 和 $1-F$，其一阶 slack 为零，故

\[
 \boxed{Y_{AF}=Y_{ZF}\quad\text{对所有原 }F.} \tag{6}
\]

这只是同一 degree-two 数组内的恒等式，不是再条件化一次，也不调用 triple moments。

取任一 marginal $\rho>0$ 的外层状态 $a$，所有条件量统一由该一个 primitive $A_{Ma}$ 的矩行除以 $\rho$ 得到。写该状态的 positive homes 权重为 $w_j$，其 conditional home claims 为 $b_j$。对应 helper 的 conditional fallback state masses、claims 记为 $\alpha_{js},\zeta_{jsu}$，并设 $f_j=\sum_s\alpha_{js}$。由同一次条件下的所有 base rows 及 (6)，有

\[
 \sum_jw_jb_j\ge\epsilon,\qquad f_j\ge b_j,\qquad 0\le f_j\le1, \tag{7}
\]
\[
 0\le\zeta_{jsu}\le\alpha_{js},\qquad
 \sum_up_{jsu}\zeta_{jsu}\ge\epsilon\alpha_{js},\qquad
 \sum_{j,s}\zeta_{jsu}\le1\quad(u\in B). \tag{8}
\]

最后一项是同一个 joint fractional packing：原资源条件容量先包含全部 groups，再删去其他 helpers 的非负 claims。它不是对每个 helper 各找一份可行 fallback 然后相加。若 $\alpha_{js}=0$，所有对应 claims 也为零。

其 weighted fractional welfare 满足

\[
 W_f=\sum_{j,s,u}w_jp_{jsu}\zeta_{jsu}
 \ge\epsilon\sum_jw_jf_j\ge\epsilon^2>0. \tag{9}
\]

## 6. 旧给定点版本：uniform winner 导出 $\epsilon^2/4$

对本行每个 helper $j$，独立选择 fallback state $s$，概率为 $\alpha_{js}$，或以剩余概率 $1-f_j$ 选择算法的 empty option。选到正 marginal 状态后，以概率 $\zeta_{jsu}/\alpha_{js}$ 请求资源 $u$。不同 helpers 的随机选择独立；这是一套新造的舍入随机变量，不是把旧矩当作真实联合分布。empty option 不是新增物理状态。

在每个资源的请求者中均匀选一个。给定某 helper 的状态及其对 $u$ 的请求，其他请求者数 $T$ 的期望至多一。整数不等式

\[
 \frac1{1+T}\ge1-\frac T2
\]

保证其赢得该资源的条件概率至少 $1/2$。若该实际临时 fallback allocation 中 helper 值为 $Q_j\in[0,1]$，empty option 的值取零，则

\[
 \mathbb E Q_j\ge\frac12\sum_{s,u}p_{jsu}\zeta_{jsu}
 \ge\frac\epsilon2f_j,
 \qquad \mathbb E\sum_jw_jQ_j\ge\epsilon^2/2. \tag{10}
\]

这一步只保证 weighted welfare。它可以精确去随机化：按固定顺序选择 helper states/empty。在每个资源和任意部分 state choices 下，写 $r_{ju}$ 为请求概率，$m_{ju}=w_j\mathbb E[p_{j,s,u}\mathbf1\{j\text{ 请求 }u\}]$ 为 weighted value-request mass。令 $D_{-j,u}(t)$ 为其余 helpers 请求数的分布，其 Bernoulli 卷积递推是 $D_{new}(t)=(1-r)D_{old}(t)+rD_{old}(t-1)$。该资源的 conditional expected welfare 精确为

\[
 \sum_j m_{ju}\sum_{t=0}^{H-1}\frac{D_{-j,u}(t)}{1+t}, \tag{10a}
\]

其中 $H$ 是本行 helpers 数。所有参数从 (7)–(8) 和已经固定的选项直接算出。扫描下一个 helper 的所有正概率选项，取不低于当前期望的一项。states 固定后，各资源直接交给 eligible chosen-state helpers 中 $w_jp_{jsu}$ 最大者，逐资源不低于剩余请求实验的期望。于是确定性地得到

\[
 W:=\sum_jw_jQ_j\ge\epsilon^2/2. \tag{11}
\]

令 $\tau=\epsilon^2/4$，Good 为 $Q_j\ge\tau$ 的 helpers，总 home 权重为 $z$。由于 $Q_j\le1$，

\[
 \epsilon^2/2\le W\le z+\tau(1-z),\qquad
 z\ge\frac{\epsilon^2}{4-\epsilon^2}\ge\tau. \tag{12}
\]

保留 Good 的不交 fallback bundles，把其各自 homes 给 outer group；本行其余 helpers 和所有其他 outer states 的 helpers 一律回自己的不同 homes。fallback 资源与全部 homes 不交，故这是真实的全组 allocation。outer 值至少 $z\ge\tau$，Good 值至少 $\tau$，其余 helpers 值一。第 3 节恢复全部原 jobs，得到第一个正式结果。

这里使用的是 uniform-winner 实现与 count DP。不能把下面 CDF-max 的较强常数归给这个旧后端。

## 7. 新证明引理：经典 CDF-max 后端的 $5/8$ 福利

从同一 (7)–(9) 出发，仍独立抽取 helper state 和请求，但将每个请求资源给分数 $w_jp_{jsu}$ 最大的请求者。对固定 $u$ 和正 score level $d$，令

\[
 \beta_j(d)=\sum_{s:\,w_jp_{jsu}\ge d}\zeta_{jsu},
 \qquad t(d)=\sum_j\beta_j(d)\le1.
\]

跨 helpers 的独立性给出

\[
 \Pr(\max\text{ score}\ge d)
 =1-\prod_j(1-\beta_j(d))
 \ge1-e^{-t(d)}\ge(1-1/e)t(d). \tag{13}
\]

最后一步是 $1-e^{-t}$ 在 $[0,1]$ 上的凹性弦界。对各资源的有限 score levels 求和，得到

\[
 \mathbb E W\ge(1-1/e)W_f>\frac58\epsilon^2. \tag{14}
\]

严格不等式用 $e>1+1+1/2+1/6=8/3$ 和 $W_f\ge\epsilon^2>0$。这是证明用的常数界；程序不比较无理数。

精确 CDF 去随机化如下。对一个资源，排好原有理正分数

\[
 0=d_0<d_1<\cdots<d_m.
\]

在任意部分 state choices 下，它的 conditional expected maximum 精确等于

\[
 \sum_{k=1}^m(d_k-d_{k-1})
 \left[1-\prod_j(1-r_j(d_k))\right]. \tag{15}
\]

未固定 helper 的 $r_j(d_k)$ 为 $\beta_j(d_k)$；固定为正 marginal 状态 $s$ 时为 $\mathbf1[w_jp_{jsu}\ge d_k]\zeta_{jsu}/\alpha_{js}$；empty 时为零。把 (15) 对资源求和，扫描下一 helper 的正概率选项并最大化 conditional expectation。平均恒等式保证不会下降；部分固定之后不需要继续假设请求总概率仍至多一。

全部 states 固定后，直接把每个资源给分数最大的 eligible chosen-state helper，或在全无正分数时空置。它逐资源支配剩余请求实验。得到真实不交 fallback bundles，且确定性地满足

\[
 \boxed{W=\sum_jw_jQ_j>\frac58\epsilon^2.} \tag{16}
\]

所有 CDF levels、state choices、乘积和比较都是显式有理数运算。此引理仍只保证 weighted welfare；必须经过下一节才能保证每个 group 的最低值。

## 8. 固定有理质量直线与全组恢复

设

\[
 a=\frac{13}{8},\qquad b=\frac{10}{8},\qquad d=\frac1{256},
 \qquad q=a\epsilon-b+d.
\]

当 $q>0$ 时，$q\le97/256<1$，且

\[
 \frac58\epsilon^2>2q-q^2. \tag{17}
\]

证明：令 $q_0=a\epsilon-b$。直接展开

\[
 \frac58\epsilon^2-(2q_0-q_0^2)
 =\frac{209\epsilon^2-468\epsilon+260}{64}\ge\frac1{64}. \tag{18}
\]

分子在 $[0,1]$ 上递减，最小值为一。又 $q>0$ 给出 $q_0>-d$，所以从 $q_0$ 加上 $d$ 至多将 $2q-q^2$ 增加 $2d+d^2<1/64$。这证明 (17)。

令 Good 为 $Q_j\ge q$ 的 helpers，其总 home 权重为 $z$。若 $z\le q$，则

\[
 W\le z+q(1-z)\le2q-q^2,
\]

与 (16)–(17) 矛盾。因此 $z>q$。保留 Good 的 fallback bundles、把它们的 homes 给 outer，其余全部 helpers 回自己的 homes，如第 6 节一样得到所有 groups 最低值至少 $q$。由于 $q>0$，Good 中不会有 empty option，留下的每个 helper 都使用原 fallback state。对应完整 schedule 满足

\[
 C\le2-q. \tag{19}
\]

这是新 CDF 后端的给定点推论；不是把旧 $\epsilon^2/4$ 的输出常数改名。特别地，若给定点在 $\epsilon=1$ 可行，可取 $q=97/256$，得到实际完整 schedule $C\le415/256$。没有给定点的全输入算法仍须自行求解下一节的 LP。

## 9. 11 次 LP 的 $13/8$ 全实际 OPT 算法

算法的输入只有 typed $Q$。先生成第 4 节全部 LP rows 的索引与系数表达式，然后执行：

1. 设 $l=0,h=1$，不保存任何零阈值点。
2. 恰好重复 11 次：测试 $\mathcal R_\epsilon(Q)$，其中 $\epsilon=(l+h)/2$。若可行，令 $l=\epsilon$ 并保存该有理点；若 FAIL，令 $h=\epsilon$。
3. 令 $q=al-b+d$。若 $q\le0$，输出所有 incidence jobs 留 private、selectors 任取本组状态的完整 baseline schedule。若 $q>0$，使用保存的点，经第 5、7、8 节输出完整 schedule。

这里没有第十二次 $\epsilon=1$ 查询，也不调用旧历史算法。每次阈值为正，至多 11 个二进制小数位。

由 $V\le1$ 初始化，且 FAIL 只可能在 $\epsilon>V$，始终有 $V\le h$。无论可行下端点是否超过真实 $V$，结束时都有

\[
 h-l=\eta=\frac1{2048},\qquad l\ge V-\eta. \tag{20}
\]

若 $q\le0$，则

\[
 aV-b\le-d+a\eta=-\frac{51}{16384}<0.
\]

故 $V<10/13$，baseline 的 $C\le2<(13/8)(2-V)$。

若 $q>0$，必有 $l>0$ 且保存了实际有理可行点。第 8 节适用，而

\[
 q\ge aV-b+d-a\eta>aV-b,
 \qquad d-a\eta=\frac{51}{16384}>0.
\]

结合 $2+b=2a$、(1) 与 (19)，

\[
 C\le2-q<a(2-V)=\frac{13}{8}\operatorname{OPT}(P(Q)). \tag{21}
\]

因此报告的非严格 $13/8$ 近似保证对所有 typed 输入统一成立，包含真实 OPT 恰好为一、LP 有 gap、无正阈值点被保存等边界。不需要知道 OPT，也不需要输入分母格点或趋零精度搜索。

## 10. 全部原 jobs、零、索引与总位成本

第 8 节的实际 allocation 保留 Good 的不交 fallback bundles，其余每个 helper 都有自己的不同 home，outer 使用 Good 的 homes。$B$ 与全部 homes 分离，所以没有隐含的跨层占位冲突，也没有丢弃某个低值辅助组。

最后明确生成原 job assignment：每个 selector 去自己的见证 state machine；只输出该选中 state 分给它的正 incidence jobs；所有其他 incidence jobs，包括所有未选 state payload、全部零 jobs，留在各自原 private machines。每个原 job 恰好出现一次，每次赋值都是原有限端点。未使用 machines 和资源保留。相同状态向量的不同索引不合并。所有选中 private loads、未选 private loads 和 unit-resource loads 已由第 3 节统一计入。

输入位长记为 $L$。矩阵规模及 LP 行列数是显式 $G,S,I,U$ 的多项式。11 次测试的阈值位长为常数；系数的总位长因此对 $L$ 多项式。标准有理 LP 返回的精确可行点可以取为多项式编码长度；这里一阶与二阶矩由 box lifts 有界，也可用 basic feasible point 的行列式位界说明这一点。

条件化只除以一个正的有理 marginal，正 marginal 再小也只增加多项式位长，不成为循环次数。零 outer marginal 不选；零 fallback marginal 的 claims 全零，不除以零。uniform-winner 的有限 count DP、CDF 的有限 score products 和 conditional expectation 扫描都只使用多项式个原输入及 supplied-point 有理因子。逐式约分或统一公共分母均给出多项式中间位长；分母数值、$1/\epsilon$ 和 $1/\rho$ 均不作为迭代界。

因此第一个正式结果是对 typed $Q$、$\epsilon$ 与 supplied point 总位长的多项式时间；第二个正式结果由于 LP 自行产生多项式位长的点，是对 $Q$ 位长本身的多项式时间。两个输入合同不同，不能由旧给定点结论直接假设第二个已有 feasible-point oracle。

## 11. 对真实近二困难性源的直接推论

固定任意 $0<\delta<3/8$。考虑承诺问题，其输入是第 2 节的 typed $Q$，且完整普通矩阵满足二者之一：

\[
 \text{YES}:\ \operatorname{OPT}(P(Q))=1,
 \qquad
 \text{NO}:\ \operatorname{OPT}(P(Q))\ge2-\delta>13/8.
\]

运行第 9 节算法并精确计算它输出的原 schedule makespan。YES 时输出至多 $13/8$；NO 时任一完整可行 schedule 都至少 $2-\delta>13/8$。用 $13/8$ 比较即可确定性多项式区分。这里的 NO 是对所有原 jobs、任意原 selector 选择的真实全局 OPT；不是只对一个给定 selector、一个给定 LP 支撑或一个条件状态证明坏负载。

所以，若某个 NP-hard 语言可通过总位多项式归约生成这样的显式 typed 输入，并具有以上真实 YES/NO 含义，复合该算法就得到 $P=NP$。在 $P\ne NP$ 下，这个单外层结构不能承担上述近二源。这个结论不声称 YES/NO 数值实例本身不存在，也不为一般 UM 建立或否定任何近二困难性。

如果源本来还为全部实例提供 $\mathcal R_1(Q)$ 的完整可行点，则第 6 节已经给绝对 $7/4$ 上界，第 8 节的新后端还给绝对 $415/256$ 上界；这类 supplied-point 障碍是更直接的实际 schedule 结论，不应与没有 supplied point 的全输入算法混为同一量词。

适用范围到此为止。多个 outer groups 同时选择 states 时，逐个条件化的 fallback 点未必能合成一个共同可行点；额外没有 own home 的辅助 groups 也不能在恢复步骤自动回家。本文不对这些域给出结论，不把尚未审查的多外层嵌入加入证明，也不把隐式高深度菜单自动当作一个已证明的困难性源。

## 12. 来源、作者读后与审查边界

本 canonical 是知情作者的自足新重构。作者实际全文阅读了以下冻结来源：

| 来源对象 | SHA256 | 本文用途 |
|---|---|---|
| `sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md` | `da4897a966e8b5e10299622c5f93d67b115f859d1ae8fc77bd29f8f7ce0aa571` | 旧给定完整点的物理域、$\epsilon^2/4$ 版本及完整原 jobs 恢复。 |
| `one_outer_full_primitive_sa1_rounding_exact_v1.md` | `7364055e2c13a8962b5a022f959721014fb6219465dbe0340676521ac9437eac` | 旧给定点输入合同与共同 primitive-SA1 系统。 |
| `one_outer_normalized_flat_13_8_approximation_exact_v2.md` | `81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69` | 新 typed $Q$-alone、固定全输入算法的量词合同。 |
| `one_outer_normalized_flat_13_8_author_proof_v2.md` | `2a6af63654c9ec36a3a83da47b4cdb95065aa298012369cf7c87dbfa5f226eaf` | root 作者的 CDF-max、固定有理直线和 11-bisection 证明。 |

作者是旧给定点引理的作者，并已读新作者 Proof；因此本页不能充作新 Exact 的独立盲审。root 对来源的实际读后、其他重构记录、本文今后的全文复核及任何外部同行评审是不同证据层，本文不相互代认。本文未读取 unknown `negative_hardness_work/`，未改动原来源、repo 或既有审查记录。最终当前版本的实际读取顺序、覆盖范围及登记状态见[独立审查记录](../../reviews/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary_review.md)，不能从本页的来源表自行推定。
