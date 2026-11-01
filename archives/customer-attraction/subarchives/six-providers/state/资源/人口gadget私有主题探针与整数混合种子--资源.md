---
id: customer-attraction/population-gadget-private-topic-probe-and-integer-mixture-seeds
kind: resource
type_tag: 资源
title: 人口gadget私有主题探针与整数混合种子
status: four-whole-primary-sources;historical-finite-BI-report-retained;static-clone-coverage-audited
truth_status: legal-integer-seeds-and-coverage-arithmetic-verified;equilibrium-readings-retain-original-finite-report-status
review_level: informed-source-and-dependency-review;one-independent-static-coverage-check;no-new-SPE-or-LP-run
scope: five-unit-providers-seven-topics;12-private-weight-inputs-and-six-integer-mixtures;no-universal-efficiency-or-population-monotonicity-claim
summary: 四源8665B完整读取，保存12项私有权扫描和六项顶点混合的全部字段；两个127维种子完整解码，interior恰为old+100new；只独立核整数覆盖与OPT/比值，不把882保留终局计数或唯一根计数当完整策略唯一性。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/population_gadget_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/population_gadget_probe.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/population_gadget_seed.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/population_interior_seed.json
---

# 人口gadget私有主题探针与整数混合种子

四主源为1978B程序、4136B报告、1291B原gadget种子、1260B混合种子，共8665B，均正常读取冻结全文并核size/SHA256/Git blob。它们是一个五人七主题有限构造资源，不是六人half结果、一般人数定理或主目标反例。这里同时保留原精确BI输出的历史身份、完整合法输入及本批独立静态覆盖核验。

## 模型、来源和两个门槛

原模型为有限单位客户、有限非空共同主题目录、单位提供者依次观察全部有序历史选择主题；客户在终局覆盖自己的提供者间均分。整数重数表示不同但兴趣相同的单位客户，不是战略大客户。允许零类型、空主题、重复选择与全部离轨平局；本资源实际输入m=5、主题标签0…6。

兴趣mask j=1…127的第j项是恰喜欢j的二进制置位主题的客户数，数组从零下标j−1存储。两种子文件根仅有`scope`与`exact_candidate`，后者仅`integer_clones`；它们没有自带玩家数、目录标签、完整策略、certified状态或效率结论。m5/k7来自调用程序与相邻报告，不能把文件名当成认证。

起点是[十二客户人口非单调例](../../../../state/反例/人数增加的十二客户全部均衡福利下降--反例.md)：同一三主题实例三人全部SPE福利12、四人全部11。该例不反half。将它每类型复制四倍得本资源的六种core兴趣，总48客户；再添四私有主题并改为五人时，原三/四人完整策略不会自动保留，需重新求真实续局。来源/启发不等于“加人加题保SPE”推导。

本报告的`ratio`方向是OPT/最差SPE福利，half违反需ratio>2。相邻热启动研究的9/5是一个已知五人坏例和指定目标，不是主half的门槛，也不是由本探针证明的全称上界。以下最大有限读数8/5仍小于9/5和2。当前[五人half定理](../../../../state/定理/五人半覆盖--定理.md)已普遍证明，本旧五人搜索不能再作为五人half仍开放的依据；六人一般问题也不由这些点解决。

## 十二个私有权输入与报告的全部首块

记前三主题A=0、B=1、C=2，另四主题3、4、5、6各有t名私有客户。core为：

| mask | 兴趣 | 客户数 |
|---:|---|---:|
|1|A|12|
|2|B|12|
|3|A,B|4|
|4|C|4|
|5|A,C|8|
|6|B,C|8|
|8|3|t|
|16|4|t|
|32|5|t|
|64|6|t|

其余117种兴趣重数为0；总客户48+4t。三个core单题大小24、24、20；最佳core两题AB覆盖44；三题覆盖48。五个比较槽可用一次最好core加四私有、两core加三私有或三core加两私有，所以静态精确值为

\[
\mathrm{OPT}_5(t)=\max\{24+4t,44+3t,48+2t\}.
\]

少于这些主题的组合可补入不减覆盖，故无遗漏。t=1…4取48+2t，t=4…12取44+3t（t4并列）。这是全部覆盖组合的直接分析，不是SPE结论。

4136B原报告顶层首七字段为`scope`=`12 finite legal seeds only; no general theorem`、`source`=`sibling continuation_order/population_paradox.md, original gadget scaled fourfold`、players=5、topics=7、base_types={1:12,2:12,4:4,3:4,5:8,6:8}、added_types=[8,16,32,64]以及以下完整rows。另第八字段是后面的六点混合块，不应被首句“12 seeds”漏掉。

下表q是七维**终局计数**，不是五步有序路径；程序从最差福利根计数集合中取字典序最小q，未输出全部最差根集合或完整策略。

| t | 原worst_root q | 原worst_welfare | 原optimum | 原ratio=OPT/W |
|---:|---|---:|---:|---:|
|1|(2,2,1,0,0,0,0)|48|50|25/24|
|2|(2,2,1,0,0,0,0)|48|52|13/12|
|3|(2,2,1,0,0,0,0)|48|54|9/8|
|4|(2,2,1,0,0,0,0)|48|56|7/6|
|5|(2,2,1,0,0,0,0)|48|59|59/48|
|6|(2,2,1,0,0,0,0)|48|62|31/24|
|7|(2,2,1,0,0,0,0)|48|65|65/48|
|8|(2,2,1,0,0,0,0)|48|68|17/12|
|9|(2,2,1,0,0,0,0)|48|71|71/48|
|10|(2,2,0,0,0,0,1)|54|74|37/27|
|11|(1,1,1,0,0,1,1)|70|77|11/10|
|12|(1,1,1,0,0,1,1)|72|80|10/9|

十二点内最差比为t9的71/48，不可从t1…9的同一计数外推更大t仍保它。t10与t11已出现不同最差计数，说明添私有客户改变激励。原报告未冻结代码SHA、环境、命令、时间、逐状态集合或SPE策略；“worst”属性在此保为原精确solver的有限输出，不冒本批重新验证。

## 两个127维种子的全部语义

`population_gadget_seed.json`的scope原文为`scaled colleague population gadget plus private topics; legal seed only`。完整127项恰为上表t=9，各非零项为(1:12,2:12,3:4,4:4,5:8,6:8,8:9,16:9,32:9,64:9)，其余全部0；总84名单位客户。它是扫描中71/48输入，文件自身不保存任何完整策略证书。

可选混合使用相邻`restricted_m5p7_population.json`的`exact_candidate.integer_clones`作新向量v；本批只完整读该127向量与相关元数据，**未读取或复核它的2801行动表**。其全部非零项是(7:5,16:1,32:1,72:1)，其余123项0，总8客户。mask72=8+64表示同一客户同时喜欢主题3和6；不能误拆成两位私有客户。

相邻原文件记录固定root(2,2,1,0,0,0,0)、比较组合(0,1,3,4,5)、exact value8/5、W5、OPT8及固定策略锥的exact dual8/5；`restrict_outcomes=true`和浮点最优状态属于受限搜索，不构成全策略全输入界。这些大文件的完整策略由另批独立处置，本批不借`certified=true`虚称已审全部动作或对偶。

新v上0/1/2三标签覆盖相同五客户，3/6覆盖相同一客户，4与5各一客户，实际四覆盖类。其端点“8/5”本就对应五人全big的结构，不是七个不同极大主题的新下界。原README另称v有81根终局计数、全状态保留2506，但这些不是本四源报告直接输出的独立端点统计，本批不重跑或认证该旧叙述。

`population_interior_seed.json`的scope原文为`legal interior mixture seed only`。完整127项非零表为：

| mask | 重数 |
|---:|---:|
|1|12|
|2|12|
|3|4|
|4|4|
|5|8|
|6|8|
|7|500|
|8|9|
|16|109|
|32|109|
|64|9|
|72|100|

其余115项全0，总884客户。逐一比较所有127坐标得准确关系

\[
\boxed{c_{\mathrm{interior}}=c_{\mathrm{old}}+100v.}
\]

因此它正是下表f100那一个输入，不是额外一例未记录的实验。它并非127维非负正交体内部点，因为115坐标仍零；“interior”文件名也没有提供相对哪一个锥的严格内点证书。两个数组都仅断言合法整数输入。

## 六个混合点及不随计数误读的退化诊断

若相邻restricted文件存在，程序取其v及old种子，依次检查f∈{1,2,5,10,100,1000}的c=old+fv。原报告完整第八字段`finite_vertex_degeneracy_probe`含以下六行，每行都有new_to_old_scale、root_221_realizable、root_outcome_count、all_state_retained_outcomes、ratio：

| f | root_221_realizable | root_outcome_count | all_state_retained_outcomes | ratio |
|---:|---|---:|---:|---:|
|1|true|1|882|79/53|
|2|true|1|882|3/2|
|5|true|1|882|111/73|
|10|true|1|882|151/98|
|100|true|1|882|871/548|
|1000|true|1|882|8071/5048|

其中root_221指完整七维计数(2,2,1,0,0,0,0)。`root_outcome_count=1`意为根可实现终局**计数**集合只有一元素，不是完整历史纯SPE唯一，也不是有序在轨路径唯一。`retained_outcomes`由规范solver定义为Σ_(全部已缓存计数状态c)|E(c)|，882不是客户数、历史数、策略数、根终局数或简单状态数。

覆盖可独立精确分析。根221覆盖old的48客户和新v的5f客户，所以W(221)=48+5f。最优取A、B以及私有标签3、4、5，覆盖old的71和v的全部8f；任何三core+两私有至多66+7f、一个core+四私有至多60+8f，两core至多71+8f，其余更少。因此对所有非负整数f，**静态**OPT=71+8f，q221的比值为(71+8f)/(48+5f)。这解释表中所有精确分数。该比随f增大并趋于8/5，因为分子导数交叉差8·48−5·71=29>0；这不是对表外f的SPE可实现性、唯一根或882统计的外推。

混合两份客户数组保证合法输入，却不会在没有同一完整策略对二者共同可行的证据时自动保留某份SPE。原脚本确实每个f重新调用全终局solver；不能把这次有限反馈现象概括成任意实例的退化复杂度定理或一般插值定理。

## 原1978B程序的完整合同

程序无CLI参数、无main guard；模块顶层从自身祖先中找含`customer_attraction/__init__.py`者为ROOT，把ROOT及ROOT/tests/audits置入sys.path。它从策略锥审计模块导入`instance_from_clones`，从规范包导入`ExactSPESolver`。即便只用克隆构造函数，前一个模块顶层仍导入NumPy/SciPy；不能说本探针仅需标准库，也不能把import称只读操作。

首块构造长度127的非负整数组c，在mask1/2/4/3/5/6赋固定core，mask8/16/32/64赋t=1…12。每次instance_from_clones(7,5,c)把非零mask展开为单位客户类型；solver.worst_outcomes返回所有根最差福利计数，min按字典序取一个。i.welfare(q)、i.optimal_welfare和solver.inefficiency_ratio填五个行字段。

可选块只由`restricted_m5p7_population.json`是否存在触发；存在时还要求同目录old种子可读，以zip(new,old)逐坐标计算六份数组，并调用outcomes/stats/inefficiency_ratio。代码没有数组长度相等的断言，zip一般会截短；本次冻结三向量全为127项，静态核已排除实际截短。它**从不读取population_interior_seed.json**，该种子是独立保存的同f100输入。若restricted不存在，只保存十二点首块；不可拿缺失可选输入的运行复现完整八字段报告。

最后以`Path(__file__).with_suffix('.json').write_text(...)`覆盖写同名报告，再stdout打印单个JSON。没有拒绝覆盖、排他创建、运行日志或代码自指纹。为保持原证据，本批只保存原件并补齐直接import/数据依赖，未import或运行该模块；未来复现应另复制运行树。

## 规范solver保留完整历史量词的原因

已实读并按冻结SHA核同规范model/exact/__init__/certificate和导入helper。对终局q，收益是Σ_(兴趣包含动作a) c_I/(Σ_(b∈I)q_b)，福利是被q支持命中的客户总重数；optimal_welfare枚举至多五个不同主题支持。规范exact以Fraction作比较，保根全部可实现终局计数：

\[
E(q)=\{q\}\ (|q|=5),\quad M(c)=\max_a\min_{q\in E(c+e_a)}u_a(q),
\quad E(c)=\bigcup_a\{q\in E(c+e_a):u_a(q)\ge M(c)\}.
\]

必要性来自每个偏离孩子都须给当前玩家一个可实现续局；充分性是在未选孩子独立选择最低收益的真SPE，在选中孩子实现q，再用阈值确保当前最佳。按剩余深度归纳，这保任意有序历史平局。按计数缓存的是**可实现集合**，不是强制所有同计数历史采取同一动作的Markov策略。本探针没有调用certificate/verify_certificate来保存或逐节点核任何完整策略；四主源只有计数与数值报告。

可复用[全历史终局递推资源](../../../../state/资料/全历史纯SPE终局搜索的递推与有限证据--资料.md)比较另一个独立整数实现，但旧27136输入/13次交叉核验不是本18个输入的新核验，也不使本原报告自动多出完整策略审计。

## 本批新增核验与可接续停点

没有查到本1978B原程序同SHA已成功运行的独立记录；旧人口悖论审计验证不同人数/输入，不能借来认证此18点。四原件的状态仍是原有限精确solver报告，而不是本次新SPE通过。

本批只另写并**执行一次**独立标准库整数覆盖检查：不import原模块或规范包，不跑solver/IC/LP；读取全部三127向量，核old+100new逐坐标相等，并对12+6原报告输入枚举至多五主题支持。全部显示q覆盖、静态OPT和精确比值均匹配。检查源码、输出及四输入SHA绑定在[证据包](../../tools/evidence/population-gadget-probe-primary/README.md)。这可以核源数据及分数，不验证q为SPE、最差SPE、根集合唯一、882统计或原LP对偶。

后续若使用该seed作新策略搜索，应保完整依赖及原限定状态，重新比较真实后继；若要声称同一策略对整段混合可行，须提供共同策略及其逐行线性IC证据。原人口单调反例、此有限私有扫描、受限DAG优化、已知8/5端点及当前五人普遍half各有不同量词，不能互相代替。
