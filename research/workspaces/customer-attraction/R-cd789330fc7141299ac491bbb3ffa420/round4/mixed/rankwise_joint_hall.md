# 同一随机排序中的逐world联合Hall取消

2026-10-23，mixed_menus。任意m、一般catalog的解析组件；relay与credible已分别独立重构全部cut并确认。给R/I-query同world取消，不证明query费用。Q-CAG-HALF仍OPEN。

固定最优O、owner Q_i⊆T_i、actual叶Z和同一无并列全局priority U。对每个owner实际未覆盖的O客户x：若最高U actual coverer j高于owner，建owner→j容量1；否则建owner→客户终点容量1。后者恰是joint核query token存在事件（R恒有，I^-需owner最高）。角色边严格升U，无循环。

每个actual G客户整1 source给其actual coverer中U最高者。source g_i(U)逐world总和G、期望等于原u_i(G)；它不是逐world固定g_i。

任意角色cut J，令M(J)为owner∈J、actual coverers全部不在J的O客户。owner hybrid给G被J覆盖数<=|M(J)|。source g_U(J)<=G被J覆盖数。每个M(J)必owner未覆盖，其所选最高coverer若存在则在J外，否则终点边出割；每客户都贡献1。因此cutcap(J)>=|M(J)|>=g_U(J)。

maxflow-mincut逐world运满G。所有容量/source整数，可选整数流，恰取消G枚实际存在的R/I-query token。可依整个world的query终点价自适应选择可行流，不需λ/κ均值换算。

对actual负载c的owner未覆盖客户，每个coverer j成为出口的事件是j在owner加所有actual coverer中最高，概率1/(c+1)=actual e_j；sink概率同为κ=1/(c+1)。R sink恒1。期望图恰为actual Hall-B error容量与missing-owner库存，source期望为actual G原利润。

同一排序使终点逐world存在，区别于固定λ条件删除。本证明没有把平均容量当作点态容量。

## 净库存与未付费用

将每个actual覆盖客户整1收入也给其最高U actual coverer，记随机收入u_i^hat(U)，期望为原u_i，总和W。G source正是其中G部分。流取消量λ_i(U)和角色流f满足λ_i+out−in=g_i(U)，且incoming不超过实际I随机winner收入（每条入边的目标正是该客户winner）。所以随机净库存

    η_i^hat(U)=u_i^hat(I;U)+λ_i(U)>=0，Ση_i^hat=W。

平均后Eη_i^hat=u_i(I)+Eλ_i，仍是一份总W净预算，E角色流不超actual e容量。

查询whole-IC价格却仍为原常数u_i/D_i(a)，不能把随机winner收入u_i^hat替换进原IC。它与query/取消事件相关，SOURCE-NET也不能凭均值直接恢复。

逐world取消G后，R/query-I剩余总质量的期望为R+κ^-−G。每固定state的吸收不超过未取消Beta/势边际上界，因为0<=保留<=1；但不能将上界乘平均残比例。

因此本组件真正新增的是R、I-query单位库存、G source及error边在一份随机排序中的兼容取消。要闭half，还需同一whole-IC费用总和<=W+κ^-；该容量尚未证明。旧固定Hall-B λ机制的SOURCE-NET是另一份可选证书，不和此world-adaptive图分别花G。

## credible的R-only投影及独立重构

credible提出下列投影，mixed已独立核对。固定每world的token路线和终点价格v=u_i/D_i(a)>=1。另设A图：每I客户都从owner向其最高U actual coverer连unit边（自环可删），R客户仍只有unit sink。source沿用G赢家coupon。相同HYB cut给A可运满G；它的期望边容量为actual单位份额1/c。

B图的角色边为A子图。取一份B流，只保留终点为R的路径，即A上的partial flow。用普通residual增广至满G；增广路不经过终点t后再离开，因此不会使用R-sink边的反向t边，全部已有R取消量λ_R保持不减。最终R取消γ_R>=λ_R，额外取消量恰为B取消的I-query量λ_I。A角色边可降priority，不声称仍有B的DAG性质。

记N_I(U)为此world实际出现I-query token数。额外每枚R取消至少节省1，未取消I-query价格也至少1，故

    K_Ronly(U)<=K_joint(U)−N_I(U)，
    E K_Ronly<=E K_joint−κ^-。

所以若联合方案总费<=W+κ^-，便有R-only随机coupon方案总费<=W。这个投影没有证明该费用界，也未固定任何匹配。期望A流位于原actual Hall-A可行集，但单个world容量为unit赢家coupon，不要求每world流都属于原均值容量Γ_A。
