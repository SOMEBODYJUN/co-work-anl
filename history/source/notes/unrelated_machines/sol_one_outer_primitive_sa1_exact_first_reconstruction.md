# One-outer full primitive SA1：Exact-first 独立重构与攻击记录

审查者：`sol_general_repair`，2026-10-18。

只读输入：`one_outer_full_primitive_sa1_rounding_exact_v1.md`，预期 SHA256
`7364055e2c13a8962b5a022f959721014fb6219465dbe0340676521ac9437eac`。
本记录先冻结，未读 identity 的 `single_outer*` 作者稿，未索取作者证明，未读 NSW
针对此限定算法的私聊推导。此前已研究并与队友交流一般 primitive-SA1、singleton
state closure 及当前 \(Q_t\) 的 \(\epsilon^2D\) cut；故这是 Exact-first 独立重构，
不是无背景 blind review。以下 welfare backend 从有限概率、Bonferroni 和精确条件
期望直接重构，不调用未读作者实现或一般 XOS 舍入定理。

**当前结论：** 按所读 Exact 的全部物理域及 full primitive-SA1 前提，重构得到
\(V\ge\epsilon^2/4\)、全部原 jobs 的 \(C_{\max}\le2-\epsilon^2/4\)。
未发现 fatal。关键依赖是原 claim primitive 的**补乘子**、每个 fallback state 的
条件 value 行、同一共同二阶数组，以及只有一个 outer、所有其他组都有各自独立 home。
不升级为多 outer、任意辅助 core、degree-four PSD 或一般 UM 结论。

## 1. 记号与二阶语义

对任一原 primitive \(X\) 写一阶 \(\mu_X\)、共同对称二阶 \(Y_{XY}\)，
\(Y_{XX}=\mu_X\)。线性化符号只记录次数至二的约束，不假定已有真实共同 law。
全部 box 行乘原 primitive 及其补，给

\[
0\le Y_{XY}\le\min(\mu_X,\mu_Y),\qquad
Y_{XY}\ge\mu_X+\mu_Y-1.
\tag{1.1}
\]

state partition、gate、resource 和逐 state value 的乘式均使用这个同一 \(Y\)。
给定点是显式有理数组；算法只作有限有理运算和比较。

## 2. Singleton state 整化不使用 triple

固定 helper 的 own state。令 \(h=A_{H,\mathrm{own}}\)，
\(z=Z_{H,\mathrm{own},g}\)。其 value 行是 \(z-\epsilon h\ge0\)，gate 是
\(h-z\ge0\)。gate 乘 \(z\) 及 box \(h\le1\) 乘 \(z\) 给
\(Y_{hz}=\mu_z\)。value 行乘**原 claim 的补** \(1-z\) 给

\[
0\le L[(z-\epsilon h)(1-z)]
=-\epsilon(\mu_h-Y_{hz})
=-\epsilon(\mu_h-\mu_z).
\]

而 gate 的原行给 \(\mu_h\ge\mu_z\)，故 \(\mu_h=\mu_z\)。
再把 \(h-z\ge0\) 分别乘任意原 primitive \(r\) 与 \(1-r\)：

\[
Y_{rh}-Y_{rz}\ge0,\qquad
(\mu_h-\mu_z)-(Y_{rh}-Y_{rz})\ge0.
\]

所以

\[
Y_{rh}=Y_{rz}\quad\text{对每个原 primitive }r.
\tag{2.1}
\]

所有式子至多二次。没有把二阶点当真实分布，也没有使用 \(rhz\) 三阶条目。
仅有 state 乘子、没有 claim primitive 及其补时，本步骤不成立。

## 3. 只条件化一次 outer state

选任意 \(a\) 使 \(\rho=\mu_{A_{M,a}}>0\)，存在性来自 outer state partition。
记 \(r=A_{M,a}\)。对 \(j\in J_a\) 定义

\[
u_j=Y_{r,Z_{M,a,g_{a,j}}}/\rho.
\]

由 outer 的 value 行乘 \(r\)，

\[
\sum_{j\in J_a}w_{a,j}u_j\ge\epsilon.
\tag{3.1}
\]

对本行 helper \(j\) 的每个 fallback state \(s\) 定义

\[
\alpha_{js}=Y_{r,A_{H_j,s}}/\rho,\qquad
\zeta_{jsu}=Y_{r,Z_{H_j,s,u}}/\rho\quad(u\in B),\qquad
\tau_j=\sum_{s\text{ fallback}}\alpha_{js}.
\]

只保留正 coefficient 的 \(\zeta\) 即可；原零 claim 可以丢出算法 benchmark，
不能从物理矩阵删除。由各原 gate/value/state-partition 行乘 \(r\)，

\[
0\le\zeta_{jsu}\le\alpha_{js},\quad
0\le\tau_j\le1,\quad
\sum_u p_{jsu}\zeta_{jsu}\ge\epsilon\alpha_{js}.
\tag{3.2}
\]

home resource 列乘 \(r\)，丢去其他非负项，再用 (2.1)，给

\[
u_j+Y_{r,A_{H_j,\mathrm{own}}}/\rho\le1.
\]

helper partition 乘 \(r\) 给 \(\tau_j=1-Y_{r,A_{H_j,\mathrm{own}}}/\rho\)，因此

\[
\tau_j\ge u_j,\qquad \sum_jw_{a,j}\tau_j\ge\epsilon.
\tag{3.3}
\]

每个 \(B\)-resource 列乘 \(r\)，只保留本行 helpers 的 fallback 项，给

\[
\sum_{j\in J_a,s}\zeta_{jsu}\le1\qquad(u\in B).
\tag{3.4}
\]

丢去其他组、其他外行、原零 incidence 的项均合法，因为这些二阶条目由原非负行
乘 \(r\) 保证非负。这没有假设其他组实际不需要资源；它们稍后统一领各自 home。
由 (3.2)-(3.3)，显式 fractional weighted welfare benchmark 是

\[
W_{\rm frac}=\sum_{j,s,u}w_{a,j}p_{jsu}\zeta_{jsu}
\ge\epsilon\sum_j w_{a,j}\tau_j\ge\epsilon^2.
\tag{3.5}
\]

这里每个 fallback state 的 value 乘式不可替换为若干彼此独立的行 witness；
所有 \(\alpha,\zeta,u\) 确实来自同一 \(r\) 行。

## 4. 自足的确定性 1/2 welfare backend

写 \(w_j=w_{a,j}\)。为说明初始 benchmark，构造一个新的随机实验；这不是声称
原 \(Y\) 有共同 law。每个 helper \(j\) 独立按概率 \(\alpha_{js}\) 选择一个 fallback
state，另以概率 \(1-\tau_j\) 选 empty 算法选项。若选 \(s\) 且 \(\alpha_{js}>0\)，
在资源 \(u\) 上以概率 \(\zeta_{jsu}/\alpha_{js}\) 作虚拟 claim，claim 的分值为
\(d_{jsu}=w_jp_{jsu}\)。零 \(\alpha\) 必有零 \(\zeta\)，无需相除。

对固定 \(u\) 与正 threshold \(d\)，helper \(j\) 的分值达到 \(d\) 的概率是
\(\beta_j(d)=\sum_{s:d_{jsu}\ge d}\zeta_{jsu}\)。它至多一，且
\(q(d)=\sum_j\beta_j(d)\le1\) 由 (3.4) 保证。不同 helpers 的实验独立，故

\[
\Pr[\max_j \mathrm{score}_{ju}\ge d]
=1-\prod_j(1-\beta_j(d))
\ge q(d)-\sum_{j<k}\beta_j(d)\beta_k(d)
\ge q(d)/2.
\tag{4.1}
\]

对该资源的有限分值层作离散积分，再对资源求和，得最大 claim 分值之和的期望
\(\Phi\ge W_{\rm frac}/2\)。这里只用有限 Bonferroni 下界；没有抽样成功概率或
无理数精度义务。

**精确条件期望去随机化。** 按固定 helper 次序选择其 state。对一个已固定 state
\(s\)，其资源 \(u\) 分值达到 \(d\) 的概率改为
\(\mathbf1[d_{jsu}\ge d]\zeta_{jsu}/\alpha_{js}\)；固定 empty 时为零；未固定 helper
仍用 \(\beta_j(d)\)。任意前缀的 score 期望可由

\[
\Phi(\text{prefix})=
\sum_u\sum_{k=1}^{m_u}(d_k-d_{k-1})
\left(1-\prod_j(1-\beta^{\rm prefix}_j(d_k))\right),
\tag{4.2}
\]

精确计算，其中 \(0=d_0<d_1<\cdots<d_{m_u}\) 为资源 \(u\) 的不同正分值。
下一个 helper 的各正概率 state/empty 选项的 \(\Phi\) 加权平均恰为当前 \(\Phi\)，
故枚举其显式选项、取精确 \(\Phi\) 最大者不会下降。无需在条件前缀下重新主张
\(q(d)\le1\)；(4.1) 只用于初始期望，下界由条件期望恒等式保持。

全部 states 固定后，不实际抽 claim。直接将每个资源给 chosen clause 分值
\(w_jp_{j,s_j,u}\) 最大的 helper；零分值可不分配。完整候选集的最大分值逐资源
不小于其随机 claim 子集的期望最大值。因此输出不交 \(B_j\subseteq B\)，满足

\[
\sum_j w_j f_j(B_j)\ge\Phi\ge W_{\rm frac}/2\ge\epsilon^2/2,
\tag{4.3}
\]

其中 \(f_j\) 是 helper 的 fallback states 的最大加性值；无 fallback 时定义零。
\(f_j\) 至少 chosen clause 值，且由每个 state norm-one 有 \(f_j\le1\)。
若改选达到 \(f_j(B_j)\) 的另一原 fallback state，只提高该组值，不改变资源冲突。
empty 是算法中的零贡献选项，不是新增物理 state。

**位长。** (4.2) 的层数、helper 数、资源数和候选 state 数都受显式输入控制。
所有条件量由 supplied point 的有理坐标加减乘除得到；只对正 \(\rho\) 和正
\(\alpha\) 相除，分子分母位长相加而不是按其数值倒数循环。每个乘积及有限和
包含多项式个显式有理因子/项，故总位长多项式。层排序、候选 \(\Phi\) 比较及最大
分值分配均可精确确定性完成。不需近似对数、指数、概率离散化或 \(1/\epsilon\) 展开。

## 5. 好组阈值、所有组回填及全部原任务

令 \(\eta=\epsilon^2/4\)，Good 为满足 \(f_j(B_j)\ge\eta\) 的本行 helpers。
\(\sum_jw_j=1\)、\(f_j\le1\) 及 (4.3) 给

\[
\epsilon^2/2\le\sum_jw_jf_j(B_j)
\le\sum_{j\in\mathrm{Good}}w_j+\eta,
\qquad
\sum_{j\in\mathrm{Good}}w_j\ge\eta.
\tag{5.1}
\]

outer 选原 state \(a\)，领取 Good 对应的 homes。Good helpers 领取上述不交的
fallback bundles，并选实际 attaining 原 fallback state。其余本行 helpers 领取
自己的 home；**所有其他外行 helpers 也全领取自己的 home**。全部 homes 跨
\((a,j)\) distinct，且与 \(B\) 不交，所以没有冲突。outer 与 Good 值至少 \(\eta\)，
其余 helpers 值一。若某 helper fallback mass 为零，它不贡献 (3.5)，但仍可回 home。

调度输出：每组 unit selector 放在上述原 indexed-state root；仅导出所选 state
实际领取的正 incidence jobs；全部其他 jobs 留在各自原 private roots，包括所有
未选 outer states、所有未选 helper fallback states、Good helper 未选 own state 的
原 unit incidence，以及全部原零 incidence。未选 roots 负载一；selected roots
负载为二减实际所领值；每资源机至多一枚 unit job。因此
\(C_{\max}\le2-\eta\)。所有 jobs 的 identities 和有限资格均来自原矩阵，输出扫描
其显式列表，大小和时间多项式。unused resources 为空；重复 indexed states 不合并。

## 6. 主动攻击与范围检查

- singleton 整化确实使用 \(Z\) 的补乘子；若只有 outer-state 条件 value 与 fractional
  home gate，原 \(Q_t\) 一类会逃逸。Exact 明确给 full original A/Z primitives，故
  该攻击不适用。没有借 optional whole-core 行、unit-FSLP 或 PSD 补缺。
- 每 fallback state 的 value 行都需乘同一个 outer \(r\)。只看 global leaf flow 或各
  state 独立 conditional Hall，不能推出 (3.2)-(3.5)。Exact 的共同数组和全部乘式足够。
- deterministic welfare 并非“期望好所以任挑 states”；(4.2) 明确给 rational backend
  和候选比较。最后忽略虚拟 claim 只提高按 chosen clause 计算的福利，方向正确。
- 全组回填依赖全部非 outer 组均有自己的独立 home。若加一个没有 home 的辅助 core，
  把它从 benchmark 丢去就可能使最终回填失败；若多个 outer 同时要用 \(B\)，同样不能
  分别执行本 proof。Exact 逐字排除了这两项外推。
- \(\epsilon\) 可为任意正 binary rational；本证明不用常数大小枚举。零 \(\lambda\)、零
  fallback mass、零 incidence、重复 indexed states、unused resources 均按以上规则处理。
  state norm-one 和 positive outer weights 排除了空 \(J_a\) 的非法输入；零 claim 项不被
  当成必须导出的正工作。\(\epsilon=0\) 不属于 Exact，singleton 整化也明确需正性。
- supplied rational point 的查验或求解不是重构中的隐藏 oracle。所需数值均直接来自
 该点；没有求实际 OPT、未知 target allocation、通用 CONFIG 或 SDP exact solver。

本记录是对冻结 Exact 的独立数学重构及 scope 攻击，不声称已运行作者程序、已枚举
全物理矩阵 assignments、已完成作者读后审查或已证明一般目标。主目标仍 OPEN。
