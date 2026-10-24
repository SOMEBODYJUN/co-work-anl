# 全 fresh／全客户广播组件的独立审查

2026-10-24，Boss10 independent_proof。**结论：核心表示组件通过独立解析审查；它不是 half 付款定理。** 下文两处范围措辞宜澄清，不影响 LOSS、合法域、DAG 消元与 COUPON-LOAD 的正确性。未认证文献新颖性或外审。

审查输入为 `credible/all_fresh_submarkov_elimination.md`，已冻结为本目录 `broadcast_author_snapshot.md`，SHA256：`92097196be6df0fd2da75785d0c39749b485cdb334dc0e05972cd6346502ac91`。先依 root 消息独立写成 `broadcast_blind_reconstruction.md`，之后才读作者全文对照。未读取作者或 root 的审计实现。

## 1. 固定量词、两个 completion 与零域

采用一般 CAG-MODEL，固定任意完整有序历史纯 SPE σ，实际有序叶 Z、实际覆盖 C。对自然 context t=(g,i)，a=σ_i(g)，B=finish(g)，A=finish(Z_<i,a)。v=u_i(B)，D=u_i(A)，e=u_i(Z)−D≥0。e 只用实际第 i 节点的真实偏离 IC；它是总利润 slack，不是逐客户非负量。

所有式子都逐真实有序 context 运算，不识别同主题或同计数的不同历史。A 的未来可与 B 全部不同；没有冻结后继。

有限单位客户下 v=0 当且仅当当前规定主题 a 为空客户集。此时 D 与全部 q、P、N、J、L 都为零。作者第3节已把任意非负初始注入限定到 v>0 的 context，因此 β=h/v 的零域正确；不能再无条件允许空主题节点有正 b。正边接收者含其传输客户，必有正利润，所以正域递推闭合。

末位 i=m 没有 future 边；全客户版可以有 past 出口。m=1、全零目录、空主题、重复行动和相同覆盖标签均不改变上述处理。

## 2. 独立重构的逐客户恒等式

对 x∈a，在两叶中均由当前角色 i 覆盖，令 J_A,J_B 排除 i，c_A=1+|J_A|、c_B=1+|J_B|。写 p=|J_A\J_B|、n=|J_B\J_A|、l=|J_A∩J_B|。则

\[
c_A=1+l+p,\quad c_B=1+l+n,
\]

\[
\frac1{c_B}-\frac p{c_Ac_B}
=\frac{1+l}{c_Ac_B}
=\frac1{c_A}-\frac n{c_Ac_B}>0.
\tag{U}
\]

因此全客户式 `v−P^>−P^<=J^all+L^all=D−N^all` 正确，严格号正好限于 v>0。q± 的方向也正确：A-only coverer 为正广播，B-only coverer 为负项。

对 fresh x∉C，A 的过去无人覆盖 x；B 的过去覆盖数为 b(x)，未来集合为 U,V。于是 p=|U\V|，n=b(x)+|V\U|，l=|U∩V|。直接代入 (U) 就给作者的 FRESH、F-DIFF 和 LOSS：

\[
v-P=X+J+L,
\qquad v-D=(X-Y)+P-N.
\]

这里 fresh 自身不必在 g 上首次出现，b(x) 可以正；作者确实保留了这部分负项，没有把 R/outside 误作 actual C。

对任意 k 个所选角色，固定 x 上所选 A-only 数 d≤k 且 c_A≥d+1，所以 d/c_A≤k/(k+1)。乘 1/c_B 后求和并除完整 v，得到 SUBSET。fresh 权重之和可以小于一，仍然成立。PRICE 也正确：对每个 x 取其实际正 recipient 子集，分母不小于一加该子集大小，再对 p_tx 混合。全客户对应的所有角色子集界同理成立。

这组关系是普遍计数恒等式；基础版确未使用 off-history 的 ell≥0，不能因此声称已支付所有后继理性。

## 3. future 与 past 的合法域分别成立

若 j>i 且 q^+_tj(x)>0，A 在 j 及以后按原 σ 行动，所以新 context (A_<j,j) 的规定动作正是 A_j，规定完成叶恰为 A，且 u_j(A)>0。原 g 的过去如何变化不影响这个事实。future 角色严格增大，所有自然 context 是有限 DAG。

若 j<i 且 q^+_tj(x)>0，则 A_j=S_j 为原实际动作，x∈S_j 且 x∉g_j，故 x∈C。此项可以写成 actual coupon (j,x) 的需求，且该券价值 1/c_Z(x)>0。这里**没有**调用 A 中过去玩家 j 的 IC；A 包含其未来的强制 query，不能冒充该过去节点的规定完成叶。

作者将出口 z 形式化为实际 context 的 z/u_j 系数也合法，因为正出口蕴含 u_j>0；这只是一种需求表示，不是券容量证明。若把实际 context 同时展开进递推，不能又把同一出口另加一次。

## 4. DAG 消元与 source 同钱包

在正利润 context 上给非负注入 b，定义 h=b+incoming，β=h/v。按角色递增唯一确定所有量。对全客户版只递推 future 正项，有限求和时各 future 边恰好出入相消，得到

\[
\sum b=\sum\beta(v-P^>)
=\sum\beta[J^{all}+L^{all}+P^<]
=\sum\beta[u_i(Z)+P^<-N^{all}-e].
\tag{F}
\]

fresh 版没有 past，逐节点 `(v−P)=X+J+L>0`，同理得到 MASS 和 C-LEDGER。两个图的 β 分别重算，不能相加付款，也不能替换旧 capture-flow 的 w。

INIT 也正确：对一个被 owner query 首先覆盖且原实际遗漏的 x，实际前缀不覆盖它，故当前加全部真实未来 coverer 的 rho/c_Y 份额恰好相加为 rho。future 注入对象均为真实规定 context。每个单一 source 的当前吸收≤其 query 利润≤实际 u_i；多个来源合并后没有 β≤1 或同角色总系数≤1 的推论。

全客户式的正 actual 需求精确为

\[
\sum_{j,x\in S_j}\frac{\Lambda_{jx}}{c_Z(x)},\qquad
\Lambda_{jx}=\sum_{t:i=j}\beta_t+
c_Z(x)\sum_{t:i>j}\beta_tq^+_{tj}(x).
\]

若 source 吸收用实际整行支付，可取 gamma_i=A_i^src/u_i（u_i=0 时 source 也为零，取 gamma_i=0），其需求必须加在**同一个** coupon 系数 `gamma_j+Lambda_jx` 中。负 N、e 目前只以总项保留；过去 q^- 的角色来自 g，不一定是实际 S_j，故不能按客户名任意退给实际 (j,x)。作者准确停在这个缺口。

## 5. 同 context 取消、因果区间及可选折扣

作者第6节的 past-first 取消正确。因为同 context、同客户的正负单价均为 1/(c_Ac_B)，取消 min(p,n) 对使剩余净值不变；剩余过去正数 `(p_<−n)_+` 不超过 `(pastload_A−pastload_B)_+`。删减核逐边不增，在同一 v、同一 b 的角色 DAG 中归纳即有 β'≤β。whole actual 与 past 正需求分别不增，但负退款也变化，不能单独保留旧退款后声称更优 net 付款。

取消后正边只留 c_A>c_B 的客户；沿保持同一个客户的后继边，其旧规定叶负载严格增加。完整行归一化可以重采其他客户，作者没有把它错误扩大为全部流的共同负载势。

第7节 INTERVAL 对 INIT 生成的单条谱系成立：父 query k 产生 context i，则两历史在 j<k 上相同，过去差异只在 [k,i)；下一条 future 边到 l 后，新差异区间为 [i,l)。对任意外加 b 的自然 context 不自动有该源区间结构。

**需澄清的一处措辞：** “单谱系每角色只出现一次”应限于这些 **past 差异／出口区间**，不能解释为所有实际费用每角色只出现一次。当前角色 i 的 whole actual 费用 β_tu_i 之后，下一代区间 [i,l) 仍可向角色 i 的 past coupon 收费。下面的合法非零例实际出现此情况。该澄清不改变 INTERVAL 或作者明确保留的共同容量缺口。

第9节令 nu=v−chi、chi≤κ(v−P)、κ<1，则 `nu−P≥(1−κ)(v−P)>0` 正确，故重算后的图仍为严格 sub-Markov DAG，相应 signed ledger 多 −chi 也正确。**需明确**旧 SUBSET/PRICE 的数值常数不能因这句而原样继承到分母 nu；通常只能先乘 v/nu，再另用严格行和界。作者没有明确声称保留这些常数，故是范围澄清而非代数反例。β 需重算且可能增大，净费改善仍未证。

## 6. 独立的非零 fresh 传播实现审计

`audit_broadcast.py` 不导入作者脚本、root 审计、规范 SPE solver 或 payoff verifier，直接建立22名不同单位客户。原十四客户残余例的 A,B,T,D,E 外，加8名只属于 H 的客户，并取3位玩家。实际叶为 `(H,A,B)`，利润 `(8,4,5)`。

末位在全部36个有序前缀直接选最佳回复；H 后沿原两人 SPE 的末位规则。H 后第二位选 A；D 后第二位选 T；其余首前缀按真实末位续局逐一最大化。根 H 收8，任何原主题总大小至多6，所以根严格最优。脚本按单位客户全树精确重放43个决策历史、258项含自身动作 IC。

本例专门使 fresh 广播不为零。对 natural context `g=(D),i=2`，规定 a=T，

\[
B=(D,T,H),\quad A=(H,T,D),\quad v=D=4.
\]

两名 T∩D 客户均在实际 C 外，原 B 由过去 D 覆盖、重置 A 由未来 D 覆盖；每客户产生 future 正价 1/4 和 past 负价 1/4，总 `P^>=N=1/2`，接收 context 为 `(H,T),i=3`。此末位 context 的 reset 叶为 `(H,A,D)`，产生 past-C 正价1及 fresh 负价1。

合法 INIT 取第一位 source query D、rho=1 只放在这两名遗漏客户：rho 总2=source吸收1+注入1。于是第一自然 context β=1/4，向末位传利润1/8，末位 β=1/40。fresh/all 两个图的消元质量都精确为1；全客户实际 coupon 正需求为23/20，负 N/e 退款为3/20，差为1。fresh C-LEDGER、past-first 取消后新流、β'≤β也精确通过。

输出冻结在 `audit_broadcast.json`。这只是一个明确非零的实现及域测试，不是一般模型的计算覆盖，也不证明容量或 half；一般正确性的依据是前面逐客户代数与有限 DAG 证明。

## 7. 审查后的真实状态

已核的新增一般关系是：所有客户的 future 正项可送到合法规定 context，past 正项明确变成 actual coupon 出口，并在利润归一化的有限 DAG 中给出 (F) 及精确需求系数 Lambda。fresh 创新不需要另领 owner 库存；作者没有声称这解决 actual C 的共同容量。

尚未证明 source、whole actual 行与 past 出口在同一实际预算 W 中只付一次；也没有负 N/e 的同券退券方案。该组件不等于旧 K_in 下降、PB-extra、W≥mv、一般 half 或任何 cap1 定理。两项措辞澄清后，可作为全范围内部可靠的**表示与消元组件**使用。
