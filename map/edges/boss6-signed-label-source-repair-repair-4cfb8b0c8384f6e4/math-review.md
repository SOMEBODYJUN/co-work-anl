# Boss6：signed字典包的来源修复与保留审读

任务：`boss6-signed-label-source-repair-repair-4cfb8b0c8384f6e4`。替代Boss1已done的`customer-attraction-3a-3a-b3aa35f6dc170e18`，核心26、共享10。此次完整实读36个当前登记记录、原任务定义及原收据、全部17个旧边JSON；完整实读下列当前正文：共同标签模型、signed主定理、新标签元组审查、二值/signed反馈资源、价格上下域定理、HALF5主定理；随后完整补读改版P7资源855a97…和P7 v2登记。旧包其它正文与大证书不假称本次逐页重读；其成熟结果按相同端点、相同数学合同、相同有效证据字节继承。具体文件与84个引用跨度的处理见reading-ledger。

初读时仅两条旧边命中signed源或两个改版端点；随后发现共享P7证据来源变化，经Boss1发布来源/登记与任务刷新、Root核实后通知，另两条P7边也需替换。最终四条保稳定edge_id替换，其中两条signed重构实施、两条仅更新P7版本并保同一数学；其余13条原path/SHA原样retained。没有删除、重写旧边、旧原始审查、历史证明或旧收据。没有数学程序、LP、策略枚举、扫描或HALF5证书回放。字节散列、JSON读取与引用比较不是数学计算证明。

## 修复改变的实施条件

当前模型的行动是有限非空标签集A，覆盖cov:A→2^N允许非单射。假设a≠a′且cov(a)=cov(a′)，则只改该坐标标签的两个Cartesian元组可能覆盖完全相同。客户块不交只能把覆盖集合投影到客户块，不能唯一反演原标签。原文的唯一反演句因此错误。修复保留完整元组标签，而非对相同覆盖取商：

\[
A_* =\prod_c A_c,\qquad \operatorname{cov}_*((a_c)_c)=\bigsqcup_c\operatorname{cov}_c(a_c).
\]

有限性与非空性保持，每人仍在同一个共同目录中选一次标签，人数m不变。历史保存实际元组，所以逐坐标有序标签历史直接可读，原别名、空标签、重复、零客户和平局全部保留。旧无别名集合目录是仍有效子域。此次没有改变M-04595…的支持函数/限定字典最小值或signed修复的陈述、域、量词；版本与source改变用于使实施证明符合已声明标签域。

## 固定字典原始—对偶及精确成本

对m≥2的末位BR目标，记i<m的正常收益u_i，正常前缀强制每个标签T后真正完整子SPE的最低强制者收益为ell_i(T)，M_i=max_T ell_i(T)，g_i=M_i−u_i；max包含own标签。由于有限树、有限标签与有理份额，可选达到的真完整子策略。P=Σg_+、N=Σ(−g)_+、p=max g_+、n=max(−g)_+，空部取0。

字典组件H_I有g=−1_I、B=2|I|+1；LOW_I有g=1_I、B=1−|I|。H的编译只需要已证上界g≤−1_I；LP精确最小性才用相等。当前signed主定理给相等所需下界：不交整数资源总客户2m−1，任一长度t<m历史至少一资源R的旧计数低于|R|。强制R后若没人复制，收益≥1；若有人复制，则与该更深真行动者同叶份额相等，深度归纳给≥1。联同已证低退出M≤1，正常各M=1。补读价格上下域定理完整clean/cutoff论证，确认H出口永久BI、提前Y未越cap仍clean；LOW则用全历史freshQ地板与B计数cutoff给每个正常M=1，故其标记外坐标严格0。未将这些真子SPE换成静态NE或若干终局。

对正高度0=s_0<s_1<…<s_a=p，I_l={i:g_i≥s_l}，权w_l=s_l−s_(l−1)，每个正坐标的权重恰g_i。因此正层供应−g_+，成本2P+p。负高度0=t_0<…<t_b=n，J_l={i:−g_i≥t_l}，权v_l=t_l−t_(l−1)，LOW供应(−g)_+，成本n−N。所有权非负有理，零层省略，总signed缺陷≤0，总成本

\[
C(g)=2P-N+p+n.
\]

这里成本是附加组件的half差额2W−OPT；多负坐标使它为负不涉及负客户或负复制权重。单负坐标成本0。

限定LP为min Σ_s B_s y_s，约束g+Σ_sg_s y_s≤0、y≥0。其对偶为max λ·g，λ≥0且B_s+λ·g_s≥0。H的全部非空子集约束等价Σ(λ−2)_+≤1；LOW等价Σ(1−λ)_+≤1。因此对偶域恰K_pm。对任意λ∈K_pm，正部贡献≤2P+p，负部贡献≤−N+n；令正坐标λ=2并使一个最大正坐标为3，负坐标λ=1并使一个最大负坐标为0，零坐标λ=1，两类为空则省略，两个预算同时满足并达到C(g)。层原始成本与显式对偶价同值，弱对偶即足证精确最小。

此达到价可依g变化。结论只属于固定H/LOW字典、非负权与sum-g供给规则，不是产品exact-M最优、所有修复器最优，也不证明同一个λ在全实例上付款。标签编码修复不进入上述LP、支持函数或符号代数，所以成本未变。

## 完整标签历史上的永久退出与全树IC

对每个组件c、每个早期正常位置i、每个标签T_c，指定从该正常前缀强制T_c后的完整真子SPE rho^c_(i,T_c)，含T_c等于own。记当前上界U_i^c，且正常末位为BR。任意正常前缀后的不同元组T=(T_c)_c触发唯一首次异常层i：所有坐标含未改坐标永久转入其rho^c_(i,T_c)。rho读取实际投影标签历史。后续任意偏离不重选退出点，也不因偶然再等于正常标签而reset。

尚未退出的早期节点，任意不同元组偏离的收入≤Σ_c U_i^c≤Σ_c u_i^c，正常IC成立。原精确M表可令U=M；有限非紧U表同样可用，只需每一合法标签及其完整退出都被覆盖。尚未退出的末位节点逐坐标BR相加。

已经退出的任意有序节点，其最早异常层及当时元组是历史的固定部分。当前再偏离不改变它，故各坐标仍在同一份完整rho中比较真实后继。各坐标IC均非负，客户块不交使联合偏离收益差为其和，全局IC成立。这覆盖所有合法有序历史，不只实际路径或第一次偏离的叶。own退出必要，因为只改一个坐标时其它坐标的原normal尾可能尚未可信；保留normal尾无法用其真退出帽付款。

这证明的是一份具体构造产品SPE，不声称任意联合SPE可分解，不假exact-M可加。清共同正整数Q后，原有理质量及所有层高化为不同单位客户/整数不交副本；收益、弱IC和BR同比缩放，玩家仍为m名单位玩家。

## 福利精确可加及HALF5应用

不交客户给正常W_*=Σ_cW_c。对任意全局m槽元组，投影是每个组件合法m槽，故OPT_*≤Σ_cOPT_c。反向逐组件选最优m槽元组，将相同槽号的标签配成全局标签；完整Cartesian目录使每一槽合法，并同时取得各组件最优覆盖。非空目录和允许重复使少于m槽可补齐。于是OPT_*=Σ_cOPT_c，差额恰

\[
B_\mathrm{new}=Q[B+C(g)].
\]

U版取d=U−u分层，原g≤d使总实际缺陷≤0；层的W/OPT成本仍恰C(d)，非仅上界。因此严格负预算才可编译成反例；本轮没有给出严格负种子。

固定m，HALF(m)⇒每个末位BR目标B+C(g)≥0，否则产品反驳HALF。反向若全部目标预算非负，对原真SPE的实际目标有g≤0，故C=n−N≤0，B≥N−n≥0。两方向的m保持相同。m=2只有一个g，正侧3g，负侧0；m=1另用单人BR，不硬套字典。零客户不生严格负种子。

已完整重读HALF5主定理的同标签历史范围、53行的非负组合、全部类型覆盖机制和零福利边界，继承其已有精确全域证书结果，没有回放核验器或原数组。把已证HALF5作用于上述m=5产品，Q>0推出每个五人目标的B+C(g)≥0，完整U版亦然。该应用只付五人预算方向，不给一般m、六人预算或RT5真值。原边保contribution而不是把这一应用说成源输入推出signed目标整条定理。

## 成熟数学继承与P7的定向版本修复

其余15个旧边不依赖signed覆盖反演。共享P7由v1刷新v2后，下表的p7-supports与p7-and-parent两条命中变更端点而改为replaced，另13条的端点pin及全部直接证据字节仍相同，原path/SHA保留。全部旧边的条件、ALL前提、whole_result/contribution及完整解释均已实际读过：

| 旧边文件 | 保留的具体数学及边界 |
|---|---|
| strict-tail-instance-fresh-copy-floor.json | P+C/m=2m+1；强制fresh叶若被复制，以同叶同收益和更深IC归纳，不从尾列价格直接读利润。 |
| strict-tail-small-player-guard-specialization.json | β=0、κ=1、叶大小m²+2<2(2m+1)仅m=2,3；不冒全m守卫。 |
| predictable-seat-kernel-to-fixed-p-bellman.json | 原时间几何首次active权，不按价格重排；ordinary报告不认证ACT最优化或NET。 |
| true-last-two-pay-rt5-terminal-regret.json | 同背景真末回复付r4+r5≤实际差集税≤Z；不支付前三人。 |
| insurance-sample-rt5-pressure.json | 44客正经济/银行块20个Cartesian标签，既有控制器及R/Z=20/23仅给压力；这些正块标签本就可区分，signed编码修复不影响它。此边为checks。 |
| rt5-and-terminal-implication-yield-five-half.json | RT5与任意叶充分蕴涵必须ALL；关系conditional，HALF5不能反推RT5。 |
| integer-core-credit-lifts-to-full-history-guard.json | 整数平衡信用与非核心1/m，未满可选/严格拒满双归纳；outside不需小。 |
| pb-fixed-background-cannot-be-realized-on-path.json | 末D单例真偏离排除固定PB背景接regular尾的在轨实现，不否其合法离轨子SPE。 |
| occupancy-transfer-produces-two-client-wallet-failure.json | XY→YX→YY的A_B=2、X_B=−1、社会差1；不否actual路径钱包。 |
| p7-supports-true-third-rows-in-266-cone.json | 两真实第三节点各11个合法P7实例，只付266中的22行；不抬升松弛点为游戏。 |
| fractional-vertices-to-fixed-complete-policy-price-rows.json | 固定全树Γ与非负价格的有限V_p，含W=0；没有跨σ统一付款。 |
| population-affine-audit-supports-strict-family.json | q22严格基点和非负斜率付全q族，原13/40表独立；此边为checks。 |
| containing-prefix-specializes-to-repeated-prefix.json | E=F=C、p=2c和同索引真枝使96角限制到48角；不升六人。 |
| fixed-rank-family-specializes-to-one-departure.json | k=1的同完整形式σ只保D≤1，rank2省略行负；九人仅族内首个half分离。 |
| p7-and-parent-closure-complete-indexed-menu-rows.json | P7与父闭包ALL，55新增行保索引/共同d/全family；浮点6750不认证精确可行。 |

26核心的19 linked/7 isolated状态沿原数学用途保留。两个ADM保存点不同输入的53/17与47/24，无互推边；逐根坏后继的最早两层未可信；四主题16客只否局部独占信用而全局余额为正；背景总税反例只反其k−1税合同；44客压力与人口恢复只有语境边。因此这些isolated-after-review既不应因本次源变更删除，也不应为增加连通性硬造逻辑边。上述数字与证书是历史成熟结果的继承，不是本轮新增计算结果。


## P7改版对两条旧边的精确影响

当前P7 v2仍为：前缀两位负载p∈{0,1,2}，同背景1/(p+3)加权最大H，强制H后同一sigma的真Q/R，对任意两个合法五槽菜单D/J有17040u+1085K−2679Σj/(p+3)−ΣF(p,d)≥0。当前资源§2的F表仍分别为(0,960,1220,1480,1740,2000)、(0,1665/4,2745/4,3785/4,4825/4,5865/4)、(0,320,524,728,932,1136)，权重仍17040,9000,10080,600,1085,360,2679。K只作裸大小cap，强制者不当真优化者。

`p7-supports-true-third-rows-in-266-cone`：actual与最大根后的两个真实第三位，各取同一最优五槽D和11个合法J（原最优及十个路径标签各重复五次），每节点11行，共22行。D与J允许重复，不要求主题覆盖单射；强制最大根后续真第三位仍由同sigma定义。故版本刷新不改变其局部contribution，其余244行和松弛点实现性仍不在本边结论内。

`p7-and-parent-closure-complete-indexed-menu-rows`：P7与父94/60闭包保持ALL；三固定源七回复J加indexed本族三J得到24实例，自身末题重复J给三固定源各8种D和indexed4种D共28，indexed自身三个主题重复另3，共55。indexed均先同索引真背景/当前代入再求和，保5theta在求和内。6541→6565→6659→6687→6747→6750仍是原库路径。固定共同d和全max_bits后每个新增项最多涉及一个完整family，未把浮点发现升级为全域精确证书。

资源§6的退化弦界没有被这两条边作为前提；它的来源字节变化通过P7证据引用导致端点pin变化，正是替换这两条而不改其数学的理由。本worker没有复算144态、6750行或原数组。新增当前资源§2与本节作定向证据，旧原审查与旧15条成熟解释均不重写。

## 比较路由与精确读取边界

当前新任务没有声明overlap_comparisons/follow-up对，故不新增closed_overlaps。旧任务仅有任意占用流—路径钱包in-packet对，已经由保留的转移边准确说明；记录为additional_comparisons。字典成本—真实编译、HALF5—五人预算也是本次实读的additional_comparisons。RT5前三位预算、六人预算、ADM全称、松弛点真实抬升等原有open义务保持各自范围；不以本次来源修复假闭合。

散列预检的全部76个当前reading_refs另在ledger逐文件记录。共享P7审计资源曾出现task引用54cf3b…与工作区855a97…不同，已立即报Root，reading-checkpoint保留该实际事件。Root确认来自Boss1提交65c720cb2af4e71896081ed79bd91a693723c204：只补§6超几何弦界q=0,d=0和q=1,d=5恒端点、其余分母为正及r=0/5等号，§2的P7没有数学变更。Boss1将P7登记发布刷新为v2/pin60de1ef4c05b1a893c0b5671b1528ca2beba582a8e6bfc6dadef5a16cba3b9f6，并发布本任务共享输入刷新和资源855a97…；Root只核Git来源及实际published状态后通知本worker。本worker随后完整读资源当前全文及v2记录，确认P7的七权、3×6表、真第三节点与合法两菜单范围保持。两条受P7端点影响的旧边保原数学论证/edge_id作定向替换，其余13边原字节retained。四个新边的当前直接证据均已按其实际源核SHA；科学程序仍0次。
