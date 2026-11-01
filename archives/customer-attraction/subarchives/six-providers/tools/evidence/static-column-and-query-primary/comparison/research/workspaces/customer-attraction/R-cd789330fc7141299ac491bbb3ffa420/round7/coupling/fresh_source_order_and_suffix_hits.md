# Fresh 源的角色因果序与后缀命中细化

2026-10-24，coupling7。任意人数、一般有限共同目录、每份完整有序历史纯 SPE。**Q-CAG-HALF 仍 OPEN。** 本页是 round5 [全客户消元 §7](../../round5/credible/all_fresh_submarkov_elimination.md)因果区间与 round6 [全图角色命中](../../round6/relay/global_role_coupon_hitting.md)的一个合并推论；不主张新颖性，不声称实际容量已付。下列解析证明已获 [root 独立重构及对稿](../parent/source_order_reconstruction.md)和 [credible 独立盲重构及对稿](../credible/source_time_coupling_review.md)通过；不是外审。

## 1. 允许的来源、图与记号

固定原完整 SPE、实际叶 Z=(S_1,...,S_m)、实际覆盖 C。只使用同一份全客户 SAFE 净券图，或其合法删正边/CLIP 版本；各版本须各自重算流，不相加。当前 natural context t=(g,i) 的规定动作是 a=sigma(g)，规定完成叶为 B=finish(g)，actual-reset query 完成叶为 A=finish(Z_<i,a)。未来正边 j>i 进入 A_<j 的真实规定 context；过去正边 j<i 只能终止于真实 actual 角色券 (j,x)，且其正性要求

    x in S_j(Z),   x not in g_j.                    (PAST-DOMAIN)

SAFE 只从同一当前 actual 整行退券。CLIP/同客户取消等合法净化只删除原正边，并把删除的相应质量留给当前实际角色；它们不增加新的支持边。本页无需比较不同图的 beta 或净负载。

每个 fresh 源 alpha 在角色 k=k(alpha) 的 actual-prefix 下强制一个合法主题 T_alpha。令

    Y_alpha=finish(Z_<k,T_alpha),
    rho_(alpha,x)>=0 supported on x in T_alpha\C,
    M_alpha=sum_x rho_(alpha,x).

来源可有任意有限非负质量；唯一 owner、rho<=1、最优性都不是本页因果命题的条件。通常 OPT-owner 或固定 trim 源是特例。每个 x 的 rho/c_Y(x) 留给当前 actual 角色 k，每个 j>k 的真实 Y_j coverer 得 rho/c_Y(x) 并进入 natural context Y_<j。因为 x 不在 C，没有任何 j<k 的初始 past 支付。首行是包含 k 的均匀角色子集行的非负混合，总质量 M_alpha 守恒。

证明中始终保留 alpha 标签。若实现把相同 natural context 的输入合并，线性流仍可事后按这些标签分拆；这不把不同历史或不同 source 的 IC 合为一条新 IC。记 M_k=sum_(alpha:k(alpha)=k) M_alpha，A_(alpha,j) 为该源最终到 actual 角色 j 的非负净金额，A_j=sum_alpha A_(alpha,j)。

## 2. 所有终端实际角色都不早于源角色

**SOURCE-ORDER（合并推论）。** 对上述每个 fresh 源，

    A_(alpha,j)=0 for j<k(alpha).                  (ORDER)

更强地，可为每个由 alpha 到达的 natural context t=(g,i) 保留一个重置标记 q，满足

    k(alpha)<=q<i,  and g_j=S_j for every j<q.      (PREFIX)

一个实际 context 可直接作为无边终端；也允许形式记 q=i，此时 g=Z_<i，没有不同于实际的 prefix。

证明：首个 future recipient i>k 位于 Y_alpha，故其 history 在 k 以前等于原 actual，取 q=k。若在 t 走一条 future 正边 l>i，新规定 history 是 A_<l，而 A 由 actual_<i 的 query 开始，所以新标记可取 q'=i>=q。若 A=Z，则新 history 直接实际，亦没有正传播边。

若在 t 走一条 past 正边到 j，则由 (PAST-DOMAIN)，g_j 与 S_j 在客户 x 上不同。由 (PREFIX)，j<q 不可能，故 j>=q>=k。当前吸收发生在 i>=k。初始当前吸收在 k，而初始 future 边从不进入 k 以前。因此所有终端角色均>=k。合法删边或把删除质量留给当前角色显然保留此支持不变量。证毕。

本结论没有声称单条轨迹上的角色始终增加：natural current 角色可以先增加，再通过 past coupon 降到区间 [q,i)。它只说该区间的左端点不会早于原 fresh 源，而且重置标记沿 future 步骤增加。这正是 round5 §7 区间的源标签版本。

**零收益边界。** 正 source 份额或正 future q 到达的规定动作含一个客户，故其 v>0；其 actual-reset 动作同样非空，D>0，原 actual IC 又给 u_i>=D>0。因此正实际支付无需除以零。v=0 的空动作 context 没有正 q，也不由上述合法初始化/正边接收正量，可删去。actual context 的 B=A=Z，所有正边为零，正输入完全吸收于当前实际角色。零质量来源略去即可。

## 3. 逐源后缀角色命中界

任取 actual 角色集合 K，定义

    K_k=K intersect {k,...,m},  h_k(K)=|K_k|.

由 ORDER，该源落入 K 与落入 K_k 的终端质量相同。若 k不在K，round6 GLOBAL-HIT 对目标集 K_k 给

    sum_(j in K) A_(alpha,j)
       <= h_k(K)/(h_k(K)+1) M_alpha.              (SUFFIX-HIT)

若 k在K，只使用守恒上界 M_alpha。这里 GLOBAL-HIT 可包括本页允许的首行：首行 current 为 k，所有 fresh coverer 都在未来；其 uniform-subset/PRICE 合同与后续 SAFE/CLIP 图相同。也可以直接照该页角色逆序归纳，把目标集从 K 换成 K_k。没有把自然 current 角色在 K 时假定为立刻停止。

所有来源同时相加得到

    A(K) <= sum_(k in K) M_k
            +sum_(k notin K) [h_k(K)/(h_k(K)+1)] M_k. (ORDERED-HIT)

这是旧 INIT-HIT 的细化，因为 h_k(K)<=|K|。它针对同一固定合法图和同一份 source。源取消或路由若事后依赖已抽出的轨迹，须另证条件转移；本页不自动涵盖这种适应选择。

特别对前缀 K={1,...,p}，在 k>p 时 h_k(K)=0，故

    sum_(j<=p) A_j <= sum_(k<=p) M_k.             (PREFIX-CUT)

总量 sum A=sum M 再给等价后缀式 sum_(j>=p)A_j>=sum_(k>=p)M_k。对于完整 O 初始化，上述支持不变量一般不成立：x在C的源可能在 owner k 以前已有 actual coverer，初始化即有合法 past 支付。因此不能把 ORDER/PREFIX-CUT 无条件用于 full-O cap2 接口。

## 4. 后缀角色价格包络

给任意非负 actual 角色价格 lambda_j。固定源角色 k，把满足 j>k 且 lambda_j>lambda_k 的角色价格降序排列

    lambda_(1)>=...>=lambda_(l)>lambda_k.

只对可达后缀使用 round6 价格层积分，得到

    sum_j lambda_j A_(alpha,j)
      <= M_alpha H_k^suffix(lambda),
    H_k^suffix(lambda)=lambda_k/(l+1)
                       +sum_(s=1..l)lambda_(s)/[s(s+1)]. (SUFFIX-PRICE)

证明：ORDER 删除所有 j<k 的质量；以 lambda_k 为基线，丢去低于基线的负差。每个高价层中的前 s 个角色不含 k，SUFFIX-HIT 使其质量比例<=s/(s+1)；按价格差望远镜即得显示式。l=0 时 H=lambda_k。此式只是 round6 [角色价格包络](../../round6/parent/role_price_envelope.md)限制到源可达后缀的推论。

若 lambda 随角色非增，则没有高于 lambda_k 的后来角色，故

    sum_j lambda_j A_j <= sum_k lambda_k M_k.     (DECREASING-PRICE)

这亦由 PREFIX-CUT 的分部求和直接推出。

## 5. 精确用途与仍缺的付款

SOURCE-ORDER、ORDERED-HIT、PREFIX-CUT 与 SUFFIX-PRICE 都对一般输入成立，但仅约束比较来源 M 到实际金额 A 的可达运输。它们不把 M_k 变成 u_k，不给 A_j<=u_j 或 A_j<=2u_j，不给客户券 cap，也不把 sum A=sum M 变成福利不等式。常数价格仍只给 M<=M。

可能的接法是：在同一份合法 fresh 残源/owner选择中，把 source 到 actual 的运输限制为上三角，再与 actual-wallet 容量或价格对偶共同处理。此前尚未证明这种联合选择可行；本页没有替代 Q-CAG-HALF 的实际容量义务，也未把一般主目标的已证范围扩大。
