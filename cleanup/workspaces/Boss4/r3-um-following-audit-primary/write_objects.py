from pathlib import Path
import json
stage=Path(__file__).resolve().parents[4];base=stage/'archives/unrelated-machines/state/资源';base.mkdir(parents=True,exist_ok=True)
objects=[]
def put(name,body):
 p=base/(name+'--资源.md');p.write_text(body.strip()+'\n');objects.append(str(p.relative_to(stage)))
put('裸菜单反向放大的完整原矩阵审计入口',r'''
---
id: bare-cartesian-menu-original-matrix-audit-entry
kind: resource
type_tag: 资源
title: 裸菜单反向放大的完整原矩阵审计入口
status: integrated
truth_status: finite-exact-implementation-bound-to-separate-general-proof
review_level: full-363-line-primary-read-and-frozen-output-comparison
summary: 保全Cartesian原程序的完整矩阵生成、实际任务分配、独立checker、补组交点与仅t1完整优化；复用真实同SHA十五输出及root复核。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/audit_normalized_flat_cartesian_tensor_reverse_amplification.py
---

# 原入口与完整数学输入

[原程序](../../tools/evidence/um-following-audit-primary/original/audit_normalized_flat_cartesian_tensor_reverse_amplification.py) 共363行、16567字节，SHA-256 `efa03ab9bc976f899e7a1b9bd7af6a96a68ef76c18decbbb7e31921eb18d262c`。只导入 argparse、Counter、hashlib、itertools.product、json、Path；无作者 Proof、项目构造器或第三方库导入，没有随机输入。EXACT_SHA256 固定为 `60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac`，它是声明身份，并非运行时读入的文件。

输入数学对象为整数t≥1、D=2^t，组g和状态ℓ为二元t向量，资源逐坐标用u_i=2a_i+b_i∈{0,1,2,3}编码，满足 b_i+g_i a_i=ℓ_i。每状态支持D枚真实资源。每资源一机R_u，每组状态一机M_(g,ℓ)；组的selector只在本组全部M上用时1；每合法(g,ℓ,u)有独立incidence，只在本M用时1/D、R_u用时1。所有未选状态的任务也实际存在。

机器2D²、任务D³+D、有限资格2D³+D²。程序以整数D单位记录时间、起讫、负载，不用浮点；按全部4^t资源扫描每个状态支持，绝不是先按给定好见证生成一部分矩阵。`construct_matrix` 拒绝bool、非整数或t<1；CLI没有可变t选项，main固定t=1,2,3,4。

# 逐函数实际义务

`check_matrix` 回读实际稀疏P：机器id连续且资源/private标签完整唯一；每任务id唯一，selector精确有本组D个时间D的端；incidence身份(g,ℓ,u)唯一，坐标式逐项成立且实际端恰为自身private时间1/资源时间D。对每个state重新从整个资源宇宙求支持，核恰D及全部state表。t1还核四个基例支持 {0,2}/{1,3} 和 {0,3}/{1,2}。因此输入包含全部原任务和实际有限资格，不是局部槽/部分菜单。

`cyclic_state(g)` 将向量左旋一位。构造调度时selector去该状态，仅将已选状态且a≠全1的incidence外送，其余全部留private。每机按任务顺序串行安排，记录start/finish。`check_assignment` 再从真实P核每job恰一次、原端/时间、整数非负起讫、同机无重叠、总负载和末完成时；独立按标签重判每件任务应内留还是外送。每组选D−1项，每已选private负载D+1、未选为D，资源负载0或D且至多一件外送；使用资源D(D−1)，不用D枚。

`complementary_intersections` 检查**每个有序**g、补组h=1−g以及任意状态对(ℓ,ℓ′)，由实际P支持求交，再与坐标闭式a=ℓ+ℓ′、b=ℓ+g·a的唯一资源比较。共D³证书；unordered represented为D³/2，不能将二者相加。代码不枚举一般组间所有pair，只枚举声明的补组pair。

`exhaustive_t1_actual_opt` 明确拒绝t≠1；从P中每job真实finite列表作全部笛卡尔选择，累加每机负载、直方图及一个最优赋值。t1有1024份完整调度、最优3个半单位=3/2。t≥2的精确最优值来自另存一般证明，程序只核给定见证与交点。

# 软件证据与一般定理怎样衔接

[既有裸菜单反例](../反例/裸笛卡尔菜单乘积的精确反向放大--反例.md)已经自足证明V_t=1−1/D、OPT=1+1/D，不因本程序再命名一个定理。其承重点是：任意补组状态恰交一资源，不能都取满；循环标签领取a≠1时，碰撞给δ_(i+1)=a_iδ_i，从一个零坐标沿环得δ=0，故各组真不交；实际调度下界对C≥2平凡、C<2由所选private的共同资源冲突迫至少一件incidence内留。未选状态任务都被保全，不能从部分分配直接跳到全调度。

程序实现无约束裸菜单的循环见证，未实现另一逐坐标f_i(g_i)一致配额的匹配，也未物理强制这种一致性。t2裸菜单P有32机68任务144边、见证5/4；完整基矩阵Kronecker平方有64机100任务400边，是另一对象，不可互换。构造/检查时间按显式P及输出规模计多项式，不是poly(t)输出Θ(8^t)件任务。

# 真实历史输出、保护语义和本批复用

历史命令为 `python audit_normalized_flat_cartesian_tensor_reverse_amplification.py --output-dir /absolute/fresh/output_dir`。`mkdir(exist_ok=False)`要求父目录已存在且目标目录全新，每文件用open('x')；浮点递归拒绝并以allow_nan=False写JSON。这里只静态实读此分支，拒覆盖的历史执行者是fee，不能补称root或本批又亲跑了一次。

[完整旧输出目录](../../tools/evidence/um-following-audit-primary/historical-runs/cartesian_menu_reverse_v1/manifest.json) 的manifest列14个成员hash，另加manifest自身为程序15输出；本批还保留第16份root_original_matrix_verification，它是后来独立复核，非该程序第16个输出。旧记录显示root在新目录真实重跑同SHA程序，15文件逐字节一致，另不导入构造/校验器而独立重建全部有限端、核4710个原任务，重复t1的1024枚举。本批充分复用，新增原程序运行0；旧记录未记数值退出码或耗时，不填造。

| t | m / n | finite资格 | 实际见证峰 | 有序补组/状态证书 | 完整优化 |
|---|---|---:|---:|---:|---|
|1|8 / 10|20|3/2|8|1024份全原调度|
|2|32 / 68|144|5/4|64|未执行|
|3|128 / 520|1088|9/8|512|未执行|
|4|512 / 4112|8448|17/16|4096|未执行|

fee先读Exact未读Proof后实现；root读完整代码后独立核表，并另重跑；rank的数学认证仅原§1–5，不含§6–7另一Claim或软件。新正文保这些真实先验和完整原入口，不以共同整稿hash合并角色。audit_only、有限证据、一般证明、外审与新颖性继续分开；一般UM目标未解。
''')
put('完整双轨立方体的原构造与独立全割前沿',r'''
---
id: dual-rail-fullcube-primary-constructor-complete-cut-oracle
kind: resource
type_tag: 资源
title: 完整双轨立方体的原构造与独立全割前沿
status: integrated
truth_status: symbolic-normal-form-and-finite-cut-certificate-audit
review_level: full-both-primary-code-read-and-actual-input-comparison
summary: 保全全cube两份原代码的精确矩阵、满流实际证书、所有变量侧cuts与负载breakpoints；独立oracle不调用被测formula/flow但实际导入被测模块。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/balanced_dual_rail_fullcube.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/balanced_dual_rail_fullcube_independent.py
---

# 原输入与两个入口

[构造器](../../tools/evidence/um-following-audit-primary/original/balanced_dual_rail_fullcube.py) 6143B/157行，SHA `fb26f8eb03572406562f3f3d39329c742122209248ff6486773d189962e62c31`；[独立程序](../../tools/evidence/um-following-audit-primary/original/balanced_dual_rail_fullcube_independent.py) 7204B/164行，SHA `568c0826e01fa89b8b1585ed6d6789af37f7178c4bd05ac7b39d13eaacb038a7`。构造器仅标准库、CLI --A整数默认3；`instance`断言精确type(A) is int且A≥1。独立main无参数，固定A1..5，以同目录importlib导入**被测**构造器，不能称完全不导入规范程序；独立oracle自身不调用其formula/flow函数。

给A≥1，d=2A−1、k=2^(d−1)。变量v各有轨2v、2v+1，一枚selector仅在这两机时间1。每个mask∈[0,2^d)是一个真实clause机2d+mask；每个(v,mask)有不同port，negative为mask的第v位，有限端恰为对应轨时间1/k及本clause时间1/A。共m=2d+2^d、n=d+d2^d，每job恰两个不同端。全符号cube是显式输入，所有未述资格不可用，无背景负载。

# 精确公式与任意实际调度的下界

对A≤B≤d，R_B=Σ_mask (popcount(mask)−B)_+，r_B=ceil(R_B/d)，F_B=max(B/A,1+r_B/k)。`exact_formula` 直接扫描所有mask和B，取(value,B)字典序最小候选。必须保留min_B；不能把总取B=A当作程序或定理。已有[完整cube版本审查](../审查/双轨指定例外与完整cube精确前沿的版本审查--审查.md)承载一般OPT=min_B F_B证明，本资源保存其完整原实现，不再授一次主定理。

其一般下界需要真实规范化而非有限割输出自证：任意峰C≥1，完整cube同构可翻每变量的两轨并同步置换全部clause masks，使全部selector在负轨。把无selector的正轨ports全收回，正轨恰1≤C，其他负载只减，故无更优实际调度丢失。若C≥d/A，B=d已有F_d≤C；否则B=floor(AC)∈[A,d−1]。每负轨可内留h=floor((C−1)k)件，每大小s负clause至少内留(s−B)_+件，因此dh≥R_B，C≥F_B。该推导只适用于完整cube对称性，不能给任意阈值源公式免费使用。

# 构造器怎样落实全部原任务

`deletion_flow` 建source→每clause容量need=(s−B)_+，clause→每负变量单位边，变量→sink容量r_B。对每clause将need/s均匀分给其s个变量，变量置换对称给每个总流R_B/d≤r_B，所以满流存在。IntegralFlow 保存反向残余边，BFS找路、按瓶颈整数增广；从单位incidence边最终剩余容量0读出真实内留port集合，并核总数R_B。

`physical_certificate` 将selector负轨、全部正port自身轨、被满流选中的负port自身负轨，其余负port送真实clause；逐job原边检查并求全部机器Fraction负载。各clause外放恰min(s,B)，负轨最多r_B件，所以峰≤F_B；R_B>0时总数与上整迫至少一轨达到r_B，R_B=0时selector给1，且全负clause达到B/A，故实际峰恰F_B。`construct`核这个等式，输出完整instance、sigma/loads/内留身份、全部公式候选和自身hash。

A3另给七port手工证书：每缺i的大小4负集内收(i+1 mod5)，全5负集内收0、1。负轨内收[2,2,1,1,1]，峰9/8，所有clause≤1。若C<9/8，规范化后每负轨最多1件，共≤5，但五个大小4和一个大小5的clause合需≥7件，矛盾。原始[42机165任务双证书](../../tools/evidence/um-following-audit-primary/fixtures/dual_rail_fullcube_A3_actual_certificate.json)完整保全，两份sigma是不同真实分配。

# 独立全割与全部物理负载断点的含义

独立程序对每B=0,…,d和每非空变量子集I计算

\[
D_B(I)=\sum_{S\subseteq[d]}\max\{(|S|−B)_+−|S\setminus I|,0\}.
\]

在负轨每变量可收h件时，clause的need中最多|S\I|件能经单位边交给I外变量，故至少余量必须进I。对所有I要求D_B(I)≤h|I|，等价于该二部整数删除网络存在满流：任意mincut在给定变量侧后，各clause取更小切法即得此式。空I恒为0，不必枚举。独立oracle由此枚举全变量侧cuts，不使用构造器自己的F_B或maxflow。

候选C是{1+h/k:0≤h≤k}∪{B/A:A≤B≤d}。规范化调度的最大负载必在这两个真实网格，所有≥1候选足够；对每C取h=floor((C−1)k)、B=min(d,floor(AC))，用全割判断，取最小可行候选。这里的“physical”依赖上述一般规范化/mincut等价证明，不是枚举2^n份实际σ。

`physical_check` 独立按job顺序重新生成全部期望二端矩阵：前d件selector，余件以divmod(index−d,d)恢复mask/v；逐job检查所有身份与eligible值、sigma原端和全机负载、负轨内留数。它不直接相信被测data的稀疏表。A≥2另独立选每变量前k/2个负文字数≤A的clause外送，正轨全内留、负轨恰3/2、clause≤1；每变量可选数≥k/2。另对全部2^d源赋值核违反clause mask=assignment xor全1，只有A≥2才称弱阈值d−1仍NO。A1不误记NO。

# 实际历史运行和严格有限范围

[冻结聚合JSON](../../tools/evidence/um-following-audit-primary/historical-runs/dual_rail_threshold_soundness_boundary_audit.json)的boss11_dual_rail_cube_cut_actual字段同时绑定两代码SHA、完整输出计数及下表。旧审查记录root读并重跑，聚合另记8个退出码全0；该无逐命令下标的列表不被本批强行分配给某个单独run。新增原入口运行0，无新stdout或耗时。主默认A3有完整冻结输出，独立实际A1..5会调用每个原construct，因此原入口内容有充分同SHA执行证据。

| A | m / n | OPT | 全cuts | 负载断点 | 可行断点 |
|---|---|---:|---:|---:|---:|
|1|4 / 3|1|2|2|2|
|2|14 / 27|5/4|28|5|4|
|3|42 / 165|9/8|186|19|17|
|4|142 / 903|35/32|1016|65|59|
|5|530 / 4617|277/256|5110|261|240|

合计6342cuts、352断点、10实际证书、11592逐job原边/负载检查和680源赋值。10证书=5最优满流+4半量(A2..5)+1 A3手工；11592包含对同输入不同证书的重复任务检查，不能当互异job总数。A1..5仅五个实例，所有一般A的精确式/趋一估计来自证明；A20最优B21是旧数学审查算术叙述，不能称本代码实际展开了2^39个clause。

复杂度按显式2^d clauses、d2^d ports和输出长度计，增广总量≤R_B≤d2^d，候选B≤d，不是poly(A)或poly(log A)。本代码不实现其它scalar/split/指定exception合同，也不把某显式NO族当NP困难源；未知一般UM目标、新颖性、外审仍未认证。
''')
put('低重数标签束的生产接口与原父点独立审计',r'''
---
id: bounded-collision-production-and-original-parent-oracle
kind: resource
type_tag: 资源
title: 低重数标签束的生产接口与原父点独立审计
status: integrated
truth_status: restricted-constructive-proof-plus-finite-distinct-oracles
review_level: full-both-primary-code-dependency-and-fixture-read
summary: 保存五个生产API、后截断碰撞重数、原需求排序包络、原资源父点与一标签规范化两种oracle、有限调度桥和真实旧运行域。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/bounded_collision_bundle_floor.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/bounded_collision_bundle_independent.py
---

# 两主源、实际依赖与模型

[生产程序](../../tools/evidence/um-following-audit-primary/original/bounded_collision_bundle_floor.py) 25120B/510行，SHA `7f2fca2c8974661b51d4b499b4e3a38424ae0f3232d8a43f1c1198459efb410e`；[独立程序](../../tools/evidence/um-following-audit-primary/original/bounded_collision_bundle_independent.py) 13256B/303行，SHA `b2232aee8aa706bdd755353c9645b51bd4d8120db6cbcef22221a1d614e605d7`。均Fraction/整数无容差。独立代码只导标准库，不导生产代码或任务桥；生产main实际import同目录[rooted_dag_token_bridge](../../tools/evidence/um-following-audit-primary/dependencies/rooted_dag_token_bridge.py)，SHA825e6001…，并按`parents[3]/examples/...`读取[pairwise fixture](../../tools/evidence/um-following-audit-primary/historical-runs/pairwise_label_resource_floor.json)，SHA8cd207ea…，两依赖已完整读取和保全。单独调用生产构造API不执行main的指数oracle。

数学输入为四层简单DAG r→x→label→resource，q个变量、标签专属于一变量，每标签有显式互异资源支持S_e和正二进制需求K_e；根需求q、变量1、标签K_e、资源0。真实树每非根选中点一父，正需求输出叶仍收费，评分b=min({1}∪{outdegree/demand})。q0时是原零需求根终端，b*=1，桥仍有一件根任务、OPT=1，不是空UM的OPT0。

# 给定完整束的实际生产接口

`bounded_collision_floor(resource_sets,demands,owner_orders=None)` 要每需求为非bool正整数≤支持大小，资源为互异非负精确int；支持排序后截为前K_x项。Δ是**截断后**真实重数，可能小于原完整支持重数；可选owner_orders须恰覆盖所有使用资源且每项为该资源拥有者的排列。q0返回score1、delta0空标记，不作1/0。

逐资源按拥有者次序赋互异颜色0,…,Δ−1，不要求变量端边色互异。变量x有K_x次出现，至少一色给ceil(K_x/Δ)项。某色达标变量≥ceil(q/Δ)，选择该色全部达标变量及其所获真实资源；根比≥1/Δ、变量比1、标签比≥1/Δ，同色资源不重复父点，故b≥1/Δ。代码逐变量核鸽巢、选色按最大达标数/最小色破平局，再`validate_allocation`核真实资源不重用、支撑/长度和精确原需求评分。

`select_locally_full_labels` 为每变量选第一个K≤|S|的标签；若某变量没有，只输出“full_value_one_impossible_by_local_deficit”，绝不判所有正分数不可能。10^100需求只作比较，不按数值展开。`to_dag_and_tree` 把真实完整支持（含未分配资源边）编成r/x/label/resource DAG及本次选树，交给原任务桥检验。未选替代标签不受所给一标签束的Δ约束。

[既有低重数审查](../审查/低重数着色地板的原需求评分与独立枚举范围--审查.md)保一般颜色证明及域修正；本页补的是生产函数的精确截断、校验、破平局和有限原入口。二重锐性对每个K≥1成立：成对同K集，b>1/2会迫每标签取>K/2资源，因此每对最多选一变量而根比≤1/2；选每对一变量达界。一般Δ锐性只用K1单资源族，不能扩大到每个束宽均同样锐。

# 无给定标签见证的排序包络与原需求回算

`group_degree_label_approximation` 允许空菜单、空支持和K>|S|。Δ_G计所有替代标签关联到每资源的**不同变量组数**，不是标签入度。每组取a_x=max_e min(1,|S_e|/K_e)，平局首标签，空组a0；按(a降序,x升序)排序，取最小最大化前缀s，使U=max_s min(s/q,a_(s))。任意正分数β的原树至少有βq组，且每组选中标签有局部密度≥β，故b*≤U，原树可有多个标签而不破此上界。

U0返回根单点score0；q0独立score1。其余选前s组各最佳标签，截支持大小min(K,|S|)>0，把该大小仅作临时需求交颜色接口。所得局部重数Δ′≤Δ_G、选择组≥s/Δ′、每标签获≥|B|/Δ′。最终**按原q和原K_e重算**，根比≥s/(qΔ′)≥U/Δ_G，标签比≥a_x/Δ′≥U/Δ_G，所以b≥U/Δ_G≥b*/Δ_G。

`label_dag_and_tree`保全部替代标签及原需求；检查每组至多选一个本构造标签、分配不重资源，精确原评分与返回值一致。桥输出C≤2−b；由OPT=2−b*及差值2(1−1/Δ_G)(1−b*)≥0，得C≤(2−1/Δ_G)OPT，仅限此显式四层桥图像。Δ_G0且q>0时b*=0/OPT2，q0走终端OPT1；不把上界排序当通用最大树oracle。

循环由显式关联数、q和候选标签控制，K只出现在位长受控的有理数/比较中；截束大小不超过显式支持，无巨大二进制需求展开。

# 两种真实有限oracle及独立构造的差别

生产 `exact_bundle_optimum` 对每资源选拥有变量或absent，再遍历非空变量子集；允许资源暂给未选变量不影响最大值，因为可改absent。`exact_label_optimum` 先枚举每组absent/一个原标签，再枚举原资源所有者。只用一标签足够求最优有证明：β≤1且变量需求1，从任何正评分树每个组选一个已有标签，删其余标签/资源不减根比或所保留标签比、释放资源。因此这是该合同下的规范化，不是将一般树定义改为一标签。

独立 `exact_tree_optimum` 则直接对每个原资源枚举**所有原父标签或absent**，由正计数标签及祖先恢复树，允许同变量同时保留多个标签。正分数树必无正需求死叶，所以这些原父点选择覆盖全部正分数树；q>0时没有正树返回0，q0返回1。此不同oracle检验生产的一标签规范化，不导其核心。

独立 `collision_certificate`对所选标签的**整个原支持**计重数，未先截到需求；若K<|S|，其Δ可能大于生产后截断Δ，检验的1/Δ界可能较弱，二者不可声称逐数相同。它仍只计一个所选标签/组，不计未选替代标签，数学上完整支持中可再选需求子集，故界安全。

独立无见证构造保留Γ={1}∪{h/K_e:1≤h≤min(K_e,|S_e|)}。每τ取所有有密度≥τ的组、首合格标签、排序支持前ceil(τK_e)项，以逆组次序赋色，选择得分最大色。用Δ_G而非局部Δ′作阈值，得score≥upper/Δ_G；另以formula-only排序U核upper相同、原父点oracle核b*≤U及score≤b*。Γ大小按显式支持控制，仍不按巨大K循环。这是与生产排序不同的独立构造；后面的指数oracle才是有限审计，不能混作多项式API。

独立程序对调度仅检查桥梁代数`2-score`和`(2−1/Δ_G)(2−b*)`，**不实际调用桥、不输出完整schedule**。真实任务回填由生产main限定子集另承担。

# 实际任务桥、四份原证书与有限范围

真实桥对任意DAG建一件根job只能root耗1；每正需求点u建q_u=min(K_u,outdegree(u))枚不同token，每枚在u耗1/K_u或任一孩子耗1；K_u>q_u再建一个私有filler耗(K_u−q_u)/K_u。总jobs≤1+|E|+n，需求再大也不按K_u展开。给真实树，从每点最多保留K_u条子边、沿根递归外送对应token，其余全部本地，得到C≤2−b。任何C<2调度每机至多一枚外来单位token，沿根读取外送边为真实树且b≥2−C；C≥2时解码器明确拒绝，不能超出域调用。

生产main实际读两个fixture，另加q0和异质资源例。冻结输出完整保存其tree、所有job目的机及全机负载；本批又从原DAG和桥公式静态物化这些四份真实P/证书，注明不是新原入口运行。

| 原fixture/代码病例 | vertices / jobs | 构造b / b* | 实际峰 |
|---|---|---|---|
| identical_pair_k3 |8 / 11|1/2 / 1/2|3/2|
| triple_singleton |8 / 10|1/3 / 1/3|5/3|
| empty_root_terminal |1 / 1|1 / 1|1|
| heterogeneous_private_resources |12 / 13|2/3 / 2/3|4/3|

# 真实旧运行而非本批扩大范围

[双路冻结结果](../../tools/evidence/um-following-audit-primary/historical-runs/bounded_collision_label_floor_audit.json)完整绑定生产/独立/桥/fixture SHA。原命令分别运行两原脚本；原审查末尾明确root读并重跑最终两代码，退出码均0。规范旧elapsed_seconds=5.508641，属于旧run，不能称当前运行耗时；本批新增原入口运行0。

| 实际路径 | 完整有限域及数字 |
|---|---|
| 生产给定束 | r1..4、q1..3、所有非空支持及1..支持大小需求，35795族；三种资源拥有者次序107385着色；仅r≤3的1971族做328231 oracle状态 |
| 生产锐例/边界 | Δ1..5的两独立单资源组；K1..6同集标签对；5个label扫描病例、6个非法输入拒绝；四份实际回填 |
| 生产无见证 |2490菜单、35565一标签oracle状态；每个只核树；仅前12个及之后每第251个共21例调用实际调度桥 |
| 独立给定束 |240全菜单DAG、1056所给选择，500随机DAG，K1..9标签对、K1..4双对、Δ1..12单资源例、3退化边界；421839原父点选择 |
| 独立无见证 |4666 DAG、489061原父点选择；六标签的64局部菜单含空在q1/2的完整乘积，另500随机和6边界；seed2026101711 |

独立随机500例也参与无见证部分，分类有交叠，不能相加声称全部互异DAG数；原父点计数和生产“资源分配×变量子集”状态含义也不同。200位需求只证实际代码不按该数值展开。内部statement-first证明、实现者知情攻击、root实读/复跑的身份如原审查保留；当前读源码不倒填早期审查先验。

本页补的是完整原API、原输入、独立oracle及真实有限域。没有源CSP解码、Label Cover soundness、一般UM逆表示、外审或新颖性认证；一般UM目标仍OPEN。
''')
(stage/'cleanup/workspaces/Boss4/r3-um-following-audit-primary/object-paths.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n');print({'formal_objects':len(objects)})
