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

## 8. 新合同：阈值 unit-demand 叶、完整条件 Hall 流与共同边际

本节至§11另立新身份 **`UM-THRESHOLD-LEAF-HALL-CONSISTENT-MARGINALS-PATH-PROJECTION-GAP-v1`**。前七节、原 v3 身份及其既有依赖、审查范围保持原义；新增条款的 Exact-first 重构、作者读后及最终正文实读范围须另记，不能回填为旧审查已经覆盖。所用相邻 helper 路径来自既有 BCG2009 机制。本节研究的新合同与其投影结论不认领新的通用复制或归一化方法，亦不提供一般 UM 算法或困难性结论。`UM-TARGET-v1` 仍 OPEN。

- **Objects / Domain：** 完整显式 normalized-flat 菜单、其全部原 jobs 的普通 UM 矩阵、阈值 unit-demand 叶图、指定 core-state 的 \(\lambda,z\)、global 叶流及全部 perspective 条件叶流。groups 非空，每组非空有限 indexed states，各 state 非负二进制有理系数和恰一；允许零 incidence、重复 indexed states、unused 资源。\(0<\epsilon\le1\) 为二进制有理数。core 系数可为一，不承诺全系数微小。
- **Quantifiers：** 对每个该域内 \(Q,\epsilon\)，(8.5) 的必要性成立；对每个非空指定旧 core 集合及每个 supplied basic 点，\(D_+\) 逐点投影与有理扩展成立；对每个整数 \(t\ge2\)，同一个 \(Q_t\) 的 sharp gap 成立。自动消去全部阈值 unit-demand 组的版本另以每个旧组均非阈值 unit-demand 为共同前提。
- **Exact Statement：** ① \(\operatorname{OPT}(P(Q))\le2-\epsilon\) 蕴含完整 \(R_{\rm cons}\) 及弱 \(R_{\rm leaf}\) 可行，二者为确定性总位多项式有理 LP；② 指定 partition 下 \(\operatorname{proj}_{\lambda,z}R_{\rm cons}(D_+(Q))=\operatorname{proj}_{\lambda,z}R_{\rm leaf}(D_+(Q))=B_\epsilon(Q)\)，保给定点而不要求 \(z=\lambda\)；③ \(Q_t\) 在 \(\epsilon=1\) 两合同均可行且全组 FSLP(1) 可行，但精确 \(V(Q_t)=1/t\)、\(\operatorname{OPT}(P(Q_t))=2-1/t\)。弱合同有每条件单整数 matching 乘 \(\lambda\) 的 witness；强化 (MC) 合同仅承诺条件 matching 混合。
- **Assumptions：** 无复杂度假设或外部 source-YES 见证；只用标准有理 LP、二部 matching、有限运输及本文明确完整矩阵。未假设 exact SDP feasibility、配置优化 oracle 或所有 cores 的共同 law。
- **Scope：** 仅指定 normalized-flat 结构、所定义的叶流合同及 supplied point 转换；不是一般 UM CONFIG 等价或全输入调度算法。与 literal 当前二阶/degree-four PSD 合同不同；不把叶边际一致当完整 matching law 或多个 cores 的共同选择。
- **Conclusion：** 此必要 relaxation 可在实际 \(V\to0\)、ordinary OPT 趋二时仍以 unit 阈值接受，因此其可行性不蕴含统一正常数 \(V\) 或相对该 unit 阈值统一次二保证。该结论不否定相对 actual OPT 的一般近似，也不否定 actual-YES promise 算法。
- **Dependencies：** 本页§1–7的 `UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v3` 仅按其既有 scope 使用；完整实际值桥 `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`；BCG2009 既有相邻 helper 路径。新的 \(D_+\) 与旧 \(D\) 的零标签名单明确区分；本章另证其实际值/FSLP保持及共同边际投影。
- **Evidence：** root 已实读新 Exact 与新增正文，并实际读、独立重跑两套独立 checker；每套程序及弱/强合同覆盖仅按新审查和冻结运行记录的实际范围登记。旧弱程序输出不因加入 (MC) 而升级为强合同审计，原作者有限统计不转记成 root 认证。
- **Counterevidence / Objections：** 自动 partition 前提不可省；强 (MC) 条件流一般需混合；positive-degree 三不等于所有零资格也三度；反例含 unit core 系数且不提供常数比例坏组稳健性。未给出 standing fatal 的结论须以新审查实际记录为准，不能从旧 review 继承。
- **Status：** 证明及新 Exact 已分离冻结；独立重构、作者读后、v3 (MC) 重放与最终正文实读的完成范围另记新记录，本草稿不提前升级未完成步骤。外审、全球新颖性及一般近似保证未认证；主目标 OPEN。
- **Related Files：** [完整实际值桥](normalized_weighted_menu_santa_value_and_size.md)、[旧实际 normalform](degree_three_weighted_menu_cube_embedding.md)、[仅覆盖前七节的旧审查](../../reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md)。本新 Claim 的冻结 Exact、作者证明、独立重构及重放另由新审查记录定位，不复用旧审查身份。

对象仍为§1的完整显式 normalized-flat 菜单：非空 groups，每组非空有限 indexed states，各 state 的非负二进制有理系数和恰一。允许零 incidence、重复 indexed states 与 unused resources。记

\[
v_g(B)=\max_{s\in S_g}\sum_{u\in B}p_{gsu},\qquad
V(Q)=\max_{(B_g)\text{跨组不交}}\min_gv_g(B_g).
\]

固定有理 \(0<\epsilon\le1\)，目标 \(T=2-\epsilon\)。定义

\[
H_g(\epsilon)=\{u:\max_s p_{gsu}\ge\epsilon\},\qquad
b_g(\epsilon)=\max_s\sum_{u\notin H_g(\epsilon)}p_{gsu}.
\tag{8.1}
\]

令 \(L=\{g:b_g(\epsilon)<\epsilon\}\)、\(C=G\setminus L\)。对每 \(\ell\in L\)，有

\[
v_\ell(B)\ge\epsilon\quad\Longleftrightarrow\quad B\cap H_\ell(\epsilon)\ne\varnothing.
\tag{8.2}
\]

右侧显然充分；若没有 heavy item，任意 state 在所领集合上的值至多 \(b_g\)。反之，若 \(b_g\ge\epsilon\)，完整补集 \(U\setminus H_g\) 自身就否定 (8.2)。所以这是精确阈值 unit-demand 判别，包含所有 states 均为 unit singleton 的组，并非只按句法识别 singleton。以下称 \(L\) 为叶组，\(C\) 为 core。

对 core-state 引入 \(\lambda_{cs}\ge0\)、\(\sum_s\lambda_{cs}=1\)，以及正 support 上 \(0\le z_{csu}\le\lambda_{cs}\)；非正 support 的 \(z\) 固定零。要求

\[
\sum_u p_{csu}z_{csu}\ge\epsilon\lambda_{cs}.
\tag{8.3}
\]

叶边集为 \(E_L=\{(\ell,u):u\in H_\ell(\epsilon)\}\)。引入同一全局叶流 \(y^0\)，并为每个 core-state 引入一份条件叶流 \(y^{cs}\)，均非负且仅支撑于 \(E_L\)。弱合同 \(R_{\rm leaf}\) 的全部行列为

\[
\begin{aligned}
\sum_{u\in H_\ell}y^0_{\ell u}&=1
&& (\ell\in L),\\
\sum_{c,s}z_{csu}+\sum_{\ell\in L}y^0_{\ell u}&\le1
&& (u\in U),\\
\sum_{u\in H_\ell}y^{cs}_{\ell u}&=\lambda_{cs}
&& ((c,s),\ell\in L),\\
z_{csu}+\sum_{\ell\in L}y^{cs}_{\ell u}&\le\lambda_{cs}
&& ((c,s),u\in U).
\end{aligned}
\tag{8.4}
\]

每个条件列只放该 \((c,s)\) 自己的 \(z\)，没有放其他 cores 的条件用量。每一份条件流覆盖**全部**叶，不是只核若干资源或邻近叶；容量是 perspective 的 \(\lambda_{cs}\)，不是一。\(\lambda_{cs}=0\) 时整份 \(z,y^{cs}\) 为零。空 \(C\)、空 \(L\)、unused 资源与零系数均按原式解释。

强化合同 \(R_{\rm cons}\) 再要求每个 core 的整个菜单恢复同一全局**叶边边际**：

\[
\sum_{s\in S_c}y^{cs}_{\ell u}=y^0_{\ell u}
\qquad(c\in C,(\ell,u)\in E_L).
\tag{MC}
\]

它仍不要求所有 core states 与一个完整叶 matching 的共同 law，也不把各份条件流的分解强制成同一份完整 matching 分布。

**必要性。** 若 \(V(Q)\ge\epsilon\)，在一份实际达到分配中为每个 core 选 attaining state，置该 state 的 \(\lambda=1\)、其他为零；保留该 state 实际领取的正资源，令 \(z\) 为其所有权指示。每个叶保留一枚实际领取的 heavy item。这些叶物品构成一份覆盖全部叶的整数 matching，且与全部 core 所领资源不交。把该 matching 用作 \(y^0\) 及每个正 \(\lambda\) 的条件流，零 \(\lambda\) 流置零，即同时满足 (8.3)、(8.4)、(MC)。故

\[
\operatorname{OPT}(P(Q))\le2-\epsilon
\quad\Longrightarrow\quad R_{\rm cons}\text{ 可行}
\quad\Longrightarrow\quad R_{\rm leaf}\text{ 可行}.
\tag{8.5}
\]

记 core indexed-state 数为 \(S_C\)、正 core-state incidence 数为 \(I_C\)。弱合同有 \(S_C+I_C+(1+S_C)|E_L|\) 个变量，行数为 \(O(I_C+S_C(|U|+|L|)+|U|+|L|)\)，另含归一化及非负界；(MC) 至多增加 \(|C||E_L|\) 行。阈值测试、全部 LP 系数与所列行列均按显式输入和 \(\epsilon\) 的总位长多项式构造。标准有理 LP 给确定性总位多项式可行性、可行点或 Farkas 拒绝证书。本结论没有调用 exact SDP feasibility，也不把拒绝的逆命题当作实际调度证书。

## 9. 正邻居路径 \(D_+\)：连共同叶边际也恰投影回 basic LP

先以非空旧组集 \(C\) 为**指定 core**，不对它们重新消元。定义旧 basic 多面体 \(B_\epsilon(Q)\)：保留 \(\lambda,z\) 的归一化、support 界及 (8.3)，并要求

\[
\sum_{c,s}z_{csu}\le1\qquad(u\in U).
\tag{9.1}
\]

本节允许任意分数 \(z\)，不假设 \(z=\lambda\)。

对旧资源 \(u\)，按固定顺序列其 **positive** neighboring groups \(c_1,\ldots,c_d\)，每组只列一次。在 \(d\ge1\) 时建立 ports \(u_1,\ldots,u_d\)，group \(c_i\) 的所有 states 对旧 \(u\) 的正系数都移到自己的 \(u_i\)。添加 \(d-1\) 个叶组；叶 \(j\) 有两个 unit singleton states，分别在 \(u_j,u_{j+1}\)。\(d=1\) 无新叶，\(d=0\) 保留旧 unused 资源。每个原零 incidence 保留 private time 零：原组有 own port 时用 own port，否则在 \(d\ge1\) 时用该旧资源的一个固定 port，在 \(d=0\) 时用保留资源。不同旧资源的 tags 不合并。记此明确操作为 \(D_+\)。

这是§3既有相邻路径思想的正邻居变体。**旧 \(D\) 的名单还包括仅有零 incidence 的组；此处 \(D_+\) 不包括它们，而将其零标签按上段路由。两定义不互相替换。** 这里仅主张各自完整构造实例间的值与下述证书关系，不说旧、新矩阵或机器完全相同。新资源的 positive-group degree 至多三；仅零 incidence 可能增加完整 finite-eligibility 度，因此不能把 positive-degree 界冒称全部零标签也只有三度。

在 \(D_+(Q)\) 中，指定 \(L\) **恰为新增路径叶**、\(C\) 恰为全部旧组。则有精确投影

\[
\operatorname{proj}_{\lambda,z}R_{\rm cons}(D_+(Q))
=\operatorname{proj}_{\lambda,z}R_{\rm leaf}(D_+(Q))
=B_\epsilon(Q),
\tag{9.2}
\]

并逐点保留同一个旧 \((\lambda,z)\)。

**正向及同一全局边际。** 对旧 basic 点，在旧 \(u\) 上记

\[
b_i=\sum_s z_{c_i s u},\qquad \sum_i b_i\le1.
\]

选有理 hole 分布 \(\pi_i\ge b_i\)、\(\sum_i\pi_i=1\)，例如把全部余量加到第一项。令 \(M_h\) 是 hole 为 \(u_h\) 的完整路径 matching：叶 \(j<h\) 取 \(u_j\)，叶 \(j\ge h\) 取 \(u_{j+1}\)。其恰占除 \(u_h\) 外的全部 ports。取

\[
y^0=\sum_h\pi_hM_h.
\tag{9.3}
\]

每叶行一，port \(i\) 的叶占用为 \(1-\pi_i\)，故加上 \(b_i\) 后不超过一。

固定某 core \(c=c_i\)，写 \(\lambda_s=\lambda_{cs}\)、\(z_s=z_{csu}\)，非正 state incidence 的 \(z_s\) 为零。构造运输矩阵 \(w_{s,h}\ge0\)，要求

\[
\sum_h w_{s,h}=\lambda_s,\qquad
\sum_s w_{s,h}=\pi_h,\qquad
w_{s,i}\ge z_s.
\tag{9.4}
\]

先置 own entry \(w_{s,i}=z_s\)。剩余行量 \(\lambda_s-z_s\)、剩余 own-column 量 \(\pi_i-b_i\) 与其他 column 量 \(\pi_h\) 均非负，两侧总余量都恰 \(1-b_i\)。按固定次序每步运输行列余量的最小者，即得 (9.4)。若 \(c\) 不是此旧资源的 positive 邻居，直接用 \(w_{s,h}=\lambda_s\pi_h\)，无 own-entry 下界。对每个 core、每条旧资源路径分别构造，但始终使用同一个 \(\pi\)。

定义该路径上的条件叶流

\[
y^{cs}=\sum_h w_{s,h}M_h.
\tag{9.5}
\]

每叶行是 \(\lambda_s\)。own port 的叶占用为 \(\lambda_s-w_{s,i}\)，加 \(z_s\) 后不超过 \(\lambda_s\)；其他 ports 没有该 state 的正 \(z\)，也满足容量。对每个叶边求同一 core 的 state 和，

\[
\sum_s y^{cs}
=\sum_h\Bigl(\sum_s w_{s,h}\Bigr)M_h
=\sum_h\pi_hM_h=y^0.
\tag{9.6}
\]

故 (MC) 对所有 cores、全部叶边同时成立。不同资源路径互不相交，拼接这些流便覆盖全部新增叶。条件流可解释为 \(\lambda_{cs}\) 倍的完整整数叶 matching 的有理混合；一般不能改说单个整数 matching。构造不用除以 \(\lambda_s\)、\(b_i\) 或 \(\pi_i\)：零 \(\lambda_s\) 自动整行零，\(b_i=1\) 时剩余运输为空。\(d=1\) 的 matching 为空、(MC) 无叶行，只有 \(z\le\lambda\)；\(d=0\) 保 unused 资源且正 \(z=0\)。零 incidence 不进入正 support，始终保留为 private time 零的原 job。

**反向。** 任意 lifted 点在旧 \(u\) 的 \(d\) 个 global port columns 相加，减去 \(d-1\) 个完整叶行，得

\[
\sum_{c,s}z_{csu}+(d-1)\le d.
\]

即 (9.1)。其他 basic 条件只改了资源名称；\(d=1\) 直接读唯一 port 列，\(d=0\) 的旧列为零。因此 (9.2) 是两个投影方向的逐点等式，非仅可行性等价。

相同操作还精确保实际值及 FSLP：

\[
V(D_+(Q))=V(Q),\qquad
\operatorname{OPT}(P(D_+(Q)))=\operatorname{OPT}(P(Q)).
\tag{9.7}
\]

实际正向为旧资源的正 owner 留 own hole，匹配其他 ports 给叶，各旧组值不变、叶值一。实际反向在任何正最小值分配中，每路径的 \(d-1\) 叶各领一枚不同正 port，至多剩一枚供全部旧 cores 正用；合回旧资源无冲突，各旧组值保持。若旧 \(V=0\)，任何新正值解会由此反向矛盾，故零端点也保持。FSLP 的正向用同一 hole 构造、反向用同一列相加；在 \(\epsilon=1\) 时 (8.3) 与 \(z\le\lambda\)、state norm-one 也直接迫使每个正 incidence 的 \(z=\lambda\)。

本节指定 partition 是共同前提。若用§8自动消去**全部**阈值 unit-demand 组，必须另要求所有旧组在同一 \(\epsilon\) 下均非阈值 unit-demand。\(D_+\) 只改它们的正资源名称，保留其阈值性质；在此此前提下自动 \(L\) 才恰为新增路径叶。没有此前提时，额外旧组会移入 \(L\)，不能把 (9.2) 偷换为另一 partition 的投影结论。

## 10. 同一完整 \(Q_t\)：弱条件可取单 matching，边际一致仍有趋二间隙

取整数 \(t\ge2\)、\(D=t^2\)。先建立全部为指定 core 的旧菜单 \(B_t\)。资源是 \(g_{a,j}\)（\(a,j\in[D]\)）及 \(A_{a,h}\)（\(a\in[D],h\in[t]\)）。Main \(M\) 有 \(D\) 个 states；state \(a\) 在本行全部 \(g_{a,j}\) 上各给权 \(1/D\)。每 \(H_{a,j}\) 有两个 states：home 在 \(g_{a,j}\) 上给权一，parking 在同行全部 \(A_{a,h}\) 上各给权 \(1/t\)。所有 states 总质量一。特别地，cores **含 unit coefficient**；这里不声称全系数微小。

定义 \(Q_t=D_+(B_t)\)：对 \(g_{a,j}\) 按 \(M,H_{a,j}\) 排序，对 \(A_{a,h}\) 按 \(H_{a,1},\ldots,H_{a,D}\) 排序。\(\epsilon=1\) 时，main 没有 heavy item、tail 为一；每 \(H\) 虽有 heavy home item，但 parking 整个 state 的 tail 仍为一。因此所有旧组均非阈值 unit-demand，新路径叶全部是；不存在给 singleton 加趋零尾巴来规避消元。对任意固定 \(\epsilon>0\)，只要 \(t>1/\epsilon\)，同一结论仍成立。

原 basic/FSLP 证书为

\[
\lambda_{M,a}=1/D,\qquad
\lambda_{H_{a,j},\mathrm{home}}=1-1/D,\qquad
\lambda_{H_{a,j},\mathrm{parking}}=1/D,
\tag{10.1}
\]

并在每正 support 取 \(z=\lambda\)。每 \(g\) 的占用是 \(1/D+(1-1/D)=1\)，每 \(A\) 的占用是 \(D(1/D)=1\)，每 state 的值恰 \(\lambda\)。由§9，**同一个**旧 \((\lambda,z)\) 延伸成 \(R_{\rm cons}\) 的完整有理证书，故也满足弱 \(R_{\rm leaf}\) 与全组 FSLP(1)。

弱合同还有一份更特殊的 witness：对每 core-state、每条旧资源路径，只要该 state 在此路径有正 \(z\)，就留本 core 的 own port 作 hole；否则任选 hole。所有路径匹配拼成一个覆盖**全部叶**的整数 matching，乘该 \(\lambda_{cs}\) 即为整份条件流。global 叶流仍按共同 hole 边际单独构造。此单匹配条件 witness 属于弱合同；加上 (MC) 后使用§9运输给出的条件混合，**不将弱 witness 升级为同时满足 (MC) 的单匹配 witness**。

实际值精确为

\[
\boxed{V(B_t)=V(Q_t)=1/t,\qquad
\operatorname{OPT}(P(Q_t))=2-1/t.}
\tag{10.2}
\]

证明先看任意旧正值分配。若 main 的 attaining state 为 \(a\)，并领 \(r\) 个该行 \(g\)，共同最小值 \(v\le r/D\)。对应 \(r\) 个 helpers 失去自己的 home item，必须从同一 \(t\)-item parking pool 取得其值；该 pool 的总可分质量仅一，故 \(rv\le1\)。因此 \(v^2\le1/D=1/t^2\)；\(r=0\) 时 \(v=0\)。达到时任选一行，main 领其中 \(t\) 个 \(g\)，给相应 \(t\) 个 helpers 各一枚不同 \(A\)，其余全部 helpers 领自己的 \(g\)。main 及这 \(t\) 个 helpers 值为 \(1/t\)，其余值一。§9的实际路径扩展给全部新增叶值一，证明 (10.2)。

这条下界量化全部 states、全部 partial bundles；不假定 helper 预先被绑在某枚停车资源。固定 \(\epsilon>0\) 后取 \(t>1/\epsilon\)，同一 \(R_{\rm cons}\) 点仍可行而 \(V(Q_t)<\epsilon\)。所以连完整 global matching 流、每 state perspective matching 流及全菜单共同叶边边际，也不能推出任何统一正的实际 \(V\)，或相对其 unit 证书阈值统一次二的排程界。

## 11. 完整原任务、明确规模、证据与仍开放的共同选择

上述达到分配给一份完整普通 UM 调度：每个原 selector 放在实际选择的 indexed-state private root；仅导出该 state 所领取正资源的 incidence jobs；所有其他原 incidence jobs——尤其**全部未选 states 的 jobs**——留各自 private roots。未选 roots 负载一；selected core root 负载为二减所领值；selected path-leaf root 负载一；每 resource machine 至多接一枚 unit job。故最高负载恰 \(2-1/t\)，每原 job 恰执行一次。反向若峰值 \(C<2\)，resource 端至多一枚 unit job，每个被 selector 选中 root 必导出至少 \(2-C\) 正质量；读这些实际正 exports 得原菜单不交分配，故 (10.2) 的值上界也是对所有完整普通排程的下界。

显式零 incidence 始终可放在其 private 零端；任意新调度中的额外零 exports 或未选态 exports 只占更多 resource 容量，不能削弱以上下界。追加的 unused 机器可为空，重复 indexed states 仍有各自原 jobs/root。所有这些数据均可保留，不能从“分配时忽略零值”写成“从矩阵删除零 job”。

对零 incidence 为空的明确基础族，记

\[
K=1+D^2,\quad S_C=D+2D^2,\quad
P_0=D^2(t+2),\quad L_0=D^2+Dt(D-1).
\tag{11.1}
\]

其中 \(K\) 为旧 cores 数，\(S_C\) 为 core indexed states 数，\(P_0\) 为新 ports 数，\(L_0\) 为新叶数。\(Q_t\) 共 \(K+L_0\) 组、\(S_C+2L_0\) states、\(I=P_0+2L_0\) 个 positive incidences。完整普通矩阵有

\[
\#\mathrm{machines}=S_C+2L_0+P_0,\qquad
\#\mathrm{jobs}=K+L_0+I,
\tag{11.2}
\]

及 \(S_C+2L_0+2I\) 个有限资格；稠密输入另列全部 \(\infty\)。每 port 有一个正 core 邻居及至多两个路径叶邻居；在本族每 core port 恰出现在一个 core state，因此 positive indexed-state incidence 度也至多三。这里没有额外声称每个 core 至多三 states。\(t=2\) 时为 17 cores、40 leaves、64 resources、116 indexed states、144 positive incidences，即 180 台普通机器、201 枚原 jobs，精确 \(V=1/2\)、\(\mathrm{OPT}=3/2\)；不主张这是所有反例中的最小实例。

基础正数据规模为 \(O(t^5\operatorname{polylog}t)\)，稠密矩阵也在 \(t\) 上多项式；不是仅按 binary \(t\) 的 \(\operatorname{poly}(\log t)\) 免费展开。一般 \(D_+\) 的 ports/leaves 数受显式 distinct positive group-resource incidences 及 unused 资源数控制。运输的 row/column 量只作有理加减，每次贪心至少清空一个余行或余列；(9.5) 仅作有理权求和。给定 basic 点后输出全部流的时间、支持和分子分母位长均按显式输入及该点总位长多项式，不按概率、\(p\)、\(1/V\) 的数值倒数复制。强化合同增加的 (MC) 全是 \(0,\pm1\) 系数等式。

软件证据只按新审查及冻结运行的实际范围登记。root 已实际读、独立重跑两套独立 checker；弱合同与强 (MC) 合同的实际覆盖须逐套列明，旧弱程序输出不自动成为强化审计。原作者脚本及有限统计仅保留其历史来源身份，不在本 Claim 中转记为 root 验证，也不把停车约化核称作完整矩阵 assignments 的独立优化 oracle。新 Exact v3、运输作者 Proof、新增章及两套独立 checker 的冻结、读取和重放记录均独立于前七节旧记录；尚未实际完成的 v3 (MC) 重放或最终正文实读步骤不得提前记为通过。

新 gap 只否定从所定义必要 relaxation 的可行性本身作统一正质量提取。它不是实际 YES 的反例，不给 NP-hardness，不否定相对 actual OPT 的一般近似，也不排除对多个 cores 同时条件化价值与容量、共有完整 matching law、更高阶信息或其他输入下界。缺口是多个 core 选择与叶资源的共同可实现性，不能用每个 core 菜单平均到同一叶边边际来替代。主目标 `UM-TARGET-v1` 仍 OPEN。
