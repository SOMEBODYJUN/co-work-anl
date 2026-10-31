# 七态原作业星：作者全文读后比较与接线边界

2026-10-18。scratch read-after 记录；不修改旧 Exact-first，不登记新 Claim，不认证软件或递归定理。

## 1. 实际阅读顺序

先仅据 `sol_seven_state_star_global_quadratic_exact_v1.md`（SHA256 `939a9b12b0dc8d74aa9809f816140b8569d6c6d091ee6fd809492256d1a0b477`）完成独立重构，并在读作者 Proof 前实际全文读后冻结：

`sol_identity_coupling_seven_state_star_exact_first_reconstruction.md`

SHA256 `7d61b211b43d03cdf3c64d16605ab745a2ef77dd1e0cf43896ff59b886f8ab86`，10797 bytes，224 lines，0444。root 随后消息确认已实际全文读该记录。旧记录已有 raw SH3/M2/旧 diluted-law 背景的披露，不冒全方向盲审。

本轮经 root 释放后，实际全文读了作者文件：

`sol_seven_state_star_global_quadratic_coercivity_learning.md`

核得 SHA256 `d560f9cf9a263d75cb1fa518a118078bcd013de91af4a8c771ced9257f3ef072`，6379 bytes，86 lines。其 §§1–7 全部实际阅读，包含 §5 外部背景话语与 §6 更高次数方向。

没有打开或运行作者代码、JSON，没有读新的 growing-depth 草稿，也没有把作者关于有限代码的描述当成我的执行证据。

## 2. 任意全局二次 q：作者证明有效

作者先将全部原端点代成 C、1−C、Y_j、1−Y_j，再对 home-job 标签置换平均。对该明确原矩，所有其他原变量确实已列尽；这不是遗漏其他机器变量后的局部投影。

Boolean 化简后的任意原次数≤2 多项式的置换平均是

\[
\bar q(C,H)=P(H)+C(a+bH),\qquad\deg P\le2.
\]

所以 active 与 inactive 两支的二次系数相同。每个正余量 (C,H) 类别内 Jensen 给 E(q²|C,H)≥bar q(C,H)²；唯一负余量类别 C=1,H=d 只有一个 home 集，置换平均保持 q 的实际值。因此只控制对称均值足以控制所有全局、非对称、任意实系数二次 q。

令 λ=d/h=2/η≥4。作者五点评估恒等式逐项展开正确，五系数的平方和为

\[
2\lambda^2+2(1-\lambda)^2+1
=4\lambda^2-4\lambda+3\le4\lambda^2=16/\eta^2.
\]

五个正状态的质量乘 slack 都至少 η/40；特别 inactive H=d 的权重 eη>0.79η。坏质量满足

\[
p(1-\eta)\frac{16}{\eta^2}
\le\frac{16\eta}{1000}<\frac{\eta}{40}.
\]

所以作者的普通 Cauchy 估计已足够，不存在全局维数因子。与我的 Exact-first 加权 Cauchy 界 S<321η^−3 相容；作者较粗的估计相当于 S≤640η^−3，仍有严格余量。两套证明都只声称 PSD，不能声称在含原 one-hot/Boolean 零向量的 monomial 基中有统一正最小特征值。

原 u、z_j 行逐样本负载≤1，所以同一个全局 q 在这些行也通过。作者的全部全局二次局部化结论在 Exact 原矩上成立。

## 3. 原单位端点、全部 jobs 与共同矩

R 是同一枚原 job，C 与 1−C 是它的两原端点；每枚 j 是自己的 Y_j 与 1−Y_j。两个 unit 端的处理时间都实际写为一；不是 pinned arrival 或匿名读口。

每个七态样本完整分配所有 d+1 枚原 jobs。故 L 是一个真实 assignment law，其 M3 以及所有定义出的更高共同 Gram 矩阵自动 PSD，所有原 Boolean/one-hot 等式逐样本成立。这不依赖 SDP 计算或未知可行调度。

实际 OPT=1：全部 jobs 回所定义 home 给负载一；R 只能用时一，又给下界一。P 中的峰二坏样本不把这个小实例变成实际 gap。

## 4. 完整 row CONFIG first/pair 与位复杂度

作者合法 v 行 law 的质量及支持与 Exact 相同。active H 取 s、0、h，inactive H 取 0、h、d，全部在 CONFIG(T) 内。

用均匀子集，v 行全体原 first/pair 恰由 E(C)、E(H)、E(CH)、E[H(H−1)] 决定。前三级统计量匹配；最后一级的损失/增量是

\[
-p d(d-s)+u_0d^2/4=0,
\]

因为 u_0=4p(1−η)、s=ηd。包括对角 pair，全部原端点都覆盖。u、z_j 的配置 law 是真实单 job Bernoulli 边际，不需要多机共同配置支持。

作者给的 (H)_t/(d)_t 公式生成不同 home 指标的矩；互补端点通过固定次数的仿射展开同样覆盖。我的 Exact-first 更直接写出的 (H)_a(d−H)_b/(d)_{a+b} 亦给全部原 endpoint monomials。参数及固定次数矩的 numerator/denominator 位长 O_D(log d)，共 O_D(d^D) 个矩，故固定 D 的全部矩、M3、所有全局二次负载局部化矩阵、row first/pair 都可按显式原输入长度在确定性多项式总位成本内生成。没有指数支持枚举或精确 SDP finder。

§7 所提有限代码检查，我没有读或执行；本记录不认证其参数清单、输出或实现正确性。

## 5. §5 外部背景只能按单行合同使用

作者 §5 的最后一段明确保留父行/孩子行收费义务。我认可其单行 v 插值合同：逐背景固定其他原 assignment 指示，改变 C,Y 时完整原指示向量仿射于这些变量，且被检验 v 的负载公式仍是 C+H/d；那么任意全局 q 的系数可依背景变化，前面的同一个常数估计逐背景成立，再积分也成立。

“背景固定”本身不保证保留这个负载公式。若 v 另有固定负载 b_v，却仍用 T=1+η，则 slack 变成原 slack−b_v，必须另付预算或改变阈值，不能直接套作者 §4。例如 d=4,s=2，原 P 有 E(load_v)=37/40；额外在 v 固定一单位原 job 后，q=1 已给 E(T−load_v)=−17/40。此例不是原 Exact 的实例，只说明任何扩写的背景合同须明确 v 上没有未收费的固定额外负载。

即使 v 保持原公式，其余行也不能自动接成内部节点。若在某个 z_j 增加固定背景负载 b>η，保留原七态 law，则原 q=1−Y_j（次数一）给

\[
L[(T-\operatorname{load}_{z_j})(1-Y_j)^2]
=(\eta-b)L(1-Y_j)<0.
\]

同理，u 加固定负载 b>η 时，q=1−C 立刻给负值。它们在原小星不发生，因为这些机器无其他 payload。让内部孩子主动导出 payload、让 R 返回上游后触发其他 jobs，都需要新的共同证明；仿射 q 插值不支付这些行的 slack。

原 unit 导出位置也不能随意合并：若 z_j=z_k（j≠k），则同机两 unit endpoints 的 pair 至少 Pr(H=0)=1/10>0，无法匹配 T<2 的 CONFIG pair；若 u=z_j，则相同 pair 至少 Pr(C=0,H=0)=1/20>0。这些只是边界检查，不是对 Exact 的反例；Exact 中这些机器全部不同。

因此 §5 应明确理解为单行噪声控制及原 assignment 的可表达性，不能升级为任意外部背景下的所有行共同可行点。作者末段已有相应保留；若后来进入正式正文，建议把“保持 v 原负载公式”在应用合同里直接写明。

## 6. 更高次数段落与最终判断

§6 中 active-minus-inactive 的次数≤D−1 是正确的形式观察，固定 D 的分离节点可导向 Lagrange 估计。但作者已将它列为方向，没有给完整常数、全部 row trade、节点选择、递归预算；本记录不把它升格为已证明的新 Exact 或算法。

对所释放七态 Exact 的全部正式陈述，没有发现 fatal；作者 Proof 与此前独立重构吻合。对正文额外接线话语，以上明确保留单行公式和所有其他原机器预算，不认证任何未写递归。该对象仍是实际 OPT=1 的局部噪声构件，既不是 near-two 整数 gap，也不是 hardness 或一般求解器。

旧 Exact-first 字节保持不变。本文只是实际全文读后比较，不回填、改称或扩大此前独立性；未外审，未签未读软件。
