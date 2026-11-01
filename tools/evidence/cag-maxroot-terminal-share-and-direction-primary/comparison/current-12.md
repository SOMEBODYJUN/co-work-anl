---
id: "customer-attraction/history-mean-floor-domain-with-frozen-actual-tag"
kind: "lemma"
type_tag: "引理"
title: "逐历史均值门槛的受限实际标签域与重置资格"
status: "proved-endpoint-characterization-and-dual-credit; reset-transport-unresolved"
summary: "由当前人max-min门槛刻画全部孩子SPE端点，再放松为每个严格未来有序历史的均值floor；对偶仅价允许raw标签，实际tag改尾仍需重标及钱包运输。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/reset_floor_domain_independent_check.md"
---

# 规范门槛与全部有序端点

采用[有限单位客户、共同目录与完整历史模型](../定义/共同目录完整历史模型--定义.md)。人数\(m\ge1\)，目录有限非空，允许空主题、重复、零客户和任意离轨历史平局。对任意有序历史\(h\)，令\(\mathcal R(h)\)为其后**某份完整纯SPE**可产生的全部有序终局；\(\mathcal R(h,A)\)表示当前人被强制选择\(A\)后，未来采用完整孩子SPE所得的终局全集。若当前角色为\(k=|h|+1\)，规范门槛定义为
\[
\boxed{M(h)=\max_{A\in\mathcal S}\min_{z\in\mathcal R(h,A)}u_k(z).}
\tag{M}
\]
内层取的是**同一当前角色\(k\)**的终局收益，不是孩子下一角色的收益。游戏有限，纯SPE逆向归纳保证每个孩子全集非空，所有最值达到。

此\(M(h)\)也等于\(\min_{z\in\mathcal R(h)}u_k(z)\)。一向由节点IC：任意当前规定叶对每个备选孩子的实际续局收益都不小，而该备选收益至少为其孩子全集的最小值，故规定收益至少\(M(h)\)。反向取达到max的行动\(A^*\)，该孩子选达到本行内层min的完整子SPE；每个其他行动孩子也选达到自身当前角色收益min的完整子SPE。不同**有序孩子**的后代互不相交，可同时拼接；选\(A^*\)时收益恰为\(M(h)\)，并不劣于任何其他孩子。于是得到收益恰为\(M(h)\)的完整纯SPE。

进一步，对任意延伸\(h\)的合法有序终局\(z\)，有
\[
\boxed{z\in\mathcal R(h)\quad\Longleftrightarrow\quad
u_k(z)\ge M(z_{<k})\ \text{对所有后缀决策角色 }k.}
\tag{FLOOR-IFF}
\]
必要性在选定路径每个节点用上面的IC比较。充分性沿指定\(z\)自后向前构造：所选孩子使用已经构好的后缀SPE，每个离轨兄弟孩子独立拼入使当前角色收益最小的完整子SPE；(FLOOR-IFF)使指定行动不劣于全部兄弟。这样既保指定有序路径，也填写全部离轨子树。

这是既有[终局全集递推](../算法/完整历史纯SPE终局全集--算法.md)与可信菜单的机制，不认领为本源新发现。相同计数历史的后缀游戏同构，故规范全集及\(M(h)\)可按计数缓存；给定\(\sigma\)在两个同计数有序历史仍可选不同后继，原历史对偶乘子也不能据此设成相同。

# 保留实际标签限制的分析放松

固定原完整纯SPE \(\sigma\)、实际路径\(B\)、实际前缀\(h_i=B_{<i}\)、实际收益\(u_i\)。一行\(i\)的raw带标签叶\((A,z)\)保留\(h_i\)，进入角色选\(A\)，未来主题任意；若\(A=B_i\)，**仅允许原实际终局**。记该有限允许集合为\(\mathcal Z_i^{\rm fr}\)。叶不必为孩子SPE；\(d_i(z)=u_i(z)\)，\(\ell_i(z)=c(z)-\mathbf1_{z_i}\)。

行内每个严格未来有序历史\(h\)的当前角色为\(k>i\)，定义
\[
\Delta_{ih}(z)=\mathbf1_{z\text{延伸}h}\,[M(h)-u_k(z)].
\]
考虑归一彩票\(q_i\in\Delta(\mathcal Z_i^{\rm fr})\)，约束
\[
E_{q_i}d_i\le u_i,\qquad
E_{q_i}\Delta_{ih}\le0\quad\text{对每个严格未来有序历史 }h.
\tag{MF}
\]
强制进入角色\(i\)本来无需最佳回复；若再给它加\(M(h_i)\)的floor，会错误排除合法强制孩子。所有floor只对\(k>i\)实施。

原\(\sigma\)每个强制行动后的真叶在允许集合中，且进入收益\(\le u_i\)，所有严格未来floor逐叶成立。因此(MF)非空，有限线性约束给紧凸多面体。它包含[可信端点全行均值cap域](可信端点均值cap的三域与松弛信用--引理.md)的所有彩票，却一般不等于\(\operatorname{conv}\mathcal R(h_i,A)\)或纯/混合SPE实现域：同一\(h\)内的正floor缺额可以由负缺额抵消。约束中的\(\mathbf1_h\)没有合并不同有序历史。

# 对所有允许raw列的对偶及原源正信用

固定线性shadow分数\(s_i(z)=w\cdot\ell_i(z)\)。最大化其期望的有限LP有对偶\(\mu_i\ge0\)、\(\lambda_{ih}\ge0\)、\(\eta_i\in\mathbb R\)，满足
\[
H_i=\eta_i+\mu_i u_i,
\qquad
s_i(z)\le\eta_i+\mu_i d_i(z)+\sum_h\lambda_{ih}\Delta_{ih}(z)
\quad\text{对每个 }z\in\mathcal Z_i^{\rm fr}.
\tag{ALL-PRICE}
\]
符号来自最大化拉格朗日函数减去\(\mu_i(E_qd_i-u_i)\)及\(\sum_h\lambda_{ih}E_q\Delta_{ih}\)。\(\eta_i\)没有非负要求。(ALL-PRICE)对每个保留的raw变量成立，哪怕该叶作为单点彩票违反(MF)；因此允许的非实际标签重置叶也被定价，同时显式支付其所有floor缺额。

源始终保留原\(\sigma\)真查询叶\(z_i^0(A)\)。对任意共同查询\(A\sim p\)，有
\[
I_i=u_i-E_pd_i(z_i^0(A))\ge0,\qquad
\Delta_{ih}(z_i^0(A))\le0.
\]
令约化成本
\[
R_i(A)=\eta_i+\mu_i d_i(z_i^0(A))
+\sum_h\lambda_{ih}\Delta_{ih}(z_i^0(A))-s_i(z_i^0(A))\ge0.
\]
若\(G=\sum_i[H_i-E_ps_i(z_i^0(A))]\)为同一共享shadow最优域的KKT差额，则逐行代入得
\[
\boxed{G=\sum_i\mu_iI_i+
\sum_{i,h}\lambda_{ih}E_p\bigl[\mathbf1_h(z_i^0(A))
                    (u_{|h|+1}(z_i^0(A))-M(h))\bigr]
+\sum_iE_pR_i(A).}
\tag{FLOOR-CREDIT}
\]
各项非负，但只分拆同一\(G\)，不是新增三份独立库存。

# 实际标签例外与未付运输

若原源的进入主题就是\(B_i\)，在其未来某人处改变动作所得叶仍带\(B_i\)却已改尾，一般不属于\(\mathcal Z_i^{\rm fr}\)；因此(ALL-PRICE)不能自动用于这片叶。它可按其相对原实际路径的**第一次偏离角色**重索引到更晚行，此时允许资格改变，但\(\mu,\lambda,\eta\)、归一概率和可支配原源库存也一起改变。身份重标本身未证明跨钱包预算相容。

另一选择是明确释放实际标签到所有raw叶，得到更大的分析域；原源仍证明非空，但不再是本页受限标签域。现行[规范门槛均值域与复制成本](规范门槛均值域与复制偏离的精确成本--引理.md)已采用这种释放后的版本，并另区分单行NET-cap和全局NET-cap。释放标签、合并cap及统一乘子各是单独的域变化，不能无声明地互换。

重置会改变所有更早未来祖先的终局收益，所以需检查其影响到的**每个祖先**floor，而非仅偏离人的一个floor。要把正重置缺额支付为(FLOOR-CREDIT)，仍需将所用重置叶的到达质量运输到同一原源的floor盈余和约化成本，并证明不重用。某历史未被任何原查询源达到，则该历史原源盈余库存为零，即使其\(\lambda_{ih}>0\)。所选背景的互补松弛只说明正乘子处目标**均值**floor紧，容许正负缺额抵消；它未界定任意新增重置需求。

允许raw叶这一改变移除了非实际标签重置的“必须是完整孩子SPE端点”资格门，但实际标签例外、祖先缺额、到达容量和单次支出仍在。本页没有给这些义务的联合付款。

# 实读比较与关系

主源4473字节全文实读，另读后续matching对实际标签例外的明确修正、credible的重置恒等式、现行真实流及复制成本正文。源自述是收到root放松合同后攻击端点刻画/域/对偶符号的内部检查；后续matching确认这些符号并报告实际tag门。原内部先后关系保留，不称本批盲审、外审或金额认证。原件及对比路径见[证据资源](../../tools/evidence/credible-cap-fixedpoint-primary/README.md)。无程序源、无新增有限扫描。

本页保持原受限实际标签域身份，现行释放标签复制引理保持其更大域身份；二者共同依赖规范门槛与有序孩子独立拼接，关系是显式域包含和条件对偶比较。原源的五人未得half只说明本接口停界，现行另证[五人半覆盖](../定理/五人半覆盖--定理.md)不受影响。六人或一般人数付款均未由(FLOOR-CREDIT)闭合。正式超图留第三阶段。
