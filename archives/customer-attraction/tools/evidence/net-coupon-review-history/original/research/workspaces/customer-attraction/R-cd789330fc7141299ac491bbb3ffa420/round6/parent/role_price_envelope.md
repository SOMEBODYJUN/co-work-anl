# 净券行的uniform-subset表示与全图角色价格包络

2026-10-24，root。原模型全部输入，任意完整历史纯SPE。此为一般角色价格关系，不是actual客户券cap或福利证明。relay提出全图HIT，root收到陈述后独立重构；以下给更强局部表示和其价格层积分，作为衍生工具而非另领一次主目标进展。

## 1. SAFE净券行的局部凸包

固定natural context、v>0。完整客户核每个recipient角色j原价q_j满足

    q_j ≤ J ≤ J+L = D−N。

这是逐客户包含关系：q_j仅在某些客户上取1/(c_A c_B)，J在当前行动全部客户上各取一次。SAFE后current actual角色i吸收p_i=(J+L)/v，每个其他角色j获正出流p_j=q_j/v，合计一；未来送真实natural context，过去送actual角色终端。因此p_j≤p_i。fresh-only核以nu取代v、无past，同式成立；CLIP删正边并增加current吸收，也保留该不等式。

任意概率向量p满足p_j≤p_i，当且仅当它在“包含i的非空角色子集上均匀分布”的凸包中。构造：对0<t≤p_i令U_t={j≠i:p_j≥t}，以密度(1+|U_t|)dt混合uniform({i}∪U_t)。总混合质量p_i+Σp_j=1；i的边际p_i、j的边际p_j。有限个断点给有限混合。故任意角色价格lambda_i和recipient续价z_j有

    p_i lambda_i+Σ p_j z_j
      ≤ max_U [lambda_i+Σ_(j∈U)z_j]/(1+|U|)。

这里只在角色层聚合past标签，不改变actual(j,x)容量，更不购买过去IC。

## 2. 全图HIT的独立重构

固定k角色集K，h=k/(k+1)。对当前角色i不在K的任意natural source，current净吸收的K命中值0；past终端在K取1、外K取0；future在K最多1，外K由角色逆序归纳最多h。一个subset最多含a≤k个价1，其余l个价≤h，故

    (a+l h)/(1+a+l) ≤ h。

由上一节凸包，最终actual角色落K概率≤h。角色在K的source只用平凡上界1。past边是终端，未假设它能向过去递推；future严格递增保证归纳终止。同一角色的不同context保持区分，跨客户重采不破坏这项角色概率上界。

合法OPT-owner INIT中，每个客户从owner当前角色和真实查询叶的其他coverer中均匀选一个：past actual coverer进终端，future进真实context，current份额用同一whole-IC作actual整行净付款。该首行也属上述凸包。所以若owner源总量为M_i、终端actual角色总净券质量为A_j，便有

    A(K) ≤ M(K)+k/(k+1) M(K^c)。

全O源只在full核使用；仅fresh核允许R或固定fresh残源。各用自己的同一合法初始化，不能混用旧SOURCE预付。

## 3. 任意非负角色价格的层积分

固定源owner i，给actual角色非负价格lambda。把高于lambda_i的其他角色价格降序列为lambda_(1)≥...≥lambda_(l)>lambda_i。HIT应用于这些前k个高价角色，加权层积分给源的一单位最终角色价上界

    H_i(lambda)=lambda_i/(l+1)
                 +Σ_(k=1..l) lambda_(k)/[k(k+1)]。

证明：以lambda_i为基线，丢去低于基线的负项；每层命中质量至多k/(k+1)，再按价格差望远镜。l=0时H_i=lambda_i。于是整个合法初始化和净券图有

    Σ_j lambda_j A_j ≤ Σ_i M_i H_i(lambda)。

这是HIT的解析推论，不是新的独立容量假设；lambda为K指示向量即还原上一节。它可接角色价格对偶，但只含M和lambda，没有actual u容量。

## 4. 实际未付点

A的总量恒为M。上述反集中和价格包络并未给A_j≤u_j，更没有按actual客户标签的load≤1；lambda恒1只得到M≤M。因此不能把它叫全局费用≤W，也不能从跨角色分散推出half。即便source current系数各≤1，不同来源仍可复用同一actual行。

full/fresh核及CLIP的新beta各不同，这里分别适用它们自己的守恒图，不将三份券叠加。基本coverer核仍未实质用off-history ell≥0；真实后继IC或其他机制怎样限制这些净券总量，仍是一般承重点。

## 复核与策略域

relay读稿后独立逐式重构通过（非盲），核对uniform-subset边际、价格基线和full/fresh/CLIP域。HIT作者[自足正文](../relay/global_role_coupon_hitting.md)保留原发现/独审来源，本页不另算重复价格关系。

结论针对固定合法净券核与初始化。事先确定rho/owner/删边后可重建同图；观察随机路径后续结果后再选择保留source，或套用另一priority-world适应取消，均不能未经重证保留本图条件转移律。固定图HIT不自动涵盖事后选择的路径。
