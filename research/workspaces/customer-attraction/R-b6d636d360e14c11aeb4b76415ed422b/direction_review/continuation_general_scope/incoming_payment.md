# SOURCE-NET 与 capture-after-reset 的一般机制审查

2026-10-24。只读审查；未改仓库、未发公屏、未提交。对象严格为任意人数、任意有限共同目录、每个完整有序历史纯 SPE。Q-CAG-HALF 仍 **OPEN**。下文的有限重算只校公式和旧证书，未开展固定人数正面研究。

## 结论

**SOURCE-NET 是真实新增的一般组件，incoming 付款仍是实质缺口。** 新增之处是把所有角色的初始化 source 当次吸收，同时放入同一份实际 Hall-A 的取消量与净库存；它比单根容量、单叶总量或“每个 source 各能付一次”更强。它不使用 IC，也没有跨过重置后的互斥 query 合流。

把 `NET?` 写成 `K_i^in≤η_i−K_i^src` 本身是等价分拆，没有再新增不等式；但 `NET?` 是一类具体付款证书的充分可行性要求，**没有被证明等价于 half**，且其正 IC 税可能使它强于福利目标。不能因尚未闭合而将 SOURCE-NET 判作无价值，也不能因 source 已付就推断 incoming 仅剩记账。

建议继续一次有明确产出的“一般 incoming／总费用桥”研究：必须接入原真实查询叶内部捕获者的完整 IC，证明一个此前没有的跨历史关系。停止扩展已经闭合的 SOURCE-NET、静态 Hall 网络、积分／势重表达以及无区分力的有限阴性积累。自由查询 Bellman 是值得接入的更宽接口，不能替代它尚未证明的价格预算。

## 一、核对位置与量词

仓库根为 `仓库根`。以下路径均相对该根，行号为本次读取版本。

| 位置 | 精确用途与判断 |
|---|---|
| `research/current/customer_attraction/model.md:8–32` | 有限共同目录；任意完整历史 IC；相同计数历史允许不同续局。整个审查保留这些量词。 |
| `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/GENERAL_PROOF_WORKING.md:176–193` | 实际 Hall-A 钱包、SOURCE-NET 与 incoming 末端义务的总接口；其 OPEN 标级准确。 |
| `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/credible/owner_hybrid_transport.md:22–70` | 全部角色子集 HYB 与 Hall-A；下面独立重构其割证明。 |
| 同文件 `:119–180` | 实际 γ/f、同时局部取消、η、SOURCE-NET 的完整推导。 |
| 同文件 `:194–204` | 任意合法叶只享静态容量；购买原 IC 还须核真实历史；这项限制不可省略。 |
| `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/credible/increasing_role_capture_flow.md:15–59` | 实际前缀查询、重置、守恒及唯一 whole-IC 标量；重置不是继续旧叶。 |
| 同文件 `:87–99` | 正 IC slack 是付款税；总费用可能强于福利目标，作者已准确保留此点。 |
| `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/mixed/capture_hitting_capacity.md:13–35,53–83` | 单行到达 ≤ρ/2；多行只控制曾命中概率；不控制多行动之和，也未付 NET。 |
| `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/shared/review_owner_hybrid_transport.md:73–89` | 已有对稿核对覆盖 SOURCE-NET；本审查另从定义重构，不称盲审。 |
| `research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad/GENERAL_WORKING.md:7–19,29–35` | Mpath／pair／安全值等候选仍须共同真实 IC 付款；没有可直接拿来付 incoming 的已证跨孩子预算。 |
| `research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/transport/free_start_capture_prices.md:22–75,77–98` | 自由客户路由仍合为同 query 单一 IC 系数；Bellman 及自由起点可重构，KAPPA? 未付。 |

## 二、可独立重构的已证数学

固定最优合法 m 槽元组 T，O 为其覆盖，选分析分割 `O=⊔Q_i`、`Q_i⊆T_i`。实际叶 S 的覆盖分成 I=C∩O、G=C\O、R=O\C。记 g_i=u_i(G)。Q_i 不是目录行动，不能当玩家偏离。

对任意合法叶 B 和角色集合 J，只把 J 槽换成 B，其余放 Q，然后将未换 Q 扩回合法 T。最优性给

\[
\left|\bigcup_{i\in J}(B_i\setminus O)\right|
\le |\{x\in O:o(x)\in J,\ C_x(B)\cap J=\varnothing\}|. \tag{HYB}
\]

在角色图上给每个已覆盖 O 客户 x 建 `owner(x)→每个覆盖者`、容量 1/c_x；每个遗漏 O 客户建 owner→终点、容量 1。J 的 O 外源利润不超过 HYB 左端；HYB 右端每客户提供一单位出割容量。故全部源可同时饱和。对 B=S，终点正好为 R，得到一份 γ、I 边流 f：

\[
0\le\gamma_x\le1,\quad \sum_R\gamma_x=|G|,\qquad
\gamma_i+\operatorname{out}_f(i)-\operatorname{in}_f(i)=g_i,
\quad\operatorname{in}_f(i)\le u_i(I).
\]

这不是只由总量 `G≤R` 任意删除 G 个客户，而是带 I 份额容量的定位。若先指定 `0≤δ_x≤1` 且每 owner `δ_i≤g_i`，直接预送 δ 后，每个角色割的源与终点容量同减 δ(J)，故残余仍可饱和。于是可以 **同时** 取 `δ_i=min(g_i,|Q_i∩R|)`，并扩为一份完整 γ；无需每个角色重领 G。

定义同一净库存

\[
\rho_x=1-\gamma_x,\quad \sum_R\rho_x=\operatorname{OPT}-W,
\qquad \eta_i=u_i(I)+\gamma_i,
\quad\sum_i\eta_i=W. \tag{1}
\]

在角色 i 唯一 source 查询 T_i 上，初始吸收为

\[
A_i^{src}=\sum_{x\in Q_i\cap R}\frac{\rho_x}{c_x(Z_i(T_i))}\le D_i(T_i),
\qquad K_i^{src}=u_iA_i^{src}/D_i(T_i)\le u_i. \tag{2}
\]

零分母意味着无正吸收，费用取零。若 `g_i≤|Q_i∩R|`，局部预取消保证 γ_i≥g_i，故 η_i≥u_i；反之本 owner 的 R 全取消，K_i^src=0。由此所有角色 **同时** 满足

\[
K_i^{src}\le\eta_i,\qquad \eta_i-K_i^{src}\ge0. \tag{SOURCE-NET}
\]

这是真正新增的共享预算兼容关系；不是先用每个 u_i 付款，再额外加一笔 η_i。证明甚至不要求 σ 是 SPE，所以它不能单独蕴含 half。根无 incoming，因而根整行已付；其他角色没有相同推论。

## 三、incoming 为什么仍未付

每个查询 s=(i,a) 的总吸收 A_s，只购买一条完整真实收益比较，唯一系数为 `w_s=A_s/D_s`。source 与 incoming 的分拆是同一固定分母下的线性分拆：

\[
w_s=(A_s^{src}+A_s^{in})/D_s,
\qquad K_i=K_i^{src}+K_i^{in}=u_i\sum_a w_{i,a}.
\]

重置后读取的是原实际前缀 h_j 下的 Z_j(b)，不是旧查询叶中捕获者所在历史的续局。两者前缀不同，不能让旧叶收益自行成为新行收入。完整 SPE 给每个历史自身的 IC，未给跨历史比较；需利用旧真实叶内部捕获者的 IC 建立新的桥，而非删除祖先调用较小游戏 SPE。

HIT 只给每个非owner客户进入某一行的总量 ≤ρ_x/2。由此能界单个 query 权，不会把很多不同 query 的 `Σ_a A/D` 压到剩余 η。COV 把正形式边际债局限到低权节点，也没有将各节点互斥叶上的 I error 压成一次实际 I。锚定 Hall 图消除已锚角色，是同叶支持和合法 IC 适用域的推进；不同锚叶之间的余额仍会变。

因此必须禁止三种重复：A/B 两图相同客户容量相加；同一实际 I 一边路由 G 一边再次全额购买 query；先付 source 再给 incoming 一份完整 u_i。原稿对这些限制的表述准确。

## 四、最弱剩余接口及“等价重述”的准确边界

保留当前 source／Hall-A／η 接口时，逐角色 NET? 的剩余项恰为

\[
K_i^{in}\le\eta_i-K_i^{src}\quad(\forall i). \tag{3}
\]

式(3)只是 NET? 的等价分拆。更弱、足够闭合福利的接口为

\[
\sum_iK_i^{in}\le W-\sum_iK_i^{src}. \tag{4}
\]

任何同一合法全吸收流都有 `ΣA=δ:=OPT−W`。SPE 下令

\[
E_\rho=\sum_s\frac{A_s}{D_s}(u_{i(s)}-D_s)\ge0.
\]

精确地 `ΣK=δ+E_ρ`，所以(4)等价于 `E_ρ≤2W−OPT`。这解释了为何付款桥可能更强于 half：half 只要求右端非负，没有控制某个受限捕获规则产生的正 IC 税。仅把 incoming 改名为税、重置债或 LP 没有新增关系；但显式收费桥不是已证明与原目标互相等价的重述。

**可进一步放宽而不违反 whole-IC 的接口。** 自由查询稿允许每个客户在捕获角色任选含它的合法新 query，仍按最后 A 聚合为同 query 一个 w。对固定原实际菜单，独立逆归纳得到

\[
V_i(x)=\min_{a\ni x}\frac{u_i/D_i(a)+\sum_{j\in F_{i,a}(x)}V_j(x)}{1+|F_{i,a}(x)|},
\qquad\kappa_x=\min_i V_i(x)\ge1. \tag{5}
\]

不同客户的最优选择相加不会使 IC 逐客户重权；聚合后付款仍恰为 Σ_su_iA_s/D_s。只求总钱包时可以不保留旧 η/f 合同，直接选择净质量 `0≤q_x≤1, Σq=δ`。该更宽类的最小总费为

\[
\min_{0\le q\le1,\,\sum_Rq=\operatorname{OPT}-W}\sum_Rq_x\kappa_x. \tag{6}
\]

故“某个最优 O 使(6)≤W”是当前明确、较弱的充分价格桥。它是先算真实菜单价格再比较预算的非循环候选；尚未得到普遍价格上界。无需强求它兼容旧 SOURCE-NET γ/f；一旦改用该总钱包，应完整弃去旧逐行钱包的额外限制，不能再加一笔旧 G 或 I 信用。

## 五、可诊断的下一任务；此段是独立推导级，非新支付定理

固定 owner/matching、原菜单和旧捕获规则，令 v_i(x) 是单位 source x 最终在角色 i 支付的费用。这些是非负确定数，且 `K_i(ρ)=Σ_xρ_xv_i(x)`。令 Γ_δ 是同一 Hall-A 可行 γ 且满足已经选定局部预取消的集合。Γ_δ 非空、紧、凸。逐行 NET 可行当且仅当对每个非负 λ：

\[
\sum_i\lambda_i\left(\sum_xv_i(x)-u_i(I)\right)
\le\max_{\gamma\in\Gamma_\delta}
\sum_x\gamma_x\left(\sum_i\lambda_iv_i(x)+\lambda_{o(x)}\right). \tag{7}
\]

证明是把 `Σ_xγ_x[v_i(x)+1_{o(x)=i}]≥Σ_xv_i(x)−u_i(I)` 的共同可行性，应用紧凸集加向下正交锥的分离；非负 λ 恰为所有可能的不足方向。该诊断只重写已知可行性，不算主线进展。若仅要总费用(4)，直接取总费价格 v(x)=Σ_iv_i(x)，只需证明可行取消能节约 `Σ_xv(x)−W`，无须逐行全部 λ。

**继续的具体任务：** 优先选择(4)或更宽的(6)，证明一条来自查询叶内部捕获者真实 IC 的新不等式，将对应重置税一次支付。若坚持逐行路线，必须证明(7)全部 λ 的右端由同一 γ 共同达到；逐 λ 另选 γ 可以用于支持函数判据，但最终需由凸分离推出一份共同 γ，不能把各 λ 的最优 γ 当多份实际信用。应交付该新解析不等式、其 IC 支持历史、每项容量只用一次的对应，或交付真正否定当前充分系统的完整历史分离。全程对象保持一般。

**停止的具体任务：** 不再证明 SOURCE-NET 的另一个名称；不再单独扩 Hall-A/B、HIT 或 Exp 表示而没有跨叶关系；不将更多 fixed 样本 PASS 算作 incoming 正面证据；不以某一 fixed matching/γ 失败否定所有共同选择，更不否定 half。自由 κ 的定义和 Bellman 已有可重构证明，下一份新工作应是预算桥，而不是第二个同义最短路／LP。

## 六、独立有限回归

`incoming_payment_regression.py` 不导入作者实现或 solver，直接读取旧 `portfolio_matching_failure` 实例与完整证书，重构全部历史、终局收益、实际 Hall-A 残余最大流、局部 δ、捕获 source/incoming、固定价格与自由 Bellman。输出在同目录 `incoming_payment_regression.json`。

结果 PASS：核全历史 IC 30 项；原实际路径(E,A)，T=(B,D)，W=44、OPT=45、R=42、I=3、G=41。未取消流的 source 费用为 `(385/19,22)`、incoming 为 `(0,5/2)`，总费 `1701/38=42+105/38`，准确保留正 IC 税与 row overload。按同一实际网络先局部取消后，γ=(20,21)、η=(22,22)，剩余净源一单位，source 费(0,1)、incoming 为零，总费1；该例此时无未付 incoming，所以不能拿它替一般 incoming 做背书。固定单位源价格为 `1,41/38,22/19`；自由 κ 全为1，84项逐客户／起点的完整确定 query policy 穷举与 Bellman 相符。这里的枚举只回归已有一般公式，不新增特殊正面结果。
