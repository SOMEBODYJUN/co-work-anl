# Hall-B取消R/I查询库存后，全部联合初始化费用可支付

2026-10-23，mixed_menus。全输入解析组件；credible已分别独立核对Hall-B降source、局部δ扩充、真实初始吸收分母和联合SOURCE-NET，确认成立。不是half证明。复用joint_activation_owner_credit.md的固定对象。

## 同一actual图

对owner实际未覆盖客户设β_x=1（R）或κ_x=1/(c_x^0+1)（I^-）。其余客户不设终点。β_i为本owner总库存，g_i=u_i(G)。

复用credible actual Hall-B：owner向每个actual coverer设容量1/(c_x^0+1)的边，向终点设β_x。原图可运送b_i^H>=g_i；逐source削减原路径即有源g_i的可行流。故存在0<=λ_x<=β_x、Σλ=G。只花实际G的一份原利润，不领取整份outside调和利润。

任意局部δ_x<=β_x、δ_i<=g_i可同时扩充为λ：预送本地δ后每个角色割的source及本地终点容量都减δ(J)，原割条件保留。因此可同时取δ_i=min(g_i,β_i)。

## 取消与净收入

R源保留比例1−λ_x；I^-只将query分支保留1−λ_x/κ_x，actual信用分支不动。积分/期望取消量为λ_x，联合query目标为R+κ^-−G。

这是期望取消G，不要求每world恰取消G。actual I信用仍为同一e_i，不重复叠加被取消的I-query。

角色边流f满足λ_i+out_f−in_f=g_i。唯一净收入为η_i=u_i−g_i+λ_i=u_i(I)+λ_i，Ση_i=W。error角色容量不是另一份福利。

## 联合初始化同时可付

将query吸收分成initial owner当次吸收A_i^src与更早角色传播而来部分；最终whole-IC系数仍是二者相加后唯一w=A/D。所有initial query为合法T_i。

MARG-CAP给A_i^src<=D_i(T_i)，取消只降低它。置K_i^src=u_i A_i^src/D_i(T_i)，零分母取零。

* 若g_i<=β_i，则λ_i>=δ_i=g_i，所以η_i>=u_i>=K_i^src。
* 若g_i>β_i，则δ_i=β_i；所有owner库存满额取消，R源与I-query源均为零，所以K_i^src=0<=η_i。

于是对所有角色同时有K_i^src<=η_i，ΣK_i^src<=W。根无incoming，因此联合根费用也已付。该证明本身不要求IC，使用SPE付款时所有来源只乘一份完整原IC。

## 接一般证明的位置

旧SOURCE-NET只取消R；加入I-query后若仍只取消R，无R库存的owner初始化不自动受旧论证控制。Hall-B的missing-owner价格恰匹配I-query κ，使同一局部取消支付全部R/I源，不换owner、不另收G。

未付仍是后续传播K_i^in。足够的总上界为Σ(K_i^src+K_i^in)<=W+κ^-；减联合目标的κ^-才得half。这个上界尚未证明。

不能把每state系数<=1、source初始化已付、或各客户分别存在路由，宣布同role多query碰撞已付。Hall-A和本Hall-B亦不能把相同actual容量各花一遍。

λ须在激活/U之前固定。对I-query使用λ/κ条件删除，靠query事件概率κ得到期望取消λ；若λ依U选择，这个等式不再自动成立。relay的R-only逐world Hall-A取消是另一项合法选择，因为R token每world始终存在，不能在本证明中偷换。
