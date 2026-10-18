# 归一化菜单 full-support LP 证书保持：作者 Proof v1

对应 Exact：`normalized_menu_full_support_lp_preservation_exact_v1.md`，SHA256 `9fd644392d624431050d0d1489bea4464284a1594f7868bf4a3667641233a763`。

作者 rainbow，2026-10-18。只在 clone 外冻结，先仅交 root；不直接给 Exact-only reviewer。本证明的主合同是分数正support证书保持，实际normalform/value桥引用已存完整合同，不把旧selector/parking gap重新命名为新hardness。

## 1. 共同约定与0项

每个state总private权恰1，P_gs={u:p_gsu>0}，所以P_gs非空。FSLP资源系数始终为1_{u∈P_gs}，不是p本身。旧incidence权0的真实UM job仍保留；FSLP与SC只在其对agent的正价值为0这一层忽略它。两种对象不可混同。

重复indexed states按不同s分别有λ变量与SC agent；资源在同state内互异。以下所有分数都是给定有理数的有限部分和/比较/缩减，不生成隐式无限配置。

## 2. Binary selector-tree：正向FSLP证书

给源FSLP可行λ。对每个原g的树，令每顶点v的x_v为其子树叶states的λ总和；root x=1。K_g=1时只有旧state，直接令其新group概率1。

对于K_g>1：root的两个child singleton states分别给概率x_left、x_right。非root internal v的own state概率1−x_v，两个child states概率x_left、x_right；非root leaf v对应s时，own state概率1−x_v，原state概率x_v=λ_gs。所有概率非负、每新group总和1。

每fresh own-resource a_v仅在parent选择child v的singleton与v自己的own state中出现，两项资源占用概率为x_v及1−x_v，总和恰1。每个旧资源的正support占用与源λ完全相同：它只经原state在对应leaf保留，概率仍λ_gs。原0项在leaf仍0，不额外占正support。故全部资源容量≤1，得到完整树FSLP证书。

## 3. Binary selector-tree：反向FSLP证书

给任意树FSLP可行点μ，不假设它来自正向公式。K1的root就是旧state，直接保留。对K>1的每棵树，从root发一单位activation flow，记到v的质量f_v。root的child states概率和1，可把root flow按该两概率向下送。

非root v的own-resource容量给

    μ_parent,child-v + μ_v,own ≤1。

归纳保持f_v≤μ_parent,child-v。因此v的非own state概率总和1−μ_v,own≥μ_parent,child-v≥f_v。

若v internal，可在两个child states的概率容量内选择总和f_v的非负出流，送到两个child，分别不超过其对应μ。按固定顺序先填左边再填右边即可；若v为leaf，则原state概率μ_v,orig=1−μ_v,own≥f_v。令旧state λ_gs=f_leaf。

每root发1、内部不丢质量，所以同一原group的所有叶flow总和1。每叶旧λ_gs≤其树中原state μ_v,orig。对任意旧资源u，

    Σ_{g,s:u∈P_gs} λ_gs
       ≤ Σ_{对应leaves:u∈P_gs} μ_leaf,orig ≤1。

最后一项是树FSLP自身的旧资源容量。故投影成源FSLP可行点。它允许树中存在额外off-path activation，不把所有非own概率误当作一单位总flow。

## 4. Port-path：正向FSLP证书

给源λ。对某资源u，将全部菜单内（含0项）incident groups列为g_1,...,g_d。令

    x_i=Σ_{s:p_gisu>0} λ_gis，Σ_i x_i≤1。

d0为unused资源，保留无需新变量；d1只重定向到唯一port，x_1≤1，且无helper。d≥2时，在所有d个ports中选择一概率分布π，满足π_i≥x_i、Σπ_i=1。例如把额外质量1−Σx_i全加到π_1，其余π_i=x_i。

对于helper j的左singleton z_j，给概率Σ_{h>j}π_h；右singleton z_{j+1}给概率Σ_{h≤j}π_h。每helper概率和1。等价于先按π选一个hole h，j<h的helper取左，j≥h取右；这只是λ证书的有限公式，不随机执行真实jobs。

每port i的helper占用概率恰1−π_i，加旧group正support概率x_i，总量≤1。所有旧state概率保持，全部旧权及0项保持；新的helper states权1且normalized。对不同u分别这样处理，fresh资源命名不交，得到全局path FSLP证书。

## 5. Port-path：反向FSLP证书

给path目标任意FSLP证书，限制到所有旧groups/states，其group概率仍和1。对资源u的d≥1个ports，令x_i为旧groups在port i上的正support占用。

d−1个helper每个概率和1、其state均为一个正权singleton，因此它们在全部ports的总占用恰d−1。把这d个port容量相加，得到

    Σ_i x_i + (d−1) ≤ d，

故Σ_i x_i≤1，正是合回原u所需的FSLP约束。d1同式或直接取该唯一port容量；d0无旧正占用。零private incidences虽使某group属于Γ(u)，其x_i贡献仍按正support定义计，helper总量公式不受影响。

所有原资源都满足容量，得到源FSLP证书。于是T、D以及组合N=D∘T均双向保持可行性，并有显式有理证书转换。

## 6. State-dummy：FSLP到SC CONFIG(1)

给λ可行。对stateagent a_gs，其所有real正item的总价值恰1，所以P_gs本身是价值1的合法配置。该agent以权λ_gs取此配置。

若K_g≥2，对本组每个dummy item分别给该agent singleton配置权

    (1−λ_gs)/(K_g−1)。

这些配置价值都是1；该agent总配置权为λ+(K_g−1)(1−λ)/(K_g−1)=1。每个dummy的所有agents总占用为

    Σ_s(1−λ_gs)/(K_g−1)=(K_g−1)/(K_g−1)=1。

每real item占用就是FSLP中Σλ_gs 1_{u∈P_gs}≤1。K1时λ=1，无dummy，只取其real support配置。于是所有agents与items同时满足SC CONFIG(1)。每agent至多K_g个配置，全部支持显式多项式。

## 7. SC CONFIG(1)到FSLP

给任意显式有限有理CONFIG(1)证书。先对每配置做向下修剪，不增加任一item边际：若配置含本group的某个正值dummy，取其中编号最小的一件，删其它items；若不含本groupdummy，则全部正值只能来自该agent的real row，而其real总价值恰1。配置价值≥1迫它包含全部P_gs，故可修剪为P_gs。外国dummy和0值real项均可删。

于是每agent配置只有两种：完整real support P_gs，或某个本组singleton dummy。令ρ_gs为该agent完整real配置概率。每agent配置权和1，而每组仅K_g−1个dummy、每个容量1，所以

    Σ_s ρ_gs ≥ K_g−(K_g−1)=1。

从ρ_gs中按固定次序削减为λ_gs≤ρ_gs且Σ_sλ_gs=1。资源容量继承为

    Σ_{g,s:u∈P_gs} λ_gs
       ≤Σ_{g,s:u∈P_gs} ρ_gs ≤1。

这就是FSLP证书。该步骤以实际给出的有限配置支持为输入，不隐含取得未知指数配置表或解决一般SC CONFIG分离oracle。

任意target>1的SC配置必须含一个本组正值dummy，因为real row总值仅1。若所有agents都要target>1，每组K_g个agents需要至少K_g总dummy边际，但本组只有K_g−1件容量1的dummy，矛盾。故CONFIG最高阈值≤1；当FSLP可行时第6节达到1，因而最高阈值恰1。

## 8. 实际值、最终row/degree与已存actual依赖

已存normalform保证V(N(Q))=V(Q)，含正阈值partial allocation双向及V0。这里添加的是新分数证书合同，不以整数值相等自动推断它。

State-dummy桥的实际V等值也可直接检查：给每组一state和不交real子集价值≥v≤1，让对应stateagent取该子集，其余agents各取不同本组dummy；反向在任何实际SC allocation中，每组至少一个agent没拿到自己的正值dummy，因dummy数比agents少一。选该agent，其real子集价值至少全局minutility，且不跨agents重复items，恢复同一state/组的实际partial allocation。该agentreal总值1也证明实际SCOPT≤1。此为已存桥的原合同，未处理一般高总值SC行。

N(Q)的每group至多3states、每resource跨全部states至多3groups。SC每agent的real总值1，加K_g−1个正值dummy，rowtotal=K_g≤3。一个real item被正估值的agents至多3groups×每组3states=9，zero不计只会更小；dummy positive-degree≤3。由前述分数等价，FSLP源可行就给该精确bounded-row/degree像的CONFIG(1)证书。

## 9. 显式旧gap模式Q_D与应用后间隙

资源为g_{a,j}、A_a，a,j∈[D]。Main group state a的D个g各权1/D；每(a,j)helper group两singleton choices g_{a,j}或A_a，权1。全部normalized。

FSLP证书为：main每state概率1/D；每helper取g的state概率1−1/D，取A的state概率1/D。g_{a,j}占用1/D+(1−1/D)=1，A_a有D个helper各1/D，亦总占用1。全部groups概率和1。

在任意正共同值v的实际allocation里，每helper必须拿到g_{a,j}或A_a中的至少一件单位价值item。若main拿到某g_{a,j}，对应helper就只能拿A_a。每个A_a只能给一个helper，因此main在任意同一state a的D个g里至多拿一件，其实际value≤1/D。可达性：main取g_{1,1}；helper(1,1)取A_1，其余helpers各取自己的g。所有helpers价值1，main值1/D。因此V(Q_D)=1/D。

由已存actual normalform及state-dummy桥，I_D=SC(N(Q_D))实际OPT=1/D；由本分数保持与SC CONFIG等价，CONFIG最优值=1。最终rowtotal≤3、item degree≤9，正值只有1/D、1（tree/path只添权1，dummy也1）。

Q_D有n=1+D² groups、S=D+2D² states、I=3D² incidences、|U|=D²+D；现有normalform保持显式poly(D)规模，因此最终agents/items与dense估值矩阵亦poly(D)。原λ分母D，树activation与path hole只有限求和，最后dummy配置分母再乘至多2，证书有显式多项式支持。D按输出规模参数，不按log D承诺输出Ω(D²)项。

这个例子是旧selector/重轻与uniform parking gap模式的重表达，技术不主张原创。此处承重增量为将其分数证书通过既有normalform/value桥，在精确row≤3 / degree≤9结构里保留下来。它否定的是“CONFIG1即可实际保正常数”的合同；这些实例的实际值都是1/D，不是实际OPT≥1的YES，因此完全没有否定真实promise算法。

## 10. BCG归属、位复杂度与剩余实际问题

本作者实际重读BCG2009原PDF §2.2/Theorem2.4/Fig2（印/PDF8–9）。它把一个度d item拆成d copies，加d−1相邻dummy players取∞。每原agent的旧item估值逐一保持，故原agent的全部rowtotal不变，不能由一般degree-three等价直接得bounded-row≤3。把dummy∞裁到给定target1时dummy自身row2，也不改变这点。当前path的LP保持是相同标准hole/matching技巧的直接合同，不冒称新degree reduction。

Tree的正向/逆向flow、path概率/求和、CONFIG canonicalization与削减都是显式有理数的有限运算。每一步数值的分子/分母位长按输入有理位长总和与多项式部分和界定；没有按数值分母或1/p生成objects。标准LP可行性在源FSLP上是显式多项式大小问题，不能因此推出实际partial allocation或SC minutility最优可算。

已实际检查current normalform与SC桥正文及CLAIMS相应ID，它们先前记录actual/partial归约，没有本full-positive-support LP双向合同。本记录不覆盖一般UM CONFIG，也不把SC CONFIG gap当NP-hardness、promise lower bound或一般SC算法反证。

真正待解仍是rowtotal≤3、item-degree≤9、实际OPT≥1时是否能det-bit-poly找某固定正常数minutility。该问题需要超出当前CONFIG证书的信息或真正的实际joint结构；本Proof没有解决它。主near-2 source仍OPEN。
