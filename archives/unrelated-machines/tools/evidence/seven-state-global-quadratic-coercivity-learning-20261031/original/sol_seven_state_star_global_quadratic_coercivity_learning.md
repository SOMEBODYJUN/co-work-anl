# 七态原作业大星的全局二次局部化与行配置 trade

2026-10-18，scratch 递归噪声构件。作者证明；root 已消息级重构核心插值，但没有把本文记为独立全文审查。这个小原矩实际 OPT=1；它不是 near-two gap，更不是完整 growing-depth H_U law。

## 1. 一个完整普通原矩

d 为正偶数，s 为正偶数，2<=s<=d/2，eta=s/d，h=s/2。机器是 u、v、z_1,...,z_d，共 d+2 台。原 job R 在唯一 home u 上时间一、在 v 上时间一；原 jobs j=1,...,d 在 v 上时间 1/d、在各自不同的 z_j 上时间一。其余时间无穷。共 d+1 枚原 jobs、2(d+1) 个有限条目。

记 C 为 R 在 v 的指示，Y_j 为 job j 留在 v 的指示，H=sum Y_j。每个状态都把 R 放在其两个原端点之一、每枚 j 放在其两个原端点之一，因而是完整原 assignment。负载为

    load_u=1-C,
    load_v=C+H/d,
    load_(z_j)=1-Y_j.

所有非 v 行始终负载至多一。所有 jobs 回 home 即给完整峰一调度，故实际 OPT=1。

## 2. 同一个真实七态 law

令 T=1+eta，

    p=eta^3/1000, b0=b1=c0=c1=1/20,
    u0=4p(1-eta), e=1-1/5-p-u0.

以下 law 中，每个给定 H 的 home 集均为均匀 H-subset：

| C | H | 概率 | g_v=T-load_v |
|---|---|---|---|
| 1 | d | p | eta-1 |
| 1 | 0 | b0 | eta |
| 1 | h | b1 | eta/2 |
| 0 | 0 | c0 | 1+eta |
| 0 | h | c1 | 1+eta/2 |
| 0 | d/2 | u0 | eta+1/2 |
| 0 | d | e | eta |

e>0.79，所有概率合法。这是一个真正的全原 assignment 分布；其全部共同矩阵 M_k 自动 PSD。坏状态 v 负载二的概率恰为 p>0。

## 3. 完整 row CONFIG(T) 的 first/pair 一致性

只需另给 v 的合法配置 law 来匹配其 original first/pair，并不把它与真实七态 law 的支持混同。将上述分布中 bad(1,d) 部分作如下改变：

- active H=s 质量 p/eta；active H=0 质量 b0+p-p/eta；active H=h 质量仍为 b1。
- inactive H=0 质量 c0+u0/2；inactive H=h 质量 c1；inactive H=d 质量 e+u0/2；inactive H=d/2 质量变为零。

所有质量非负。active 行 H<=s，inactive 行 H<=d，故全部配置合法。两种 law 的 C、H、CH、H(H-1) 期望相同：active bad 的二阶损失为 p d(d-s)，inactive half-home 转为 0/d 的二阶增量为 u0 d²/4，二者相等。均匀 home 子集使这些 aggregate moments 精确决定每个原 Y_j、Y_jY_k、CY_j 的 first/pair。u 和 z_j 各只有一枚可见原 job，其 row 配置 law 直接取真实边际即可。

因此一个共同真实 law 与每行完整 CONFIG(T) first/pair 完全一致；没有把逐行配置 law 拼成另一个真实全局 law。

## 4. 所有全局二次多项式的局部化

任何原端点变量都仿射于 C,Y_1,...,Y_d，因而任意 global degree-at-most-two polynomial q 在本原矩上仍是这些变量的次数至多二多项式。

对 home job 标签的置换作平均，令 bar q 是对称化。各正状态中 g_v 为正常数，Jensen 给 E(q²|C,H)>=bar q(C,H)²。唯一负状态的全部 Y_j=1，对称化不改变其 q 值。故只需证明对称化多项式。Boolean 化简后可写

    bar q(C,H)=P(H)+C(a+bH), deg P<=2.

令 lambda=d/h=2/eta。记 q_a(x)=bar q(1,x)、q_i(x)=bar q(0,x)，则精确恒等式为

    q_a(d)=lambda q_a(h)+(1-lambda)q_a(0)
             +q_i(d)-lambda q_i(h)-(1-lambda)q_i(0).   (1)

五个系数的平方和为 4lambda²-4lambda+3<=4lambda²=16/eta²。Cauchy 因而将负状态的 q² 支配于这五个正状态的 q² 之和，系数至多 16/eta²。每个对应正状态的质量乘 slack 至少 eta/40，而

    p(1-eta)16/eta² <=16eta/1000 < eta/40.

其余 inactive half-home 状态的贡献也非负。故对所有 global deg(q)<=2，严格证明

    E[(T-load_v)q²]>=0.

所有其他行逐点 g>=0，因此同一个七态 law 满足全部机器的 global quadratic load localizers。它给一个真实共同 M3、全原 Boolean/one-hot、完整 row CFG first/pair 的必要系统点，虽然该真实 law 的支持有峰二坏样本。原矩自身有完整峰一调度，故完全没有近二实际 gap。

## 5. 可接线的原 assignment 耦合合同

更一般地，固定一个完整外部背景、一个原 incoming job R 的“在 v / 在上游 home”开关，以及 v 的 d 枚原 home jobs 各自不同的可用 unit 导出位置。改变 C 与 home 子集时，全部原 assignment 指示向量仿射于 C,Y；其他 jobs 必须真的固定，unit 导出位置也必须是真的不同且未被背景占用。此时第 4 节对任意 global quadratic q 仍逐背景成立，随后可对背景分布积分。

这个合同不能免费应用到深层源：把 d 枚 jobs 导到内部孩子，会给这些孩子增加 unit arrivals；incoming R 回其原 home 也会收费父行。它们在上面小矩是终端/无额外负载机器，所以逐点合法；在 growing-depth 背景下不保证。因此本文只给单行的 dimension-free coercivity 与 pair trade，不给所有行共同预算或任何外部强解 oracle。

## 6. 固定更高次数的插值方向

同一思想可对固定次数 D 使用 D 个不同的 active home-count 节点 H_j<=eta d/2，以及相同的 inactive 节点。对称化后的 active-minus-inactive 是次数至多 D-1 的 H 多项式，故在 H=d 的值可由 Lagrange 插值表达，系数 O_D(eta^(-D+1))。负质量若取 c_D eta^(2D-1)，可由这些正态的 slack eta/2 支配，仍无 d 因子。需要 s 足够大以容纳分离节点；此处只将其作为明确可推的固定 D 扩展方向，未把未写出的所有常数和全局递归记为已完成。

## 7. 计算性与精确核对

七态和合法 row law 都有短的精确参数描述。均匀 H-subset 的 t 个不同原 home 指示乘积矩为 (H)_t/(d)_t，故任意固定次数共同矩可用有理算术多项式时间计算，无指数支持枚举或未知优化 oracle。半子集描述并不是声称列出了每个配置；其完整分布与所有所需 moments 均已明确。

有限代码另外检查各参数的质量、row first/pair trade、对称五维 signedslack 矩阵，并对小 d 检查完整 monomial 矩阵。它不检查 growing-depth 的跨行收费；该部分仍是主线核心义务。literal_budget_attack 消息级逐式核过先前五态 pair trade 和 affine rectangle，root 消息级核过本七态二次插值；两者不冒称读过本文全文或其代码。
