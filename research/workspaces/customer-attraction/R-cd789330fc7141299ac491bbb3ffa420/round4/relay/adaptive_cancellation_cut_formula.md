# 适应取消总费用的嵌套全割公式

2026-10-23。一般任意 m/catalog。relay先独立重推后与shared稿对照：本页静态RANK/嵌套贪心/费用/DEFICIT与 `../shared/net_dynamic_rank.md` §2–4 完全同对象；该主稿已有 `../credible/review_net_dynamic_rank.md` 独审，**不另认新公式或新付款**。shared另已读本页并核对逐批增广证明无异议。本页仅保留本人推导及将同一公式逐world用于新适应取消的接口。

**本页只是精确优化归约，未给 half 所需的新总费用上界。** 它让同一 world 的取消决定可直接用实际 Hall-A 全割表示，供完整真实 IC 接合；不以静态对偶本身算已付预算。

采用 `adaptive_cancellation_priority_world.md` 的固定实际叶、最优 owner、共用排列世界和可选终点价 v_x(U)>=1。为只求较弱的总体费用界，暂时放弃 SOURCE-NET 所需局部取消下界，令 Gamma_0 为原实际 Hall-A 的**全部**可行满 source 流和取消。它非空且 sum gamma=G，故一切 LEGAL-COST 与逐world质量仍成立；不再据此声明 SOURCE-NET。

## 1. 限定取消终点的最大流

给任意 K subset R，定义 r(K) 为实际 Hall-A 中只开放 K 终点时的最大流值。全部 role 边仍只用原实际 I 的等分容量，source i 的容量是 g_i=u_i(Z;G)。客户 x in I 从 owner o(x) 到每个实际 coverer j 的边容量为1/c_x(Z)；每个 x in K 从其 owner 到终点的容量1。与原图同样允许自环，但它不影响割。显然

    0<=r(K)<=min{|K|,|G|}，    r(R)=|G|。

取角色集合 J 为 source侧，最小割公式给

    r(K)=min_J [g(J^c)+cap_I(J,J^c)+|K intersect Q_J|]。

令 L=J^c，故取消不足量有显式公式

    d(K):=|K|-r(K)
       =max_L [|K intersect Q_L|-g(L)-cap_I(L^c,L)]，  (CUT)

其中

    cap_I(L^c,L)=sum_(x in I:o(x) notin L)
                     #{j in L:x in Z_j}/c_x(Z)。

L为空给0，故 d>=0。K=R 时 d(R)=|R|-|G|=OPT-W。这里所有容量来自同一实际叶，不把任意 query 叶称作 actual G。

## 2. 所有嵌套高价集合可同时最大化取消

固定任意非负有限客户价格 v_x。令 K_t={x in R:v_x>t}，t>=0。这是一条有限嵌套集合链。存在同一 Gamma_0 中的满流 gamma，使对该链全部集合同时成立

    gamma(K_t)=r(K_t)。

自足证明：从最高价客户集合开始，先在只开放它们的终点边的网络中取最大流。然后依价格下降逐批开放新终点边，并用标准残余网络增广到新的最大值。增广路径不把共同 sink 作为内部节点，所以不会走旧终点边的逆向边，不减少任何已经送入旧终点的流量。原先开放集合的最大总量 r(K) 因而始终保持。最后开放全部 R，流值 r(R)=G，得到原实际 Hall-A 满 source 流。必要时只移除无关流循环，不改变终点量。

这一步也证明同一取消方案可最优处理所有价格层，不能在每层任意挑一份互不相容的 gamma 后直接积分。

## 3. 最小残费的精确 layer-cake

对任意可行 gamma，客户容量不超过1，所以

    sum_x(1-gamma_x)v_x
       =integral_0^infty [|K_t|-gamma(K_t)]dt
       >=integral_0^infty d(K_t)dt。

上一节的同一可行 gamma 同时取得每层等号。因此

    min_((gamma,f) in Gamma_0) sum_x(1-gamma_x)v_x
        =integral_0^infty d(K_t)dt。                (EXACT-CUT)

这也可称网络 sink 向量的 polymatroid 贪心公式；证明不依赖外部定理。若 v>=1，零至一的积分恒为 d(R)=OPT-W，故

    最省残费=OPT-W+integral_1^infty d(K_t)dt。

一般 full-SPE 目标若想经本接口完成，还须证明右侧期望<=W；本页没有这个不等式，尤其不因积分项非负就默认2W-OPT非负。

## 4. 接回同一共用世界

取 fixed-earliest终点价或前页的最小可达rank终止价 v_x(U)。因为世界只有有限排列，所有价格与集合链有限，逐world选择上述贪心流可测。于是较弱的适应总费用恰为

    V_0=E_U integral_0^infty max_L
       [|K_t(U) intersect Q_L|-g(L)-cap_I(L^c,L)]dt。

V_0不超过强制局部delta的 V_best，并仍由一次整条 IC 常数系数实现。如果能共同选择最优 matching/owner 和合法路径证明 V_0<=W，就能闭合 half；**当前没有该全称证明**。

K_t(U) 的内容是：x 在该排列世界所有可达强制终止查询的最低真实费用仍高于 t。它不是任意指定的客户价格，也不允许删去原历史来调用较小 SPE。真正剩余工作是将这些价格事件/role cut与完整真实孩子 IC 联立，而不是继续重排静态 maxflow。
