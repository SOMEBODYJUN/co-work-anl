# 共享菜单负载的凸对偶：未闭合草稿

本页是父方对 aggregate11 自由共享负载候选的解析展开，不是新一般福利界。原 half、一般聚合安全值均 OPEN。所有历史仍沿原完整策略；没有固定后继。

实际角色 i 的真实强制行动 A 叶删除当前槽后的负载记 L_i(A)。自由共享负载域是 K=(1/m)Σ_i conv{L_i(B):B∈S}，每个 L∈K 仍是总质量 m−1 的合法分数目录负载。给查询分布 p，ρ_x=Pr_p[x∈A]，F_p(L)=Σ_xρ_x/(1+L_x)。

候选是对每个 p 有 min_(L∈K) F_p(L)≤W/m；若真，凸 minimax 给共享背景的全目录 cap，进而 W≥m δ_m，再由既有静态比较推出 half。这里只保留准确充分性，不把问号消去。它比先分别计算每个删槽背景 reciprocal 再平均的 AFC 更弱，不能同已败实际缩放背景混同。

固定其极小负载 L*，令 t_x=1/(1+L*_x)。KKT 给任一实现 L* 的每个支持菜单列 B：L_i(B) 最大化 Σ_x ρ_x t_x² L_i(B)_x。此处最大化符号来自 F 梯度为负。

逐项精确式对任意 z≥0、l≥0 有

    1/(1+z) = 1/(1+l) − (z−l)/(1+l)²
                 + (z−l)²/[(1+l)²(1+z)]。

代入真实查询，记 IC_i=u_i−E_A d_i(A)≥0，可得

    W−mF_p(L*) = Σ_i IC_i − C + D,
    C=Σ_i E_A Σ_(x∈A) t_x² [L_i(A)_x−L*_x],
    D=Σ_i E_A Σ_(x∈A) t_x² [L_i(A)_x−L*_x]²/[1+L_i(A)_x] ≥0。

因此付款等价于 C≤D+ΣIC。KKT 只控制将 1_(x∈A) 换为 ρ_x 的去相关线性项；它没有直接控制 C。要求更强 C≤0 会够用，但未证且可能过强。不能只用 reciprocal 凸性或 KKT 把关联项丢掉。

新观察的用途是将同一共享分母下的剩余项变成明确的加权线性负载关联及 Bregman 正项；这只是等价/充分接口，没有新增金额。下一步应让完整后继 IC 与这个特定最优权 t² 耦合，而非扩大同一锥阴性。

## 后续独审与准确停界

[tree独审](../tree/shared_load_independent_review.md)核全部域、KKT、零ρ和IC，另保留G_KKT≥0得W−mF=ΣIC+G_KKT+D−Cov。仍无Cov金额界。joint saddle另给γ=F(p*,L*)，每个主题g_t(A)=Σ_A t≤γ，查询支持等号；L*是m−1份合法主题分数负载，故ΣtL*≤(m−1)γ。此额外条件不使C非正。

matching允许角色查询运输：每行p_i质量1且平均为p，仍精确W−mF_p(L*)=Σ_iIC_i(p_i)−C(p_i)+D(p_i)。每角色一份whole IC，此自由度不是资金。

[精确旧保险族诊断](../aggregate/shared_load_components_and_exact_sign_boundary.md)证明m6有唯一global primal负载，所有joint saddle仅支持nonanchor主题，逐行C在这些主题恒定。共同重选saddle及角色运输仍C135/242>0，但D2017/1210、IC4/5给W−6γ21/11>0。只关闭C≤0加强，不否定SHARED。[matching独审](../matching/insurance_saddle_independent_review.md)及[root字面16客户复核](shared_insurance_literal_independent.json)通过；全历史SPE继承同行一般证明，180菜单不是全树审计。

C≤D等价于原查询总和Σ_iE_p d_i(A)≥mF，也是未证加强，不是已败个体SELF。完整C≤D+ΣIC仍是一般义务。[terminal同p互补银行](../direct/direct_general_working.md)提供另一精确非负需求，早期IC仍未付款。[saddle完整后继IC尝试](../tree/saddle_price_law_and_variance_attempt.md)保留输入/后继两种曲率及r_beta插入势差；等price条件不能免费删它。

同式m5只给条件9W/5，无无条件half。本轮停在上述实际推导的金额缺口，未有新福利界、目标反例、外审或新颖性认证；不重复零C、原钱包系数或同锥阴性来代替付款。

## 直接按原half放松，而非强求锐2−1/m

原目标只需较弱的shared界 W≥(m−1/2)γ，因为已有静态关系 OPT≤(2m−1)δ_m≤(2m−1)γ。于是准确付款目标可放松到

    C≤D+ΣIC+γ/2。

这是允许的目标余量，不是一笔已经存在的信用。强SHARED仍OPEN；较弱HALF-SHARED也未证。m5同式是(9/2)γ≤W即可给OPT_5≤9γ≤2W，仍完全依赖未付的不等式。后续优先判断完整后继重置/曲率差能否由这一半个共同query及已保留的银行共同支付，不必强求C≤D或W≥mγ。该放松本身没有新增无条件福利界。
