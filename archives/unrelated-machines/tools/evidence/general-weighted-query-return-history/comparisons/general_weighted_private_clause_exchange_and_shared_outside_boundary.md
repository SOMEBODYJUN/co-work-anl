# 任意异权私有子句网络的三半交换与共享外端边界

读取目的：把[逐机统一时间交换](machine_uniform_query_return_index_exchange.md)扩至任意非负异权，再真正控制变量环的共同负载。这里给一整个私有子句模板的实际三半上界，限制新增辅助任务修复近二NO的路线；最后两个共享外端例子精确说明哪些接口没有被排除。新增假设、存在量词和给见证的算法量词分开，主目标仍OPEN。

## 1. 任意异权的完整私有外端接口

**ID / Version：`UM-GENERAL-WEIGHTED-QUERY-RETURN-THREE-HALVES-EXCHANGE-v1`。**

**Objects / Domain / Definitions / Quantifiers。** 给有限内部机器H、固定辅助原任务A、两族不同边界原任务Q={q_1,…,q_k},R={b_1,…,b_k}，k≥2，三族互异，T>0为二进制有理数。内部所有条目是任意非负有理或∞，允许同机异权、zero、有限时间>T和任意资格。每A任务至少有一内部有限端且只可在H执行；每边界任务z另有互异私有原机O_z，仅z可在其上耗时T。这是全部普通P，无其它资格、任务或预载。令N=|A|+2k；原机数|H|+2k，dense输入有(|H|+2k)N项。

模式X指定全部A及恰X中的边界任务在H，其余边界任务各去自己的原O_z。Inactive为X=R；aligned_i为X={q_i}∪(R\{b_i})；指定cross(j,i)为X={q_j}∪(R\{b_i})。

**Exact Statement / Conclusion。** 给同一P中两个不同索引i,j的完整actual aligned分配σ_i,σ_j，均峰≤T，可确定性总位多项式输出原P全部任务的一份实际分配，峰≤3T/2，并明确为inactive或指定cross(j,i)。每个输出内部端可仅取该原任务在两输入见证实际用过的内部端；所有A保留内部，所有原任务一次。

若inactive在≤3T/2不可行，输出必为指定cross。全部aligned的strict见证存在且inactive在3T/2被禁，则全部有序错配均存在；给全部k份实际见证时才承诺计算全部输出，不凭存在性搜索未知strict调度。任意B≥3T/2若禁止B内inactive，也无法同时要求所有aligned strict可选而B内只能同编号。

**证明与共同前提。** 只调用已有[双见证查询分离v2](two_witness_query_separation.md)的完整实际single-query与非query支持不交合同，不调用费用或§5计数。令A′=A∪(R\{b_i,b_j})。从σ_i删q_i得到A′+b_j的内部≤T分配；σ_j给A′+b_i+q_j内部≤T。

建立分析实例：原内部H上保这些任务的两见证已用端，任务为A′∪{b_i,b_j,q_j}；三特殊任务各有一台分析outside零端。ρ_0将A′+b_j内部、b_i和q_j各在零端；ρ_1将A′+b_i+q_j内部、b_j在零端。这是同一分析P的两份完整实际≤T分配。取两query为{b_i,q_j}，它们确在owner改变集，旧端均zero，故δ=0。已有定理给两个实际≤3T/2的single-query分配，其非query改派支持不交。

b_j是非query且只有它可从内部变到outside，至多被一个支持移出。因此至少一份single-query分配仍把b_j留原内部端。A′的两输入端均在H，全部留内部。选b_i的那份内部恰A∪R，选q_j那份恰A∪(R\{b_i})∪{q_j}，正是所需二选一。所有H机器在同一分配同时≤3T/2。

保留选中内部原端，把原P所有其余边界任务放各自真实O_z、耗时T，**包括分析P未列的q_i、其它Q及未内部化query**。每个原任务一次，分析zero端不输出；各原O_z只有自身一任务，外部同时≤T。因此原完整峰≤3T/2。交换i,j重做给反向，inactive禁用推论不需要算法判不可行性。

**Assumptions / Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 精确依赖UM-MODEL-v1、本节完整P、两实际见证及UM-TWO-WITNESS-QUERY-SEPARATION-v2；这是该定理直接结构推论，非新分离算法。只有内部两份已用有限端参与运算，zero不除零，∞不运算；分析规模≤N任务、|H|+3机器，有理和/比较与最终输出按显式总位长多项式，不按分母或T倒数展开。无给定见证时仅存在量词，不能隐藏一个一般调度求解器。H空时aligned前件不成立，A空合法。

真实共享outside若替代O_z，恢复可能累积负载，本节不保证外接；辅助可外送、多个query/return bundles也须另证。general先据Exact及旧依赖独立重构，冻结后才读作者Proof；root实际读各原件，独核两个证明路线。完整审查见[局部异权审查](../../reviews/unrelated_machines/general_weighted_query_return_exchange_review.md)。无软件、finite实验或外审/全球新颖性认证；严格负载T交换只在旧uniform域保留，不能把本节3T/2误写T。

## 2. 私有异权子句网络加真实变量环的全公式上界

**ID / Version：`UM-PRIVATE-CLAUSE-QUERY-RETURN-UNIVERSAL-THREE-HALVES-v1`。**

**Objects / Domain / Definitions / Quantifiers。** T>0有理，任意显式有限CNF，每clause c有k_c≥2枚实际occurrences，重复文字/变量允许，每occ只属一clause。只保出现变量，将各自occ排环，显式padding至≥3。含dummy总N、真实总L、dummy数d=N−L；最少padding N≤L+2v，额外长padding按实际表收费。空公式输出一idle机零任务，OPT0。

非空时每索引有原ring机M_i及原任务q_i,b_i。每clause另给内部H_c及辅助A_c；各H_c互异且与ring及dummy私有机分离，各A_c互异且只可在自身H_c执行。真实i∈c的q_i,b_i在H_c所有时间/资格任意非负有理或∞。q_i外部端**恰**M_i与M_(i⁺)，两端时间各在[0,T]；b_i唯一外端为pin(i)，时间在[0,T]，正literal pin=M_i、负literal pin=M_(i⁺)。Dummy q只有两个ring端[0,T]，dummy b仅其互异私有机D_i:T，不返回ring。其它端∞，无其它原jobs/预载。任何实际clause需求任务必须明确包含在始终内部的A_c，不能在证明中删去。

给每c的每个真实i一份实际局部aligned证书λ_(c,i)，覆盖恰A_c+q_i+(R_c\{b_i})，全部H_c峰≤T，其中R_c是该clause的b任务集，**不是机器**。这些不是整个源P的全局strict调度，也不预设存在共同SAT赋值。

**Exact Statement / Conclusion。** 对全部上述输入及所给合法证书，无论源SAT/UNSAT、内部异权/zero或环次序如何，可确定性总位多项式输出原P全部2N+Σ|A_c|任务的共同实际分配τ，C_max≤3T/2。各H_c≤3T/2，每台真实ring机恰一原q或真实b、负载≤T，dummy D_i负载T。每clause或者inactive（全部b内部、全部q在ring），或者恰一query j内部、恰一return r在原pin，其余边界相反，可j=r或错配。

若只假设各λ存在而没有输入见证，仍有OPT≤3T/2的存在结论，不声称能计算未知strict证书。因而满足该准确模板的归约，即使另有YES≤T，也不能在NO声称OPT>(2−δ)T、δ<1/2。

## 3. 局部模式库、共同匹配与完整实际回填

对每clause将各λ补私有测试outside:T，满足§1的局部定理条件；测试端只为调用，不是实际P的原机。按固定次序遍历全部有序不同(i,j)，实际运行§1二选一：若有一次返回inactive，称该clause baseline并保存其H_c实际内部调度；否则称active，已实际存下全部cross(j,i)内部调度，diagonal另用输入λ。Active分类不主张inactive真的不可行，算法没有使用任何一般异权可行性oracle。k_c≥2保证有待运行的不同对。

现在另为**真实ring共同负载**构造二部匹配。左侧为全部原q_i,b_i及每active c一分析label w_c；右侧为全部真实M_i、每索引一分析label K_i及每active一V_c。两边均2N+h。边：q_i→两个ring端，active真实q还→V_c；真实b_i→pin(i),K_i，dummy b仅→K_i；w_c→本clause所有K_i。没有q→K边。w,K,V都不是实际执行的任务或机器。

Active i∈c取θ_i=1/k_c≤1/2，其余θ_i=0。每q两个ring端先各给matching质量1/2，active时从其pin端扣θ并加到V；真实b给pin质量θ、K质量1−θ，dummy b给K质量1；w_c给各本clause K质量θ。各行和1；每M被q扣的质量被同编号b补回，列和1；每active K为1−θ+θ，其余K为1；每V收Σθ=1。全局同一个fractional perfect matching的Hall整数性给一个共同perfect matching，质量不是原处理时间。

每真实M恰一q或b，dummy b不进ring。Baseline/dummy K唯一邻居是其b，故b匹配K、q必用ring；每active V恰选一q_j，w恰占一个K_r迫该b_r返回pin，其余b匹配K。由此每active恰一query/return，所有返回pins与剩余q的环端已共同协调，不能按子句分别选局部见证拼接。

实际回填时，baseline H_c用已存inactive；active H_c用已存(j,r)模式。每个匹配ring端的q/b在该原端按真实时间≤T执行，dummy b去原D_i:T。每A_c一直在其H_c，每真实q/b恰内部或ring二者之一，dummy两任务各一次；全部原jobs覆盖，无任何测试outside、分析K/V/w遗留在输出。H_c互异使已存内部实际≤3T/2能同时成立；ring每机一实际任务给≤T，D_i为T。因此完整全机峰≤3T/2，关闭本模板的真实外部负载义务。

**Assumptions / Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 共同前提为UM-MODEL-v1、§2全部实际矩阵与每索引局部strict证书、§1异权交换；再直接重构标准保护环共同matching。原P机器N+H+d、jobs2N+a、finite条目3N+E_int，dense(N+H+d)(2N+a)；局部交换至多Σk_c(k_c−1)≤L²次，模式库/分析图与全部输出多项式。所有参数按二进制有理和显式证书收费，不按分母、时间倒数、隐式padding展开。

本结论不覆盖辅助跨网络外送、真实内部机/任务跨clauses共享、非全索引strict可选、其它外部资格或多个query/return bundles。单纯新增资格保留旧三半分配，不能移除它；新增guard若仍有固定clause归属且保局部证书，就纳入相应A_c继续受界。具体source要退出此模板须给真实改变的共同容量/身份合同，本页不证明这些改变充分。也不从外端near-unit自动宣布任意接口strict SAT解码。fee先仅据Exact、局部交换Exact及旧查询定理独立重构，之后才读作者Proof；root实际亲核所有原jobs及匹配回填。见[全模板审查](../../reviews/unrelated_machines/private_clause_query_return_universal_review.md)。数学技巧已扣除标准来源；无软件、外审、全球新颖性或near2主目标反面认证。

## 4. 共享外端不能免费私有化：四任务边界对照

这是标准matching环的完整反例，不另立新研究Claim。给0<ε<1有理，内部H,I、真实共享外部E_1,E_2，四原任务仅有q_i:H:1/E_i:1，b_1:I:1/E_1:1，b_2:I:1−ε/E_2:1，余端∞。

两aligned完整分配(q_1H,b_2I,q_2E_2,b_1E_1)及其反向均峰1，故OPT1。若完整C<2−ε，四台机每台至多一原任务：各自唯二任务总时间为2、2−ε、2、2。四任务迫四机各一，资格环恰两perfect matchings，正是两aligned；覆盖所有其它partial模式。Inactive的两个b在I给精确2−ε，cross在某E_i两unit给2。临界C=2−ε还会接纳inactive及各一个query加全部b内部的三种assignment，不能把严格不等号改闭。

任意δ∈(0,1)有理取ε=δ/3，B=2−δ<2−ε，便有near2模式排除且位长O(bitlenδ)，四机四任务八finite固定。它只说明真实共享outside会阻断局部交换的完整延伸，不提供可供clause读取的状态：两strict见证每机都有一件，presence相同；ε=0的unit环已有该机制。新增资格/其它jobs/外机合并都须重证，不能借这个OPT1常数模块声称源困难性。作者Exact、bicriteria先行16模式重构、作者Proof实际读后及最终边界审查均按原件保存；无一般外接或全球新颖性认证。

## 5. 小查询与共享返回池的精确多查询关系

**ID / Version：`UM-SHARED-OUTSIDE-SMALL-QUERY-RETURN-POOL-EXACT-RELATION-v1`。**

**Objects / Domain / Definitions / Quantifiers / Assumptions。** 任意k≥2，显式正有理a_i且Σa_i≤1；内部机H及P_1,…,P_(k−1)，外部机E_1,…,E_k，全2k台互异。仅有2k件原q_i,b_i；q_i仅H:a_i或E_i:1，b_i仅任意P_r:1或E_i:1，余端∞，无aux/预载。E_i由同编号q_i,b_i真实共享。任意S,T⊆[k]规定q在H索引恰S，b在E索引恰T，其余b自由选任意P_r；定义pattern OPT为这些完整分配的最小峰，不预设池机容量1。

**Exact Statement / Conclusion。** 对全部输入与任意S,T，pattern OPT恰1当∅≠T⊆S，否则恰2。因而任意1≤B<2的实际完整weak调度必∅≠T⊆S，且它本身已有峰≤1；每个满足关系的pattern都可det-bit-poly给完整unit调度。不给S=T或恰一query/return的额外合同。

**证明。** 完整C<2时E_i不能同住两unit，故若b_i在E则q_i必在H，T⊆S。每P至多一unit，而k−1个池机无法接全部k个b，故T非空。反向∅≠T⊆S给≤k−1个内部b，逐一放不同P；H总Σ_(i∈S)a_i≤1，E每机至多一unit，全部原jobs一次，峰≤1。每b所有finite时间均1，给全局下界1。

坏pattern若T不包含于S，有E_i两unit给下界2；若T空，k个b在k−1个P中使某机≥2。上界总可给≤2：全部q按pattern，若T非空则内部b≤k−1各放不同P；T空时只让一池放两个b、其它各一（k=2时唯一池两件），H≤1，E≤2。因此坏pattern精确2。Good pattern的任意不恰当池分配仍可峰2或更高；只对其最优构造与实际C<2时已无同池碰撞的调度声称峰1。

**Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 全部singleton aligned S=T={i}可strict1，inactive S=T=∅及singleton cross精确2；H可真实共居任意多small queries，和§4满一件matching不同。但孤立模块总OPT1，例如S=T=[k]，没有源NO。新增q外端、将E并入变量环或多个i共享机均改矩阵，T⊆S不免费保留。它只给精确多query身份containment，不给变量一致性、source嵌入或困难性。依赖显式完整矩阵、Σa≤1及unit计数，标准pool/共享端技巧非新matching理论。2k机2k任务、finite k²+2k、dense4k²；构造/原身份解码/有理负载回算按总位长多项式，不枚举所有patterns或按分母数值展开。作者先冻Exact，bicriteria只据陈述独立全证后才读作者Proof；root独核全部pattern。见[共享外端边界审查](../../reviews/unrelated_machines/shared_outside_small_query_pool_review.md)。无软件/外审/全球新颖性认证，UM-TARGET-v1保持OPEN。
