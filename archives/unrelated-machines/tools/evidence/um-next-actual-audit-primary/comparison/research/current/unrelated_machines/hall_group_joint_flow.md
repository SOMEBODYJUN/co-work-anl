# 共同资格私有组的Hall容量与宏微任务联合流舍入

## 1. 精确对象、两个身份与主目标

本文给一个允许接收机器数量随输入增长的正面接口。它同时重选宏任务占用的home和私有组的接收机器，允许接收机增载，输出全部实际任务。它没有把一般矩阵变成本类的分解器，`UM-TARGET-v1`仍OPEN。

显式逐台给定机器不交并`H∪Z`，`|H|+|Z|≥1`；允许Z为空。任务不交分成宏任务B及私有组`J_h(h∈H)`。宏任务仅在homes可用，每个宏任务至少有一条有限边。对每个h给共同资格`E_h⊆Z`，可为空；每件`j∈J_h`恰在`{h}∪E_h`可用，且这些端点上的时间均为同一个非负有理`w_j`。宏任务处理时间可随home不同。写`W_h=Σ_(j∈J_h)w_j`，空max定义为0。机器、任务、资格图和处理时间为显式二进制输入，不使用任务多重性紧凑编码。

### UM-HALL-GROUP-JOINT-FLOW-v1：给定阈值的共同选择

给二进制整数`q≥2`和有理`δ≥0,T≥0`，`qδ<2`。要求每条有限宏home边`p_hb>T/2`，所有组和私有任务满足

`(1/2+1/q)T≤W_h≤T`，`w_j≤δT`。

这些条件包括T=0。宏边大于T仍可在原输入存在，算法剪掉它们。设

`τ=(q−1+qδ)/(q+1)`，`r=q(2+δ)/(q+1)`。

**Exact Statement / Quantifiers。** 对所有上述合法输入，存在统一确定性、输入总位长的多项式算法，返回FAIL或实际合法调度；每次成功均满足`C_max≤rT`。若OPT≤T，必成功，所以FAIL蕴含OPT>T。成功不判定T精确可行。q可以作为二进制输入增长，没有按q数值复制机器。

### UM-HALL-GROUP-PROMISE-APPROX-v1：无需给定OPT的实际近似

给上述结构、q和δ，不给T。承诺在真实OPT处有：全部有限宏边`p_hb>OPT/2`，每组`(1/2+1/q)OPT≤W_h≤OPT`，每私有任务`w_j≤δOPT`。要求`qδ<2`；δ0单独按零值分支处理。

**Exact Statement / Quantifiers。** 存在统一确定性总位多项式算法，对每个满足该承诺的输入输出实际完整调度，`C_max≤rOPT`，包括OPT0。算法不需要承诺的证书或OPT的值。对固定q和固定δ且qδ<2，本类有统一正数`2−r=(2−qδ)/(q+1)`；q增长时该改善可以趋零。因此这个承诺类结论既不替代一般UM-TARGET，也不声称可识别任意矩阵是否满足关于OPT的承诺。

**Dependencies / Status。** UM-MODEL-v1；下文共同资格/同体积假设、Hall条件、整数增广流和真实前缀收费。证明自足，不调用配置LP、最优分布或整数调度oracle。标准Hall/maxflow/prefix工具的组合；完整限域证明及内部独立审查，未外审，未认证全球新颖性或独立论文价值。

## 2. 原T调度产生共同的整数接收槽

设T>0且存在真实T调度，令S为其中放了宏任务的homes。宏边>T/2，故每home至多一个宏；原宏任务分配是B到S的全覆盖匹配。

对h∈S，home私有任务留量`≤T−p_hb<T/2`，因此原调度从该组撤离的实际体积`e_h`满足

`e_h>W_h−T/2≥T/q`。

任取非空A⊆S。这些组的出口只能在`N(A)=∪_(h∈A)E_h`，所有任务在home/sink按相同体积计量，所以

`|A|T/q<Σ_(h∈A)e_h≤|N(A)|T`。

从而`|A|<q|N(A)|`，特别有q副本Hall条件。将每个sink在存在性证明中复制q次，Hall匹配将S中每个home指定到一个合法sink，每sink接至多q组；与原宏匹配联合形成下一节的整数流见证。**算法不建立这q个副本**，也不逐组独立选sink。

共同资格与同体积是这里新增的承重信息。仅有总work而资格不完整时，不能从全局容量推出所有这些Hall条件。

## 3. 一次网络同时选择宏任务、home与接收机器

网络有源s、汇t、每个宏任务b、每个home拆分的`h_in,h_out`及每个sink z。容量为

- s→b：1；b→h_in：1，当原宏边有限且`p_hb≤T`；
- h_in→h_out：1；h_out→z：1，当z∈E_h；
- z→t：`min(q,|B|)`。

固定节点顺序，按最短增广路径求整数最大流。若值小于|B|，返回FAIL。由§2，OPT≤T时必有全流；将sink容量截到|B|不会改变一个总值≤|B|的流。全整数流给每个macro一个不同home，并给每个占用home一个共同接收sink；每sink至多q组。

未占用home的私有任务全部留原处。每个占用home按输入任务顺序撤离一个前缀，直到留下的真实私有负载≤τT；整段前缀送它在流中选中的sink。宏任务按流恢复，私有任务每件恰留home或退出一次。

`0<τ<1`：q≥2、δ≥0给前者，qδ<2给后者。每个占用home的宏负载≤T，私有留量≤τT，故负载≤(1+τ)T；未占用home负载W_h≤T。

若某组W_h≤τT则不用撤离。否则最后一件撤离之前，累计撤离量严格小于W_h−τT；加最后一件至多δT，所以实际出口

`e_h<(W_h−τT)+δT≤(1−τ+δ)T`。

零尺寸任务不会阻止终止：扫描至多本组任务数，全部撤离后留量0。每sink至多q组，故其负载≤q(1−τ+δ)T。直接恒等式

`1+τ=q(1−τ+δ)=r`，`2−r=(2−qδ)/(q+1)>0`

同时给所有机器的声明界。没有冻结原macro匹配，也不要求每台机器负载逐坐标不增。

## 4. 零值、显式输出和总位复杂度

T0时直接逐任务选择零边；若某任务无零边则FAIL。私有组W_h≤0使其全部w_j0；宏若存在，其有限时间>0，故正确拒绝。空任务返回空分配，H可空但无home时不能有宏或私有任务。Z/E_h为空时，零宏直接留home；有宏而全流失败的拒绝仍是可靠必要条件。输入非法条件与可靠FAIL分开。

网络点边数为显式输入规模的多项式。每个s→b容量1，每次整数增广至少增1，总值至多|B|，故最多|B|次BFS增广；所有sink容量为min(q,|B|)，位长不随q数值增长。τ、r及T的乘积用精确有理运算，位长由输入位长多项式控制；每组真实前缀和最多加本组任务数项，分母乘积的位数至多各分母位数之和。最后输出恰n个原机器编号，位长`O(n log(m+1))`。规范代码附带逐机负载，是对显式机器列表的多项式大小辅助输出。

因此整个构造是按二进制总输入位长计的多项式；不把“每步多项式”代替成功轮数证明，不按处理时间、q或分母数值循环。后文审计中的指数分配枚举不属于生产构造。

## 5. 不知道OPT时的有限瓶颈搜索

先逐任务检查零边，若每件都有零边就输出零调度。对满足promise且δ0的输入，这一步必成功：若OPT>0，则宏存在会要求home存在，或有正私有任务；然而任意home组W_h≥(1/2+1/q)OPT>0与全部w_j≤0矛盾。无home又无任务时OPT0。δ0非零输入可拒绝（API报ValueError），不声称该域外输入满足promise。

下设δ>0。忽略T的组大小/宏下界检查，保留§3网络结构，只把macro→home边限定为p_hb≤u。其余资格及容量固定。随u增大，网络边只增加。设D为所有有限宏处理时间的去重排序表；用整数最大流在D中二分，取得可覆盖全部宏的最小瓶颈B；若最大候选阈值仍无全流，则拒绝为promise违例（API报ValueError）。无宏时取B=0。

设空max=0，并取

`t=max(max_h W_h, max_(private j) w_j/δ, B)`。

在promise的真实OPT处，§2适用，故B≤OPT；另外两个量由promise不超过OPT，因此t≤OPT。于是所有有限宏边>OPT/2≥t/2，每组W_h≥(1/2+1/q)OPT≥(1/2+1/q)t；上界W_h≤t和w_j≤δt由t定义成立。在t上调用阈值构造，网络必满流并输出

`C_max≤rt≤rOPT`。

t0已由零边分支处理。搜索只作`O(log(|D|+1))`次网络可行性调用，所有候选来自实际输入宏时间；不二分连续实数，不使用最优值精度oracle，不假定整个阈值合同对T单调。对promise域外的t条件失败可拒绝（API报ValueError）；算法没有免费判定promise的义务。

## 6. 最近边界、负控制与可回收机制

同组共同资格承重：两个私有任务若只能分别去不同sink，取资格交集可能漏掉真解，取并集则可能非法迁移。每home两件1/2任务分别可去自己的sink，加home时间3/4的macro，T1可行但无共同合法接收机；它不属于本类。

组负载下界也承重。q2、三home各有仅在本home时间2/3的macro，每组四件1/6，唯一共同sink。每home留两件、退两件，sink恰负载1，所以T1可行；但q2槽网络只容纳两个组。该例违反W_h≥T，不能用它攻击本定理。

不能因§2的严格Hall号就把q槽降为q−1。q2、三个home各有唯一macro时间3/5、每组十件1/10，两个共同sink；原T1可行，每home留四件，前两组各退六件到不同sink，第三组分退三件到各sink，sink各9/10。q−1槽总数只有2，不能覆盖三个macro。本构造的q接收预算不可凭严格号免费逐机减少。

一个自然推广也需警惕：任意有理接收容量下，“每选组提供一个可分割单位流”的可行home集合不一定是拟阵。四sink容量各1/2，三组资格`E_a={x1,y1}, E_b={x1,x2}, E_c={y1,y2}`，每选组需求1。{a}和{b,c}均可分流，但{a,b}/{a,c}的邻容量均3/2<2，违反增广交换。此为低成本负控制，限制该拟阵识别，不是一般选择或UM目标困难性。

**Mechanism / Value / Novelty。** 可复用的正面机制是“真实occupied组的最低出口体积→整数接收槽→macro/home/receiver一个共同流→调整真实留量平衡两侧负载”。它无需固定sink数，且真实macro时间仍可随机器变化。只导入标准Hall和整数流，不调用BLMRS2024的一般近似归约或matroid覆盖算法；并未认证新颖性。一般跨home私有任务、同组异资格、异端时间或缺负载下界时，尚无保持该流接口和统一余量的转换。这仍是下一承重义务。

## 7. 规范实现、审查和可复现证据

实现及有限审计为[hall_group_joint_flow.py](../../../tests/audits/unrelated_machines/hall_group_joint_flow.py)，提供阈值接口`solve`与未知OPT接口`solve_promise`。独立原矩阵阈值DFS见[hall_group_joint_flow_independent.py](../../../tests/audits/unrelated_machines/hall_group_joint_flow_independent.py)；未知OPT接口另用[hall_group_opt_promise_independent.py](../../../tests/audits/unrelated_machines/hall_group_opt_promise_independent.py)，从逐机子集和候选阈值加DFS求原OPT，不调用规范flow或OPT核。k是显式sink列表长度的API简写，不声称对二进制紧凑给出巨大k的表示也有相同复杂度。实现拒绝浮点、布尔和违反输入合同；所有时间为整数/Fraction或精确有理字符串，全部计算为整数与Fraction。

实际输入与实际调度分别见[共同选择输入](../../../examples/unrelated_machines/hall_group_joint_flow_cases.json)及[任务分配证书](../../../evidence/certificates/unrelated_machines/hall_group_joint_flow_witness.json)。规范和独立冻结记录为[规范报告](../../../evidence/runs/unrelated_machines/hall_group_joint_flow_audit.json)、[独立报告](../../../evidence/runs/unrelated_machines/hall_group_joint_flow_independent.json)，及[未知OPT独立报告](../../../evidence/runs/unrelated_machines/hall_group_opt_promise_independent.json)，分别注明代码hash、Python版本、运行命令、枚举范围与未覆盖部分。原矩阵OPT、独立阈值DFS和实际输出负载逐件回算与一般证明分开；有限证据不升级为普遍证明。

[独立冻结审查](../../reviews/unrelated_machines/hall_group_joint_flow_review.md)记录先只看精确命题自行重构，再攻击冻结正文与代码；promise搜索另独立核对。共同登记与地图保留主目标OPEN，不以完成这个结构类替代一般统一ε。
