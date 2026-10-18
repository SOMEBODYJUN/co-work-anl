# Normalized flat CONFIG、FSLP 与 bounded-row SC：作者 Proof v3

对应最终 Exact：`normalized_menu_full_support_lp_preservation_exact_v3.md`，SHA256 `6a31b2699304f18847d1226305fa72c8f56998a2930f846a3467ca45309194bf`。

rainbow，2026-10-18。仅clone外冻结，先仅root保管，未直接交任何Exact-only reviewer。v1 Proof（SHA `7f8bd074a0f137dd4c75260fd7c8bd4023bcd24d5bd96042b56b46c552e47740`）保留原字节；本成熟Proof重述关键旧核心并自足证明新增flat CONFIG桥与SC层path，未制作v2独立Proof或给过程稿另造审查地位。

## 1. FSLP到完整flat UM machine CONFIG(1)

固定normalized Q、可行λ。对每private M_gs，记I_gs为其全部真实incidence jobs，Z_gs为其中private权0的jobs。给两个原合法配置：

- {J_g}∪Z_gs，权λ_gs，实际负载1；
- I_gs（无selector），权1−λ_gs，实际负载Σp=1。

它们权和1。若权0可略去；同一zero job在两配置都出现，private总coverage恰1。每positive incidence私有coverage为1−λ_gs；group selector跨全部私有机coverage为Σ_sλ_gs=1。

对每真实resource machine R_u，为每个p_gsu>0的不同原incidence job给unit singleton配置，权λ_gs；这些权和≤1正是FSLP约束，用empty configuration补足到1。0权原incidence不需要resource配置，因为其原private coverage已恰1；unused resource只取empty。

每positive原job的coverage为(1−λ)+λ=1；每zero job coverage1；每selector coverage1，全部原machine权和1，配置真实时间≤1。输出包含全部未选state原jobs，没有用删zero任务换取可行性。总支持O(S+I+|U|)，每private配置列表只重复各自原jobs有限次，显式多项式。

## 2. 完整flat UM CONFIG(1)到FSLP

给任意有限有理machine CONFIG(1)，每machine配置权和1、各原job coverage≥1。令λ^0_gs为M_gs配置中含原J_g的总权，则每group Σ_sλ^0_gs≥1。

对每positive原incidence j=(g,s,u)，private处理时间p>0。它与unit selector不能同时出现在负载≤1的private配置，所以其private coverage α_j≤1−λ^0_gs。该job只有这一个private端和唯一resource端；为覆盖≥1，其resource coverage β_j≥1−α_j≥λ^0_gs。

每resource上的所有原jobs真实处理时间都是1，任何负载≤1配置至多一件，所以Σ_{j外端u}β_j≤1。只取positive private jobs，便得

    Σ_{g,s:u∈P_gs} λ^0_gs ≤1。

把每group的λ^0按固定顺序向下削减到总和1，得到λ_gs≤λ^0_gs。资源行不会增大，故λ为FSLP可行点。0权jobs不提供这个资源下界，也没有被误加到P_gs；它们在输入CONFIG中仍作为原job被覆盖。

若采用精确coverage=1的CONFIG版本，selector总和本已1。一般≥版本与精确版的有限证书转换也可显式做：逐job删去其coverage超出1的部分，只把含该job的配置修剪；每job最多在一个配置处切分一次。负载向下封闭，每machine总权不变，最终支持至多原支持加原job数，位长多项式。本桥本身已从λ输出精确覆盖，不需隐式大证书。

因此restricted完整flat machine CONFIG(1)⇔FSLP。这里只用了原矩阵两有限端与private总质量1；没有一般UM或任意T的CONFIG保持结论。

## 3. Tree FSLP的双向有限证书

正向：对每原group树顶点v，令x_v为其子树叶states的旧λ总和。Root x=1。Root internal两个child states概率x_left,x_right；非root internal own概率1−x_v、children概率x_left,x_right；非root leaf own概率1−x_v、旧state概率x_v。K1直接保旧state。

每own-resource a_v仅被parent child-state与v own-state使用，概率x_v+(1−x_v)=1；旧positive资源占用恰原λ。全部groups概率和1，树FSLP可行，0项不改正support。

反向：给任意树可行μ，从每root发1单位flow。若到非root v的flow f_v≤μ_parent,child-v，own-resource容量使

    1−μ_v,own ≥ μ_parent,child-v ≥ f_v。

Internal v可在其child-state概率容量内分配总和f_v的两路出flow，按固定顺序填即可；leaf旧state概率至少f_v，令旧λ_s=f_leaf。每树leaf总flow1，且各旧λ_s≤对应leaf旧state μ，故旧资源容量≤树原资源容量≤1。K1直接保留。额外off-path activation无需全部投影，避免把leaf概率总和误算成1。

## 4. Menu-level path FSLP双向证书

对旧resourceu、all-menu（含0项）incident groups g_1,...,g_d，令x_i为其old λ在该group所有positive-u states的概率和，Σ_i x_i≤1。d≥1时取hole分布π_i≥x_i、Σπ=1，例如将余量加π_1；helperj左state概率Σ_{h>j}π_h、右state概率Σ_{h≤j}π_h。每helper概率和1，每port i helper占用1−π_i，合旧positive占用≤x_i+1−π_i≤1。d1无需helper，d0资源unused。

反向给任意目标证书，旧groups λ照取。把某u的d个port容量相加：d−1个normalized singleton helpers总占用恰d−1，故旧positive总占用Σx_i≤d−(d−1)=1。Zero incidences只影响Γ(u)名单，不误算positive占用；d0/d1直接成立。

故T、D、N均双向保FSLP，配合第1–2节立即给flat unit-threshold CONFIG双向有限证书转换。Actual V/完整UMOPT保持引用已存完整normalform合同，不从分数等价倒推实际相等。

## 5. State-dummy SC CONFIG(1)精确桥

每stateagent real row总价值1。给FSLPλ，该agent取完整positive support配置P_gs，权λ_gs；若K_g≥2，每个本组singleton dummy另权(1−λ_gs)/(K_g−1)。各agent总权1，每dummy总占用Σ_s(1−λ_s)/(K_g−1)=1，real item容量是FSLP约束。K1只有λ1的real support配置。

反向给SC CONFIG1，将含本组dummy的配置修剪为其中一个dummy singleton；不含本组dummy的配置，价值≥1且real row总值恰1，故必须含全positive support，可修剪到P_gs。外国dummy和real零值项均可删，不增加任何item marginal。

令ρ_gs为修剪后的real-support配置概率。每组只有K_g−1个dummy容量，故Σ_sρ_gs≥1。从ρ逐group向下削成λ≤ρ、Σλ=1，real资源容量随之不增，得到FSLP。给有限配置列表的转换有限、显式且多项式。

Target>1的每个SC配置必须含本组某dummy（real total仅1），于是K_g agents要求至少K_g总dummy边际，超过K_g−1容量。故SC CONFIG最优阈值≤1；FSLP可行时达到1。Actual SCOPT=V由已存state-dummy值桥：每组至少一个agent没有own dummy，取它的real bundle反解同state；正向给其余stateagents不同dummies。这个实际值桥不把CONFIG1当实际YES。

## 6. SC层path：完整原对象与actual正阈值

固定任意非空old agents、有限items、有限非负有理估值。对itemu的positive agents列i_1,...,i_d，各有自己的copy z_{u,j}，只有旧agent i_j保持原正估值；新增helperj对相邻copies各值1。d0保unused item，d1无helper；0原估值不造正copy。

Actual前向，给old minutility≥v、0<v≤1。删去各agent的0值items；每u若由old agent i_a领取则以a为hole，否则任选hole。将该old item给它自己的copy；helpers j<a取左copyj，j≥a取右copyj+1，恰填hole外所有copies，各得unit1≥v。Old agents价值原样保持，不同u的items/helpers互异，得到完整new allocation。

Actual逆向，给new minutility≥v>0。每helper必须获得至少一枚自己的positive copy，d−1helpers占至少d−1枚不同copies；每u最多剩一枚copy给old agents。Oldagent只对自己的copy有正值，先删0值items，再将其所领copy合回old u。每old u至多分给一oldagent，所有oldagent实际价值原样保持≥v。Helper若领两copies只会减少旧可用数，不影响逆证。

因此前向在v≤1、逆向在任意v>0成立。若oldOPT≤1，两向给actualOPT相等；oldOPT0时new若有任意正值就逆向矛盾，故0也保持。OldOPT>1不据此宣称前向保最优值。

## 7. SC层path：CONFIG前向有限证书

给old CONFIG(t)有限有理证书，0<t≤1。先删每配置的0值items，再把oldagent i的每个old positive item u重命名为自己的copy。

对固定u，令x_a为oldagent i_a配置中u的总边际；Σ_a x_a≤1。取π_a≥x_a、Σπ=1（余量放第一项）。新增helperj的两个singleton配置分别给权Σ_{a>j}π_a与Σ_{a≤j}π_a；每helper总权1、配置值1≥t。

每port a的helper边际恰1−π_a，旧agent边际x_a，总量≤1。d0无positive边际、unused资源保留；d1无需helpers直接cap1。旧agent配置值与权不变，新证书全部agents满足目标t，items容量同时成立。只增加2h个helper singleton配置，不按分母展开随机hole分布。

## 8. SC层path：CONFIG逆向任意正阈值

给new CONFIG(t)有限有理证书，t>0，先删全部配置0值items。每helper只有两相邻copies、各值1，因此每个正配置非空，expected copy件数至少1。对某u，将d个port容量相加；记oldagent各自copy marginal为x_a，则

    Σ_a x_a + Σ_{j=1}^{d−1} expected_copy_count(helperj) ≤ d，

所以Σ_a x_a≤1。Oldagent修剪后对每old u只可能含自己的那一枚正copy，将其重命名回u不会在同配置重复同一old item，配置价值完全相同；old u总边际Σx_a≤1。删除新增helperagents即可得到old全部agents的CONFIG(t)证书。

这适用于t>1：helper配置可能含两copies，但只用非空这个下界。前向仅t≤1保证，因为singleton helper配置只有unit值。若old CONFIG最高阈值≤1，正阈值双向给新旧最高值相等；0端点由new若有正证书必使old有正证书补足，不能在t0要求helper非空。两个实例的CONFIG0可分别用empty configurations实现。

## 9. Rowtotal、degree与完整composition

SC path对每oldagent只把每条positive估值搬到自己的copy，rowtotal精确不变；newhelper正值恰两个unit，总和2。每copy只被其一个oldagent及至多两相邻helpers正估值，positive-degree≤3，unused0。

N(Q)每group K_g≤3，因此SC(N(Q))每agent rowtotal=1+(K_g−1)≤3；其actual与CONFIG最高值都≤1。第6–8节由此精确保到J(Q)=P_SC(SC(N(Q)))，最终row≤3、item degree≤3。CFG1的源可行性同于FSLP，同于restricted flat machine CFG1；actual V精确保，所有值/阈值0与1边界都按各自正确合同处理。

BCG2009 §2.2/Theorem2.4/Fig2是相同adjacent dummy路径的已知来源；保old rowtotal意味着它不能将一般SC无界row压成3，本应用是先已有bounded-row SC像才使用它。没有新degree-three思想、没有误套VW degree2或一般SC困难性。

## 10. Q_D与无界CONFIG gap的准确应用

Main group state a为g_{a,1},...,g_{a,D}各权1/D。每(a,j)helper二选singleton g_{a,j}或A_a、权1。FSLP可行：main λ_a=1/D；helper取g概率1−1/D、取A概率1/D，每g marginal1、每A marginal D·1/D=1。

任意正实际allocation中，每helper必须拿自己的g或A；main在任一state a里领取r个g，就迫r个不同helpers全拿同一个A_a，故r≤1、main value≤1/D。给main g_11、helper11 A_1、其余helper各自g即可达1/D。因此V(Q_D)=1/D。

经actual normalform / SC值桥 / 新SC path，J_D actualOPT=1/D；经FSLP / 双CFG桥与新path，SCCONFIG最高值恰1，flat normalform machine CFG1也可行而actualUM值2−1/D。所有新正值仅1，旧正值1/D或1，所以最终SC仅此两种positive values。

这只是标准selector/重轻与既有uniform parking gap模式，经新精确证书保持合同的转述，不是source NP-hardness。每个J_D actualOPT都小，并非actualOPT≥1的YES，故没有否定任何实际YES promise finder。

## 11. 位复杂度与最终界限

所有证书转换按实际显式输入及有限证书支持长度多项式。Tree是有限部分和/贪心剪flow；menu path与SC path是有理hole概率部分和；SC CONFIG修剪不增边际；flat CONFIG正向至多两private配置与每positive原job一个resource singleton，原zero jobs精确保留。无分母、1/p、T/s或隐式D展开。

Normalform规模由既有计数2S−n groups、5S−4n states、I+4S−4n incidences与线性helper上界给出；SC path helpers≤old positive entries、items≤positive entries+unused items，dense乘积亦多项式。Q_D本身O(D²)显式对象，所有后续步骤poly(D)，不声称poly(log D)输出。

v3是一个成熟合同：restricted-flat machine CFG1、FSLP、SC CONFIG1及normalform与SC path保持；v1/v2仅保冻结来源，不凭过程稿次数增加真值或新颖性。没有新软件、有限枚举替代一般证明、外审或全球原创认证。

ActualOPT≥1时是否能在row≤3、degree≤3/9下det-bit-poly找固定正常数minutility仍OPEN；本CONFIG反例只排仅凭该LP可行性得到常数的合同。真实near-2 source及一般UM主目标没有由此解决。
