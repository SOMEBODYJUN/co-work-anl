# 同一∞输出的M-LP接口及原InfDegreeTwo存在性的3B比较

对同一符号∞helper输出，整数、原始CONFIG和阈值规范化M-LP分别有独立的全正阈值保持证明；三个证明不能以松弛同名互相替代。明确T-block源族同时给原InfDegreeTwo的CONFIG/M-LP存在性gap与降度后交域的精确CONFIG值，但两处玩家人数不同。

本报告对应Boss6任务`boss6-inf-chain-transfer-3b-ea6be0c00b1186cf`。五个核心：F=M-080d9b22ae87408f9a673a898c7a6dc3（当前v4），A=M-16209762a32e42e48ec20b76381b5e9d（v1），B=M-7bc9eab74ecd475db7df33c3f4b75e61（v1），D=M-a9534c70ffa74fca9a91cd270468de3f（v3），G=M-b126c4b3ff29400589f7f38abdca4d85（首读v3、随后仅scope/evidence定向纠正）。额外直接桥H=M-b86375379821448d857231e8c38d8f46；cap边界C=M-b6605b3864cb41e399d926496739f12d。实际绑定的最终对象版本/pin和文件SHA以收据/ledger为准。

clone只读；本报告、边草稿和收据只在指定staging写。未执行Git、work.py、队列或公屏写入，未重跑旧数学程序或证书。accepted为数学判断，最终native绑定、check、发布由Root串行处理。

## 1. 共同模型与五端点的完整目标

有限非空玩家、有限可空物品、非负加性估值、物品不可分且单归属。估值为二进制有理或符号∞。原始CONFIG(s)每玩家全部达s配置质量和一、每物品总边际≤一；这不是联合整数随机分配。Degree与InfDegree首先约束物品侧。

F的有限unit-helper合同正向只限所保目标≤1，反向任意正阈值；两个最高目标等式分别要求旧actualOPT或旧CONFIG最高阈值≤1。原估值不必每端≤1。D是固定t>0的整数合同，不自动含全阈值或CONFIG。A先造同一J∞再对全部有限s>0分别保integer与CONFIG，另有物品∞端排序、计数及给定证书位复杂度。B是明确J_T的ConfigOPT=T、整数OPT=floor√T、N=T³+T、两侧∞度≤2及物品总正度≤3，gap为该族Θ(N^(1/6))。G只要求原InfDegreeTwo存在参数族的两种LP gap为Ω(n^(1/4))，不要求每实例gap或一般两LP同值。

对这五个端点已完整实读当前对象记录、指定正文、必要证据及原PDF相应页。F v4唯一变化为其他evidence中P_gate全任务调度补全：root pin留root、未选connector留root、未选selector去gate、其余incidence留private。其unit-helper主body SHA8bfbaa…和模型/statement/量词未改；本轮直接读当前补句与全部SC路径主证明，没有将该delta扩大成另一门控菜单审查。

## 2. M-LP原方程与额外全阈值桥

原PDF SHA为7f7b21ff…；本次直接pdftotext导出实读印刷页6–8、12–13，且渲染页7核公式。Definition2.2先依M/λ重估大端为M，式(4)–(8)是列容量、big质量+z≥1、small效用≥Mz、每small x≤z及非负。先将全部零端x置零，仅改善容量与small上界；并无行总x=1的约束。

H的独立完整证明已在正式主正文给出，本报告复述关键承重以说明真实比较。固定I先建同一D∞(I)，每条d>3物品链有d个专属副本、d−1位仅在相邻副本取∞的helper。对每个M>0、λ≥1，原正端大小分类与small系数逐副本相同；新增helper正端全big。正向记q_r=x_{i_rj}、Σq≤1，补w≥q、Σw=1，前缀W_k=Σ_{r≤k}w_r。旧x按专属副本重命名、旧z保持；helper z=0、左右big x为1−W_k和W_k。各副本helper负载恰1−w_r，加旧q_r≤1；原行(5)–(7)逐项不变、helper行全部成立。

反向先去零，helper无正small端，(6)给0≥Mz_h而M>0迫z_h=0；(5)迫两big质量≥1。d列容量扣d−1名helper总占用≥d−1，得旧owner自己的副本总边际≤1；合回旧物品，旧行所有正系数与z保留，恢复全部约束。故同一数值M与同一数值λ下双向保持，固定λ的正可行集合相等。此集合不必前缀，上确界相等不依赖二分单调性；也不能把λ=f(n)换成λ=f(N)。

H不依赖CONFIG→M-LP或M-LP→CONFIG接口。本3B不重复其主3A边；只在实际注册后以精确SHA复用或将其作为额外比较证据。

## 3. 不同松弛、有限helper与真实阈值边界

原CONFIG(M)到规范化M-LP的正向成立。重估R不是点态不减；准确理由是每个原达M配置，若含将被重估成M的端则该端已足，否则全部值不变。含big配置剪为big singleton，其余small配置总质量作z、物品边际作x，立得(4)–(8)。未经此canonicalization不能声称任意原配置的全部边际自动满足small x≤z。

cap λ=1不能无条件回原CONFIG(M/2)。n≥4、n−1件共享值v=(n−1)/n、每位一件私有值a=(2n−1)/n²时，raw整数与CONFIG最高值均a；cap正可行集合精确(0,a]∪(v,1]。低段私有big可匹配；中段(6)/(7)逼z=0而n玩家争n−1共享；高段全部small，shared x=1/n、private x=1、z=1给行值一；M>1时全实例总值n不足Mn。n4在M1可行、raw CONFIG1/2不行，已否定一般二倍接口且表明非前缀。

安全小端结论由切片顶点直接证明：给small x/z≤1且Σp x/z≥M，先逐坐标下减到加权和M；立方体加一条加权等式的每顶点至多一分数坐标，凸分解后丢该分数坐标，剩bundle值≥M−pmax、边际不增。乘z、补big singleton并按总质量≥1归一，即得规范化CONFIG(M−pmax)存在；若pmax≤M/2才有M/2，原值big解码还限M/λ。本文不借这条存在性论证冒称多项式显式分解算法。原Theorem2.3首步的重估/减z/截x不能在cap反族点原样用，不能把其印刷文字当作无前件cap结论。

有限H的integer/CONFIG只保0<s≤H；存在d>3链时s>H每helper需两件副本，2(d−1)>d而不可行。M-LP有所不同：正向至少M≤λH时helper为big可用上节的前缀公式；反向全M成立，超过λH时helper全small、z≥1，耗量≥M/H>λ≥1仍可扣总容量。d4,H1的helper两端x依次(1,1/3)、(2/3,2/3)、(1/3,1)、z均1，给cap目标4/3；配旧玩家私有100可使完整输出cap最高4/3，但raw整数/CONFIG最高一。旧4人private100+shared100实例cap最高125，raw二者100。故不能将CONFIG的高阈值无解理由照搬给M-LP。

## 4. 明确交域族投影回原人数的完整G推导

B的明确构造是J_T=D∞(I_T)。源I_T有T个block、每block一root a_r和T位b_{r,k}，物品u_{r,k}、w_{r,ℓ}；root对本block全部u值一，b_k对自己u值∞、对本block所有w值一，另T−1件B_r给相邻root值∞。其原人数n=T²+T、物品m=2T²+T−1。只有T²件w的总正度T需降度，新增S=T²(T−1)给J_T人数N=T³+T。B携带的是这份明确族及其完整输入，而不是任选存在性实例。

从B精确J_T的两个raw目标，A的反向全阈值投影恢复I_T的ConfigOPT=T与整数OPT=q=floor√T。独立直接验证也成立：root在full-u配置质量1/T、相邻B singleton总质量1−1/T；b在自己u singleton质量1−1/T、full-w质量1/T，各物品边际一。s>T时每个root都必须含B，T行对T−1容量矛盾。整数任一正最低值V时有root无B、拿s≥V件u，失u的s位b要求sV≤T，给V²≤T；每root取q件u、相应q位b各取q件互异w，其余b拿∞u，达q，故精确值成立。

取固定λ=2、整数T≥4，T/λ≥2，所有单位端严格为small、全部原∞端为big，重估后∞/big度并未增加。I_T物品∞度≤2：u为1、w为0、B为2。对CONFIG(T)证书作§3的big-singleton/small质量映射，得到M-LP(T)。甚至可直接写：全部root及b的z=1/T；root每u x=1/T；b自己big u x=1−1/T、每w x=1/T；B_r左右质量(T−r)/T与r/T。每行big+z=1、small效用1=Tz、small x=z、各列容量一。

因此两种LP各自除以同一整数OPT得到至少T/q≥√T；又n=T²+T≤2T²，故

T/q≥√T≥2^(−1/4)n^(1/4)。

取无限多个T完成G的整个存在性statement。这个whole关系使用A与B：B给明确J_T=D∞I_T和精确数据，A把两raw目标恢复到人数n的I_T；CONFIG→M-LP正向是本节已直接付清的证书映射。新H不承担这条必要步骤，因此不能为了新节点连通把它塞入ALL前提。原PDF脚注本身没有提供完整I_T，本文及已登记正文明确提供补充证明。

另一方面，J_T上的两raw目标为T与q、新人数N=T³+T，所以交域CONFIG gap是Θ(N^(1/6))；不能仅凭B抽象N指数1/6句子反推n指数1/4，必须使用其明确构造和A的反向投影。H可另证该J_T的M-LP也保同目标，正文还核任意λ的最高M-LP参数max(T,λ)，但那不是G存在性所需的前提。

## 5. 复用、补充比较与闭合范围

本3B不重复三条已成熟关系：F→D的固定阈值缩放、F→A的同一∞输出扩展、A→B的明确精确交域迁移。已逐一完整实读其最终canonical JSON及实际推导，核其路径在当前registry.edge_files中，并按精确SHA列入本收据assets，借同一已接受边覆盖相同作用。

本包独立新关系为ALL{A,B}→G的上述whole迁移。G v4已实际将“完整构造在primary”scope最小更正为“primary印刷页13仅脚注存在性，完整I_T在补充正文”，并添加准确证明evidence；statement、模型和truth_status不改，没有改动共享PCSP汇编全文七对象。当前v4完整record及新增evidence均已实际读取，所有数学步骤已付，不应虚留conditional/open。

H与C的直接主边另有主3A任务。本包比较它们的实际用途，准确区分不把A的CONFIG证明冒作H，不把C误称反驳G；C的原族人数n与D∞后人数n²−n+1也不能混。H、C正式record、body及准确审查evidence均已实际读取；本收据仅复用上述三条已有canonical边，不预填或重复H/C的新主3A边。

本任务无declared follow-up，故closed_overlaps为空；普通端点比较和本轮发现的边界列additional_comparisons。实读范围是任务当前五端点及这里具名额外对象；没有宣称不存在仓库其他潜在关系，也没有全仓重审。

## 6. 实读证据与发表边界

原PDF直接导出页6–8、12–13，页7视觉核公式；既有maxmin.txt只作定位/对照，不冒称本轮全文49页审读。完整读A/B主正文、其独立274行复核、F成熟76行正文及五evidence的相关内容、PCSP汇编的MaxMin语境。外部历史scratch的canonical Exact/Proof未再取得，未把审查中列SHA冒作自己原稿实读。

新H正文及其独立审读对全部(4)–(8)纸面验证，cap反族全部四区间与D∞计数在本轮再次核算。精确字节、读取范围、对象pin与reuse边SHA另列reading-ledger.json；最终native bind/check与推送由Root实际执行，本worker不把尚未执行的工具结果写为PASS。

## 7. 最终任务与正式引用核对

沿同一任务恢复。G v4 plan回执request为75a766b001934e86bc90a3a67f9f25aa，remote tip为486087e32fa376f099ca14eb2f672198ae44aff2；H/C read-add回执request为2970cfc04ab94034a9c1c271c27d7aba，remote tip为a97f3b36d69bf333f9bacc16d2cd1cc2e132f9e3。实际读取两份native日志的pushed/request/remote/local-sync字段，并实际读取当前task全文：仍claimed Boss6，五core和两个read。当前task字节SHA为deb1398b3fbd448e3b0c9947c4f05aae692f6bd9f06f0ad1da542a644fe61cc4。对七个指定当前完整object记录按稳定规范JSON逐一计算pin，全部与task.input_pins一致；具体值在ledger/receipt列明。

正式H正文SHA为f07cd5f7128a9e8ac0f4667b8e69f5d89905b8d4e4d999edd090612cb95a9dfb，已以审定08fb全文加正式差异完整对读；正式C正文SHA为b3454530c3cfff2700e16d39114ade01a645526863d5130efcc61e5253c3fece，已全文实读。独立审查的正式副本与已全文实读的staging字节分别同为18e0e2725aca9fd8fe6887b8dcade0f033887ac2f6db7a704a505c00893515cf和e5a5ce699585185b304799e0db30debf8e1d5f9d46b79f70f5977707ec512978。新edge所列三段formal evidence的文件SHA和唯一标题已直接核对。三条reuse仍在当前registry.edge_files且字节SHA未变。

这里只完成本包对象、正文和元数据的定向核对，没有声称读完这些remote提交的其他内容。新edge保留无native binding的数学accepted稿，Root复制后执行edge-bind/edge-check并刷新其asset SHA；本worker没有执行该检查，也不将其提前写为PASS。H/C主3A另按其实际任务推进，本包不填未来任务号或伪follow-up。
