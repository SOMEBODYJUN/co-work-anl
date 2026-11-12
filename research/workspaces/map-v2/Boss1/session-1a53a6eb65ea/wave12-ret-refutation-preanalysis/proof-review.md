# RET-COMPLETION-3D：只读预分析与精确漏接

本稿未认领core、未交formal coverage、未改registry/队列/canonical、未使用Git、未执行数学程序/LP/枚举。只读现有clone，输出只在本外部目录。全部当前合同快照、原字节全SHA、native object pins、实读范围见同目录 `refs.json`。

**结论先行。** Root提出的 `S_i≤L_i` 方向正确，但它已经是当前accepted canonical边的准确内容，不能登记为新桥。真正尚未接好的事项是：已proved的 `CA-PREFIX-BALANCE-NO` 使 `S_1=L_1>P_1`，从而反驳当前仍标open的 `M-dfcc6e32210c40c3b80ff0808d132d0b`。旧00c291覆盖说明甚至已经明确识别“负前缀族也使其随机池L_1>u_1”，但没有接到该候选端点。本轮应定位为既有反例到精确候选的漏接/状态勘误，不是新数学发现。

## 1. 精确输入映射与完整短证明

为防止行动和累计机会损失都写S，记实际行动为 `A_1,…,A_m`，实际前缀覆盖 `C_i=⋃_{j≤i}A_j`、`C_0=∅`；记累计机会损失 `𝒮_i=Σ_{j≤i}δ_j`，对应Root的 `S_i`。所有 `u_j` 都是同一完整原SPE actual终局收益，`P_i=Σ_{j≤i}u_j`，不是在第i步重新结算的前缀客户价值。

这里必须用privateledger/ME的**含过去覆盖的总覆盖**

\[
F_k(Q)=\max_{T\in\mathcal S^k}|Q\cup\textstyle\bigcup T|,\quad F_0(Q)=|Q|.
\]

它不是RET末段另一个同名 `F_r(b)=max Σ_x c_x/(b_x+c_x)`（背景下后继玩家最大总利润）。令 `V_i=F_{m-i}(C_i)`，则privateledger的定义恰为

\[
\delta_j=V_{j-1}-V_j\ge0,
\qquad \mathcal S_i=V_0-V_i=\mathrm{OPT}_m-F_{m-i}(C_i).
\tag{1}
\]

相消沿同一实际行动序列逐项成立；每个节点如何选择达到最大值的比较补全都不改变数值，因此“不断重优化”不引入额外差项。最初 `V_0=OPT_m`，末端 `V_m=|C_m|=W`。

固定合法m槽比较元组 `T=(T_1,…,T_m)`，并集记 `O`。均匀排列**槽索引**，删前i槽后保留的索引集为 `R_i`，令

\[
H_i(T)=\mathbb E|C_i\cup\textstyle\bigcup_{j\in R_i}T_j|.
\]

RET恰给 `L_i^T=|O|−H_i(T)`。对每个随机实现，保留的m−i槽都是 `F_{m-i}(C_i)` 的合法候选，所以

\[
H_i(T)\le F_{m-i}(C_i).
\tag{2}
\]

若T为最优、`|O|=OPT_m`，(1)(2)立刻给

\[
\boxed{0\le\mathcal S_i\le L_i,
\qquad L_i-\mathcal S_i=F_{m-i}(C_i)-H_i(T)\ge0.}
\tag{3}
\]

这里 `F_{m-i}(C_i)≤OPT_m`，因为actual i槽加任意剩余m−i槽仍是合法m槽。端点 `i=0,m` 的差均为零，特别 `𝒮_m=L_m=OPT_m−W`。中间等号恰在每份保留补全都达到静态最大值时成立（均匀有限支持上平均非负松弛为零）。`L_i−L_(i−1)`与 `δ_i` 没有逐步大小关系；两者的差是非负gap在相邻时点的增量，不是gap本身。

空主题、重复槽和同覆盖异标签均不破坏可行性：保留的是索引，标签在每个槽保持原样；0槽按 `F_0(Q)=|Q|`；目录非空且有限保证最大值存在，重复补槽保“恰k槽”定义；零客户时所有式子直接为零。`i=m`无需空标签，空的是0元组。式(1)–(3)不使用SPE，只要actual是合法行动序列；SPE只在动态付款/Γ≥0处使用。

若T并非最优，设 `g=OPT_m−|O|≥0`，准确关系变为

\[
\mathcal S_i\le L_i^T+g,\qquad
L_i^T-\mathcal S_i=F_{m-i}(C_i)-H_i(T)-g.
\tag{4}
\]

不能仍写 `𝒮_i≤L_i^T`；终点反而 `L_m^T−𝒮_m=−g`。例如m=1，目录含空标签和一客户标签，actual取后一标签、比较取空标签，则 `𝒮_1=0>L_1^T=−1`。RET原文“L_i可负”是任意比较元组合同，与最优比较、合法长度i actual下(3)不冲突。

## 2. 已登记完整SPE内严格 `L_i>𝒮_i` 的四客户例

复用已proved对象 `customer-attraction/fully-shared-actual-omission-constant-SPE-near-two-family` 的 `m=2,a=1` 实例。客户为x,y,z,q，目录

\[
A=\{x,y,z\},\quad B=\{x,q\},\quad D=\{y,q\}.
\]

原完整策略在全部历史恒选A。对每个合法T有 `|A\T|≥2|T\A|`，由已登记CONST全历史充要判据，该策略为完整纯SPE；也可直接比较：根改B/D后尾仍A，当前收益仍3/2；任意一层历史后末位A为最佳回复。actual AA，`u=(3/2,3/2)`，固定最优比较元组 `(A,B)` 覆盖4人。

第1步actual覆盖A，保留一槽时各半概率为A或B，因此

\[
H_1=(3+4)/2=7/2,\quad L_1=4-7/2=1/2,
\quad F_1(A)=4,\quad\mathcal S_1=0.
\]

严格gap在合法完整SPE内存在。可是本例 `P_1=3/2` 同时支付两者，**不分离**两个付款条件。

## 3. 已有负前缀族精确否定RET全前缀候选

已登记proved `CA-PREFIX-BALANCE-NO` 正文的全部历史解析证明已实读：客户构造、末位全部五类、非末位全部四类及唯一最优支持在同一页，不能把它误认成仅actual证书或浮点LP。

其任意n≥4实例，置 `x=n−2`，目录 `A,B,L_1,…,L_n`。每个普通叶j<n有x个仅L_j客户、1个A/L_j客户、x个B/L_j客户；特殊叶n有x个仅L_n客户、x个B/L_n客户、n−1个A/B/L_n客户。各组互不相同。叶主题两两不交，覆盖所有客户；每叶存在x>0个独占客户，故**唯一最优n槽支持是全部n叶**，任意最优元组仅重新排列这些叶。因而每个比较客户的重数 `d_z=1`，没有最优O选择逃逸。

完整策略：根A；非空历史且仍非末位时，若此前全B则A，否则B；末位取真实份额最佳回复，平局优先B,A,L_1,…,L_n。原正文§二–四穷尽并证明全部历史IC。actual为 `A B^(n−1)`，并有

\[
u_1=n-1/n,\quad W=n^2-2,\quad OPT_n=2n^2-2n-2,
\quad |A|=2(n-1),\quad F_{n-1}(A)=2(n-1)^2.
\]

所以

\[
\mathcal S_1=OPT_n-F_{n-1}(A)=2(n-2).
\]

最优O为全部客户；`d_z=1`使RET首步删除概率为1/n，且没有O外退款。因此

\[
L_1=|O\setminus A|/n
=[2n^2-2n-2-2(n-1)]/n=2(n-2)=\mathcal S_1.
\]

于是每个n≥4均有

\[
\boxed{L_1=\mathcal S_1=2(n-2)>n-1/n=P_1.}
\tag{5}
\]

n=4时为**22名单位客户、6个合法主题的完整SPE**：普通叶各(2,1,2)三组，特殊叶(2,2,3)三组；最优元组 `(L_1,L_2,L_3,L_4)`，O22人、A6人、每客d=1，`L_1=16/4=4>15/4=P_1`，亏1/4。原比较元组量词即使弱化为“存在一份最优元组”也失败，因为唯一最优支持仅可排列且RET不变。

本族 `2W−OPT_n=2(n−1)>0`；n4为6。因此它确实把**仅终点half**与两个**全前缀预算**分开。它不分离“全前缀𝒮≤P”与“全前缀L≤P”：本族首步两者相等。

更强的现成事实是，对本族i≥2，actual并集已经是A∪B，剩余未覆盖是n个互不交的叶私有块各x人。静态剩n−i槽最多也可恰覆盖n−i块，所以 `𝒮_i=i x`；RET同样 `L_i=(i/n)nx=i x`。这条核对仅用上述现有构造，没有搜索新输入。

## 4. 与SHARE/LEDGER/TOTAL及现有candidate的准确关系

在actual位置k任取一份真正最优余槽补全及一槽j，沿同一原σ的强制T_j枝，记

\[
K_k=L_{kj}-d^{out}_{kj}-|D_j\cap A_k|-e_k-\varepsilon_{kj}-\Gamma_{kj}.
\]

privateledger精确给 `K_k=δ_k−u_k`；故任意前缀（无需兼容耦合各强制枝的尾利润）都满足

\[
\sum_{k\le i}K_k=\mathcal S_i-P_i.
\tag{6}
\]

全部信用保留的**终点**(6)非正恰是Q-CAG-HALF；全部信用保留的**每个前缀**(6)非正恰是CA-PREFIX-BALANCE-NO所否定的旧不变量。选择哪个补全/槽都不改变左侧总和的数值，不能借选j消除(5)。

`M-8f6719ad729d4806b16e6288dff1806f` 的B?问是否能共同选每位补全/索引，使**终点** `Σ[L−dout−|D∩A|−e]≤0`，即删去ε、Γ后的更强付款；它推出half，但不等价half，也不要求每个前缀非正。负前缀族不反B?，RET全前缀失败也不反B?。现有accepted边 `private-block-common-payment-condition-to-half` 已完整承担此充分归约。

`M-dfcc6e32210c40c3b80ff0808d132d0b` 精确对应固定根最优池RET全前缀 `L_i≤P_i`，现应按(5)接入反驳。`M-9ae63ef5abd846b28c67b72f4df146cb` 是每个玩家对**终点**净差的另一候选 `OPT−W≤m u_i`，不是(6)的累计前缀式，不能合并或一并更改状态。静态 `M-229d7c0b44324c27b2755e659b46d235` ME/MM仅负责可行替槽、非负交换松弛；本地重置最优池的均匀单删给 `local L_1=δ+avg ε`，不把根固定池改成每位的新池，也不提供任何跨分支金额。

作为逻辑条件，有 `全前缀L≤P ⇒ 全前缀𝒮≤P ⇒ 终点half`。式(3)严格gap只证明数值不恒同；它不自动证明第一箭头在完整SPE类有严格模型分离。当前有界实读没有提供满足全前缀𝒮预算却违反全前缀L预算的实例，故不声称第一箭头严格；第二箭头由上述已登记真SPE族确实不可逆。

## 5. 已有canonical、owner与具体接续建议

已存在accepted边：

- `map/edges/customer-attraction-3a-3a-00c291811e5de4b9/retained-comparison-pool-controls-static-private-block-loss.json`，全文SHA **f787c849c072e77caad5bb0698969680518693e4495616c720fe8bd29c5ba4ed**，已经准确写“任一保留的m−t索引给F_(m−t)(C_t)的可行补全，取期望得OPT−F_(m−t)(C_t)≤L_t，末期等号”。其端点是RET引理→privateledger，`contribution`正确限制为静态一步。**本轮桥已付，不新建重复边。**
- 同包 `private-block-common-payment-condition-to-half.json` 已承载ALL(B?, privateledger)条件性全人数half归约。
- 同包 `negative-prefix-family-forces-first-credit-factor-two.json` 已承载CA-PREFIX到固定首步系数障碍，未命中M-dfcc。

更关键的旧覆盖原文，在 `map/receipts/customer-attraction-3a-3a-00c291811e5de4b9.json` 的RET coverage.reason，当前 `map/coverage.json` 也保留：

> 静态F最佳余槽给OPT−F_(m−t)(C_t)≤L_t，末端等号；因此本包负前缀族也使其随机池L_1>u_1。该比较保O外退款及重复索引，不产生实际付款；程序旧点中的F_r(b)是背景剩余利润，与总覆盖F_k(C)不同。

旧receipt与当前总覆盖的精确全SHA已冻入refs；当前coverage注明最近范围 `boss5-eta-status-round55-repair-6cda1bce3d48b546`。这说明数学否定已识别，漏的是候选身份、状态与精确关系。M-dfcc当前registry为v1/open，map coverage为needs-decision / No completed comparison batch，当前canonical无其端点边。

建议Root定向处理：以已有 `CA-PREFIX-BALANCE-NO` 为反例source、M-dfcc为精确被否目标，保留RET静态恒等式与Q一般问题真值；原RET正文“累计付款…开放”的状态与相关描述要做最小订正，再由正式定向流程接反驳，不为𝒮_i或gap新造节点。此报告不替Root登记或声称修复完成。

## 6. RET共享文件变更的精确影响清单

若Root改RET正文，当前全文件SHA `aeb776e8877dadb113c2039c34007a2a5509a77dfea8231a3ce485216eeeb218` 命中4个对象，须按既有版本/证据引用规则一起刷新，不能只改M-dfcc：

| 对象 | 当前版本/状态 | RET引用角色 | native object pin |
|---|---|---|---|
| optimal-comparison-pool-net-exchange-and-random-retention-identity | v2/proved | body全文 | 38e6d2a40b21871b26c4c206333f740613ae4b7cc07e2e5dcb73d202f08c0c84 |
| M-dfcc6e32210c40c3b80ff0808d132d0b | v1/open | body「累计付款是目标而非已证不变量」 | f6d1128771ba50b849e369729710721d290f204ae75aa3cc9d4c831bfc0514ef |
| M-140da849797c486ba0ad22e4dfbe2631 | v3/proved | evidence全文 | cb232d31fdf7245d80e8fd74a5c2d7822b3832eaf95eff3f7338e6c4e3d976ea |
| M-8a98d8d3ca9a42089dbad81715d6f020 | v2/proved | evidence全文 | 166f0c5bf0eac4a897e9345d798f7bc6aacbac04d3b009044d6d6a3af78861ee |

当前canonical直接引用RET字节的边共2条：上述retained-comparison桥，以及 `map/edges/customer-attraction-3a-3a-227c1bd1c11fc2c4/private-block-witness-violates-net-swap-step.json`。另外2条canonical边经受影响对象pin关联：同227包的 `root-tax-controller-restricts-to-square-credit-failure.json`、`root-tax-controller-restricts-to-private-floor.json`。四条的全文SHA、canonical edge pins、端点均在refs的 `current_canonical_edges_touching_shared_objects`。这是刷新绑定范围清单，不表示这些原有关系有数学错误。

当前CA-PREFIX native pin `4d500022638bb5dcc117edeace66f673af98737256c72c9ebf3217ac49949bb1`；其正文全SHA **b42e57e311686c2d737d6ade6642efaa05caa28dded02c9cf035ef0ed9c70072**。本次不改变该proved反例或其正文。
