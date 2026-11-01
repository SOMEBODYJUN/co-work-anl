# 任意比较组合的坐标保留双预算初始化

2026-10-24，Boss10/root。任意有限共同目录、任意人数、每份完整历史纯 SPE。**一般 Q-CAG-HALF 仍 OPEN。** 本页由 root 在保留 B 正价的反向 SD 核上推导；global 和 coupling 均从陈述独立核对，见 [global 审查](../global/two_budget_initialization_audit.md)和 [coupling 合同盲重构](../coupling/optimal_coordinate_inventory_blind_review.md)。没有外审或新颖性认证。

## 1. 固定同一个实际父叶

B=(B_1,...,B_m) 是给定完整 SPE 的实际终局，利润为 u_i。取任意比较元组 T=(T_1,...,T_m)，并集 O，负载 c_T。比较元组本身不要求 SPE；最优性只在最后把 |O| 识别为 OPT_m。

对 x∈T_i，定义

    p_ix=1/c_T(x)， d_ix=c_B(x)+1−1_(x∈B_i)。

这是客户 x 分给比较角色 i 的单位库存份额；Σ_(i:x∈T_i)p_ix=1。

W_i=finish_sigma(B_<i,T_i) 是同一原策略的真实偏离完成叶。用静态中间分母 SD 的逐客户正负量 P^B_ix,N^B_ix,P^W_ix,N^W_ix，原始恒等式为

    p_ix = z_ix + P^B_ix − N^B_ix + P^W_ix − N^W_ix，
    z_ix=1/c_(W_i)(x)。                           (COORD)

P^B 送到实际 B 角色；P^W 只送到 W_i 的 j>i 真 prescribed context，原价

    q^W_ij(x)=1/[d_ix c_(W_i)(x)]

的支持为 x∈T_i∩(W_(i,j)\B_j)。所以第一批未来来源是该角色 actual 主题未覆盖的客户，可能在别的 actual 角色已被覆盖；不能一概称为 fresh。

## 2. 坐标剩余与一次 whole-IC

第一类正价的 ROW 逐客户给 P^B_ix≤p_ix。置

    r_ix=p_ix−P^B_ix≥0， q_ix=P^W_ix≥0， r_i=Σ_x r_ix。

COORD 立即给

    r_ix−q_ix=z_ix−N^B_ix−N^W_ix≤z_ix。

因 z_ix≥0，所以正部仍满足 (r_ix−q_ix)_+≤z_ix。**此处尚未按客户使用 IC。** 先求和，之后只使用原节点 i 的一次完整收益比较：

    Σ_x(r_ix−q_ix)_+ ≤ Σ_x z_ix = u_i(W_i) ≤ u_i。

于是

    S_i:=Σ_x min(r_ix,q_ix)
        =r_i−Σ_x(r_ix−q_ix)_+ ≥ r_i−u_i。

需要外送的总额 b_i=(r_i−u_i)_+ 因而满足 0≤b_i≤S_i。可明确选

    a_ix=(b_i/S_i) min(r_ix,q_ix)  (S_i>0)，否则全零。

将 a_ix 再按原 q^W_ij(x) 的比例分到每个 j>i；q_ix=0 时 a_ix=0。所有原边子容量、客户标签和真实 context 域均保留。

当前支付留下 c_ix=r_ix−a_ix≥0，满足

    d_i:=Σ_x c_ix=r_i−b_i=min(r_i,u_i)≤u_i。

这笔 d_i 付到 actual i 的完整利润行；x 仅是来源库存标签，**不要求 actual B_i 覆盖该 x**，不可将其误读成 actual(i,x) 客户券。

每个坐标精确守恒：

    p_ix=P^B_ix+c_ix+Σ_(j>i)a_ijx。

因此所有比较角色合起来，每个 O 客户的一单位都被精确保留，没有凭空新增客户库存，也没有按客户重权调用原 IC。

## 3. 已付两份预算与精确剩余

记 H_l=Σ_i P^B_i,l 为第一类正价最终付给 actual l 的金额。固定父 B 共同 COLUMN 给

    0≤H_l≤u_l(B;(O∩B_l)\T_l)≤u_l。

当前支付 d_l≤u_l。于是初始化的这两类支付同时有界，且

    |O|=Σ_l(d_l+H_l)+Σ_i b_i。                   (INIT-2)

将**只包含** a_ijx 的真实未来 injections 放入同一份原 full-customer SAFE/合法 CLIP 图，重算全部同 context 输入，得到非负 actual 终端金额 A_l^out，Σ_lA_l^out=Σ_i b_i。这个接法只用既有严格 future 角色 DAG，无需将反向 SD 递归加入而引入新环。

因此一个精确的充分目标是

    A_l^out≤R_l:=2u_l−d_l−H_l  对每个 l。         (RESIDUAL-CAP?)

这里的通用候选量词是：每个原实例、每份完整 SPE，是否存在一个最优 T 及允许的坐标剪枝/全客户 SAFE 或 CLIP 选择，使这些角色界同时成立；没有声称对每个固定 T/路由成立。

R_l≥0，且有可见的不交支持余量

    R_l≥(u_l−d_l)+u_l(B;(B_l\O)∪(B_l∩T_l))。

但没有证明 RESIDUAL-CAP，也没有证明更弱的总资金上界；INIT-2 只是把所有已付项和未付来源放进同一张可审计的账。输入 future q_W 的来源标签 i，后续 past 出口不早于 i，因为每个初始 history 在 i 前等于 actual；这只给时间支持，不能给 whole INIT 行 PRICE/HIT——当前剪枝后需另证该价格合同。

## 4. 仍缺什么，以及没有证明什么

剩余量是这批受控 O 客户未来来源在原全客户重采后的共同 actual 容量。它们每个源坐标有库存上界且第一接收角色的 actual 主题不覆盖源客户，但 whole-profit 重采不保留后续客户支持；不能把源单位库存偷换成 actual 钱包余额。单个 context 的 ell、SAFE/CLIP 或时间界也没有解决多来源列容量。

本页是一个一般初始化/充分接口，未扩大 Q-CAG-HALF 的已证输入范围。没有把等式 |O|=已付+未付 当作福利证明；真正需要的是 RESIDUAL-CAP 或另一个可合法支付未付部分的一般关系。

## 5. 真正激活未来来源的定义级审计

[独立实现](audit_coordinate_initialization.py)不导入 solver/作者实现，展开同一旧348单位客户与不变全历史策略，固定最优 T=(5,2,4)、actual B=(0,3,4)。重算全部比较库存和坐标分配后，current=(147/2,159/2,69)，B-columns=(20,18,0)，future=(10,0,0)，合计270=OPT。10单位未来来源在原全客户 SAFE 图中激活3条正边；每个 O 客户库存精确为1，终端守恒通过。[冻结结果](coordinate_initialization_independent.json)明确仅是一个非零实现检查，不能当一般 RESIDUAL-CAP 或 half 的证据。原完整策略43历史/258含自身IC已由同目录另一root脚本独立核对。
