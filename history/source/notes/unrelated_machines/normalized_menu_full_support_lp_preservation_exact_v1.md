# 归一化菜单正规形与 SC 的 full-support 分数证书保持：Exact v1

ID/version：`UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v1`。

作者 rainbow，2026-10-18。本文件只冻结完整对象、转换及精确量词结论，不含作者证明，供 Exact-only 独立审查。仅 clone 外 scratch；不修改 repo / Work / Git。主增量是已存 normalform / SC 桥对下述分数证书的保持合同，不把旧 selector / parking 配置间隙再包装成新的困难性源。

## 1. 原 normalized flat 对象与明确的 full-positive-support LP

输入非空显式 groups G，每组有限非空 indexed states S_g；资源 U 显式。每 state (g,s) 给不同资源的有限表及非负二进制有理权 p_gsu，满足 Σ_u p_gsu=1。允许0项、重复 indexed states、unused resources；不存在同 state 同资源重复项。所有 states / incidences 均为真实原输入，不隐式枚举指数多菜单。

令 P_gs={u:p_gsu>0}。Full-positive-support state LP，简称 FSLP，为

    λ_gs≥0，Σ_s λ_gs=1（每g）；
    Σ_{g,s:u∈P_gs} λ_gs≤1（每u）。

这里资源系数是正 support 的0/1指示，**不是**private权 p_gsu；零权原 jobs 仍保留在完整 flat UM 与其实际调度内，但不占本 LP 的正 support。W=1保证每 P_gs 非空。

实际 partial allocation 值 V 是：给每组一个 indexed state s_g 及其正权资源子集 B_g，两两不交，最大化 min_g Σ_{u∈B_g}p_gs_gu。可分配后丢弃零值项，不改变 V；0≤V≤1。对应完整 flat ordinary UM 沿用已存定义：每state一private机，每group一个unit selector，每incidence一原 job，private时间p、其资源端时间1，全部未选state jobs也保留；actual OPT_UM=2−V。

FSLP是一个多项式大小显式有理 LP，不是一般SC CONFIG或UM CONFIG的同义词。给定 λ 证书时，以下转换按其真实输入位长计；有理LP求可行点是标准显式LP步骤，不要求求实际 V 或源assignment。

## 2. 已存 binary selector-tree 与 port-path 的精确输入输出

Binary-tree 转换 T：每原 group g 的 indexed states 是一棵显式 full binary tree 的叶，K_g=1则根即叶。每顶点v建一个新group；每非root有fresh own-resource a_v。完整 normalized 菜单为：

| 顶点 | 菜单 |
| --- | --- |
| internal root | 左、右 child own-resource 的两个singleton states，权1 |
| 非root internal | own singleton与两个child singletons，共3states，权1 |
| 非root leaf，对应旧s | own singleton与旧完整state（含全部0项），共2states |
| root即单叶 | 仅旧完整state |

这就是已存 `UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1` 的第一步，不改变旧 p 或其原实际 job 身份。新singletons均是实际完整flat state，并按通常selector/incidence规则生成真实jobs。

Port-path 转换 D：对任意资源u，按其全部菜单（**含0项**）中的 distinct incident groups 列为 g_1,...,g_d。d≥1时用ports z_1,...,z_d替换该资源，同一旧group的所有states内该u都重定向其同一个port。增加d−1个helpers，第j个helper有两个singleton states：z_j权1或z_{j+1}权1。d=1无helper，d=0旧unused资源保留。所有helpers也按完整flat规则生成真实selector/private/incidence jobs。

组合 N=D∘T 正是已存正规形：每group至多3states，每资源跨全部states至多3groups，仍W=1。旧actual partial V与完整UM OPT均精确保持，包括V0 / OPT2，依赖既有正规形actual合同，不在此偷偷改域为未归一化SC行。

**新分数保持结论。** 对任意上述 normalized 输入：FSLP在原对象、T对象、N对象上的可行性等价。给任何一边的显式有理可行证书，可确定性总位多项式转换为另一边的显式有理可行证书。单独D转换也双向保持FSLP，含zero incidences、unused resources、d0/d1及重复indexed states。

没有声称一般UM CONFIG由这两步保持；此处只定义并证明这个精确FSLP合同。

## 3. state-dummy SC 对象、实际值与 CONFIG(1)

对任意 normalized 菜单 Q 建 additive Santa Claus 实例 SC(Q)：每state一个agent a_gs；每原资源u一个real item，该agent对u的价值为p_gsu（缺项为0）；每group新增K_g−1个不同dummy items，每件对本组全部stateagents价值1、对其它agent价值0。没有其它agents/items/价值。

每agent的全部正价值总和精确为

    1+(K_g−1)=K_g。

实际SC minutility最优值等于 V(Q)，包括0端点。这是已存 `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1` 的完整实际合同，不假设已给目标OPT或将一般SC高总值行免费归一化。

定义 SC CONFIG(1)：对每agent，给其总价值≥1的item子集非负配置权，权和1；每item在全部agents配置中的总边际≤1。Items允许不使用，任务不可拆分的实际分配与该分数对象区分。可把配置中0价值items删去。

**新精确分数桥。** FSLP(Q)可行当且仅当SC(Q)的CONFIG(1)可行；给显式有限有理证书时两向均能确定性总位多项式转换。由FSLP生成的CONFIG证书每agent只需正real support配置及本组singleton dummy配置，支持总数多项式。

此外，SC(Q)的CONFIG最优阈值总是≤1；因此若FSLP可行，其CONFIG最优值恰1。实际SCOPT≤1也由既有值桥保持，不把CONFIG1当作实际YES witness。

## 4. 最终行总值≤3 / item度≤9 的强类型

对N(Q)的SC像：每agent正价值总和 K_g≤3。每real item只属于至多3个groups的全部menus，每组至多3states，因此它有正价值的agent数≤9；每dummy item正价值agent数≤3。所有正价值≤1，允许零条目。

所以，对任意输入Q，若FSLP(Q)可行，则SC(N(Q))在CONFIG(1)可行，实际OPT等于V(Q)，同时满足rowtotal≤3、item positive-degree≤9。以上是确定性显式位多项式转换；没有使用degree2 VW算法。

BCG2009 §2.2/Theorem2.4的degree-three路径装置只重分配原item副本；每个原agent的原全部价值原样保留，故一般情况下不会把原rowtotal降至3。其∞dummy裁到目标1后rowtotal2不解决原agent总值。这一已实际核读的来源条件不能被误用为一般SC到当前bounded-row域的归约。

## 5. 已有间隙模式的显式应用：CONFIG方向不能保常数

对任意显式整数D≥2，定义 normalized 菜单 Q_D：资源g_{a,j}（a,j∈[D]）及A_a（a∈[D]），全部不同。

- 一个main group，有D个states。第a个state包含g_{a,1},...,g_{a,D}，各权1/D。
- 每(a,j)另一个helper group，有两个singleton states：g_{a,j}权1，或A_a权1。

以上是全部groups/states/resources/权，均显式。该例是标准selector/重—轻资源与既有uniform parking配置间隙模式的重表达；不主张例子或CONFIG gap思想原创。它有

    V(Q_D)=1/D，FSLP(Q_D)可行。

把它经上述既有normalform与SC桥，得到明确实例 I_D=SC(N(Q_D))，满足

    每agent正价值总和≤3，
    每item被正估值的agent数≤9，
    CONFIG最优值=1，实际SCOPT=1/D。

所有正价值仅为1和1/D。实例有poly(D)个显式agents/items、dense总位编码亦poly(D)；并附多项式支持的有理CONFIG1证书。D按显式规模参数计，不声称poly(log D)输出Ω(D²)对象。

因此，该bounded-row / bounded-degree类上CONFIG(1)可行**不能**保证任何与D无关的实际minutility正常数；CONFIG积分间隙无界。不能把这一系列NO实例当作“OPT≥1的promise算法不存在”：本Claim没有复杂度hardness，没有给任何实际YES/NO计算gap，也没有否定从真实YES结构或更强证书找常数值的算法。

## 6. 规模、证书位长与准确剩余问题

原输入 n groups、S states、I incidences。T转换有2S−n groups、5S−4n states，保留全部I原incidences并新增4S−4n singleton incidences；K1边界按表直接保留。之后D路径helper数至多中间incidence数，全部ports、state与实际UMjobs及dense矩阵均多项式。SC agents为最终state数，real items为最终resources，dummy数为Σ(K_g−1)，正价值条目及dense估值矩阵也多项式。

给定λ、normalform及SC CONFIG证书的转换仅做显式有理部分和、缩减、容量匹配/分配等标准有限操作，全部按输入/证书位长多项式；不按分母、1/p或1/V展开。一般SC CONFIG证书的逆向转换以实际给出的有限支持为输入，不承诺枚举所有配置或取得未知指数证书。

现行CLAIMS及normalform/SC桥正文已实际检索，未见本FSLP保持合同被登记；此前actual归约本身不自动证明分数保持，本Claim单列这一新合同。标准selector-tree、BCG路径、state-dummy与已有gap模式均明确扣除，全球新颖性与外审未认证，没有新软件或有限枚举代替证明。

真正仍未解：在此精确bounded-row≤3、item-degree≤9类上，是否有固定c>0的det-bit-poly算法，承诺实际OPT≥1时输出实际minutility≥c。当前CONFIG反例不决定这个问题；也没有一般UM或一般SC的算法/困难性升级。主真实near-2 source仍OPEN。
