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


## 13. 完整局部 law 仍不能直接给 canonical primitive-SA1

本节另立身份 **`UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1`**。前十二节的两个算法及其输入、审查、软件状态不变。本节是给定物理证书的同点提取反例，不是实际 OPT gap；不能据此否定第九节另求 LP 点的算法。

| 字段 | 精确内容 |
|---|---|
| Objects / Domain | 下述完整 ordinary normalized-flat 有理族 $P(Q_c)$，全部原 selector、incidence jobs 和有限端均保留。 |
| Quantifiers | 对每个二进制编码有理数 $0<c<1$，取 $T=1+c$、$\epsilon=1-c$；存在下述同一个明确指定的共同有理矩 functional 及有限 legal row laws。 |
| Exact Statement | 该 functional 满足全部 degree-four Boolean/one-hot、global $M_2\succeq0$、每物理机对所有原全局 affine $q$ 的 raw-load localizer，并与每机同一份 CONFIG law 共享该行全部 Boolean 局部矩；但将 claim 直接定义为 selector 乘 resource-export 后，所得共同 canonical 二阶点不满足 plain primitive-SA1。 |
| Assumptions | 每机 CONFIG load 至多 $T$、总质量一；共同矩只要求 global degree-four 和 $M_2$，不另加任意 global triple/quartic literal 非负。局部 law 相容包括全部本地 degree $\le4$ 及完整 row membership law。 |
| Conclusion | 同一证书的指定 direct canonical pullback 不是第4节 $\mathcal R_\epsilon(Q_c)$ 点；raw slack 的 affine localizer 也不能自动换成下述 activation slack 的 raw-affine localizer。真实 $\operatorname{OPT}(P(Q_c))=1$。 |
| Complexity | 实例与证书维数固定；给定 $c$ 后可确定性按其总位长多项式显式生成全部原矩阵、共同矩和 row laws，不调用 SDP solver。 |
| Dependencies | 完整 flat 矩阵定义、下述自足三位 functional/PSD 证明和逐机 law。无需前十二节的福利舍入或第14节另证的 source-S3 充分桥。 |
| Evidence / Status | 本节的 Exact-first、作者读后、最终实读与有限程序范围分别记于新增接口审查。一般参数由下述代数证明承担，有限重放不能代替它；旧两算法的审查不覆盖本节。 |
| Counterevidence / Scope | 真实 makespan-one witness 明确存在；不排除改点、重新求解、另一种 packing 提取或直接输出好 schedule。增加 global triple literal 非负会切掉本证书。无一般 UM 困难性、外审或新颖性声明。 |
| Related Files | 本页第1–12节及其审查记录；本节 Exact-first、作者读后、最终正文与实际代码范围须在同一专题的审查/证据记录中单独登记。 |

### 13.1 完整普通矩阵和全部原端点

资源 $u,v,r,s,w_u,w_v,w_r,w_s$ 全部物理不同。只有一个 outer $M$ 和四个 helpers；完整显式菜单为

| group | state 0 | state 1 |
|---|---|---|
| $M$ | $u:c, v:1-c$ | $r:1-c, s:c$ |
| $H_u$ | $u:1$ | $w_u:1$ |
| $H_v$ | $v:1$ | $w_v:1$ |
| $H_r$ | $r:1$ | $w_r:1$ |
| $H_s$ | $s:1$ | $w_s:1$ |

每个 listed incidence 均为正，每 state 总和一。outer 的四个 homes 跨所有 state 索引互异；每 home 有 own-singleton helper，四个 fallback 资源与全部 homes 不交，没有别的 groups。按第2节生成完整普通矩阵：每 group 一个 unit selector，在本组两个 distinct private machines 上有资格；每 incidence 一个不可拆 job，在自己的 private 时间原系数、在 exact resource 时间一，其他单元无穷。故有 **18 machines、17 jobs、34 finite endpoints**：10 private、8 resource、5 selectors、12 incidences。没有 guard 或逻辑状态约束。

用三个形式 Boolean bits $b_1,b_2,b_3$ 指定全部原 assignment variables。每个 incidence 的 private 端是其下表 resource 端的补；每组两个 selector 端是同一个原 job。

| group/state | selector 在本 private 的变量 | 本 state incidence 的 resource 端变量 |
|---|---|---|
| $M/0$ | $b_1$ | $u:b_2;\quad v:1$ |
| $M/1$ | $1-b_1$ | $r:1;\quad s:1-b_3$ |
| $H_u/0$ | $1-b_2$ | $u:1-b_2$ |
| $H_u/1$ | $b_2$ | $w_u:b_2$ |
| $H_v/0$ | $0$ | $v:0$ |
| $H_v/1$ | $1$ | $w_v:1$ |
| $H_r/0$ | $0$ | $r:0$ |
| $H_r/1$ | $1$ | $w_r:1$ |
| $H_s/0$ | $b_3$ | $s:b_3$ |
| $H_s/1$ | $1-b_3$ | $w_s:1-b_3$ |

这张表和取补规则给出全部34个原端，没有省略 job。所有端都是 affine literals 或常数，Boolean 与原 job one-hot/exclusivity 是三位 Boolean 商代数中的恒等式，乘至原总 degree 四也成立。

### 13.2 一个共同 global $M_2$ 的自足 PSD

在三位 Boolean 商代数上定义线性 functional $\ell$：

\[
 \ell(1)=1,\qquad \ell(b_i)=\frac3{10},\qquad
 \ell(b_i b_j)=\frac3{80} (i\ne j),\qquad
 \ell(b_1b_2b_3)=-\frac1{160}.
\]

重复位按 Boolean 合并；原共同 $L$ 为先按表 affine substitution 再用 $\ell$。因为各原端 affine，原 degree $\le4$ 的所有矩均已明确指定。这里不把 $\ell$ 当概率分布。

按基 $1,b_1,b_2,b_3,b_1b_2,b_1b_3,b_2b_3$ 形成矩阵，entry 为两基单项式 Boolean 并集的 $\ell$ 值。其精确 Schur 正 pivots 为

\[
 1,\quad \frac{21}{100},\quad \frac{63}{320},\quad \frac7{40},\quad
 \frac7{256},\quad \frac7{288},\quad \frac7{384}.
\]

也可直接证明，不依赖这些消元数值。$\ell$ 的 cube signed weights 为：$000$ 和三个 singleton patterns 各 $35/160$，三个 doubleton patterns 各 $7/160$，$111$ 为 $-1/160$。任意三位 degree $\le2$ polynomial $q$ 满足三阶差分恒等式

\[
 q(111)=q(110)+q(101)+q(011)-q(100)-q(010)-q(001)+q(000).
\]

令 $S$ 为七个 positive patterns 上的 weighted $q^2$ 和。weighted Cauchy 给

\[
 q(111)^2\le\left(4\frac{160}{35}+3\frac{160}{7}\right)S
 =\frac{608}{7}S,\qquad
 \ell(q^2)=S-\frac{q(111)^2}{160}\ge\frac{16}{35}S\ge0.
\]

每个原 degree $\le2$ polynomial 拉回该七维 span。因此完整原 global $M_2$ 是上述 PSD 矩阵的线性拉回，覆盖全部 $1+34+\binom{34}{2}=596$ 个原 square-free degree $\le2$ monomials。没有只核一个原小 principal submatrix。

### 13.3 全部物理机的 raw affine localizers

两个 outer private 的 raw loads/slacks 分别为

\[
 \operatorname{load}_{M0}=b_1+c(1-b_2),\qquad
 T-\operatorname{load}_{M0}=(1-b_1)+c b_2,
\]
\[
 \operatorname{load}_{M1}=(1-b_1)+c b_3,\qquad
 T-\operatorname{load}_{M1}=b_1+c(1-b_3).
\]

其他全部 private loads 及四个 home-resource loads 恒一；四个 fallback-resource loads 是 $b_2,1,1,1-b_3$。任意原全局 affine $q$ 拉回三位 affine。对任意 literal $l$，Boolean 恒等式与 global $M_2$ 给

\[
 L(lq^2)=\ell((lq)^2)\ge0,
\]

因为 $lq$ 的 degree 至多二。两个 outer slacks 是 nonnegative literal 和；恒一行的 slack 为 $c>0$；其余 literal-load 行的 slack 为 $c+(1-l)$。故每台原机器的 raw-load localizer 对**所有原全局 affine $q$** 均 PSD。这是所有 $0<c<1$ 的统一证明。

### 13.4 每机完整 CONFIG law 与全部本地矩

$\ell$ 在任一 bit 上是真实 Bernoulli：$P(1)=3/10$。在任意两个 bits 上，它的完整真实边际是

| two-bit pattern | probability |
|---|---:|
| 00 | $35/80$ |
| 10 | $21/80$ |
| 01 | $21/80$ |
| 11 | $3/80$ |

每台机器的全部 endpoint variables 同时至多依赖两个 bits：$M/0$ 依赖 $b_1,b_2$，$M/1$ 依赖 $b_1,b_3$，其余至多一个 bit 或常数。取对应真实边际，按本行变量值生成 membership configuration，便给该机一份有限 law。

为明示合法性，$M/0$ 的端记为 selector $S=b_1$、private payload $P_u=1-b_2$、$P_v=0$，时间为 $1,c,1-c$。其全部 CONFIG law 为

| configuration | weight | load |
|---|---:|---:|
| $\{P_u\}$ | $35/80$ | $c$ |
| $\{S,P_u\}$ | $21/80$ | $1+c=T$ |
| empty | $21/80$ | $0$ |
| $\{S\}$ | $3/80$ | $1$ |

$M/1$ 的 selector 为 $S'=1-b_1$，private payloads 为 $P_r=0,P_s=b_3$，时间为 $1,1-c,c$。其全部 law 为

| configuration | weight | load |
|---|---:|---:|
| $\{S'\}$ | $35/80$ | $1$ |
| empty | $21/80$ | $0$ |
| $\{S',P_s\}$ | $21/80$ | $1+c=T$ |
| $\{P_s\}$ | $3/80$ | $c$ |

其余机器的端是单位互补 pair、单 literal 或常数，故上述单 bit law/常数 law 的配置 load 至多一。每份 law 总质量一且 legal。

本行任何 Boolean polynomial 拉回后只依赖其至多两个 bits，所以与该同一 law 的期望完全一致。于是全部本地 square-free monomials、全部 membership/complement patterns、完整 row law 都共享，而不只 first/pair。各行的 law 不被拼成一个真实 global schedule law。此例每行原端数至多三，故所有 Boolean 本地矩也已由 degree $\le4$ 覆盖。

### 13.5 实际 OPT 与两个跨行负式

真实 schedule 选择 $M/0,H_u/1,H_v/1,H_r/0,H_s/0$。每 selector 去其选中 private；选中 state 的全部 positive incidence jobs export 到 exact resource，所有其他原 incidence jobs 留 private。资源 $u,v,w_u,w_v,r,s$ 各接一件 unit；所有 private loads 为零或一。全部17个原 jobs 各出现一次，给 $C=1$，而单位 selector 给 $\operatorname{OPT}\ge1$，所以

\[
 \operatorname{OPT}(P(Q_c))=1.
\]

直接 canonical state $A$ 取物理 selector 端，claim $Z$ 取 selector 乘该 incidence 的 resource 端。canonical degree-two 矩拉回 physical degree $\le4$，有

\[
 A_{M0}=b_1,\qquad Z_{M0u}=b_1b_2,\qquad
 Z_{M0v}=b_1,\qquad A_{H_s0}=b_3.
\]

因此 canonical claim 非负 row 乘 state primitive 已失败：

\[
 \boxed{L(Z_{M0u}A_{H_s0})=-1/160<0.}
\]

并且 $\epsilon=1-c$ 下 activation-quality slack 为

\[
 h'=cZ_{M0u}+(1-c)Z_{M0v}-\epsilon A_{M0}=c b_1b_2,\qquad
 \boxed{L(h'A_{H_s0})=-c/160<0.}
\]

三个因子分别可取 M-selector 的 private-$M0$ 端、M-u-incidence 的 resource-$u$ 端、Hs-selector 的 private-$H_s0$ 端，位于三台不同机器。没有一行包含三个 bits。因此失败不再来自某一行未共享的 triple；全部 local law 已共享。

这里 $h'=A_{M0}(T-\operatorname{load}_{M0})$ 是 raw degree-two polynomial。取 **raw affine** $q=A_{H_s0}=b_3$，$L(h'q^2)=-c/160$ 是 degree $\le4$ 的明确负值，故 raw slack 的 affine localizer 不自动变成该 activation slack 的 raw-affine localizer。没有宣称可把任意 canonical affine $F$ 免费当 raw affine；canonical claim 本身是 raw quadratic，含它的平方测试可能需要六阶矩，本文不延拓这一范围。

### 13.6 位成本、有限证据与前身范围

给定 $c$ 后，只有固定数量的机器、任务和矩条目；处理时间为 $c,1-c,1$，矩和 row-law 权重为固定有理数。生成及输出总位长对 $c$ 的二进制编码多项式。不取 $c=0,1$，不把零权端或 $T=1,2$ 端点混入本族。

自足 Fraction audit 为这族固定维证书构造完整18机17job34端，核 Boolean/one-hot substitution 恒等式、7维拉回 Gram 正 pivots、每个给定参数的18个4维 raw-affine localizer、全部72个本地 monomials及72个完整 membership patterns、两个负式和逐一17-job makespan-one witness。作者 default $c=3/4$ 及三个附加有理参数均实际通过；root 已实读代码并四次 CLI 重放。一般参数仍由本节 literal-SOS/PSD及full-law证明承担，不称有限程序穷举了所有参数、全部原四阶 identities 或所有完整 assignments。代码不是一般 SDP solver。

旧14机13job前身只共享同机first/pair。其关键private行有 $L(SP_uP_v)=7/160>0$，而该triple load二，在legal CONFIG中应为零；故共享该行triple会切旧证书。原冻结Exact/Proof/code保持这一诚实局限，不另立正式Claim或把其有限证据冒作本18机族的运行。新族用跨行negative triple补上了这个重试范围。

本节排除的仅是指定direct same-point pullback。Q本身有别的 $\mathcal R_1$ 点及实际最优schedule；改点、另求解、其他packing接口、前十二节算法均未被排除。若要求所有 global triple literal 的期望非负，本证书因 $L(b_1b_2b_3)<0$ 被排除。第14节另证的source-S3充分桥不作为本反例前提；一般多人共享/deep结构与UM主目标继续OPEN。


## 14. 完整 raw 三次 literal lifts 到 canonical plain-SA1 的同点提取

- **ID / version**：`UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1`。
- **Objects / Domain**：任意完整显式 normalized-flat 菜单 Q 及 ordinary P(Q)；非空有限 groups，每组非空有限 indexed states，非负二进制有理 listed incidence coefficients，每 state 总质量一。保全部 selectors、所有 listed incidences、显式零 incidence、重复 indexed states、inactive states 及 unused resources；每个原 job 的全部 finite endpoints 都是原变量。阈值为每个二进制有理 `1≤T<2`，`epsilon=2−T∈(0,1]`。
- **Quantifiers / Exact Statement**：每份实际 makespan≤T 的完整 schedule 都给出下述 raw `S3(P,T)` 的 Dirac 可行点。对**每个给定的共同有限有理 S3 点 L**，指定 product substitution `A_s=a_s,Z_e=a_sE_e` 的 degree≤2 pullback F 满足完整 canonical `R_epsilon(Q)` plain primitive-SA1；原 L 不改。若同一 L 另有 raw M2 PSD，则同一 F 另有 canonical M1 PSD。
- **Assumptions / Definitions**：S3 的全部原 boxes、物理 raw-load slack 及 unit-resource **cap1** 行，均乘全部长度≤3 的原 literals；Boolean/job one-hot identities 完整到 degree4。精确定义在§14.1。S3 不要求原 exports≤activation、inactive jobs 留 private、CONFIG law 或 PSD。
- **Conclusion / Algorithm**：可建立并解一个显式 rational LP；不可行时给出实际 threshold-T 不可行的 soundFAIL，可行时按指定 substitution 输出一个 R 点。输出是 canonical 点，不是实际 schedule。可选 PSD 部分只转换已给出的同一 M2 证书，不提供 exact SDP finder。
- **Complexity / Dependencies**：固定次数的显式 LP、共同有限矩表、normalized equality、原 Boolean/one-hot 和有限有理运算。LP 构建/有理解算及给定点提取的总位成本均为输入规模的多项式；§14.6给位长论证。无需未知 integral benchmark、CONFIG oracle、概率倒数循环或高阶 moment oracle。
- **Scope / Limits**：source-S3 适用一般 normalized-flat Q，但本结论仅付清指定同点接口。S3 本身未含 M2/CONFIG，不能称其包含全部 raw K2；raw K2 也不自动含这些 S3 lifts。对仅持有 raw K2 的点，须额外核验这些 S3 rows 才能调用本节；S3 本身也可独立作 source。没有 S3 与真实可行性的反向等价、constant rounding、一般 UM 近似或 actual-gap 上界。
- **Status / Software**：数学证明如下；算法仅为数学规格。本 ID 的软件实现、checker、run 均为 **none**；不借其他固定反例程序补签。全球新颖性未认证；一般 UM 主目标仍 OPEN。

### 14.1. 全部原变量、source LP 与 canonical 目标

State s 的 private root 与其他 states 及资源机器全部不同。每 group 的一枚 unit selector 可在该组全部 indexed roots 执行；记其去 root s 的端指标为 a_s。每 listed incidence e=(g,s,u) 是独立原 job，在该 root 时间 p_e、在原资源 u 时间一，其他端为无穷。记其 private/resource 两个原端指标为 D_e,E_e；即使 p_e=0，两原端和该 job 均保留。

对每原 job 的每个 finite endpoint 保留变量 x，总数 N。共同 L 给出所有 total-degree≤4 monomials 的有限有理表，L1=1，并满足

\[
L((x^2-x)m)=0\quad(\deg m\le2),\qquad
L((\sum_{i\text{ finite for }j}x_{j,i}-1)m)=0\quad(\deg m\le3).
\tag{14.1}
\]

每个原 literal 是 x 或 1−x。以下每条原 affine row h≥0，均要求 `L(hB)≥0` 对每个长度≤3 的原 literal product B，含空乘积：

\[
\begin{array}{ll}
x\ge0,\ 1-x\ge0 &\text{对每个原 finite variable},\\
T-\sum_jp_{i,j}x_{j,i}\ge0 &\text{对每台物理机器，和只取 finite 端},\\
1-\sum_{e:u(e)=u}E_e\ge0 &\text{对每个原 unit resource，含全部零 incidence heads}.
\end{array}
\tag{14.2}
\]

这就是本节 `S3(P,T)`。最后一行是 **cap1**，与该机另有的物理 slack `T−ΣE_e` 分别列出；不能互相免费替代。重复/互补 literals 均用(14.1)解释，没有全局真实 law 假设。

置 canonical primitives `A_s=a_s,Z_e=a_sE_e`。对 canonical degree≤2 polynomial f，定义

\[
F(f)=L(f(a,aE)).
\tag{14.3}
\]

右侧 degree≤4，故由给定 L 唯一确定。这里“同点”指原 L 和所用 raw entries 都不改；不是声称 `F(Z_e)=L(E_e)`。

目标 `R_epsilon(Q)` plain common primitive-SA1 的完整含义是：F1=1，每 primitive V 有 `F(V²−V)=0`；每 group 的 `Σ_sA_s=1` 及其乘任意 primitive/补的等式成立。下列 base affine rows，分别乘 `1`、任意 canonical primitive V、或 `1−V` 后，F 值全部非负：

\[
\begin{gathered}
A_s\ge0,\quad1-A_s\ge0,\quad Z_e\ge0,\quad1-Z_e\ge0,\quad A_s-Z_e\ge0,\\
1-\sum_{e:u(e)=u}Z_e\ge0,\qquad
\sum_{e\in s}p_eZ_e-\epsilon A_s\ge0.
\end{gathered}
\tag{14.4}
\]

所有 listed zero-incidence claims 也在目标中；其 quality 系数零，gate/boxes/resource 行仍保留。目标未额外要求 M1，除非按§14.5的可选部分加入。

### 14.2. 必要性与 soundFAIL

真实 schedule 的原端指标为 Boolean，全部 job one-hot exact，原 boxes 及每机器 raw physical slack 非负。每资源的 eligible jobs 都为 unit，makespan≤T<2 迫至多一 job，所以(14.2)的 cap1 也有效，包括 private 时间零的 job。

在该真实 assignment 上，每个 literal product 为0或1，故每 row 乘任意≤3 literals 仍非负。其 Dirac degree-four table 满足完整 S3。这对全部 ordinary jobs、inactive exports 和所有原 finite endpoints 同时成立。因此 S3 infeasible 推出实际 threshold-T 不可行；没有反向实际可行性断言。

### 14.3. Canonical 的正性工具、Boolean 和 one-hot

每个长度≤4 的 raw cylinder B 有 `L(B)≥0`：非空时取一个 literal 作为(14.2)的 box row，其余≤3 literals 为 multiplier；空乘积用 L1=1。

每个 canonical multiplier `W∈{1,V,1−V}` 的 pullback 都是系数为正的 raw cylinders 之和，每项长度≤2。唯一需写出的 complement 是

\[
1-a_tE_f=(1-a_t)+a_t(1-E_f).
\tag{14.5}
\]

故两个额外 raw literals 乘 W 的每项是长度≤4 cylinder；一个原 linear row 再乘一个 raw literal 及 W 时，row 的 multiplier 长度≤3。

Canonical Boolean 性由原(14.1)支付。对 claim，明确有

\[
(a_sE_e)^2-a_sE_e
=(a_s^2-a_s)E_e^2+a_s(E_e^2-E_e),
\tag{14.6}
\]

两个 Boolean multipliers 分别为 degree2、degree1。Group `ΣA_s−1` 是原 selector job one-hot；乘 W 后其 raw multiplier degree≤2，故等式成立。若显式要求同组 distinct selector pair 零，用 one-hot 乘 A_t、各 pair cylinder 非负及 Boolean 性即可逐项推出。全部 indexed states 保留，包括重复 states。

`A_s`、`1−A_s`、`Z_e=a_sE_e`、`1−Z_e` 及 gate `A_s−Z_e=a_s(1−E_e)` 各乘 W 后，都按(14.5)展开为长度≤4 raw cylinders 的正和。因此(14.4)所有 boxes/gates 的全部 plain-SA1 lifts 成立，亦包括 zero-incidence claims。

### 14.4. 每个 resource 与每个 state 的全部 lifts

固定原资源 u，记 `r_u=1−Σ_{e:u(e)=u}E_e`。精确 polynomial identity 是

\[
1-\sum_{e:u(e)=u}a_{s(e)}E_e
=r_u+\sum_{e:u(e)=u}(1-a_{s(e)})E_e.
\tag{14.7}
\]

乘任意 W。第一项由原 cap1 row 乘长度≤2 raw cylinders 非负；每个和项是两个 raw literals 乘 W，故由长度≤4 cylinder 正性非负。这付清每个 canonical resource row 的所有 primitive/补 lifts。Unused resource 的空和也包括；没有合并 tags 或遗漏 zero jobs。

固定 state s，原 private raw load 是 `a_s+Σ_{e∈s}p_eD_e`。令 `h_s=T−load_s`；原 incidence job one-hot 和 `Σ_{e∈s}p_e=1` 给

\[
h_s=(T-1)-a_s+\sum_{e\in s}p_eE_e,
\qquad
a_sh_s\equiv\sum_{e\in s}p_ea_sE_e-(2-T)a_s.
\tag{14.8}
\]

后式仅用 `a_s²=a_s`。为求它乘 W 的 L，private-end 替换用原 job identity 乘 `a_sW`，degree≤3；Boolean defect 用 multiplier W，degree≤2。所有等式总次数≤4，所以

\[
F\!\left(\left[\sum_{e\in s}p_eZ_e-\epsilon A_s\right]W\right)
=L(h_sa_sW)\ge0.
\tag{14.9}
\]

最后由 W 的正展开：每项再乘 a_s 是长度≤3 的原 literal product，正是原 physical h_s row 的 source lift。W 可来自任何其他 group/state 的 A、Z 或补；这里始终是同一个 L，没有另选 conditional 点。零 p_e、inactive exports 与 T=1 时的 epsilon=1 都在相同身份内，没有除系数或概率。

§14.3–14.4已证明完整 R_epsilon(Q)，不是只证明 first rows 或部分 selectors 的 conditions。

### 14.5. 可选 raw M2 到 canonical M1

若给定的同一个 L 满足 `L(p²)≥0` 对全部 raw degree≤2 p，则每个 canonical affine q 经(14.3)代入后为 raw degree≤2 polynomial，故

\[
F(q^2)=L(q(a,aE)^2)\ge0.
\tag{14.10}
\]

这只保 canonical M1。Plain R 的 positivity 由显式 source lifts 证明，不能反向说 raw M2 或 raw affine localizers 已提供它们。可选部分没有有理 SDP finder、任意实可行点的 rational-witness 定理或更高层数保持结论。

### 14.6. 显式 LP、总位复杂度和边界

全部 total-degree≤4 moment variables 数为 `binom(N+4,4)=O((N+1)^4)`。Boolean/job identities 的 multipliers 分别≤2、≤3；raw rows 数为 `2N+#machines+#resources`，各自有 `O((N+1)^3)` 个≤3-literal multipliers。每乘积展开至多8项，每 raw row 长度至多线性，系数来自有理输入 p、T 与多项式大小整数运算；约束数、系数 bitlength 均多项式。

有理 witness 位长也可控制。每个 square-free monomial M、degree≤4，由 box lifts 得 `0≤L(M)≤1`：一个 box literal 乘其余≤3给非负；`(1−x)M'` 给 `L(xM')≤L(M')`，逐次归至 L1=1。重复幂由(14.1)消去。因此 reduced feasible polytope 有界，非空时可取 vertex。清各 row 分母后，活跃整数线性系统的位长多项式；Cramer/Hadamard 给 vertex 的 rational bitlength 多项式。可用普通 rational LP 方法求点或判不可行。

给定完整有理 L，每个 canonical degree≤2 entry 用固定次数 product substitution，从已给 degree≤4 表直接计算，时间与输出总位长由显式输入和该点总位长多项式控制。没有按 `1/epsilon`、概率或最小正系数展开，也不搜索未知 CONFIG/SDP 证书。

本节只解决上述同点 point-pullback。S3 可独立作为 LP 使用；若 source 另有 raw K2，本节的充分假设是显式加入这些 global literal-row lifts，不能把各机 full local law 自动换成它们。不主张该层数最小、锐或每条 source row 都必要。所得 F 仍是 canonical relaxation point，不能免费拼成全 groups 实际 allocation 或一般 UM schedule。软件实现、checker 和运行均无；`UM-TARGET-v1` 仍 OPEN。

本节与§13的实际审查次序、原件、软件范围及当前状态见[新增接口审查](../../reviews/unrelated_machines/raw_k2_canonical_pullback_and_sa3_repair_review.md)；不从旧两算法的审查推定新合同已被认证。
