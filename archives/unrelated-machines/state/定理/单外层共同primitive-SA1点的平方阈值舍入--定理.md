---
id: "unrelated-machines/one-outer-supplied-point-rounding"
kind: "theorem"
type_tag: "定理"
title: "单外层共同 primitive-SA1 点的平方阈值舍入"
status: "proved-under-explicit-single-outer-scope"
truth_status: "proved-for-supplied-rational-common-point"
review_level: "full-author-source-read-and-cross-version-comparison"
summary: "在一个 outer、全索引互异 homes、每 home 一个 own-singleton helper、B-only normalized fallback、无其它组的完整 ordinary UM 域内，任意给定 full primitive-SA1 有理点在 0<epsilon<=1 时可确定性总位多项式舍入为全组实际质量 epsilon²/4 及完整原 jobs 调度峰值 2−epsilon²/4。完整保留一次共同条件化、均匀赢家、Bernoulli-count DP、阈值重组和回填证明；不把后续 Q-only 13/8 或 CDF 审计转记为本算法的运行。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md#1-7"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md#1-7"
legacy_ids:
  - "UM-SINGLE-OUTER-PRIMITIVE-SA1-EPS2-4-v1"
source_id: "c36482710e27da1bc3f7"
source_sha256: "da4897a966e8b5e10299622c5f93d67b115f859d1ae8fc77bd29f8f7ce0aa571"
source_size: 10715
scope: "explicit one-outer normalized-flat; independent own homes; full original A/Z primitive-SA1; supplied rational point"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/single-outer-sa1-threshold-floor/original/sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md"
---

# 对象身份和准确结论

本页保存 `c36482710e27da1bc3f7` 作者全文 §1–7 的自足数学正文。该源是 scratch structural rounding deduction；后续 Exact-first 和作者 read-after 对相同限定结论未报告 fatal，本次逐式实读也未发现方向或量词错误。它是给定点舍入定理，不负责从菜单寻找可行点。标准福利估计和条件期望方法本身不认领新颖性。

令输入是下述显式菜单 Q、正有理阈值 `0<epsilon<=1`，以及同一完整 primitive-SA1 系统的一个显式有理可行点。存在确定性算法，时间对三项输入的总二进制编码长度为多项式，输出每个真实组的一个原 indexed state、两两不交的资源 bundles 和全部原 jobs 的普通合法 assignment，使

\[
\min_g q_g\ge\tau:=\epsilon^2/4,
\qquad C_{\max}\le2-\tau.
\tag{T}
\]

这里 `q_g` 是所选原 state 对实际 bundle 的加性价值；若 V 表示最优的全组最小 menu value，(T) 也给 `V>=epsilon²/4`。不存在把任意二阶点当作真实 joint state distribution 的前提。PSD、whole-core quality rows 和 unit-FSLP 均不是证明所需；若额外加入这些行，结论仍适用于其可行点。

# 1. 完整物理域与共同矩系统

恰有一个 outer 组 M，其有限非空 indexed states 记为 a。state a 的资源为 `g_(a,j), j∈J_a`，系数 `w_(a,j)>0` 是显式二进制有理数，且

\[
\sum_{j\in J_a}w_{a,j}=1.
\]

所有 homes 在整个 `(a,j)` 索引上物理互异。每个 home 有唯一对应 helper `H_(a,j)`。其 own indexed state 是该 home 上系数一的 singleton；其余各 fallback indexed state s 是有限资源集 B 上的显式非负有理向量 `p_jsu`，每 state 的系数和为一。B 与全部 homes 不交；fallback 支撑可任意重叠，也可跨不同 outer states 重叠。允许 helper 没有 fallback states。没有其它组，没有无 own home 的 auxiliary core。

普通 unrelated-machines 矩阵完整生成如下：每组一枚 unit selector，可在该组各 state 的互异 private machines 上运行；每个原 listed state-resource incidence `(g,s,u)` 对应一枚不可拆 job，在该 state-private machine 上时间 `p_gsu`，在其 exact resource machine 上时间一；其它单元为无穷。每 state 的全部 incidence private load 为一。未选 states、重复 indexed states、零 incidence jobs 和 unused resources 全部保留，没有把逻辑 side constraints 加入实际调度。

对 state primitive `A_gs`、claim primitive `Z_gsu`，基系统为

\[
\sum_s A_{gs}=1,\qquad 0\le A_{gs},Z_{gsu}\le1,\qquad Z_{gsu}\le A_{gs},
\tag{1}
\]
\[
\sum_{g,s} Z_{gsu}\le1\quad(u\in U),\qquad
\sum_u p_{gsu}Z_{gsu}\ge\epsilon A_{gs}\quad(g,s).
\tag{2}
\]

每一基行，包括非负、box、gate，分别乘每个**原始 A/Z primitive** F 与其补 `1−F`，然后线性化。所有乘式使用同一个一阶数组 x 和对称二阶数组 Y，并有 `Y_XX=x_X`。这正是本页 full strong primitive-SA1 的含义；只含 state 乘子、只含 outer-state 条件行或各 helper 分别给出的条件点不够。

# 2. Own singleton 在每个原 primitive 条件下闭合

固定一个 helper own state，写其 state 为 A、唯一 claim 为 Z。gate 是 `A−Z>=0`，quality 是 `Z−epsilon A>=0`。quality 乘 `1−Z` 并用 `Z²=Z`，得到

\[
0\le L[(Z-\epsilon A)(1-Z)]
=\epsilon(Y_{AZ}-x_A).
\]

因为 epsilon 正，`Y_AZ>=x_A`。box `A<=1` 乘 Z 给 `Y_AZ<=x_Z`；一阶 gate 给 `x_Z<=x_A`，因此

\[
x_A=x_Z=Y_{AZ}.
\tag{3}
\]

将 gate 分别乘任意原 primitive F 及 `1−F`：

\[
Y_{AF}-Y_{ZF}\ge0,\qquad
(x_A-x_Z)-(Y_{AF}-Y_{ZF})\ge0.
\]

结合 (3)，

\[
Y_{AF}=Y_{ZF}\qquad\text{对每个原 primitive }F.
\tag{4}
\]

全部只用同一数组的 degree-two 行。没有再次条件化一个已经条件化的点，也没有调用未提供的 triple moment。`epsilon=0` 不在本页域内；只给 claim 正乘子而缺其补时，上述整化亦不成立。

# 3. 一次 outer 条件产生一份共同 fallback packing

由 M 的 state partition，存在 `lambda_a=x_(A_Ma)>0`。任取一个这样的原 state a，只条件化一次 `r=A_(M,a)=1`：任意原 primitive F 的条件一阶量为 `Y_rF/lambda_a`。每个基行乘 r 后除以 lambda_a，保证该同一条件向量满足全部基行；无需假设 Y 有真实全局 law。

下文只暂时记本行 helpers `j∈J_a`，省去 a 下标。outer 对其 home 的条件 claim 记为

\[
b_j=Y_{r,Z_{M,a,g_{a,j}}}/\lambda_a.
\]

outer quality 行给

\[
\sum_jw_j b_j\ge\epsilon.
\tag{5}
\]

helper j 在此条件下的 fallback-state masses、claims 和总 mass 为

\[
\mu_{js}=Y_{r,A_{H_j,s}}/\lambda_a,
\quad t_{jsu}=Y_{r,Z_{H_j,s,u}}/\lambda_a,
\quad f_j=\sum_{s\text{ fallback}}\mu_{js}.
\]

同一 r 行的 partition、gate、quality 给

\[
0\le f_j\le1,\qquad 0\le t_{jsu}\le\mu_{js},\qquad
\sum_up_{jsu}t_{jsu}\ge\epsilon\mu_{js}.
\tag{6}
\]

home 容量在该行中同时计入 outer claim 和 helper own claim。由 (4)，own claim 等于 own-state 条件 mass；partition 又给 own-state mass 为 `1−f_j`。因此

\[
b_j+(1-f_j)\le1,\quad f_j\ge b_j.
\tag{7}
\]

对每个 `u∈B`，原 resource 行也乘同一个 r。丢去其它外行 helpers 的非负条件 claims，仅保留本行 fallback 项，得到

\[
\sum_{j\in J_a,s}t_{jsu}\le1.
\tag{8}
\]

被丢的只是这一步福利计算中的非负项，不是真实组；所有其它外行 helpers 最终都回自己的 homes。(6)–(8) 是同一份共同 fractional packing，不是逐 helper 另找并拼接的 perspective flow。其 weighted fractional welfare 满足

\[
W_{\rm frac}:=\sum_{j,s,u}w_jp_{jsu}t_{jsu}
\ge\epsilon\sum_jw_jf_j
\ge\epsilon\sum_jw_jb_j
\ge\epsilon^2.
\tag{9}
\]

# 4. 均匀赢家随机实验给一半福利

这一步另造一个随机实验，未声称是原矩 Y 的真实联合分布。各 helper 独立按概率 `mu_js` 选 fallback state s，以概率 `1−f_j` 选 inactive 算法选项。选中正 mass state 后，在每个资源 u 以概率 `t_jsu/mu_js` 请求它；可令这些请求币相互独立。`mu_js=0` 时 gate 强制全部 t 为零，该 state 不参与除法。每个资源在请求 helpers 中均匀给一人；无人请求则不用。所得 fallback bundles 两两不交。

helper j 在 u 上的边际请求概率是 `sum_s t_jsu`。由 (8)，所有 helpers 的请求概率总和不超过一。固定 j 的所选 state 和自身对 u 的请求后，其他 helpers 的请求仍独立于 j 的选择；其总数 N 满足 `E[N]<=1`。对每个整数 `N>=0`，

\[
\frac1{1+N}\ge1-\frac N2.
\tag{10}
\]

N 为零或一时等号；N 至少二时右边非正。因此 j 已请求 u 条件下的平均赢率至少一半。若 `q_j` 是所选 fallback state 在实际获分配 bundle 上的价值，inactive 时设为零，则

\[
\mathbb E q_j\ge\frac12\sum_{s,u}p_{jsu}t_{jsu}
\ge\frac\epsilon2 f_j,
\qquad 0\le q_j\le1.
\tag{11}
\]

由 (5)、(7)，

\[
\mathbb E\sum_jw_jq_j\ge\epsilon^2/2.
\tag{12}
\]

这是暂时的福利下界。它没有声称所有本行 helpers 此时都有正质量，更没有把其余真实组删除。inactive 只是算法选项，不是新增原 state。

# 5. Bernoulli-count DP 精确去随机化

按固定次序逐一选定 helper state/inactive，始终只固定正概率候选。给定任意 state-prefix，尚未固定的 helper 仍独立；对每资源 u 定义

\[
r_{ju}=\Pr(j\text{ 请求 }u\mid\text{prefix}),\qquad
m_{ju}=w_j\mathbb E[p_{j,s,u}\mathbf1\{j\text{ 请求 }u\}\mid\text{prefix}].
\tag{13}
\]

这些数完全显式：尚未固定 j 时分别为 `sum_s t_jsu` 和 `w_j sum_s p_jsu t_jsu`；已固定正 mass state s 时为 `t_jsu/mu_js` 和 `w_j p_jsu t_jsu/mu_js`；inactive 时都为零。不同 helpers 的随机实验独立，所以 j 的 value/request 与其他 helpers 的请求数 `N_(-j,u)` 独立。资源 u 的均匀赢家福利的精确条件期望为

\[
\Phi_u=\sum_j m_{ju}\,
\mathbb E\frac1{1+N_{-j,u}}.
\tag{14}
\]

这里没有把 `m_ju` 错换成期望价值乘请求概率；尚未固定 state 的价值与请求可以相关。同一 helper 在不同资源上的相关性不影响逐资源期望之和。

对固定 `(j,u)`，`N_(-j,u)` 是参数为 `r_hu, h≠j` 的独立 Bernoulli 和。用 count-convolution DP 计算其分布。初值 `P_0(0)=1`，加入参数 r 时更新

\[
P_{k+1}(\ell)=(1-r)P_k(\ell)+rP_k(\ell-1),
\qquad
\mathbb E\frac1{1+N_{-j,u}}=\sum_\ell\frac{P(\ell)}{1+\ell}.
\tag{15}
\]

越界 P 取零，count 范围至多本行 helper 数。由 (14)–(15)，对每个候选正概率 state/inactive 都可精确重算 `Phi=sum_u Phi_u`。所有候选的原概率加权平均恰是当前 Phi，故至少一候选不降低 Phi；选择最大候选继续。此后不必重新主张 prefix 下请求概率总和仍不超过一：容量仅用于初始下界 (12)，后续保持的是精确条件期望。

全部 states 固定后，无须再投请求币。每个资源 u 给该资源上有正请求概率的 chosen-state helper 中 `w_jp_jsu` 最大者；无人正请求就不用。该最大值不小于剩余请求币与均匀赢家实验在 u 上的期望值，所以确定性输出的 disjoint fallback bundles 满足

\[
S:=\sum_jw_jq_j\ge\epsilon^2/2.
\tag{16}
\]

若某 selected state 对所得 bundle 有更好的原 state，可再改选以提高值；本证明不需要这一步。保留原 chosen state 已足够。

**总位复杂度。** 输入包含显式全部 states、resources、原 incidences 和 supplied rational x/Y。条件量只除以正 lambda 或正 mu，其数值倒数不成为循环界。所有 r、m 的分子分母位长由多项式个输入有理数运算控制。对固定 `(j,u)`，DP 分布的公共分母可取至多 n 个 Bernoulli 参数分母的乘积，其位长为这些分母位长之和；各概率在 [0,1]。再求 (15) 时新增公共分母可用 `n!` 控制，位长 `O(n log n)`。对全部资源、excluded helpers、显式候选 states 重算多项式次，每次 DP 只有多项式个 counts 和更新，精确比较和最后 max 分配也为多项式。没有按 `1/epsilon`、权重分母或隐式 state 组合枚举。

# 6. 阈值重组恢复所有组

令 `tau=epsilon²/4`，`R={j:q_j>=tau}`，`W_R=sum_(j∈R)w_j`。由 (16)、weights 和一以及 `q_j<=1`，

\[
\epsilon^2/2\le S\le W_R+\tau(1-W_R),
\qquad
W_R\ge\frac{\epsilon^2}{4-\epsilon^2}\ge\tau.
\tag{17}
\]

只保留 R 中 helpers 的两两不交 B-bundles，令这些 helpers 使用各自实际 chosen fallback state。outer 使用原 state a，领取 R 对应的 homes；本行其余 helpers 和**所有其它 outer states 对应的 helpers**都使用 own state、领取其独立 home。由 B 与 homes 不交、所有 homes 物理互异，这是一份真正全组 disjoint allocation。outer 质量为 `W_R>=tau`，R 中 helpers 质量至少 tau，其余 helpers 质量一。inactive helpers 不可能进入 R，故输出无需虚构 inactive state。

该重组正是单 outer 与全部非 outer 组受 own-home 保护的承重之处。若多个 outer 同时选行，分别条件化得到的 B-packing 未必能共同使用；若还有无 home auxiliary group，丢去其福利项后就无法在此恢复它。不能删除这些假设再援引 (17)。

# 7. 完整 ordinary jobs 回填

对每个真实组采用上节选定的原 indexed state，将其 unit selector 放在该 state 的原 private machine。仅将该 selected state 中实际获分配的正 incidence jobs 导出到其 exact resource machine。其余每一原 incidence job 都留在自身原 private endpoint，包括：未选 outer states 的所有 jobs、未选 helper fallback states 的所有 jobs、R 中 helper 未选 own state 的 unit incidence，以及全部零 incidence jobs。

每个未选 state-private machine 的负载仍为完整 normalized payload 一；每个 selected state-private machine 的负载为

\[
1+\left(1-q_g\right)=2-q_g\le2-\tau.
\]

disjoint allocation 保证每个 resource machine 至多承载一枚 unit incidence job；零 incidence 留 private 的时间零端点。所有原 jobs 恰好输出一次，资格来自原矩阵，没有丢 job、额外逻辑容量或拆分 job。重复 indexed states 不合并，unused resources 可空；因 `tau<=1/4`，未选 private 与 resource 的负载一也满足 (T)。输出只需扫描显式原 jobs 列表，遂得完整调度和定理。

# 8. 版本差别、关系与证据限度

本源扩充的是早期 unit-threshold 学习记录的阈值域；`epsilon=1` 时恢复质量 `1/4` 地板，早期冻结记录不因此被改写。对每个固定正 epsilon，本定理排除该精确 one-outer 架构内的 vanishing-quality 方案；当 epsilon 随输入趋零时，界本身也可趋零，不能称为一般近零 gap 排除。

与现有对象的关系如下：

| 现有对象 | 重复部分、区别和复用方式 |
|---|---|
| [one-outer13-8与primitive-SA1同点后端](../资料/one-outer13-8与primitive-SA1同点后端--资料.md) | 同一 given-point epsilon²/4 结论；其独立 Exact-first 用有限 weighted-score CDF/Bonferroni 后端，本页保留作者 uniform-winner/count-DP 的完整证明。不是新增更强定理。 |
| [单外层primitive-SA1作者read-after与count-DP审查](../审查/单外层primitive-SA1作者read-after与count-DP审查--审查.md) | 后续 read-after 直接审本源 hash 和 §1–7，确认 (3)–(17)、DP 与全部 jobs。它是知情数学审查；本页补回它所审的作者完整数学对象。 |
| [单外层normalized-flat三源精读与13-8版本边界审查](../审查/单外层normalized-flat三源精读与13-8版本边界审查--审查.md) | v1 Exact 只陈述本 given-point 合同；v2 是 typed Q-alone 的 13/8 算法，自行生成/解 LP，并换用 5/8 级 CDF 福利。不能把该 Q-only 输入量词转给本页。 |
| [单outer 13-8作者proof释放后读后与版本边界审查](../审查/单outer%2013-8作者proof释放后读后与版本边界审查--审查.md) | 13/8 作者 Proof 的 11 次 adaptive threshold LP、固定 affine margin，与独立重构的 128-grid 算法身份不同；二者均不是本页 count-DP 已执行的实现。 |
| [单外层canonical final v2全文post-read与13-8版本边界审查](../审查/单外层canonical%20final%20v2全文post-read与13-8版本边界审查--审查.md) | 后续 canonical 保持 supplied-point 与 Q-alone 两 claim，未改本页域或常数。其 NP-source corollary 依 Q-alone 13/8，不由本页自动推出。 |

现有 32 个 Fraction CDF 小例核的是独立 CDF 后端，不是作者 count-DP，也不认证 LP 构造、11 次查询或完整 scheduler 软件。本次仅完成原文及相关对象的数学阅读、比较和正文保全；没有运行作者程序、求 LP 或穷举所有物理 assignments。普通有理 DP 的算法证明不等于已有端到端 implementation。

本定理不处理多个 outer、重合 homes、无 own-home 辅助组、一般 normalized multicore、隐式指数菜单、任意 ordinary UM、near-two hardness、外部同行评审或全球新颖性。一般 UM 主目标及与之独立的六人 CAG/SPE 目标未由此闭合。
