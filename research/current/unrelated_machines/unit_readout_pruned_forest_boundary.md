# 单位读出双树：配额森林恒等式与半密度三半障碍

读取目的：把原两树强制器开放并接入源clauses后，所有低负载实际调度到底允许哪些组合对象写成精确双向合同。它是既有 unit-token 机制在一个 all-variables 森林上的专门正规形，不主张新的普适 token identity；不提供源问题困难性。第6节进一步证明arity≤2A的整个单位读出模型，无论深度和接线均有三半调度；超出该密度或成本合同的designer仍需独立分析。

## 1. 精确Claim对象、定义和量词

**ID/version：UM-UNIT-READOUT-PRUNED-FOREST-IDENTITY-v1。**

Objects：有限变量集V；整数k>=1,h>=1；每变量两棵内部机器完全私有、彼此也不重合的完整k叉深h树，符号为正/负。内部机器是深0,...,h-1的节点；深h的“叶”是实际port jobs，不是额外内部机器。不同变量的内部机器不共享。

Original jobs：

1. 每变量一枚selector job，只能在该变量两根之一运行，时间均1。
2. 每内部parent-child边一枚独立job，父端时间1/k、子端时间1；无其他有限端。
3. 每内部深h-1节点有k枚不同leaf-port jobs。每枚在其父端时间1/k，另属于恰一个clause c，可在该clause任一unit slot运行、时间均1；没有其他有限端。

每clause有非负整数容量A_c，arity_c为接到它的port jobs数。可直接使用A_c台不同slot machines；也可只建立q_c=min(A_c,arity_c)台，它们对所有port分配完全等价，因为外送port数不会超过arity。每slot只资格接收本clause的ports，没有preload、其他jobs或跨clause机器重叠。若A_c=0，该clause的port只有内部有限端，仍是合法UM任务。

上述是全部原始任务、机器和资格；不隐藏额外状态。给有理数C属于[1,2)，令

    r=ceil(k*(2-C)),   1<=r<=k.

Definition：一个必选r配额森林为：对**每一个变量**恰选一个符号根；从该根出发，每个选中内部节点恰选r个孩子（深h-1时是r枚leaf-port jobs）。未选轨及未选分支不属于森林。另为全部选中leaf ports给出其所属clause的slot注入，等价每clause的选中leaf数<=A_c。

**Exact Statement / Conclusion。** 对每个上述显式输入及每个C属于[1,2)，存在完整实际调度makespan<=C，当且仅当存在必选r配额森林。给任一方向的实际见证，可确定性总位多项式构造另一方向见证。调度正规化后的每active内部机器负载精确为1+(k-r)/k，其余内部机器负载至多1，unit slots负载至多1。

Domain / Scope：只包括这些私有树、unit selectors、固定clause读出及无额外外部负载。所有变量mandatory，不能只取某一根的可达分量或遗漏难变量。V为空时是空森林及空原任务的显然边界；需要UM至少一台机器时保留一台空闲机。以下证明写V非空的实质情况。

## 2. 实际调度到必选森林及完整正规化

给实际sigma，Cmax<=C<2。每变量selector恰放一个符号根，给该根一个unit incoming。这是每变量必选根，不需要未知源赋值。

从该根递归。某active内部节点已有一个unit incoming（根是selector，其他点是其唯一parent-edge job）。它有k个本地outgoing jobs，每个若留下耗时1/k。于是留在父端的数量至多floor(k*(C-1))，至少

    k-floor(k*(C-1))=ceil(k*(2-C))=r

个outgoing jobs已在原sigma中放子端或外slot。只从这些原已下传jobs中，按固定次序选r个。

内部孩子只对这r条边递归；深h-1节点只保留原来已外放的r枚ports。对其他孩子分支，把连接edge改放原父端，该整个分支所有内部/leaf jobs改为各自父端。另一整轨同样全部放父端。selector不变。

这个构造是同时定义全部原jobs的最终目的地，不是在中途超载态上假设最终结论。每active内部节点最终恰有k-r个本地small jobs，并有一个incoming1，故负载恰1+(k-r)/k<=C。每inactive节点没有incoming，它全部k个本地outgoing之和恰1；其父edge已经放在父节点，不会被重复计入本节点。未选轨同理。不存在重复父亲，因为内部骨架是私有树且每条边只有一枚job。

每个最终选中leaf port原本就在外slot；保留它原先实际slot。C<2和外部时间均1保证原sigma每slot最多一枚port，且没有其他外部jobs或preload，因此保留子集仍是注入。最终每clause选中叶数<=q_c<=A_c。

所以构造既给必选r森林，也给完整合法低负载正规化sigma'。这里的“所有外叶是原外叶子集”是承重事实，未重新使用一个可能不可行的fractional残余容量。

## 3. 必选森林到实际完整调度

给森林和注入。每selector放相应根。每active节点的r个选中outgoing放所选孩子或给定外slot，其余k-r个留父端。所有非森林分支及另一轨的jobs全部放父端。

每active内部节点恰有unit incoming，负载1+(k-r)/k<=C；每inactive内部点负载1；每slot最多一个unit port，负载<=1<=C。每个原job恰被放一个原有限端，完整合法，不是只给选中边的partial solution。故反向成立。

## 4. 边界、构造性和总位复杂度

k=1时r=1，所选轨只能沿唯一链到外叶，正规形仍正确。h=1时根直接有k枚leaf ports，归纳无内部child层，所有计数不变。C=1时r=k，全部所选轨叶都须外送；C趋近2但仍小于2时r至少1，没有将r=0漏入。A_c=0会使任何到它的选中leaf不可能注入，恰对应其单位port不能外送的实际限制。

树和ports均显式输入；算法扫描每个原job至多常数次，搜索/剪枝时间多项式。r用精确有理乘法和向上取整，不遍历C分母或按其倒数循环。k个outgoing jobs已在输入中，未以二进制巨大k偷偷建未列任务。slot数可用min(A_c,arity_c)，故binary A_c不会造成伪多项式展开。外叶给现成sigma slot时直接复用；从计数给注入时按编号占前若干slot即可。

Dependencies：非负实际负载、unit job在C<2时单slot至多一枚、私有树唯一父结构、整数floor/ceil恒等。未调用配置LP、MMDA算法、PCSP困难性或任何未重构的近似定理。

## 5. 与既有单根token桥、BCG森林模型的扣除

既有 `rooted_dag_degree_token_bridge.md` 的UM-DAG-DEGREE-TOKEN-IDENTITY-v1从一个mandatory根出发，其他顶点只在该根可达时收费，定义单树b*并证明OPT=2-b*。本页有每变量一个独立mandatory selector，**所有变量都必须保留**，并在固定阈值C处要求精确r子配额。不能给一个全局根随意选择部分变量，然后沿用b*分数声称仍覆盖所有源变量。若强加新的全部变量必达约束，已改变对象，必须另证。

Paper Fact对照已实读仓库原始作者PDF：Bateni–Charikar–Guruswami TR-848-09，§4.1 Definition4.3、Lemma4.6（印14–15，注册manifest定位pp14–16）。其M-pyramid包含所有原sources，严格说是forest of arborescences；每非sink至少M孩子，且输出sink须为原sink。先按§4.1删除拥有至少两个big items的players后，Definition4.5的依赖图与剩余InfDegreeOne子实例在Lemma4.6中有保持M的多项式对应；回填原实例的Lemma4.7只保证floor(M/2)。因此“多sources全mandatory森林”及unit资源不能重复的机制本来已有，不是本页新发现。

本页专门合同与该Paper Fact也不应逐字混同：selector选择点只有选一个符号根，内部树配额为r，选择点不是统一M>=r的branching节点；所有branching骨架是显式私有k叉树，clause资源是unit slots。它是已知all-sources/token机制的阈值正规形及当前源读出对象的精确记录。未重构BCG后续近似算法或从其困难性获得新的近二结论。全球新颖性和独立论文价值未认证。

## 6. 半密度条件下，任意深度、任意接线都不能保留近二间隙

**UM-UNIT-READOUT-HALF-DENSITY-THREE-HALVES-v1。** 保持第1节完整单位读出模型，另假设每clause的实际port arity满足d_c≤2A_c。对每个整数k,h≥1、每个显式变量集和任意wiring，可确定性总位多项式输出全部原jobs的实际σ，所有内部机器负载≤

    1+floor(k/2)/k ≤ 3/2,

所有clause unit机器负载≤1。k1时全部≤1；V空为OPT0。非空实例selectors又给OPT≥1，故同时是这个具体结构类的三半近似；下面锐例只证明绝对T1界锐，不宣称近似比紧。

这是经典ST半质量有序槽的直接推论，不是新近似算法。证明自足如下。

每内部机器恰有一枚incoming任务在本机用时1（根为selector，其他内部点为父边job），并恰有k枚outgoing任务在本机用时1/k。每件原job在两个原端各放半片：selector在两根、内部边在父子；port在父与一个合法的外部unit。对clause先把d_c枚ports任意两两配对，给第t对使用第t台unit；只需ceil(d_c/2)≤min(A_c,d_c)台。每port的另一个原外端仍可用，不删资格；这是构造matching时固定一份合法半质量证书。

每内部机器把incoming半片排第一，随后k个outgoing半片，每两枚为一槽。每clause用到的unit只有一槽，含至多两个port半片。每job恰邻接两个不同槽、每槽至多两半片，所以任意job子集S有2|S|≤2|N(S)|；Hall匹配一次覆盖所有job。匹配槽所属机器即原合法实际σ。

若incoming匹配至本机，它占首槽，其他可匹配outgoing数≤ceil((k+1)/2)−1=floor(k/2)，负载≤1+floor(k/2)/k。若incoming不在本机，至多它原有的全部k个outgoing留下，负载≤1。每外unit只一槽，实际至多一件时间1的port。未用unit负载0。每原任务恰一次，所有内机和unit在同一次matching共同满足界；没有先独立选各机最有利任务。

k1、h1、A_c0（此时d_c0）、空变量和任意大binary A均合法。slots最多原job半片数，实际外机可截min(A,d)；对完整原P中其余可用机补零负载即可，不按A数值展开不存在的任务。复杂度按显式树/port/资格及二进制容量总编码长度；不是按压缩log k、log h展开树。

**绝对三半锐性。** [双轨编码](dual_rail_threshold_soundness_boundary.md)的split四clause例恰为k2,h1：三变量、每sign两leafports、四clause均A2、arity3≤4。14机器15jobs真实OPT3/2，已给完整原P及8种selector容量下界。可直接取所有selectors在正轨，正ports外送但将第一clause的一枚x+port留x+轨；四clause外送数变为2,1,2,0，逐一注入各两unit；x+轨负载3/2，其余轨≤1。无C≤1及半整数负载网格给下界。这里复用同一锐例，不重新复制资产或把slot模式枚举冒称物理σ枚举。

由第1节等价，该条件下每变量必选的r=ceil(k/2)森林一定能共同packing。树深、端口排列、选某种“纠错wiring”不能改变本节量词。要用这一类部件做超过三半的NO阈值，必须改变至少一项已声明条件，例如clause密度、单位incoming/归一化small总量、私有树结构或外部容量耦合；没有证明这些更一般模型也可三半。

## 7. 完整实际源NO证书与局部预载模块不混域

[实际证书](../../../examples/unrelated_machines/unit_readout_two_tree_actual_certificates.json)含以下六份完整原P/σ；[独立读取核验](../../../tests/audits/unrelated_machines/unit_readout_two_tree_independent.py)不导入生成器，逐条重建树资格和每机负载。有限检查为4440个任务归属、2544个机器负载、两个NO版本各128个源赋值，不承担一般定理。

k4,h3时每sign21个内部机器、64枚leafports。七变量与全部128种七元符号clause、每clause A4，给806机器1183jobs的unit实例。每变量选择负根，沿每个word digit<2的二叉pruned tree下传，仅8枚负叶外送。将这些叶逐一接到该变量为负且总负文字数≤4的clauses中，其余叶与剩余同sign出现按序双射；合格clause至少32个，足供8叶。每clause选中叶≤其负文字数≤4，注入四unit，全部active内机3/2、inactive内机1。源任何赋值都有全七真clause，连弱阈值6也无解，实际却C3/2。第6节现在更强地覆盖同密度**所有**wiring，故此具体证书不被误当作全部接线的唯一反例。

同一完整证书另含单外端时间1/4的比较版（422机器1183jobs），同样实际C3/2；它是不同外部成本，不能混为unit原P。以及同规模806机器1183jobs的严格YES：64个全正和64个全负clauses，取3真4假，每clause真文字数为3或4，所选sign树全部下传给实际C1；selector也给OPT≥1。

还有私有host加真实0/1不可迁移pin的局部模块：170机器、169枚basejobs+128枚pins，共297jobs。全正host开放或全负开放各有C1；只开负轨digit<2的8个host有精确OPT3/2。上界沿二叉pruned tree。下界：在C<2下，被单位incoming激活的全闭子树必须继续至少下传一件并最终在闭host产生负载2，所以不可能；正轨全闭，负根也不能进入首digit≥2的闭分支，至少两枚1/4 jobs留根，含selector负载≥3/2。这个含pin模块不属于第1节slots无其他任务的IFF模型，不能用它反驳或伪证第6节。

## 8. 虚拟叶补齐的精确命中门槛

**UM-PRUNED-TREE-LEAF-HITTING-v1。** 对任意整数k,h≥1、1≤r≤k，令q=k−r+1，N=k^h。一棵完整k叉深h树的叶集合中，碰到每棵rooted r-pruned subtree的最小叶集合大小恰为q^h；等价地，不含任何rooted r-pruned subtree的叶子集最大大小恰为N−q^h。两个界每个参数均可达到，见证可在显式树/叶地址总编码长度内多项式构造与核验。

这是标准递归threshold/叶证书机制的自足实例，不主张新组合技术或已确认全球优先权。h0基例只有根叶，最小命中数为1。对高度h的命中集R，其root有k个孩子：若少于q个孩子的R限制能命中该child的全部r子树，就至少有r个孩子各有R-avoiding r子树，合根得到避开R的完整r子树。反之至少q个children各被命中时，任意r个children中必含一个被命中者，因为r+q=k+1。因此最小数满足H_h=q H_(h−1)，即q^h。取固定q个children递归所得q叉子树的叶为锐命中集；取补集得最大r-free叶集。

也可给显式双色证据提取：将R称红、其补集蓝。叶蓝good恰为蓝；内部点蓝good当且仅当至少r个孩子蓝good。root good时逐层取r个good孩子，提取纯蓝r子树；root bad时逐层取q个bad孩子，提取纯红q子树，其q^h红叶碰到任意r子树。扫描显式树及输出路径即为位多项式。k1、r1、rk、h1均包括；若k1而h只有二进制数值、未显式列h条边或长度h叶地址，则不能借本页宣称poly(log h)输出。

**补虚拟端口的准确含义。** 若某sign轨的真实出现叶数严格小于q^h，其余虚拟叶一定含完整r子树；若这些虚拟叶的外部资源也能共同容纳它们，调度便可沿这些虚拟叶绕过真实源出现。这里的资源可容纳是额外前提：本叶集合定理不自动解决clause packing。严格小于是必要措辞；等于q^h已有命中所有r子树的锐blocker。反过来真实叶数量≥q^h也不保证其具体位置已经命中。

**同样开放数量，祖先兼容性不同。** k4,h3,r2时q3，最小blocker27叶、最大r-free集合37叶。取F为所有三位digits并非全部<3的37叶；正轨开放F，负轨只开放F中的任27叶，合计开放64个私有hosts，其他host有pin1。两轨开放叶均不含二叉pruned tree。若C<7/4则ceil(4(2−C))≥2，单位激活递推迫使某轨有完整二叉子树落在开放叶，矛盾。任选一枚开放叶沿单路径下传达到C7/4：active点1+3/4，inactive点1，host加pin≤1。所以这个170机器297jobs模块真OPT7/4。对照仅开放正轨全部64叶有真OPT1。它反驳“只冻住半数叶的容量匹配即可三半补齐”的恢复合同；它不反驳第6节一次匹配保留全部祖先槽兼容的dense模型。代码及独立枚举只作为这些具体结构的核验，不取代一般递推。

## 9. 超出半密度的源约束：先防空YES，再证所有森林的NO

若非空source有m>0个clauses，每个arity恒d、容量阈值A，且每个变量正负出现数相等，则任何赋值的总真occurrence数恒为md/2。因此d>2A时总量>mA，没有任何满足每clause≤A的严格YES。空公式不在这个“YES为空”结论中。把近二阈值源改到d>2A，不能仍用这个完全平衡域来声称得到有YES的归约。

不平衡源、constants或dummy叶补齐并未因此被一般排除；但要写出实际YES和NO合同。补叶必须处理第8节的纯dummy子树及其共同外部容量。对一般arity的第1节模型，真正soundness义务是：从每个mandatory r森林的clause packing中可靠解码源弱赋值，或证明NO源根本没有这种packing；只排除完整sign赋值不够。当r1时每变量只需任意sign的一条root→leaf路径，等价变量到可达clause slots的普通匹配，可位多项式解，因此近二归约还不能让其目标阈值进入r1区域。

这三个结论是明确模型的表示、经典工具推论及命中门槛，不是近二NP-hardness；未证明一般UM-TARGET-v1或其反面。所有正式Claim的Objects、Domain、Quantifiers、Assumptions、Definitions、Scope、Conclusion、Dependencies已在各节给出，Evidence和Counterevidence分别为上述原P证书、相应范围限制及[实际审查](../../reviews/unrelated_machines/unit_readout_pruned_forest_boundary_review.md)。Status：限定范围证明及内部独立攻击/精确软件核验；外审、新颖性及独立论文价值未认证。新的主要义务仍是可保持YES且排除所有低负载pruned森林的非此半密度归约。
