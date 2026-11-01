# 自洽平均负载：独立审查与一次带 SC 的定向检验

2026-10-24，capacity。独立阅读 [root 原稿](../root/self_consistent_pool.md)，按原模型重新展开 q、固定点、Jensen 及静态常数。**表示与条件推导通过；付款仍 OPEN。** 非外审或新颖性认证。后续 direct/construction 的纯点反例已单独注明，不把它归给本分支。

## 1. q、mu 与存在性

令 K_(T,A)=[m(m-1)]^(-1) sum_i #{j!=i:Z_i(A)_j=T}。每个 Z_i(A) 是恰 m 槽，删当前槽后恰 m-1 槽，所以 sum_T K_(T,A)=1，K>=0。因此 q(p)=Kp 确实是主题分布，而且逐客户恰有

    mu_x(p)=(1/m) sum_i sum_A p_A c_x(V_i(A)).

不是多除或少除一个 m-1。固定过去与真实后继均计入；只删当前槽。

g_T(p)=sum_(x in T)1/(1+mu_x(p)) 连续，分母>=1。原稿 logit 映射连续且映单纯形入自身，Brouwer 给 p^eps。不动点取 eps->0 的子列极限；若极限上 g_T 比另一 g_A 严格小，指数比给 p_T^eps<=exp(-a/eps)->0。因此极限支持只含最佳主题。SC 集合可写为所有

    p_T[max_A g_A(p)-g_T(p)]=0,

故闭而紧。该存在论证不需 SPE，不能据此给 actual 付款。

## 2. 确定查询的 Jensen 与更强常数

对 p=e_A，mu 是同一个确定 A 的 m 份真实竞争负载平均。倒数凸性方向为

    g_A(e_A)<= (1/m) sum_i d_i(A)<=W/m.

若 e_A 还是 SC，则 max_Tg_T(e_A)=g_A(e_A)，所以它的一个明确自由分数 m-1 槽背景已经给 delta_m<=W/m。

静态常数也可直接重构，无需把 delta_m 与 iid 或整数安全值混同。对任意主题分布 q，置 L_x=(m-1)q_x、M=max_T sum_(x in T)1/(1+L_x)。比较 m 个最优主题的重数 d_x，有

    1_(d_x>0)<=(d_x+L_x)/(1+L_x).

求和后，OPT<=mM+sum_x L_x/(1+L_x)<=mM+(m-1)M=(2m-1)M。取自由 q 的最小值即 OPT<=(2m-1)delta_m。因此“存在纯 SC”确会推出

    OPT_m<=(2-1/m)W,

而不只是 half。m=5 条件常数9/5正确。但 direct 的完整16单位客户反例现已否定普遍纯 SC 存在；该失败不涉及混合 SC 存在与混合付款。

## 3. 混合点的确切未付项

取 I 在实际角色上均匀、A~p，并令 alpha_x=1_(x in A)、L_x=c_x(V_I(A))、mu_x=E L_x。原真实 IC 只支付

    D(p)=E sum_x alpha_x/(1+L_x)<=W/m.

SC 使用的则是 G(p)=sum_x Ealpha_x/(1+mu_x)。它没有把 A 与其响应 L 解耦。SC 规定支持主题的 g 值相等，并给所有目录主题的最佳回复比较；它不是 p=q(p)，也不是自由 q 极小化的 KKT。

旧635客户坏 p=(e2+e5)/2 上 g2!=g5，故该旧点不满足 SC。这使加入支持等式成为真实的新检验条件，不能继续用 all-p 失败直接否定 SC 付款。

## 4. 一次固定 p 的 SC 检验及精确 whole-IC 支付

仅使用既有三人六主题完整 group policy，不随机生成策略、不换人数。固定 p=(e2+e5)/2。其 pooled q 固定为

    q=(5/12,1/6,0,1/3,1/12,0).

对全部63个非空兴趣类型的非负重数，保留全部258条含自身的完整有序历史 IC，加入 g2=g5 及 g2>=gA，最大化 3G-W。数值最优为0；这本身不是一般证据。

随后重构了一个**精确**证书。令 Gamma_hA 是该固定完整策略的真实整行 IC，n_t 是客户类型重数。已核对

    W-3g2 = sum_(20 rows) lambda_hA Gamma_hA
              -(181356/300677)(g2-g5)+sum_t r_t n_t,
    lambda_hA>=0, r_t>=0.                           (EXACT-CONE)

因此在**这一固定 policy cone、这一固定 p** 内，只需支持等式 g2=g5 就能支付 3G<=W；其它最佳回复不等式甚至未用于该证书。这确实组合了真正 off-history IC，而非只付每个确定查询的 Jensen 行。20个精确乘子及63列余项在 `mixed_sc_fixed_query_probe.json`；`audit_mixed_sc_dual.py` 不调用优化器，重新构造全部列并以 Fraction 验证 identity、非负及系数。

该系数不宣称能在其它 policy、其它 p 或其它 m 原样使用；也未从这个单 cone 证书抽出一般机制。不继续扩同锥网格或重数扫描。

## 5. 16客户纯点反例的准确位置

direct 的 [纯点及全混合支持分析](../direct/self_consistent_pure_shortcut.md) 证明该例唯一混合 SC 支持为{2,5}，其

    p=t e2+(1-t)e5,
    t=(27-sqrt(537))/6 in (5/8,2/3).

独立计算 g2-g5=3(3t^2-27t+16)/[8(8-t)(9-t)]，相同根正确；G约4.37340604<W/3=14/3。construction 还独立发现更强的有限事实：该例所有纯列/查询值均<=107/24<14/3；各 g_T 对 p 凸，故所有 p 都付款。因而它不能提供混合 SC 付款反例。本分支不重复其全策略或纯点证书。

## 6. 结论与 m=5

原稿 q 归一、SC 存在、纯查询 Jensen、自由分数常数及条件9/5均通过。本次真正测试 SC 支持等式的一次 LP 没有分离，且得到上述固定 cone 精确付款组合；它不是一般结论。

对一般 m=5，存在性照旧成立；若某个混合 SC 满足5G<=W，则静态界给 OPT_5<=9W/5。当前没有证明这种 paid SC 总存在，故本轮没有新增无条件五人或全人数福利常数。
