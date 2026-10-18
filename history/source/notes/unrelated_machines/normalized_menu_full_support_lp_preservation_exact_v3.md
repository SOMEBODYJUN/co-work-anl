# Normalized flat CONFIG、FSLP 与 bounded-row SC 的成熟证书合同：Exact v3

ID/version：`UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v3`。

作者 rainbow，2026-10-18。本文件为完整 statement-only 最终合同，新增 restricted-flat UM CONFIG(1) 精确桥，合并v2的SC层path；不含作者Proof或证明策略。仅clone外scratch，未改repo / Work / Git，不直接发正在仅读v1 Exact的reviewer。

v1 Exact/Proof与v2 Exact均保原字节，分别SHA：`9fd644392d624431050d0d1489bea4464284a1594f7868bf4a3667641233a763`、`7f8bd074a0f137dd4c75260fd7c8bd4023bcd24d5bd96042b56b46c552e47740`、`0176af114d1323cb963c98481533a41d35d50d6bd5f81c5dd10094ffd27c9c8b`。旧来源是冻结过程，不据此假称每个中间版本已有独立审查/登记。

## 1. 完整 normalized flat 原对象、actual值与FSLP

非空显式groups G，每group有有限非空indexed states S_g，全部resources U显式。每state对不同resources给非负二进制有理p_gsu，总和恰1；允许0项、重复indexed states、unused resources，不允许同state同resource重复项。各state完整正support P_gs={u:p_gsu>0}非空。

完整普通UM P(Q)：每state一个不同private机器M_gs，每resource一台不同R_u；每group一枚unit selector J_g，仅可在该group任一private机时间1；每个原incidence(g,s,u)一枚不同原job，仅可在M_gs耗p_gsu，或R_u耗1；其余∞。全部未选state jobs及0权原jobs都保留，不能从实际输入删去。

实际one-state partial allocation值V(Q)∈[0,1]：每group选一个indexed state及该state资源子集，各group所领资源全局不交，最大化最小private质量。已存actual合同为OPT_UM(P(Q))=2−V(Q)，含V0 / OPT2。

Full-positive-support state LP（FSLP）定义为

    λ_gs≥0，Σ_sλ_gs=1（每g）；
    Σ_{g,s:u∈P_gs}λ_gs≤1（每u）。

系数是正support的0/1指示，非p值；0权真实incidence仅在这个分数证书层不占资源。LP显式多项式大小，不把λ当实际allocation。

## 2. 新增 restricted-flat machine CONFIG(1) 精确桥

对完整原P(Q)，machine CONFIG(1)要求每machine给其合法jobs子集（实际总处理时间≤1）非负配置权、权和1，每原job覆盖至少1；允许empty configuration。与逐job精确覆盖1版本按向下封闭等价；下面转换均能给明确有限有理证书，不丢0权原jobs。

**Exact Statement。** 对任意第1节完整normalized flat Q：

    UM machine CONFIG(1)可行 ⇔ FSLP(Q)可行。

给任一方的显式有限有理可行证书，可确定性总位多项式转换为另一方证书。FSLP正向可输出全部原machine与每枚原job精确覆盖1的配置证书；unused resources、zero incidences、duplicate states均包含。

这是阈值**恰1**、上述完整restricted-flat矩阵的结论，不声称一般UM CONFIG保持、任意T的CONFIG最优值保持、或保给定证书的全部边际。没有将实际OPT或SAT见证当输入。

## 3. Binary-tree / menu-path normalform与FSLP双向保持

Tree T：每原group的K_g个indexed states为full binary tree叶，K1即root单叶。每顶点一个newgroup；每非root v有fresh own-resource a_v。Root internal菜单为两个child own-singletons；非root internal为own singleton及两个child singletons；非root leaf为own singleton及旧完整state；root leaf仅旧state。新singletons权1，旧权与全部0项不变，各state仍normalized。

Menu path D：对资源u列全部menus（含0项）中distinct incident groups g_1,...,g_d。d≥1时用ports z_1,...,z_d替u，每旧group的所有u incidences统一改至本group对应port；新增d−1个helpergroups，第j个恰两个singleton states z_j或z_{j+1}，权1。d1无helper，d0保留unused资源。

N=D∘T是既有完整flat normalform，每group≤3states、每resource跨全部states≤3groups，精确保actual V与完整UMOPT含端点；其新增分数合同为：FSLP在原、T、N之间双向可行性等价，给任意一边显式有理证书均可总位多项式转换。单独D亦双向保持FSLP。

结合§2可得：P(Q)与P(T(Q))、P(N(Q))的machine CONFIG(1)可行性同样等价，并可转换**完整原任务**的有限有理证书。这仍只unit阈值，不额外宣称非flat或任意尺度CONFIG结论。

## 4. State-dummy SC与FSLP / CONFIG(1) 精确桥

SC(Q)：每state一agent a_gs；每原resource u一real item，其价值为p_gsu（缺项0）；每group K_g−1个不同dummy items，每个对本组全部stateagents价值1，对其它agents0。没有其它agents/items/value。

每agent全部正价值总和恰K_g，实际SCOPT=V(Q)（已存actual state-dummy合同，含0），CONFIG最高阈值≤1。SC CONFIG(t)为每agent价值≥t的item子集配置权和1，每item跨agents的总边际≤1；允许unused items，给定证书为显式有限有理列表。

**Exact Statement。**

    FSLP(Q)可行 ⇔ SC(Q) CONFIG(1)可行。

给显式有限有理证书两向总位多项式转换；正向配置支持多项式。0价值items可从SC配置删去，但不删agent。若FSLP可行，该SC CONFIG最优值恰1。

所以当前三个分数对象在上述严格域/阈值有同一可行性：完整flat UM machine CONFIG(1)、FSLP、state-dummy SC CONFIG(1)。三者对象仍不同，不把一般SC行免费归一化。

## 5. SC层path：新旧完整对象与精确阈值

对任意非空有限old agents、有限items（可空）、有限非负有理additive估值v_iu，按正估值Γ(u)列i_1,...,i_d。d≥1时把u替为d个不同copies z_{u,j}；old agent i_j只对自己的copy取原v_i_ju，其余copies价值0。加入d−1个不同helperagents，第j个只对相邻z_{u,j}、z_{u,j+1}各取值1。d1无helper，d0保留u为unused全0item。原0值不生成正copy/新helper资格，没有其它agents/items/价值。记该SC转换为P_SC。

其精确合同为：

- Actual前向：每0<v≤1，old allocation minutility≥v可映为new actual≥v；实际逆向对每v>0成立。若old实际OPT≤1，新旧实际OPT相等，含0端点；oldOPT>1不声称最优值保持。
- CONFIG前向：每0<t≤1，old有限有理CONFIG(t)可映为new证书；CONFIG逆向对每t>0成立。若old CONFIG最优阈值≤1，新旧CONFIG最优阈值相等，含0端点。t0不在非平凡投影合同内，两边可另以empty configurations实现。
- 以上给定allocation /有限证书的转换均det-bit-poly；helpers配置可能含一或两copies，不能逆向偷假设恰一；oldagent配置先删0值copies，避免同old item多份正值误合并。
- 每oldagent rowtotal精确不变，newhelper rowtotal2；每newitem positive-degree≤3，unused为0。

此步骤构造不输入OPT或阈值，只有helper估值固定1。它是标准BCG2009 adjacent dummy路径的有限unit目标重构，不是新的degree-three思想。

## 6. 最终typed composition与配置间隙应用

令J(Q)=P_SC(SC(N(Q)))。Old SC像actualOPT与CONFIG最高阈值均≤1，故§5精确保其actual值与CONFIG(1)可行性；最终rowtotal≤3，item positive-degree≤3。全部actual oldagent与helper都必须有值，0/unused端点按上述合同处理。

用显式D≥2的旧selector/parking gap模式Q_D作应用：资源g_{a,j}、A_a全异；一个main group的D个states，第a state为D个g_{a,j}各权1/D；每(a,j)helper group两singleton states g_{a,j}或A_a，权1。它满足V(Q_D)=1/D、FSLP可行。例子及gap思想明确扣除既有selector/重轻资源与uniform parking，不主张新hardness。

最终J_D=J(Q_D)有：

    所有positive values仅1/D与1；
    每agent全部positive value总和≤3；
    每item positive-degree≤3（故也≤9）；
    SC CONFIG最优值=1，实际SCOPT=1/D。

并有显式有限有理poly(D)支持CONFIG证书、poly(D) agents/items/dense编码。相应flat normalform machine CONFIG(1)亦可行，实际UM值2−1/D；这正是旧配置间隙在限定证书合同下的转述，不是新的源gap。

因此CONFIG(1)可行本身不能在该精确bounded-row/degree类保任何统一实际正常数。**不能**由这一系列actual NO推出承诺actualOPT≥1时不存在常数promise算法，也不宣布一般SC / UM困难性。

## 7. 显式总位复杂度与边界

原Q有n groups、S states、I incidences；T有2S−n groups、5S−4n states、I+4S−4n incidences，K1按定义无新增own资源；D helper数至多中间incidences数。所有flat实际jobs/machines和dense矩阵仍多项式。

SC state-dummy agents为state数，items为real resources及Σ(K_g−1)dummies；SC path的old正条目数E_+给新增helpers≤E_+、newitems≤E_++unused数，dense乘积多项式。给定有限配置列表的支持转换按其实际长度计，不承诺取得未知指数证书。所有有理部分和/缩减/整数容量/配置修剪按总位长多项式，不按分母、1/p或隐式D生成objects。D族本来Ω(D²)显式规模，不声称poly(logD)输出。

完整flat的selector、全部未选states、0权原incidence与unused machines均不得省；SC 0值items可删出配置仅因价值0，这不是删除原UM任务。Group/source空不在本normalized非空域，SC path保oldagent非空以使minutility定义明确。

## 8. 归属、实际核查与剩余问题

已实际读取current normalform/SC桥与CLAIMS对应ID，先前actual合同本身未登记本fractional保持；新增独立合同应以本v3统一叙述，不给v1/v2过程稿重复资产地位。标准selector-tree、BCG路径、state-dummy与旧gap例明确扣除，全球新颖性/外审未认证，无新软件或有限实验代替证明。

BCG路径保原agent每条旧估值，故不把无界原row降至3；这里先经normalized-menu像才得到old row≤3，再保到最终。一般SC degree3等价因此不能被误套为一般SC到此bounded-row源的归约，degree2 VW亦未调用。

真正剩余问题仍是：rowtotal≤3、item-degree≤3（或原≤9）且实际OPT≥1时，是否能det-bit-poly找某个固定c>0的实际allocation。当前CONFIG反例只关闭LP充分性，不解该promise finder，也不解真实near-2源或一般UM主目标。
