# Normalized flat CONFIG / FSLP / SC path：v3 statement-first 独立审查

审查者：general_query_response_review。2026-10-18。

## 1. 实际顺序、定义和正式判断

本轮首次仅据以下完整v3 Exact独立审查：
/workspace/scratch/038d9dcc4cac/normalized_menu_full_support_lp_preservation_exact_v3.md

SHA-256：6a31b2699304f18847d1226305fa72c8f56998a2930f846a3467ca45309194bf。

此前已冻结pre-Exact研究checkpoint及v1独立全证（分别b33a165f...、dff69ad0...），并早已独立审过tree/menu-path的integral V与完整UM保持。新增machine CONFIG桥和SC层path在本轮单独从v3定义重构；没有读v1/v2/v3任一作者Proof，没有读v2 Exact或其它agent策略。v3只列出的历史Proof SHA不是Proof内容，本记录不把它算作读取。

FSLP严格按positive support 0/1计，不按private权，也不把零incidences计容量。所有真实0权UM jobs仍在原矩阵。本轮正式核完整v3，原记录不回写。

**结论：v3全域有效，无fatal。新增restricted-flat machine CONFIG(1)精确桥、SC层path的actual与有限CONFIG阈值合同均成立；继承的tree/menu-path/SC桥和自足D族也一致。只scratch新增，无repo/Work/Git修改、无软件或有限枚举认证。**

## 2. 新桥：FSLP→完整flat UM machine CONFIG(1)

固定state(g,s)，记I_gs为其全部incidence jobs，Z_gs为其中private时间0的jobs，J_g为group selector。给FSLP概率lambda_gs，在private M_gs给两种合法配置：

- 概率lambda_gs：{J_g}∪Z_gs，总处理时间1；
- 概率1−lambda_gs：I_gs，总处理时间严格1。

概率和1。Selector J_g跨其private machines覆盖sum_s lambda_gs=1；每个positive incidence private覆盖1−lambda_gs，每个zero incidence private覆盖lambda+(1−lambda)=1。

对每resource R_u，将每个positive incidence I_gsu的singleton配置赋概率lambda_gs。FSLP保证这些概率总≤1，剩余给empty configuration。Resource端每个incidence耗时1，所以singleton合法。0权private incidence不在resource配置中覆盖，其已在private精确覆盖1。Unused R_u给empty概率1。

于是全部原machines配置概率和1，全部原selectors、未选state incidences、zero incidences均精确覆盖1。不同indexed states和jobs身份不合并，完全没有删掉原任务或假设实际unit调度存在。

## 3. 新桥：任意flat machine CONFIG(1)→FSLP

给完整有限证书，机器各配置概率和1，原job覆盖≥1。令alpha_gs为M_gs配置中含J_g的总概率。J_g仅可在本组private机执行，因此

A_g=sum_s alpha_gs≥1。

对任意positive incidence e=I_gsu，其在M_gs的覆盖beta_e≤1−alpha_gs：因为J_g时间1，p_e>0，二者不可能同处≤1配置。该job只有M_gs、R_u两个原端，所以resource覆盖gamma_e≥1−beta_e≥alpha_gs。

R_u上每个原incidence时间都为1，任何合法配置至多一枚job，包括private时间为0的那些jobs。因此

sum_(g,s:u∈P_gs) alpha_gs≤sum_(positive e at u)gamma_e≤1。

令lambda_gs=alpha_gs/A_g，组内和1且lambda_gs≤alpha_gs，得到所有正support容量≤1。Zero private jobs不能用于beta_e排斥，因为它们可以与selector同居；这恰是FSLP忽略zero而仍正确的原因。

输入若job覆盖恰1同样成立；若只≥1，以上得到lambda后再按§2输出新的精确覆盖1证书即可，未承诺保原边际。一般的向下封闭解释也正确：逐job剪除多余覆盖，必要时拆分一个配置权，删job不增负载、其它job边际不变；显式有限证书的拆分次数多项式。

该证明关键依赖unit selector、unit资源端、state private总质量1及精确两端资格，不升级成一般UM CONFIG、其它阈值或CONFIG优化值保持。反向不用实际OPT、SAT赋值或未知allocation。

## 4. Tree / menu-path / state-dummy的完整v3范围

v3 §3与已审v1的positive FSLP及旧actual合同同域，以下独立要点继续适用：

- Tree forward按source state概率走root-to-leaf，off-path选own，fresh own资源usage恰1，原positive资源usage不变。K1直接原state。
- Tree reverse记parent选v的概率q_v、v选own概率o_v，则q_v+o_v≤1，非own分支质量≥q_v。Root发出1，逐层得本树全部leaf original-state概率W_g≥1。将各leaf概率除W_g得到source组概率，全部原positive资源usage只减，不假定target只有一条活路径。
- Menu-path按全部membership含0项列groups，但a_j只计positive states概率。Forward选hole h_j≥a_j、sum h=1，helpers覆盖每port概率1−h_j；reverse求和d个port容量，d−1个helper各总positive singletonusage1，故sum a_j≤1。d0/d1、全zero membership、重复states和unused均成立。
- 因此原/T/N的FSLP双向等价；结合本记录§2–3，三个完整flat UM的machine CONFIG(1)也双向可构造。证书需要覆盖每个对象自己的全部原jobs；这不是假装不同矩阵有完全相同task边际。
- State-dummy SC forward：agent(g,s)以lambda_gs取全positive-real support，其余概率分到K_g−1个本组dummy singletons；K1无dummy、lambda1。
- SC CONFIG(1) reverse：删0值items。有dummy的配置可剪成一个dummy；无dummy的≥1配置必须恰含全部positive real support，因real总值严格1。令此配置质量w_s，dummy容量给sum_s w_s≥1；组内缩减归一即FSLP。
- SC threshold>1时，每agent配置必须含至少一个本组dummy，K名agents需dummy边际至少K而只有K−1容量，矛盾。G非空、K1边界均处理。因此SC CONFIG最高≤1，FSLP可行时恰1。

实际SCOPT=V也可由每group至少一名state-agent未拿dummy及反向给其余agents dummy直接得出，含0；zero UM jobs不能从实际flat输入删去，SC中删0值items只是一种不同分数对象的安全配置修剪。没有把SC CONFIG最高阈值与UM machine CONFIG makespan最小阈值混淆。

## 5. 新SC层path：完整对象与actual双向

任意非空old agents、有限items（可空）、有限非负有理估值。对u的d个positive agents，只有i_j对copy z_(u,j)保持原v_i_ju>0；其它old agents对该copy值0。Helpers r各只对z_r,z_(r+1)值1。不同u的copies/tags互异。

### Actual forward，0<v≤1

先从old allocation删每agent的0值items，不改utility。每u最多一个positive owner i_j，为它保留hole j；若无人领取则任选hole。Old agent取自己copy，helpers按hole路径匹配各取一个其它copy，value1≥v。Old utilities不变，全部new agents满足v，items不交。d1无helper，d0保unused全0item，不需用它。

### Actual reverse，任意v>0

先删new allocation中每agent的0值items。每helper至少得到一个相邻positive copy，可能得到两个；d−1 helpers占用至少d−1枚不同copies，所以old agents合计至多领取u的一枚copy。每old agent对同old u也只有自己的一个positive copy，故合回原u不重复、不冲突、utility完全相同。Helpers删除仅在回到old SC对象的投影中发生，不是假称new allocation遗漏helper。

不需要也不能偷假设helper恰拿一个copy。若v>1，helper可能需两枚，仍满足上述至少一枚的计数。正阈值逆向给new实际OPT≤old；若oldOPT≤1且正，forward可作用于达到该值的old allocation给相反界。若oldOPT0，逆向排除new任何正值。因此oldOPT≤1时精确保actual最优含0，但oldOPT>1不作一般最优值保持。

Oldagent rows精确不变，每helper row2，每copy正度≤1 oldagent+2相邻helpers=3；unused为0。构造不用OPT或目标阈值作参数。

## 6. 新SC层path：有限CONFIG阈值双向

### Forward，0<t≤1

给old有限有理CONFIG(t)，先删每配置中0值items，然后将oldagent i_j配置中的u重标为自己copy。每配置价值与概率不变。

对u记a_j为oldagent i_j配置包含u的总概率，old容量给sum a_j≤1。选hole分布h_j≥a_j、sum h=1；helper r用left singleton概率sum_(h>r)h_h、right singleton概率sum_(h≤r)h_h。每helper配置value1≥t，概率和1，各port helperusage1−h_j，加oldusage≤1。d1/d0与全0item如上处理。

### Reverse，任意t>0

给任意new有限证书，对所有agents配置删0值items。每helper配置若要value≥t>0，至少包含一个本path的positive copy，可能同时含两个；所以d−1 helpers的总copy边际usage至少d−1。将d个copy容量相加，得到oldagents的positive copy边际总和≤1。

每oldagent对同old u只有一枚positive copy，删0值copies后配置中不会有多份正值u；合并回原u保持配置价值≥t和概率和1，且刚得的边际≤1正是old item容量。若helper一配置含两copies，只会加强占用下界；t>1时不能把它剪成singleton，本证明没有这样做。

因此给定有限证书的两向转换正确。Old CONFIG最高≤1时，正threshold逆向给new最高不大于old，forward给不小于old；有限估值/有限item集的可行阈值有达到值。Old最高0时逆向排除new正值，两边CONFIG0均可另用empty configurations。t0不属于该非平凡merge投影合同：helpers可empty时不能用d−1消耗推理，v3正确单列此点。

正向仅需旧证书marginals、hole前缀和和每helper两singleton证书；逆向只strip和重标合并，不求未知配置或allocation。这里是普通SC的unit helper重构，不是在一般UM中加free容量。

## 7. 最终composition与自足gap

SC(N(Q))原agent row≤3、每real item正度≤9，其actualOPT和CONFIG最高均≤1。SC层path因此同时精确保actualOPT=V(Q)及CONFIG最高；final J(Q)旧rows不变、新helper row2，item正度降至3。其SC CONFIG(1)可行性与FSLP、flat machine CONFIG(1)等价。

Q_D的自足证明不依赖BS：
- Main state a按行D枚g各权1/D；若main领取超过一枚，则对应多个helper只能竞争同一A_a，不能都正值，所以V≤1/D。Main取一枚、对应helper取A_a、其余helper取自己g达到1/D。
- Main states各lambda1/D，helper以1−1/D取g、以1/D取A_a；每g和A资源usage恰1，FSLP可行。

经所有已证桥后，J_D actualOPT=1/D、SC CONFIG最高=1，rows≤3、item正度≤3（因此也≤9），positive values仅1、1/D。Normalform的flat UM machine CONFIG(1)可行，而actualUM=2−1/D；这只是在明确对象上的既有gap转述，不是新的复杂性源。

D族原groups D²+1、states2D²+D、incidences3D²、resourcesD²+D；各normalform/SC/path新增数线性于相应显式条目，总poly(D)，dense亦poly(D)，给定lambda的CONFIG输出支持多项式。不能称poly(logD)输出Ω(D²)对象。

## 8. 证书总位复杂度、零/空边界与限制

各转换只对实际给定的显式有限有理证书收费。CFG→FSLP用selector/real概率和及除组总和≥1；FSLP→CFG只列规定有限配置；tree/path用部分和、hole和/组内缩减。分母和数值无需展开，无除以p或1/V。条目标签、配置集合和dense矩阵均计入总输入/输出位长。

Normalized Q的groups非空、各menus非空且W1，保证positive support非空；unused机器在UM证书有empty概率1，zero jobs被明确精确覆盖。SC path允许空items及全0估值，但保oldagents非空；正值前向在这类实例可为空前件，0端点则用逆向排正值/empty证书处理，未让minutility对空agents未定义。

BCG路径的标准技术归属不升级新颖性；不靠degree3 general SC等价自动保rowtotal，也未调用degree2 VW。此新fractional合同不推广一般UM、 arbitrary-scale machine CONFIG或给定证书全部边际保持。I_D/J_D真实OPT<1，不反驳实际OPT≥1的promise算法；CONFIG障碍与真正finder/near2源义务分开。

**最终v3 statement-first冻结：完整v3通过，无fatal；新增machine-unit CFG桥、SC path全部正阈值/zero/empty/有限证书合同及最终row3 degree3 gap成立。未读任一作者Proof或其它agent策略。**
