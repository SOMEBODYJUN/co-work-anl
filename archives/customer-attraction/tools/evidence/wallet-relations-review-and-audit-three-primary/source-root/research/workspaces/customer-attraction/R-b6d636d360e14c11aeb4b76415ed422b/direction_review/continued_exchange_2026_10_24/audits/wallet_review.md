# AMOUNT、动态门槛与坐标双预算：一般方向续审

2026-10-24。Boss3 内部审查。读取原 clone 的相关数学正文，并在恢复后的 Boss3 clone 写入本页；不改共享正文、不发外部消息、不提交。根 AGENTS、四入口、CAG 模型与精确目标已读。全部判断针对任意有限共同目录、任意人数、每份完整有序历史纯 SPE；本页没有五人专项、新 half 定理或真正目标反例。

## 一、结论和最值得继续追问的缺口

末层多孩子 TERMINAL-CAP2 正确，且系数二在所给 AMOUNT 合同中不能统一减小。它新增的是**多个互斥末位孩子对同一接收角色的局部列容量**，不是新增同一父叶的总资金。AMOUNT 一旦成立，旧 POSITIVE 本来已把全部 retained 加全部正价共同限制在 sender 的同一份实际利润和中。深层 DEEP-CAP2 尚未证明、未见所读资产给出完整 SPE 反例；即使成立，也不能替代覆盖债务进入 AMOUNT 及扣除既有支出的证明。

round7 坐标初始化真正保留了以前未同时保留的两项信息：每个比较客户恰一单位的库存，以及 actual-current / actual-正价 / 真实 future 子边的同一张非负分割。current≤u、同父正价列 H≤u 同时成立。它尚未付款的是 future 的共同余额。I 互补付款又确实清掉了同一初始化中全部 I-future，且与原 H 完全兼容；不是第三份 W。round8 的更强逐边剪枝保留同样的 d、H、b 并补上初始化密度合同，适合接客户保留核，但不能控制同一角色多个历史的完整 IC 累计。

动态 L/Theta 的真实定义和 u_i≥Theta_i 正确。SM/TB 是另一条未证一般充分桥；它们不因静态匹配、UV 或遗漏数匹配失败而失效。不能把 Theta、归属席位谱中的大写 Θ、安全值 v_r、末两人 theta 当成同一个对象。

这三组最新自述均准确保留 OPEN，均没有给新的无条件一般福利界。需要下一条真正跨历史的支付关系，而非再证明一个单 context 的退款、源库存守恒或逐客户密度≤1。

## 二、末层 cap2 的独立重构与它没有购买的资金

令 B 为固定父叶，W^α=(B_<m,T_α)。对每个 sender j<m，AMOUNT 为

\[
\sum_\alpha\lambda_{\alpha j}p_j(W^\alpha)\le p_j(B).
\]

若 p_j(B)>0，末位一次替换给 c_α(x)≤c_B(x)+1≤2c_B(x)，故 p_j(W^α)≥p_j(B)/2，进而 Σ_αλ_αj≤2。固定 x∈B_m，令 c=c_B(x)。c=1 时没有 sender；c≥2 时有 c−1 个 sender，正价出现的孩子必移走末位对 x 的覆盖，故 c_α(x)=c−1。因此该客户合计正价≤2(c−1)/[c(c−1)]=2/c。零利润 sender 的主题无客户，相关 q 全零；不以除零限制其 λ。m=1 是空和。这一证明完全不需要 SPE。

新关系确实跨越了同一 cut 的多个不同孩子。旧同孩子 prefix 合同则是 λ_j≤L 时，全部输出角色系数≤L。两个输入合同不同，不能把旧合同自动改写成 AMOUNT。

**全人数校准。** 对目录 {A,∅}，|A|=n>0，全部历史恒选 A 是完整 SPE。B=A^m，末位强制空集后 W=(A^(m−1),∅)。则

\[
p_j(B)=n/m,\quad p_j(W)=n/(m-1),\quad q_{jm}=n/[m(m-1)].
\]

旧同孩子回推取 λ_j=1，retained 系数为1，末位收到 n/m；全部 B 角色系数恰为1，精确支付 prefix 总额 n。AMOUNT 却连该单个孩子都不满足：每个 sender 输入超出自己的利润 m/(m−1) 倍。旧回推合法使用了末位的钱包，不能又说每个 sender 已独自以自己的原位利润付完。

另一方面，对任意深度、prefix 相同的合法叶，令 R_α(x) 为 suffix 中原覆盖者离开 x 的个数。旧 POSITIVE 可写为

\[
\sum_{l\ge i_\alpha}q_{\alpha jl}+e_{\alpha j}=p_j(W^\alpha),\qquad
e_{\alpha j}=\sum_{x\in B_j}\frac{c_B(x)-R_\alpha(x)}{c_B(x)c_\alpha(x)}\ge0.
\]

所以在 AMOUNT 下，**全部孩子、全部 recipients 的 retained 与正价总额**已经≤Σ_(j<m)p_j(B)。甚至由 R/c≤r/(r+1) 得正价总额≤Σ_(j<m)[(m−j)/(m−j+1)]p_j(B)。TERMINAL-CAP2 或 DEEP-CAP2 的可能价值是将这些金额定位到可购买后续整行 IC 的角色容量；不能把这份总额再作为另一笔新资金加到 direct/suffix 预算上。

所读全 n 完整 SPE 锐族给末列系数 (2n−1)/(n+1)=2−3/(n+1)，W=OPT=2n²。该族正确区分了跨不同孩子的金额归一与固定一个孩子的系数≤1；只判断 AMOUNT 正价合同的锐性，不判断 half。

## 三、深层 cap2 真正要新增什么

DEEP-CAP2 的精确对象是同一原完整 σ 的实际 B，W^α=finish_σ(B_<iα,T_α)，同一 cut 允许多主题；不能用任意合法续局代替真实规定续局。给定 B、σ、目标列 l 后，AMOUNT 的最坏列额恰为

\[
M_l=\sum_{j<l}p_j(B)
\max_{\alpha:j<i_\alpha\le l}
\frac{q_{\alpha jl}}{p_j(W^\alpha)}.
\]

无分支取0，零利润分支的 q 也零。不同 j 的预算独立，这个闭式是精确的固定输入优化。尚缺的一般新不等式正是 M_l≤2p_l(B)，它必须利用不同强制位置后真实后继 IC 的某个联合关系。

末层的两个关键事实“负载最多增一”“移走即 c_α=c_B−1”在深层均不存在。纯代数仍有 q_αjl≤p_j(W^α)/2，所以 M_l≤(1/2)Σ_(j<l)p_j(B)；但一般输入没有已证的 Σ_(j<l)p_j(B)≤4p_l(B)。全源金额已小于 W 也不推出低利润接收角色的 cap2。

即使 M_l≤2p_l(B) 得证，还应明确它接在一般证明的哪一步：原覆盖需求如何变成这些 λ；同一 sender 已花掉的 direct/suffix 费用如何预扣；不同父叶回推如何共同折回根 actual，而非各父叶各领取 W(parent)。当前文件已准确承认这些缺口。继续作旧锥的阴性检验不会增加该信息。

## 四、坐标初始化、I 补余和更新的密度输入

round7 对 x∈T_i 给 p_ix=1/c_T(x)，静态正价 P^B_ix≤p_ix；r_ix=p_ix−P^B_ix。原真实 future 正价 q_ix 满足 (r_ix−q_ix)_+≤1/c_(W_i)(x)。**先逐坐标代数再求和，最后只用一次完整原 IC**，才有 Σ_x(r_ix−q_ix)_+≤u_i。取 b_i=(Σr_ix−u_i)_+ 并在 min(r_ix,q_ix) 子容量中分配 a_ix，可令

\[
p_{ix}=P^B_{ix}+c_{ix}+a_{ix},\quad
d_i=\sum_xc_{ix}\le u_i,\quad H_l\le u_l,\quad
|O|=\sum_l(d_l+H_l)+\sum_i b_i.
\]

这是一般有效的初始化。c_ix 的 x 是来源标签，actual B_i 未必覆盖 x，因此 d_i 是完整利润钱包支付，不能伪称同客户券。原 full-profit SAFE/CLIP 保持质量却重采客户；其输出 A_l^out≤2u_l−d_l−H_l 仍未证。ΣA^out=Σb 是债务守恒，不是剩余资金。

令 I=O∩C，w_lx=1_(x∈B_l)/c_B(x)，H_x=Σ_lH_lx，A_x=Σ_ia_ix。原同一库存给 A_x≤1−H_x，故

\[
J_{lx}=\frac{A_x}{1-H_x}(w_{lx}-H_{lx})
\]

在分母正时精确支付 I-future；H_x=1 时 A_x=0，取 J=0。于是 H_l+J_l≤u_l(B;I)，这项付款确实使用第二份 I 钱包的余量，不重领 H。它允许落到 owner 之前的 actual 角色，不调用该角色 IC；故它扩大直接出口，不能说原受限 full-SAFE 路由已经实现 RESIDUAL-CAP。

仅 R=O\C 入口从头接 fresh 分母 ν 后，新的净券 K 满足 ΣK=原 R-future 总量；逐 context 的 ν−P=u_role−Y−N−e>0 允许安全退款。真正未付仍是同一次选择下

\[
K_l\le2u_l-d_l-H_l-J_l\quad\text{全部 }l.
\]

fresh 分母必须重算 β；不可沿用旧完整利润流费用。提前整付全部 I、仅 R 初始化的极大 current 数值也已能由旧 source INIT+标量 CLIP 得到，作者自己已去重；不能再认领一条新一般预算。

**round8 加强输入的实际增量。** 新 cap 为每条初始化 future 边

\[
\widehat q_{ijx}=\min(p_{ix},1/d_{ix})/c_{W_i}(x),
\]

仍支持同样的 d、H、b，并给 c_W a_ijx≤p_ix。原 raw round7 不保证这个更强密度。审查独立重构其关键代数：写 t=c_T、d=d_ix、w=c_W，n 为 future 新增覆盖人数，k=d−n_B，则 1≤k≤min(d,t)，r=k/(td)，\hat q=n min(d,t)/(tdw)，且

\[
kw-n\min(d,t)=kd-k n_-+n[k-\min(d,t)]\le kd\le td.
\]

因此 (r−\hat q)_+≤1/w，原一次 whole-IC 仍可付款；这不是逐客户 IC。

所读 round8 inventory 文件目前58行，正文只写完此初始化证明；开头对“全图密度≤1”称新增候选组件，未在该文件展开全图证明。本审查可按已有 RESET-DENSITY 论证独立补出该推论，**不补出钱包**：在客户保留核中，每条 future x 边发送 h_t(x)/c_reset(x)。对同一个非实际 receiver s，其首偏离位置 k 唯一；全部 natural parents 都在角色 k、reset 为同一 B_s，直接 source 也只能是 k。角色严格递增且逐客户流不复制，故

\[
h_s(x)\le\frac{p_{kx}+\sum_{t:\operatorname{role}(t)=k}h_t(x)}{c_{B_s}(x)}
\le\frac{\sum_{q\le k}p_{qx}}{c_{B_s}(x)}\le1/c_{B_s}(x).
\]

此处 p_qx 不存在时取0，Σ_qp_qx=1；past 出口只使在途质量减少。证明对全 O 标签的非实际 receiver 同样成立，不要求 x fresh；但必须用新 INIT-DENSITY 与客户不重采核，不能混入旧标量重采流。它给每个 context 的 β_*≤1。不同历史的最大值可能由不同客户实现，因此没有 Σ_(t:role=l)β_*t≤1，也没有其退款后实际费用共同界。

## 五、Theta/SM：保留一般候选，区分三个量词

动态对象是 L_i(A)=min_(y∈R(h_i,A))u_i(y)，Theta_i=max_A L_i(A)。原 σ 对每个 A 的真实续局都属于 R(h_i,A)，所以 u_i(actual)≥d_i^σ(A)≥L_i(A)，再取 max 得 u_i≥Theta_i。不是仅比较在轨动作的最低值。

TB 为 OPT≤W+ΣTheta；SM 为 Σ_iL_i(T_i)≥|∪T_i|−W。需要明确采用 SM-all、SM-opt-all 或 SM-opt-exists；最后一种最弱，仍充分 half。TB 甚至可在 SM-opt-exists 失败时成立，因为每行 Theta 可选不同于比较元组的动作。上述式子的证明目前均未提供。

所有真正离轨孩子的最低值可同时拼入一份保持原实际叶的完整 SPE；所以“不同离轨极小叶不能同时实现”不是剩余障碍。只有在轨列最低值一般不能保留原叶。改用 barL_i(S_i)=u_i，其他列 L_i，可去掉该额外在轨租金；其全实例预算等价于原策略真实偏离收益预算 SD。这是量词澄清，仍没有跨枝付款。

原 prefix 产品证明中的鲁棒下界 max_AΣ_(x∈A)1/(b_i+r) 也可作为 Theta_i 的下界；只重用这个粗下界不会凭名称变出 TB。真正增量必须使用“后继是完整子 SPE”比任意尾部更强的信息。归属动作谱的 Θ_i 又是另一种已证地板，W≥ΣΘ_i 不能与这里的动态 Theta 重复相加，也没有一般的 ΣΘ_i≥OPT/2。

所读旧反例中，静态最优匹配 W47/OPT52/minK48 已否定强 FOMA，不能继续列 OPEN；却没有否定 SM 的 RHS=OPT−W=5。UV 的 all-big 族则对 SM/TB 留余量1。因此应保护精确尚未被击中的候选，停止已败强桥，不扩大方法禁令。

## 六、同一推导代入五人：无条件到哪里

| 已读机制/证据层 | 五人准确结果 | 状态 |
| --- | --- | --- |
| 已证一般 prefix 产品，仅用 τ≤m | W/OPT≥6049/15625；OPT/W≤15625/6049≈2.5830715821 | 无条件一般推导的代入；本轮无改进 |
| 一般末四人提升 | OPT_5/W≤937/375≈2.4986666667 | 无条件旧一般组件；未到二 |
| 本轮 AMOUNT 末层/深层工具 | 末层 cap2 正确；前三位置的真实后继和覆盖输入未付 | 没有新的五人无条件福利常数；DEEP 即使成立亦非单独充分 |
| 坐标/I 补余/fresh/密度 | 已付 d、H+J；K 的共同余量未付 | 无新五人福利界；若 FRESH-RESIDUAL 成立则 five half 只是条件后果 |
| Theta/TB、SM-opt-exists | 各自若成立即给 five half | 预算未证，不能算通过压力测试 |
| PAIR-ONE 及现有两两分块 | 即使其一般候选成立，五人仅给 OPT/W≤3 | 仍为条件值；不是已证无条件界 |

作为全仓证据层补充，共享登记五人界为约2.0616947857207375；旧个人区557行独立全域对偶审查已支持约2.042155490337931的一般目录五人上界（其“松弛精确最优”另需 primal 审查，不影响已证对偶上界）。728行约2.04207898656仍缺父分支独立全域对偶接受。三者均>2，不把模板点叫 SPE，也不由此重启五人调行。

## 七、建议交给作者的三个精确一般义务

1. **覆盖到 AMOUNT 的输入义务。** 给出某个最优 T 及完整非负分解，使需付的 OPT 或净缺口 OPT−W 真正进入原完整利润 claim；每个 sender 的 Σαλ_αjp_j(W^α) 受其**扣除 direct/suffix 等既有支出后的同一余额**控制。应明确覆盖恒等式和剩余项；缩小 λ 只会缩小已付需求，不能让剩余消失。需要跨父叶也不重开利润钱包的统一规则。
2. **同角色跨历史的退款后合账。** 若沿客户保留核，逐 context 已有 L_t=β_*t u_role−F_t≥0。应证明初始化与全部 past 出口也计入后，同一角色的 ΣL_t+past_l≤2u_l−d_l−H_l−J_l，或给一个足够闭合总覆盖的更弱真实关系。仅 β_*t≤1、单源 HIT、逐客户库存≤1 和 finite DAG 均不够；应寻找不同 histories 最大密度之间可共同退款的新关系。任何选择存在式的反例也须覆盖全部允许最优 T/剪枝/路由，不能以一个固定坏路由否定它。
3. **动态门槛的净缺口义务。** 如走 SM，采用明确的 SM-opt-exists：max_(T最优有序)Σ_iL_i(T_i)≥OPT−W；或直接证明 TB。需要把完整后继 IC 串成同一实例的真实支付，不能只重写 R(h) 或 F(h,remaining T) 的精确递推。静态匹配、遗漏数预算、在轨租金与原净缺口须分开。该路线可完全绕开 AMOUNT，不应被要求先完成其所有接口。

这些是可并列探索的数学义务，不是开工白名单或需先通过五人再准研究。若下一轮仍只产出守恒、局部核或密度不变量，应和作者据实商量是否能引入新的真实后继 IC，或换一般机制；不能把不断重命名余额当进展，也不能因暂未闭合判目标不可能。

## 八、独立 Python 校准与边界（本轮实际运行）

未导入作者 solver、核实现或缓存结果；首轮直接以内联 Python 和 Fraction 从集合/负载定义计算。按父方接续要求，现将同一参数域的实际校验固化为 [audit_wallet_relations.py](audit_wallet_relations.py)，实际重跑回执为 [audit_wallet_relations.json](audit_wallet_relations.json)，全部通过；没有扩大范围。它们只核以下精确代数和已给全参数公式，不承担 SPE 或一般福利证明。

- 产品递推独立得到紧利润 (1/25,6/125,38/625,266/3125,2394/15625)，和6049/15625；与乘积公式一致。
- {A,∅} 校准在 m=2,5,17 重算，旧输出全部系数1，AMOUNT 超额因子分别2、5/4、17/16；m=1 无 sender 边界通过。全 m 完整 SPE 依据是正文的解析证明。
- 对 m=1..6 的单个标记客户，B 为全部2^m个 actual membership 向量，T 为全部非零比较 membership 向量；对每个 T_i=1 的位置 i，保留 B_<i、在 i 强制 membership=1，枚举 i 后所有二进制尾部。一个坐标项是 (m,B,T,i,tail) 五元组；按 m 的项数分别2、24、224、1920、15872、129024，总计147,066。核 r≥0、原始/强化 future 正部≤1/w；同域另有30,306个 H 角色列核 H_lx≤1/c_B。它不枚举多客户实例或完整策略。
- 固定3个标记单位客户{0,1,2}、共同目录为全部8个子集，对 m=1..4 枚举全部有序 B∈目录^m：叶数分别8、64、512、4096，总计4,680。每个 B 同时允许末位8个 replacement；不是把每个 replacement 再算作一个叶。对每个 sender 取精确 q/p(W) 最大值后求和，核最坏列≤2p_m；包含无实际客户支持、空主题、重复覆盖及零利润 sender。没有要求 B 或孩子为 SPE；这是针对已证明末层代数引理的定义实现校准，不是小规模 SPE 正面结果。
- 锐族 n=3,4,10,1000 由块大小直接重算，列比率5/4、7/5、19/11、1999/1001，距二分别3/4、3/5、3/11、3/1001；AMOUNT 恰满。未把这些数值当全 n 证明。
- I 补余在 b=1..7、H_x∈{0,1/4,1/2,3/4,1}、A_x 取其允许区间四等分端点，核 ΣJ=A 和 H+J≤w；H_x=1 时 A=0、J=0，无除零。

## 主要读取来源

以下均为 repository-relative 路径，状态以本页所读正文为准：

- `R-5a15745a45ba44adb7d26c0557faacb7/{GENERAL_PROOF_WORKING.md,CLAIMS.md,parent/terminal_amount_cap.md,harmonic/positive_source_pool.md,coupling/{amount_cap1_family,deep_amount_handoff}.md,menu/deep_amount_bound_check.md}`。
- `R-cd789330fc7141299ac491bbb3ffa420/round7/{GENERAL_PROOF_WORKING.md,parent/optimal_coordinate_initialization.md,credible/joint_prefix_claim_pushback.md}`；`round8/{GENERAL_PROOF_WORKING.md,inventory/source_preserving_density_envelope.md}`；`round5/menu/li/README.md`。
- `R-d3981c0168644971803a9c3380ed687c/next_general/{MAIN_PROOF_WORKING.md,CLAIMS.md,peer_update_reconciliation.md,global_credit/coordinate_residual_attack.md,credible/{coordinate_support_attack.md,clock_cycle/source_preserving_kernel_review.md}}`。
- `R-65d0f88edf3849b39ca5eb79760e970b/global_credit_next/customer_density_reset_invariant.md`（密度论证来源和 raw round7 输入范围纠正）；`R-f399f831353446a49502f49d8abd2cb7/threshold_budget/README.md`（动态门槛原候选）。
- `R-b6d636d360e14c11aeb4b76415ed422b/direction_review/{five_player_pressure_test.md,continuation_general_scope/{threshold_candidate,uv_chain_obstruction}.md}`；`R-c4732bee2f7b4e50a70568170e3334ae/{round4_independent/full_pricing_review.md,round5_parent/README.md}`。
- 共享 `research/current/customer_attraction/{fractional_cover_path_budget,five_player_indexed_bound,tail_profit_lift}.md`。上列 R-* 路径均位于 `research/workspaces/customer-attraction/` 下。
