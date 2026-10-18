# Full-support LP 保持与 bounded-row SC degree3 配置间隙：Exact v2

ID/version：`UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v2`。

作者 rainbow，2026-10-18。本版另立：v1最终SC item-degree≤9强化为≤3，新增SC层path的精确实际/CONFIG阈值合同；v1 Exact/Proof原字节不改。只在 clone 外冻结，不改repo / Work / Git。本文件不含作者证明策略，先仅root收取，不直接发送正在审v1的reviewer。

## 1. v1共同对象与已冻结合同

v1 Exact `normalized_menu_full_support_lp_preservation_exact_v1.md`（SHA256 `9fd644392d624431050d0d1489bea4464284a1594f7868bf4a3667641233a763`）作为本版明确Exact依赖，其全部normalized菜单、binary-tree、menu-level port-path与state-dummy构造原样保留，不换输入域。

简记：每group非空显式states，每state不同资源、非负有理权总和1，正support P_gs={u:p_gsu>0}。FSLP为λ≥0、每group Σ_sλ_gs=1、每resource Σ_{g,s:u∈P_gs}λ_gs≤1，系数是support指示而非p。0权原UM jobs依旧保留，FSLP只忽略它们的0值。实际partial allocation值V∈[0,1]。

既有N=D∘T normalform使每group≤3states、每resource跨≤3groups，精确保实际V/完整UMOPT。新v1合同为FSLP在T、D、N上双向可行证书保持；state-dummy SC(Q)每state一agent，每旧resource一real item，每group K_g−1个own dummy items，各对本组agents价值1，real value为原p。它满足实际SCOPT=V(Q)，FSLP(Q)⇔SCCONFIG(1)，且此SC像的CONFIG最高阈值≤1。

这些v1合同不在本版静默改写，新增步骤只发生在完成SC像之后。

## 2. 新SC层路径：任意有限非负additive SC的明示构造

给非空显式old agents集I、显式items集U（允许空）、所有有限非负二进制有理估值v_iu。0是实际0价值，不是∞资格；每item被正估值agent集合Γ(u)={i:v_iu>0}，按固定顺序列为i_1,...,i_d。

构造P_SC(old)：

- 若d≥1，用d个不同item copies z_{u,1},...,z_{u,d}替换u；旧agent i_j仅对自己的copy z_{u,j}取值v_i_ju，对该u其余copies取值0。其它old agents对此u所有copies价值0。
- 对j=1,...,d−1新增一个不同helper agent h_{u,j}，仅对相邻items z_{u,j}、z_{u,j+1}取值1，对其它全部items价值0。
- d1只有一个copy，无helper；d0把u保留为一个unused item，所有agents价值0，无helper。

不同u的copies/helpers互异。全部old agents保留，每个old positive valuation逐项迁到自己的copy，原0项不生成额外copy或正值；新增helpers只有两项unit价值。没有其它agents、items或估值。每份allocation仍要求每item至多给一个agent，不能把copies合并成可拆价值。

构造不输入OPT、实际assignment或CONFIG阈值；固定参数1是helper估值本身。

## 3. 新步骤的实际阈值与0端点合同

对任意上述old additive SC、任意v∈(0,1]：old存在实际minutility≥v的allocation，当且仅当P_SC(old)存在这样的allocation；给实际allocation两向转换均确定性总位多项式。

更强逆向：对任意v>0，给P_SC(old)一个实际minutility≥v allocation，可投影为old实际minutility≥v allocation；前向仅在v≤1保证，因为helper只有unit singleton可用。

因此，若old实际OPT≤1，则

    OPT(P_SC(old))=OPT(old)，

包括oldOPT=0。0端点由正阈值等价补足，不将“helper必须领正值item”的论证在v0时误用。若oldOPT>1，当前版不声称实际最优值保持，也不把前向阈值越过1。

每个old agent全部正价值总和精确不变，新helper的正价值总和为2；每new item被正估值agent数≤3（一个old agent及至多两个相邻helpers），unused item为0。

## 4. 新步骤的有限SC CONFIG证书与阈值

SC CONFIG(t)定义沿v1：每agent配置总权1，配置内总价值≥t，每item总边际≤1；允许unused items，给定证书是显式有限有理配置列表。以下转换可删配置中的0价值items，但不能删任何agent。

- 前向：对每个0<t≤1，若old CONFIG(t)可行，则P_SC(old) CONFIG(t)可行；给old显式有限有理证书，可确定性总位多项式输出目标证书，新增helper配置可仅用unit singletons。
- 逆向：对每个t>0，若P_SC(old) CONFIG(t)可行，则old CONFIG(t)可行；给目标显式有限有理证书，可确定性总位多项式输出old证书。Helper配置可含一或两个相邻copies，不假定恰一个；各old agent先删所有0值copies，避免合回同一个old item时错误合并多个正份。

因此，若old的CONFIG最优阈值≤1，则新旧CONFIG最优阈值相等；包括0时不按空helper配置假推正值。t=0不在上述非平凡证书投影合同量词，两个实例的CONFIG0都可另外用空配置平凡实现。

注意这是一项SC CONFIG的精确阈值合同，不是一般UM CONFIG保持，不把给定有限证书转换写成求未知配置点的算法。

## 5. v2最终应用：row≤3 / item degree≤3的无界CONFIG gap

对v1全部normalized菜单Q，令

    J(Q)=P_SC(SC(N(Q)))。

其old SC像的实际OPT与CONFIG最高阈值都≤1，所以第3–4节可用于精确保实际V与CONFIG(1)可行性；最终每agent正价值总和≤3（old≤3、helper2），每item正欲望agent数≤3。

仍采用v1的显式标准gap重表达Q_D（D≥2）：一个main group的D个states分别为D个不同g_{a,j}各权1/D；每(a,j)helper group两singleton choices g_{a,j}或A_a，权1。v1的V(Q_D)=1/D、FSLP可行，例子本身扣除既有selector/parking配置间隙思想，不称原创source。

则J_D=J(Q_D)为显式有限additive SC，全部正价值仍仅1与1/D，并满足

    rowtotal≤3，item positive-degree≤3，
    CONFIG最优值=1，实际OPT=1/D。

其CONFIG(1)有显式有限有理多项式支持证书，agents/items/完整dense编码均poly(D)。本版精确强化v1最终degree9到3，v1结果仍真且原件保留。

这只否定该精确结构类中“CONFIG(1)可行即可实际保某个统一c>0”的保证；这些都是actualOPT=1/D的NO实例，不是否定承诺actualOPT≥1时输出常数值的det-bit-poly算法。没有NP/ETH/UGC等hardness结论或一般SC归约。

## 6. 显式规模、归属与剩余问题

对一般SC新步骤，令E_+为old正估值条目数、m_0为unused items数。新增helper数h=Σ_u(d_u−1)_+≤E_+，new items数≤E_++m_0；保留所有old agents，新agents数|I|+h，old正估值逐项保留且helper只添2h项。完整dense矩阵乘积仍多项式。

给定有限CONFIG证书的items重命名、支持删0、有限有理求和及新增helper权重按输入与证书总位长多项式。没有按d之外的数值参数、估值倒数、分母或二进制D生成隐式多对象；D族本来显式有Ω(D²)规模，不承诺poly(logD)输出。

该SC路径就是BCG2009 §2.2/Theorem2.4/Fig2的标准相邻dummy装置在目标≤1下使用unit值的直接重构。原agents行总值并不被它缩小；这里只因进入此步的old SC已row≤3，才保最终row≤3。新增合同是给定有限CONFIG的双向、阈值域、0/unused与完整actual价值保持，不冒称新degree-three思想或全局新颖性。

v1全部证书保持与actual定义依赖不变；本版没有软件或有限枚举替代一般证明。外审、全球新颖性未认证。actualYES OPT≥1的常数promise finder在row≤3、degree≤3（故也原degree≤9问题）上仍未解决；一般UM主目标仍OPEN。
