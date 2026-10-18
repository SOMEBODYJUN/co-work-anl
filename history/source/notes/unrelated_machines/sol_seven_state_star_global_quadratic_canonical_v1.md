# 七态原作业星：共同二次负载检验的局部核

ClaimVersion: UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v1

2026-10-18，scratch 正文草稿。对象是实际 OPT=1 的完整普通原矩。下述结论不声称递归接线或实际 near-two gap；证明使用对称化、有限点评估与 Cauchy 不等式。

## 1. 精确原矩与结论

令 d,s 为正偶数，2<=s<=d/2；置 eta=s/d、h=s/2、T=1+eta。机器为 u,v,z_1,...,z_d。全部原 jobs 是 R,j_1,...,j_d，其有限时间恰为

    p_(u,R)=p_(v,R)=1,
    p_(v,j_l)=1/d, p_(z_l,j_l)=1，1<=l<=d.

其余时间无穷。共 d+2 台机器、d+1 枚独立不可拆原 job、2(d+1) 个有限条目；所有调度完整分配所有原 jobs。

记 C=1 当 R 在 v，Y_l=1 当 j_l 在 v，H=sum_l Y_l。全部原端点指示为 C,1-C,Y_l,1-Y_l。定义

    p=eta^3/1000,
    u0=4p(1-eta),
    e=4/5-p-u0.

下面的真实完整 assignment law P，在每个 H 类别中均匀选大小 H 的 home 集：

| C | H | 质量 |
|---|---|---|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

对全部原端点变量 X，令 L[f]=E_P[f(X)]。则：

1. L 的共同次数六矩给 M3(L) 正半定，并满足所有原 Boolean、原 job one-hot 等式；所有矩来自同一个真实完整 assignment law。
2. 每台机器 i 与任意全局实多项式 q(X)，只要 deg q<=2，均有 L[(T-load_i)q^2]>=0。q 可使用任意机器和原 job 的端点变量。
3. 每台机器均有支持在完整 CONFIG(T) 上的配置分布，与 L 的该行全部原端点 first/pair 矩精确一致，包括对角项。
4. 输入的实际 OPT=1。P 以正概率 p 产生峰值二样本；它不声称其自身逐点满足 makespan T。

## 2. 原 assignment、边界与共同 PSD

全部质量为正、总和为一；eta<=1/2 给 p<=1/8000，e>0.79。每次抽样把 R、每枚 j_l 各放在恰一个有限原端点，实际负载是

    load_u=1-C,
    load_v=C+H/d,
    load_(z_l)=1-Y_l.

所以非 v 行在每个样本负载均至多一。把 R 放 u、全部 j_l 留 v 给完整峰值一调度；R 在任何有限端点处理时间都是一，故实际 OPT=1。P 中只有类别 (C,H)=(1,d) 的 v 负载超过 T，该类别负载恰为二。

任意次数至多三的多项式 a 都满足 L[a^2]>=0，故共同 M3 PSD。Boolean 和每个原 job 的 one-hot 在每个样本精确成立，因而相应所有已定义矩等式也成立。

## 3. 合法完整行配置的精确 pair trade

对 v 使用以下另一配置分布 K_v，每类仍取均匀 H-subset：

| C | H | 质量 |
|---|---|---|
| 1 | s | p/eta |
| 1 | 0 | 1/20+p-p/eta |
| 1 | h | 1/20 |
| 0 | 0 | 1/20+u0/2 |
| 0 | h | 1/20 |
| 0 | d | e+u0/2 |

这些质量非负、总和一。active 配置 H<=s，inactive 配置 H<=d，故负载至多 T。由 exchangeability，一行全部 C、Y_l 的 first/pair 只需核 C,H,CH,H(H-1)。

将 P 的 active bad 质量 p 改到 active H=s、质量 p/eta，并用 active H=0 平衡质量，保持 C,H,CH；它使 H(H-1) 减少 p d(d-s)。将 inactive H=d/2 的质量 u0 平分到 inactive H=0,d，保持总质量和 H，且增加 H(H-1) 数量 u0 d^2/4。由 u0=4p(1-eta)，两个数量相等。其余类别不变，故全部 original first/pair 精确匹配。

u 行只有一枚可见原 job R；z_l 行只有一枚可见原 job j_l。其真实 Bernoulli 边际本身就是合法 CONFIG(T) 分布，并匹配该行 first/pair。以上逐行配置 law 不被冒称为另一个共同 assignment law。

## 4. 所有全局 q 的二次负载局部化

在本原矩中，全部原端点变量仿射于 C,Y_1,...,Y_d。因此任意全局 deg q<=2 的多项式仍是这些变量的次数至多二多项式。

对所有 home 标签置换作平均得到 bar q。每个类别的 slack g=T-load_v 是常数。在 g>=0 的类别，Jensen 给 E[q^2|C,H]>=bar q(C,H)^2；唯一负类别 Y 全一，不受置换影响。因此只需核对称化多项式。Boolean 化简后它恰可写为

    bar q(C,H)=P(H)+C(a+bH)，deg P<=2.

记 q_a(x)=bar q(1,x)、q_i(x)=bar q(0,x)，lambda=d/h=2/eta。active-minus-inactive 为仿射函数，故精确有

    q_a(d)=lambda q_a(h)+(1-lambda)q_a(0)
             +q_i(d)-lambda q_i(h)-(1-lambda)q_i(0).

五个系数平方和为 4lambda^2-4lambda+3<=16/eta^2。五个右侧类别的质量乘 slack 各至少 eta/40；其中 inactive H=d 类别使用 e>0.79。Cauchy 因而给

    p(1-eta) q_a(d)^2
      <= (16p(1-eta)/eta^2) sum_(five classes) q_class^2
      <= (16eta/1000) sum_(five classes) q_class^2
      <  (eta/40) sum_(five classes) q_class^2.

其余 inactive H=d/2 类别的贡献非负，故 L[g q^2]>=0。非 v 行的 slack 在 P 每个样本非负，直接得到它们的全部全局 q 局部化。所有机器在这一步使用同一个 L。

## 5. 可用的背景接口及其准确限制

固定一个外部背景 b，设同一完整普通原矩的全部原 assignment 指示可写为 Phi_b(C,Y)，每个坐标均仿射于 C,Y。要求 P 支持上的每个 Phi_b(C,Y) 都是真实完整 assignment，且指定行 v 的可见原 jobs 恰为某枚 R 与 d 枚指定 payload jobs，端点指示仍恰为 C,Y_l；在 v 没有新增 payload。因此 v 的实际负载仍是 C+H/d。

在该合同下，任意全局 deg q<=2 的 q(Phi_b(C,Y)) 仍为局部 deg<=2，故第 4 节逐背景给 v 的全部负载局部化。第 3 节的配置 trade 也逐背景给 v 的 original first/pair 匹配。若 b 随机，须对每个 b 使用同一参数的 P，才能直接积分这项结论。

这项背景接口只自动证明指定行 v。新背景中 u、各导出头及其他机器的负载、原 job 覆盖和配置矩都须由完整 Phi_b 及单独论证核实；第 4 节不替它们承担新增负载。只有当其他行逐点 load<=T，或已另证其共同负载局部化与配置匹配时，才能宣称扩展输入满足全部行条件。

例如在某 z_l 上加入固定 payload b0>eta 而其余公式不变，取 q=1-Y_l 即有

    L[(T-load_(z_l))q^2]=(eta-b0)P(Y_l=0)<0.

所以将 z_l 改为有自有 payload 的内部孩子不能免费接线。直接将不同 z_l,z_j 合并也会出现正概率的两个 unit jobs 同头，而 T<2 的完整 CONFIG pair 不允许它。这里没有递归 shared-head 定理。

## 6. 总位复杂度与实际审计范围

所有参数和概率均为显式二进制有理数。给定 H 类别，t 个不同 home 指示乘积的期望是 (H)_t/(d)_t；补端点用有限展开，冲突 one-hot 单项式为零。因此任意固定次数 D 的全部共同矩可在显式原输入总位长的确定性多项式时间与位长内精确生成。D=6 足以列出本合同全部 M3 与二次负载矩阵；行配置 first/pair 同理。这里没有枚举所有子集，也没有优化或精确 SDP oracle。

实际 Fraction 审计代码为 sol_seven_state_star_quadratic_audit.py，129 行，SHA256 86d05b9013dda128a753f610eaeb9eec4146212c34fa9afcd2bbea3ccab382bd。它检查 12 组参数，及其中 3 组完整 small M3、全部 global q2 负载矩阵（最大分别 130、46 维）。实际输出 sol_seven_state_star_quadratic_audit.json 的 SHA256 为 9be19dec14e2abdb97377175372f63cbe47c08414e52516de5cc65cd74599335；root 已独立 fresh-output 重放得到同字节。有限审计没有代替上面的任意 d,s 证明，也没有检查 growing-depth 接线。

原作者稿 sol_seven_state_star_global_quadratic_coercivity_learning.md（SHA256 d560f9cf9a263d75cb1fa518a118078bcd013de91af4a8c771ced9257f3ef072）保留原字节。本文为其局部定理的自足重整，未纳入高 D 插值猜想或未完成的跨行 law；新正文仍待 root 实际 final-read。
