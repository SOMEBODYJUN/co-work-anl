# 同一实际角色的 source-preserving 完整 query 压缩

2026-10-24，credible8。适用任意有限共同目录、任意人数、每份完整历史依赖纯 SPE。**一般 Q-CAG-HALF 仍 OPEN。** 本文给一个可明确接到 role-cap 的一般充分接口；未证明其共同 coefficient budget。无外审、新颖性或一般 half 结论。

## 1. 原始完整 query 钱包

固定实际叶 Z=(S_1,...,S_m)，实际利润 u_j。对每个实际角色 j 和每个目录主题 a，定义同一原策略的完整偏离完成叶

    A^(j,a)=finish_sigma(Z_<j,a),
    z_(j,a,x)=1_(x in a)/c_A^(j,a)(x),
    D_(j,a)=sum_x z_(j,a,x).

无覆盖时 z=0；只在 x∈a 时使用分母，故其正。原 actual-prefix 的 whole IC 恰为

    D_(j,a)<=u_j.                                      (QIC)

后文每次只把同一个完整 D_(j,a) 乘一个非负标量；没有按客户重权调用 IC。

若 u_j=0，则所有 D_(j,a)=0。共同目录中若有一个非空主题，偏离该主题的利润严格正，矛盾。因此这个情况仅可能所有主题均空，所有 source 金额均零。以下有正 source 时可取 u_j>0。

## 2. 同角色所有 natural contexts 的精确 source 向量

natural context t=(g,j) 的原规定动作记为 a_t，规定叶为 B_t；其 actual-prefix reset 是 A_t=A^(j,a_t)。对 x∈a_t，置

    b_t(x)=c_Bt(x),
    a_t^load(x)=c_At(x),
    r_t(x)=|cover_Bt(x) intersect cover_At(x)|.

这里 r_t(x)>=1，当前角色 j 属于交集。令 h_tx>=0 为到该 context 的 source 客户 x 金额，且只在 x∈a_t 有正值。考虑逐客户的原正边比例核：每个新 reset-coverer l∈cover_At(x)\cover_Bt(x) 收到

    h_tx/a_t^load(x),

而当前 actual 角色 j 收到

    g_tx=h_tx r_t(x)/a_t^load(x).                       (CURRENT)

因为新 coverer 数为 a_t^load−r_t，这些金额逐客户精确加回 h_tx。future recipient 是真实 natural context；past recipient 必须是相应 actual 客户券，不对其调用假 IC。

本文仅研究这个 source-preserving 核的最终当前付款。若选用不同剪枝、不同分母或 full-profit 重采，必须重新推导对应 g，不能混用下列公式。

把同一 actual 角色 j 的所有 natural contexts 合并，得到

    g_j(x)=sum_(t:role(t)=j) g_tx.                       (GROUP)

可以再把 source-preserving 的实际初始正价 H_j(x) 和 past 终端券 P_j(x) 加入 g_j；它们都是同一 source 客户上的实际正金额。原初始化若另有只在整行上支付的 current 金额 d_j，则把它单独保留，不能假设它按客户受 z_(j,a,x) 控制。

关键：共同 source 库存能约束 g_j(x)，但 (QIC) 的钱包是完整 D_(j,a)，不能对各个 x 分别花一份 u_j。

## 3. 完整 query 共同覆盖引理

对固定 j，设存在非负目录系数 lambda_(j,a)，使

    g_j(x)<=sum_a lambda_(j,a) z_(j,a,x)  对所有 x。     (COVER)

则同一角色全部这些 source 付款有共同实际金额界

    sum_x g_j(x)
      <=sum_a lambda_(j,a) D_(j,a)
      <=u_j sum_a lambda_(j,a).                         (PAY)

证明只需对 (COVER) 求和，再对每个 a 使用一次原始完整 (QIC)。其中 source 标签用于建立向量支配；最后一步没有把任何 IC 的客户权重改成 lambda_x。

若 g_j 已含 H_j 及传播终端金额，另有整行初始 current d_j，则

    sum_a lambda_(j,a)<=2-d_j/u_j                      (BUDGET?)

足以给该角色所有来源的共同 2u_j 金额。对全部角色求和才可支付 OPT。**没有证明一般 BUDGET；PAY 本身不是 half 证明。** 这个接口也可能比仅要求金额 role-cap 更强，不能反向等同为原目标。

## 4. 同 prescribed 动作合并，比逐 context 最大密度更精确

先只取 natural-current 部分。对每个目录动作 a，定义

    F_(j,a,x)=sum_(t:role(t)=j,a_t=a) h_tx r_t(x),
    M_(j,a)=max_(x in a) F_(j,a,x),

空主题时 M=0。因为这些 context 的 reset 叶都等于同一个 A^(j,a)，有精确等式

    g_j(x)=sum_(a:x in a) F_(j,a,x) z_(j,a,x).          (ACTION-GROUP)

故 lambda_(j,a)=M_(j,a) 满足 COVER，得到

    sum_x g_j(x)<=u_j sum_a M_(j,a).                    (GROUP-PAY)

这把同一 prescribed 动作的所有 context 在调用 whole IC 之前共同入账；不能每个 t 独享一份 u_j。

若 f_tx=b_t(x)h_tx 是逐客户输入密度，单 context 的安全 coefficient 为 theta_t=max_x f_tx。由 r_t<=b_t，

    M_(j,a)<=sum_(t:role(t)=j,a_t=a) theta_t.

因此 ACTION-GROUP 从不劣于先逐 context 取最大密度再相加；它保留了共享 reset 叶以及客户间不同时饱和的信息。不同动作的源支持重叠还可能允许比 M 更小的共同 COVER；不能据此宣称其总和<=1 或<=2。

## 5. 一个精确、有限、可反驳的公共预算候选

令 menu-cover norm 为有限 LP

    K_j(g)=min sum_a lambda_a
      subject to lambda_a>=0,
                 sum_a lambda_a z_(j,a,x)>=g(x) 对所有 x。

source 客户来自目录并集，故总有有限 cover；空 source 给 K=0。标准有限 LP 对偶给

    K_j(g)=max sum_x y_x g(x)
      subject to y_x>=0,
                 sum_x y_x z_(j,a,x)<=1 对所有 a。      (DUAL)

于是候选 K_j(g_j)<=2-d_j/u_j 是精确的一般充分陈述，可以用完整 SPE 的明确 source 过程检验；不能把有限无分离当证明。DUAL 的客户权重只是 cover LP 的数学对偶，**不是**允许按 y_x 重权原始玩家 IC。

库存上界 sum_j g_j(x)<=1 本身不控制这个 norm。在线性松弛层，若 query 向量为互不相交的单位基向量，g 每个坐标都为1，则客户库存均合法而 K 为坐标数。这个描述仅分离“库存+各完整 query IC”的抽象松弛；没有声称相应 g 可由某个完整 SPE 的合法过程生成，也不是 Q-CAG-HALF 反例。仍需真实跨历史约束把可生成的 g 限制到适当的 query convex hull。

## 6. 真实 off-history IC 的四叶位置

仍固定 t=(g,j)，a=a_t。再定义相反方向的真正 off-history query

    V_t=finish_sigma(g,S_j),
    w_t=u_j(V_t),
    ell_t=u_j(B_t)-w_t>=0,
    e_t=u_j-D_(j,a)>=0.

精确 rectangle 为

    u_j(B_t)+u_j-D_(j,a)-w_t=ell_t+e_t>=0.             (RECT)

四叶各自都是原策略的真实完成；RECT 使用 actual-prefix IC 与 g 上改实际动作的 off-history IC。它并不给 u_j(B_t) 的共同上界：右侧真实 ell 是非负优势，不是一个已经付到实际钱包的退款。把 v_t 换成 w_t 会留下正的 source 金额 ell_t，必须另行支付；不能直接删除。

因此本文没有把 GROUP-PAY 冒称为实质用尽了 off-history IC 的新福利关系。当前真正未解的是：如何由全部真实 RECT/IC、共同最优 tuple 以及 source 可生成性，证明 BUDGET 或更弱的跨角色总金额界。

## 7. 状态与接续

解析部分 §1–5 是一般向量支配、whole-IC 支付和有限 LP 合同。residual8 对稿独立检核 CURRENT、ACTION-GROUP、PAY、有限 LP 对偶及零利润边界通过；这是公式与充分接口的对稿检查，不是共同 BUDGET 或 HALF 审查通过。本接口未运行有限搜索、未选固定人数正面任务、未更改旧证书。与 round7 单子枝 prefix 回推相比，这里把实际角色的互斥 prescribed 动作显式放在同一 query-cover 账本中，但尚未证明它们共享所需 coefficient 总量。

继续研究应针对 BUDGET、源可生成性或真实 off-history 四叶之间的共同关系。重复逐 context cap1、source 守恒或每动作 QIC 不补该缺口。
