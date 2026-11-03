# 未认领的共享加权最大主题来源：实读接续备忘

**本件只是Boss5内部接续阅读备忘，不是正式数学对象、清洗回执或新证书。** 父方37源领取事务整体失败后，停止对这些未领来源继续扫读；下列十源未由本代理claim、未done。本代理没有Git、checkpoint、公屏、认证或凭据操作。任何后续正式归档须先核实际owner并协调，不能凭本笔记勾选他方源。

所有来源属于五人旧探索，不能因为当前主问题为六人就放进六人子档。代码使用五个比较索引、`k=5-i`、32种最大路径状态和64种最大路径/H联合状态。当前五人半覆盖已有独立精确证明，本笔记中的必要行点及未闭合付款都不改变它；六人问题亦未由这些点解决。

## 1. 来源身份及实际阅读方式

主冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`，另一同字节出处 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。十源共同原路径前缀为

`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/`。

| 源ID | 原文件 | 字节 | SHA-256 |
|---|---|---:|---|
| 8e293d0080b48dda85c7 | joint_weighted_maxima.py | 5415 | c8c0f0fb53ae3b8cd3c70793cd192bd57600bbc9ebfefc394fe2b928368a167e |
| 19afdf2bd2adb4e27d6a | joint_weighted_maxima_exact_current_source_fixed_v1.json | 867 | 3f6bbbda18251b6855ab4f5165ba6dc9577fd3a08e267ba40782879840f562d5 |
| 41201ebaff42959590f8 | joint_weighted_maxima_exact_current_source_source_last_v1.json | 2239 | 501f40345d8e00b61525aaa7995fc3f255ea0e8824dc35786c8fbde31f6e16c4 |
| 891a9e91438dc2380ff1 | max_indexed_coupling.py | 11829 | 32704775277544852e3c3b69bac4bc6c9303643ea880183b416c250322a29e81 |
| 5520585e6f2722abe96e | coupled_discovery.json | 213774 | e1922ff4862cb8cc9d5c888a3167f3754979f52e06e158445a3e1c0065dadbab |
| f5d9fc65b38fa090161e | exact_weighted_source.json | 52775 | 5d4f10fd8182f5257ce44b3e5ac67541c72fe08da779bfb950775063b00ef4f0 |
| 19453f21a12102366982 | weighted_discovery.json | 253826 | 952601aa1e7ec1365692a6ce8def7feb5819669a416b5311eec4204136ce8f6f |
| 61c1cd003cb4507ba643 | weighted_lift_coupled_discovery.json | 2290 | 1be345d58f009126293b8f9d152064c8ed493889b67e59bbe1ec0b15677c1bd0 |
| dfeeda2f80a50ab3e4e4 | weighted_maximum_query.py | 10305 | eaadba0b044a17c70251de4af4b5bbebbf20c7a340fbd806798900102f43d19a |
| 226371a6e7c7c6440cc8 | weighted_true_branch.py | 7706 | df6320716f09054459bbc1426dc0c9fde3aa9379ca9f97385e08c578fccb1e6c |

四份程序已全文读，控制流及副作用均读到main尾段。两份短joint JSON及weighted_lift的所有字段、53个projected coefficients和57个diagnostic atom bounds均已查看。两份长discovery JSON所有字段已解析；5421/5484个行名逐元素读入、按原语法分组并检查无重复，以及weighted前5421行与coupled逐字符串一致；63与114个原子逐记录查看，直方图以保留索引的稀疏表示显示，零项仍保在原JSON。exact_weighted_source的64项逐记录与weighted原子除质量外各字段比对，全部唯一对应，再逐条读恢复后的精确质量。

这不是重新认证旧oracle或全部5484行有理可行性。最初长结果发生过展示截断，已用字段/分组/逐原子紧凑输出补读相关内容，不能把最初截断输出当完整阅读证据。

## 2. 模型、主题和必要条件的量词

固定有限单位客户、有限非空共同带标签目录及一份在所有合法有序历史上定义的五人纯SPE σ。空主题、重复选择、同覆盖异标签、零客户及任意离轨平局全部保留。相同负载但不同有序历史可以有不同后继；每次强制偏离后沿同一原σ继续，不另选均衡。

实际路径为ABCDE；在(A)强制第二位E，真路径AEUVW；在(A,B)强制第三位E，真路径ABEXY。被强制的E本身没有新分支最优者身份。五个合法比较索引T_i可重复；d_x是该客户在五个T_i中的次数。AB/AE族直方图分别记录五个(T_i,回复1,回复2)三位，Sbranch记录五个(T_i,回复1,回复2,回复3)四位。mX/mY、mU/mV/mW是五项索引菜单，不是旧固定位X/Y/U/V/W单个主题。

选一个同目录裸大小最大主题M，强制根M后原σ给最大根路径(z0=M,z1,z2,z3,z4)，会员位mb共32态。其根被强制，后四位是真优化节点。原子还保十固定位、三个索引族完整hist及旧菜单端点`menus_lh`。这些压缩记录是原SPE的必要投影，非任何非负原子质量组合都能反向拼成共同目录或完整策略。

记q(a,b)=a/b（分子零时取零）。真实节点旧负载p、余k、当前利润u，对合法主题T有安全查询u−Σ1_T/(p+k)≥0。任意合法主题C,D的加倍AP，若两查询菜单长度n_C,n_D、客户次数c,d，则客户行

`n_C n_D a_k u_x − ((a_k−2)n_D c+2cd)/(p+k) − 2(n_C d−cd)/(p+1)`，

其中`a_k=8(k−1)+k²`。这来自菜单笛卡尔求和，包含重复/相等索引；两端同族时只产生该族计数的至多二次项。单客户系数可负，保证非负的是对全部客户求和后的真实行。

## 3. 最大根与旧索引菜单完整耦合

`max_indexed_coupling.py`在上游4007行基础追加1414行：AB/AE各401（AP204、K8、Tax35、Tuple154），Sbranch612（AP315、K12、Tax54、Tuple231）。共5421。AP在最大根真实后继i=1,2,3使用余k=5−i；K在i=1,…,4；Tax在i3的同一个末两人历史；Tuple在余3/4人真实尾部。

同一末两人税的客户预算为`Htax=(mb3+mb4)/sum(mb)+mb3/((p+1)(p+2))`，其中p=sum(mb[:3])。两查询菜单行是

`n_C n_D Htax − (n_D c+n_C d−2cd)/(p+1) − 2cd/(p+2)`。

Tuple选一个旧索引菜单中的某个主题重复n次，另配最大根五个标签的带重复多重集qs。对单客户记ss=Σ_{j∈qs}mb_j、该菜单客户次数c，背景p=sum(mb[:5−rem])，得到

`5 β_rem ·sum(mb[5−rem:])/sum(mb) − (5−c)ss/(p+ss) − c(ss+n)/(p+ss+n)`，

rem3用β3=5/3，rem4用β4=1499/750并另减`5 RHOMIN[mb0,mb1..4]`。这是合法背景尾部利润比较，非把根覆盖直接平移；RHOMIN必须保留这份旧四尾证书版本，不能换成后来的二谱或二值重权余项。

定价必须条件化完整32态mb，而不能只保末前缀负载。固定十位、d和mb后，各新增项只依一个旧族完整直方图，故三族最大化仍可分。源码`price`逐32态调用继承定价再去重；`family_score`把新增常数和计数/计数乘积全部收在本族，乘120。原程序显式禁止integer定价，并要求Fraction separation auditor负责精确结果；读代码不等于这个全域oracle已经本轮运行或重新认证。

`audit_frozen()`会对上游两指定精确点扫描1414行、输出exact_indexed_separation.json；本代理没有运行此入口，没有将它的旧精确分离当新运行。

## 4. 两份浮点discovery的真正状态

| 文件 | 行 | 存储原子 | 正primal支持 | restricted β | 历史 |
|---|---:|---:|---:|---:|---|
| coupled_discovery.json | 5421 | 63 | 57 | 2.012034007865775 | 仅iteration0 |
| weighted_discovery.json | 5484 | 114 | 64 | 2.01171824589555 | 仅iteration0 |

两者history均为new_columns=0，minimum_scaled_residual=null，pricing_contexts=null。不是一次完整定价得到没有负列：程序在β>2+1e−7时直接设minimum/context为None并跳过price，随后退出。报告中的dual只是受限矩阵的浮点乘子；这些文件不提供全域对偶界或精确最优性。

**质量字段陷阱：** coupled前部原子携带`exact_mass`，weighted又复制这些字段；这些是旧来源遗留质量，不等于本次受限LP的`primal_float`，不能把它们直接加总当本点有理质量。run和lift在有primal_float时明确以它为准；weighted的114个存储原子恰由coupled的57个正浮点原子各加H=0/1而来，其中有零及负零质量。真正恢复本5484行点的64正有理质量在单独exact_weighted_source.json。

本代理已读全部56个正浮点dual项及全部history记录；未改原小数、零和负零，未重新求LP或发现搜索。

## 5. 同一H位共享给全部菜单的63行

`weighted_maximum_query.py`在最大根第三位真实历史(z0,z1)选合法H，使Σ_H1/(p+3)最大；p=mb0+mb1，u=mb2/sum(mb)，K=Σ_H1/(p+3)。H会员位h∈{0,1}必须共用到所有旧菜单查询，不能三个族各挑自己的h。这是新增合法主题，而非给固定AP随意改乘子。

63行由裸大小cap、当前保底、16个固定/比较菜单各cap+BNS、一个global-root-BNS、十旧真节点安全查询、四个最大根真后继查询、七旧索引菜单各cap+BNS组成。对长度n菜单、客户次数c，cap与BNS客户贡献为

`n h/(p+3) − c/(p+3)`；

`8n u_x − 7n h/(p+3) − hc/(p+3) − (1−h)c/(p+1)`。

BNS用同一背景加权最大H和原真实偏离后继；当前只是把后继消去，并未证明这些行足够实现H。global-root-BNS为`80 root_x−15mb0−(5−4mb0)h`，它在实际根比较M和合法H，不能把根最优身份赠给强制M。完整定价块32×2=64态；旧族仍条件化共享h而可分。

weighted_lift固定coupled正浮点质量（57项，以十进制字符串转Fraction再浮点送LP），允许每项按h=0/1分拆，新增63行。冻结报告为浮点不可行，uniform violation=0.03050067328983795，诊断权只用wmax:BNS:opt≈0.13157894736842088和Sbranch:wmax:cap:mW≈0.8684210526315789，另存57个浮点atom bounds。没有恢复精确Farkas证书，不能把这些浮点权改成有理数后直接称已证分离。

版本缺口：此lift报告的code_sha256是`f914e87f7eef654ae6e5a9619a8497648540a184c8a82bc134b0fb475bff5c9f`，不同于本批现存weighted_maximum_query.py的`eaad...`。来源coupled SHA可准确绑定，代码版本不能假装逐字节一致。本代理没有为消除此差异重跑它。

## 6. 真实H,Q,R八态与精确源重建

`weighted_true_branch.py`保留同一真实第三位历史：强制加权最大H后沿原σ到Q,R。H受迫，不被称新分支优化者；Q,R为真正优化节点。隐藏八态是(h,q,r)∈{0,1}³。记s=p+h+q+r，V_H=h/s、V_Q=q/s、V_R=r/s，原第三位收益current，K=h/(p+3)。行包括current−V_H、H对全部固定/自己/比较及旧索引菜单的加权最大性、Q/R各自安全查询、三新主题裸大小及十旧节点/四max节点对它们的查询、同一末两人税和Q节点AP。FIXED含十旧标签、五max标签、f0/f1/f2及opt。

`exact_source`仅保留浮点质量>1e−8的支持，利用近似活跃行及QR选满秩方程，再用Fraction求精确质量；最后断言全部旧行余项≥0。报告exact_weighted_source为5484行、64正原子、最小余项0，source SHA准确指向weighted_discovery。其scope明确只为后续true-branch projection恢复输入，不给新福利最优界或游戏。

本代理没有重新运行此QR/有理恢复或检查全部5484旧行；本轮确认的是冻结字段、64精确质量及逐项输入身份，不能把原程序断言表述为本轮已执行结果。

随后lift为允许重新选择H，先按旧atom_key+max_bits合并先前H位分拆，64项成为55旧原子，再用完整八态。不可行时浮点辅助LP只找候选乘子；真正固定点分离来自将乘子有理化、逐原子八态取**最大值**g(a)、精确算Σm_a g(a)<0。因为每个真实八态的非负总行组合≤g，原SPE一定Σg≥0；负值只否定这个固定必要点的延拓。

相关但不属十源的exact_trueH_projection.json（ac2fe9ddfcab41331382）已作比较：55原子、747新行；七正权分别为sourceIC=4260/10211、weighted-cap:f1=2250/10211、weighted-cap:f2=2520/10211、R:K:opt=150/10211、global-size:0=1085/40844、tax:f2:opt=90/10211、Sbranch:weighted-cap:mW=2679/40844，即既有七行整数权整体除40844。其精确负值

`−169500194513991512083150016856795303715058552168132987135 / 24368697863582404164257358829723456062199106455303425183072`

约−0.006955652512204998。55个projected_atoms已逐项对照64源的对应/合并质量、coefficient与maximizing_state（该报告所选均000）；没有重跑747行lift、候选乘子恢复或八态计算，也未done这一比较来源。

## 7. 两个历史共享目录的四态接口及正确归因

`joint_weighted_maxima.py`分别在actual第三位(A,B)和max第三位(M,z1)选择最大H_a、H_m，背景p_a、p_m可不同。单历史各63行；除了大小、保底、cap、BNS和旧节点查询，还含已证七行包络在J=H重复五次时的K-envelope。随后四态(ha,hm)共用旧原子，加入

`Σ(ha−hm)/(p_a+3)≥0`、`Σ(hm−ha)/(p_m+3)≥0`。

它们是两个合法H必须互相接受对方查询的共同目录条件。只有两个单历史各先可行、联合新增互查后失败，才可归因新增跨历史兼容。单历史浮点成功仍不等于完整主题/策略可实现；真正分离须非负有理权和全隐藏状态精确最大值。

| joint报告后缀 | 输入SHA | 原子 | 单actual/max | 联合 | 允许新增兼容归因 |
|---|---|---:|---|---|---|
| fixed_v1 | 5bb6dba2eeb2792afd2f70813b25b0c60ccaafa0c369782e02c384c8ec01270c | 50 | 均浮点可行 | 浮点可行 | true仅是门槛许可，本例没有失败可归因 |
| source_last_v1 | 66d63289facc5945502371e6a8fd8857eef9eb9ed95835b08686cd39ee20a2db | 53 | 均浮点不可行 | 不可行，有精确负证书 | false |

两报告joint_rows128、hidden_states4、code SHA均准确等于本批joint程序。source_last有53个完整projected coefficients，其非零乘子只有

`actual:cap:V =13395/13396`，`actual:trueQR:K-envelope =1/13396`。

设v=1_V，m=mb0；K-envelope客户系数为`17040u_actual+1085m−13395K−F(p_a,d)`，cap为`K−v/(p_a+3)`。两行精确相加直接消K，得到

`g(a)=[17040u_actual+1085m−13395v/(p_a+3)−F(p_a,d)]/13396`。

**g与ha、hm都无关，两个cross行乘子均零。** 它正是已有七行关系(P)对合法V重复五次（Jcount=5v）的缩放，而非跨历史共同目录的新机制。冻结报告给出精确和

`−1615235803663103962900851282714651857955142931200397921609029753285 / 121090985230569162778503397748501348118202583034660747523471086889026`

约−0.013339026027309431。此值是固定输入点的严格分离，既不是新的half常数，也不构成原模型反例。fixed初始受限点覆盖比<2、source_last精确必要点覆盖比>2的区分来自后来certificate/README的明确校正，本代理未由两个joint报告本身重新证明其比值。

七行F表已与成熟引理及trueH_table_certificate.py全文对照：

| p\\d | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
|0|0|960|1220|1480|1740|2000|
|1|0|1665/4|2745/4|3785/4|4825/4|5865/4|
|2|0|320|524|728|932|1136|

其一般合法性来自任意真实第三位选择同一背景加权最大H、原σ真Q/R、七条非负原行及144态有理系数表。此备忘只做完整公式对照，没有重复运行成熟144态审计。

## 8. 实际比较材料、遗漏义务与接续建议

实际全文比较过的冻结相关代码：round13的lift_maximum_branch.py（8c0ec91d5d96b0977f49）、max_menu_joint_pricing.py（f640f8636aa8f4c9adb7）、max_menu_tuple_pricing.py（1f4560c9319c2a285e47）、menu_ap_pricing.py（95ae42780dac898a9c0d）；本工作区trueH_table_certificate.py（f4b7fe87b66d27263c18）；round8_five/README（f7048528c95cde186312）及certificate/README（d4f7253c134f336c8d49）。比较读了两个joint输入的top-level身份，未把它们的旧行全集再认证。旧full_pricing/cross_pair/exact_cross_primal等递归实现没有在本轮完整重新审计或执行。

结果树实读比较包括共同目录完整历史定义、共享加权最大双菜单铰链引理、真实第三位七行最大根包络引理、真实源AP笛卡尔求和审查及二值四尾保留余项引理的主要推导；五人正式定理的范围与结束状态也已核对。它们给出合法节点、BNS、AP、F表及旧RHOMIN资格，不能将“材料相互链接”说成重新完成独立实现。

父方若取得本组实际owner协调，可把四程序与两阶段数据归到父档`state/程序/共享加权最大主题的耦合与真实后继--程序.md`，配独立`tools/evidence/joint-weighted-source-primary/`资源包。数学对象可拆共享H行接口与双历史归因审查；应与邻组七行/实际十三行投影正文相互引用，避免重复造定理。此路径仅是建议，当前没有正式文件或receipt。

如后续正式处置，应保全十主源原字节、逐源身份、运行0次的明确记录及上述版本差；相关依赖只作comparison/dependency，不替它们认领或done。两份discovery的所有字段、原子、浮点dual、history均有独有历史内容，不能只记一个β后退休。exact_weighted_source是恢复输入而非同名浮点原子exact_mass的重复；两个joint报告分别记录可行与可分离，亦不能因没有跨H新障碍就丢弃。

本代理实际执行仅限只读导出展示、JSON解析、原子对应/字段/维度/行名一致性检查；LP/定价/发现/随机搜索/原审计/精确分离重放均**0次**。没有新增运行证书，没有声称全域最优、SPE反例、外审、新颖性或六人结论。
