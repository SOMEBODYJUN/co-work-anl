---
id: "unrelated-machines/single-outer-canonical-final-post-read-v2-review"
kind: review
type_tag: 审查
title: "单外层 canonical final v2 全文 post-read 与 13/8 版本边界审查"
status: integrated
truth_status: "canonical-post-read-consistent-with-typed-13-8-and-supplied-point-claims"
review_level: "full-read-10691-byte-post-read-cross-archive-comparison"
scope: "sol_single_outer_canonical_final_post_read_v2.md, canonical one-outer 13/8 final, supplied-point primitive-SA1, Q-only Proof, count-DP/CDF backends and hardness-source boundary"
summary: "13fb650… 是对 8c5fcf… canonical final v2 的最终全文 post-read 记录。本文完整读取 374 行/10691 字节记录，核对其对两个正式 claim（给定 primitive-SA1 的 epsilon²/4 与 typed-Q-alone 的 13/8）、完整 ordinary P/OPT=2−V、两种福利后端、11 次二分、总位复杂度、全原 jobs 回填及 NP-source corollary 的最终复核；与仓内单外层 Exact/Proof/read-after、primitive-SA1 count-DP、多outer backend 和 gated-menu 13/8 对象去重，不建立第三个算法或一般 UM 结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_single_outer_canonical_final_post_read_v2.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_single_outer_canonical_final_post_read_v2.md"
  - "related-source:3858f37087ca3c8a80f0:history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_approximation_exact_v2.md"
  - "related-source:47c955a8da722b2e7a1c:history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_author_proof_v2.md"
  - "related-source:0f20dfac4647048db69c:history/source/notes/unrelated_machines/one_outer_full_primitive_sa1_rounding_exact_v1.md"
related_objects:
  - "单外层normalized-flat三源精读与13-8版本边界审查--审查.md"
  - "单外层primitive-SA1作者read-after与count-DP审查--审查.md"
  - "单outer 13-8作者proof释放后读后与版本边界审查--审查.md"
  - "多outer single-state tiny-home 19-10 Exact-only与proof-canonical-backend版本审查--审查.md"
  - "归一化门菜单v2三源精读与13-8算法版本审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/single-outer-canonical-final-post-read-v2-20261031/original/sol_single_outer_canonical_final_post_read_v2.md"
source_sha256: "81491b420b5054782a48e085109ddc510b03780d473cbbc84aa6e783acdb6eb9"
source_size: 10691
---

# 1. canonical final post-read 身份与冻结对象

本轮完整读取 13fb6509d9bb4fba20fd 的 post-read 记录，10691 字节，SHA-256 为 81491b420b5054782a48e085109ddc510b03780d473cbbc84aa6e783acdb6eb9。该记录说明其完整读取了标题、开头、身份表和 §1–12，没有以摘要或局部 diff 代替全文；记录对应的 canonical 正文是 single_outer_shared_selector_rounding_and_hardness_source_boundary_final_v2.md，SHA-256 8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221，实际 374 行。

本页保存的是 post-read 记录原字节。canonical 正文的数学身份以该记录内给出的 hash 和仓内既有单外层 Exact/Proof 审查为准；不将 canonical 末尾 review 链接或旧 hash 代作本轮重新读取未导出的其它文件。post-read 作者此前已读给定-point Exact、作者 read-after 和 typed-Q 13/8 独立重构，因此本轮属于知情后的最终 canonical 复核，不是新的 blind review 或外部同行审查。

# 2. 两个正式 claim 的分离

canonical final 保持两种算法身份：

## 2.1 supplied-point primitive-SA1

UM-SINGLE-OUTER-PRIMITIVE-SA1-EPS2-4-v1 接收 typed Q、正有理 epsilon<=1 和同一个完整共同 primitive-SA1 有理点。结论是实际不交 allocation 的最低质量至少 epsilon²/4，并回填完整 ordinary jobs 得到 Cmax<=2−epsilon²/4。位复杂度对这三项完整编码计；该 claim 不负责从 Q 生成可行点。

其物理域是单 outer、所有 state 正 homes 在全索引中物理互异、每 home 一个 own-singleton helper、fallback B 与 homes 分离、无其它组。fallback 可以跨 helper 共享或不存在；零 incidence、重复 indexed states、unused resources 和未选 state jobs 都保留。

## 2.2 typed-Q-alone 13/8

UM-SINGLE-OUTER-TYPED-13-8-v1 只接收显式 typed Q，由自身生成普通矩阵、内部 LP、11 次阈值查询和至多一次 CDF 舍入，输出全部原 jobs 的 assignment，满足 Cmax <= (13/8)OPT(P(Q))。位复杂度对 Q 本身计，不输入 OPT、福利分配、primitive-SA1 点、actual oracle 或精度参数。

两个 claim 都只在单 outer、互异 homes、own helper、shared fallback B、无其它 group 的 typed 域成立；不识别任意普通矩阵，也不迁移到多 outer、home 重合、隐式菜单或一般 UM。canonical final 没有把 supplied-point 的 count-DP 与 Q-only 的 11 次 LP 混成一个 claim。

# 3. 完整 ordinary P 和 OPT=2−V

canonical §2–3 的物理对象是每 group 一个 selector、每 listed incidence 一个不可拆 job、每 indexed state 一台 private machine，规模为 S+U 台机器、G+I jobs、S+2I 有限资格单元。零 incidence 仍作为 private 零端点，未选 state payload、重复索引和 unused resources 不删除。

定义 V 为不交资源 bundles 上最小 group welfare 的最大化。完整真实 assignments 满足

1 <= OPT(P(Q)) = 2 − V <= 2。

正向把选中 state 的正 allocated incidences 导出 resource machines，selector 放 selected private，所有其它 jobs 留 private；反向若 C<2，unit resource machine 至多接一枚 incidence，selector 所在原 state 的 selected-private 负载读出 disjoint bundle，质量至少 2−C。未选 state 的 exports 可还原到 private 而不抬高峰值；OPT=2 时 V=0 边界也闭合。

unit selector 给出非空域下 OPT>=1。canonical 没有把空任务/零 OPT 的一般 UM 情形悄然纳入。

# 4. LP、FAIL 语义和同一条件点

每次阈值查询都显式包含全部 A/Z binary primitives、boxes、nonnegative/gates、resource capacities、state partitions 和 perspective qualities，并乘每个原 primitive 与补，统一在一个对称二阶数组中，binary diagonal 合并。无 PSD、额外 unit-FSLP、未知 joint law 或高阶 oracle。变量和约束数随显式 Q 多项式增长，标准确定性有理 LP 可以返回精确点或精确 infeasible。

真实 quality>=epsilon 的 allocation 提供 rank-one 0/1 可行点，因此 LP infeasible 才推出 V<epsilon；FAIL 不等于 timeout 或数值 solver 未找到解。epsilon monotonicity、mu_A/Y_AF 闭合均由相同 box/gate lifts 给出；feasible 下端点不必小于 V，算法只使用必要性方向。

own singleton 即便携带零 incidences，乘 1−Z 后仍有 mu_A<=Y_AZ，boxes/gates 给 Y_AZ<=mu_Z<=mu_A；同一 gate 与 F/补相乘导出 Y_AF=Y_ZF，不使用 triple。选一个正 marginal state 只条件化一次，所有 fallback claims 来自同一 conditioned row。无 fallback helper 的 f_j=b_j=0，alpha=0 不除法；删除其它 helper claims 只放松资源行。由 f_j>=b_j 和 weighted home mass 得 Wf>=epsilon²。

# 5. 两种 welfare 后端的最终复核

## 5.1 Uniform-winner/count-DP（supplied-point）

给定 state/request 后，其他 helpers 的请求独立于 j，期望请求数不超过 1。整数不等式 1/(1+T)>=1−T/2 给每个正请求至少一半的均匀赢家质量，得到 W>=epsilon²/2。公式同时保留请求概率和 weighted value-request mass，即使未固定 state 的 value 与 request 相关也不破坏分解。

Bernoulli count-DP 对每资源、逐 excluded helper 计算 E[1/(1+N)]；固定 state 后选择正请求者中最大 w_j p_jsu 的 helper，支配均匀赢家实验。Good 阈值 tau=epsilon²/4 给 home mass z>=(epsilon²)/(4−epsilon²)>=tau。未选行、其它 outer rows、zero/duplicate jobs 和 unused resources 均按原 private/home 端点回填。

## 5.2 CDF-max（Q-only 13/8）

CDF 后端只在初始 fractional packing 中使用 beta 总量<=1。score level d 的跨 helper 独立请求给

1−product_j(1−beta_j(d)) >= (1−1/e) sum_j beta_j(d) > (5/8)sum_j beta_j(d)。

有限 score levels 积分得到 W>(5/8)epsilon²。条件期望阶段不能继续假设条件后的请求总量<=1；canonical 复核确认它改用有限 score product 重新计算，并在最终每资源选择原 chosen-state 的最大请求系数，支配剩余 request experiment。

两后端数学上都闭合，但实现身份不同：count-DP 不获得 CDF 的新常数；已有 CDF 小审计不认证 count-DP。canonical 的 Software=None、无 11-LP 端到端实现说明准确。

# 6. 13/8 仿射质量线与二分边界

canonical 固定

a=13/8，b=10/8，d=1/256，q0=a epsilon−b，q=q0+d。

恒等式为

(5/8)epsilon²−(2q0−q0²)
= (209epsilon²−468epsilon+260)/64。

在 [0,1] 上分子递减、最小值为 1，基础余量为 1/64。q>0 给 q0>−d，平移消耗严格小于 2d+d²=513/65536，相对 1/64=1024/65536 留有严格余量；q<97/256<1。若 Good home mass z<=q，则 W<=z+q(1−z)<=2q−q² 与严格福利矛盾，故 z>q，回填峰值 C<=2−q。

Q-only 查询从 l=0,h=1 开始，恰 11 次正 dyadic midpoint。FAIL 时 V<midpoint 并降低 h；feasible 时保存点并抬高 l，唯一安全不变量是 V<=h，feasible l 可以超过 V。结束 h−l=1/2048。

q<=0 时，aV−b<=−d+a eta=−51/16384<0，故 V<10/13，baseline C<=2 满足严格 13/8 比率。q>0 时，l 来自真实 feasible query，q>=aV−b+51/16384，从而 C<(13/8)OPT。不存在第 12 次 epsilon=1 查询，不生成 epsilon=0 点，也不需要真实 objective oracle。

# 7. 完整 jobs、复杂度与 NP-source corollary

canonical §10 明确恢复 selector、selected private、unselected private、resource loads 和全部 original incidences。zero jobs 留 private 零端，duplicate indexed states 不合并，unused machines 仍在模型中；无被丢弃 helper、guard 或逻辑容量。

标准 rational LP、正 marginal state 枚举、一次 CDF/DP、有限 score levels 和原 jobs 回填均按显式输入长度计算。倒数只作为有理编码进入运算，不作为循环界；count-DP 的 1/(1+t) 可用 factorial 公共分母控制位长，CDF products 只包含多项式个因子。canonical 没有将一般 arithmetic circuit 的多项式操作数自动当成多项式位长。

§11 的 hardness-source corollary 只针对 typed presentation 的真实 promise：固定 0<delta<3/8，YES 是完整 OPT=1，NO 是完整 OPT>=2−delta>13/8。若某 NP-hard 语言总位多项式归约到此 typed 域，运行 13/8 算法并计算实际 makespan 会区分两类；因此在 P 不等于 NP 下该特定结构不能承载此真实近二 source。它没有推出一般 UM 困难性，也没有把固定 selector 的局部坏负载当作真实 NO。

若另给 R_1 完整点，绝对 7/4 与 415/256 是 supplied-point 的直接上界，不能替换 Q-only 算法。canonical 明确 delta 严格在范围内，不把等号端点扩写为算法合同。

# 8. 与全仓对象的去重与最终范围

本记录与单外层 normalized-flat 三源审查的重复主链是：v1 supplied-point epsilon²/4、v2 typed-Q 13/8、OPT=2−V、primitive-SA1/二分、CDF/回填和完整 jobs。独有内容是 canonical final v2 的 §1–12 逐式 post-read 复核、count-DP 与 CDF 后端的相互独立、11 次查询细节、FAIL 不变量、NP-source corollary 和 final wording 边界。本页不创建第三份 13/8 theorem。

与 primitive-SA1 author read-after：其 count-DP 是 supplied-point claim 的后端；canonical 的 CDF 是 Q-only 13/8 claim 的后端。两者共享 singleton closure 但输入量词不同。与多outer tiny-home 19/10：后者是 k 可变、1/(4096k^4) tiny-home、多 outer、MW/整块方差/双资源 CE 的相邻 typed 对象，不能迁移为单 outer 13/8，也不反向证明它。与 gated-menu 13/8：数值相同但 P_gate、group/allocation 量词和对象身份不同。

post-read 未发现 8c5fcf 正文数学或量词 fatal；本记录不要求修改 canonical。它也不认证未打开的生产代码、外部同行评审、全局新颖性或一般 UM-TARGET-v1。多人共享、多 outer、深层菜单、重合 homes 和一般 UM 仍是开放范围。

