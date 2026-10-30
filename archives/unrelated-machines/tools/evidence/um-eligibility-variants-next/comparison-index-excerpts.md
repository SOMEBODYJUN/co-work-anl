## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/claims.md lines 880–885

| UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1 | `|B|=|H|`、宏仅home且每个home的有限宏边同一 `P_h>T/2`；私有任务任意逐件资格、每条有限私有边≤δT。固定宏完美匹配后 LST/ST 给所有机器≤(1+δ)T，OPT≤T时LP必可行。 | [同质大宏任意私有边 ST 候选](../questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md)；标准机制结构重构，候选审查未冻结。 |
| UM-HOMOGENEOUS-MACRO-PRIVATE-PROMISE-v1 | 同结构未知 `OPT`，承诺每个home `P_h>OPT/2`、私有边≤δOPT；有理网格单调LP候选输出≤(1+δ̄)OPT（固定δ̄<1）。 | [同质大宏任意私有边 ST 候选](../questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md)§2；承诺算法候选，主目标OPEN。 |
| UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-v1 | 全局同量子 `u`、恰 `|H|` 个全home可用home固定宏时长 `p>T/2`、逐私有任务资格 `E_j` 任意；带下界整数流可行当且仅当 `T` 可行，输出精确 `Cmax≤T` 调度。 | [任意资格等量子流候选](../questions/unrelated_machines/equal_quantum_arbitrary_eligibility_flow_candidate.md)；候选证明及3000个小实例穷举，正式审查/新颖性未认证。 |
| UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-PROMISE-v1 | 同结构未知 `OPT`，承诺 `OPT<2p`；在 `{p+ku}∪{ku}` 断点上单调测试下界流，候选精确求 `OPT` 并输出实际调度。 | [任意资格等量子流候选](../questions/unrelated_machines/equal_quantum_arbitrary_eligibility_flow_candidate.md)；断点/边界待冻结核验，主目标OPEN。 |
| UM-RATIO-GROUP-JOINT-SLOT-v1 | 唯一home共同资格组内 `p_zj=ρ_hz w_j`，给定T、W_h≤T、w_j≤δT、宏端>T/2；候选联合槽输出 home≤(3/2+δ)T、sink≤(1+ρ_max/2)T，ρ_max<2。 | [比例组联合槽候选](../questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md)；候选证明草稿，内部两路攻击无fatal报告，正式审查/新颖性未认证；主目标OPEN。 |
| UM-RATIO-GROUP-PROMISE-APPROX-v1 | 同一比例组结构，OPT处承诺阈值，固定 δ̄<1/2、ρ̄<2 时候选 `Cmax≤max(3/2+δ̄,1+ρ̄/2)OPT`；比例分组不是一般输入免费结构。 | [比例组联合槽候选](../questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md)§1、§5；候选状态，未替代UM-TARGET-v1。 |

## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/claims.md lines 961–962

| UM-DISTORTED-GROUP-JOINT-SLOT-v1 | 完整声明范围证明；内部独立审查；新颖性/外审未认证 | ∀显式不交H∪Z、宏B与唯一home私有组J_h；组内共同E_h，home时间w_j，给有理0≤δ<1/2、κ≥1、B̄≥0、0≤b_hz≤B̄，满足(b_hz/κ)w_j≤p_zj≤b_hz w_j。∀有理T≥0、1/2≤r<1−δ，若W_h≤T、w_j≤δT且全部有限宏端>T/2，则有确定性总位多项式算法返回FAIL或实际完整σ，home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，OPT≤T必成功。 | [正文](unrelated_machines/distorted_group_joint_slot_rounding.md)；准确身份/软件限制见专题账本。 |
| UM-DISTORTED-GROUP-PROMISE-APPROX-v1 | 完整声明范围证明；内部独立审查；新颖性/外审未认证 | ∀同一显式包络结构及有理参数，不给OPT；承诺在真实OPT处W_h≤OPT、w_j≤δOPT、全部有限宏端>OPT/2，则确定性总位多项式算法输出Cmax≤α(r)OPT的实际完整调度，α=max(1+r+δ,κ+B̄(1−r))，含空任务/OPT0。固定δ,κ,B̄满足κ+B̄δ<2时取r*=max(1/2,(κ+B̄−1−δ)/(1+B̄))，有本结构类统一α(r*)<2；参数趋边界时不声称统一余量。 | [正文](unrelated_machines/distorted_group_joint_slot_rounding.md)；准确身份/软件限制见专题账本。 |

## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/CLAIMS.md lines 1098–1180

## UM-RATIO-GROUP-JOINT-SLOT-v1：组—汇点比例处理时间的联合槽候选

- Exact Statement / Quantifiers：显式不交 home/sink、宏任务与唯一home私有组；组内任务只在 home 或共同资格 sink 集可用，home 时间为 w_j，且每个组—sink 对存在任务无关有理比例 ρ_hz 使 sink 时间 p_zj=ρ_hz w_j；给定 T、0≤δ<1/2，若 W_h≤T、w_j≤δT、所有有限宏端>T/2，则确定性位多项式算法返回 FAIL 或实际调度，home≤(3/2+δ)T、sink≤(1+ρ_max/2)T，且 OPT≤T 时必成功。
- Objects / Domain / Definitions：UM-MODEL-v1；组—sink 比例、d_h=(W_h−T/2)_+、成本 c_hz=ρ_hz d_h 及联合宏/home/sink槽流按候选正文定义。
- Assumptions / Scope：唯一home、共同资格、宏大边仍承重；比例条件需逐边核验。固定 δ≤δ̄<1/2 与 ρ_max≤ρ̄<2 时给 α=max(3/2+δ̄,1+ρ̄/2)<2；ρ_max 仅逐实例小于2不产生统一 ε。不是一般 UM 算法。
- Conclusion：候选正面结构接口；等端处理时间的加权组是 ρ_hz=1 特例。未知OPT承诺版本另记 UM-RATIO-GROUP-PROMISE-APPROX-v1。
- Dependencies：UM-MODEL-v1、UM-WEIGHTED-GROUP-JOINT-SLOT-v1；标准有理LP、带成本排序的有序槽和整数流。
- Evidence：内部两路独立重构；Fraction 随机前缀与槽收费边界核验；候选正文给必要性、联合流、真实前缀、未知OPT网格和位复杂度。
- Counterevidence / Objections：尚待正式冻结审查；去掉精确比例时必要LP可错误拒绝（仅有上界 q≤ρw 不足）；分组生成、跨home任务和一般矩阵转换仍未解决。
- Status：candidate; proof draft complete at stated scope; internal attack pending formal review; external review and novelty unverified。
- Related Files：research/questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md；对应承诺版本同文件§1；与 weighted_group_joint_slot_rounding.md 的关系见候选§6。

## UM-RATIO-GROUP-PROMISE-APPROX-v1：组—汇点比例结构的未知OPT候选

- Exact Statement / Quantifiers：同一比例组结构，不给 OPT；承诺在 OPT 处 W_h≤OPT、w_j≤δOPT、所有有限宏端>OPT/2，且 δ≤δ̄<1/2、ρ_max≤ρ̄<2 固定。确定性位多项式算法输出实际调度，Cmax≤max(3/2+δ̄,1+ρ̄/2)OPT，含空任务与 OPT=0。
- Objects / Domain / Definitions：同上；阈值测试使用原处理时间分母乘积网格和单调比例成本LP。
- Assumptions / Scope：结构承诺不是一般输入可免费识别或生成；候选状态，不替代 UM-TARGET-v1。
- Conclusion：条件类统一低于2的承诺算法候选，固定 ε=min(1/2−δ̄,1−ρ̄/2)。
- Dependencies：UM-RATIO-GROUP-JOINT-SLOT-v1、UM-WEIGHTED-GROUP-PROMISE-APPROX-v1。
- Evidence：同一候选正文§1、§5；尚无独立冻结审查。
- Counterevidence / Objections：比例核验和单调网格端点需形式化复核；ρ/δ逼近边界时统一余量消失。
- Status：candidate; proof draft complete at stated scope; internal attack pending formal review; external review and novelty unverified。
- Related Files：research/questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md。

## UM-C2-PREFIX-CONDITIONING-DEGREE-v1：四阶 C₂ 与深层真前缀容量的锐利信息边界

- Exact Statement / Quantifiers：存在同一一般 UM 处理时间矩阵、两份真实 `OPT=T=2` 调度分布 `μ_even,μ_odd`，使全部相容 one-hot 矩 `y_S`（`|S|≤4`）及其 C₂-load/localizer 数据完全相同，但某个相容深度四前缀 `F` 的完整条件 B 负载分别为0与1；判别所需条目是五阶矩。
- Objects / Domain / Definitions：one-hot 调度分布、四阶 C₂-load、条件平均负载按 [c2_prefix_conditioning_degree_boundary.md](../current/unrelated_machines/c2_prefix_conditioning_degree_boundary.md) 定义；修复见证含7任务、3机器、四个零时间前缀任务、一个A/B单位任务、一个固定A的零任务和独立C机器的强制2任务；原互补双3/2见证不能证明整机负载差异。
- Assumptions / Scope：这是表示信息边界，不是复杂度下界或 C₂ 整体 integrality gap；分布显式存在且两份都是真实 OPT=T 调度。
- Conclusion：仅给四阶矩不能免费反复条件化到深度4；深度 t 的完整条件 C₂ 通常需 t+4 阶或等价条件 oracle。
- Dependencies：UM-MODEL-v1；标准 one-hot 矩与条件化恒等式。
- Evidence：偶/奇五位 parity 的32态精确枚举，`y_F=1/16`，五阶续接项分别0与1/16；Python Fraction/整数核验见阶段记录。
- Counterevidence / Objections：旧见证的两件3/2任务互补使完整B负载抵消，已显式替换；只否定“低阶矩唯一恢复指定来源的深层条件负载”的合同；不排高阶证书、重算残余矩、自适应舍入或一般 UM 算法。
- Status：complete stated-scope proof; internally exactly enumerated; external review and novelty unverified。
- Related Files：research/current/unrelated_machines/c2_prefix_conditioning_degree_boundary.md。

## UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-v1：全占用同宏下任意逐件资格的精确流候选

- Exact Statement / Quantifiers：机器分成 homes H 与 sinks Z；每组私有任务 J_h 只能在其 home 或任意逐件资格集合 E_j⊆Z 上运行，所有有限端处理时间都是同一全局量子 u>0；恰 |H| 个宏任务在所有 home 上可用且处理时间相同 p>T/2。给定有理 T，令 r=floor((T−p)/u)、q=floor(T/u)、k_h=max(0,|J_h|−r)。一个带下界整数流在 h→j→z 资格网络中可行，当且仅当存在 makespan≤T 调度；流恢复实际完整分配，FAIL 等价于该结构类在 T 下不可行。
- Objects / Domain / Definitions：UM-MODEL-v1；固定全占用宏位置、逐件 E_j、等量子 u、home/sink下界流，按候选正文定义。
- Assumptions / Scope：全局同量子、|B|=|H|、宏 complete 且共同 p 是承重条件；允许 E_j 任意交叠、空集或完全不共同。不是一般 UM 算法。
- Conclusion：给定阈值的确定性位多项式精确可行性/实际调度候选；相比共同资格组，去掉共同出口资格但牺牲宏占位和任务尺寸异质。
- Dependencies：UM-MODEL-v1、标准带上下界整数流和有理 floor。
- Evidence：独立流证明与 3000 个随机小实例的穷举资格/容量核验；未完成正式冻结审查。
- Counterevidence / Objections：u 异质后变成加权容量/二箱选择；宏资格或宏时长异质会重新耦合占位与外送流；未知OPT只在承诺 OPT<2p 的home固定宏时长类中记录。
- Status：candidate; proof draft complete at stated scope; internal attack pending formal review; external review and novelty unverified。
- Related Files：research/questions/unrelated_machines/equal_quantum_arbitrary_eligibility_flow_candidate.md。

## UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-PROMISE-v1：home固定宏时长承诺下的未知OPT精确搜索候选

- Exact Statement / Quantifiers：同一全局量子/逐件资格/全占用home固定宏时长结构，不给 OPT，承诺 OPT<2p（等价 p>OPT/2）。在临界集合 `{p+ku}∪{ku}` 上测试带下界资格流，得到最小可行阈值并输出精确 OPT 调度；含 u=0、空资格和空任务边界。
- Objects / Domain / Definitions：同上；阈值单调且 floor 断点显式多项式。
- Assumptions / Scope：承诺识别和结构生成不属于算法；若 promise 不成立只报告域外，不作一般实例结论。
- Conclusion：该受限类的未知OPT实际调度候选比率1。
- Dependencies：UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-v1。
- Evidence：候选正文未知OPT段；形式断点和位复杂度待冻结代码核验。
- Counterevidence / Objections：宏时长异质、u异质或宏数不等于home数时不适用；外审/新颖性未认证。
- Status：candidate; proof draft complete at stated scope; internal attack pending formal review; external review and novelty unverified。
- Related Files：research/questions/unrelated_machines/equal_quantum_arbitrary_eligibility_flow_candidate.md。

## UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1：同质大宏占位下任意逐件资格的 ST 候选

- Exact Statement / Quantifiers：机器分为 homes H 与 sinks Z；宏集 B 满足 |B|=|H|，只在 H 可用；对每个home h所有有限宏边时间同为 P_h>T/2，宏边图有完美匹配；私有任务任意逐件资格 A_j⊆H∪Z，且每条有限私有边 p_ij≤δT。固定任意宏完美匹配，私有 LST LP 在home h容量 T−P_h、sink容量T上经ST舍入得到完整调度，所有机器≤(1+δ)T；若OPT≤T，LP必可行。
- Objects / Domain / Definitions：UM-MODEL-v1；home固定宏时长占位、任意私有边、剪枝LST/ST按候选正文定义。
- Assumptions / Scope：宏数等于home数、每个home宏端同一P_h>T/2及私有统一小边δT承重；不要求唯一home、共同资格或等端tiny。是标准ST机制的结构重构，不是一般算法。
- Conclusion：候选结构类给定T的 (1+δ) 实际调度；未知OPT承诺版本另记。
- Dependencies：UM-MODEL-v1、UM-ST-ROUND-v1、标准有理LP及二分图完美匹配。
- Evidence：证明草稿；独立内部重构确认宏固定占位和私有LP/ST界，尚未正式冻结审查或端到端实现。
- Counterevidence / Objections：宏时长/数量异质会重新耦合匹配与残余容量；私有边大于δT则无统一小加性项；一般输入不提供该分层。
- Status：candidate; proof draft complete at stated scope; internal attack pending formal review; external review and novelty unverified。
- Related Files：research/questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md。

## UM-HOMOGENEOUS-MACRO-PRIVATE-PROMISE-v1：home固定宏时长承诺下的未知OPT候选

- Exact Statement / Quantifiers：同上结构不给OPT，承诺真实OPT处每个home P_h>OPT/2 且所有私有有限边≤δOPT，固定δ≤δ̄<1。按有理分母网格单调测试宏匹配与私有LP，得到 t*≤OPT 的实际调度，Cmax≤(1+δ̄)OPT。
- Objects / Domain / Definitions：同上；测试删去 p_ij>t 的私有边，home容量 t−P_h 与 sink容量 t 随t单调。
- Assumptions / Scope：承诺结构不是一般输入识别；候选不替代UM-TARGET-v1。
- Conclusion：该结构类未知OPT实际调度候选统一比率1+δ̄。
- Dependencies：UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1。
- Evidence：候选正文§2给网格、加性误差δOPT和位复杂度；正式断点审查待完成。
- Counterevidence / Objections：若δ仅逐实例<1则没有统一ε；宏占位异质时不适用。
- Status：candidate; proof draft complete at stated scope; internal attack pending formal review; external review and novelty unverified。
- Related Files：research/questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md。

## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/README.md lines 228–252


同页的 `UM-LST-SUPPORT-RELEASE-v0` 旧族仍反驳固定正支撑填充，但其精确 `OPT=1−49/[100(m+1)]<1`，撤回旧的 `OPT=T=1` 标签。新增 `UM-LST-SUPPORT-RELEASE-OPTIMAL-v1` 用 `r` 个独立块把真实 `OPT` 固定为1，并证明少于 `r` 条零质量边时比值为 `2−1/m`；容量释放机制必须允许支撑扩张或共同 `(H,z)` 证书。rank-jump-one 路线已分层：对真实有限正权支持可用 Boolean 代数闭合恢复 `R+1` 原子；对一般伪矩仍缺共同交换投影与 `V2` localizer。`4-2√2` 支持候选未认证。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。

## 新候选：组—汇点比例处理时间

问题账本新增 `UM-RATIO-GROUP-JOINT-SLOT-v1` 与 `UM-RATIO-GROUP-PROMISE-APPROX-v1` 候选。它把 `weighted_group_joint_slot_rounding.md` 的“组内所有有限端时间相同”放宽为：对每个组 `h` 和共同资格 sink `z`，存在任务无关比例 `ρ_hz`，使 `p_zj=ρ_hz w_j`。按 `c_hz=ρ_hz(W_h−T/2)_+` 排序造槽并与宏/home容量一次整数流，可得 home≤`(3/2+δ)T`、sink≤`(1+ρ_max/2)T`；固定 `δ<1/2, ρ_max<2` 才有结构类统一低于2。候选正文、必要性、未知OPT单调网格和待审义务见 [组—汇点比例联合槽候选](../../questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md)。分组生成、唯一home和共同资格仍未从一般矩阵中可计算提取，`UM-TARGET-v1`保持OPEN。

## 更宽的固定宏占位候选

`UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1` 把私有任务资格放宽到任意逐件集合 `A_j⊆H∪Z`，并允许每条私有边有不同处理时间，只要求≤`δT`；承重条件改为 `|B|=|H|`、宏只在 home、每个 home 的宏边时间固定为 `P_h>T/2` 且宏图有完美匹配。任取宏完美匹配后，私有 LST LP 的 home 容量 `T−P_h` 与匹配无关，ST 舍入给 `(1+δ)T` 候选。承诺 `P_h>OPT/2`、私有边≤`δOPT` 时，网格搜索给未知 OPT 的 `(1+δ̄)` 候选。该接口是标准 LST/ST 的结构重构，未认证新颖性；宏身份相关时长、宏数不等于 home 数或大私有边会重新产生联合容量义务。正文见 [同质大宏任意私有边候选](../../questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md)。

## 异质宏身份下的统一残余容量候选

[异质大宏统一残余容量](heterogeneous_macro_uniform_residual_st_rounding.md)给 `UM-HETEROGENEOUS-MACRO-ARBITRARY-TINY-v1`：宏数等于 home 数、宏仅在 home、每条有限宏边严格大于 `T/2` 且不超过 `T`，但宏时长可依赖任务身份；tiny 任务资格与边成本完全逐件任意，只需每条 tiny 边≤`δT`。任意宏完美匹配后把全部 home tiny 容量统一收紧到 `T/2`，保留 OPT tiny 分配作 LP 见证，ST 后得到 `(3/2+δ)T`；承诺未知 OPT 版本以保留全部 tiny 边的单调 `F(t)` 和 `Q` 网格整数二分给 `(3/2+δ̄)OPT`。这去掉了同质宏和共同资格/等端 tiny 假设，但仍承重 `|B|=|H|` 与大宏 promise，不是一般 UM 算法。

同一正文记录 `UM-HETERO-TINY-3PARTITION-FLOW-BARRIER-v1`：即使所有异质 tiny 边均缩放到任意固定 `δT` 以下，精确 T 可行性仍可编码强 3-PARTITION，分数残余 LP 可行而整数调度不可行；该障碍只反驳普通整数流/简单 polymatroid 精确化，不反驳 ST 加性余量候选。

## 严格次二局部修复能垒

[严格次二批量能垒](strict_sub2_batch_barrier.md)给 `UM-STRICT-SUB2-BATCH-BARRIER-v1`：每个 `k≥2` 都有真实 `OPT=1` 的三机族，其 `Cmax<2` 坏态在每步最多 `k` 件且中间态严格 `<2` 的状态图中孤立，首个出口需 `k+1` 件。进一步，对任意固定目标余量 `ε` 和常数支持预算 `r`，取 `k>max{r,1/(8ε)}` 后坏态仍高于 `(2−ε)OPT`，因此常数支持的严格次二局部修复不能达到目标。它只限制局部修复，不是一般近似困难性；下一步若走修复路线必须允许规模增长的共同容量释放、跨过 `2T` 或全局重选。


## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/README.md lines 182–202

本结果终止的是固定顺序max||Aeψ||²后左乘的具体充分机制。真实所有阶矩和逐行容量算子也不能免费保过去联合支撑；仍不排重新耦合、自适应顺序、好μ选择或其他提取。§8的交换算子边界可回收；真正未解仍是一般输入可求的共同容量与实际输出/总进展，UM-TARGET-v1保持OPEN。

## 加权共同组的新增正面接口

[共同资格私有组的加权出口与联合槽](../current/unrelated_machines/weighted_group_joint_slot_rounding.md)给`UM-WEIGHTED-GROUP-JOINT-SLOT-v1`及未知OPT的`UM-WEIGHTED-GROUP-PROMISE-APPROX-v1`：给定不交home/sink、唯一home私有组、同组共同资格与等端w_j≤δT、W_h≤T及macro端>T/2，在0≤δ<1/2时实际输出≤(3/2+δ)T（sink≤3T/2）；无组负载正下界、sink数不固定。未知OPT承诺版用单调加权LP及有理整数网格搜索。数学算法完整，软件仅实现给定精确LP见证的验证/舍入；独立审查与双路有限Fraction核验已登记，外审/新颖性未认证。一般矩阵如何生成这些分组和处理异端容量仍未解，UM-TARGET-v1保持OPEN。

### 新增候选与表示边界

- `UM-RATIO-GROUP-JOINT-SLOT-v1` / `UM-RATIO-GROUP-PROMISE-APPROX-v1`：组内任务在 home 与共同资格 sink 之间按组—汇点恒定比例缩放；按真实比例成本 `ρ_hz d_h` 排序造槽，给出 home `≤(3/2+δ)T`、sink `≤(1+ρ_max/2)T` 的候选接口。唯一 home、共同资格、宏大边和固定比例仍是额外结构，正文在 `research/questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md`。
- `UM-C2-PREFIX-CONDITIONING-DEGREE-v1`：偶奇五位真实来源的四阶矩完全相同，但深度四前缀的下一步容量相反；仅四阶 C₂ 不能自动提供深层条件 oracle。精确边界在 `research/current/unrelated_machines/c2_prefix_conditioning_degree_boundary.md`。

两项均不关闭 `UM-TARGET-v1`；前者的分组提取、后者的高阶/重算证书仍是一般路线的未解义务。

### 固定宏占位与任意私有资格

新增候选 `UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1`：`|B|=|H|`，宏只在 homes，且每个 home 的宏端处理时间只依赖 home、满足 `P_h>T/2`；任意私有任务可在任意显式资格边上运行，只要求每条私有边≤`δT`。固定任意宏完美匹配后，LST/ST 给 `(1+δ)T`；承诺 `P_h>OPT/2` 时用网格测试得到未知OPT候选。它精确显示共同资格与唯一home可去掉，但宏占位同质性仍是额外结构，不能替代一般 `UM-TARGET-v1`。


## 低重数标签资源的新精确边界

[低重数标签资源的确定性地板与锐界](../current/unrelated_machines/bounded_collision_label_resource_floor.md)：所选资源重数Δ给真实b≥1/Δ，二重资源对任意束宽恰保留1/2；全局不同变量组度Δ_G给无需见证的实际(2−1/Δ_G)桥梁调度。只排除该四层有界碰撞接口的近二归约；高重数/跨层一致性与一般UM-TARGET-v1仍OPEN。

## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/CATALOG.md lines 475–477

| [组—汇点比例处理时间的联合槽候选](<questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md>) | `research/questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md` | 记录把等端时间放宽为组—汇点恒定比例的联合宏/home/sink槽候选、完整量词、证明义务和未解决的分组生成限制。；配套 [共同资格私有组的加权出口与联合槽舍入](<current/unrelated_machines/weighted_group_joint_slot_rounding.md>) | 候选或未闭合义务；保存不升级状态；关联 `UM-DISTORTED-GROUP-JOINT-SLOT-v1`、`UM-DISTORTED-GROUP-PROMISE-APPROX-v1`、`UM-RATIO-GROUP-JOINT-SLOT-v1`，[命题合同（共 4 项）](assets.json) |
| [任意逐件出口资格的等量子下界流候选](<questions/unrelated_machines/equal_quantum_arbitrary_eligibility_flow_candidate.md>) | `research/questions/unrelated_machines/equal_quantum_arbitrary_eligibility_flow_candidate.md` | 记录去掉共同出口资格后，在全占用同质宏与全局等量子条件下用带下界整数流精确恢复实际调度的候选证明和边界。；配套 [组—汇点比例处理时间的联合槽候选](<questions/unrelated_machines/group_sink_ratio_joint_slot_candidate.md>) | 候选或未闭合义务；保存不升级状态；关联 `UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-PROMISE-v1`、`UM-EQUAL-QUANTUM-ARBITRARY-ELIGIBILITY-v1`，[命题合同](assets.json) |
| [同质大宏占位下任意私有边的 ST 舍入候选](<questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md>) | `research/questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md` | 记录固定同质大宏占位后，任意逐件私有资格和小边处理时间如何由 LST/ST 联合恢复，并明确宏异质时重新出现的容量耦合义务。；配套 [不相关并行机的精确目标、经典舍入与配置间隙](<current/unrelated_machines/model_and_classical_barriers.md>) | 候选或未闭合义务；保存不升级状态；关联 `UM-HOMOGENEOUS-MACRO-PRIVATE-PROMISE-v1`、`UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1`，[命题合同](assets.json) |
