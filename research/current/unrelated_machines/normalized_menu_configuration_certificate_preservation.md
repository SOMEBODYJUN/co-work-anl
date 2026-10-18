# 完整归一化菜单的配置证书保持与三行三度 Santa Claus 间隙

## 精确身份与读取目的

- **ID / version**：`UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v3`。v1/v2是保留原字节的过程来源，不另登记成熟成果。
- **Objects / Domain**：下述完整显式 normalized flat 菜单、其普通 UM 矩阵、正 support 状态 LP、state-dummy SC 与 SC 路径对象；非空 groups，每组非空有限 indexed states，非负二进制有理权，各 state 总质量恰1。允许零 incidence、重复 indexed states、unused resources；同一 state 不重复列同一 resource。
- **Quantifiers / Exact Statement**：对每个该域内对象，完整 flat UM 的 machine CONFIG(1) 可行，当且仅当正 support 状态 LP 可行，当且仅当其 state-dummy SC 的 CONFIG(1) 可行。已有 binary-tree / menu-path normalform 双向保持这些 unit-threshold 证书；再接 SC 路径可将 SC 的 item positive-degree 降至3，保其实际最优值及 CONFIG 最高阈值。给定任一方的显式有限有理证书，所述转换确定性总位多项式。
- **Assumptions / Definitions**：没有复杂度假设。machine CONFIG 的机器配置处理时间≤1、每机器配置权和1、每原 job 覆盖≥1；SC CONFIG(t) 的 agent 配置价值≥t、每 agent 权和1、每 item 总边际≤1。允许 empty configuration；对象与不等号方向不同。
- **Conclusion**：得到 rowtotal≤3、item positive-degree≤3、positive values 仅1与1/D的显式 SC 族，CONFIG 最高阈值1而实际 OPT=1/D。完整 flat normalform 的 machine CONFIG(1) 亦可行而实际 makespan=2−1/D。
- **Dependencies**：完整 flat 的实际值 `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`；完整 normalform 的实际保持 `UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1`；具体矩阵与证书的自足证明如下。相邻 helper 路径归属 BCG2009，不主张新的 degree-three 思想。
- **Scope / Limits**：这是限定对象/阈值的有限证书合同与既有 gap 的精确转述，不是一般 UM CONFIG 保持，不保任意阈值或给定证书全部边际，不提供取得未知配置证书的 oracle。CONFIG 反例不是 actual OPT≥1 的 YES，不能据此否定实际 promise 算法或证明 near-2 困难性。
- **Evidence / Counterevidence**：完整 statement-first 独立重构后才读作者 Proof；root 实读并核全部新桥、零值与位长。原审查前独立研究的 all-membership LP 与本 positive-support LP 明确分开；无 standing fatal。最终正文及来源的实际审查见[审查记录](../../reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md)。
- **Status**：限定证明完整；内部独立审查和作者读后完成，最终正文另记实读范围；无新软件/有限实验认证，外审和全球新颖性未认证；`UM-TARGET-v1` 仍 OPEN。
- **Related Files**：[实际 normalform](degree_three_weighted_menu_cube_embedding.md)、[实际 state-dummy 桥](normalized_weighted_menu_santa_value_and_size.md)、[审查](../../reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md)。

## 1. 完整矩阵与正 support LP

记 groups 为 G，group g 的 states 为 S_g，resources 为 U。state (g,s) 的显式 incidence 权为 p_gsu≥0，和为1，正 support 为 P_gs={u:p_gsu>0}。

完整普通 UM 矩阵 P(Q) 含每 state 一台不同 private 机器 M_gs、每 resource 一台 R_u。每 group 一枚 unit selector J_g，可在该组任一 private 机器执行。每 incidence 一枚不同原 job，仅可在 M_gs 耗 p_gsu 或在 R_u 耗1；其余∞。所有未选 state 的 jobs、零时间原 jobs 与 unused 机器都在完整对象中。

正 support 状态 LP（FSLP）为

\[
\lambda_{gs}\ge0,\qquad \sum_s\lambda_{gs}=1,\qquad
\sum_{g,s:u\in P_{gs}}\lambda_{gs}\le1.
\]

系数是正 support 的0/1指示，既不是 p 权，也不计零 incidence。记 V(Q) 为每 group 选一 state 并领取其资源子集、跨 groups 所领资源不交时，最小所领质量的最大值。已有实际合同给 OPT(P(Q))=2−V(Q)，包括 V=0。

## 2. FSLP 与完整 flat machine CONFIG(1)

给定可行 λ。在 M_gs 上记其全部 incidence jobs 为 I_gs，零权 jobs 为 Z_gs。配置 {J_g}∪Z_gs 给权 λ_gs，配置 I_gs 给权1−λ_gs；两配置真实负载均为1，机器权和1。每 positive job 的 private 覆盖为1−λ，每 zero job 的 private 覆盖为1，每 selector 的跨 private 覆盖为1。

对 R_u，每个 positive incidence singleton 配置给权 λ_gs，剩余给 empty。FSLP 保证权和≤1；补 empty 后为1。于是全部原 positive jobs 覆盖恰1，零 jobs 也恰1，unused 机器用 empty。支持 O(S+I+|U|)，不删任何实际原任务。

反向给完整有限 machine CONFIG(1)。令 α_gs 为 M_gs 上含 selector J_g 的配置总权。每组 Σ_s α_gs≥1。positive incidence 与 unit selector 不可能同处 private 合法配置，故其 private 覆盖≤1−α_gs。它仅另有 R_u 一端，为满足覆盖≥1，resource 覆盖至少 α_gs。R_u 的 jobs 全为 unit，每配置至多一枚，故每 u 的 positive incidences 对应 Σα≤1。将每组 α 向下缩减为总和1的 λ，所有 resource 容量仍成立。

零 private job 可以与 selector 同居，不能用它作排斥下界；这正是 FSLP 只计正 support 的原因。原零 job 在正向新证书中已精确覆盖。若需将一般≥覆盖证书改为精确覆盖，逐 job 剪除多余覆盖，必要时拆分一个配置；向下封闭使负载不增、其它边际不变，每 job 至多新增一次切分。也可直接经 FSLP 正向输出新的精确覆盖证书。均不保原证书所有边际。

## 3. 完整 normalform 的证书双向保持

Tree T：将每组 K 个旧 states 作 full binary tree 叶，每顶点一新 group，每非 root 顶点 v 有 fresh own-resource a_v。root internal 菜单为两个 child singletons；非 root internal 菜单为 own singleton 和两个 child singletons；非 root leaf 菜单为 own singleton 与原完整 state。root leaf（K=1）仅保原 state。新 singleton 权1，旧零 incidence 仍保留。

FSLP 正向令 x_v 为其 subtree 旧 λ 总和。root children 概率为 x_child；非 root own 概率1−x_v，children 或旧 leaf state 概率为相应 x。每 own-resource 占用 x_v+(1−x_v)=1，旧 resource 正 support 占用不变。

反向不假设仅一条路径活跃。从 root 发1单位流。若进 v 的流 f_v≤parent 选择 v 的概率，own-resource 容量给非 own 菜单概率和≥f_v。按 child 菜单概率容量贪心分流；leaf 送出的旧 λ 不超过其旧 state 概率。每旧组叶流和1，旧 resource 占用只减。K=1直接保留。额外 off-path activation 不影响这个剪流证明。

Menu path D：对旧 u 列全部菜单中 incident 的 distinct groups g_1,…,g_d，包含仅有零 u 项的 group。d≥1时用 ports z_1,…,z_d 替 u；本组所有 u 项改至本组 port。加 d−1个 helper groups，各有相邻两个 port 的 unit singleton states。d=1无 helper，d=0保 unused 资源。

给旧 FSLP，令 x_i 为 g_i 对 positive-u states 的概率和。Σx_i≤1。选 hole 分布 π_i≥x_i、Σπ=1；helper j 左 singleton 概率 Σ_(h>j)π_h，右 singleton 概率 Σ_(h≤j)π_h。port i 的 helper 占用1−π_i，加旧 x_i 不超过1。反向把 d 个 port 容量相加，d−1 helpers 的 singleton 总占用恰 d−1，故旧 positive 占用≤1。零 incidence 只影响 port 名单，不占 positive 容量。

因此 T、D、N=D∘T 双向保 FSLP；结合§2也双向保各自完整原任务的 machine CONFIG(1)。已有 actual normalform 合同另保 V 与 UMOPT，不从分数等价倒推实际保持。N 每组≤3 states、每 resource incident groups≤3。

## 4. State-dummy SC 的实际值与 CONFIG(1)

SC(Q) 为每 state 一 agent，每 resource 一 real item，价值 p_gsu；每组另有 K_g−1个 dummy items，各对本组所有 state agents 值1、其它值0。每 agent real row 总值1、全部 rowtotal=K_g。实际 SCOPT=V(Q)：每组至少一 agent 未拿 dummy，用其 real bundle 反解；反向给其余 agents 各一不同 dummy。

FSLP 正向：agent(g,s) 以概率 λ_gs 取完整 positive support；若 K_g≥2，对每 own dummy singleton 另给概率 (1−λ_gs)/(K_g−1)。每 dummy 总占用1，real 容量恰为 FSLP。K=1时 λ=1，无除零。

SC CONFIG(1) 反向：含 own dummy 的配置剪为一个 dummy；无 own dummy 的合法配置必须含完整 positive real support，因为 real row 总值恰1。删外国 dummy 及零价值项不会增加边际。令 real-support 配置概率为 ρ_gs；K−1个 dummy 容量迫每组 Σρ≥1。向下缩减到每组概率和1即得 FSLP。target>1时，每 agent 每配置必须有 own dummy，K个 agents 需要至少 K 总 dummy 边际而只有 K−1容量，矛盾。因此最高 CONFIG 阈值≤1，可行时恰1。

这没有将一般 SC 的无限 row 免费归一化；也没有把 SC CONFIG 的最大阈值误作 UM CONFIG 的最小阈值。

## 5. SC 层路径的实际与有限证书合同

对任意非空 old agents、有限 items（可空）、有限非负有理 additive 估值，列 item u 的 positive agents i_1,…,i_d。d≥1时以 d 个 copies z_(u,j) 替 u，old agent i_j 只对自己的 copy 保原正值；加 d−1个 helper agents，helper j 只对两个相邻 copies 各值1。d=0保全零 unused item；d=1无 helper。记转换为 P_SC。

实际前向对每 0<v≤1成立：删 old allocation 的零价值 items，为每 u 的实际正 owner 留 hole；其余 copies 以路径匹配给 helpers 各一枚，helper 得1≥v，old agent 值不变。无人领 u 时任选 hole。

实际逆向对任意 v>0成立：先删零价值 items。每 helper 至少领一枚相邻 copy，可能两枚；d−1 helpers 占至少 d−1枚不同 copies，故 old agents 合计至多领一枚该 u 的 copy。合回 old u 没有冲突，值完全保留。因此若 oldOPT≤1，新旧 actualOPT 相等；oldOPT=0由逆向排除任何 new 正值。oldOPT>1不声称最优值保持。

CONFIG 正向对每 0<t≤1：删 old 配置零值项，将 u 重标为该 agent 自己的 copy。令 x_j 为其 u 边际，Σx≤1；如§3选 hole π≥x，并给 helpers 相邻 singleton 配置相应前缀/后缀概率。每 helper 配置值1≥t，每 port 边际 x_j+1−π_j≤1。

CONFIG 逆向对任意 t>0：删配置零值项。每 helper 配置非空，其 expected copy 件数至少1，即使它同时含两个 copies。将 d 个 copy 容量相加，helper 总占用≥d−1，old agent 的 copy 边际总量≤1。每 old agent 对该 old u 只有自己的一枚正 copy，所以重标回 u 不会在单配置合并多份正值，配置值不变。这即为 old CONFIG(t)。不能在 t>1时将 helper 配置剪成 singleton。

若 old CONFIG 最高阈值≤1，新旧最高阈值相等；0端点由正阈值逆向排除及两边各用 empty CONFIG(0) 处理。t=0不用于 helper 非空投影。old rowtotal 精确不变，新 helper rowtotal=2；每 copy positive-degree≤一个 old agent加两个相邻 helpers，即3。构造不依赖 OPT 或目标阈值。

这是 BCG2009 adjacent-dummy 路径的 unit 目标证书重构；它保 old rowtotal，所以单独不把一般 SC 无界 row 降至3。

## 6. 组合与自足间隙族

令 J(Q)=P_SC(SC(N(Q)))。SC(N(Q)) 的 rowtotal≤3、actualOPT及 CONFIG 最高阈值均≤1。因此§5同时精确保两最优值，最终每 row≤3、每 item positive-degree≤3。

固定显式整数 D≥2。Q_D 有 resources g_(a,j)、A_a（a,j∈[D]）。main group 有 D 个 states，第 a 个含本行 D 个 g_(a,j)，各权1/D；每(a,j)有 helper group，二选 singleton g_(a,j) 或 A_a，权1。

FSLP 取 main 每 state 概率1/D，helper 取 g 概率1−1/D、取 A 概率1/D。每 g、A 占用恰1。实际分配中 main 若在某行领 r 个 g，相应 r 个 helpers 都必须领该行同一 A 才能有正值，所以 r≤1。main 取 g_(1,1)、对应 helper 取 A_1、其余 helpers 各取自己的 g 达到 V=1/D。

故 J_D 的 actual SCOPT=1/D、CONFIG 最高阈值1；row≤3、item positive-degree≤3，正价值仅1或1/D。相应完整 flat normalform 的 machine CONFIG(1) 可行，实际 UMOPT=2−1/D。

这是既有 selector/parking gap 模式经明确证书合同的转述，未提供源 NP-hardness。J_D 是实际 OPT<1 的 NO，不能反驳承诺实际 OPT≥1时的常数 finder。

## 7. 总位复杂度与未解决义务

原 Q 有 n groups、S states、I incidences。Tree 有2S−n groups、5S−4n states、I+4S−4n incidences；路径 helper 数至多相应显式 incidences 数。SC 的 agents 为 state 数，items 为原 resources 加 Σ(K−1) dummies；SC 路径 helpers≤old positive 条目数，items≤positive 条目数加 unused 数。所有 dense 矩阵乘积仍多项式。

证书转换只用给定有限列表、概率部分和、组内削减/归一、流剪枝和配置修剪；按实际支持编码长度收费，不按分母、1/p、1/V展开，也不承诺取得未知指数支持。Q_D 本来有 D²+1 groups、2D²+D states、3D² incidences、D²+D resources；后续规模 poly(D)，并非 poly(logD)。

空 items/全零 SC 估值的正值前件可为空，0端点仍正确；保 old agents 非空以使 minutility 有定义。Normalized-flat 非空且 state 总质量1保证 positive support 非空。完整 UM 任务和 SC 配置中可删的零价值项是不同对象。

真正留下的义务是：rowtotal≤3、item degree≤3且 actualOPT≥1时，是否有固定正常数的 deterministic bit-polynomial allocation finder；或构造具有真实 completeness/soundness 的 near-2 源。本证书结果均未完成它们。
