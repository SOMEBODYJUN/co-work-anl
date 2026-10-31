# 单 outer 13/8：作者证明释放后的独立读后记录

日期：2026-10-18。审查者：`/root/sol_general_repair`。本记录为 scratch 后置核对，不改变一般 UM-TARGET-v1 的 OPEN 状态。

## 1. 读取范围、顺序与冻结对象

我在作者证明释放前已独立重构同一 Exact，冻结于：

- Exact：`one_outer_normalized_flat_13_8_approximation_exact_v2.md`，SHA256 `81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69`。
- 独立记录：`sol_one_outer_13_8_exact_first_reconstruction.md`，SHA256 `399c6b29f54b1c0f49ee21e3ef64552edc1fec21fe09579a4dd91eecb5fe710f`。

现已实际完整读取作者证明 §1–6：`one_outer_normalized_flat_13_8_author_proof_v2.md`，SHA256 `2a6af63654c9ec36a3a83da47b4cdb95065aa298012369cf7c87dbfa5f226eaf`，并重读 Exact。作者证明实际使用 **11 次二分、固定仿射质量线**；我的 Exact-first 重构实际使用 **128 点网格、枚举实际 fallback 质量阈值**。这是满足同一输入输出 Exact 的两种算法，不能互换算法身份或软件验证范围。

我此前熟悉一般 primitive SA1、Q_t、单 outer 的 singleton closure，并曾独立重构 supplied-point 的 epsilon-squared 定理；这不是无背景盲审。当前读取发生于独立记录冻结、root 实读后释放作者证明之后。原独立记录字节保持不变。

## 2. 作者算法的合同与 LP

输入仅为 Exact 中显式 typed Q：一个 outer；每个 outer state 的 homes 在所有行中互异；每个 home 有一位 own-singleton helper；任意 normalized fallback states 仅使用与 homes 不交的 B。没有其他组。构造完整普通矩阵 P(Q)，保留原 selector、全部 listed incidences、零、重复 indexed states 与 unused resources。

作者使用的每次查询是显式标准有理 LP：原 A/Z binary primitives 的共同对称二阶数组，state partition、box、gate、resource capacity、perspective quality 各原线性行及其乘每个原 primitive/补。无 PSD、无额外 unit-FSLP、无实际分配 oracle、无高阶条件化接口。若把 base 行写成 h=c+sum_i a_i X_i>=0，其两类 lift 恰为

    c mu_t + sum_i a_i Y_it >= 0,
    c(1-mu_t) + sum_i a_i(mu_i-Y_it) >= 0.

LP 变量数为原 primitive 数的平方量级，显式行数亦为多项式。标准确定性有理 LP 的可行点编码长度与求解位复杂度为输入规模的多项式；11 个 threshold 只含至多 11 位二进制小数。

实际质量 V 的完整分配给出 rank-one 0/1 可行点，故 infeasible(epsilon) => V<epsilon。作者只使用这个方向，未把 feasible 当实际分配，亦未假设 feasible lower endpoint 必须 <=V。原矩阵的完整 flat 身份 OPT=2-V 适用于此规范化、保留全部任务的域；1<=OPT<=2。

## 3. 一次条件化与 CDF backend

own-singleton 的质量行乘 1-Z，结合 gate/box，强制 mu_A=mu_Z=Y_AZ。对每个原 F，gate A-Z 分别乘 F、1-F，再用边际差为零，得到 Y_AF=Y_ZF。这里没有 triple。

选正边际 outer state a，并仅条件化其 primitive 一次。该同一 row 的 state partition、gate、quality、resource rows，连同上述 singleton 闭合，给出作者列出的 alpha、zeta、f、b packing。特别是所有 fallback helper 的资源列由共同 conditioned resource row 控制，非从不同局部点拼接。由 sum_j w_j b_j>=epsilon、f_j>=b_j，以及每个 fallback quality 行可得

    Wf=sum_(j,s,u) w_j p_jsu zeta_jsu >= epsilon^2 > 0.

作者的 CDF-max 概率实验在 helper 之间独立选 state，在给定 state 下请求单个资源的概率为 zeta/alpha；alpha=0 时该 state 不列入候选且 zeta=0。不同资源间请求相关性可以任意，因所需 welfare 期望逐资源求和。对每个资源和正 score level d，beta_j(d) 的总和 r<=1，因此

    1-product_j(1-beta_j) >= 1-exp(-r) >= (1-1/e)r.

最后一步在 r in [0,1] 由凹性。积分为有限有理 score-layer 求和。e>8/3，故 1-1/e>5/8；结合 Wf>0，作者得到严格 W>(5/8)epsilon^2。该常数只用于分析，不要求计算或比较 e。

确定性实现逐 helper 枚举原正概率 state/empty option，以有限 CDF product 精确计算 conditional expectation；选择最大者不降低期望。全 state 固定后，各资源直接给 chosen-state 中加权系数最大者，逐资源支配剩余 request 实验。实际 chosen-state Q_j in [0,1]。empty 仅为算法选项，非新增物理 state。

位复杂度可直接按原 rational alpha、zeta、w、p 表达计算：每个 CDF 值是多项式个有理因子的乘积及有限和，层数、helper 数、候选数均显式多项式；无需展开所有 state 组合，也不把数值倒数作为循环次数。选择状态的条件期望计算可以每次从原因子重新形成，故不会产生递归表达式倍增。

## 4. 仿射质量线与严格余量

令 a=13/8，b=10/8，d=1/256，q0=a epsilon-b，q=q0+d。作者使用的恒等式确为

    (5/8)epsilon^2-(2q0-q0^2)
      = (209epsilon^2-468epsilon+260)/64.

在 [0,1] 上分子导数 418epsilon-468<=-50，因此最小值在 1，值为 1。基础余量至少 1/64。

在 q>0 分支，q0>-d，而 epsilon<=1 给 q<=3/8+d=97/256<1。仿射平移所增加的量为

    (2q-q^2)-(2q0-q0^2)=2d(1-q0)-d^2 < 2d+d^2.

其中 2d+d^2=513/65536<1/64=1024/65536，至少还保留 511/65536 的严格安全余量。因此 (5/8)epsilon^2>2q-q^2 的结论成立。此处 q0 可能为负，作者显式使用 q>0 才取得 q0>-d，未把负分支套入错误的非负阈值论证。

Good={j:Q_j>=q}、z=sum_Good w_j。有 W<=z+q(1-z)。因为 0<q<1，若 z<=q，则右侧<=2q-q^2，与已得严格 welfare 矛盾。因此 z>q。outer 取 Good 的 homes，Good 保留 fallback 资源；当前行其余及其他全部行的 helper 返回各自互异 home。B 与 homes 不交；只使用一个 outer state。于是所有组达到至少 q。q>0 还排除 Good 的 empty option。

## 5. 11 次二分的未知 V 合同

初始 l=0,h=1；每次 exact LP 查询 midpoint，feasible 更新 l 并保存对应点，否则更新 h。真正需要的不变量仅是 V<=h：初始成立，infeasible 更新时由 V<midpoint 保持。feasible 的 l 可以超过 V；这不破坏该不变量。

11 次后 h-l=eta=1/2048，故 l>=V-eta。算法无需生成 epsilon=0 的点。最终 q=a l-b+d。

- 若 q<=0，aV-b<=q-d+a eta<=-d+a eta<0，故 V<10/13，显式全 private baseline 的 C<=2 已满足 C<(13/8)(2-V)。
- 若 q>0，则 l>0，最后的 l 必来自某次 feasible 查询，保存点确实存在。应用一次 rounding，C<=2-q，而

      q>=aV-b+d-a eta,
      d-a eta=51/16384>0.

  因此 C<(13/8)(2-V)=(13/8)OPT。

两分支均不依赖 LP feasibility 阈值等于实际 V。作者未以当前 LP 的虚假 feasible 上界代替真实 OPT，也未使用目标值 oracle。若所有正查询均 infeasible，则 l=0，自动落入安全 fallback。

## 6. 完整任务回填、比较与结论

选定每组的原 state 并构造 disjoint bundles 后，只有选定 state 的获分配正 incidence jobs 去 exact resource；该组 selector 去其选定 state-private machine；所有其他原 incidence jobs，包括未选 state、listed zero，留在自己的 private endpoint。private load 为选定行 2-value、其余行 1；资源 load<=1。每个原任务恰出现一次，duplicate indexed state 不合并，unused resources 不删除。

我的原独立算法以固定 128 个 LP threshold、有限 AMGM 的 5/8 backend 下界、枚举实际 Q_j 阈值闭合，分析余量为 3/512；作者算法以 11 个 adaptive LP threshold、CDF 的严格 1-1/e>5/8 下界、固定仿射 q 闭合，使用上述 511/65536 与 51/16384 余量。两套数学算法分别满足同一 13/8 Exact；不能把我的网格调度或实际阈值枚举说成作者实际算法。

本轮只做数学重构后的作者全文读后核对，没有执行作者 11 次 LP 算法或完整 P 构造程序。此前 32 个小型 Fraction CDF 检查只覆盖我独立 backend 的有限实例，不覆盖此次整套算法、作者 11 次二分或所有输入，也不构成 5/8 常数的软件认证。标准有理 LP 是显式可调用的多项式 backend 定理，并非已运行的 repo 实现。

结论：对 Exact 限定的 typed one-outer 全输入域，作者 §1–6 的数学算法与 total-bit 论证未发现 fatal；其 13/8 结论可由该证明独立核对成立。该结论不扩展到多 outer、任意菜单或任意 unrelated 矩阵，不识别结构，不升级任何旧软件验证、旧 review、novelty 或一般主目标。
