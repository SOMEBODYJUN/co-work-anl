# 统一端口与全局单位停车：余横截配置间隙及真实近似

读取目的：区分“配置或拟阵边际证书能否保常数”与“相对真实最优能否做次二实际调度”。前者在本页的显式族上失败，后者对整个统一D结构类由现有BLMRS定理直接闭合。它不构成一般UM算法或近二困难性；新颖性及独立成文价值未认证。

## 精确身份与共同输入合同

**UM-UNIFORM-PORT-PARKING-PAPER-APPROX-v1。** Objects / Domain / Quantifiers：任意显式有限主点U，每u非空显式状态族L_u；共同整数D≥1，每状态有D个不同外部资源C_{u,a}⊆R。每(u,a)有私有parent，与R全部互异；一枚unit selector可去u全部parents；每state每r∈C_{u,a}有一枚port，parent时间1/D、r时间1，除此无有限端。任意有限mandatory unit aux jobs，每job非空显式资格子集仅在R。上述是全部机器/任务。若全空则添一空dummy machine。结构随输入给出，不声称识别任意P。

**Exact Statement / Conclusion：** 对每个固定有理η>0，可确定性总位多项式输出全部原任务实际σ，Cmax≤(2−1/(4+η))OPT。若aux本身最优unit makespan B≥2，则本实例OPT=B并可精确输出；U为空则仅做unit aux精确调度，含空任务OPT0。B≤1且U非空时，本页定义的真实vacancy标签保留值β*满足OPT=2−β*，构造负载≤2−β*/(4+η)。此为published算法的直接应用；不要求CONFIG或纯右列证书。Dependencies：显式模型、标准matching/Rado/matroid intersection，以及BLMRS2307.08453v1 Definition7和Theorem4 two-value算法。Proof / Internal Review：下文自足给精确归约/负载和外定理适用条件；先陈述独立重构与冻结证明读后攻击均通过。Implementation：BLMRS及通用matroid算法未在本仓集成；不是已运行的一般调度程序。External Review / Novelty：未认证。

## 1. 标签配置的实际值

给 m≥1 个主点，每 u 有有限非空标签集 L_u，每标签有一个显式 resource 集 C_{u,a}，全部 |C_{u,a}|=D≥1。资源全体 R 上给一个有多项式时间 rank oracle 的 matroid M。不同标签的配置可以重叠，配置本身也不要求 M-independent。目标选每 u 一个实际标签及 S_u⊆C_{u,a_u}，满足 S_u 两两不交、Σ_u S_u 为 M-independent；最大化 β=min_u |S_u|/D。最优值记 β*∈[0,1]。

下面的相对真实最优值算法**不需要** CONFIG 分数证书，也不需要原源满足 pure-right-column 完备。这与从分数证书证明常数保留是不同合同。

## 2. 全局 matroid 计数是一个整数 polymatroid

每个标签建 variant player p=(u,a)，其 cheap 资源 eligibility 为 C_p。对 variant 子集 X 定义

f(X)=r_M(∪_{p∈X} C_p)。

这是规范化、单调、整数 submodular 函数：由 matroid rank 的 submodularity 及集合并运算可得。其 evaluation oracle 只需要形成显式 union 后调用 r_M。

对整数非负向量 x，存在互不交的 I_p⊆C_p、union I_p∈M 且 |I_p|=x_p，当且仅当 x(X)≤f(X) 对全部 X 成立。必要性直接。充分性为 Rado 的独立代表条件：把 player p 复制 x_p 份、每份可取集合 C_p，任何 copies 子集的邻集由其涉及的完整 players 决定，故完整 player 子集不等式已强于部分 copies 子集的条件。独立代表可用 matroid intersection 实际构造：以 eligible pairs (p,r) 为元素，resource r 的不同 player 副本在 M 的 parallel extension 中平行；与每 p 至多 x_p 的 partition matroid 求交，取总大小 Σx_p。

因此 cheap 分配计数恰是整数 polymatroid P_f；没有把一般 matroid 配置间隙误当成可直接舍入的普通 unit matching。

## 3. 两值 resource-polymatroid Santa Claus 的精确归约

在 BLMRS 的 Definition 7 中，用一个价值 1 的 polymatroid resource P_f 表示全部 cheap 资源。再对每个 u 给 |L_u|−1 个大 resource，每个价值 D，允许分配给 u 的任一个 variant，约束为该 group 上 rank-1 uniform matroid。

这是其 restricted **two-value resource-matroid Santa Claus**：resource 的价值只依赖 resource（1 或 D），并不依赖 player。不能把该模型与“每个资源由一个普通 player 获得、所有已用物品受一个 global matroid”混为一谈；上节计数 polymatroid 正是两种模型之间的显式桥梁。

此 Santa Claus 实例的真实最优值恰为 β*D。给 label 方案，使所选 variant 收到 I_u、其余 variants 各收一个大 resource。反向，每 u 的大 resources 比 variants 少一个，因此至少一个 variant 没收到大 resource；它至少获得 Santa Claus 最小值那么多单位 cheap 资源。用上节 lifting 实际分配后，从每 u 选这样一个 variant，丢弃其它 variants 的 cheap 资源，得到一个全局标签及 M-independent 的实际保留集合。至少一个 variant 没大 resource，且其 cheap eligibility 总共 D 件，故 Santa Claus 实际值≤D。

BLMRS Theorem 4 在此 two-value 情况给每固定 η>0 的确定性多项式时间 (4+η)-approximation。因而可实际构造

β_alg ≥ β*/(4+η)。

尤其，如果存在完整实际 YES（β*=1），就能构造所有主点至少常数 D/(4+η) 个资源；所以此统一 D 的模型不能承载对每个 δ>0 的 NP-hard (1,δ) gap，除非 P=NP。CONFIG 仍可有巨大间隙：该相对真实 OPT 的算法没有声称把 β_LP=1 变成常数 β。

## 4. 全局 mandatory unit parking 的普通 UM 实现

现在令 M 为某个 mandatory unit jobs 系统的 vacancy matroid。资源机器 R 上有 unit auxiliary jobs，每个有显式可用机器集合；假设这些 aux 本身能在 makespan 1 真实匹配。令 N 为 ground set R 上的 transversal matroid：一个 resource 子集独立，当它可匹配到不同 aux；r_N(R)=n_aux。则 M=N*，S∈M 当且仅当 aux 可全匹配到 R\S。其 rank

r_M(S)=|S|+r_N(R\S)−r_N(R)

可用普通 matching 多项式计算，且保留 S 后的实际 aux parking matching 可同样求出。

每 (u,a) 一台私有 rail，u 有一个时间 1 的 selector job 可去其所有 rails；每 r∈C_{u,a} 有一个 port job，可在该 rail 用时 1/D，或在 r 上用时 1；无其它边。所有 rails 与 R 互异。于是该普通 UM 实例严格有

OPT_UM=2−β*。

正向：selector 放选定标签 rail，选择 I_u 外送，其余全部 ports 留自己 rail，aux 匹配到 R\union I_u。选中 rail 负载 2−|I_u|/D，未选 rail≤1，资源机器≤1。反向：OPT≤2 由 aux 的 C=1 matching 加所有 ports 留 rail 保证；若 C<2，所有 unit aux 和外送 ports 在 R 上不能共享同一机器。selector 所在标签的外送 ports 给实际标签保留方案及 vacancy 独立性。β*=0 的边界同样得 OPT=2。

用上节 BLMRS 算法，实际调度负载≤2−β*/(4+η)。对 β∈[0,1]，

(2−β/(4+η))/(2−β)≤2−1/(4+η)，

因为该比值随 β 单调增加，最大在 β=1。故统一 D、全局 mandatory unit parking 结构类有确定性位多项式 (2−1/(4+η))-approximation，系数与 m、D、标签数无关。这个结论是现有算法的直接应用，不是一般无关机突破。

aux 若自身最小 unit-job makespan 为 B≥2，可用普通 b-matching 精确求 B；让全部 ports 留 rail，selectors 任放，得到 max(B,2)=B。原问题 OPT≥B，所以此分支最优。无主点/无 selectors 时只需求解 aux unit scheduling；没有任何 jobs 则输出空调度、负载 0。D≥1 的合同不包括空配置；空 label rails 可另处理，不在本文悄悄扩展。

## 5. 反面路线必须改变什么

root 的 cotransversal uniform-config 反例正确地否定“fractional certificate→uniform actual constant”这个合同，但并没有完整 integer YES。它不妨碍本算法。要从这里构造 actual near-zero hardness，至少需要退出统一 D 的 two-value 归约、或退出 polymatroid 可压缩的资源机制；仅添加更多单元 parking aux 或复杂 cotransversal rank 还不够。

D_u 不统一时，若仍用 cheap resource 价值 1，则各 group 的 big 值变为 D_u、理想最小需求也依 u；若按每 variant 1/D_u 归一化，cheap 值又依 player，不能调用 restricted Theorem 4。这里没有免费处理多尺度；这正是尚在研究的全局源义务。


## 显式余横截族：每个完整配置独立也不能保常数

**ID/version：UM-COTRANSVERSAL-UNIFORM-CONFIG-SHARP-GAP-v1。** Objects / Domain / Quantifiers：对每个整数D≥3，m=D+1个主点，u∈[m]、a∈[D]、j∈[D]。外机为g_{u,a,j}、A_{u,a}、B_j，全互异。一枚mandatory unit任务L_{u,a,j}仅可去g_{u,a,j}、A_{u,a}、B_j。N为这些外机在“机器—mandatory任务”二部图上的transversal matroid，M=N*。每主点的D个状态配置为C_{u,a}={g_{u,a,j}:j∈[D]}。

**Exact Statement / Conclusion：** 每个C_{u,a}均M-independent；边际y_g=1/D、y_A=y_B=0属于P(M)，且每人uniform选择配置的边际恰为y。但选每人一个状态a_u及S_u⊆C_{u,a_u}、各S互不交且其并M-independent时，最优min_u|S_u|/D精确等于1/D。

把这族按共同输入合同编译为普通UM（每parent D枚ports；每u一枚selector可选其D个parents；相同mandatory任务），其配置LP精确阈值Tconf=1，真实OPT=2−1/D。因此sup配置gap仍2，甚至每个单配置已能给完整mandatory匹配。Scope：限定LP/边际舍入合同障碍，不是计算困难性；本族OPT闭式可求。它不反驳上面的相对真实OPT算法。

### 证明：真实匹配、边际与共同容量

所有mandatory任务先去自己的g，故r_N(R)=#L，S∈M恰为全部L能匹配到R\S。单配置C_{u,a}被删时，该组D枚L改放D个不同B_j，其它L保持自己的g，得到完整匹配；故每C独立。

对每固定j，I_j={g_{u,a,j}:所有u,a}也M-independent：将这些受影响L改放各自不同的A_{u,a}，其它L保持g。uniform混合D个I_j，得到确切y_g=1/D和其余0。此处是实际独立集的凸分解，不只核总rank。

现在选每u一个a_u。若保留S_u，则每个所保留g对应的L都失去自己的g，只能去该u的同一个A_{u,a_u}或D个全局B。全部受影响任务总邻集至多m+D=2D+1台。如果每人保留≥2，则至少2m=2D+2枚任务，Hall矛盾。故某人保留≤1。反向每人任保一个g，其L去本人的A，其它L去g，达到每人1；最优比例精确1/D。

### 配置LP、全部原调度与真实整数下界

T1的显式配置：每parent单selector配置权1/D，全部D ports配置权1−1/D；每g单port配置权1/D、单L配置权1−1/D；每A的D种单L配置各权1/D；每B空配置权1。所有机配置权和1，所有job覆盖恰1，每个配置负载≤1。selector的每条有限边为1，故任何T<1的配置LP不可能覆盖selector，Tconf精确1。

实际上界：每人固定一状态，把selector放它parent，仅该状态的一枚port外送到自己的g，对应L送A，其余所有ports留其parent、其余L留g。活跃parent负载1+(D−1)/D=2−1/D；其它parent为1，外机≤1，得到全原任务实际σ。

若实际C<2−1/D，则每个selector所在parent至少外送2枚ports；这些unit port所在g在C<2时不能再放对应unit L。所有受影响L只能去选定m个A和D个B，与上面的2m>m+D矛盾。故真实OPT恰2−1/D。没有由有限枚举替代一般下界。

### 不可偷加的源完备性

本族只给fractional边际，并无β*=1的完整整数YES。若试将每个L的三个可用外机强行归入同一个纯右列guard，这些三元资格会把所有g/A/B连进一个block；完整选择的共同独立性将立即违反上述Hall界。把A拆私有或拆block会改变容量和消去gap。因此它不是“纯右列完备标签源”的无成本编译，更不能只据large matroid gap声称有近二hardness。

Dependencies：显式源/普通UM定义、transversal dual的删除匹配刻画、实际Hall计数；没有未解oracle。Evidence：一般证明、两路独立陈述重构及冻结D3/D4完整P/配置/匹配/实际σ核验。Counterevidence / Objections：相对真实OPT的统一D算法正是上半页，构造不具integer perfect-completeness。Status：限定证明完整、内部攻击无standing fatal；显式族和有限核验实现，外审及新颖性未认证。Related Files：本页、[实际审查](../../reviews/unrelated_machines/uniform_port_parking_matroid_review.md)、[精确审计代码](../../../tests/audits/unrelated_machines/cotransversal_uniform_configuration_gap.py)、[冻结原P与证书](../../../evidence/runs/unrelated_machines/cotransversal_uniform_configuration_gap_audit.json)。

## 来源、实现与位复杂度范围

已实际读取仓库原始[BLMRS v1](../../../history/source/literature/unrelated_machines/bamas_et_al_2023_santa_claus_makespan_matroids_v1.pdf)：Theorem4印3，Definition7印7；只导入two-value resource-polymatroid Santa Claus的(4+η)算法。所有资源的rank oracle在本文都由显式matching实现。Rado lifting的eligible-pairs地集大小为Σ|C_p|；D枚ports已显式列出，所以循环依D不是按二进制数值伪多项式。固定η属于算法参数，不随P趋0。输出包含全部未选state ports、全部selectors和全部aux，位复杂度及零实例由上文分支处理。BLMRS算法本身未集成到本仓软件，数学可构造性与实现状态分开。

D3/D4审计逐项核全部原P，配置覆盖/行和、每C的完整aux匹配、D个边际凸分解原子，以及一port/人实际调度。按state对称性分别核81与7776个“两port/人”模式的真实邻集和独立matching；未枚举所有完整原调度。D3有63机76job，实际5/3；D4有124机165job，实际7/4。root全文读代码并复跑，冻结JSON所有字段相同。有限checks不替代一般证明。

原始CONFIG大gap及普通两值难度本来已知；本页新增可接续的精确信息是“每个完整配置均vacancy-independent仍有1/D共同保留”与它在同一个实际结构类中被published算法相对OPT解决的并置。没有认证全球新颖性或独立论文价值，不升级一般UM-TARGET-v1。
