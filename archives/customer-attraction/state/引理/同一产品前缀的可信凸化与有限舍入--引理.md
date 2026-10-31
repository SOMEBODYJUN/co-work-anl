---
id: "customer-attraction/same-product-prefix-credible-convexification-and-uniform-remainders"
kind: "lemma"
type_tag: "引理"
title: "同一产品前缀的可信凸化与有限舍入"
status: "proved-all-role-all-query-upper-bound"
summary: "真后继菜单只在下一角色总IC上凸化；整块D副本实现DbarL，任意联合query按主题分组保C_i余数，同一产品同一目标所有i有真M上界，非M可加或原单组件混合SPE。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/prefix_repair_next/product_threshold_prefix_attack.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/prefix_repair_next/product_threshold_prefix_attack.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/prefix_repair_next/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/prefix_repair_next/README.md"]
source_ids: ["5378e5437ea1be35c1e1", "13cac8c9e5f2a1bd3ca4"]
review_status: "五原稿全文和早期全m产品转移/旧静态产品表示及全仓正式对象比较；知情解析核，原后续父审范围和先验另保"
truth_status: "静态双证/成本/有限真实反例编译为已证条件工具，未提供严格种子或一般half/强弱安全证明"
---

# 原组件、同一目标和真实菜单

有限组件t=1,…,K，同m≥2、同j∈[1,m−1]、不交单位客户、任意有限非空共同目录。每t给目标z^t=(A₁^t,…,A_m^t)，及长度j前缀后的真完整SPE π^t实现尾；前j无需IC。记W_t,O_t,u_i^t和固定正常h_i^t。

R_t(g)为固定有序历史g后全部真完整SPE可实现终局（含过去动作）。对i≤j、强制A，

\[
L_i^t(A)=\min_{z\in R_t(h_i^t,A)}u_i(z),\quad
\theta_i^t(A)=\max_B\min_{z\in R_t(h_i^t,A,B)}u_{i+1}(z).
\]

下一角色存在，因为i≤m−1。有限菜单E_i^t(A)是全部B与z∈R_t(h_i^t,A,B)的对(d_z,v_z)=(u_i(z),u_(i+1)(z))，只要求B后续真SPE，不要求B本身理性，更不扩大到任意终局。

有限有理LP

\[
\bar L_i^t(A)=\min\{\sum_zp_zd_z:p\ge0,\ \sum p=1,
\ \sum p_zv_z\ge\theta_i^t(A)\}
\]

可行：任取(h_i,A)后真SPE的实际孩子，其下一利润≥θ。单个菜单叶可成为该下一节点选中孩子 iff v_z≥θ：其他B贴最低真后继即可。这给L_i(A)=min_(v_z≥θ)d_z，故barL≤L；有理有限LP取有理最优，选其共同分母D_(t,i,A)≥1。它不是原单组件的混合SPE。i=m−1时v_z全部≤末位最大θ，LP只能混BR，故barL=L，该角色余数损失0。

# D复制品的纯SPE孩子

固定t,i,A，用D个同组件副本，相同正常前缀，当前在各坐标强制A。分配D p_z个坐标使用菜单叶z；其后角色i+1规定各叶的B，B之后贴该叶真正后续SPE的积。下一角色总利润ΣD p_zv_z≥Dθ。

对任何其他联合动作(B₁,…,B_D)，所有坐标**含未改者**各选使下一角色收益达到相应min的真后继，再作产品，给总偏离≤Dθ。不同联合孩子是不同有序分支，可独立设定；后继真SPE产品确保所有更深联合历史IC。因此从强制A向量之后得到真完整SPE，当前第i角色总所得恰D barL_i^t(A)。当前A向量本身无需在父节点最优。

若某坐标所选叶v<θ，其投影不是该坐标完整SPE，但下一角色跨坐标真实利润盈余足以付总IC；B后子树本身仍逐坐标真SPE。不能用“产品投影必SPE”阻止这种合法补偿，也不能把LP叶分布直接执行成随机玩家策略。

# 任意复制数和任意联合query的统一余数

取任意整数n_t≥0，产品P为n_t副本的**完整Cartesian**目录，固定同一目标z_P及正常路径，各坐标都为z^t。无偏离正常j尾用同一π^t积，是真完整SPE。每(i,A)已固定分母D，与n无关。

在同一正常h_i^P强制任意合法联合主题B=(B^1,…,B^N)，按(t,B^l=A)分组；每组拆D整块加至多D−1余项。整块用上节可信子SPE；每余项用达到L_i^t(A)的原真孩子。所有块/余项产品是强制B后的真完整SPE。因此

\[
L_i^P(B)\le\sum_l\bar L_i^{t_l}(B^l)+C_i,\quad
C_i=\sum_{t,A}(D_{t,i,A}-1)[L_i^t(A)-\bar L_i^t(A)]\ge0.
\]

C_i与B、n均无关。即使n_t被所有D整除，任意联合query的**各主题组人数**也未必整除，不能免费令C_i0。

令barM_i^t=max_AbarL_i^t(A)，d_i^t=barM_i^t−u_i^t（保符号），C=max_(i≤j)C_i，取全部联合B的最大得

\[
M_i^P\le\sum_tn_t\bar M_i^t+C_i,\quad
u_i^P(z_P)=\sum_tn_tu_i^t,\quad
\Delta_P\le\max\{0,\max_{i\le j}(\sum_tn_td_i^t+C_i)\}.
\]

这是**真M上界**，不是可加等式。某A有barL<L不保证取max后的barM<M，更不保证最大角色缺陷Δ严格下降。

# 所有i为何能服务同一保险输入

各i每个query用同一P、同一z_P、同一h_i^P和同一目标利润；没有为不同i换目标叶或π尾。只需每(i,B)各存在一份真孩子，不要求在无保险的原P中把它们连同不可信normal目标预拼成一张策略。

加入前缀bank后，第一次银行/联合异常的位置和动作给不同完整产品历史；即使旧B等于normal旧动作，保险变化仍区分这次真实子树，原编译器永久进入该(i,B)孩子。其他i的假设退出因firstbank位置不同不冲突；无偏离一直保同一π产品尾。全部联合偏离与正常主动作不变的保险异常都包括。

该一般闭包来自早期全m产品转移稿的barL及有限主题余数；三人[精确菜单凸化](../定理/三人笛卡尔可信菜单与根门槛凸化极限--定理.md)有更强特殊刻画，但不从其r3下界等式推出这里全m等式。旧[福利非可加](../反例/笛卡尔目录的福利非可加性--反例.md)也只说明一般产品SPE可耦合，不是此组合的新half种子。
