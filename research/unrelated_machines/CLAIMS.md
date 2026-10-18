# 不相关并行机的精确命题账本

本存档ID为 `unrelated-machines`；共同模型见 [正文](../current/unrelated_machines/model_and_classical_barriers.md)。所有命题均要求合法有限输入；作者结果与本团队的新结论严格分开。

## UM-TARGET-v1：通用统一常数突破

- Exact Statement / Quantifiers：∃ε∈(0,1)，∃确定性算法A，∀m≥1、n≥0及所有合法P，A在P的二进制总编码长度的多项式时间内输出合法σ，C_max(σ)≤(2−ε)OPT(P)。ε和多项式次数与P、m、n无关。
- Objects / Domain / Definitions：UM-MODEL-v1；p_ij为非负有理数或不可用标记∞，每任务有有限边，全部不可拆分任务必须安排；目标为最大机器负载。
- Assumptions / Scope：离线中央计算、无预测承诺、不拒绝任务、m不固定；OPT=0也必须精确满足不等式。
- Conclusion：统一优于2的可构造近似；仅估值不满足完成标准。
- Dependencies：模型定义；任何未来证明须显式列所需全部引理和算法复杂度。
- Evidence：经典方法与障碍已重构；有日期的文献检索未找到解决该身份的结果。
- Counterevidence / Objections：配置LP间隙排除一种相对LP值的舍入合同；没有据此证明本主目标为假。尚无候选算法或一般证明。
- Status：OPEN，用户选定主攻；不是“已证猜想”，未作可完成时间或录用承诺。
- Related Files：[数学地图](../current/unrelated_machines/README.md)、[前沿](RESEARCH_STATE.md)、[启动提示词](BOSS_START.md)。

## UM-DENSE-SMALL-INTEGER-EQUIVALENCE-v1：稠密正小整数与原目标的等价

- Exact Statement / Quantifiers：UM-TARGET-v1成立，当且仅当在所有显式m×n、m,n≥1、每项为1..n²正整数的全有限矩阵上存在统一严格次二的确定性位多项式实际调度算法。具体∀固定整数k≥2，该域上一个(2−1/k)算法可转为原完整模型上的(2−1/(2k))算法；不宣称输入k时的统一复杂度。
- Objects / Domain / Definitions：原UM-MODEL-v1与上述稠密域D；n为实际任务数，转换不添加任务。任意实数ε>0可由更小的1/k替代，算法保持同一个有限程序。
- Assumptions / Scope：无复杂度假设；假设的稠密算法确为总位多项式并输出实际分配。算法存在性的等价，不是NP源的gap归约或近二困难性。
- Conclusion：极大分母、零时间及不可用边不是主目标存在性与否的独立分界；反面主攻可集中普通整数域，仍须证明所有算法的下界。
- Dependencies：非负性下OPT0刻画、固定任务数枚举、精确几何阈值列表、向上取整及严格大成本排除；完整证明见模型正文§6，不调用未知可行性oracle。
- Evidence：精确陈述先行独立重构，冻结§6全文攻击与独立Fraction审计；审计挑战每个满足所假设比率的有限输出，而非仅最优输出。
- Counterevidence / Objections：必须使用OPT_Q≤(4kn/T)OPT+n的强式回译，粗界仅用于排除n²边；p=0的取整误差是≤1不是<1。仅给n²的逐实例改善仍不提供统一ε。
- Status：标准缩放机制的完整限范围接口重构，经独立内审；无外审、全球新颖性或独立论文价值认证；UM-TARGET-v1及其全常数反面均OPEN。
- Related Files：[模型正文§6](../current/unrelated_machines/model_and_classical_barriers.md)、[独立审查](../reviews/unrelated_machines/dense_small_integer_equivalence_review.md)、tests/audits/unrelated_machines/dense_small_integer_equivalence.py、evidence/runs/unrelated_machines/dense_small_integer_equivalence.json。

## UM-ST-ROUND-v1：给定剪枝可行解的加性负载舍入

- Exact Statement：∀合法P、∀有理T≥0、∀剪枝LST的有理可行x，存在可由确定性位多项式程序构造的合法σ，∀i，L_i(σ)≤Σ_j p_ijx_ij+max{p_ij:x_ij>0}≤2T；空max为0。
- Objects / Domain / Quantifiers / Assumptions：模型、T和x全部明确输入；正质量仅在p_ij≤T边；逐任务质量恰1、每机器分数负载≤T。
- Definitions / Scope：正文第2–3节。只实现给定x的负载舍入，不含通用LP求解器或ST保成本版本。
- Conclusion：真实整数分配及每机器界；不声称统一低于2。
- Dependencies：有序单位槽、正质量分数匹配、Hall条件、整数增广匹配、非增序负载收费。
- Evidence：自足一般证明；独立审查见本题reviews；Fraction程序及冻结有限证据。
- Counterevidence / Objections：未消除的实质异议阻止重构升级；原始定理本身仍以ST1993精确版本为Paper Fact。
- Status：已知结果的当前重构；内部审查覆盖范围以实际审查文件为准，非原创贡献。
- Related Files：正文第3节，tests/audits/unrelated_machines/rounding_and_gap.py，evidence/runs/unrelated_machines/classical_baseline_audit.json。

## UM-CONF-GAP-v1：配置LP的supremum间隙

- Exact Statement：在所有OPT>0的UM-MODEL实例上，sup_P OPT(P)/T_CONF(P)=2；即使每任务至多两条有限边，sup仍为2。
- Objects / Domain / Quantifiers / Assumptions：T_CONF为第2节精确配置可行性阈值，不是近似oracle输出；m,n无界。证明用每k≥4的显式有限两树族。
- Definitions / Scope：配置族含空集、向下封闭；gap是上确界，不声称有限实例取得2。
- Conclusion：对任何固定ε>0，不可能仅从任意T的配置可行性保证输出≤(2−ε)T；不推出相对OPT的主目标不可实现。
- Dependencies：配置边际投影＋UM-ST-ROUND-v1给上界；重索引两树族的OPT=2−1/k、T=1+1/k配置证书给下界。
- Evidence：VW原始Theorem2为Paper Fact；正文第4节独立重构，明确修正v1高度索引；配置证书与有限枚举/树DP分别核验。
- Counterevidence / Objections：原arXiv v1高度记号不一致，不照抄；本文由基例递推重索引并显式截减根边际。配置证书仅给T_CONF≤T，未声称T_CONF=T。
- Status：已知障碍的当前重构；非新不可近似性结果；审查范围见reviews。
- Related Files：正文第4节、FAILED_ROUTES.md、原始VW2014版本、精确核验代码与冻结结果。

## UM-LONG-PATH-GAP-v1：高围长简单图的配置间隙

- Exact Statement / Quantifiers：∀整数g≥3，在OPT(P)>0、每任务恰两条有限边、机器图简单且围长≥g的UM-MODEL-v1输入上，sup_P OPT(P)/T_CONF(P)=2。
- Objects / Domain / Definitions：机器图以机器为顶点、两端任务为边；阈值为精确配置阈值；sup仅取正最优值实例。
- Assumptions / Scope：非负二进制有理、无额外调度承诺；反例族只用{1/k,1,∞}。g固定但任意；m,n无界。
- Conclusion：消除平行任务或排除任意固定长度短环，仍不能单凭配置阈值统一舍入到低于2倍。
- Dependencies：UM-MODEL-v1、UM-TREE-CERTIFICATE-v1、UM-ST-ROUND-v1；长链阈值保真和配置证书转移见[正文](../current/unrelated_machines/long_path_coalition_gap.md)。
- Evidence：k≥4、ℓ≥2族的一般证明，OPT=2−1/k，配置可行T=1+1/k，girth=2ℓ；独立重构/冻结攻击和有限Fraction审计。
- Counterevidence / Objections：0/0域缺口已按审查显式修补；不声称T_CONF=T，不声称计算复杂度困难性或一般算法不可能。
- Status：完整范围证明、独立内部攻击、未外审；经典gap的运输扩展，全球新颖性和独立论文价值未认证。
- Related Files：long_path_coalition_gap.md、long_path_coalition_review.md、两个精确审计脚本与long_path_coalition_gap_audit.json，均由正文链接。

## UM-COALITION-PROJECTION-GAP-v1：固定机器联合投影的间隙

- Exact Statement / Quantifiers：∀整数r≥1、g≥3，在上述正最优值简单图围长≥g子类上，sup_P OPT(P)/T_CC,r(P)=2。
- Objects / Domain / Definitions：CC_r由[正文第1节](../current/unrelated_machines/long_path_coalition_gap.md#1-对象强化及量词)定义：同一个完整单机配置分布y；每个|U|≤r有不交配置元组见证，保持全部单机配置分布。不同U不要求多机交叠分布一致。
- Assumptions / Scope：r固定但任意，m,n无界；不是完整SA/全交叠层级，不假设有多项式精确oracle。
- Conclusion：仅增加这类固定机器联合投影仍不能相对该阈值统一优于2；包含仅匹配x_ij边际的更弱版本。
- Dependencies：UM-MODEL-v1、UM-LONG-PATH-GAP-v1、森林条件耦合引理；上界用UM-ST-ROUND-v1。森林耦合是标准工具的直接应用。
- Evidence：girth>r使所有≤r机器诱导森林，任意原配置分布均有所需见证；长链族给比值≥2−3/(k+1)。代码核对有限联合分布、全任务补全和路径传播。
- Counterevidence / Objections：完整三机交叠相容性反而在该树宽2族上精确；不能将本命题扩大到该更强合同或算法困难性。无主目标新近似保证。
- Status：完整范围证明、独立内部攻击、未外审、未认证新颖性；UM-TARGET-v1保持OPEN。
- Related Files：同上；精确例子与配置证书分别在examples/及evidence/certificates/unrelated_machines/。

## Paper Fact、解释与观察的边界

LST的2近似/ρ<3/2困难性、SV的2−1/m、restricted assignment的估值/准多项式构造等，逐条位置与假设在[LITERATURE](LITERATURE.md)和manifest；尚未重构的完整证明不能借本账本自动升级。没有“所有有限实验通过所以主目标成立”的Claim。更强困难性是可研究的独立方向，必须另定假设、常数和归约身份，不能把“某个2−ε不能达到”当作排除全部统一改善。

## UM-HEAVY-MATCH-FILTER-v1：大边匹配残余安全过滤

- Exact Statement / Quantifiers：∀合法P、∀有理T≥0，从p_ij≤T域出发执行正文§1精确GHMR，整个确定性过程在P,T总位长上多项式，保留每一个C_max≤T调度的所有使用边；拒绝蕴含OPT>T。
- Objects / Domain / Definitions：UM-MODEL-v1；小边p≤T/2，大边p>T/2；N无小端、U_i唯一小端i、F_i总小端时间；每个大边j→i查询覆盖N∪{j}且固定j→i的最大U_i任务权匹配W_ij。
- Assumptions / Scope：每大边机器最多一任务；仅删除无匹配或p_ij+F_i−W_ij>T的边，迭代到固定点；无配置求解或嵌套探测。零、空和不可用边均含。
- Conclusion：安全必要条件与位多项式过滤；接受不蕴含T可行，没有近似比例或一般输出调度。
- Dependencies：UM-MODEL-v1，任务权匹配贪心/增广的完整§2证明，逐次安全删边归纳。
- Evidence：自足普遍证明、先独立重构后冻结攻击、两路Fraction有限核验。
- Counterevidence / Objections：UM-ESCAPE-MATCH-GAP-v1保留gap趋2；未把逐查询最优匹配当共同调度。
- Status：本轮限范围完整证明及内部独立审查；标准匹配工具，全球新颖性/外审未认证。
- Related Files：[正文§1–3](../current/unrelated_machines/heavy_matching_residual_and_escape.md)、[审查](../reviews/unrelated_machines/heavy_matching_escape_review.md)、tests/audits/unrelated_machines/heavy_matching_residual.py及独立审计、evidence/runs/unrelated_machines/heavy_matching_residual_audit.json与heavy_matching_escape_independent.json。

## UM-SIMPLE-SUPPORT-GAP-v1：简单机器支撑的配置间隙

- Exact Statement / Quantifiers：∀整数k≥4，正文§4路径终端两树族合法、每任务恰2有限边、每无序机器对至多1任务，所有时间仅{1/k,1}，OPT=2−1/k，配置LP在T₀=1+1/k可行；故此子类sup OPT/T_CONF=2。
- Objects / Domain / Definitions：UM-MODEL-v1及UM-CONF-GAP-v1的重索引h、配置定义；末端平行束替换为k终端星及k−1条unit占位路径。
- Assumptions / Scope：k无界，实例有限但可很大；给出阈值证书而不声称T_CONF=T₀，不声称有限实例取得2。
- Conclusion：已知配置障碍在简单支撑下保持；不是计算复杂度困难性。
- Dependencies：UM-MODEL-v1、UM-ST-ROUND-v1（上界）、原两树核心配置递推、正文§4终端计数与显式配置。
- Evidence：普遍替换证明、独立同构重构、k=4逐配置与匹配证书；大k只作明确压缩核验。
- Counterevidence / Objections：没有尚成立fatal objection；该小强化可能属于标准改造，不能认证新颖性。
- Status：本轮限范围完整证明及内部独立审查，非新的近似算法；外审/新颖性未认证。
- Related Files：同正文§4及同审查/代码/证据；原经典gap身份不变。

## UM-ESCAPE-MATCH-GAP-v1：共享逃逸容量击穿逐星匹配

- Exact Statement / Quantifiers：∀整数k≥4，正文§5三选占位任务族P_k^esc满足OPT=2−1/k、T₀=1+1/k配置可行，GHMR从全部剪枝域首轮零删边即接受；故∀固定ε>0，∃(P,T)通过上述两个必要测试但OPT>(2−ε)T。
- Objects / Domain / Definitions：§4族加一机器z，每占位任务新增成本1/2的z边；核心/星任务恰2选，占位任务恰3选；GHMR为本页精确定义的UM-HEAVY-MATCH-FILTER-v1。
- Assumptions / Scope：k≥4保证h≥3；配置与各查询是独立证书，不声称存在共享联合分布；不包含nested probing、联合容量或所有匹配强化。
- Conclusion：这两个必要测试的合取不足以得到相对其T的统一低于2保证；不排除相对OPT的新算法。
- Dependencies：UM-MODEL-v1、§4路径配置和上界调度、§5至少二叉下传及四活跃簇迫使z负载≥2、逐类强制匹配证书。
- Evidence：一般证明、独立重构和冻结攻击；展开k=4的配置及全部大边匹配，压缩参数范围单独记录。
- Counterevidence / Objections：k=2,3的h=1不在身份内（添加z可能降低OPT）；遗漏此条件会使声明错误。单查询未匹配任务的小端容量以及查询间一致性均未表达。
- Status：本轮限范围完整方法反例及内部独立审查；主目标OPEN，外审/新颖性未认证。
- Related Files：正文§5–7、heavy_matching_escape_review.md、两路审计与冻结证据。

## 成束强化与细分攻击的新接口

三个身份只限制准确的方法合同，不关闭UM-TARGET-v1。

### UM-BUNDLE-MOMENT-v1：末端任务束的聚合二阶相容阈值

- Exact Statement / Quantifiers：For every k>=4 the canonical VW two-tree instance has strengthened configuration threshold exactly 2-1/k after adding the aggregate second-moment complement equation for each terminal bundle.
- Objects / Domain / Definitions：UM-MODEL-v1；正文第2节式(1)、第3节闭包或第4节两机器LP，各自范围不互换。
- Assumptions / Scope：第一项仅既有k≥4族；第二项一般合法输入、T≥0；第三项每任务恰两台可用机器、正最优值，m,n无界。
- Conclusion：分别为旧族强化效果、健全过滤/可算下界、特定LP上确界间隙2；均非新的OPT相对近似保证。
- Dependencies：UM-MODEL-v1；族结论使用UM-TREE-CERTIFICATE-v1；gap上界另用UM-ST-ROUND-v1。具体定义与完整推导见正文。
- Evidence：自足一般证明，冻结审查，Fraction与独立枚举，范围见实际记录。
- Counterevidence / Objections：过滤器及二阶修补被任务细分绕过；不能将接受当作调度可行；不排三机器overlap一致性或先消去mid。没有在已声明范围内尚成立的fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；源机制可能为标准工具直接推论，外部评审/新颖性未认证。
- Related Files：[research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)、[冻结审查](../reviews/unrelated_machines/bundle_subdivision_review.md)、`evidence/runs/unrelated_machines/bundle_subdivision_audit.json`。

### UM-CARDINALITY-CLOSURE-v1：强制残余容量的健全多项式计数闭包

- Exact Statement / Quantifiers：For all legal P and rational T>=0 the synchronous forced-residual cardinality filter preserves every T-feasible schedule and terminates in deterministic bit-polynomial time. Its monotone integer-scaled bisection gives a lower bound B<=OPT; acceptance is not feasibility.
- Objects / Domain / Definitions：UM-MODEL-v1；正文第2节式(1)、第3节闭包或第4节两机器LP，各自范围不互换。
- Assumptions / Scope：第一项仅既有k≥4族；第二项一般合法输入、T≥0；第三项每任务恰两台可用机器、正最优值，m,n无界。
- Conclusion：分别为旧族强化效果、健全过滤/可算下界、特定LP上确界间隙2；均非新的OPT相对近似保证。
- Dependencies：UM-MODEL-v1；族结论使用UM-TREE-CERTIFICATE-v1；gap上界另用UM-ST-ROUND-v1。具体定义与完整推导见正文。
- Evidence：自足一般证明，冻结审查，Fraction与独立枚举，范围见实际记录。
- Counterevidence / Objections：过滤器及二阶修补被任务细分绕过；不能将接受当作调度可行；不排三机器overlap一致性或先消去mid。没有在已声明范围内尚成立的fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；源机制可能为标准工具直接推论，外部评审/新颖性未认证。
- Related Files：[research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)、[冻结审查](../reviews/unrelated_machines/bundle_subdivision_review.md)、`evidence/runs/unrelated_machines/bundle_subdivision_audit.json`。

### UM-PAIR-SUBDIVISION-GAP-v1：两机器配置耦合的细分间隙2

- Exact Statement / Quantifiers：The pair-configuration LP, with common singleton machine marginals and exact complementarity for every degree-two job internal to each pair, has supremum gap 2 even on simple bipartite machine graphs. The stated cardinality filter makes no deletion on the subdivided VW certificates.
- Objects / Domain / Definitions：UM-MODEL-v1；正文第2节式(1)、第3节闭包或第4节两机器LP，各自范围不互换。
- Assumptions / Scope：第一项仅既有k≥4族；第二项一般合法输入、T≥0；第三项每任务恰两台可用机器、正最优值，m,n无界。
- Conclusion：分别为旧族强化效果、健全过滤/可算下界、特定LP上确界间隙2；均非新的OPT相对近似保证。
- Dependencies：UM-MODEL-v1；族结论使用UM-TREE-CERTIFICATE-v1；gap上界另用UM-ST-ROUND-v1。具体定义与完整推导见正文。
- Evidence：自足一般证明，冻结审查，Fraction与独立枚举，范围见实际记录。
- Counterevidence / Objections：过滤器及二阶修补被任务细分绕过；不能将接受当作调度可行；不排三机器overlap一致性或先消去mid。没有在已声明范围内尚成立的fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；源机制可能为标准工具直接推论，外部评审/新颖性未认证。
- Related Files：[research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md](../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)、[冻结审查](../reviews/unrelated_machines/bundle_subdivision_review.md)、`evidence/runs/unrelated_machines/bundle_subdivision_audit.json`。

UM-PAIR-SUBDIVISION-GAP-v1的pair-LP核心是UM-COALITION-PROJECTION-GAP-v1的r=2特例；本页登记保留独立长度2重构及与计数闭包的准确合同，不把两个身份当作两次原创突破。

## UM-JOINT-SMALL-ROUND-v1：给定共同大边见证的条件舍入

- Exact Statement / Quantifiers：∀合法P、∀有理T≥0、δ≥0及正文(Aδ)的有理见证H,x，可在(P,T,δ,H,x)总位长的多项式时间内确定性输出全部任务合法调度，保持H，∀i有L_i≤(3/2+δ)T。
- Objects / Domain / Definitions：UM-MODEL-v1；H为p∈(T/2,T]的大边整数匹配，剩余x只用p≤T/2小边，且h_i+Σp_ijx_ij≤(1+δ)T。
- Assumptions / Scope：输入已经给出共同H与x；T=0、空任务和零边包含；不含找到H的算法。
- Conclusion：真实调度及全部机器同时负载界；δ=0的3/2是ST直接推论，不是无条件通用3/2算法。
- Dependencies：UM-MODEL-v1、UM-ST-ROUND-v1的加性排序槽证明，精确合同(Aδ)。
- Evidence：完整推导、冻结独立审查，实际给定见证舍入与边界检查。
- Counterevidence / Objections：共同H选择不可当普通匹配；UM-JOINT-CHOICE-NP-v1仅限精确/低余量接口，不排所有近似路线。
- Status：完整条件性构造证明，标准工具直接推论；内部独立审查，外审/新颖性未认证。
- Related Files：[共同选择与块切面正文](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)、joint_matching_completion_review.md、三份相关审计代码与joint_matching_completion_audit.json。

## UM-JOINT-CHOICE-NP-v1：唯一小端共同匹配选择的精确困难

- Exact Statement / Quantifiers：∀固定有理δ∈[0,1/3)，判定上述(Aδ)见证是否存在为NP完全，即使T=1、每任务恰一个small端（N空）、所有有限时间仅{1/3,1}。
- Objects / Domain / Definitions：大小分界仍按原T/2，匹配大边限p≤T；δ仅放宽剩余总分数容量，不改大小边定义。
- Assumptions / Scope：显式有限3DM输入多项式归约；NP完全性无假设，排多项式精确oracle需P≠NP；不含δ=1/3。
- Conclusion：整体H与残余容量耦合不是免费匹配oracle；不是主目标或某个近似比的困难性结论。
- Dependencies：UM-MODEL-v1、接口(Aδ)、Karp1972完美3DM NP完全性Paper Fact（原p94/95，本次2010重印PDF14/15已图像核对）、正文无pins归约和NP证书位长证明。
- Evidence：正反两向全量词归约；q=0/s=0边界；唯一small使剩余质量0/1、负载1/3网格；两路独立调度oracle。
- Counterevidence / Objections：δ=1/3时q1空三元组、4激活任务源负载4/3给归约失效；旧归约本身不排δ∈[1/3,1/2)；新UM-JOINT-HALF-CHOICE-NP-v1另用半单位输入关闭该窗口。其他算法仍未排除。
- Status：完整限域复杂度证明、内部独立审查；经典源困难性未在本专题重证，外审/新颖性未认证。
- Related Files：同正文§3、原始Karp重印/manifest、审查和精确代码/冻结证据。

## UM-ESCAPE-BLOCK-CUT-v1：条件末簇容量恢复逃逸族真实阈值

- Exact Statement / Quantifiers：∀整数k≥4、∀有理1≤B≤θ_k=2−1/k，在P_k^esc末簇g上，Z_g≥(r_B−1)Y_v为每个B可行整数调度的有效不等式，r_B=k−floor(k(B−1))。将每簇该切面加到配置LP，则B<θ_k时不可行，B=θ_k时可行，故该族强化阈值恰θ_k；B<1由根任务拒绝。
- Objects / Domain / Definitions：UM-ESCAPE-MATCH-GAP-v1的明确族；Y_v父端incoming选择，Z_g该簇reserve去共同z数量，配置版用相应包含边际。
- Assumptions / Scope：切面随B重算；在T₀时r−1=k−2，但θ处系数0；只对已识别本族，未给一般块分离oracle。
- Conclusion：修复整个逃逸族而不只是单份旧证书；没有一般gap界或调度近似。
- Dependencies：UM-MODEL-v1、UM-ESCAPE-MATCH-GAP-v1族及上界调度、每层单机配置计数+任务覆盖、终端条件占位计数、z的配置负载≤B。
- Evidence：一般不等式/对所有强化解的矛盾证明；两路局部定向枚举和精确floor区间检查。
- Counterevidence / Objections：固定使用T₀系数到θ会变成无效切面，禁止；多机条件化可能是标准层级投影，新颖性未认证。
- Status：完整限族强化证明及内部独立审查；一般求解、分离和舍入仍OPEN。
- Related Files：同正文§4、冻结审查和块容量有限核验。


## UM-TREE-MARKOV-COMPLETION-NO-v1：生成树投影后的固定补全反例

- Exact Statement / Quantifiers：存在五机、每任务恰两端的简单机器图输入P、T=OPT=1、真实全局T分布D及指定连通生成树F，使D的完整单机/树边pair边际经Markov树耦合后，有正概率1/4的态在冻结F任务后任何补全都至少2T，且可达2T。
- Objects / Domain / Definitions：UM-MODEL-v1的上述子类；树耦合按完整父配置条件化。非树任务暂时选择丢弃，仅冻结F任务。
- Assumptions / Scope：被否定的是“所有这类输入、每个正概率态都可补<2T”的合同；不更换树、不迁移F任务。正面边界：同合同连通树至多四机均可补T。
- Conclusion：不能在任意树支持态后沿用原残量LP可行性或直接保证统一低于2；不排算法本身。
- Dependencies：UM-MODEL-v1、明确有限输入与真实D、标准Markov树条件耦合；不依赖复杂度假设。
- Evidence：五机逐项证明、中心顶点/边的小机器数边界、两个独立Fraction实现及全部32个调度枚举。
- Counterevidence / Objections：本坏态只需迁移一个任务即可修复；好的择态、换树、更多相关信息和使用原D均未被排除。
- Status：完整所述范围反例，独立内部攻击、未外审、全球新颖性未认证；UM-TARGET-v1保持OPEN。
- Related Files：[正文](../current/unrelated_machines/tree_markov_completion.md)、[冻结审查](../reviews/unrelated_machines/tree_markov_completion_review.md)，代码和冻结输入/结果由正文链接。

## 精确星消去与共享容量接口

### UM-MINIMAL-STAR-CONTRACTION-v1：极小超载星的精确消去与调度提升

- Exact Statement / Quantifiers：For every legal P,T>=0 after pruning p>T, if a machine full neighborhood F has S>T and S-p_va<=T for every a, its replacement by one job with outside min times preserves T-feasibility. Every reduced schedule B lifts in deterministic bit-polynomial time to max(B,T); <=m repeated contractions retain the same bound.
- Objects / Domain / Definitions：UM-MODEL-v1；新稿第1节剪枝/极小星，第3节显式资源族，第4节GPC₂，第5节残余profile。
- Assumptions / Scope：消元针对全邻域并保持阈值T；gap仅正最优输入与所定义pair/预处理合同；q压缩仅固定q普通任务、同外机及全部列明profile。
- Conclusion：精确可恢复消元、特定强化上确界间隙、特定表示不可能性；均不代替UM-TARGET-v1。
- Dependencies：UM-MODEL-v1；gap上界另用UM-ST-ROUND-v1、UM-CARDINALITY-CLOSURE-v1及极小星恢复引理。具体条件和自足证明见新稿。
- Evidence：一般证明、独立先重构后攻击、精确有限审计；原始BLMRS2024只作为机制来源，第5节来源boss4。
- Counterevidence / Objections：不允许部分邻域消去、不允许重复min当多任务身份、不把pair witnesses当全joint；初稿OPT>0域省略已修补。已声明范围无尚成立fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。已知资源机制/标准工具扣除后不宣称新近似或独立论文价值。
- Related Files：[自足正文](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结审查](../reviews/unrelated_machines/minimal_star_capacity_review.md)、`evidence/runs/unrelated_machines/minimal_star_capacity_audit.json`。

### UM-CAPACITY-ONE-PAIR-GAP-v1：不可极小星消去的容量一资源族及全pair间隙2

- Exact Statement / Quantifiers：Over positive-OPT UM inputs the general pair-configuration LP GPC2 has supremum gap 2, even after iterating the specified residual-cardinality filter and minimal-star contraction. Explicit two-value family has m=k²+3k-1,n=2k²+k,T=1,OPT=2-1/k, all pair witnesses, and neither preprocessing rule triggers for k>=3.
- Objects / Domain / Definitions：UM-MODEL-v1；新稿第1节剪枝/极小星，第3节显式资源族，第4节GPC₂，第5节残余profile。
- Assumptions / Scope：消元针对全邻域并保持阈值T；gap仅正最优输入与所定义pair/预处理合同；q压缩仅固定q普通任务、同外机及全部列明profile。
- Conclusion：精确可恢复消元、特定强化上确界间隙、特定表示不可能性；均不代替UM-TARGET-v1。
- Dependencies：UM-MODEL-v1；gap上界另用UM-ST-ROUND-v1、UM-CARDINALITY-CLOSURE-v1及极小星恢复引理。具体条件和自足证明见新稿。
- Evidence：一般证明、独立先重构后攻击、精确有限审计；原始BLMRS2024只作为机制来源，第5节来源boss4。
- Counterevidence / Objections：不允许部分邻域消去、不允许重复min当多任务身份、不把pair witnesses当全joint；初稿OPT>0域省略已修补。已声明范围无尚成立fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。已知资源机制/标准工具扣除后不宣称新近似或独立论文价值。
- Related Files：[自足正文](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结审查](../reviews/unrelated_machines/minimal_star_capacity_review.md)、`evidence/runs/unrelated_machines/minimal_star_capacity_audit.json`。

### UM-STAR-Q-JOB-COMPRESSION-NO-v1：任意多任务星的普通任务残余接口压缩障碍

- Exact Statement / Quantifiers：For every integer q>=2, there is a (q+1)-job star with T=1 for which no q ordinary replacement jobs on the same external machines, with arbitrary nonnegative/infinite times and no extra identity constraints, preserve feasibility for every specified A/B residual capacity profile.
- Objects / Domain / Definitions：UM-MODEL-v1；新稿第1节剪枝/极小星，第3节显式资源族，第4节GPC₂，第5节残余profile。
- Assumptions / Scope：消元针对全邻域并保持阈值T；gap仅正最优输入与所定义pair/预处理合同；q压缩仅固定q普通任务、同外机及全部列明profile。
- Conclusion：精确可恢复消元、特定强化上确界间隙、特定表示不可能性；均不代替UM-TARGET-v1。
- Dependencies：UM-MODEL-v1；gap上界另用UM-ST-ROUND-v1、UM-CARDINALITY-CLOSURE-v1及极小星恢复引理。具体条件和自足证明见新稿。
- Evidence：一般证明、独立先重构后攻击、精确有限审计；原始BLMRS2024只作为机制来源，第5节来源boss4。
- Counterevidence / Objections：不允许部分邻域消去、不允许重复min当多任务身份、不把pair witnesses当全joint；初稿OPT>0域省略已修补。已声明范围无尚成立fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。已知资源机制/标准工具扣除后不宣称新近似或独立论文价值。
- Related Files：[自足正文](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结审查](../reviews/unrelated_machines/minimal_star_capacity_review.md)、`evidence/runs/unrelated_machines/minimal_star_capacity_audit.json`。

## UM-HEAVY-ALTERNATIVE-FILTER-v1：重备选星匹配的安全删边接口

- Exact Statement / Quantifiers：∀合法P、∀二进制有理T≥0，从p≤T的域开始反复执行正文§2式(1)，保留每一个makespan≤T调度的全部边，并在(P,T)总位长的确定性多项式时间内终止；空域蕴含OPT>T。
- Objects / Domain / Definitions：UM-MODEL-v1；F_i(j)包含除j外能在i执行且全部其他当前端均耗时>T/2的任务（无备选按空真）；W是F到其他机器的最大任务源端权部分匹配。
- Assumptions / Scope：只使用p_ij+sum_F p_iell−W>T删边；包括小探测、零、空任务、单可用边；不额外覆盖F外的全局必经大任务。
- Conclusion：安全必要条件，接受不意味着可行或输出调度。与既有GHMR相关但合同不同；不重复主张匹配工具的新颖性。
- Dependencies：UM-MODEL-v1；真实移出任务的大于半阈值注入、非负负载、标准最大权二分匹配。
- Evidence：正文§2的一般证明与总轮数/位长；先独立重构后冻结攻击；独立3375小矩阵上8192可行调度边保持核验。
- Counterevidence / Objections：UM-DILUTED-SINK-PROBE-GAP-v1使此过滤无首次删除；没有全局近似保证。
- Status：完整所述范围证明及内部独立审查；标准匹配接口，外审/新颖性未认证。
- Related Files：[正文](../current/unrelated_machines/diluted_sink_probe_gap.md)、[冻结审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)、两路代码与证据由正文和本题地图链接。

## UM-DILUTED-SINK-PROBE-GAP-v1：独立配置证书与全部逐边线性探针的共同间隙2

- Exact Statement / Quantifiers：∀整数k≥4，存在正文§4显式合法P_k、T_k=1+1/k，使OPT=2−1/k，配置LP在T_k可行，全部有限边均未剪枝且每边分别有x_ij=1的同目标剪枝LST点，UM-HEAVY-ALTERNATIVE-FILTER-v1不删任何边。因此这些独立证书测试合取/联合迭代的相对阈值sup gap=2。
- Objects / Domain / Definitions：UM-MODEL-v1；重索引两树每底端换N=k(k−1)终端和N−1个全终端可用unit阻塞任务；条件LST点彼此独立，配置证书与条件点不耦合。
- Assumptions / Scope：每个k给有限实例；阻塞任务有N可用机器，不保留degree2；有限时间仅{1/k,1}。未声称精确配置阈值等于T_k或实例规模在log k上多项式。
- Conclusion：∀统一ε>0，∃通过全部上述测试的(P,T)而OPT>(2−ε)T；不否定UM-TARGET-v1或相对OPT的其他算法。
- Dependencies：UM-MODEL-v1、UM-TREE-CERTIFICATE-v1的树内递推、第3节容量稀释引理、第5–8节全部证书；sup上界另用UM-ST-ROUND-v1。
- Evidence：完整一般证明、先独立重构后冻结攻击、Fraction实际配置/条件点/星匹配/整数上界；k4主审计全4562边、独立审计58条件点及全部星；k2独立128调度枚举。
- Counterevidence / Objections：在条件LP内部加入大任务基数约束即识别此族；本族也被覆盖全部unit阻塞任务的GHMR识别。未排除条件配置LP、SA、全局容量相关或更强过滤。
- Status：完整所述范围方法反例、内部独立已审，外审/新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/diluted_sink_probe_gap.md)、[审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)、diluted_sink_probe_gap.py、independent_dilution_audit.py及两份冻结结果。

## UM-BIG-CARDINALITY-PROBE-v1：条件化大任务槽的安全探针与本族精确识别

- Exact Statement / Quantifiers：∀合法P、∀二进制非负有理C，逐边强制x_ij=1并在剪枝LST内加入每机sum_{j:p_ij>C/2}x_ij≤1、删去不可行边并迭代，保留全部C可行调度且总位多项式；对每个UM-DILUTED-SINK-PROBE-GAP-v1实例P_k，拒绝当且仅当C<OPT=2−1/k。
- Objects / Domain / Definitions：UM-MODEL-v1；条件化前每次重建当前域LP；严格>C/2为大边；拒绝为空域。
- Assumptions / Scope：一般安全性包括零值、空任务、单可用边；准确阈值只针对本文未加逃逸边的显式族。标准有理LP算法可调用，未实现通用LP求解器。
- Conclusion：多项式必要条件及一族的精确识别；未建立一般间隙、舍入保证或主目标算法。
- Dependencies：UM-MODEL-v1、真实大任务每机至多一项、单调域收缩、安全删边归纳、第9节终端槽总和与底向上传播。
- Evidence：正文一般证明、独立冻结审查；软件状态为未实现通用LP，有限证书审计不能当作该程序运行。
- Counterevidence / Objections：尚无其与配置可行性合取后的全类统一余量或一般构造；本文旧反例不是对该更强合同的反例。
- Status：完整所述范围证明、内部独立已审；外审/新颖性未认证，未宣称新算法近似比。
- Related Files：[正文§9](../current/unrelated_machines/diluted_sink_probe_gap.md#9-多项式的加强探针准确识别本族)、[审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)。


## UM-DILUTED-ESCAPE-PROBE-GAP-v1：共享逃逸与全部普通边探针的共同间隙2

- Exact Statement / Quantifiers：∀整数k≥4，正文§11的显式新实例P̂_k在T=1+1/k配置可行，全部有限边（含新增z边）分别有x_ij=1的同目标剪枝LST点，既有GHMR及本页星匹配均首轮零删除，而OPT=2−1/k。因此这四种独立必要证书合取/迭代的相对阈值sup gap=2。
- Objects / Domain / Definitions：UM-MODEL-v1；UM-DILUTED-SINK-PROBE-GAP-v1的每个阻塞任务另加同一z上1/2边；GHMR精确采用UM-HEAVY-MATCH-FILTER-v1；不同条件点不要求共享分布。
- Assumptions / Scope：k≥4保证h≥3；阻塞任务有N+1个可用机器，有限时间{1/k,1/2,1}；不含强制后嵌套GHMR、条件配置LP或条件大任务基数。
- Conclusion：∀固定ε>0，∃上述通过全部测试的(P,T)而OPT>(2−ε)T；未否定OPT相对算法或UM-TARGET-v1。
- Dependencies：UM-MODEL-v1、UM-DILUTED-SINK-PROBE-GAP-v1的底座证书、UM-ESCAPE-MATCH-GAP-v1的共享小端机制、现行GHMR合同；上界另用UM-ST-ROUND-v1；新增边后整数下界重新证明。
- Evidence：至少四活跃底簇的一般证明、全部边分类证书、先独立重构后冻结攻击；k4主审计全部4914边LST点/星、4394 GHMR查询、实际规范GHMR零删除；独立102条件点及全部匹配重算。
- Counterevidence / Objections：同行随B重算的条件块切面Z_g≥(r_B−1)Y_v仍识别此族：本N终端组同样最多N−d个单位blockers留终端；见UM-ESCAPE-BLOCK-CUT-v1，未另报为新定理。第9节底座准确阈值不自动推广到此变体。
- Status：完整所述合同反例、内部独立已审；外审/全球新颖性未认证，主目标OPEN。
- Related Files：[正文§11](../current/unrelated_machines/diluted_sink_probe_gap.md#11-共享小端与稀释终端的共同探针边界)、[两阶段审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)、diluted_escape_probe_gap.py与independent_diluted_escape_audit.py及冻结结果。

## UM-JOINT-HALF-CHOICE-NP-v1：半单位共同选择的全窗口NP完全边界

- Exact Statement / Quantifiers：∀固定有理δ∈[0,1/2)，T=1、唯一small端、有限时间仅{1/2,1}时(Aδ)存在性NP完全，且该整个子类上(Aδ)存在⇔OPT≤1。
- Objects：UM-MODEL-v1，正文(Aδ)的大边匹配H和剩余small分数分配x。
- Domain：显式合法矩阵；T=1；每任务恰一个small端；有限时间仅1/2和1；m,n可变。
- Definitions：大小分界固定原T/2；未选任务唯一small使剩余分配0/1。
- Assumptions：NP完全性本身无P≠NP假设，导入完美3DM源事实。
- Scope：δ∈[0,1/2)，不含1/2；旧UM-JOINT-CHOICE-NP-v1的时间与范围不变。
- Conclusion：整个δ<1/2见证存在性窗口NP完全；不是统一低于2近似困难性。
- Dependencies：UM-MODEL-v1、(Aδ)、Karp1972完美3DM事实、逐x源显式归约、半整数与NP证书界。
- Evidence：自足两向证明、先重构后冻结攻击、双路整数/Fraction审计。来源boss4公屏166；本阶段核实与规范化保存。
- Counterevidence / Objections：δ=1/2时本构造全部留small即通过；q0用闲置机器修补m≥1。当前声明范围无未解fatal；未认证新颖性。
- Status：complete stated-scope proof with independent internal reconstruction and exact audits; unrefereed; novelty unverified。
- Related Files：[research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)§3a、`research/reviews/unrelated_machines/half_unit_joint_choice_review.md`、`evidence/runs/unrelated_machines/half_unit_joint_choice_audit.json`及两份新审计。

## UM-JOINT-HALF-PROMISE-NO-v1：半单位共同见证承诺搜索的全窗口障碍

- Exact Statement / Quantifiers：假设P≠NP，∀固定有理δ∈[0,1/2)，不存在总确定性位多项式算法，对所有OPT≤T的合法输入保证输出(Aδ)见证；即使只要求T1、唯一small、时间{1/2,1}子类亦不可能。域外可任意输出。
- Objects：UM-MODEL-v1，正文(Aδ)的大边匹配H和剩余small分数分配x。
- Domain：显式合法矩阵；T=1；每任务恰一个small端；有限时间仅1/2和1；m,n可变。
- Definitions：大小分界固定原T/2；未选任务唯一small使剩余分配0/1。
- Assumptions：明确假设P≠NP及算法总确定性位多项式；非承诺输入可任意输出。
- Scope：δ∈[0,1/2)，不含1/2；旧UM-JOINT-CHOICE-NP-v1的时间与范围不变。
- Conclusion：排除这条充分见证路线；不排联合舍入或不输出该见证的调度算法。
- Dependencies：UM-JOINT-HALF-CHOICE-NP-v1、P≠NP、总时间界和可验证证书。
- Evidence：自足两向证明、先重构后冻结攻击、双路整数/Fraction审计。来源boss4公屏166；本阶段核实与规范化保存。
- Counterevidence / Objections：δ=1/2时本构造全部留small即通过；q0用闲置机器修补m≥1。当前声明范围无未解fatal；未认证新颖性。
- Status：complete stated-scope proof with independent internal reconstruction and exact audits; unrefereed; novelty unverified。
- Related Files：[research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)§3a、`research/reviews/unrelated_machines/half_unit_joint_choice_review.md`、`evidence/runs/unrelated_machines/half_unit_joint_choice_audit.json`及两份新审计。

## UM-GLOBAL-ROW-COUNT-FILTER-v1：全局单行基数匹配的安全过滤

- Exact Statement / Quantifiers：∀合法P、有理T≥0，正文§1同步过滤在(P,T)总编码位长多项式内终止，保留每一个T可行调度使用的全部边。固定同一组全行有效H_i及c_i时，最大全局查询等价支配所有相应资源子池查询。
- Objects / Domain / Definitions：UM-MODEL-v1；当前剪枝域D；h_i为全当前行最小存活时间，空行c_i=0、零min为n、正min为min(n,floor(T/h_i))。每边j→v固定后，覆盖所有不能留v的任务，以容量匹配最大化其他邻任务从v的卸载权。
- Assumptions / Scope：任务权仅依任务，非任意边权；全机真实负载只对被查询v精确，其余只约束计数。每池另行提高下界不属全池支配结论。含空、零、不可用边、大分母。
- Conclusion：健全位多项式必要条件；拒绝⇒OPT>T，接受不是调度可行或新近似保证。
- Dependencies：模型；任务权匹配前缀/增广证明及容量克隆；逐轮保边归纳；至多e个删边轮。
- Evidence：自足一般证明、独立先重构后冻结攻击；全部所列小矩阵的精确全分配oracle核查询值/真调度保边。
- Counterevidence / Objections：UM-COMPACT-COUNT-ESCAPE-GAP-v1中所有查询通过而OPT趋2。H=0不能除法或复制巨大槽，规范实现作n截断；未留此异议。
- Status：完整所述范围证明及内部独立审查；标准匹配容量扩展，外审/全球新颖性未认证。
- Related Files：[正文§1](../current/unrelated_machines/row_count_escape_gap.md)、row_count_escape_review.md、row_count_probe.py、row_count_escape_audit.json。

## UM-COMPACT-COUNT-ESCAPE-GAP-v1：紧凑共享逃逸与全部单行计数见证

- Exact Statement / Quantifiers：∀整数k≥2，正文§2的N=2k²块、N−2k全局单位机、Y共享z成本1/k族满足OPT=2−1/k、GPC₂(1)可行。极小星消元与既有单/双域计数闭包无起点；UM-GLOBAL-ROW-COUNT-FILTER-v1首轮零删边。对每台v、每个C∈C_v(1)，均存在v精确取C且全部其他机器守初始row-min计数cap的全任务分配。因此这些必要条件合取在正OPT输入的sup gap恰2。
- Objects / Domain / Definitions：UM-MODEL-v1；m=2k³+6k²−2k+1、n=4k³+2k²，时间仅{1/k,1,∞}。GPC₂为完整单机边际与各pair不双选，不要求跨pair交叠一致；V/z cap k、G/R cap1。
- Assumptions / Scope：不同查询/配置延伸可用不同分配；其他机器不要求真实负载≤1；不含条件LST、条件配置LP或全部共同负载。预处理仅指正文列明的规则，非所有局部消元。
- Conclusion：任何固定ε>0取k>1/ε即击穿相对接受T的(2−ε)T合同；不否定相对OPT算法或UM-TARGET-v1。
- Dependencies：模型、GPC₂定义、全局过滤合同；显式配置/pair及avoid-v构造、整数容量计数；ST加性舍入给gap上界，若先消元用max(2T,T)恢复。
- Evidence：一般证明及冻结独立攻击；两路精确配置/pair、全机avoid证书、k2全部实际优化查询、独立单块真实转移对称DP。真实有限参数在冻结记录，未做全实例全调度枚举。
- Counterevidence / Objections：既有条件块cut直接适配即可把本族强化阈值恢复θ_k；这不是该更强机制的反例。N块/激活缺口与旧k块/缺口1族不同，不覆盖旧Claim。无尚成立fatal objection，全球新颖性未认证。
- Status：完整所述合同反例、内部独立已审；未外审，未给统一近似算法。
- Related Files：[正文§2–5](../current/unrelated_machines/row_count_escape_gap.md)、row_count_escape_review.md、compact_count_escape.py、independent_row_count_escape.py、row_count_escape_audit.json及k2实际输入/证书。

## UM-ROW-SPREAD-TWO-ROUND-v1：逐机两倍跨度的直接联合槽构造

- Exact Statement / Quantifiers：∀合法非负有理UM输入，删除有零端任务后，若每个非空机器行的有限正时间均在某[γ_i,2γ_i]内（各γ_i>0可不同），则存在确定性位多项式算法输出全部原任务合法调度，C_max≤3OPT/2；含空任务/OPT0。
- Objects：UM-MODEL-v1的原始矩阵、零任务预处理、逐行固定γ_i、目标T、分数LP及覆盖槽匹配。
- Domain：二进制非负有理/∞，m≥1,n≥0；行尺度和分母不固定。
- Definitions：剩余行γ_i取最小有限时间，跨度max/min≤2；两个严格阈值前缀及T<4γ_i时的总计数。
- Assumptions：保留明确额外行跨度结构；只调用标准有理LP位多项式算法，不调用配置或共同H oracle。
- Scope：该受限类全输入；一般跨度无界不在范围。
- Conclusion：实际全部任务的确定性位多项式3/2近似；不输出NP难的(Aδ)中间证书。
- Dependencies：UM-MODEL-v1、UM-ST-ROUND-v1、整数前缀槽保持、四区间估计、有理gcd格点及单调LP搜索；VW2010 Theorem8为机制来源，不把本推论说成原文定理。
- Evidence：自足证明、先重构后冻结攻击、83810局部行及实际半单位奇偶实例精确核验。
- Counterevidence / Objections：行内tiny与large任意混合无法归入本类；尚无一般跨尺度归约；无当前范围fatal异议。
- Status：complete stated-scope proof; known-tool corollary with independent reconstruction and exact audits; unrefereed; novelty unverified。
- Related Files：[research/current/unrelated_machines/joint_slot_prefix_rounding.md](../current/unrelated_machines/joint_slot_prefix_rounding.md)、`research/reviews/unrelated_machines/joint_slot_prefix_review.md`、两份审计与`evidence/runs/unrelated_machines/joint_slot_prefix_audit.json`。

## UM-SPARSE-CONDITIONED-CONFIG-GAP-v1：三选稀疏深树的全边独立条件配置间隙

- Exact Statement / Quantifiers：∀整数k≥3，按正文s0、M及任意合法H构造的有限实例P满足每任务至多3台可用机器、有限时间仅{1/k,1,γ}，γ=2^(2−H)，OPT=2−1/k。在T=1+1/k时，∀有限边(i,j)，存在同一完整实例的配置LP点满足x_ij=1。因此仅迭代删除无独立条件配置证书的边，从初始域第一轮即零删除；基数LST单边探针亦全通过。由本族比值2−3/(k+1)及ST上界，正目标独立证书合同的sup相对阈值间隙为2。
- Objects / Domain / Definitions：UM-MODEL-v1；两棵H层k叉核心树、每底簇k星终端与k−1路径占位任务、全局γ成本逃逸机z；s0=min{s≥1:k((k−1)/k)^s≤1}，M=(k−1)k^(s0−2)，H≥s0且2^(H−2)≥M。配置及强制覆盖定义见正文。
- Assumptions / Scope：T>0的显式反例族；各边查询的配置分布相互独立，不要求共同基点、平均回收或多机交叠一致性。允许∞；每任务有有限边。不声称精确配置oracle位多项式，也不声称对log k多项式展开。
- Conclusion：加强到每次探针内完整单机配置仍不足以相对其阈值统一优于2；不排除UM-TARGET-v1或相对OPT的其他算法。
- Dependencies：UM-MODEL-v1；正文内部α→((k−1)/k)α配置递推、坏簇全移z的共同容量证书、整数二叉激活计数与单路径上界；sup上界另用UM-ST-ROUND-v1。机制来源连接既有共享逃逸及boss1事件168，正文自足重构。
- Evidence：全部6类强制边的一般证书、独立先重构后冻结攻击、双路Fraction；k3,H5实际729机1051任务全部2426有限边逐点核验；大k仅冻结结果记载的压缩公式核验。
- Counterevidence / Objections：只移ceil(kβ−1)条固定路径占位边的总槽捷径无效，已改为坏簇全部撤离且总数≤M。完整四机器bag联合分布在整个交集上一致可精确glue本族；路径端点可触发极小星消元，本命题未覆盖加入该预处理后的合同。
- Status：完整所述范围证明、内部独立重构及冻结审查；未外审、未认证全球新颖性或独立论文价值。主目标仍OPEN。
- Related Files：[research/current/unrelated_machines/sparse_conditioned_configuration_gap.md](../current/unrelated_machines/sparse_conditioned_configuration_gap.md)、[research/reviews/unrelated_machines/sparse_conditioned_configuration_review.md](../reviews/unrelated_machines/sparse_conditioned_configuration_review.md)；正文链接两路代码、实际稀疏输入、配置/调度证书与冻结结果。

## UM-COMPACT-MULTIROW-EXTENSION-v1：共同真实负载行数的尖锐中心预算

- Exact Statement / Quantifiers：∀整数k≥2，在UM-COMPACT-COUNT-ESCAPE-GAP-v1的同一族中，∀U⊆M且|U∩V|≤N−2k，∀v∈U，∀C∈C_v(1)，可确定性输出完整合法σ，σ⁻¹(v)=C，∀i∈U有L_i≤1，∀i∈M任务数≤初始c_i。构造时间在族实际编码长度上多项式。该统一预算尖锐：∃含N−2k+1个中心及z的U、v=z、C=∅使上述分配不存在。
- Objects / Domain / Definitions：N=2k²；V为中心集合；c_V=c_z=k、c_G=c_R=1；(4)由正文§6精确定义。非中心机器均可加入U，不改变结论。
- Assumptions / Scope：仍是指定两值族，非一般P结构定理。不同(U,v,C)独立选见证，无共同全局概率/多机边际一致性；不主张一般(4)可多项式求解，也不是条件LST/configuration或SA障碍。
- Conclusion：同时对除2k个中心以外的全部机器检查真实负载，仍可通过每个单独配置pin；再多要求一个中心则有明确失败查询。任意固定r的独立真实行/单配置见证仍不能单凭该合同相对T统一优于2。
- Dependencies：UM-COMPACT-COUNT-ESCAPE-GAP-v1的族/基线、至多一次完整卸载、边界补位与全局X槽计数；无新增外部定理。
- Evidence：§6一般构造、尖锐计数证明、独立重构/冻结攻击；有限全配置/中心子集审计范围见multirow_count_extension_audit.json，未枚举所有k。
- Counterevidence / Objections：sharp查询z空会禁止所有Y逃逸，才迫U内中心不能接X；不能省该pin或将G+1的失败说成每个查询都失败。此前单行v1范围保持不变。
- Status：完整所述范围证明及内部独立审查；未外审，全球新颖性和独立论文价值未认证，主目标OPEN。
- Related Files：[正文§6](../current/unrelated_machines/row_count_escape_gap.md)、row_count_escape_review.md末节、multirow_count_extension.py与对应冻结结果。

## UM-MACHINE-CONFIG-PROBE-GAP-v1：全部完整单机配置的独立延伸仍有间隙2

- Exact Statement / Quantifiers：∀整数k≥2，row_count_escape_gap.md§2的同一紧凑实例P_k在T=1满足∀机器i、∀本地合法配置C∈C_i(1)，∃完整配置LP可行点y^(i,C)，y^(i,C)_(i,C)=1；OPT(P_k)=2−1/k。故正OPT且满足该(MP)合同的实例/目标对上sup OPT/T=2；本族与原GPC₂及列明过滤固定点也同时相容，不要求条件点自身满足GPC₂。
- Objects：UM-MODEL-v1；同一N=2k²块、G=N−2k全局机、Y在共享z耗1/k的多项式规模族；完整配置点含每机归一、合法配置容量和每任务精确覆盖。
- Domain：T=1，k≥2，有限处理时间{1/k,1}；m=2k³+6k²−2k+1、n=4k³+2k²；主目标的一般合法输入子族。
- Definitions：(MP)=∀i∀C∃y^(i,C)，不是一个共同base y及其条件分布。固定C要求该机C外任务边际0。
- Assumptions：不同探针可用不同完整LP点；无跨探针混合恒等式、条件pair一致或完整SA/LS条件。
- Scope：全部合法单机配置包括空、全部Z子集、G/R单任务及z任意≤k个Y；每给定C可多项式位长构造延伸，但未声称多项式枚举全部配置或通用精确LP求解。
- Conclusion：反驳基于这些独立延伸性质的统一(2−ε)T保证，包含全部边独立CONFIG强制探针；不否定相对OPT算法或UM-TARGET-v1。安全删配置迭代无第一次删除。
- Dependencies：UM-MODEL-v1、UM-COMPACT-COUNT-ESCAPE-GAP-v1的实际族/整数最优值；§7全部分类证书和有理单位槽装配；UM-ST-ROUND-v1给sup上界。GPC₂仅独立同时成立，不作为条件证书前提。
- Evidence：§7自足证明；先独立重构再冻结攻击；主实现实际核k2全部333配置、k3/4全部非z及列明z配置，独立不导入生成器复核k2全配置、k3..8代表及k2..128标量。
- Counterevidence / Objections：(MP)不是一般T整数可行的必要条件，不能因一个失败配置直接拒绝；仅可安全删除该配置。共同base的逃逸一阶矩恒等式立即导出既有条件块cut并排本族；未建立一般求解/舍入、新颖性或外审。
- Status：完整所述范围证明，实际独立内部审查与双路精确核验；未外审，未认证全球新颖性，主目标OPEN。
- Related Files：row_count_escape_gap.md§7、machine_config_probe_review.md、compact_config_probe.py、compact_config_probe_independent.py、compact_config_probe_audit.json。来源保留boss2紧凑族、boss3稀疏修复与boss1本节新延伸机制。

## UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1：真实最优凸包内的固定槽舍入近2损失

- Exact Statement / Quantifiers：∀整数m≥2，正文P_m为m台完全相同机器、n=m²任务的合法正有理输入，OPT=1；m个显式真实最优调度均匀平均得全正x_ij=1/m。由该x构造的标准有序单位槽图，对任意逐机平局次序，其每一个覆盖全部任务的匹配都输出makespan=2m/(m+1)。跨槽修复另记UM-OPTIMAL-CONVEX-SLOT-REPAIR-v1。
- Objects / Domain / Definitions：UM-MODEL-v1；一个unit任务，其余m²−1任务各为1/(m+1)，所有机器同值；标准槽图仅连接正区间交长，定义沿UM-ST-ROUND-v1。
- Assumptions / Scope：T=真实OPT=1；x甚至附显式全局最优凸分解；最终输出若被限制为这个固定图的覆盖matching才受此边界。m无界，处理时间全正，无不可用边。
- Conclusion：∀统一ε>0，选m+1>2/ε，该固定输出空间不存在≤(2−ε)OPT的调度。不是松弛值低估或某个坏匹配。
- Dependencies：UM-MODEL-v1、标准槽构造/Hall覆盖；正文显式循环最优调度、整数槽数饱和及迁移计数。
- Evidence：自足一般证明；先盲重构后冻结攻击；两路Fraction审计，实际枚举范围见冻结证据；m=1控制另核。
- Counterevidence / Objections：给出凸分量时可直接返回任一最优分量，故不排一般算法；允许换x/换槽/跨槽迁移也不被排除。行跨度m+1无界，不与两倍行跨度正面结果冲突。
- Status：完整所述范围证明及内部独立重构/冻结攻击；外审/新颖性/独立论文价值未认证；UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)、[research/reviews/unrelated_machines/optimal_convex_slot_review.md](../reviews/unrelated_machines/optimal_convex_slot_review.md)、两份代码、输入/证书及evidence/runs/unrelated_machines/optimal_convex_slot_gap_audit.json。

## UM-OPTIMAL-CONVEX-SLOT-REPAIR-v1：固定槽族的一轮最少迁移最优修复

- Exact Statement / Quantifiers：∀整数m≥2，∀上述P_m任意ties固定槽图的覆盖matching对应σ，可在扫描σ后的O(n+m)组合操作及总位多项式时间内改恰m−1个任务的机器，得到C_max=OPT=1；min_{τ:C_max(τ)=1}|{j:σ(j)≠τ(j)}|=m−1。m=1按同公式为空修复。
- Objects / Domain / Definitions：前一身份的显式identical族及所有覆盖matching调度；Hamming按最终任务机器标签变化计。
- Assumptions / Scope：允许离开原槽图；只对这个可显式求解族，不是通用repair。
- Conclusion：跨槽一轮最优修复及精确最小修改数。
- Dependencies：UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1给每机任务数；双射迁移与big留/移两分支计数。
- Evidence：正文§4自足推导；冻结增补独立攻击；Fraction修复与不导入核心的整数全枚举。
- Counterevidence / Objections：不保证一般输入的修复余量、搜索或迭代复杂度；不反驳固定槽gap，因为修复突破旧槽容量。
- Status：完整所述范围证明及内部独立攻击；外审/新颖性未认证，主目标OPEN。
- Related Files：同一正文、optimal_convex_slot_review.md、两份主审计、optimal_convex_slot_repair_independent.py及统一冻结记录。

## 循环批量修复与分流合流的准确身份

### UM-ROBUST-CYCLIC-BATCH-OPT-v1：鲁棒循环批量交换的位多项式局部优化

- Exact Statement / Quantifiers：For every fixed rational eta in (0,1), all legal P,T>0 and pruned actual schedules sigma with Cmax<=2T admit deterministic bit-polynomial coordinatewise nonincreasing optimization to a state with no machine-simple arbitrary-bundle cycle reducing every participating load by eta*T. At most floor(4m/eta) successful rounds. Variable-eta complexity is polynomial in 1/eta, not log(1/eta).
- Objects / Domain / Definitions：UM-MODEL-v1；[自足正文](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§1–7的允许边、菜单和精确族。
- Assumptions / Scope：给定实际σ，使用p≤T的边且Cmax≤2T，T>0、η固定；η变量时只声称关于1/η多项式。
- Conclusion：鲁棒循环批量交换的位多项式局部优化；主目标仍OPEN。
- Dependencies：UM-MODEL-v1; explicit-menu strict-turn SCC and repeated-machine splice; exact rounded-profit minimum-arrival subset DP; fixed positive potential decrement.
- Evidence：完整一般推导；独立先重构后冻结审查，实际Fraction/整数枚举、真实槽证书见正文§8。
- Counterevidence / Objections：No makespan approximation follows; cycle existence fails on the fork family. T=0 handled separately without a no-zero-margin-cycle conclusion.
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准工具扣除后的全球新颖性及独立成文价值未认证。
- Related Files：research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md，research/reviews/unrelated_machines/cyclic_batch_fork_review.md；规范代码、独立审计、实际输入和冻结记录沿正文§8读取。

### UM-BATCH-SUPPORT-REPAIR-NO-v1：真实最优值一调度的无界单机撤离义务

- Exact Statement / Quantifiers：For every integer k>=1 the section5 three-machine family has OPT=1, a pruned schedule of loads (2,2,2), minimum sorted-lex improvement support k+1, and minimum maximum per-machine outgoing count k. Thus neither constant support nor constant outgoing budget guarantees monotone improvement.
- Objects / Domain / Definitions：UM-MODEL-v1；[自足正文](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§1–7的允许边、菜单和精确族。
- Assumptions / Scope：整数k≥1的三机两端任务族，初始负载全2，改善指按负载非增排序的lex严格下降；k=1单独覆盖。
- Conclusion：真实最优值一调度的无界单机撤离义务；主目标仍OPEN。
- Dependencies：UM-MODEL-v1; section5 exact four-parameter classification and attaining moves.
- Evidence：完整一般推导；独立先重构后冻结审查，实际Fraction/整数枚举、真实槽证书见正文§8。
- Counterevidence / Objections：A repair-neighborhood boundary only; k1 admits a one-out exchange. No LP-output claim for this family and no approximation hardness.
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准工具扣除后的全球新颖性及独立成文价值未认证。
- Related Files：research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md，research/reviews/unrelated_machines/cyclic_batch_fork_review.md；规范代码、独立审计、实际输入和冻结记录沿正文§8读取。

### UM-FORK-MINCOST-ROUND-REPAIR-NO-v1：唯一最小成本槽分配仍须分流合流的间隙族

- Exact Statement / Quantifiers：For every integer k>=2 the sections6-7 padded fork has T=OPT=1 and explicit feasible rational assignment x; every minimum-processing-cost ordered-slot matching induces the same actual schedule sigma of makespan 2-1/k. No nontrivial makespan-nonincreasing reassignment from sigma can have at most one outgoing destination per source machine, even with arbitrary bundle size and arbitrarily many machines.
- Objects / Domain / Definitions：UM-MODEL-v1；[自足正文](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§1–7的允许边、菜单和精确族。
- Assumptions / Scope：整数k≥2，m=8k+3,n=8k+6，正文uniform-current a与padding矩阵、显式x和固定槽排序；不要求x为基本点或配置投影。
- Conclusion：唯一最小成本槽分配仍须分流合流的间隙族；主目标仍OPEN。
- Dependencies：UM-MODEL-v1; section6 fork capacity implications; section7 private padding, explicit rational x, positive slot injection and strict per-job support-cost minima.
- Evidence：完整一般推导；独立先重构后冻结审查，实际Fraction/整数枚举、真实槽证书见正文§8。
- Counterevidence / Objections：The supplied x is not claimed basic and violates configuration big-cardinality at A. Does not refute configuration-derived or specially chosen initialization, support changes, multi-destination repair or nonmonotone algorithms.
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准工具扣除后的全球新颖性及独立成文价值未认证。
- Related Files：research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md，research/reviews/unrelated_machines/cyclic_batch_fork_review.md；规范代码、独立审计、实际输入和冻结记录沿正文§8读取。

## UM-DAG-DEGREE-TOKEN-IDENTITY-v1：有向需求树的精确压缩任务恒等

- Exact Statement / Quantifiers：∀正文(D,k)：显式非空简单DAG、入度0根、二进制非负需求且k=0仅在出度0顶点，逐点q=min(k,d)任务＋必要填充＋根unit构造P，有OPT(P)=2−b*。∀实际C<2调度可位多项式解码b(H)≥2−C根树；∀给定根树可位多项式构造C≤2−b(H)调度。
- Objects / Domain / Definitions：b(H)=min({1}∪{deg_H⁺(v)/k_v：选中v且k_v>0})，b*=max根树b(H)。正需求输出叶仍受约束；k=0只允许原sink。一般DAG、不固定层深；允许正需求死端、k>d、大二进制需求和不可达点。
- Assumptions / Scope：P是一般UM输入的显式正有理子类；任务数≤1+|E|+|V|，逐项可构造；不是对所有调度实例的逆表示。
- Conclusion：真实整数OPT恒等与双向实际输出；不含松弛或SA层级传递。
- Dependencies：UM-MODEL-v1、正文DAG需求定义、unit接收容量与本地1总量恒等、根可达解码、截断剪树和大k填充。
- Evidence：自足一般证明；先独立重构后冻结攻击；两份不导入彼此的精确枚举审计，实际范围见evidence/runs/unrelated_machines/rooted_dag_token_bridge_audit.json。
- Counterevidence / Objections：需要DAG和本文需求定义；不把输出叶作免费终端，不按巨大k展开。没有已成立fatal objection；SA伪分布未保真，不能升级为调度SA间隙或困难性。
- Status：已知MMDA/Santa Claus机制的直接自足重构与位复杂度补全；完整所述范围及独立内部攻击，未外审/未认证新颖性；UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/rooted_dag_degree_token_bridge.md](../current/unrelated_machines/rooted_dag_degree_token_bridge.md)、rooted_dag_token_bridge_review.md、两份代码、输入/证书及冻结证据；原文版本见manifest。

## UM-TARGET-IMPLIES-DAG-DEGREE-v1：统一调度改善的需求树必要输出能力

- Exact Statement / Quantifiers：若UM-TARGET-v1对某统一ε>0成立，则∃一个确定性位多项式算法，∀上述(D,k)输出真实根树H且b(H)≥εb*；算法不需输入b*或ε数值，对至多1+|E|个多项式规模调度输入调用同一个A。
- Objects / Domain / Definitions：前一身份的D,k及截断目标；Γ={1}∪{h/k_v：1≤h≤min(k_v,d_v)}，正阈值τ下k'_v=ceil(τk_v)，原终端仍0。
- Assumptions / Scope：明确以目标算法存在为前提；不声称现已有该A或需求树常数算法。
- Conclusion：实际树输出、确定性与总位多项式保持；一般b*小的实例也由正确需求缩放处理。
- Dependencies：UM-TARGET-v1、UM-DAG-DEGREE-TOKEN-IDENTITY-v1、最优正比值属于有限Γ、τ=b*时scaled OPT=1以及精确评分。
- Evidence：完整阈值证明和独立冻结攻击；有限阈值/oracle核验单列。
- Counterevidence / Objections：直接对未缩放实例调用A可能C≥2，不足解码；本文逐阈值规避该缺口。不是源MMDA SA gap或计算困难性到调度的转移。
- Status：完整条件性归约证明；已知必要方向的直接重构，外审/新颖性未认证，主目标OPEN。
- Related Files：同正文§5、冻结审查、两路精确审计与原始Bamas2025定位。

### UM-COORDINATE-REPAIR-ST-GAP-v1：真最优凸包槽输出上的逐坐标修复停滞

- Exact Statement / Quantifiers：For every integer m>=2 and rational eta in (0,1), on the boss7 identical-machine family P_m with T=OPT=1 and x in the true optimal-schedule convex hull, every ordered-slot matching output sigma has Cmax=2m/(m+1), and the robust cyclic-batch optimizer returns sigma in zero rounds. More generally every coordinatewise load-nonincreasing reassignment sequence preserves every load on identical machines. All such matchings have the same minimum total processing cost.
- Objects / Domain / Definitions：boss7 UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1的m台identical正有理族；标准有序槽匹配、逐机器负载非增、固定η鲁棒循环优化器。
- Assumptions / Scope：m≥2、T=OPT=1；x附真实最优调度凸分解；所有有限时间与合法分配按原模型，反例无零值。
- Conclusion：完整初始化加逐坐标优化仍无统一低于2保证；不扩张第7节one-destination makespan非增反例的配置适用范围。
- Dependencies：UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1（boss7原族）、UM-ROBUST-CYCLIC-BATCH-OPT-v1、相同机器ΣL=Σp守恒。基本恒等式的直接推论，不是新族。
- Evidence：自足正文§9、追加冻结独立审查；m2..8实际调用，m2/3全部合法调度独立枚举。
- Counterevidence / Objections：允许低负载接收机上升即可打破本障碍；本族一件small迁移已能严格降makespan。不能误读成主目标困难性或配置来源下单目的地makespan修复也不可能。
- Status：direct corollary with complete proof; independently attacked and exactly audited; unrefereed; novelty unverified。
- Related Files：cyclic_batch_repair_and_fork_obstruction.md§9、cyclic_batch_fork_review.md追加审查、identical_work_invariant_audit.py及同名新冻结JSON；源族正文optimal_convex_fixed_slot_gap.md归属boss7。

## UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1：真实最优凸包固定边际的逐行偏差间隙

- Exact Statement / Quantifiers：∀固定实常数a,b≥1，取所有OPT(P)>0的UM-MODEL-v1输入和有理x∈conv(最优整数调度)。ell_i=Σ_{j:p_ij<∞}p_ij x_ij，s_i=max_{x_ij>0}p_ij（空0），R_ab={合法σ:∀i L_i≤a ell_i+b s_i}。R_ab总非空，且sup_{P,x} min_{σ∈R_ab} C_max(σ)/OPT(P)=2。另∀固定整数b0≥0，每机任务数≤ceil(Σx_ij)+b0的合法集也非空且sup最佳比2。
- Objects / Domain / Definitions：原一般模型、正OPT、固定给定有理x，输出允许全部有限边；a,b,b0先固定、m,n无界。零最优不以0/0进入sup。
- Assumptions / Scope：只限固定x的行负载/计数输出合同，不假设可计算凸包身份，不提供好x求解器。
- Conclusion / Mechanism：凸包性质及ST给非空2上界；私有sink显式最优平均与整数计数给下界。
- Dependencies：UM-MODEL-v1, UM-ST-ROUND-v1, UM-PRIVATE-SINK-OPT-HULL-v1；对象/机制见正文。
- Evidence：自足一般证明、先独立重构后冻结攻击、实际Fraction/整数有限审计；各范围独立记录。
- Counterevidence / Objections：本族直接可最优求解；换x/集中迁移不受排除。不是配置gap、算法困难性或主目标否定。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；未外审，Truth/Value/Novelty/Mechanism/Ambition分列正文。
- Related Files：research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md；research/reviews/unrelated_machines/optimal_hull_marginal_review.md；代码/输入/证据精确路径见正文。

## UM-OPT-HULL-PAIR-NC-GAP-v1：同汇点两两负相关的尖锐期望和尾概率

- Exact Statement / Quantifiers：∀整数k≥2,r≥k，在私有sink族的OPT1和固定最优平均x上，∀保持全部x边际的合法随机Σ，若每对同sink不同small的联合概率≤1/r²，则E C_max≥2−1/k−(k−1)/(2r)。∀ε∈(0,1)，q=ceil(εk)≥2时P(C_max≤2−ε)≤min(1,k(k−1)/(r q(q−1)))。r≥max(k,binom(k,2))时期望下界和每个q的非截断尾上界均分别精确达到。
- Objects / Domain / Definitions：同一显式族，其他B-small/跨组/高阶依赖任意；边际精确。
- Assumptions / Scope：两个最优分布分别选取，不声称同一个分布同时达到所有界；r=k²给此合同的近2期望与趋零成功概率。
- Conclusion / Mechanism：每态C=2−D_H/k，整数碰撞对计数及显式对称分布；row包络定理不是本证明前提。
- Dependencies：UM-MODEL-v1, UM-PRIVATE-SINK-OPT-HULL-v1；对象/机制见正文。
- Evidence：自足一般证明、先独立重构后冻结攻击、实际Fraction/整数有限审计；各范围独立记录。
- Counterevidence / Objections：真实最优平均的组内small为正相关，不属NC类。保持正相关、重选点/选好态和一般随机算法未被排除。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；未外审，Truth/Value/Novelty/Mechanism/Ambition分列正文。
- Related Files：research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md；research/reviews/unrelated_machines/optimal_hull_marginal_review.md；代码/输入/证据精确路径见正文。

## UM-OPT-HULL-HIGHER-NC-SUCCESS-v1：高阶负相关的精确成功概率及采样择优边界

- Exact Statement / Quantifiers：任意整数k≥2,r≥k,1≤d,q≤k，在私有sink族固定最优平均x上，全部合法随机Σ保x；每同sink的2..d件不同small全送sink概率≤r^(−s)。令t=min(d,q)，则Pr[Cmax≤2−q/k]的最大值恰1(t=1)，否则min(1,binom(k,t)/(r^(t−1)binom(q,t)))；有限有理分布达到。固定ε∈(0,1)、r=k²、q=ceil(εk)、d(k)→∞时任意固定输入位长多项式次采样择优成功趋零；自适应乘积界要求每个历史的条件law守同x及同相关性合同，无条件逐轮合同只给union bound。
- Objects / Domain / Definitions：正文§2全部原任务，OPT=1、m=2r,n=rk+1，small尺寸1/k；q为成功所需集中撤离件数，d是全送sink事件的上负相关阶数。
- Assumptions / Scope：不要求补事件负相关、组外相关性或机器件数保持；精确达到只属于此明确的较宽分布类。固定d的界不足以排任意多项式次择优。输出限采到的调度之一，不排采后重排/更改边际/直接构造好态。
- Conclusion / Mechanism：阶乘矩计数给各阶上界，r≥k使最高适用阶最强；对称的q件/单件混合law同时保全部边际并达到。高阶上负相关会压制低边际sink必须承担的集中撤离。
- Dependencies：UM-MODEL-v1, UM-PRIVATE-SINK-OPT-HULL-v1；参数族/一阶身份来自既有正文，阶乘计数为自足标准机制；不是借pair结论直接升级高阶。
- Evidence：正文§11一般证明、独立Exact先行重构及作者冻结全文读后攻击、两份不互相导入的Fraction实际分配law审计、点态count-state证书及精确反算；有限范围另冻JSON。
- Counterevidence / Objections：本族可直接最优求解；真实最优平均有强正相关。稀有采样不蕴含确定性找原子困难，也不是一般随机近似困难性。补事件NC不能偷偷加入精确达到合同。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md §11；research/reviews/unrelated_machines/private_sink_higher_order_nc_review.md；tests/audits/unrelated_machines/private_sink_higher_order_nc{,_independent}.py；evidence/runs/unrelated_machines/private_sink_higher_order_nc{,_independent}_audit.json。

## UM-FOREST-BOUNDARY-AUGMENT-v1：单边界森林批量消元的根负载支配

- Exact Statement / Quantifiers：∀给定单边界森林gadget(V,r,K)、有理T≥0和0<η≤1，存在确定性poly(总位长,1/η)算法，返回FAIL（蕴含内部≤T无解）或实际τ,b≥0，根负载b、内部负载≤(1+η)T；对每个内部≤T的原分配ρ均b≤L_r(ρ)。用单端根任务b替换，保全局T可行性正向，任意约化调度B恢复≤max(B,(1+η)T)。同T,η每次删至少一机器的≤m次嵌套消元保持同界。
- Objects / Domain / Definitions：每gadget任务≤2可用端且均在V∪{r}，平行任务允许、简单机器支撑森林；K外任务无内部端。根无局部容量上限。
- Assumptions / Scope：额外结构明确；不含寻找有用森林或一般多边界/环状核心算法。η按数值倒数计复杂度。
- Conclusion / Mechanism：真实父端标量支配＋局部floor背包，原T选集包含与每机仅父包付误差，根精确恢复；总O(n+n²/η)有理状态更新。
- Dependencies：UM-MODEL-v1, UM-FOREST-SCALAR-DP-v1；对象/机制见正文。
- Evidence：自足一般证明、先独立重构后冻结攻击、实际Fraction/整数有限审计；各范围独立记录。
- Counterevidence / Objections：成功不等于原T精确可行，根b可>T。单边界承重，多边界不能逐坐标min；已有bounded-treewidth FPTAS是背景，未认证接口新颖性。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；未外审，Truth/Value/Novelty/Mechanism/Ambition分列正文。
- Related Files：research/current/unrelated_machines/forest_boundary_contraction.md；research/reviews/unrelated_machines/forest_boundary_contraction_review.md；代码/输入/证据精确路径见正文。

## UM-KNAPSACK-MATROID-ENVELOPE-v1：原任务地集上多拟阵容量外包的精确损失

- Objects / Domain / Definitions：E={h,s1,...,sk}, capacity T=1, positive rational weights 1 and 1/k; F is the intersection of p independence families on exactly E.
- Quantifiers / Exact Statement：For all integers k,p>=1, on one weight-1 item and k weight-1/k items, the minimum over all p same-ground-set matroids whose common independent sets contain every weight<=1 subset of the maximum common-independent-set weight equals max(1,2-p/k), and is attained by partition matroids. A uniform bound 2-epsilon requires p>=ceil(epsilon*k) on this family.
- Assumptions / Scope：Only complete local outer envelopes on the original ground set and guarantees for every common independent set; does not force a global algorithm to choose a bad set or exclude auxiliary elements, projections, bases or selective profiles.
- Conclusion：Sharp local capacity-envelope tradeoff, with a hitting-set identity for every admissible matroid tuple.
- Dependencies：UM-MODEL-v1; self-contained elementary classification/counting and sharp constructions in the account.
- Evidence：Complete stated-scope proof; independent statement-first reconstruction then frozen attack; exact finite audit at the scope in the new record.
- Counterevidence / Objections：No remaining fatal objection at the frozen version. Only complete local outer envelopes on the original ground set and guarantees for every common independent set; does not force a global algorithm to choose a bad set or exclude auxiliary elements, projections, bases or selective profiles.
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified; known-tool direct extension, not a new approximation algorithm or certified independent publication result.
- Related Files：[minimal_star_contraction_and_capacity_gap.md](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md), research/reviews/unrelated_machines/minimal_star_capacity_review.md, tests/audits/unrelated_machines/knapsack_matroid_envelope_independent.py, evidence/runs/unrelated_machines/knapsack_matroid_envelope_audit.json.

## UM-MIN-WORK-FACE-SUPPORT-GAP-v1：最小总处理量整个最优面的支撑损失

- Objects / Domain / Definitions：m>=2, B costs m everywhere; m-1 small jobs per home cost 1 at home and 1+1/m elsewhere; assignment LP with cutoff T and objective W=sum p*x.
- Quantifiers / Exact Statement：For every m>=2 the positive finite m-machine home-penalty family has OPT=m+1/m and T_LST=m. At T=OPT every minimum-total-processing-time assignment-LP point has the same support and every supported integer assignment has makespan 2m-1; the face contains an explicit vertex of the original LP. Exact nonincreasing total-work schedules have the same bad value. With integer q>=0 small off-home moves allowed, the exact optimum is max(2m-1-min(q,m-1),m+1/m).
- Assumptions / Scope：The family is not the true-optimal-convex-hull contract and no configuration-LP face is asserted. Changing objective/support or allowing positive total-work increase is unrestricted; no fixed relative cost-relaxation obstruction or general scheduling hardness.
- Conclusion：Near-2 support loss despite OPT/T_LST tending to 1; explicit basic witness and exact work-versus-makespan repair staircase.
- Dependencies：UM-MODEL-v1, UM-ST-ROUND-v1; self-contained elementary classification/counting and sharp constructions in the account.
- Evidence：Complete stated-scope proof; independent statement-first reconstruction then frozen attack; exact finite audit at the scope in the new record.
- Counterevidence / Objections：No remaining fatal objection at the frozen version. The family is not the true-optimal-convex-hull contract and no configuration-LP face is asserted. Changing objective/support or allowing positive total-work increase is unrestricted; no fixed relative cost-relaxation obstruction or general scheduling hardness.
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified; known-tool direct extension, not a new approximation algorithm or certified independent publication result.
- Related Files：[optimal_convex_fixed_slot_gap.md](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md), research/reviews/unrelated_machines/optimal_convex_slot_review.md, tests/audits/unrelated_machines/minimum_work_face_audit.py, tests/audits/unrelated_machines/minimum_work_face_independent.py, evidence/runs/unrelated_machines/minimum_work_face_audit.json.

## UM-FROZEN-MACRO-TINY-REOPT-GAP-v1：冻结宏任务后的全部微任务重开间隙

- Exact Statement / Quantifiers：∀整数r≥1，k=r(r+1)，存在所述受限指派P_r、r²个真实最优调度平均点x及真实ST槽输出σ，OPT=1、Cmax(σ)=2−1/r；固定全部宏任务位置后，允许全部微任务任意使用其所有有限边联合重优化，精确最优为2r/(r+1)。∀固定δ,ε∈(0,1)，可选r使微任务1/k≤δ且该值>(2−ε)OPT。
- Objects / Domain / Definitions：2r台机器H/Q/Z，r个unit宏任务，rk个大小1/k的私有home/共同Z微任务；r=1包含。
- Assumptions / Scope：宏任务最终机器保持σ；微任务可任意迁移、任意联合求解、可离开槽图。不要求x基本，不声称所有槽匹配坏。
- Conclusion：冻结宏任务后的全部微任务重开间隙；不改变UM-TARGET-v1身份。
- Dependencies：UM-MODEL-v1, UM-SHARED-SINK-MACRO-FAMILY-v1；完整定义/推导见正文新增节。
- Evidence：完整显式凸分解、正交长槽注入、工作守恒及每组外送2r件达到。先独立重构再冻结攻击；实际有限范围见审查和运行记录。
- Counterevidence / Objections：只排固定宏任务的后处理合同；重选宏任务或换x/匹配、一般算法均不受排除。当前声明范围无尚成立fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：[research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md](../current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)、`research/reviews/unrelated_machines/frozen_macro_tiny_review.md`；代码/冻结记录由正文新增节链接。

## UM-MACRO-MIGRATION-FRONTIER-v1：共同汇点族的尖锐宏任务迁移前沿

- Exact Statement / Quantifiers：∀整数r≥1、0≤d≤r−1，k=r(r+1)、s=r−d，从指定σ改至多d个宏任务最终机器、微任务全自由时，精确最优F_r(d)=ceil(2sk/(s+1))/k。∀实α∈[1,2)，M=floor(kα)，达到Cmax≤α的最少宏任务改数恰max(0,r−floor(M/(2k−M)))。允许≥r−1次改动时OPT=1。
- Objects / Domain / Definitions：同一共享Z族、指定σ及按最终机器标签计数的宏任务Hamming预算。
- Assumptions / Scope：原微任务所有有限边均可用，临时步骤不受限制；实α仅数学恒等，计算接口只用有理α。
- Conclusion：共同汇点族的尖锐宏任务迁移前沿；不改变UM-TARGET-v1身份。
- Dependencies：UM-MODEL-v1, UM-SHARED-SINK-MACRO-FAMILY-v1；完整定义/推导见正文新增节。
- Evidence：整数负载格点、s(2k−M)≤M及移动d个宏任务到不同Q的达到构造。先独立重构再冻结攻击；实际有限范围见审查和运行记录。
- Counterevidence / Objections：固定改善必改r−O(1/ε)个宏任务，但不排一次改变线性数量宏任务的位多项式算法。当前声明范围无尚成立fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：[research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md](../current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)、`research/reviews/unrelated_machines/frozen_macro_tiny_review.md`；代码/冻结记录由正文新增节链接。

## UM-DEPTH-TWO-HALF-v1：两层异质需求的半比例树及实际调度

- Exact Statement / Quantifiers：∀显式层状简单DAG D:{r}→U→W，r/U需求为正二进制整数、W需求0，存在确定性总位多项式算法输出真实根树H，b(H)≥b*/2；对原token/filler桥梁P(D,k)，实际输出调度Cmax≤2−b*/2≤3OPT/2。根为零需求终端的情形由原桥梁精确处理。
- Objects / Domain / Definitions：原需求截断评分b、共享终端、任意异质大需求、不可达U、死端和空层。
- Assumptions / Scope：只限深度二的桥梁输入族，U—W可任意共享且无宽度限制。阈值枚举只按显式出度，不求NP难完整星包装。
- Conclusion：两层异质需求的半比例树及实际调度；不改变UM-TARGET-v1身份。
- Dependencies：UM-MODEL-v1, UM-DAG-DEGREE-TOKEN-IDENTITY-v1, UM-DEPTH-TWO-STAR-PACKING-v1；完整定义/推导见正文新增节。
- Evidence：最小半配额贪心、首次失效私有叶收费、Γ含b*、真实树→调度及总位复杂度。先独立重构再冻结攻击；实际有限范围见审查和运行记录。
- Counterevidence / Objections：标准贪心收费的局部构造；深层资源共享和一般R||Cmax均未解决，新颖性未认证。当前声明范围无尚成立fatal objection。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：[research/current/unrelated_machines/rooted_dag_degree_token_bridge.md](../current/unrelated_machines/rooted_dag_degree_token_bridge.md)、`research/reviews/unrelated_machines/depth_two_quota_review.md`；代码/冻结记录由正文新增节链接。

## UM-FOREST-TWO-BOUNDARY-MENU-v1：双边界森林的一端精确与另一端乘性保零菜单

- Exact Statement / Quantifiers：∀给定双边界a≠b的森林任务gadget、二进制有理T≥0及0<η≤1，存在确定性poly(总位长,1/η)算法输出多项式大小的实际分配菜单；每项内部及b负载≤(1+η)T。∀原分配ρ，若内部≤T且L_b(ρ)≤T（a不限容），则∃同一菜单项τ使L_a(τ)≤L_a(ρ)、L_b(τ)≤(1+η)L_b(ρ)，因此严格保b=0。
- Objects / Domain / Definitions：每任务一/两有限端、允许任意平行bundle及私人任务，合并平行边的机器图为森林；内部与外部任务隔离，两个边界可有外部任务。菜单项携原任务身份及两端真实负载。
- Assumptions / Scope：给定结构的可恢复接口；同批任务/内部不交挂件可共享存活边界，前向乘性贡献求和不按件数累计，选好项后逆恢复max(B,(1+η)T)。不包括结构寻找、普通job替换、一般核心共同选择或免费串行嵌套。
- Conclusion / Mechanism：b几何预算加独立零预算，内部和b异质逐项ceil，a保真实精确目标；每预算森林标量DP精确优化，G=O(1+位长/η)、K=O(N/η)，显式backpointer恢复。
- Dependencies：UM-MODEL-v1, UM-FOREST-TWO-BOUNDARY-GRID-v1；算法对象及所有共同前提见正文。
- Evidence：完整自足证明、先盲重构后冻结攻击；规范500例及每候选完整枚举；独立458例/1211份强域调度，411份a>T、589份b0，深树/大分母/共享边界及错误拒绝检查；仅所列有限范围。
- Counterevidence / Objections：T=0必须允许a接正时间；已修复并独立重跑。非空菜单不判定原T可行。已有结构FPTAS与近似Pareto机制是背景；不认证新颖性。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；主目标UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/forest_boundary_contraction.md](../current/unrelated_machines/forest_boundary_contraction.md)、research/reviews/unrelated_machines/forest_boundary_contraction_review.md及正文链接的代码/冻结记录。

## UM-ONE-DESTINATION-SLOT-REPAIR-v1：同机槽族的单目的地最小迁移与逐批严格下降

- Exact Statement / Quantifiers：∀m≥2及UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1的任一槽输出σ，若每原来源机器全部迁出原任务至多去一个外部目的地，则达到OPT1的最小Hamming为m(m−1)/2；强制big搬走时最小为m(m+1)/2。big不动的达到构造可按路径逐批执行，第t批后C_t=(2m−t)/(m+1)，每整批严格降1/(m+1)，t=1,…,m−1。
- Objects / Domain / Definitions：已有同机族：一个unit、m²−1条1/(m+1)的small；原σ每机m任务。Hamming比较原σ与最终分配，单目的地按原初owner计，不允许以中转偷换一次迁移。
- Assumptions / Scope：仅此显式族的正面修复与精确修改数；接收机可增载。原不限制目的地的m−1最优迁移Claim不改变。没有一般配置初始化的首次进展或统一近似结论。
- Conclusion / Mechanism：原任务批量路径达到；功能图首次访问前缀的唯一外向边与净供需给三角下界；big搬走时A为净需求2无外迁汇，路径强制m,…,2并加big一次。
- Dependencies：UM-MODEL-v1, UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1；算法对象及所有共同前提见正文。
- Evidence：完整自足证明、先盲重构后冻结攻击；原任务全枚举m2/3，聚合整数流m2..5；独立身份枚举m2/3及m2..40共780个整批的完整Fraction负载。一般下界另由自足证明。
- Counterevidence / Objections：big不动的所有修复不必是路径或等距离：m3有支持7带尾循环，已记录并改用前缀割下界。只保证每整批严格下降，不保证逐任务严格下降；新颖性未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；主目标UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md](../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)、research/reviews/unrelated_machines/optimal_convex_slot_review.md及正文链接的代码/冻结记录。


## UM-STAR-CONFIG-TRANSFER-v1：外部互斥极小星的配置保持与条件边前向转换

- Objects / Domain：UM-MODEL-v1；剪枝后当前矩阵、有理T≥0、机器v的全部邻任务F满足极小超载条件，替代e按外机min定义。给定显式有理配置点或逐边证书族。
- Exact Statement / Quantifiers：对任意上述单步，约化T配置点均可逆转为原T配置点；原点y若Q_F(y)=Σ外机含F配置质量≥1，则可正向转换。特别当任意外机i、不同a,b∈F均p_ia+p_ib>T时，配置可行性双向保持，原全部有限边各有独立强制配置点⇒约化全部边也如此。对每一步都满足该条件的≤m步链，结论迭代成立。
- Definitions：不可用条目为∞；Q为配置占用概率质量，不是任务边际之和；单边强制x_ij=1，彼此不要求共同base。新e强制查询优先指定机器选mass1。
- Assumptions / Scope：全邻域极小星、同一T、每步当前互斥；前向单点只需Q≥1。运行时间相对矩阵、T与给定点/证书族总位长多项式，不提供寻找配置点或一般LP oracle。
- Conclusion：真实完整配置证书转换。前向支持S'≤S−S_v+1、r步≤S+r；初始权的公共分母格不增长。逆向单步新增v支持≤|F|。
- Dependencies：UM-MODEL-v1、UM-MINIMAL-STAR-CONTRACTION-v1、配置覆盖/归一、正文§8显式贪心和补集恢复；不是由整数等价自动推出。
- Evidence：先独立重构后冻结攻击，双路Fraction全边转移；有理/零/空、指定机器优先负控制、缺互斥与反向probe反例。
- Counterevidence / Objections：无外部占用条件时两根两叶小例使原CONFIG可行而约化不可行；即使互斥，反向全部单边探针保持也不成立。不得扩大为任意星或双向probe。声明范围无尚成立fatal。
- Status：完整限范围证明、独立内部审查与精确有限核验；外审/全球新颖性未认证，主目标OPEN。
- Related Files：research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md §8；research/reviews/unrelated_machines/star_configuration_transfer_review.md；tests/audits/unrelated_machines/star_configuration_transfer.py及独立程序；evidence/runs/unrelated_machines/star_configuration_transfer_audit.json。

## UM-CONTRACTED-SPARSE-CONFIG-GAP-v1：穷尽端点星收缩后的三选全边条件配置间隙

- Objects / Domain / Definitions：UM-SPARSE-CONDITIONED-CONFIG-GAP-v1的全部k≥3、合法H与γ实例P_k，T=1+1/k；按固定底簇顺序分别收缩左右路径端点，得P'_k。各端点全邻域两unit，外部域不交。
- Exact Statement / Quantifiers：对每个上述参数，P'_k每任务至多三条有限边、时间仅{1/k,1,γ}，无极小超载星；OPT(P'_k)=2−1/k。在T下每一有限边分别有完整强制配置点，故先按指定合法次序穷尽星消元、再迭代独立单边CONFIG删边仍接受；以P'_k直接启动也无两规则起点。正目标该接受合同的sup OPT/T恰2。
- Assumptions / Scope：证明一条明确合法穷尽次序，不声称所有消元序列相同；各探针独立，无共同base、条件混合或完整bag联合一致性。未声称通用CONFIG oracle多项式。
- Conclusion：补足旧稀疏v1留下的星预处理组合范围；不改变旧命题身份，不否定UM-TARGET-v1。
- Dependencies：UM-MODEL-v1、UM-SPARSE-CONDITIONED-CONFIG-GAP-v1、UM-STAR-CONFIG-TRANSFER-v1、UM-MINIMAL-STAR-CONTRACTION-v1；sup上界另用UM-ST-ROUND-v1。
- Evidence：自足一般证明、独立冻结攻击；k3,H5旧729机1051任务经324收缩得405机727任务1778有限边，双路全部最终边完整CONFIG核验。主程序另核整数上界压缩/完整逆恢复，旧证据未改写。
- Counterevidence / Objections：下界用恢复，θ上界另在θ<2下正向压缩，不能混同方向。更多规则、共同条件相关性或一般联合舍入未排；无尚成立fatal。
- Status：完整限合同证明与独立内部审查，有限计算非一般证明；外审/新颖性未认证，主目标OPEN。
- Related Files：research/current/unrelated_machines/sparse_conditioned_configuration_gap.md末节；同新审查/双路代码/冻结记录；examples/unrelated_machines/contracted_sparse_configuration_input.json和evidence/certificates/unrelated_machines/contracted_sparse_configuration_witness.json。

## UM-SHARED-SINK-JOINT-MACRO-v1：单共享汇点的宏任务共同匹配与整组撤离

- Exact Statement / Quantifiers：∀给定H∪{z}、仅homes可用且每有限边>T/2的宏任务、各任务仅在唯一指定home与公共z的非空子集可用的私有组、二进制有理T≥0及0<η≤1，有确定性poly(总位长,1/η)算法返回FAIL或实际调度，所有home≤T、z≤(1+η)T；OPT≤T时必成功，故FAIL蕴含OPT>T。私有任务无需尺寸上界，宏任务图任意。
- Objects / Domain / Definitions：UM-SHARED-SINK-MODEL-v1；非负有理/∞、显式分组、home数与宏任务数均可增长；仅一个sink。空组、强制端、T0和大分母包含。
- Assumptions / Scope：仅单共享sink与唯一home的给定结构，宏任务每有限边严格>T/2承重；成功不判定T精确可行，不含一般多sink/多home转换或统一ε。标准覆盖背包+匹配的组合接口，未认证新颖性。
- Conclusion / Mechanism：每个macro/home或empty模式的真实最小整组撤离成本，保零乘性覆盖DP与带dummy成本的全局最小权完美匹配；误差只对同一个真实sink预算求和，不按home数量累积。
- Dependencies：UM-MODEL-v1、UM-SHARED-SINK-MODEL-v1；正文自足的覆盖缩放与有理最小成本二分图匹配。不调用最优调度/分布或配置oracle。
- Evidence：规范Fraction覆盖子集/匹配排列/原任务分配oracle；独立全局N绝对预算floor-DP与独立实际分配枚举；实际范围、代码hash和修复见冻结审查/记录。有限核验不是一般证明。
- Counterevidence / Objections：独立审查发现的Python float/bool输入歧义已统一拒绝并重跑；宏边放宽至等号会错拒两半任务，不作此推广；多预算匹配不自动积分。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；一般UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/shared_sink_joint_macro_assignment.md](../current/unrelated_machines/shared_sink_joint_macro_assignment.md)、research/reviews/unrelated_machines/shared_sink_joint_review.md；实现/冻结记录见正文§7。

## UM-SYMMETRIC-JOB-AGGREGATION-v1：对称条件矩的任务选择聚合接口

- Exact Statement / Quantifiers：For every nonempty bounded one-hot rational P, every symmetric normalized certificate (x,Y), every given deterministic jobwise aggregation/deletion R, and every new one-hot rational polytope P′, if RY_:e belongs to x_e P′ for every old choice of every retained job, then (Rx,RYRᵀ) belongs to the same-layer pair certificate set of P′. At least one retained job is required for this sufficient criterion; no retained jobs instead require checking the zero-dimensional base. Given data and explicit P′ are checkable in bit-polynomial time.
- Objects / Domain：任意有限任务选择集、同任务选择单纯形上的有界有理多面体P、证书对(x,Y)、旧choice到同一保留任务新choice的确定映射；允许整任务删除，不允许跨任务聚合。
- Assumptions / Definitions：对称、diag=x、每个真/假齐次列；0P={0}；新系统显式有理表示。不是只给每个旧literal各自条件点的非对称N₀。
- Scope / Conclusion：正文式(3)给准确真/补列检查等价式；式(4)是更强的充分条件。只核给定R，不提供寻找R算法，也不保证旧可行性自动带来新列可行性。
- Dependencies：原始LS对称列定义、同任务互斥、对称整块求和、凸锥求和。完整证明见正文§1–2；无近似算法前提。
- Evidence：两名内部研究者先盲重构后核冻结正文；调度专用实例的Fraction实际聚合另在双路程序检查。有限证据不替代代数证明。
- Counterevidence / Objections：非对称系统不能默用整块恒等式；额外分支专用约束须实际放进P′检查。单机均匀族说明新列容量并不免费成立。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准凸锥代数接口，不称新算法。
- Related Files：research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md§1–2；research/reviews/unrelated_machines/symmetric_moment_reset_review.md；专用程序/证据从正文§8进入。

## UM-SINGLE-MACHINE-MOMENT-RESET-THRESHOLD-v1：单机既定矩推前的2T阈值与同边际T修复

- Exact Statement / Quantifiers：For each q>=2, m=2q,n=2q^2 identical jobs p=1/q,T=OPT=1, the uniform balanced true-optimum moment matrix needs exactly 2q absorbed jobs for some deterministic single-machine fallback pushforward to satisfy residual true/false capacities. Every c<2q and every fallback fail. At c=q balanced groups, the same first moment Rx has a rebuilt true residual T-distribution, in deterministic bit-polynomial time.
- Objects / Domain：§1明确的有界有理onehot多面体P、对称证书对(x,Y)、给定任务选择聚合R；阈值族q≥2、m=2q、n=2q²、p=1/q、T=OPT=1。
- Assumptions / Definitions：证书包含对称、diag=x、每个真/假齐次列；负结论固定旧真实均匀最优分布，只重定向旧删机choices，其他choices不变。包固定不是对旧分布条件化。
- Scope / Conclusion：聚合只给可检查充分条件，不寻找R；阈值精确限制既定RYRᵀ。c=q时相同Rx能重建真实残余T矩，不可写Rx∉N(P′)。
- Dependencies：UM-MODEL-v1；原始LS定义；onehot互斥/对称块求和、均匀二点概率与Hall计数。一般证明见正文§2–6，复杂度§7。
- Evidence：冻结独立审查、两路Fraction核验；q2原2520调度枚举及同base真实匹配分解。有限运行不替代全称证明。
- Counterevidence / Objections：q=1必须排除阈值下界；允许重新求矩/改其他机器choices未被排除；同一个Rx有正面修复，无层级gap、无一般算法困难性。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；部分实现仅限显式族；主目标OPEN。
- Related Files：research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md；research/reviews/unrelated_machines/symmetric_moment_reset_review.md；两份symmetric_reset审计、examples/unrelated_machines/symmetric_reset_q2.json、evidence/certificates/unrelated_machines/symmetric_reset_q2_recoupling.json、evidence/runs/unrelated_machines/symmetric_moment_reset_audit.json。

## UM-DAG-CONGESTION-FLOW-v1：共同拥塞证书的根树提取与固定支撑最小拥塞

- Exact Statement / Quantifiers：∀显式根简单DAG及二进制非负需求（零需求仅原终端），∀整数K≥1及含根支撑W上的正文共同K证书，可确定性总位多项式用一次整数流输出真实根树b≥1/(2K−1)。固定W,K的证书可行性与一整数流饱和等价；可行性对K单调，可位多项式求最小可行K或报告该W无证书。∀K≥2存在本合同证书族且真实b*=1/(2K−1)。全支撑最优κ*在b*>0时满足(1+1/b*)/2≤κ*≤ceil(1/b*)；给评分β>0的实际树及K≥1/β可构造其支撑证书。
- Objects / Definitions：D,k,r；b为选中原正需求点的截断最小出度比例。B:k≥K，L:0<k<K，Z:k=0；同一有理流f在非根I≤K、B上O≥k、非根L上O=I、低根O≥K，Z无输出。
- Domain / Assumptions：显式有限简单DAG；根原入度0；非负整数需求二进制；零需求点原出度0；评分定义与UM-DAG-DEGREE-MODEL-v1一致。
- Scope / Conclusion：W、K明确输入，允许不可达组件、正需求死点、任意根、极大二进制需求；K为整数。输出可用E[W]的零f边。给定W的不可行不意味着无好树。没有一般支撑搜索、统一常数K或一般调度算法。
- Dependencies：UM-DAG-DEGREE-MODEL-v1, UM-DAG-CONGESTION-CERTIFICATE-v1；正文逐节自证所需整数流、路径与容量性质。
- Evidence：自足路径截取、拆点整数增广、比例反算、最短增广位复杂度、K单调拓扑构造、锐层宽及树到证书证明；独立先重构后冻结攻击，有限原边流/根树oracle与大整数核验。
- Counterevidence / Objections：声明范围内未见尚成立fatal objection；一般W选择及从任意UM输入得到相应结构仍未解决。固定支撑最小K不等于全支撑κ*。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准工具应用，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/rooted_dag_congestion_flow.md](../current/unrelated_machines/rooted_dag_congestion_flow.md)、research/reviews/unrelated_machines/rooted_dag_congestion_review.md；tests/audits/unrelated_machines/rooted_dag_congestion_flow.py、tests/audits/unrelated_machines/rooted_dag_congestion_independent.py、evidence/runs/unrelated_machines/rooted_dag_congestion_audit.json、examples/unrelated_machines/rooted_dag_congestion_cases.json、evidence/certificates/unrelated_machines/rooted_dag_congestion_cases.json。

## UM-DAG-ACTIVATION-CORRIDOR-GAP-v1：父激活上界LP在单位需求汇流走廊的失效

- Exact Statement / Quantifiers：∀整数q≥2，正文四段DAG有1+q(q+3)点、2q²+2q边，根/走廊需求1、q个分叉点需求q、末端需求0。加强激活LP a_r=1、非根a_v=Σ_u x_uv≤1、Σ_w x_vw≥k_va_v、0≤x_vw≤a_v精确有理可行，但真实根树最优b*=1/q。
- Objects / Definitions：r→v_i→w_ij→x_i→t_i的显式根DAG；同一i内q条需求1走廊共享x_i。
- Domain / Assumptions：显式有限简单DAG；根原入度0；非负整数需求二进制；零需求点原出度0；评分定义与UM-DAG-DEGREE-MODEL-v1一致。
- Scope / Conclusion：仅上述激活边际LP的统一正常数充分性反例；未满足或否定共同K强证书，未导入SA或调度困难性，未认证全球新颖性。
- Dependencies：UM-DAG-DEGREE-MODEL-v1；正文逐节自证所需整数流、路径与容量性质。
- Evidence：逐变量有理赋值、选中w须继续至同一x的入度唯一性上界、实际达到路径；独立Fraction逐约束及小根树枚举。
- Counterevidence / Objections：声明范围内未见尚成立fatal objection；一般W选择及从任意UM输入得到相应结构仍未解决。固定支撑最小K不等于全支撑κ*。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准工具应用，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/rooted_dag_congestion_flow.md](../current/unrelated_machines/rooted_dag_congestion_flow.md)、research/reviews/unrelated_machines/rooted_dag_congestion_review.md；tests/audits/unrelated_machines/rooted_dag_congestion_flow.py、tests/audits/unrelated_machines/rooted_dag_congestion_independent.py、evidence/runs/unrelated_machines/rooted_dag_congestion_audit.json、examples/unrelated_machines/rooted_dag_congestion_cases.json、evidence/certificates/unrelated_machines/rooted_dag_congestion_cases.json。

## UM-INDEPENDENT-UNIFORM-MOMENT-RESET-v1：独立均匀后备的条件矩运输只需q加二任务

- Exact Statement / Quantifiers：For every q>=2 with m=2q,n=2q^2,p=1/q, the fixed uniform balanced optimal-distribution matrix under independent uniform rerouting of old deleted-machine choices satisfies residual P0(1) true/false capacities iff absorbed integer job count c>=q+2. Other old choices stay fixed; no conditioning on absorbed labels. Exact moments are deterministically bit-polynomial computable; transported states may still have load2. q=1 separately has threshold1.
- Objects / Domain：正文§3的q≥2均匀族、真实最优均匀D、任意标签包C和机器i，独立均匀后备随机量；0≤c≤n。q1单列。
- Assumptions / Definitions：不是对D条件化；每个保留任务旧非i选择保持，旧i选择独立均匀去其余K=2q−1台。新矩按真实随机实验，不能只用平均R的RYRᵀ，须修同任务块。
- Scope / Conclusion：最小c=q+2、吸收负载1+2/q，q≥3严格优于固定后备2T，q2相等；输出精确有理矩为确定性位多项式，不是随机或确定性近似调度输出。
- Dependencies：UM-MODEL-v1；§3均匀二点矩；全概率与onehot混合。完整证明§9.1–9.3，位复杂度沿§7显式输入规模。
- Evidence：两名内部研究者先盲推后核冻结稿；两路Fraction；q2全部2520源态及所有独立路由分支，q1空/退化，q2..64所有c及主q2..128范围独立登记。
- Counterevidence / Objections：m=2q不可省；一般m时q2,m8需c5即2.5T。转换分布的坏态仍可达2T；未证明一般重置、相同边际修复或主目标近似算法。当前无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准二点概率计算扩展，新颖性和独立论文价值未认证。
- Related Files：research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md§9；research/reviews/unrelated_machines/symmetric_moment_reset_review.md追加审查；tests/audits/unrelated_machines/uniform_random_moment_reset.py、tests/audits/unrelated_machines/uniform_random_reset_independent.py、evidence/runs/unrelated_machines/uniform_random_moment_reset_audit.json。

## 跨路线补充审查与身份保持

[共同容量路线整合审查](../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)补核UM-FOREST-TWO-BOUNDARY-MENU-v1、UM-DEPTH-TWO-HALF-v1、UM-FROZEN-MACRO-TINY-REOPT-GAP-v1、UM-MACRO-MIGRATION-FRONTIER-v1及UM-ONE-DESTINATION-SLOT-REPAIR-v1的所列范围。没有改变这些身份或主目标状态；标准流/仿射恢复推导用于检验接口，不另冒充新的特殊类研究成果。后续共同矩正文与研讨候选的实际覆盖另在审查中注明。

## UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1：占位模式基扩展的侧约束低维支撑

- Exact Statement / Quantifiers：∀有宏全覆盖匹配的有限宏/home二分图、每home有限非空带0/1占位标签的模式库、整数K≥0，P={每home模式和1、占位边际属于宏可匹配home基凸包}加任意K个线性侧不等式后，每个模式投影顶点至多2K个home有多于一个正模式。正支持内可用整数下界匹配和实际模式恢复，仅改变这些home；不承诺侧预算保持。
- Objects / Domain / Definitions：有限宏/home二分图、每home有限非空0/1占位模式库、可匹配全部宏任务的home基凸包，以及任意K个线性侧不等式。没有任务处理时间或T/OPT的额外假设；实际调度是后两身份的应用。
- Assumptions / Scope：K可随输入增长；一般结论只给2K支撑界。模式只依占位bit，不能依具体macro身份/残余容量；所有额外耦合约束须计入侧约束rank。
- Conclusion / Mechanism：模式积分凸包、双匹配同时交换给基面维数下界、正支持纤维维数与K个侧约束rank给R≤2K；支持内下界匹配只改这些home，资源增量由应用另行支付。
- Dependencies：UM-OCCUPATION-PATTERN-MODEL-v1；正文§4–9a自足重构交换/维数/恢复与总位复杂度。
- Evidence：先盲重构后冻结攻击；规范26小多面体/58顶点/88支持恢复，独立304宏匹配表示/20760暴露面。后两调度身份的DP、零目标和二分核验不是本抽象引理的额外前提；有限检查不替代一般证明。
- Counterevidence / Objections：不能以扩展LP basic vertex代替模式投影顶点；已用逐坐标lex精确LP避免。多预算matching边模式不满足占位基结构；无一般K/多home提取。声明范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；通用LP软件未实现，外审/新颖性未认证，主目标仍OPEN。
- Related Files：[research/current/unrelated_machines/fixed_sink_occupation_rounding.md](../current/unrelated_machines/fixed_sink_occupation_rounding.md)、research/reviews/unrelated_machines/fixed_sink_occupation_review.md；代码/冻结记录见正文§11。

## UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1：固定数量共享汇点的三半阈值构造

- Exact Statement / Quantifiers：∀固定整数K≥1，∃确定性A_K，∀给定H∪Z(|Z|=K)、仅H可用且每有限边>T/2的宏任务B、不交私有组J_h（每件仅{h}∪Z的非空子集可用）、二进制有理T≥0，A_K按输入总位长多项式返回可靠FAIL或实际调度Cmax≤3T/2；OPT≤T必成功。私有尺寸任意，有限p>T先剪枝。多项式次数依K。
- Objects / Domain / Definitions：UM-OCCUPATION-PATTERN-MODEL-v1；阈值版本与OPT promise版本分开。非负有理/∞，显式有限矩阵、零目标、空任务和强制端包含。
- Assumptions / Scope：给定T的one-sided资源增广；成功不判定T精确可行。固定K与唯一home分组承重，不提供一般实例分区/分组提取，不含K增长的统一多项式保证。
- Conclusion / Mechanism：真实home负载的多维sink上取整DP；宏任务仅保占位基；至多10K²个大贡献home分支固定后，模式投影极点至多2K个非积分home，正支持内实际宏匹配恢复；γ1/4与β1/(8K)同时付清全部sink预算。
- Dependencies：UM-MODEL-v1, UM-OCCUPATION-PATTERN-MODEL-v1, UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1；正文§4–9a自足重构交换/维数/恢复与总位复杂度。
- Evidence：先盲重构后冻结攻击；112局部菜单与997分配、4454零目标矩阵与33910分配、26小多面体/58顶点/88支持舍入/12实际恢复；独立304宏匹配表示/20760暴露面，仅有限核心范围。另16380个非单调接受表与1024宏网格合同核二分。未实现通用多项式LP/全部heavy生产调度器。
- Counterevidence / Objections：不能以扩展LP basic vertex代替模式投影顶点；已用逐坐标lex精确LP避免。多预算matching边模式不满足占位基结构；无一般K/多home提取。声明范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；通用LP软件未实现，外审/新颖性未认证，主目标仍OPEN。
- Related Files：[research/current/unrelated_machines/fixed_sink_occupation_rounding.md](../current/unrelated_machines/fixed_sink_occupation_rounding.md)、research/reviews/unrelated_machines/fixed_sink_occupation_review.md；代码/冻结记录见正文§11。

## UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1：固定数量共享汇点的大宏任务promise三半近似

- Exact Statement / Quantifiers：∀固定整数K≥1，∃确定性位多项式算法，∀同给定H/Z/B/私有组但无T的合法实例，若每条有限宏任务时间严格>OPT(P)/2（B可空），则输出实际调度Cmax≤3OPT(P)/2。零最优值精确零输出；算法不验证含OPT的promise，不要求给OPT或好调度。次数依K。
- Objects / Domain / Definitions：UM-OCCUPATION-PATTERN-MODEL-v1；阈值版本与OPT promise版本分开。非负有理/∞，显式有限矩阵、零目标、空任务和强制端包含。
- Assumptions / Scope：含OPT的大宏任务promise与结构分区为额外假设；不是一般UM-TARGET-v1。通过共同分母整数网格及可靠FAIL/任意成功负载界二分，不假定接受集合单调。
- Conclusion / Mechanism：真实home负载的多维sink上取整DP；宏任务仅保占位基；至多10K²个大贡献home分支固定后，模式投影极点至多2K个非积分home，正支持内实际宏匹配恢复；γ1/4与β1/(8K)同时付清全部sink预算。
- Dependencies：UM-MODEL-v1, UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1；正文§4–9a自足重构交换/维数/恢复与总位复杂度。
- Evidence：先盲重构后冻结攻击；112局部菜单与997分配、4454零目标矩阵与33910分配、26小多面体/58顶点/88支持舍入/12实际恢复；独立304宏匹配表示/20760暴露面，仅有限核心范围。另16380个非单调接受表与1024宏网格合同核二分。未实现通用多项式LP/全部heavy生产调度器。
- Counterevidence / Objections：不能以扩展LP basic vertex代替模式投影顶点；已用逐坐标lex精确LP避免。多预算matching边模式不满足占位基结构；无一般K/多home提取。声明范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；通用LP软件未实现，外审/新颖性未认证，主目标仍OPEN。
- Related Files：[research/current/unrelated_machines/fixed_sink_occupation_rounding.md](../current/unrelated_machines/fixed_sink_occupation_rounding.md)、research/reviews/unrelated_machines/fixed_sink_occupation_review.md；代码/冻结记录见正文§11。

## UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1：真实最优凸包槽初始化的无界机器长链修复

- Exact Statement / Quantifiers：∀整数k≥3,d≥1，正文§10的正有理两端任务族有T=OPT=1，x由两个真实最优调度显式凸组合给出。固定任意tiny平局序，全部最小总处理时间槽覆盖匹配共同诱导同一σ，Cmax=2−1/k。每个严格降序负载lex改善至少改变d+1任务并涉及d+2台新旧owner端点机器；同一实际修复同时达到两下界，Cmax=2−2/k且每源至多迁出一件。
- Objects / Domain / Definitions：UM-MODEL-v1；δ=1/k,a=1−1/(2k),D=d+2k−1；root宏/微任务各自有专属容量释放链。H={j:τ(j)≠σ(j)}，参与机为{σ(j),τ(j):j∈H}。ST边只用正长度槽交。
- Assumptions / Scope：固定σ出发的一次严格lex下降邻域；k,d均可无界。真凸包/配置来源成立，但不要求x基本。任意统一ε和固定参与机预算均可独立选k,d攻击。
- Conclusion：强初始化与最小成本择优不能保证有界参与机器的严格下降；不同于三机无界批量，也不同于单目的地分流障碍。
- Dependencies：UM-MODEL-v1、标准ST槽定义；正文直接给两最优调度、严格激活成本差1/(2k)、链容量分类与精确支持计数。无新外部定理。
- Evidence：完整自足证明、statement-first独立重构及冻结正文攻击；规范24参数精确最小成本流，独立3参数270336份全部实际分配和逐机槽匹配；范围见冻结记录。
- Counterevidence / Objections：本族明确可从链尾逐件预修，每步仅两机且Cmax不增；前置步lex恶化，故不否定弱Cmax单调路径。两个已给凸分量可直接返回，不构成算法困难性或一般下界；无当前范围fatal异议。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；全球新颖性、独立论文价值与外审未认证；UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md](../current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)§10；research/reviews/unrelated_machines/optimal_hull_long_chain_review.md；tests/audits/unrelated_machines/optimal_hull_long_chain_gap.py、tests/audits/unrelated_machines/optimal_hull_long_chain_independent.py；两份optimal_hull_long_chain冻结JSON及k3d1输入/证书。

## UM-DAG-TRANSIT-CONGESTION-v1：扩大守恒区间的共同拥塞提取与分叉支撑搜索

- Exact Statement / Quantifiers：∀上述合法D,k,r,K，新共同证书可总位多项式提取真实树b≥1/(2K−1)，每个K由单边k_r=2K−1族精确达到；固定W/K证书与一次整数流饱和等价，K可行单调且最小K位多项式可求。令h_K=#{k≥2K}，枚举这些高点子集、免费补入全L/Z，在2^{h_K}poly(总位长)判定某W证书并输出W/f/树。旧k≥K合同同W/K证书可拓扑裁流转新，反向不总成立。
- Objects / Definitions：含根W及E[W]上共同非负有理f；整数K≥1，B:k≥2K，L:1≤k≤2K−1，Z:k=0；非根I≤K，B上O≥k，非根L上O=I，低根O≥K。输出允许使用E[W]中零f边。
- Domain / Assumptions：显式非空有限简单DAG，原入度0的任意编号根，二进制非负整数需求，零需求只能是原终端；真实根树对全部选中原正需求点收费，包括输出叶。
- Scope / Conclusion：新合同另立身份，不更改UM-DAG-CONGESTION-FLOW-v1。指数因子2^{h_K}仍在，未证明一般好支撑可多项式搜索，未给统一常数K或一般UM算法。
- Dependencies：UM-DAG-DEGREE-MODEL-v1, UM-DAG-TRANSIT-CERTIFICATE-v1；标准整数流自足重构，不依赖未取得的外部定理。
- Evidence：路径分解删过量、拆点整数流、逐点同时比例、拓扑K单调/旧到新裁流、单边sharp及L/Z零流扩支撑的自足证明；先盲重构后冻结攻击，双路全树/原边流精确有限核验。
- Counterevidence / Objections：本范围内未发现仍成立fatal；一般高点共同选择及UM结构提取未解；全球新颖性未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；外审未记录，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/rooted_dag_congestion_flow.md](../current/unrelated_machines/rooted_dag_congestion_flow.md)§7–10；research/reviews/unrelated_machines/rooted_dag_congestion_review.md；tests/audits/unrelated_machines/rooted_dag_transit_branch_search.py、tests/audits/unrelated_machines/rooted_dag_transit_independent.py；evidence/runs/unrelated_machines/rooted_dag_transit_branch_audit.json。

## UM-DAG-NONUNIT-PARAMETER-EXACT-v1：非单位分叉点个数参数的精确需求根树算法

- Exact Statement / Quantifiers：∀上述合法D,k,r，令h=#{v:k_v≥2}和总二进制位长B_in；有确定性2^h poly(B_in)算法输出实际根树H，精确达到b(H)=b*。含b*=0、根终端、巨大二进制需求；不按k数值枚举。
- Objects / Definitions：b=min({1}∪{所选正需求点实际出度/k})；Γ={1}∪{a/k_v:1≤a≤min(k_v,deg_D⁺v)}，|Γ|≤|E|+1。τ阈值用k′=ceil(τk)及新K=1合同，非单位点数不增加。
- Domain / Assumptions：显式非空有限简单DAG，原入度0的任意编号根，二进制非负整数需求，零需求只能是原终端；真实根树对全部选中原正需求点收费，包括输出叶。
- Scope / Conclusion：h是输入参数，任意h时2^h不是多项式。此为根树对象的精确FPT算法，不承诺一般调度近似，不免费从任意处理时间矩阵取得需求树结构。
- Dependencies：UM-DAG-DEGREE-MODEL-v1, UM-DAG-TRANSIT-CONGESTION-v1, UM-DAG-NONUNIT-PARAMETER-v1；标准整数流自足重构，不依赖未取得的外部定理。
- Evidence：K=1证书⇔满比例真实树的双向构造、全部有效阈值集合、整数向上缩放与总位复杂度证明；两份独立9496对象全树核验，另500随机/根重标、深单位走廊及大整数fixture。
- Counterevidence / Objections：本范围内未发现仍成立fatal；一般高点共同选择及UM结构提取未解；全球新颖性未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；外审未记录，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/rooted_dag_congestion_flow.md](../current/unrelated_machines/rooted_dag_congestion_flow.md)§7–10；research/reviews/unrelated_machines/rooted_dag_congestion_review.md；tests/audits/unrelated_machines/rooted_dag_transit_branch_search.py、tests/audits/unrelated_machines/rooted_dag_transit_independent.py；evidence/runs/unrelated_machines/rooted_dag_transit_branch_audit.json。

## UM-SHARED-SINK-MACRO-EXIT-v1：宏任务可共同退出的单汇点匹配

- Exact Statement / Quantifiers：∀显式给定H∪{z}及宏B/唯一home私有组、非负二进制有理T≥0与0<η≤1；macro可在home或z使用，所有有限home宏时间>T/2。存在确定性poly(总位长,1/η)算法FAIL或输出home≤T、z≤(1+η)T的实际调度；OPT≤T必成功。宏数可超过home数，OPT0保持0。
- Objects / Domain / Definitions：UM-MODEL-v1；显式逐台机器列表，正文§8–9定义的macro/private划分及有限边，全部任务必须实际安排。
- Assumptions / Scope：仅单sink、唯一home与给定macro划分；不限制macro sink大小，不提供一般多sink容量恢复或一般输入划分。
- Conclusion：可靠FAIL或逐任务合法分配；成功不判定T精确可行，条件阈值合同不改UM-TARGET-v1。
- Dependencies：UM-MODEL-v1, UM-MACRO-EXIT-MODEL-v1；正文§3自足cover FPTAS、精确二分匹配及所列恢复证明。
- Evidence：(b+h)方阵dummy/exit完美匹配同时选择macro/home或真实sink退出与全部私有组cover；真实exit及强制成本只计一次，局部误差对同一预算相加。 一般证明、独立重构和冻结攻击；两套原矩阵Fraction核验见正文§10。
- Counterevidence / Objections：紧凑H编码异议由显式机器合同解决；没有一般分解/资格恢复器；无尚成立范围内fatal。
- Status：限域完整证明及内部独立审查；标准工具组合，未外审，未认证全球新颖性或独立论文价值。
- Related Files：[正文§8–10](../current/unrelated_machines/shared_sink_joint_macro_assignment.md)、[冻结审查](../reviews/unrelated_machines/private_group_exit_pool_review.md)、private_group_exit_pool的规范/独立代码、实际输入/证书及两份冻结报告。

## UM-BOUNDED-PROFILE-EXIT-POOL-v1：有界profile完整池的共同退出与实际恢复

- Exact Statement / Quantifiers：∀显式给定H∪Z(Z非空)、同样macro/唯一home私有组、T≥0、0<η≤1、ρ≥1、β≥0、a_z>0及c_j≥0；每任务在Z全可用或全不可用，前者逐z满足a_z c_j≤p_zj≤ρa_z c_j及p_zj≤βT。存在确定性poly(总位长,1/η)算法FAIL或实际调度，home≤T、各pool≤[ρ(1+η)+β]T；OPT≤T必成功，OPT0保持0。
- Objects / Domain / Definitions：UM-MODEL-v1；显式逐台机器列表，正文§8–9定义的macro/private划分及有限边，全部任务必须实际安排。
- Assumptions / Scope：sink数不固定，但完整资格、给定共同profile上下包络、各pool边≤βT及唯一home承重；不输出一般矩阵分解，非一般统一ε。
- Conclusion：可靠FAIL或逐任务合法分配；成功不判定T精确可行，条件阈值合同不改UM-TARGET-v1。
- Dependencies：UM-MODEL-v1, UM-MACRO-EXIT-MODEL-v1, UM-EXIT-POOL-PROFILE-MODEL-v1, UM-SHARED-SINK-MACRO-EXIT-v1；正文§3自足cover FPTAS、精确二分匹配及所列恢复证明。
- Evidence：以S=Σ1/a把总work归一化为虚拟sink并共同选择退出集合；实际最小负载list恢复，用加权已分配work守恒与逐边βT支付增量。 一般证明、独立重构和冻结攻击；两套原矩阵Fraction核验见正文§10。
- Counterevidence / Objections：紧凑H编码异议由显式机器合同解决；没有一般分解/资格恢复器；无尚成立范围内fatal。
- Status：限域完整证明及内部独立审查；标准工具组合，未外审，未认证全球新颖性或独立论文价值。
- Related Files：[正文§8–10](../current/unrelated_machines/shared_sink_joint_macro_assignment.md)、[冻结审查](../reviews/unrelated_machines/private_group_exit_pool_review.md)、private_group_exit_pool的规范/独立代码、实际输入/证书及两份冻结报告。

## UM-CONFIG-FINITE-COVER-v1：配置下界的有限覆盖实现及高围长可靠性缺口

- Exact Statement / Quantifiers：∀合法UM实例P，∀有限置换incidence覆盖Q，T_CONF(Q)=T_CONF(P)且T_CONF(P)≤OPT(Q)≤OPT(P)。∀整数g≥1，min_{有限cover Q,incidence girth>g}OPT(Q)=T_CONF(P)，最小值取得；不加g时可取q≤r^(r/2)，r≤m+n为配置等式系统rank。给定有理配置证书可输出敏感地精确实现为某cover的真实调度。
- Objects / Domain / Definitions：UM-MODEL-v1；全部有限边的机器—任务二部incidence图，q≥1，机器(i,b)、任务(j,a)及每有限(i,j)置换π_ij:a↦b，处理时间仍p_ij；配置含空集、每任务精确覆盖。
- Assumptions / Scope：非负二进制有理/∞、显式有限输入，空任务、零时间、单端、断连与孤机均含。给定证书共同分母可巨大；g限制不继承q行列式上界。
- Conclusion：cover不放大配置间隙；存在真调度坍缩到原配置阈值的cover，任意预设高围长仍可如此。
- Dependencies：UM-MODEL-v1、UM-PERMUTATION-COVER-MODEL-v1；正文自证配置投影/提升、整数socket配对、0/1基矩阵Cramer/Hadamard、自由字有限置换群与正规作用。旧编码graph-cover机制仅作来源背景，不把调度恒等式冒充源定理。
- Evidence：自足一般证明；statement-first独立重构再攻击冻结稿；规范128种原调度/160混合及边界，独立128调度/570自由字；证据有限范围另列。
- Counterevidence / Objections：仅原机器/任务等q复制及逐incidence置换、保原时间的覆盖；高围长存在性不保证小尺寸或随机概率。未排精选接线/扩张条件/其他归约，未证明UM-TARGET-v1反面；不提供相对原输入的位多项式配置求解或覆盖输出。 声明范围无尚成立fatal；精选接线仍缺源解码与位规模。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；标准graph-cover机制调度专门重构，全球新颖性/独立论文价值未认证；主目标OPEN。
- Related Files：[configuration_finite_cover_obstruction.md](../current/unrelated_machines/configuration_finite_cover_obstruction.md)、[configuration_finite_cover_review.md](../reviews/unrelated_machines/configuration_finite_cover_review.md)；代码/输入/真实证书/两份冻结结果由正文互链。

## UM-HALL-GROUP-JOINT-FLOW-v1：共同资格私有组的宏微联合流阈值舍入

- Exact Statement / Quantifiers：∀显式H∪Z、宏B/私有组J_h、整数q≥2、有理T≥0和δ≥0且qδ<2；macro仅homes且所有finite p>T/2；j∈J_h恰在h及同组共同E_h⊆Z可用且时间同为w_j≥0，(1/2+1/q)T≤W_h≤T、w_j≤δT。确定性总位poly返回FAIL或完整实际σ，Cmax≤q(2+δ)/(q+1)T；OPT≤T必成功。含T0、空Z/E及二进制q输入，实际机器至少一。
- Objects / Domain / Definitions：UM-MODEL-v1与正文§1；显式homes/sinks及资格，全部任务必须实际安排，空max取0，T0/OPT0明确处理。
- Assumptions / Scope：给定分组、同组共同资格、私有任务等端体积及组负载下界承重；q增长时改善趋零，不是一般UM统一ε。
- Conclusion：实际调度及每台机器同时负载界；前者是one-sided阈值合同，后者是未知OPT的promise实际近似。
- Dependencies：UM-MODEL-v1, UM-HALL-GROUP-MODEL-v1；正文§2–5自足Hall、整数增广、真实前缀与有限阈值搜索。
- Evidence：真实occupied组每组出口>T/q推出共同q槽Hall；一次macro→home→receiver整数流共同选位置；τ=(q−1+qδ)/(q+1)真实前缀平衡home及sink负载，不复制q个sink。 独立statement-first重构、冻结攻击及三路原任务Fraction检查；有限范围见实际记录。
- Counterevidence / Objections：共同资格、体积、组下界省略会破证明；q槽不能凭strict Hall降为q−1；没有一般结构提取或一般容量转换。
- Status：限域完整证明、独立内部已审、规范实际构造已实现；标准工具组合，未外审/未认证全球新颖性或独立论文价值。
- Related Files：[正文](../current/unrelated_machines/hall_group_joint_flow.md)、[冻结审查](../reviews/unrelated_machines/hall_group_joint_flow_review.md)、hall_group_joint_flow三份代码/冻结报告与实际输入/任务分配。

## UM-HALL-GROUP-PROMISE-APPROX-v1：未知最优值下的共同资格组实际近似

- Exact Statement / Quantifiers：∀同拓扑及q≥2,δ≥0,qδ<2，不给OPT；promise在真实OPT处所有finite macro p>OPT/2、(1/2+1/q)OPT≤W_h≤OPT、w_j≤δOPT。存在统一确定性总位poly算法输出完整实际σ，Cmax≤q(2+δ)/(q+1)OPT，OPT0含在内。q/δ可输入；固定q/δ时为该承诺类统一低于2。
- Objects / Domain / Definitions：UM-MODEL-v1与正文§1；显式homes/sinks及资格，全部任务必须实际安排，空max取0，T0/OPT0明确处理。
- Assumptions / Scope：不判定关于OPT的结构承诺；不提供一般矩阵分解，同组共同资格/等端体积和组负载范围保留；可变q时无统一正ε。
- Conclusion：实际调度及每台机器同时负载界；前者是one-sided阈值合同，后者是未知OPT的promise实际近似。
- Dependencies：UM-MODEL-v1, UM-HALL-GROUP-PROMISE-MODEL-v1, UM-HALL-GROUP-JOINT-FLOW-v1；正文§2–5自足Hall、整数增广、真实前缀与有限阈值搜索。
- Evidence：有限macro边值的最小全流瓶颈B可二分求出；t=max(Wmax,wmax/δ,B)≤OPT，由promise在t仍满足阈值合同；δ0先零端检查。无需最优精度oracle或连续搜索。 独立statement-first重构、冻结攻击及三路原任务Fraction检查；有限范围见实际记录。
- Counterevidence / Objections：共同资格、体积、组下界省略会破证明；q槽不能凭strict Hall降为q−1；没有一般结构提取或一般容量转换。
- Status：限域完整证明、独立内部已审、规范实际构造已实现；标准工具组合，未外审/未认证全球新颖性或独立论文价值。
- Related Files：[正文](../current/unrelated_machines/hall_group_joint_flow.md)、[冻结审查](../reviews/unrelated_machines/hall_group_joint_flow_review.md)、hall_group_joint_flow三份代码/冻结报告与实际输入/任务分配。

## UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1：全局四阶分配矩的近平坦实际提取

- Exact Statement / Quantifiers：∀合法一般P、给定有理T>0与0<η≤1，以及正文定义的显式有理四阶C₂分配矩证书y，令n为任务数、d为p_ij≤T有限边数、R=rank M₁≥1，压缩乘法算子A_e及δ=Σ_e tr(A_e−A_e²)。若n,d≥1且δ≤min{1/(64ndR),η/16}，则正文固定任务次序、最大Hilbert–Schmidt子分支且确定平局的贪心算法，在P,T,η,y总输入位长的多项式时间输出实际调度σ，∀i，L_i(σ)≤(1+3δ)T≤(1+η)T。空任务直接输出空分配；T=0用零时间边精确处理。
- Objects / Domain / Definitions：UM-MODEL-v1与正文C₂；M₂、one-hot理想及逐机容量局部化共用同一y。取V₁=span{1,x_e}的正定有理Gram基，A_e=G⁻¹H_e，HS范数使用Gram伴随。δ是全空间trace，不能换成初态能量。
- Assumptions / Scope：显式证书、严格小缺陷条件和总输入位长均承重；全部可用p_e≤T，允许零时间和单可用机器。原P中p>T边只被阈值剪枝；每任务须有剩余边。
- Conclusion / Mechanism：投影漏损D_e=A_e−A_e²=B_e*B_e同时控制幂等缺陷和交换子；固定次序的最大HS分支保持非零近幂等积，最终有理密度逐边损失≤3δ_e，再由同一个逐机算子容量界恢复实际负载。无需数值谱分解或抽样。
- Dependencies：UM-MODEL-v1、UM-GLOBAL-ASSIGNMENT-C2-MOMENT-MODEL-v1；正文自足投影/交换子/近幂等/逐机负载及有理位复杂度证明。Laurent–Mourrain原文仅是δ=0平坦提取和压缩乘法的经典来源，非该定量结论的来源。
- Evidence：先独立重构后冻结证明攻击；规范有理输入检查/提取、独立算子审计与真实分布贪心反例分开登记，精确范围及实际hash见冻结记录。有限核验不替代一般证明。
- Counterevidence / Objections：证书y是额外输入，未给一般输入的C₂证书生成器或小δ保证；δ=0的平坦矩提取属于经典背景，近平坦定量扩展的新颖性未认证。不能把真调度Dirac矩存在当作可多项式获得。在每个OPT≤T实例免费生成本合同的小缺陷证书会要求过强的低于3/2承诺输出，P≠NP下不能作为一般算法的未付代价前提；未否定其他矩舍入或UM-TARGET-v1。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；通用证书生成未实现、未外审、未认证全球新颖性，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/global_assignment_moment_rounding.md](../current/unrelated_machines/global_assignment_moment_rounding.md)、research/reviews/unrelated_machines/global_assignment_moment_rounding_review.md；tests/audits/unrelated_machines/nearflat_moment_extraction.py, tests/audits/unrelated_machines/near_flat_hs_independent_audit.py, tests/audits/unrelated_machines/global_assignment_flat_moment_audit.py, tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py；evidence/runs/unrelated_machines/nearflat_moment_extraction_audit.json, evidence/runs/unrelated_machines/near_flat_hs_independent_audit.json, evidence/runs/unrelated_machines/hs_effect_greedy_exact_m3_audit.json；examples/unrelated_machines/nearflat_moment_inputs.json, examples/unrelated_machines/full_hs_m3_input.json；evidence/certificates/unrelated_machines/global_assignment_moment_freeze.json；原始来源及定位见LITERATURE/manifest。

## UM-GLOBAL-MOMENT-HS-GREEDY-GAP-v1：真实最优矩上全空间HS贪心的二倍反例

- Exact Statement / Quantifiers：存在三台完全相同机器、一个处理时间1任务与八个处理时间1/4任务的实例，T=OPT=1。对全部210个真实最优调度取均匀分布，并取其完整四阶矩，rank M₁=17。对K₀=I_R、先处理单位任务再按标签处理八个小任务、机器标签最小平局规则，每步最大化∥A_eK∥²_HS并更新K←A_eK的确定算法输出负载(1,2,0)，因此Cmax=2OPT。
- Objects / Domain / Definitions：同一正文C₂压缩算子；真实最优调度以大任务目的地及另两机各四个带标签小任务确定。K₀是全空间恒等算子，HS范数以Gram度量计算。
- Assumptions / Scope：固定的三机正有理实例，所列任务顺序及确定平局；不假定小δ。任务标签和机器标签是算法输入顺序的一部分。
- Conclusion / Mechanism：全空间HS分支可逐次集中全部小任务，尽管输入全部四阶矩来自真正最优分布；保留全局相容性本身未给该贪心的统一负载余量。
- Dependencies：UM-MODEL-v1、UM-GLOBAL-ASSIGNMENT-C2-MOMENT-MODEL-v1、正文对真实分布及有理HS决策逐步重构。
- Evidence：全部真实最优调度的精确枚举、实际Gram秩及每步有理分支得分由冻结代码复核；规范与独立近平坦程序不被当作该实例之外的舍入证明。
- Counterevidence / Objections：只攻击所列全空间HS初始化、任务顺序与平局规则的无小δ贪心合同。矩来自真实最优分布，故失败不是伪矩不相容；不否定近平坦提取定理、秩一初态、所有任务排序、其他联合矩算法或一般低于2近似。有限程序核对该精确实例；正文承担实例的一般定义与实际输出证明。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；这是准确算法反例，全球新颖性与独立论文价值未认证，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/global_assignment_moment_rounding.md](../current/unrelated_machines/global_assignment_moment_rounding.md)、research/reviews/unrelated_machines/global_assignment_moment_rounding_review.md；tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py；evidence/runs/unrelated_machines/hs_effect_greedy_exact_m3_audit.json；examples/unrelated_machines/full_hs_m3_input.json；evidence/certificates/unrelated_machines/global_assignment_moment_freeze.json。

## UM-CACTUS-HIGH-GIRTH-CONFIG-GAP-v1：任意给定围长的简单仙人掌配置间隙上确界二

- Exact Statement / Quantifiers：∀整数g≥3，在正OPT、每任务恰2有限端且简单机器支撑为cactus、girth≥g的实例上，sup OPT/T_CONF=2。具体∀k≥2有全时间{1/k,1}、每非桥块为g环的P_(k,g)，OPT=2−1/k、CONFIG在T=1+1/k有显式稀疏有理证书。
- Objects / Domain / Definitions：UM-MODEL-v1；显式非负二进制有理/∞矩阵，每任务一/两有限端（间隙族恰两端）；labelled多重机器图、顶点双连通块与精确配置LP按正文定义。
- Assumptions / Scope：T只是可行配置阈值，不声称最小T_CONF=T或有限例取得2；族规模不要求对log k多项式。cactus可被真实结构精确求解，本gap不导入计算困难性或UM-TARGET反面。
- Conclusion：任意给定围长的简单仙人掌配置间隙上确界二；原目标及反面仍OPEN。
- Dependencies：UM-MODEL-v1, UM-CACTUS-GAP-FAMILY-v1, UM-ST-ROUND-v1；g环任务数比内部机器多1迫末端小负载；树路径整数传播及显式θ调度；循环k窗口/内部singleton/根边际thinning给配置证书；经典ST给gap上界。
- Evidence：完整自足证明，审查者先仅看精确Claim独立重构，再攻击冻结稿；规范/独立原任务枚举、六组实际高围长族及逐任务σ校验，有限范围另见冻结记录。
- Counterevidence / Objections：T只是可行配置阈值，不声称最小T_CONF=T或有限例取得2；族规模不要求对log k多项式。cactus可被真实结构精确求解，本gap不导入计算困难性或UM-TARGET反面。 最终冻结范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；已知工具自足扩展及末端环替换，全球新颖性、独立成文价值与外审未认证。
- Related Files：[cactus_configuration_gap_and_block_exactness.md](../current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)、[cactus_gap_and_block_exactness_review.md](../reviews/unrelated_machines/cactus_gap_and_block_exactness_review.md)；正文互链三份代码、输入/配置与真实调度证书、两份冻结记录。

## UM-TWO-CHOICE-BLOCK-RANK-EXACT-v1：最大顶点块环秩参数的精确实际调度

- Exact Statement / Quantifiers：∀support≤2合法UM输入，保留每双端任务为独立labelled机器多重边，顶点双连通块（桥独立）B的b_B=|E_B|−|V_B|+1，b=max({0}∪{b_B})，存在确定性2^b poly(总输入位长L)算法输出精确OPT及实际调度；空/零/单端/平行均含。
- Objects / Domain / Definitions：UM-MODEL-v1；显式非负二进制有理/∞矩阵，每任务一/两有限端（间隙族恰两端）；labelled多重机器图、顶点双连通块与精确配置LP按正文定义。
- Assumptions / Scope：b可增长；一般时指数不消失。不能合并平行任务来计b，也不是treewidth精确算法。b=O(log L)类可解只限制此范围hardness归约，不改变一般UM-TARGET。AMO已有对称cactus算法，端点非对称及参数版本优先权未认证。
- Conclusion：最大顶点块环秩参数的精确实际调度；原目标及反面仍OPEN。
- Dependencies：UM-MODEL-v1, UM-TWO-CHOICE-BLOCK-MODEL-v1；块割树只传最小真实单边界负载；各块独立枚举反馈边再叶交换支配，不跨块做笛卡尔积；保存任务见证；LCM整数格点二分位多项式。
- Evidence：完整自足证明，审查者先仅看精确Claim独立重构，再攻击冻结稿；规范/独立原任务枚举、六组实际高围长族及逐任务σ校验，有限范围另见冻结记录。
- Counterevidence / Objections：b可增长；一般时指数不消失。不能合并平行任务来计b，也不是treewidth精确算法。b=O(log L)类可解只限制此范围hardness归约，不改变一般UM-TARGET。AMO已有对称cactus算法，端点非对称及参数版本优先权未认证。 最终冻结范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；已知工具自足扩展及末端环替换，全球新颖性、独立成文价值与外审未认证。
- Related Files：[cactus_configuration_gap_and_block_exactness.md](../current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)、[cactus_gap_and_block_exactness_review.md](../reviews/unrelated_machines/cactus_gap_and_block_exactness_review.md)；正文互链三份代码、输入/配置与真实调度证书、两份冻结记录。

## UM-PSEUDOFOREST-CONFIG-EXACT-v1：每连通分量至多单环的配置可行性精确

- Exact Statement / Quantifiers：∀support≤2合法UM实例P及有理T≥0，若保labelled平行任务的机器多重图每连通分量环秩≤1，则CONFIG(T)可行⇔存在真实makespan≤T调度；包含两平行边的长度2环、森林、单端、零时间和空任务。
- Objects / Domain / Definitions：UM-MODEL-v1；显式非负二进制有理/∞矩阵，每任务一/两有限端（间隙族恰两端）；labelled多重机器图、顶点双连通块与精确配置LP按正文定义。
- Assumptions / Scope：要求每连通分量至多一环，不能弱化为每顶点块至多一环；多环cactus已有supgap2。没有改变一般CONFIG身份，也不导入一般近似或困难性。
- Conclusion：每连通分量至多单环的配置可行性精确；原目标及反面仍OPEN。
- Dependencies：UM-MODEL-v1, UM-TWO-CHOICE-BLOCK-MODEL-v1；单端任务在正配置中必出现；叶边可容则固定叶并删父配置中的该任务，否则强制父并计固定负载；余单环有禁止端则破环，否则统一循环定向。
- Evidence：完整自足证明，审查者先仅看精确Claim独立重构，再攻击冻结稿；规范/独立原任务枚举、六组实际高围长族及逐任务σ校验，有限范围另见冻结记录。
- Counterevidence / Objections：要求每连通分量至多一环，不能弱化为每顶点块至多一环；多环cactus已有supgap2。没有改变一般CONFIG身份，也不导入一般近似或困难性。 最终冻结范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified；已知工具自足扩展及末端环替换，全球新颖性、独立成文价值与外审未认证。
- Related Files：[cactus_configuration_gap_and_block_exactness.md](../current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)、[cactus_gap_and_block_exactness_review.md](../reviews/unrelated_machines/cactus_gap_and_block_exactness_review.md)；正文互链三份代码、输入/配置与真实调度证书、两份冻结记录。

## UM-PRIVATE-GRAFT-NO-AMPLIFICATION-v1：需求树私有组合的精确瓶颈与无放大范围

- Exact Statement / Quantifiers：∀合法需求DAG G,H，私有终端替换满足b*(G∘H)=min(b*G,b*H)，异质终端有式(2)的精确max–min；正需求k根接m个私有模块的值为max_s min(1,s/k,β_(s))（m=0取0）。固定结构/需求及常数模块、同一β输入的有限私有组合是f(β)=max(f(0),min(f(1),β))，若保YES f(1)=1则f(β)≥β，不产生NO比例放大。
- Objects / Domain / Definitions：第1节需求DAG/真实根树；私有识别、正需求根门与完全pool/直接坐标tensor分别按[正文](../current/unrelated_machines/private_graft_and_resource_repetition.md)§2–5定义。零需求只限原终端；正需求死端仍收费；3DM坐标带标签。
- Assumptions：无复杂度假设；第1节P≠NP下近2 gap合同是未完成义务，不是本Claim假设或已得结论。
- Scope / Conclusion：只限制已定义的私有值组合；不排跨模块共享、一致性测试、输入结构依赖归约或一般算法。完整根门k>0承重；式子不是已能高效求b*。 UM-TARGET-v1仍OPEN。
- Dependencies：UM-DAG-DEGREE-MODEL-v1；UM-DAG-DEGREE-TOKEN-IDENTITY-v1只用于真实调度翻译；自足有限树/max–min或整数多重边证明。不承重导入SA困难性。
- Evidence：双Astra先独立重构、再冻结hash攻击；boss亲核。规范21384替换对及实际13任务调度oracle，独立4500替换/2000根门、768 pool案例；范围与hash在冻结结果，不代替一般证明。
- Counterevidence / Objections：无尚成立fatal；冻结审查指出BLMRS页码非致命错误已修。共享接口不满足私有性；所得边界不支持否定通用调度算法。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。外审及全球新颖性未认证，不称独立论文突破。
- Related Files：research/current/unrelated_machines/private_graft_and_resource_repetition.md；research/reviews/unrelated_machines/private_graft_repetition_review.md；tests/audits/unrelated_machines/private_graft_and_resource_repetition.py；tests/audits/unrelated_machines/private_graft_independent.py；tests/audits/unrelated_machines/resource_pool_independent.py；evidence/runs/unrelated_machines/private_graft_repetition_audit.json；examples/unrelated_machines/parity_3dm_repetition.json。

## UM-RESOURCE-REPETITION-SOUNDNESS-NO-v1：完全元素池的分数整数化与直接重复的保真反例

- Exact Statement / Quantifiers：∀显式3DM A、整数r≥1，每元素r克隆且每原边含全部r³组合的完全池A^[r]有完美匹配，当且仅当A有权重属于(1/r)Z≥0的分数完美匹配。四边parity A={000,011,101,110}原无完美匹配，r2完全池及每个t≥2的直接坐标张量均有完美匹配；相应需求树token调度的真实OPT由3/2降至1。
- Objects / Domain / Definitions：第1节需求DAG/真实根树；私有识别、正需求根门与完全pool/直接坐标tensor分别按[正文](../current/unrelated_machines/private_graft_and_resource_repetition.md)§2–5定义。零需求只限原终端；正需求死端仍收费；3DM坐标带标签。
- Assumptions：无复杂度假设；第1节P≠NP下近2 gap合同是未完成义务，不是本Claim假设或已得结论。
- Scope / Conclusion：pool和坐标张量是不同操作；只否定这些明确NO保真合同。固定r显式多项式，二进制增长r的显式复制不保证位多项式。不是近2计算困难性，也不是所有张量归约障碍。 UM-TARGET-v1仍OPEN。
- Dependencies：UM-DAG-DEGREE-MODEL-v1；UM-DAG-DEGREE-TOKEN-IDENTITY-v1只用于真实调度翻译；自足有限树/max–min或整数多重边证明。不承重导入SA困难性。
- Evidence：双Astra先独立重构、再冻结hash攻击；boss亲核。规范21384替换对及实际13任务调度oracle，独立4500替换/2000根门、768 pool案例；范围与hash在冻结结果，不代替一般证明。
- Counterevidence / Objections：无尚成立fatal；冻结审查指出BLMRS页码非致命错误已修。共享接口不满足私有性；所得边界不支持否定通用调度算法。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。外审及全球新颖性未认证，不称独立论文突破。
- Related Files：research/current/unrelated_machines/private_graft_and_resource_repetition.md；research/reviews/unrelated_machines/private_graft_repetition_review.md；tests/audits/unrelated_machines/private_graft_and_resource_repetition.py；tests/audits/unrelated_machines/private_graft_independent.py；tests/audits/unrelated_machines/resource_pool_independent.py；evidence/runs/unrelated_machines/private_graft_repetition_audit.json；examples/unrelated_machines/parity_3dm_repetition.json。

## UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1：真实最优矩上固定阶向量贪心的线性最坏界

- Exact Statement / Quantifiers：每固定r≥1、每素数q>4r+2，q台机器/q+1任务的显式实例有真实最优源D，OPT=4r+2；固定V_r压缩乘法向量范数贪心在任何任务顺序上都严格把q个普通任务送0，输出比q/(4r+2)=(n−1)/(4r+2)。一般真实T源下该规则合法且≤nT；固定r故最坏量级线性。
- Objects / Domain / Definitions：UM-MODEL-v1；H=L²(D)、V_r为至多r任务指标单项式空间，A_e=P_r M_xe，ψ初始1；每任务一次选最大‖A_eψ‖²后更新。精确矩来自同一个有限有理真实T可行源；最优版T=OPT。正文§1准确合同。
- Assumptions / Scope：r固定但任意；整个过程固定D/V_r/A_e，任意任务顺序含自适应；平局可任意。下界q>4r+2为素数，普通单位时间与独占anchor时间4r+2；q≤B仅边界核验。
- Conclusion：该准确规则最坏比沿无限族Ω(n)，结合一般O(n)为线性量级；严格选择、顺序无关。不是一般近似突破。
- Dependencies：模型；(2r+1)-wise分类变量正交分解及fresh压缩恒等式；Vandermonde满射与单变量根数界；均在正文证明。
- Evidence：自足一般证明、先独立重构后冻结攻击；实际q3/5/7一级Gram/全部三阶/Fraction路径，q13全部源与三点计数，二级有限源和小投影另列范围。q13原矩阵及全部2197个最优源原子可复查。
- Counterevidence / Objections：零最优句已澄清为最优源T=OPT=0；一般真实T源仅得nT。仅固定原矩/子空间反复压缩乘法并贪心最大化向量范数的准确规则；不是层级整数间隙或一般算法困难性。真正条件化、重建矩和容量反馈未排除；主目标仍OPEN。固定r的复杂度不可扩为r输入时统一多项式。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。证明、内审、实现、新颖性分别登记；固定r矩输入位多项式不提供最优矩oracle。
- Related Files：[正文](../current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)、[冻结审查](../reviews/unrelated_machines/truncated_vector_greedy_review.md)、正文§7全部代码/输入/证书/证据。

## UM-PROJECTED-VECTOR-GREEDY-UNBOUNDED-v1：真实最优矩压缩向量规则的三机全正无界比

- Exact Statement / Quantifiers：∀整数k≥2，存在三机全正有限有理矩阵P、有限正有理真实最优调度分布μ及固定任务序，T=OPT=1，V=span{1,x_ij}上的真实压缩A_ij=ΠM_xij|V，从ψ=1按max||A_ijψ||²选边后左乘的规则全部严格选择，实际Cmax>k−1/2。
- Objects / Domain：UM-MODEL-v1；有限正有理真实完整调度分布、L²(μ)、完整一阶literal张成V、真实正交压缩与固定输入任务序。反例全时间严格正且有限。
- Definitions：UM-PROJECTED-VECTOR-RULE-v1，正文§1。每步更新不重求矩，不对过去已选事件真实条件化；非零标量归一化不改赢家。
- Assumptions：μ每个支撑原子正概率、makespan=OPT=1；不要求每条有限边边际正。严格赢家使反例不依赖平局规则。
- Scope / Conclusion：任意给定真实最优分布/固定顺序的该规则无统一有限近似比。未要求全边际正；不排选择好μ、自适应调序、重新耦合、其他更新或UM-TARGET-v1。副本数仅有效有限，未给poly(k)反例大小。
- Dependencies：UM-MODEL-v1；真实压缩定义。无界身份由§2多数恒等/持续性/净化、§3有限路径、§4正有理fullcube、§5三机全正提升共同推出；单位身份由§7显式输入及精确线性代数证书推出。无外部困难性假设。
- Evidence：完整自足一般证明与先盲后冻结攻击；规范Gram逆与独立样本投影从实际P/全部真实原子核验。三机12原子/323步、单位14原子/120序、边界和公式范围见冻结JSON；有限检查不是一般证明。
- Counterevidence / Objections：初审∞·0求和及未访问H0表述已修；非零overlap、最终V固定、finite repeats、全部机器同时守容均已独立攻击。声明范围无尚成立fatal；全球新颖性及外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。实现为给定显式分布的审计程序，不是一般真矩oracle或主目标算法。
- Related Files：research/current/unrelated_machines/projected_vector_greedy_unbounded.md、research/reviews/unrelated_machines/projected_vector_greedy_review.md、两份projected/vector审计、两个实际输入、evidence/runs/unrelated_machines/projected_vector_greedy_audit.json。来源公屏249具体规则，本对话boss2及内部独立重构。

## UM-PROJECTED-VECTOR-GREEDY-UNIT-COLLISION-v1：五机单位任务真实矩的严格投影碰撞

- Exact Statement / Quantifiers：存在五机五任务全时间1及14个真实OPT1排列的均匀分布，dimV=12；固定顺序1..5的同一压缩向量规则全严格输出(1,2,3,4,2)，Cmax=2；全部120序按最小机器破平局恰118个输出1、2个输出2。
- Objects / Domain：UM-MODEL-v1；有限正有理真实完整调度分布、L²(μ)、完整一阶literal张成V、真实正交压缩与固定输入任务序。反例全时间严格正且有限。
- Definitions：UM-PROJECTED-VECTOR-RULE-v1，正文§1。每步更新不重求矩，不对过去已选事件真实条件化；非零标量归一化不改赢家。
- Assumptions：μ每个支撑原子正概率、makespan=OPT=1；不要求每条有限边边际正。严格赢家使反例不依赖平局规则。
- Scope / Conclusion：只限给定显式分布/固定规则。成功调序存在，不称所有调序坏，不称全局最坏比恰2，不含主目标困难性。
- Dependencies：UM-MODEL-v1；真实压缩定义。无界身份由§2多数恒等/持续性/净化、§3有限路径、§4正有理fullcube、§5三机全正提升共同推出；单位身份由§7显式输入及精确线性代数证书推出。无外部困难性假设。
- Evidence：完整自足一般证明与先盲后冻结攻击；规范Gram逆与独立样本投影从实际P/全部真实原子核验。三机12原子/323步、单位14原子/120序、边界和公式范围见冻结JSON；有限检查不是一般证明。
- Counterevidence / Objections：初审∞·0求和及未访问H0表述已修；非零overlap、最终V固定、finite repeats、全部机器同时守容均已独立攻击。声明范围无尚成立fatal；全球新颖性及外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。实现为给定显式分布的审计程序，不是一般真矩oracle或主目标算法。
- Related Files：research/current/unrelated_machines/projected_vector_greedy_unbounded.md、research/reviews/unrelated_machines/projected_vector_greedy_review.md、两份projected/vector审计、两个实际输入、evidence/runs/unrelated_machines/projected_vector_greedy_audit.json。来源公屏249具体规则，本对话boss2及内部独立重构。

## 真实矩提取两条反例机制的交叉定位

本组UM-PROJECTED-VECTOR-GREEDY-UNBOUNDED-v1给固定三机、全严格正有限时间、固定序上的重复净化失效；同行UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1的[独立正文](../current/unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)另给每固定r、任意顺序的线性量级族。后者有增长机器数和专用anchor，与本组范围不同；彼此不是证明前提。已实际读取其§1–7，保留全部原身份、代码与冻结证据，不重复认领其有限独立源机制。

## UM-WEIGHTED-GROUP-JOINT-SLOT-v1：共同资格组的加权出口联合槽阈值舍入

- Exact Statement / Quantifiers：∀显式不交H∪Z、宏B与唯一home私有组J_h；macro仅H可用且全部有限p>T/2；j∈J_h恰在{h}∪E_h可用、同组共同E_h⊆Z且全部有限端时间相同w_j≥0。∀有理T≥0、0≤δ<1/2，若W_h≤T、w_j≤δT，则确定性总位poly返回FAIL或实际完整σ，home≤(3/2+δ)T、sink≤3T/2；OPT≤T必成功。无组负载正下界、sink数不固定。
- Objects / Domain / Definitions：一般UM的显式非负二进制有理/∞输入，机器不交H∪Z、原任务不交B及J_h；全部符号按[research/current/unrelated_machines/weighted_group_joint_slot_rounding.md](../current/unrelated_machines/weighted_group_joint_slot_rounding.md)§1–2，空任务/零值明确处理。
- Assumptions / Scope：唯一home/给定分组、同组共同接收资格、私有任务等端体积、macro全部端大于半阈值、尺寸δ<1/2仍承重；不是一般UM算法。LP和未知OPT是完整数学算法，软件仅实现给定精确LP见证后的验证/舍入，未实现通用有理LP后端或端到端未知OPT。
- Conclusion：具体合法完整分配，所有机器同时的负载界；阈值版为one-sided FAIL，promise版不读取OPT。
- Dependencies：UM-MODEL-v1, UM-WEIGHTED-GROUP-MODEL-v1；标准有理LP、ST有序槽和整数增广流；自足证明§2–6。
- Evidence：真实occupied组出口>d_h=(W_h−T/2)_+给共同加权token LP；按d_h造槽并用带home容量的一个整数流联合选择macro/home/sink；首次撤离前缀留量≤(1/2+δ)T使actual出口≤d_h。未知OPT用原时间分母乘积Q的整数网格和单调LP测试，最小接受t≤OPT。 独立statement-first重构及冻结攻击、两路Fraction实际任务核验；有限范围见阶段记录，不替代一般证明。
- Counterevidence / Objections：无尚成立fatal；去掉共同资格/等端体积/home角色不交会破当前证明，未主张相应一般模型不可能。全球新颖性、外审及独立论文价值未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：research/current/unrelated_machines/weighted_group_joint_slot_rounding.md；research/reviews/unrelated_machines/weighted_group_joint_slot_review.md；tests/audits/unrelated_machines/weighted_group_joint_slot.py, tests/audits/unrelated_machines/weighted_group_slot_independent.py；evidence/runs/unrelated_machines/weighted_group_joint_slot_audit.json；examples/unrelated_machines/weighted_group_joint_slot_cases.json；evidence/certificates/unrelated_machines/weighted_group_joint_slot_witness.json。

## UM-WEIGHTED-GROUP-PROMISE-APPROX-v1：未知最优值下加权共同组的实际近似

- Exact Statement / Quantifiers：∀同样显式结构及有理0≤δ<1/2，不给T；promise在OPT处全部有限macro p>OPT/2、W_h≤OPT、w_j≤δOPT。确定性总位poly输出全部实际任务分配且Cmax≤(3/2+δ)OPT，含OPT0及δ0。固定δ有本类统一ε=1/2−δ；不提供一般分组或识别promise。
- Objects / Domain / Definitions：一般UM的显式非负二进制有理/∞输入，机器不交H∪Z、原任务不交B及J_h；全部符号按[research/current/unrelated_machines/weighted_group_joint_slot_rounding.md](../current/unrelated_machines/weighted_group_joint_slot_rounding.md)§1–2，空任务/零值明确处理。
- Assumptions / Scope：唯一home/给定分组、同组共同接收资格、私有任务等端体积、macro全部端大于半阈值、尺寸δ<1/2仍承重；不是一般UM算法。LP和未知OPT是完整数学算法，软件仅实现给定精确LP见证后的验证/舍入，未实现通用有理LP后端或端到端未知OPT。
- Conclusion：具体合法完整分配，所有机器同时的负载界；阈值版为one-sided FAIL，promise版不读取OPT。
- Dependencies：UM-MODEL-v1, UM-WEIGHTED-GROUP-PROMISE-MODEL-v1, UM-WEIGHTED-GROUP-JOINT-SLOT-v1；标准有理LP、ST有序槽和整数增广流；自足证明§2–6。
- Evidence：真实occupied组出口>d_h=(W_h−T/2)_+给共同加权token LP；按d_h造槽并用带home容量的一个整数流联合选择macro/home/sink；首次撤离前缀留量≤(1/2+δ)T使actual出口≤d_h。未知OPT用原时间分母乘积Q的整数网格和单调LP测试，最小接受t≤OPT。 独立statement-first重构及冻结攻击、两路Fraction实际任务核验；有限范围见阶段记录，不替代一般证明。
- Counterevidence / Objections：无尚成立fatal；去掉共同资格/等端体积/home角色不交会破当前证明，未主张相应一般模型不可能。全球新颖性、外审及独立论文价值未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：research/current/unrelated_machines/weighted_group_joint_slot_rounding.md；research/reviews/unrelated_machines/weighted_group_joint_slot_review.md；tests/audits/unrelated_machines/weighted_group_joint_slot.py, tests/audits/unrelated_machines/weighted_group_slot_independent.py；evidence/runs/unrelated_machines/weighted_group_joint_slot_audit.json；examples/unrelated_machines/weighted_group_joint_slot_cases.json；evidence/certificates/unrelated_machines/weighted_group_joint_slot_witness.json。

## UM-THRESHOLD-COVER-JOINT-SLOT-v1：可调保留阈值与乘法覆盖的共同组结构定理

- Exact Statement / Quantifiers：在 `UM-WEIGHTED-GROUP-JOINT-SLOT-v1` 的 home/sink、共同资格、等端时间结构中，给定 `T>0`、`τ∈[1/2,1)`、`η>0`、`W_h≤T`、`w_j≤δT`，用最小覆盖背包乘法 FPTAS 选 `e_h` 后，若联合宏/home/sink 加权槽 LP 可行，则可输出实际调度，`Cmax≤max{1+τ,(1+η)(2−τ+δ)}T`；`δ+η+δη<1` 时平衡值 `((1+η)(3+δ))/(2+η)<2`。在同一结构的 `OPT` promise（`W_h≤OPT,w_j≤δOPT,p_hb>OPT/2`）下，分母乘积网格的 one-sided 接受/拒绝二分闭合未知 `OPT`。
- Objects / Domain / Definitions：共同资格私有组、宏端 `T/2<p≤T`、`d_h=(W_h−τT)_+`、`e_h` 为达到 `d_h` 的最小覆盖近似；完整定义和给定阈值证明见 `research/questions/unrelated_machines/barrier_escape_obligations.md` 新增章节。
- Assumptions / Scope：唯一 home、共同资格、等端时间、宏/私有分组和固定 `δ,η` 仍承重；FPTAS 只缩放覆盖目标成本并保留精确覆盖约束。不能替代一般 UM-TARGET-v1。
- Conclusion：条件性 `R<2` 正面接口；`η` 固定时 FPTAS 为输入位长多项式，若 `η` 输入则时间显式依赖 `1/η`。
- Dependencies：UM-WEIGHTED-GROUP-JOINT-SLOT-v1 的联合槽流；最小覆盖 FPTAS；共同资格与等端时间的真实出口计费。
- Evidence：旧公式核验只检查代数，未检查恢复；本次`threshold_cover_recovery.py`及独立脚本实现精确覆盖DP与原任务回算，冻结证明/独立审查见同一review。未知OPT重新检查one-sided整数网格不变量。
- Counterevidence / Objections：旧前缀4/5而覆盖3/5的fatal异议由同行4300c26登记，原完成状态撤回；修复直接迁出同一覆盖X使实际成本=e，并同时比较大单件/小件前缀UB、截断精确覆盖DP。已独立攻击本次修复，无尚存fatal。异资格、异端与一般结构生成不在合同内。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified; UM-TARGET-v1 OPEN。
- Related Files：`research/questions/unrelated_machines/barrier_escape_obligations.md`；`research/current/unrelated_machines/weighted_group_joint_slot_rounding.md`；`research/reviews/unrelated_machines/threshold_cover_and_support_release_review.md`；`tests/audits/unrelated_machines/lst_support_release_and_threshold_group.py`；`evidence/runs/unrelated_machines/lst_support_release_and_threshold_group_audit.json`。

## UM-LST-SUPPORT-RELEASE-v0：锁定给定 LST 正支撑的容量释放合同（已反驳）

- Exact Statement / Quantifiers：声称对任意 `OPT≤T` 实例和任意 LST 可行分数解 `x`，可在 `x` 的正支撑上先匹配大边，再将全部剩余任务整型放入释放容量；该声称为假。
- Objects / Domain / Definitions：`m` 个核心机、一个扩展机；`A_i` 在核心端 `51/100`、扩展端不可用；`m+1` 个 `B_j` 在所有端 `s_m=49m/[100(m+1)]`；LST 中 `A` 和 `B` 均只在核心支撑。旧参数族的精确最优值是 `OPT=51/100+s_m=1−49/[100(m+1)]<1`；`T=1` 可行调度使用扩展机上的零质量 `B` 边。
- Conclusion：任意 `m≥2`，正支撑大边匹配后每核心释放 `49/100`，但每个 `B` 耗时 `s_m` 且 `2s_m>49/100`，所以 `m+1` 个残余任务不能整型进入核心支撑。该接口不成立。
- Dependencies：UM-MODEL-v1；LST 负载行和；完整族及精确 Fraction 审计见问题页。
- Evidence：`m=2,…,7` 精确核验均输出 `support_residual_feasible=false`，并记录旧族精确 `OPT=51/100+s_m<1`；范围见冻结 JSON。
- Counterevidence / Objections：反驳仅针对“锁定任意给定 LST 正支撑”的合同，不是配置 gap、一般困难性或主目标反面；允许支撑扩张/联合证书后仍开放。
- Status：refuted interface; salvage is the obligation to construct support-expanding joint `(H,z)` certificates。
- Related Files：`research/questions/unrelated_machines/barrier_escape_obligations.md`；`tests/audits/unrelated_machines/lst_support_release_and_threshold_group.py`；`evidence/runs/unrelated_machines/lst_support_release_and_threshold_group_audit.json`。

## UM-LST-SUPPORT-RELEASE-OPTIMAL-v1：真实 OPT=1 的多块正支撑释放前沿

- Exact Statement / Quantifiers：对任意整数 `m≥2,r≥1`，取 `r` 个独立块；每块有 `m` 核心机、一备用机、`m` 私有任务和一个单位锚任务。私有任务在其核心和备用机耗时 `1−1/m`，锚任务在全部本块机器耗时1。LST分数点把私有任务放核心、锚均匀放核心，核心负载恰1。若最多激活 `k` 条该分数点零质量边，则最小最大负载为 `2−1/m`（`k<r`）或1（`k≥r`）。
- Objects / Domain / Definitions：显式非负有理/∞不相关调度输入；块间边不可用；零质量边指相对该LST点的 `x=0` 但处理时间有限的边。
- Assumptions / Scope：只限制固定LST正支撑加至多k条零边的输出合同；不限制重新求解分数点、联合选择支撑、无界释放或一般算法。
- Conclusion：每块锚任务给OPT≥1，锚放备用机给OPT=1；未释放块的锚与私有任务叠加为 `2−1/m`，每块至少一条零边才可达到1。令m增长，任意固定相对预算 `k<r` 的比例趋2。
- Dependencies：UM-MODEL-v1；块独立性和直接负载计数。
- Evidence：`tests/audits/unrelated_machines/lst_support_release_optimal.py` 的 Fraction 枚举覆盖 `m=2,…,5,r=1,…,3`；冻结结果见 `evidence/runs/unrelated_machines/lst_support_release_optimal_audit.json`。
- Counterevidence / Objections：这是固定支撑释放方法的精确障碍，不是一般近2困难性；允许支撑共同重选、从头构造或按实例规模激活零边后仍开放。
- Status：complete stated-scope obstruction; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：`research/current/unrelated_machines/lst_support_release_optimal_gap.md`；`research/reviews/unrelated_machines/threshold_cover_and_support_release_review.md`；审计脚本与冻结结果。

## UM-RANKJUMP-ONE-EXCHANGE-v0：一维矩缺陷下的共同交换提取接口

- Exact Statement / Quantifiers：若给定有理四阶布尔矩满足 `rank(M2)=rank(M1)+1`，并额外验证每端补投影平方条件、每任务标量块和为1、跨块共同交换条件 (CE)，以及 `V2` 上逐机负载 localizer，则可在总输入位长多项式时间提取至多 `rank(M2)` 个正权 one-hot 原子并筛出 `T` 可行实际分配。
- Objects / Domain / Definitions：`V1,V2` 为次数至多一/二的 PSD 商空间，`V2=V1⊕W`, `dimW=1`; `X_e=[A_e;B_e]`, `D_e=B_e*B_e`; `P_e=[[A_e,b_e*],[b_e,c_e]]`; (CE) 和共同谱投影见问题页的 rank-jump 章节。
- Conclusion：额外共同交换证书成立时，原子提取和四阶条目重构是确定性有理线性代数；rank jump 本身不被宣称足够。
- Dependencies：布尔四阶矩恒等式、共同交换投影、二阶 localizer；经典 flat extension 只作背景，不导入 rank-jump-one 结论。
- Evidence：目前为自足代数重构，尚无完整 C2 伪矩非交换反例，也未认证公屏 `4−2√2` 支持常数。
- Counterevidence / Objections：`rank(M2)-rank(M1)=1` 只说明一维缺陷；抽象块例仅满足逐端局部投影条件（旧第三端补齐任务守恒断言算术错误并已删除），但 `P_1,P_2` 不交换，故 (CE) 是真实 proof obligation。没有把该抽象块例升级成完整调度伪矩反例。
- Status：conditional candidate; rank-jump-one extension lemma OPEN; no general UM algorithm。
- Related Files：`research/questions/unrelated_machines/barrier_escape_obligations.md`（rank-jump 章节）；`research/current/unrelated_machines/global_assignment_moment_rounding.md`。

## UM-RANKJUMP-ONE-TRUE-SUPPORT-v1：真实有限支持上一维矩跳跃的原子闭合

- Exact Statement / Quantifiers：对有限正权真实分布 `S`（每个支持点为合法一任务一选调度），若完整四阶布尔矩满足 `rank(M2)=rank(M1)+1=R+1`，则 `|S|=R+1=rank(M2)`、`V2=R^S`，共同坐标投影可由有理矩条目确定性恢复至多 `R+1` 个正权原子；若所有支持调度均为 `T`-可行，任取恢复原子给出实际 `T`-可行分配。
- Objects / Domain / Definitions：`U=V1`，选不在U中的二次单项式 `q=x_a x_b`，`A=U+span{q}`；由 `x_bx_i=ell_{bi}+c_iq`、乘 `x_a` 和 `q²=q` 得A为包含全部坐标的函数代数，坐标指示函数给 `A=R^S`。完整推导见开放义务页真实支持章节。
- Assumptions / Scope：真实有限正权支持和完整四阶矩是额外输入；不提供从普通P生成此分布或矩的算法。结论不适用于任意PSD/守恒伪矩，后者仍需共同交换延伸和V2负载localizer。
- Conclusion：真实支持量词下，rank-jump-one自动闭合共同交换投影并给位多项式原子提取；这不是一般UM近似算法。
- Dependencies：布尔函数代数、正权Gram秩等于支持函数空间维数、有理线性代数；不导入公屏 `4−2√2` 常数。
- Evidence：自足一般闭合证明；没有把有限枚举或公屏摘要当作伪矩反例/支持常数证明。
- Counterevidence / Objections：若只给C2-load伪矩，A未必为真实函数代数，CE与V2 localizer仍是proof obligations；从普通调度输入寻找真实矩也未解决。
- Status：complete stated-scope proof; internal independent reconstruction pending; external review and novelty unverified; UM-TARGET-v1 OPEN。
- Related Files：`research/questions/unrelated_machines/barrier_escape_obligations.md`；`research/current/unrelated_machines/global_assignment_moment_rounding.md`。
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

## UM-3DM-DEMAND-FLOOR-OBSTRUCTION-v1：三维匹配需求树的低比例地板

- **Exact Statement / Quantifiers：** 对任意 (qge1)、(Kge2) 及三维匹配 (A=(X,Y,Z,E)) 的标准需求树编码 (D_K(A))，令 (mu) 为 (X)--((Y\cup Z)) 一资源匹配数、(
u) 为三维匹配数，则 (b^*(D_K(A))=\max\{\min(\mu/q,1/K),\min(\nu/q,2/K)\})。完美三维匹配时 (b^*=2/K)。
- **Objects / Domain：** 根需求 (q)，(x) 点需求1，三元组点需求 (K)，(Y,Z) 为零需求终端；边 (r\to x\to e\to\{y,z\})；(b^*) 沿 `UM-DAG-DEGREE-TOKEN-IDENTITY-v1` 定义。
- **Scope / Conclusion：** 这是直接3DM需求树接口的精确方法障碍。提高 (K) 会同时降低 YES 的 (b^*)，固定 (K=2) 仍受一终端子树地板影响；故该接口不能给任意 (\varepsilon) 的 YES (b^*=1)/NO (b^*\le\varepsilon/2) 归约。公共资源 Hall 族给出可趋零的目标形状，但没有复杂度归约。
- **Dependencies：** `UM-DAG-DEGREE-TOKEN-IDENTITY-v1`；有限树单父约束；二分图/三维匹配定义。
- **Evidence：** 自足上下界证明；Fraction 审计覆盖 (q\le2) 全边集、(q=3) 固定种子随机样本和完美匹配族；见 `three_dimensional_matching_demand_floor_audit.json`。
- **Counterevidence / Objections：** 只排除该标准局部接口与公共资源样板；不排共享标签、高距离测试、Label-Cover 或其它跨模块一致性归约，也不证明主目标反面。
- **Status：** complete stated-scope obstruction; independently exact-audited; external review and novelty unverified; `UM-TARGET-v1` remains OPEN.
- **Related Files：** `research/current/unrelated_machines/three_dimensional_matching_demand_floor_obstruction.md`; `tests/audits/unrelated_machines/three_dimensional_matching_demand_floor.py`; `evidence/runs/unrelated_machines/three_dimensional_matching_demand_floor_audit.json`。


## UM-PDM-THRESHOLD-EXACT-v1：pDM 的整数阈值调度桥梁

- **Exact Statement / Quantifiers：** 对固定 d≥3、b>d 且 gcd(b,d)=1，d-dimensional matching 实例可在位多项式时间内转为整数受限 R∥Cmax：每个 incident 顶点任务在对应超边机器上耗时 b，dummy 任务在任意机器上耗时 d；存在完美匹配当且仅当 OPT≤bd，无完美匹配时 OPT≥bd+1。
- **Scope / Limitation：** 这是精确阈值/加一间隙，不是统一低于2乘性困难性；比率 (bd+1)/(bd)→1。它只说明 pDM 路线未经放大不能关闭 UM-TARGET-v1。
- **Related Files：** `research/current/unrelated_machines/pdm_threshold_scheduling_bridge.md`。

- **Counterevidence / Status（合入复核）：** 原正文未补m<n、isolated顶点、空源的合法UM分支；固定b的含义需明确。仅NO≥bd+1不限制NO上界，原“仅加一”限制说明已纠正。暂记条件性阈值内核，完整域修补需新版本；已有槽推论给合法编译的(1,1+1/d) promise过程。见`research/reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md`。

## UM-SANTA-NO-CONSTANT-CONDITIONAL-v1：Santa Claus 无常数近似假设下的条件反面

- **Exact Statement / Quantifiers：** 若 (P\ne NP) 且一般 Santa Claus 对每个固定常数 (c) 都无确定性多项式 (c)-近似，则不存在统一 (\varepsilon\in(0,1)) 的一般 R∥Cmax (2-\varepsilon) 算法。
- **Dependencies：** LST 的 (<3/2) 困难性；BLMRS Theorem 1 的 (2-1/\alpha) Makespan 到 (\alpha+\eta) Santa 转换。
- **Scope / Status：** 条件逻辑合成；SCHA 未证，不能升级为主目标无条件反面。
- **Related Files：** `research/current/unrelated_machines/santa_conditional_reverse_barrier.md`。

## UM-SANTA-NO-CONSTANT-CONDITIONAL-v2：Santa Claus 条件反面的量词与位复杂度规范化

- **Exact Statement / Quantifiers：** 定义 SCHA_det^N：对每个固定整数 c≥3，输入价值为二进制非负有理数的一般 Santa Claus 不存在确定性位多项式时间 c-近似（最大化方向 V≥OPT/c）。若 SCHA_det^N 成立，则不存在统一 ε∈(0,1) 的确定性位多项式 R∥Cmax 算法满足 Cmax≤(2−ε)OPT。对任意 ε 取固定 q≥max{2,⌈1/ε⌉}，BLMRS Theorem 1 将 (2−1/q) 算法转为 (q+η)-Santa 算法。
- **Scope / Status：** v1 的规范化版本；只涉及确定性、实际分配输出和二进制有理输入，不涉及随机/期望保证或仅估值算法。BLMRS 原文未完整展开位增长，固定参数下的有理缩放适用性仍列为 obligation；SCHA_det^N 未证，故不是无条件困难性。
- **Related Files：** `research/current/unrelated_machines/santa_conditional_reverse_barrier_v2.md`；v1 原始条件页保留供追溯。

## UM-K-UNIFORM-BUNDLE-FLOOR-v1：k-均匀资源束的分层匹配地板

- **Exact Statement / Quantifiers：** 对任意根需求 (q)、超边资源束大小至多 (k)、超边需求 (K) 的标准需求 DAG，令 (
u_t) 为每个选中超边取 (t) 个互不相交资源的最大束匹配数，则 (b^*=\max_{1\le t\le\min(k,K)}\min(\nu_t/q,t/K))。
- **Scope / Conclusion：** 直接局部资源束 gadget 的精确逃逸公式；三维匹配 (1/2) 地板是特例。近2 soundness 必须同时压低所有 (t)-层，不能只压低完整匹配。
- **Dependencies：** `UM-DAG-DEGREE-TOKEN-IDENTITY-v1`、树的单父约束和束匹配定义。
- **Evidence：** 自足上下界证明；Fraction 审计覆盖 (q=1) 全集合系统、(q=2) 固定种子随机系统及 (
u_1=q) 地板；见 `k_uniform_bundle_matching_floor_audit.json`。
- **Counterevidence / Objections：** 只限制该层状局部接口；不排共享标签、高距离编码或其它全局一致性归约，不证明主目标反面。
- **Status：** complete stated-scope obstruction; exact finite audit; external review and novelty unverified.
- **Related Files：** `research/current/unrelated_machines/k_uniform_bundle_matching_floor.md`; `tests/audits/unrelated_machines/k_uniform_bundle_matching_floor.py`; `evidence/runs/unrelated_machines/k_uniform_bundle_matching_floor_audit.json`。


## UM-BOUNDED-COLLISION-LABEL-FLOOR-v1：所选标签资源的有界碰撞比例地板

- Exact Statement / Quantifiers：∀显式四层r→X→E_x→R需求DAG，q=|X|≥1，d_r=q,d_x=1,d_e=K_e≥1,d_R=0、各E_x不交；∀给定每x一标签e_x及K_e个不同邻资源B_x，设Δ=max_u|{x:u∈B_x}|，有确定性总位多项式算法输出真实根树b(H)≥1/Δ；既有token桥梁给完整实际调度Cmax≤2−1/Δ。
- Objects / Domain：显式简单四层DAG、根需求q、变量需求1、标签正二进制整数需求、资源零需求；真实树包含所有选中正需求点的出度收费，标签节点按变量不交。
- Definitions：所选重数Δ、全局变量组关联度Δ_G及局部上界U分别按正文§1/§3a定义；空根/零度分支明列。
- Assumptions：无复杂度假设；总位长计输入与给定见证，巨大需求不按数值展开。
- Scope：低重数是给定选择的实际重数；未给寻找最小Δ的算法，不排高重数/跨层/一般归约。
- Conclusion：可构造真实树、实际调度或所述精确锐例；不是近二困难性或UM-TARGET-v1反面。
- Dependencies：UM-DAG-DEGREE-MODEL-v1；正文资源处单射着色/鸽巢与排序上界；UM-DAG-DEGREE-TOKEN-IDENTITY-v1仅用于实际调度翻译。
- Evidence：自足一般证明；statement-first独立U重构、冻结正文攻击；规范与不导入核心的原资源父点枚举及不同阈值构造，全部Fraction；范围见冻结记录。
- Counterevidence / Objections：R为空时max0与η>0的定义精度已修；未发现冻结范围内尚成立fatal；全球新颖性及外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified
- Related Files：research/current/unrelated_machines/bounded_collision_label_resource_floor.md；research/reviews/unrelated_machines/bounded_collision_label_floor_review.md；tests/audits/unrelated_machines/bounded_collision_bundle_floor.py；tests/audits/unrelated_machines/bounded_collision_bundle_independent.py；evidence/runs/unrelated_machines/bounded_collision_label_floor_audit.json；examples/unrelated_machines/pairwise_label_resource_floor.json。


## UM-PAIRWISE-LABEL-FLOOR-SHARP-v1：二重标签资源的逐束宽锐界

- Exact Statement / Quantifiers：∀k≥1，q=2s≥2个变量成对、每变量唯一需求k标签、同对共享恰k资源且不同对不交时，b*=1/2及token实例OPT=3/2。另∀Δ≥1，q=sΔ变量每Δ个共享同一singleton、标签需求1时b*=1/Δ、OPT=2−1/Δ。
- Objects / Domain：显式简单四层DAG、根需求q、变量需求1、标签正二进制整数需求、资源零需求；真实树包含所有选中正需求点的出度收费，标签节点按变量不交。
- Definitions：所选重数Δ、全局变量组关联度Δ_G及局部上界U分别按正文§1/§3a定义；空根/零度分支明列。
- Assumptions：无复杂度假设；总位长计输入与给定见证，巨大需求不按数值展开。
- Scope：Δ2对每个束宽锐；一般Δ只声称singleton通用锐性，不声称所有固定束宽1/Δ锐。
- Conclusion：可构造真实树、实际调度或所述精确锐例；不是近二困难性或UM-TARGET-v1反面。
- Dependencies：UM-DAG-DEGREE-MODEL-v1；正文资源处单射着色/鸽巢与排序上界；UM-DAG-DEGREE-TOKEN-IDENTITY-v1仅用于实际调度翻译。
- Evidence：自足一般证明；statement-first独立U重构、冻结正文攻击；规范与不导入核心的原资源父点枚举及不同阈值构造，全部Fraction；范围见冻结记录。
- Counterevidence / Objections：R为空时max0与η>0的定义精度已修；未发现冻结范围内尚成立fatal；全球新颖性及外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified
- Related Files：research/current/unrelated_machines/bounded_collision_label_resource_floor.md；research/reviews/unrelated_machines/bounded_collision_label_floor_review.md；tests/audits/unrelated_machines/bounded_collision_bundle_floor.py；tests/audits/unrelated_machines/bounded_collision_bundle_independent.py；evidence/runs/unrelated_machines/bounded_collision_label_floor_audit.json；examples/unrelated_machines/pairwise_label_resource_floor.json。


## UM-GROUP-DEGREE-LABEL-APPROX-v1：变量组关联度控制的真实根树与调度近似

- Exact Statement / Quantifiers：∀上述显式四层DAG，不要求局部完整；令Δ_G=max({0}∪{每资源涉及的不同变量组数})。q≥1且Δ_G≥1时，不给标签见证或b*，确定性总位多项式输出b(H)≥U/Δ_G≥b*/Δ_G，其中a_x=max_e min(1,|S_e|/K_e)、空max0、U=max_s min(s/q,a_(s))；token桥梁实际Cmax≤(2−1/Δ_G)OPT。q0根终端精确1；Δ_G0且q≥1精确b*=0。
- Objects / Domain：显式简单四层DAG、根需求q、变量需求1、标签正二进制整数需求、资源零需求；真实树包含所有选中正需求点的出度收费，标签节点按变量不交。
- Definitions：所选重数Δ、全局变量组关联度Δ_G及局部上界U分别按正文§1/§3a定义；空根/零度分支明列。
- Assumptions：无复杂度假设；总位长计输入与给定见证，巨大需求不按数值展开。
- Scope：Δ_G计不同变量组而非标签总入度；仅此四层桥梁族。Δ_G增长无统一ε；非一般UM逆表示。
- Conclusion：可构造真实树、实际调度或所述精确锐例；不是近二困难性或UM-TARGET-v1反面。
- Dependencies：UM-DAG-DEGREE-MODEL-v1；正文资源处单射着色/鸽巢与排序上界；UM-DAG-DEGREE-TOKEN-IDENTITY-v1仅用于实际调度翻译。
- Evidence：自足一般证明；statement-first独立U重构、冻结正文攻击；规范与不导入核心的原资源父点枚举及不同阈值构造，全部Fraction；范围见冻结记录。
- Counterevidence / Objections：R为空时max0与η>0的定义精度已修；未发现冻结范围内尚成立fatal；全球新颖性及外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified
- Related Files：research/current/unrelated_machines/bounded_collision_label_resource_floor.md；research/reviews/unrelated_machines/bounded_collision_label_floor_review.md；tests/audits/unrelated_machines/bounded_collision_bundle_floor.py；tests/audits/unrelated_machines/bounded_collision_bundle_independent.py；evidence/runs/unrelated_machines/bounded_collision_label_floor_audit.json；examples/unrelated_machines/pairwise_label_resource_floor.json。


## UM-LARGE-BUNDLE-COLLISION-FLOOR-v1：大需求标签束的有限碰撞界与平方池锐性

- Exact Statement / Quantifiers：∀q≥1显式完整束B_x、K_x=|B_x|、Δ为所选束实际资源重数、∀整数1≤c≤q，确定性总位多项式输出真实根树b≥Λ_c=min{ceil(q/c)/q,min_x floor(K_x c/(c+Δ−1))/K_x}。q=Δ=K_x=t²、标签邻域恰共同t²池且无额外边时，max_cΛ_c=b*=1/t（t≥2取c=t+1，t1取c1）。若b*≤η∈(0,1)，cη=ceil(1/η)−1，则Δ≥1+cη[1/(η+1/Kmin)−1]；沿η→0且ηKmin→∞必要liminfη²Δ≥1，平方池达到。
- Objects / Domain：四层r→x→私有标签e_x→终端资源，根需求q、变量1、所选标签需求K_x=显式束大小，允许原图其他标签/边；有限锐例单列禁止额外边。
- Definitions：Λ_c、整数同色碰撞势Ψ、容量配额匹配及cη按正文§1–6；每个原正需求点包括输出叶均收费。
- Assumptions：无复杂度假设；给定完整束选择承重，1≤Δ≤q；复杂度按显式关联及身份总位长。
- Scope：有限参数下界、平方池精确值和带η→0/大需求条件的必要量；不主张一般b*=maxΛ，不扩展到非完整束或一般UM逆表示。
- Conclusion：真实树和token实际调度≤2−Λ_c；近2归约中的高碰撞必要条件，不是一般困难性或主目标反面。
- Dependencies：UM-LABEL-RESOURCE-COLLISION-MODEL-v1、UM-DAG-DEGREE-MODEL-v1；自足整数缺陷着色势、Cauchy及容量Hall；UM-DAG-DEGREE-TOKEN-IDENTITY-v1用于实际调度。
- Evidence：独立statement-first重构；冻结正文攻击；规范与不导入核心的原资源父点oracle/不同重染色和Hall子集审计；实际树、调度、逐机回算及零比例分支。
- Counterevidence / Objections：已明确有限锐例不得额外资源边、ε渐近必须ε→0；无尚成立fatal。singleton阻止无大需求的平方改善；高碰撞本身不证明NO，新颖性未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified
- Related Files：research/current/unrelated_machines/large_bundle_collision_square_root_floor.md；research/reviews/unrelated_machines/large_bundle_collision_floor_review.md；tests/audits/unrelated_machines/large_bundle_collision_floor.py；tests/audits/unrelated_machines/large_bundle_collision_independent.py；evidence/runs/unrelated_machines/large_bundle_collision_square_root_audit.json。

## UM-C2-LOAD-UNIT-GAP-v1：单位任务全局四阶负载松弛的锐利二间隙

- Exact Statement / Quantifiers：对每个整数m≥3，n=m+1个全单位同机任务的现行C2-load阈值恰为t=n/m，而整数OPT=2；兼容四阶矩y_S=∏a(t)_{c_a(S)}/(n)_{|S|}给显式有理证书，M2半正定且全部负载localizer为0。比值2m/(m+1)趋2；一般此C2松弛的supgap恰为2。
- Objects / Domain：一般UM模型的全局one-hot四阶M2 PSD、次数一负载localizer、端剪枝合同；下界族m≥3、n=m+1、p_ij=1、T=(m+1)/m。
- Definitions / Assumptions：不含逐条三阶非负、CONFIG或prefix-count localizer；(z)_k为下降阶乘，c_a为相容单项式中的机器a次数。证书总编码长度为输入位长多项式。
- Scope / Conclusion：回答裸C2-load本身的全称阈值舍入义务；不是指定贪心坏例，也不是所有矩方法/一般调度算法的困难性。
- Dependencies：UM-MODEL-v1；正文自足count-null与对称/反对称harmonic代数；supgap≤2另依赖UM-ST-ROUND-v1。
- Evidence：自足全m证明；statement-first独立更一般slice重构与冻结攻击；规范Fraction完整M2核m=3,4,5，独立整数Bareiss核m=3,4，并独立攻击m=2。
- Counterevidence / Objections：m=2失败，已给负平方；本族三阶同机矩为−1/m^4，另加三阶非负即排该证书；CONFIG阈值为2，不能声称C2+CONFIG间隙。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。UM-TARGET-v1保持OPEN。
- Related Files：research/current/unrelated_machines/c2_unit_multislice_gap.md；research/reviews/unrelated_machines/c2_unit_multislice_gap_review.md；tests/audits/unrelated_machines/c2_unit_multislice_gap.py；tests/audits/unrelated_machines/c2_unit_multislice_independent.py；evidence/runs/unrelated_machines/c2_unit_multislice_gap_audit.json；examples/unrelated_machines/c2_unit_multislice_m3.json；evidence/certificates/unrelated_machines/c2_unit_multislice_m3.json。

## 闭环弱单调修复与异端共同容量的新准确身份

### UM-OPT-HULL-CLOSED-CYCLE-WEAK-LOCAL-GAP-v1：真最优凸包槽初始化后的弱最大负载闭环邻域锐界

- Exact Statement / Quantifiers：∀整数k≥3,d≥1，§11的显式正有理两选实例满足T=OPT=1、所有有限边≤1；x为两个实际最优调度的正有理凸组合。任意逐机等尺寸平局排序下，标准有序单位槽的全部最小总处理时间覆盖匹配诱导同一σ，Cmax(σ)=B_k=2−3/k+3/(2k²)。任意不同于σ且Cmax(τ)≤B_k的合法τ，改变原任务数及其新旧机器端点并集大小分别至少d+1；同一严格下降动作同时达到两界。
- Objects / Domain / Definitions：UM-MODEL-v1；正文§11显式k,d环、Hamming改件、全部新旧端点和路径峰值。
- Assumptions / Scope：仅固定σ的小支持弱最大负载单调修复及本显式族单任务路径；不排无界同步动作、微小暂时增载、换初始化或一般算法。机器图为cactus，可由已有块算法精确解。
- Conclusion：真最优凸包槽初始化后的弱最大负载闭环邻域锐界；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1、ST单位槽定义与本稿显式环构造；逃逸阈值另依赖同一B和首步分类。
- Evidence：完整自足推导、先声明后冻结独立攻击、精确逐件输入/输出与双路以上有限核验；详细范围在冻结结果。
- Counterevidence / Objections：声明范围未发现尚成立fatal；暂时超额仅c=1/k²即能逐件到OPT，不能推固定正势垒或一般复杂度困难性。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。软件为显式族构造/审计，不是通用修复器。
- Related Files：`research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md`；`research/reviews/unrelated_machines/optimal_hull_closed_cycle_review.md`；`evidence/runs/unrelated_machines/optimal_hull_closed_cycle_audit.json`。

### UM-CLOSED-CYCLE-SINGLE-JOB-ESCAPE-THRESHOLD-v1：闭环族单任务最优逃逸路径的精确临时超额

- Exact Statement / Quantifiers：∀上述k,d及同一σ，在所有从σ出发、终点满足Cmax=1的有限单任务合法迁移路径中，最小可能路径最大负载精确为B_k+c，其中c=1/k²；显式(k−1)(d+1)步路径达到该值。所有非平凡单任务首步峰值至少B_k+c，故下界不要求中间单调。
- Objects / Domain / Definitions：UM-MODEL-v1；正文§11显式k,d环、Hamming改件、全部新旧端点和路径峰值。
- Assumptions / Scope：仅固定σ的小支持弱最大负载单调修复及本显式族单任务路径；不排无界同步动作、微小暂时增载、换初始化或一般算法。机器图为cactus，可由已有块算法精确解。
- Conclusion：闭环族单任务最优逃逸路径的精确临时超额；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1、ST单位槽定义与本稿显式环构造；逃逸阈值另依赖同一B和首步分类。
- Evidence：完整自足推导、先声明后冻结独立攻击、精确逐件输入/输出与双路以上有限核验；详细范围在冻结结果。
- Counterevidence / Objections：声明范围未发现尚成立fatal；暂时超额仅c=1/k²即能逐件到OPT，不能推固定正势垒或一般复杂度困难性。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。软件为显式族构造/审计，不是通用修复器。
- Related Files：`research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md`；`research/reviews/unrelated_machines/optimal_hull_closed_cycle_review.md`；`evidence/runs/unrelated_machines/optimal_hull_closed_cycle_audit.json`。

### UM-DISTORTED-GROUP-JOINT-SLOT-v1：组内异端有界畸变的共同出口槽阈值舍入

- Exact Statement / Quantifiers：∀显式不交H∪Z、宏B与唯一home私有组J_h；组内共同E_h，home时间w_j，给有理0≤δ<1/2、κ≥1、B̄≥0、0≤b_hz≤B̄，满足(b_hz/κ)w_j≤p_zj≤b_hz w_j。∀有理T≥0、1/2≤r<1−δ，若W_h≤T、w_j≤δT且全部有限宏端>T/2，则有确定性总位多项式算法返回FAIL或实际完整σ，home≤(1+r+δ)T、sink≤[κ+B̄(1−r)]T，OPT≤T必成功。
- Objects / Domain / Definitions：UM-MODEL-v1；正文§1–2的H/Z、B/J_h、上下包络、d_h=(W_h−rT)_+及c_hz=b_hz d_h。
- Assumptions / Scope：唯一home、共同资格、输入给定包络、小私有任务、宏大边承重；接收机数不固定。不是一般矩阵分解器或一般UM算法。
- Conclusion：组内异端有界畸变的共同出口槽阈值舍入；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1、标准有理LP可解性、整数流、ST有序槽；真实出口上下包络及前缀恢复由正文自证。
- Evidence：完整自足推导、先声明后冻结独立攻击、精确逐件输入/输出与双路以上有限核验；详细范围在冻结结果。
- Counterevidence / Objections：声明范围未发现尚成立fatal；缺少下包络无法保证LP必要性，缺少上包络/共同资格无法恢复选定前缀；一般结构提取仍未解。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。数学算法完整；软件只实现给定精确LP见证的验证/舍入，通用LP后端及未知OPT端到端未实现。
- Related Files：`research/current/unrelated_machines/distorted_group_joint_slot_rounding.md`；`research/reviews/unrelated_machines/distorted_group_joint_slot_review.md`；`evidence/runs/unrelated_machines/distorted_group_joint_slot_audit.json`。

### UM-DISTORTED-GROUP-PROMISE-APPROX-v1：异端有界畸变结构的未知最优值实际近似

- Exact Statement / Quantifiers：∀同一显式包络结构及有理参数，不给OPT；承诺在真实OPT处W_h≤OPT、w_j≤δOPT、全部有限宏端>OPT/2，则确定性总位多项式算法输出Cmax≤α(r)OPT的实际完整调度，α=max(1+r+δ,κ+B̄(1−r))，含空任务/OPT0。固定δ,κ,B̄满足κ+B̄δ<2时取r*=max(1/2,(κ+B̄−1−δ)/(1+B̄))，有本结构类统一α(r*)<2；参数趋边界时不声称统一余量。
- Objects / Domain / Definitions：UM-MODEL-v1；正文§1–2的H/Z、B/J_h、上下包络、d_h=(W_h−rT)_+及c_hz=b_hz d_h。
- Assumptions / Scope：唯一home、共同资格、输入给定包络、小私有任务、宏大边承重；接收机数不固定。不是一般矩阵分解器或一般UM算法。
- Conclusion：异端有界畸变结构的未知最优值实际近似；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1、标准有理LP可解性、整数流、ST有序槽；真实出口上下包络及前缀恢复由正文自证。
- Evidence：完整自足推导、先声明后冻结独立攻击、精确逐件输入/输出与双路以上有限核验；详细范围在冻结结果。
- Counterevidence / Objections：声明范围未发现尚成立fatal；缺少下包络无法保证LP必要性，缺少上包络/共同资格无法恢复选定前缀；一般结构提取仍未解。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。数学算法完整；软件只实现给定精确LP见证的验证/舍入，通用LP后端及未知OPT端到端未实现。
- Related Files：`research/current/unrelated_machines/distorted_group_joint_slot_rounding.md`；`research/reviews/unrelated_machines/distorted_group_joint_slot_review.md`；`evidence/runs/unrelated_machines/distorted_group_joint_slot_audit.json`。

## UM-HETEROGENEOUS-MACRO-ARBITRARY-TINY-v1：异质大宏与任意 tiny 资格的统一残余容量

- **Exact Statement / Quantifiers：** 给定 `|B|=|H|`、宏仅在 `H`、每条有限宏边 `T/2<p_{hb}≤T`，每条有限 tiny 边 `p_{ij}≤δT` 且固定 `δ<1/2`。若 `OPT≤T`，任取宏完美匹配；在 home 容量 `T/2`、sink 容量 `T` 的 tiny LST LP 上做 ST 舍入，得到实际 `Cmax≤(3/2+δ)T`。
- **Scope / Conclusion：** tiny 资格和端成本完全逐件任意；宏时间可依赖 `(h,b)`。这是给定结构接口，不是一般输入算法。
- **Dependencies / Evidence：** `UM-MODEL-v1`、`UM-ST-ROUND-v1`；正文和 Fraction 审计见 `research/current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md`、`tests/audits/unrelated_machines/heterogeneous_macro_uniform_residual.py`。
- **Status：** complete stated-scope proof; internally blind-reconstructed and exactly audited; external review and novelty unverified; `UM-TARGET-v1` remains OPEN。

## UM-HETEROGENEOUS-MACRO-PROMISE-v1：异质大宏承诺类未知 OPT 搜索

- **Exact Statement / Quantifiers：** 同拓扑不给 `T`，promise 在真实 `OPT` 处所有有限宏边 `>OPT/2`、tiny 边 `≤δ̄OPT`（固定 `δ̄<1/2`）。保留全部 tiny 边的单调谓词 `F(t)` 用所有有限边分母乘积 `Q` 的整数区间 `[0,QU]` 二分，输出实际 `Cmax≤(3/2+δ̄)OPT`。
- **Scope / Conclusion：** 先精确处理 `OPT=0`；二分次数按 `log(QU)` 计。分层 promise 不从一般矩阵免费识别。
- **Dependencies / Evidence：** 依赖上一 Claim；未知 OPT 的单调性和位复杂度见同一正文第 2 节及其独立审查。
- **Status：** complete stated-scope proof; internally reconstructed; external review and novelty unverified; `UM-TARGET-v1` remains OPEN。

## UM-HETERO-TINY-3PARTITION-FLOW-BARRIER-v1：异质 tiny 精确流障碍

- **Exact Statement / Quantifiers：** 对任意固定 `δ>0`，强 3-PARTITION 可缩放到所有 tiny 边 `≤δT` 的残余阈值实例；`T`-可行整数调度当且仅当 3-partition，而均匀分数 LP 始终可行。
- **Scope / Conclusion：** 只否定把异质接收成本精确化为普通整数流/简单可积多面体；不否定带 ST 加性余量的正面候选，也不是近 2 困难性。
- **Evidence：** 缩放构造在 `heterogeneous_macro_uniform_residual_st_rounding.md` 边界段；内部 `B=13` 小例和 Fraction 核验已重算。
- **Status：** complete stated-scope obstruction; internal attack and exact arithmetic checked; external review and novelty unverified。

## UM-STRICT-SUB2-BATCH-BARRIER-v1：严格次二状态图的批量能垒

- **Exact Statement / Quantifiers：** 对每个 `k≥2` 存在 `OPT=1` 实例和 `Cmax<2` 坏态；允许每步至多 `k` 件迁移且全部中间态保持严格 `<2` 时，坏态孤立，首个出口需 `k+1` 件。进一步，对每个 `ε∈(0,1)` 和每个固定支持预算 `r≥1`，取整数 `k>max{r,1/(8ε)}`，同一族坏态负载 `2−1/(8k)>2−ε`，任何每步至多 `r` 件且全程严格 `<2` 的局部合同都不能达到目标 `2−ε`。
- **Scope / Conclusion：** 只限制常数批量、严格次二局部修复；它给出对任意固定 `ε` 的 `Ω(1/ε)` 同步动作需求。允许无界批量、跨过 2 或重新求解时不适用，不是一般近似困难性。
- **Evidence / Status：** `research/current/unrelated_machines/strict_sub2_batch_barrier.md`；`tests/audits/unrelated_machines/strict_sub2_batch_barrier.py`；基础 Fraction 审计 `k=2,3,7,100` 及固定 ε 参数化审计 `ε∈{1/100,1/50,1/20,1/19}` 通过；有限审计不替代一般证明，外审/新颖性未认证。


## UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1：单任务外接端口投影的锐计数与复制障碍

- Exact Statement：内部机器非空、辅助任务仅内部、每端口恰一个内部端点及一个固定外端、时间非负有理；投影R_T完全排除外部容量。其局部入向位像向下闭。若全0与全1均可行，a0=#符号0，则|R_T|≥2^a0+2^(k−a0)−1≥2^floor(k/2)+2^ceil(k/2)−1。令z=#零时间端口，a,b为正时间两符号数，则|R_T|≥2^z(2^a+2^b−1)，任意T>0/a,b,z有锐例；T0且两一致态可行时全cube。
- Objects：UM-MODEL-v1的真实任务、内部/外部机器划分、状态独立辅助任务和signed single-job ports。
- Domain：显式有限图，非负有理处理时间及T；辅助任务可有任意非空有限内部资格。端口另一端外接但其容量不在投影。
- Quantifiers：∀上述输入；计数以两一致态可行为前提；∀k≥2、ρ≥1弱投影不能仅保留等值。给定两个具体一致见证可总位多项式构造单翻位混合内部见证，不求解未知辅助分配。
- Assumptions / Definitions：R_T由正文式(1)的全部内部容量及辅助分配存在性定义；global x=s为入向。零时间位自由，正时间两一致态支持互补。
- Scope：只否定single-job/free-external-occurrence的纯内部等值复制；多任务编码、外部联合容量、联合源/一致性机器或非等值解码不在否定范围。
- Conclusion：复制端口的精确状态计数及两机器达到例；一般signed-threshold PCSP源困难性尚缺次数保真接口，不能直接导成UM困难性。
- Dependencies：UM-MODEL-v1、非负容量单调性及布尔主理想计数；BG2016 Theorem1.3只作第5节独立源定理对照，不是本计数证明前提。
- Evidence：完整自足证明、先仅statement独立重构再冻结全文攻击、两套不互相import的Fraction实际辅助分配核验及明确外部私有host完整σ。
- Counterevidence / Objections：双内部端点或把外部共同容量加回时2任务2机能实现等值至ρ<2；这是排除假设的必要负控，不是本Claim反例。零阈值前提、未知见证可求性与实ρ阈值定义已明确。无声明范围内尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; global novelty and standalone publication value unverified。实现为已给见证的混合构造及有限审计，不是一般调度求解器。
- Related Files：`research/current/unrelated_machines/signed_one_job_port_downset.md`；`research/reviews/unrelated_machines/signed_one_job_port_downset_review.md`；`evidence/runs/unrelated_machines/signed_one_job_port_downset_audit.json`。

## UM-THREE-HOST-SELECTOR-THREE-HALVES-v1：三外接机器可用性选择器的锐三半逃逸

- Exact Statement：对任意内部机器及三不同外host a,b,c，基础任务/资格固定，非负二进制有理时间，阈值T≥0；blocked host加不可迁移预载T且原边仍可用，free预载0，内部无额外预载。若only-a和b+c-free各有实际完整总C≤T调度，则only-b或only-c至少一侧有实际完整C≤3T/2调度。给两YES可确定性总位多项式输出该侧、全部σ及负载，系数每T>0精确锐。
- Objects：UM-MODEL-v1真实不可拆分任务、固定外接空/满预载、两已给实际YES；全体机器逐台总负载。
- Domain：显式有限输入，任意多可用边、零/空/单可用及T0；m≥3由三不同host保证。
- Quantifiers：∀上述输入和两实际YES；∃由明确算法输出的坏侧完整σ；∀T>0有两任务sharp。
- Assumptions / Definitions：两完整见证实际给定；所有权非负；正文第1或第5节定义的外部可用性状态。满预载的有限任务边不被删除；物品分配不复制物品。
- Scope：独立空/满预载读出承重；不排状态相关资格、任意共同外部任务或不可私有化的跨模块残余容量，不求未知YES。
- Conclusion / Mechanism：按S1源机→S2目的机、S1端时间造非负行权，固定b1/c0只0→1闭包；W取a色类，原任务两dest均在W才用S2。W外保持S1；W内S2进入子集与S1跨出保留负载分别≤T及T/2；三host预载逐台加入。
- Dependencies：正文自足二色非负行权闭包；调度模型和本页明确两YES接口定义。BCG§7仅作既有接口对照，不依赖CCK/CONFIG/NP-hardness。
- Evidence：规范构造、独立SC补集构造、独立全矩阵最优值oracle及实际规范σ逐台核验。 先陈述攻击/读后攻击真实来源见review；有限输出不代替一般证明。
- Counterevidence / Objections：W内必须分别按真实两端时间计费，blocked零负载不等于无任务；SC来源方向与调度不同。直接平均/任意外部context不提供本合同之外结论。声明范围无尚成立fatal；全球新颖性未认证。
- Status：complete stated-scope proof; internally attacked and exact finite audited; implementation for given actual witnesses; external review and standalone publication value unverified。UM-TARGET-v1保持OPEN。
- Related Files：`research/current/unrelated_machines/three_host_selector_sharp_three_halves.md`；`research/reviews/unrelated_machines/three_host_majority_selector_review.md`；`evidence/runs/unrelated_machines/three_host_selector_majority_audit.json`。

## UM-TWO-YES-SC-DUPLICATION-HALF-v1：三物品可用性复制的无条件锐半值

- Exact Statement：至少一参与者的一般非负有理加性Santa Claus，普通物品始终可用、三不同特殊item A,B,C；ordinary+A和ordinary+B+C各有minvalue≥1实际分配，则ordinary+B或ordinary+C至少一侧有minvalue≥1/2实际分配。给两YES可确定性总位多项式输出；特殊及ordinary正度任意，half由单agent数值1,1/2,1/2锐。
- Objects：真实可闲置单件物品、加性效用、三特殊可用性状态、两具体YES allocation。
- Domain：至少一agent、有限显式非负有理values，普通可空、zero/unused允许、B/C同recipient允许，无正度上界。
- Quantifiers：∀上述输入/两实际YES，∃算法输出bad可用侧和逐件allocation；无P≠NP假设。
- Assumptions / Definitions：两完整见证实际给定；所有权非负；正文第1或第5节定义的外部可用性状态。满预载的有限任务边不被删除；物品分配不复制物品。
- Scope：只限制明确三特殊item可用性复制，不是任意Santa Claus实例常数算法，不能把效用半值直接当一般调度负载。
- Conclusion / Mechanism：补齐S1普通正物品来源，按S2接受者行及S1来源列造效用权；固定B/C来源二色闭包，W取A原recipient色类。W外保S1满值、W内得S2至少半值，逐item唯一分配。
- Dependencies：正文自足二色非负行权闭包；调度模型和本页明确两YES接口定义。BCG§7仅作既有接口对照，不依赖CCK/CONFIG/NP-hardness。
- Evidence：独立SC任意正度穷举/随机与退化回算；actual脚本明确不声称同时核SC。 先陈述攻击/读后攻击真实来源见review；有限输出不代替一般证明。
- Counterevidence / Objections：W内必须分别按真实两端时间计费，blocked零负载不等于无任务；SC来源方向与调度不同。直接平均/任意外部context不提供本合同之外结论。声明范围无尚成立fatal；全球新颖性未认证。
- Status：complete stated-scope proof; internally attacked and exact finite audited; implementation for given actual witnesses; external review and standalone publication value unverified。UM-TARGET-v1保持OPEN。
- Related Files：`research/current/unrelated_machines/three_host_selector_sharp_three_halves.md`；`research/reviews/unrelated_machines/three_host_majority_selector_review.md`；`evidence/runs/unrelated_machines/three_host_selector_majority_audit.json`。

## UM-SANTA-RESTRICTED-BRIDGE-BOUNDARY-v1：restricted Santa 与需求树桥梁的模型边界

- **Exact Statement / Quantifiers：** token桥梁中若存在正需求 (k_v>1) 且 (d_v>0)，同一外送任务在父/子端非零时间为 (1/k_v,1)，不满足 restricted Santa 的 (v_{ci}\in\{0,p_i\})；只有所有正需求为1时退化到restricted支持，此时正点只表达出度0/1层。
- **Scope / Conclusion：** Haeupler–Saha–Srinivasan 的常数结果只属restricted模型；一般桥梁与restricted不保真。
- **Related Files：** `research/current/unrelated_machines/santa_restricted_bridge_boundary.md`。

## UM-DUPLICATION-TWO-COPY-FLOOR-v1：两份完整复制的一半一致性地板

- **Exact Statement / Quantifiers：** 每变量两标签、每标签完整束 (B_x^a)，且每一副本内部束两两不交、根需求为变量数时，资源二着色和较大颜色类选择给确定性真实根树 (b(H)\ge1/2)，从而简单duplication不能给 (b^*\le\delta<1/2) 的NO侧。根需求改为 (Q) 时保证为 (|X|/(2Q))。
- **Scope / Conclusion：** 两复制地板是 `UM-BOUNDED-COLLISION-LABEL-FLOOR-v1` 的专门推论；不排跨层共享或非内部不交的一致性构造。
- **Related Files：** `research/current/unrelated_machines/duplication_two_copy_floor.md`。

## UM-DUPLICATION-STATE-MAJORITY-FLOOR-v1：两状态残余的多数状态地板

- **Exact Statement / Quantifiers：** 两状态标签束各自内部不交；对保留变量Y和任意δ，令G_a(δ)={x:|R_x^a|≥δK_x^a}。若G_0∪G_1非空，选较大状态给真实根树 (b(H)\ge\min\{|G_0\cup G_1|/(2q_r),\delta\})；根需求同步为|Y|且每变量有一好状态时得 (min\{1/2,delta\})。
- **Scope / Conclusion：** 允许任意删叶/删变量但保留状态内不交；行列池在K≥2s时达到 (min\{1/2,s/K\})。这是两复制地板的δ-sharpen，不是一般硬度。
- **Evidence / Related Files：** `research/current/unrelated_machines/duplication_state_majority_floor.md`; `tests/audits/unrelated_machines/robust_consistency_state_majority.py`; `evidence/runs/unrelated_machines/robust_consistency_state_majority_audit.json`。


## UM-COMMON-SIZE-REOPEN-v1：共同尺寸微任务的可重开容量流

- Exact Statement / Quantifiers：给定冻结核心分配 `σ₀`、核心负载 `f_i`、目标 `B` 和残余任务 `U`；每个残余任务在资格边上处理时间为同一 `q_j`。若存在有理流 `x` 列和为1且 `Σ_j q_jx_ij≤B−f_i−q_max`，则有序槽在位多项式时间内输出完整整任务分配并保持所有负载≤B；更精确地，给定流满足 `Σ_jq_jx_ij+r_i(x)≤B−f_i` 时同样成立。若每个支持连通分量内 `q_j` 相同，整数槽位最大流给无加性损失的可重开修复。
- Objects / Domain / Definitions：显式非负二进制有理处理矩、资格边、冻结核心与残余容量；允许接收机增载；一般可分流判定的 Farkas 条件为 `Σ_iλ_ib_i≥Σ_j min_i λ_ip_ij`。
- Assumptions / Scope：这是给定核心/流证书的 repair 接口，不是从一般矩阵选择核心或整流的通用算法；异端处理时间和不同尺寸共享机器仍有整数装箱缺口。
- Conclusion：共同尺寸条件下，一次联合流和有序槽整化同时决定所有接收端；单位尺寸连通分量用普通整数最大流精确恢复；失败时分数 LP 对偶或最小割给共同容量阻塞证书。
- Dependencies：UM-MODEL-v1；Shmoys–Tardos 有序槽舍入；有理 LP/Farkas 对偶；正文与独立 Fraction 审计见 `common_size_reopen_capacity_flow.md`。
- Evidence：两机三任务 `q=2,b=(3,3)` 分数负载为3但整数最优峰值4；异端矩阵 `[[2,100,2],[100,2,2]]` 反驳按任务最小值建流；给定 headroom 证书例由 Fraction 核验。
- Counterevidence / Objections：`q_max` 头部余量可能回到经典二倍；寻找满足头部条件的支持流仍是离散共同选择；不产生一般 `UM-TARGET-v1` 的统一 ε。
- Status：complete stated-scope interface; independently reconstructed and exactly audited; unrefereed; novelty unverified。
- Related Files：`research/current/unrelated_machines/common_size_reopen_capacity_flow.md`；`research/reviews/unrelated_machines/common_size_reopen_capacity_flow_review.md`；`tests/audits/unrelated_machines/common_size_reopen_capacity_flow.py`；`evidence/runs/unrelated_machines/common_size_reopen_capacity_flow_audit.json`。

## UM-TWO-STATE-POOL-EXACT-FRONTIER-v1：两状态残余行列池的精确整数前沿

- Exact Statement：对每个整数K≥s≥1，显式s×s资源池、2s变量、根需求2s、变量需求1、各标签原需求K；前s变量仅状态0行标签非空，后s仅状态1列标签非空，其余标签残余出度零。所有真实树的最优b*=max_{1≤k≤2s} min{k/(2s),h_k/K}，h_k=min{s,floor(s²/k)}；可总位多项式求值并输出达到树。
- Objects：真实根树、原需求、可裁剪标签孩子、每资源唯一父亲；不是整束冲突独立集。
- Domain：有限显式残余DAG和二进制正整数K，K可远大于度；允许根单点和正需求输出叶，均按定义收费。
- Quantifiers：∀K≥s≥1，∀真实树成立上界；∀k有达到h_k的实际配额分配；∃算法输出达到最优的真实树。
- Assumptions / Definitions：本正文行列池中没有额外资源/边；部分标签束合法、资源不复用；原空标签不免除其正需求。
- Scope：只解此残余池参数族，主多数下界保持原量词；不声称一般双状态实例可精确解。
- Conclusion：s=K=4真b*=5/8>旧声称1/2；K≥2s则b*=s/K，原K8/16/32三例保留。撤回旧全K≥s锐性，未撤回多数下界。
- Dependencies：明确残余行列池定义；资源计数上界和自足循环构造。独立Hall重构只提供另一证明，不是有限审计的替代。
- Evidence：两名内部研究者分别重构Hall最强子集和资源计数/循环构造；root亲核真实26点25边树及两代码实际运行。
- Counterevidence / Objections：整束不能共选推理错误，实际孩子可拆分资源选择；s1时h_2=0仍收正标签需求；不展开数值K；均在规范正文与审查处理。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；求值/实际循环构造有实现，指数matching仅审计，不冒称通用tree solver或一般UM困难性。
- Related Files：`research/current/unrelated_machines/duplication_state_majority_floor.md`、`research/reviews/unrelated_machines/two_state_pool_partial_resource_review.md`、`examples/unrelated_machines/two_state_pool_partial_tree_counterexample.json`、`evidence/runs/unrelated_machines/two_state_pool_exact_frontier_audit.json`。

## UM-WEIGHTED-FANOUT-PROFILE-BOUNDARY-v1：多输出两YES接口的加权构造与真实OPT总预算

- Exact Statement：q≥2个输出B、输入a及任意内部机器，基础时间/资格固定、非负二进制有理数；关闭host加不可迁移T，原有限边仍可用。给only-a与all-B-free两实际C≤T调度，对每K⊆B,k≥2和每显式有理β≥0,sum1，实际输出某i∈K状态blocked=a∪(K\{i})的完整σ，C≤(2−β_i)T。真实最优μ_{K,i}之和≤(2k−1)T，加权星整个面精确取等。
- Objects：真实不可拆分任务、原有限资格、独立空/满预载、两已给实际YES；所有机器共同最终负载。
- Domain：有限显式非负有理处理矩阵与T≥0；任意额外资格、空任务、零时间、单可用任务、任意内部规模；q+1个互异hosts为定义前提。
- Quantifiers：∀上述输入/两实际YES，∀K/β；∃deterministic总位poly完整输出。∀k≥2,T>0有加权星等号。
- Assumptions / Definitions：正文P_{K,i}、μ与ν均为同一固定基础实例的实际整数状态；预载是不可迁移真实任务；关闭不删边，状态不改变基础工作。
- Scope：仅上述给实际见证的独立预载接口；不搜索未知YES，不排跨模块联合外部容量或不同编码。
- Conclusion / Mechanism：非负行权顺序加权闭包；原S1源时间与S2接收时间分开计费；μ仅在存在性反证使用，非算法oracle。
- Dependencies：UM-MODEL-v1与明确多输出两YES模型；正文自足加权行权分割/实际拼接；缺一结论另用加权预算，不依赖外部近似或困难性。
- Evidence：uniform先陈述独立重构、weighted独立提出/重构、最终全文hash攻击、两份互不import规范的实际程序和原矩阵所有状态oracle；一般证明与有限检查分开。
- Counterevidence / Objections：不能将至多一个缺一大于三半升级为全部≤三半；正文5/4,7/4,1反例。β零权、T0逻辑状态、原两端不同时间及unknownμ不作oracle均已核。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；给两YES实际构造已实现；外审/独立论文价值未认证，UM-TARGET-v1及一般反面仍OPEN。
- Related Files：`research/current/unrelated_machines/weighted_fanout_profile_boundary.md`、`research/reviews/unrelated_machines/weighted_fanout_profile_boundary_review.md`、`evidence/runs/unrelated_machines/weighted_fanout_profile_boundary_audit.json`、`examples/unrelated_machines/weighted_fanout_profile_star.json`。

## UM-FANOUT-MISSING-ONE-THREE-HALVES-v1：任意扇出缺一状态的两两三半锐预算

- Exact Statement：同一接口下，ν_i为关闭a及b_i、其余输出free的真实OPT。任意u≠v有ν_u+ν_v≤3T，给u/v可实际构造其中之一C≤1.5T，至多一个ν_i>1.5T，且Σν_i≤1.5qT。每q≥2,T>0有degree2满二叉树使全部ν_i=1.5T，同时精确锐。
- Objects：真实不可拆分任务、原有限资格、独立空/满预载、两已给实际YES；所有机器共同最终负载。
- Domain：有限显式非负有理处理矩阵与T≥0；任意额外资格、空任务、零时间、单可用任务、任意内部规模；q+1个互异hosts为定义前提。
- Quantifiers：∀同一输入，∀输出对u≠v；∃该对中具体三半σ。∀q≥2,T>0有全部缺一状态同时锐例。
- Assumptions / Definitions：正文P_{K,i}、μ与ν均为同一固定基础实例的实际整数状态；预载是不可迁移真实任务；关闭不删边，状态不改变基础工作。
- Scope：仅上述给实际见证的独立预载接口；不搜索未知YES，不排跨模块联合外部容量或不同编码。
- Conclusion / Mechanism：把K外输出撤预载视内部，K2预算；满二叉树根=a的严格强制传播下界及单边上移达到。
- Dependencies：UM-MODEL-v1与明确多输出两YES模型；正文自足加权行权分割/实际拼接；缺一结论另用加权预算，不依赖外部近似或困难性。
- Evidence：uniform先陈述独立重构、weighted独立提出/重构、最终全文hash攻击、两份互不import规范的实际程序和原矩阵所有状态oracle；一般证明与有限检查分开。
- Counterevidence / Objections：不能将至多一个缺一大于三半升级为全部≤三半；正文5/4,7/4,1反例。β零权、T0逻辑状态、原两端不同时间及unknownμ不作oracle均已核。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；给两YES实际构造已实现；外审/独立论文价值未认证，UM-TARGET-v1及一般反面仍OPEN。
- Related Files：`research/current/unrelated_machines/weighted_fanout_profile_boundary.md`、`research/reviews/unrelated_machines/weighted_fanout_profile_boundary_review.md`、`evidence/runs/unrelated_machines/weighted_fanout_profile_boundary_audit.json`、`examples/unrelated_machines/weighted_fanout_profile_star.json`。

## UM-NORMALIZED-DUAL-RAIL-UNIVERSAL-THREE-HALVES-v1：归一化双轨全类的实际三半界

- Exact Statement：每变量两私有轨、selector两端时间1；每真实occurrence内部1/K(v,s)、外部单clause时间1/A_c，A_c≥1且arity≤2A_c−1。无额外jobs/预载/资格。任意源公式均可总位poly输出全σ且C≤3/2；存在selector时给本类3/2近似。10机15job重复occurrence例真实OPT=3/2，锐性仅为绝对T1界。
- Objects / Definitions：正文该ID自己的真实成本模型，所有port为不可拆分occurrence，所有机器共同实际负载，非抽象token目标。
- Domain：明确显式输入、二进制整数/有理时间；没有声明之外资格/背景job；空任务添dummy，K0不除零；重复occurrence合法。
- Quantifiers：∀显式变量/occurrence、各binary A_c；K可0且不平衡。无需SAT/OPT证书；∃确定性位poly实际构造。
- Assumptions：必须使用该段成本、arity与指定证书，四合同不互换。
- Scope：仅上述具体编码、构造及sharp实例；未证明一般UM-TARGET-v1正反面，也未给一般近二NP困难性。
- Conclusion / Mechanism：ST半质量有序槽直接推论；联合quarter流为另一实现，不主张新算法。
- Dependencies：UM-MODEL-v1及正文独立定义；scalar用经典ST半质量直接推论，其他采用自足整数匹配/流和计数；cube另依归一化模型定义与全符号对称，不由三半界推出精确OPT。
- Evidence：两内部数学审查与root全文/代码亲核、原矩阵/全负载回算；具体有限范围冻结于`evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。
- Counterevidence / Objections：固定exception与自由max条件已修；绝对界不等于近似比锐性；split模式不是物理σ枚举；cube A1非NO且按显式规模计，A20最优B21排除总取B=A。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；外审/论文价值未认证；一般目标及其反面OPEN。
- Related Files：`research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md`、`research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md`、`tests/audits/unrelated_machines/normalized_dual_rail_three_halves.py`, `tests/audits/unrelated_machines/normalized_dual_rail_half_slot_independent.py`, `examples/unrelated_machines/dual_rail_scalar_and_unit_sharp_input.json`, `evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。

## UM-SPLIT-CAPACITY-DUAL-RAIL-THREE-HALVES-v1：split unit外部容量的全类三半界

- Exact Statement：与scalar不同的真实P：外部每clause有min(A_c,m_c)台互异unit机器、port可至其任一台且时间1；arity≤2A_c。其余归一化轨不变。任意源均可总位poly输出全σ，轨≤3/2、unit≤1；14机15job重复例真实OPT=3/2，绝对T1界锐。
- Objects / Definitions：正文该ID自己的真实成本模型，所有port为不可拆分occurrence，所有机器共同实际负载，非抽象token目标。
- Domain：明确显式输入、二进制整数/有理时间；没有声明之外资格/背景job；空任务添dummy，K0不除零；重复occurrence合法。
- Quantifiers：∀显式输入、非负/空轨及巨大binary A_c；∃无SAT/OPT oracle的实际构造。
- Assumptions：必须使用该段成本、arity与指定证书，四合同不互换。
- Scope：仅上述具体编码、构造及sharp实例；未证明一般UM-TARGET-v1正反面，也未给一般近二NP困难性。
- Conclusion / Mechanism：变量供给floor((K++K−)/2)的共享整数流，再挑达到ceil(K_s/2)的一sign，只保留该sign外送。
- Dependencies：UM-MODEL-v1及正文独立定义；scalar用经典ST半质量直接推论，其他采用自足整数匹配/流和计数；cube另依归一化模型定义与全符号对称，不由三半界推出精确OPT。
- Evidence：两内部数学审查与root全文/代码亲核、原矩阵/全负载回算；具体有限范围冻结于`evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。
- Counterevidence / Objections：固定exception与自由max条件已修；绝对界不等于近似比锐性；split模式不是物理σ枚举；cube A1非NO且按显式规模计，A20最优B21排除总取B=A。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；外审/论文价值未认证；一般目标及其反面OPEN。
- Related Files：`research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md`、`research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md`、`tests/audits/unrelated_machines/split_capacity_dual_rail_three_halves.py`, `examples/unrelated_machines/dual_rail_scalar_and_unit_sharp_input.json`, `evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。

## UM-DUAL-RAIL-ONE-EXCEPTION-FLOOR-v1：非均匀内端的单例外匹配合同

- Exact Statement：另一模型：port内部非负有理w_e、每轨总W≤1；selector1；外部统一scalar1/A、arity≤2A。给ρ≥1，空轨预处理，其余每轨指定exception满足W−w_e≤ρ−1。可总位poly完整C≤ρ且clause≤1。对ρ1，arity2A+1的两clause族真实OPT=1+1/A，显示arity假设锐。
- Objects / Definitions：正文该ID自己的真实成本模型，所有port为不可拆分occurrence，所有机器共同实际负载，非抽象token目标。
- Domain：明确显式输入、二进制整数/有理时间；没有声明之外资格/背景job；空任务添dummy，K0不除零；重复occurrence合法。
- Quantifiers：∀上述显式P、ρ、指定exceptions；∃实际完整构造；∀A≥1存在越界锐例。
- Assumptions：必须使用该段成本、arity与指定证书，四合同不互换。
- Scope：仅上述具体编码、构造及sharp实例；未证明一般UM-TARGET-v1正反面，也未给一般近二NP困难性。
- Conclusion / Mechanism：两exception候选各半质量与clause容量A的整数匹配；不能用自由max替换固定指定端口。
- Dependencies：UM-MODEL-v1及正文独立定义；scalar用经典ST半质量直接推论，其他采用自足整数匹配/流和计数；cube另依归一化模型定义与全符号对称，不由三半界推出精确OPT。
- Evidence：两内部数学审查与root全文/代码亲核、原矩阵/全负载回算；具体有限范围冻结于`evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。
- Counterevidence / Objections：固定exception与自由max条件已修；绝对界不等于近似比锐性；split模式不是物理σ枚举；cube A1非NO且按显式规模计，A20最优B21排除总取B=A。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；外审/论文价值未认证；一般目标及其反面OPEN。
- Related Files：`research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md`、`research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md`、`tests/audits/unrelated_machines/dual_rail_one_exception_independent.py`, `examples/unrelated_machines/dual_rail_exception_arity_sharp_certificates.json`, `evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。

## UM-DUAL-RAIL-FULLCUBE-EXACT-FAILURE-v1：完整符号cube的真实OPT精确前沿与近一逃逸

- Exact Statement：归一化scalar的特殊族：A≥1,d=2A−1,k=2^(d−1)，含全部2^d符号clauses。R_B=Σ_s(s−B)_+ binom(d,s)、r_B=ceil(R_B/d)。真实OPT=min_{B=A..d}max(B/A,1+r_B/k)，可按显式展开P位poly构造。A≥2源弱阈值d−1仍NO，而OPT≤1+1/(2sqrt(d))+1/k→1。A3真实OPT9/8。
- Objects / Definitions：正文该ID自己的真实成本模型，所有port为不可拆分occurrence，所有机器共同实际负载，非抽象token目标。
- Domain：明确显式输入、二进制整数/有理时间；没有声明之外资格/背景job；空任务添dummy，K0不除零；重复occurrence合法。
- Quantifiers：∀整数A≥1；输入/输出已显式展开，非按log A多项式。近一NO及弱解码失败仅A≥2，不声称该族本身NP-hard。
- Assumptions：必须使用该段成本、arity与指定证书，四合同不互换。
- Scope：仅上述具体编码、构造及sharp实例；未证明一般UM-TARGET-v1正反面，也未给一般近二NP困难性。
- Conclusion / Mechanism：完整cube符号同构、整数内留计数下界、变量置换对称分数flow与整数化精确上界；必须min_B，不能总取B=A。
- Dependencies：UM-MODEL-v1及正文独立定义；scalar用经典ST半质量直接推论，其他采用自足整数匹配/流和计数；cube另依归一化模型定义与全符号对称，不由三半界推出精确OPT。
- Evidence：两内部数学审查与root全文/代码亲核、原矩阵/全负载回算；具体有限范围冻结于`evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。
- Counterevidence / Objections：固定exception与自由max条件已修；绝对界不等于近似比锐性；split模式不是物理σ枚举；cube A1非NO且按显式规模计，A20最优B21排除总取B=A。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；外审/论文价值未认证；一般目标及其反面OPEN。
- Related Files：`research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md`、`research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md`、`tests/audits/unrelated_machines/balanced_dual_rail_fullcube.py`, `tests/audits/unrelated_machines/balanced_dual_rail_fullcube_independent.py`, `examples/unrelated_machines/dual_rail_fullcube_A3_actual_certificate.json`, `evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json`。

## UM-UNIT-READOUT-PRUNED-FOREST-IDENTITY-v1：单位读出全变量必选配额森林恒等式

- Exact Statement：每变量两私有满k叉深h树；selector两根时间1、内部edge父1/k子1、leaf父1/k或本clause任一unit slot时间1。原资格恰此、slots跨clause互异无pins。对每有理1≤C<2，r=ceil(k(2−C))，真实C可行当且仅当每变量恰选一sign的深h恰r分叉森林可注入slots；给任方向见证可显式输入总位poly转另一方向。
- Objects / Definitions：正文对应节的显式完整树、所有mandatory变量、实际不可拆分任务/原资格；叶命中合同是独立组合树对象，不暗含slot容量。
- Domain：整数k,h≥1；调度仅声明的私有树与unit读出；A_c可0并截至arity；无job时dummy；完整叶深度不能提前停止。
- Quantifiers：∀整数k,h≥1、任意arity、A_c≥0和显式wiring；∀C∈Q∩[1,2)；完整σ与mandatory森林双向可构造。
- Assumptions：原资格恰声明边，机器组互异；半密度只在第二合同；第三合同转实际逃逸另需联合外部注入。
- Scope：非一般UM算法或近二NP-hardness；不把private-host pins模块混入无pins IFF，不按binary(k,h)压缩展开。
- Conclusion / Mechanism：原实际incoming1→至少r条实际下传；只保子集并复用原slot，所有其余jobs父置；active负载2−r/k、inactive1。
- Dependencies：正文自足证明；森林用UM-MODEL-v1与完整unit读出定义，半密度另用该定义、密度和既有split锐例；命中只用完整树定义及递推。
- Evidence：命题先行独立重构、冻结全文攻击、root全码亲读与原P/全机负载重算；六旧完整证书及两份同64open不同OPT证书，有限计数见`evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json`。
- Counterevidence / Objections：BCG Paper Fact已限制预处理剩余子实例，回填仅floor(M/2)；无外部定理被用来证明三合同。dummy需严格小于且外部可pack；平衡源空YES需非空clauses；仅叶容量忽略祖先兼容会给OPT7/4而非三半。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；软件身份audit_only，外审/论文价值未认证，一般目标正反面OPEN。
- Related Files：`research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md`、`research/reviews/unrelated_machines/unit_readout_pruned_forest_boundary_review.md`、`examples/unrelated_machines/unit_readout_two_tree_actual_certificates.json`、`evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json`、`tests/audits/unrelated_machines/unit_readout_two_tree_certificates.py`, `tests/audits/unrelated_machines/unit_readout_two_tree_independent.py`, `tests/audits/unrelated_machines/unit_readout_half_density_three_halves.py`。

## UM-UNIT-READOUT-HALF-DENSITY-THREE-HALVES-v1：半密度单位读出全高度三半锐界

- Exact Statement：同一模型另有每clause arity d_c≤2A_c。任意树深和任意wiring均可确定性总位poly输出全部原jobs实际C≤1+floor(k/2)/k≤3/2，所有外unit≤1。k1非空OPT1；k2h1复用14机15job split例真实OPT3/2，使整类绝对T1界锐，不声称近似比锐。
- Objects / Definitions：正文对应节的显式完整树、所有mandatory变量、实际不可拆分任务/原资格；叶命中合同是独立组合树对象，不暗含slot容量。
- Domain：整数k,h≥1；调度仅声明的私有树与unit读出；A_c可0并截至arity；无job时dummy；完整叶深度不能提前停止。
- Quantifiers：∀上述显式模型、∀k,h≥1及任意wiring；∃无SAT/OPT oracle的完整构造。
- Assumptions：原资格恰声明边，机器组互异；半密度只在第二合同；第三合同转实际逃逸另需联合外部注入。
- Scope：非一般UM算法或近二NP-hardness；不把private-host pins模块混入无pins IFF，不按binary(k,h)压缩展开。
- Conclusion / Mechanism：经典ST半质量直接推论；每内机唯一incoming半片优先，clause半片成对使用真实units，Hall一次全jobs匹配。
- Dependencies：正文自足证明；森林用UM-MODEL-v1与完整unit读出定义，半密度另用该定义、密度和既有split锐例；命中只用完整树定义及递推。
- Evidence：命题先行独立重构、冻结全文攻击、root全码亲读与原P/全机负载重算；六旧完整证书及两份同64open不同OPT证书，有限计数见`evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json`。
- Counterevidence / Objections：BCG Paper Fact已限制预处理剩余子实例，回填仅floor(M/2)；无外部定理被用来证明三合同。dummy需严格小于且外部可pack；平衡源空YES需非空clauses；仅叶容量忽略祖先兼容会给OPT7/4而非三半。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；软件身份implemented，外审/论文价值未认证，一般目标正反面OPEN。
- Related Files：`research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md`、`research/reviews/unrelated_machines/unit_readout_pruned_forest_boundary_review.md`、`examples/unrelated_machines/unit_readout_two_tree_actual_certificates.json`、`evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json`、`tests/audits/unrelated_machines/unit_readout_half_density_three_halves.py`。

## UM-PRUNED-TREE-LEAF-HITTING-v1：修剪树叶命中与虚拟叶门槛

- Exact Statement：完整k叉深h树、1≤r≤k，q=k−r+1。命中每个rooted深h恰r分叉子树的最小叶集恰q^h；不含任何该子树的叶子集最大恰k^h−q^h，所有参数锐。显式树双色DP可构造蓝r子树或红q子树；真实叶少于q^h时补集有纯dummy r子树，实际逃逸仍需外部共同容量。
- Objects / Definitions：正文对应节的显式完整树、所有mandatory变量、实际不可拆分任务/原资格；叶命中合同是独立组合树对象，不暗含slot容量。
- Domain：整数k,h≥1；调度仅声明的私有树与unit读出；A_c可0并截至arity；无job时dummy；完整叶深度不能提前停止。
- Quantifiers：∀整数k,h≥1、1≤r≤k和全部叶集；全部边界及达界例；复杂度只按显式树或完整路径输入。
- Assumptions：原资格恰声明边，机器组互异；半密度只在第二合同；第三合同转实际逃逸另需联合外部注入。
- Scope：非一般UM算法或近二NP-hardness；不把private-host pins模块混入无pins IFF，不按binary(k,h)压缩展开。
- Conclusion / Mechanism：标准threshold证书递推/补集对偶；根命中 iff 至少q个children各命中。非新一般树技术。
- Dependencies：正文自足证明；森林用UM-MODEL-v1与完整unit读出定义，半密度另用该定义、密度和既有split锐例；命中只用完整树定义及递推。
- Evidence：命题先行独立重构、冻结全文攻击、root全码亲读与原P/全机负载重算；六旧完整证书及两份同64open不同OPT证书，有限计数见`evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json`。
- Counterevidence / Objections：BCG Paper Fact已限制预处理剩余子实例，回填仅floor(M/2)；无外部定理被用来证明三合同。dummy需严格小于且外部可pack；平衡源空YES需非空clauses；仅叶容量忽略祖先兼容会给OPT7/4而非三半。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；软件身份audit_only，外审/论文价值未认证，一般目标正反面OPEN。
- Related Files：`research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md`、`research/reviews/unrelated_machines/unit_readout_pruned_forest_boundary_review.md`、`examples/unrelated_machines/unit_readout_two_tree_actual_certificates.json`、`evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json`、`tests/audits/unrelated_machines/pruned_tree_leaf_hitting.py`, `tests/audits/unrelated_machines/pruned_tree_leaf_hitting_independent.py`。

## UM-UNIT-READOUT-CALIBRATED-SLOT-v1：给定下传基数证书的校准实际槽舍入

- Exact Statement：同私有k叉双树unit读出模型，给1≤r≤k、有理edge/leaf下传t∈[0,1]、selector两根质量合1；每internal Σout t≥r−1+incoming且每clause Σleaf t≤A。可按P加见证总位长poly输出全σ，内部≤2−r/k、unit≤1。uniform x0=1/2,x_l=(r−1+xprev)/k使行取等，若d_c x_h≤A_c则所有wiring均可构造。
- Objects / Definitions：正文原P的私有满树、唯一incoming单位端、统一small1/k及clause共同unit资格；fraction为质量非处理时间。
- Domain：k,h≥1、A_c≥0、固定原深h、显式完整树/leaf paths；没有pins或隐藏资格。无任务时dummy机器，输出空σ；A截至arity。
- Quantifiers：∀显式P、k,h,r及满足共同条件的完整有理见证；∃确定性完整舍入；uniform自产分数按P位长poly。
- Assumptions：所有约束由同一组有理变量共同满足；D密度只在第二合同，所有真实/dummy ports均计arity。
- Scope：给定强证书仅充分；r>1 LP失败不一般证明OPT>1。受限C1必要性另需k>1及a d_c≤A_c。不是一般UM或近二NP-hardness。
- Conclusion / Mechanism：原行分数任务数≤整数k−r+1，大incoming优先唯一首槽；质量Hall一次覆盖全部jobs。
- Dependencies：UM-MODEL-v1、既有私有双树unit定义及本文基数证书；第二合同另用第一合同与mandatory r1路径必要性。ST有序槽为经典直接祖先。
- Evidence：三位内部先陈述独立重构、两冻结全文攻击、root全码亲读和实际原P回算，冻结于`evidence/runs/unrelated_machines/unit_readout_calibrated_cardinality_slots_audit.json`。
- Counterevidence / Objections：强LP非必要4机5job真OPT1；弱Σdown≥r*y不足4机9job真OPT7/4；matching失败5机10job真OPT2。任意外给见证位长计入输入，Python整数文本上限已解除并实际测过5000位。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；given-witness/uniform/bounded-D实际构造已实现，一般LP求解器未集成；无外审或论文价值认证，主目标正反面仍OPEN。
- Related Files：`research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md`、`research/reviews/unrelated_machines/unit_readout_calibrated_cardinality_slots_review.md`、`examples/unrelated_machines/unit_readout_calibrated_counterexamples.json`、`evidence/runs/unrelated_machines/unit_readout_calibrated_cardinality_slots_audit.json`、`tests/audits/unrelated_machines/unit_readout_calibrated_cardinality.py`、`tests/audits/unrelated_machines/unit_readout_calibrated_independent.py`。

## UM-UNIT-READOUT-BOUNDED-DENSITY-SUBTWO-v1：固定clause密度类的统一次二算法

- Exact Statement：对每个固定有理D≥2，同unit读出模型中若全部d_c≤D A_c，存在deterministic总位poly完整σ使C≤(2−1/(4D))OPT，允许k,h无界。大k校准r=1+floor((k−1)/(2D))；小k用r1容量匹配，失败证OPT2并全parent达到。空变量OPT0。
- Objects / Definitions：正文原P的私有满树、唯一incoming单位端、统一small1/k及clause共同unit资格；fraction为质量非处理时间。
- Domain：k,h≥1、A_c≥0、固定原深h、显式完整树/leaf paths；没有pins或隐藏资格。无任务时dummy机器，输出空σ；A截至arity。
- Quantifiers：∀固定D≥2，∀该结构类显式P；ε_D=1/(4D)与k,h、P规模无关。D无界时不算一般UM统一ε。
- Assumptions：所有约束由同一组有理变量共同满足；D密度只在第二合同，所有真实/dummy ports均计arity。
- Scope：给定强证书仅充分；r>1 LP失败不一般证明OPT>1。受限C1必要性另需k>1及a d_c≤A_c。不是一般UM或近二NP-hardness。
- Conclusion / Mechanism：校准质量≤1/D；rootselector给OPT≥1；r1 mandatory path匹配的必要性使失败分支精确最优。
- Dependencies：UM-MODEL-v1、既有私有双树unit定义及本文基数证书；第二合同另用第一合同与mandatory r1路径必要性。ST有序槽为经典直接祖先。
- Evidence：三位内部先陈述独立重构、两冻结全文攻击、root全码亲读和实际原P回算，冻结于`evidence/runs/unrelated_machines/unit_readout_calibrated_cardinality_slots_audit.json`。
- Counterevidence / Objections：强LP非必要4机5job真OPT1；弱Σdown≥r*y不足4机9job真OPT7/4；matching失败5机10job真OPT2。任意外给见证位长计入输入，Python整数文本上限已解除并实际测过5000位。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；given-witness/uniform/bounded-D实际构造已实现，一般LP求解器未集成；无外审或论文价值认证，主目标正反面仍OPEN。
- Related Files：`research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md`、`research/reviews/unrelated_machines/unit_readout_calibrated_cardinality_slots_review.md`、`examples/unrelated_machines/unit_readout_calibrated_counterexamples.json`、`evidence/runs/unrelated_machines/unit_readout_calibrated_cardinality_slots_audit.json`、`tests/audits/unrelated_machines/unit_readout_calibrated_cardinality.py`、`tests/audits/unrelated_machines/unit_readout_calibrated_independent.py`。

## UM-HEAVY-LIGHT-JOINT-RESIDUAL-MINMAX-v1：重轻任务联合残余 LP 的 min–max 障碍候选

- Exact Statement：固定阈值 `T>0` 与 `δ∈(0,1/2)`，若先将 `p_ij>(1−δ)T` 的任务整数放置到各机、再要求其余任务只用轻边完成残余分数 LP，则固定 heavy 放置 `h` 的可行性由全部 `λ≥0` 的 Farkas 不等式决定；逐个 `λ` 选择放置只证明 `∀λ∃h`，一般算法需要同一 `h` 满足 `∀λ`。
- Objects / Domain / Quantifiers：普通 `R||C_max` 矩阵、不可用边允许；本记录的障碍是对该“heavy matching→light residual LP”接口的量词反例，不是对所有算法的全称困难性。
- Evidence：仅在δ>3/20时分类正确的两机 `T=1` 符号实例 `A=(.95,.95)`, `B=(.85,.85)`, `ℓ_1=(.1,∞)`, `ℓ_2=(∞,.1)`；两个 heavy 匹配的残余容量分别为 `(0.05,.15)` 与 `(0.15,.05)`，均无法容纳对应固定 light 任务。计算仅作分数回算，核心为显式 Farkas/min–max 推导。
- Status：历史候选的量词示意已独立核查并修正范围；OPT=21/20>T，未否定YES承诺算法。原未明确剪枝及anchor统一下界，不能用于二倍结论。精确凸化/锐界另立UM-HEAVY-LIGHT-PRICE-CONVEXIFICATION-v1，不改v1为一般不可能性；后续应攻击真正非可加共同容量而非更多价格样本。
- Related Files：`research/questions/unrelated_machines/heavy_light_joint_residual_minmax_obstruction.md`。

## UM-HEAVY-LIGHT-PRICE-CONVEXIFICATION-v1：机器价格凸化的精确身份与锐容量界

- Exact Statement / Quantifiers：∀合法P、二进制有理T>0、β∈[1/2,1)，剪枝p≤T后按p>βT分类。∀非负机器价格可各选一个big部分匹配H并给其余任务最便宜light端，价格费用≤TΣλ，当且仅当任务守恒、逐机big质量≤1、逐机负载≤T的显式有理LP可行。固定有理价格的响应为确定性总位多项式整数费用流。
- Objects / Domain：UM-MODEL-v1；m、n可增长；P允许∞、0、空任务和大分母。T=0单独按零边精确处理；所有比值仅T>0。
- Definitions：B={(i,j):βT<p_ij≤T}、L={(i,j):p_ij≤βT}。H为B上的部分匹配，必须覆盖无L端任务；Γ为在固定B、L内共同H及未匹配任务light分数补全的最小最大机器负载。扩容时不重新分类或恢复剪掉的边。
- Assumptions：big严格阈值与β≥1/2保证任意真实T调度每机至多一个big；空light域必须由H覆盖。不存在H时价格式为+∞而非伪通过。
- Scope / Conclusion：LP不可行⇒OPT(P)>T。LP通过⇒Γ≤2T，对每个固定β，sup Γ/T=2；不剪枝的对应合同每个固定m有sup Γ/T=m。另若某个精确最优归一化价格λ*下全部最优流具有相同big向量，则可用O(|B|)次受限费用流核验，恢复Γ=τ（凸化最优容量）；τ≤T时实际ST输出≤τ+βT。面条件不满足不能作FAIL⇒OPT>T。
- Dependencies：UM-MODEL-v1；整数网络流凸包与有理LP分离/强对偶（正文自足推导）；UM-ST-ROUND-v1；UM-CONF-GAP-v1。半单位promise范围推论另引用UM-JOINT-HALF-PROMISE-NO-v1，未另造困难性。
- Evidence：两条内部独立推导、statement先行重构及最终全文/代码攻击；独立有理顶点与价格折点oracle、原P全分配小例、给定见证ST与真实逐机负载回算；冻结范围见heavy_light_price_convexification_release_audit.json。一般证明不依赖有限枚举。
- Counterevidence / Objections：旧数值两机例的heavy分类仅δ>3/20且OPT=21/20>T；新参数族覆盖全部β但仍不是YES承诺反例。任意非最优价下H唯一不足；不剪枝不能用2T上界。最优价格面的一般唯一性与可用共同容量均未证明。
- Status：complete direct consequence; independently reconstructed and exactly audited; external review and novelty unverified。已知ST/配置gap的精确接口综合，不认证新算法、新困难性或论文价值。审计实现有限oracle与见证舍入；一般LP/priceflow软件未集成。
- Related Files：`research/current/unrelated_machines/heavy_light_price_convexification.md`；`research/questions/unrelated_machines/heavy_light_joint_residual_minmax_obstruction.md`；`research/reviews/unrelated_machines/heavy_light_price_convexification_review.md`；`tests/audits/unrelated_machines/heavy_light_price_convexification.py`；`evidence/runs/unrelated_machines/heavy_light_price_convexification_release_audit.json`。

## UM-RESIDUAL-THROUGHPUT-LATTICE-v1：任意异端时间的容量格次模

- Exact Statement / Quantifiers：对固定有限 M,R,E 与非负有理处理时间 p，F(c)=max{Σx:任务质量≤1、机器处理量≤c、x≥0} 在数学上对实容量向量 c,d∈R_+^M 满足 F(c)+F(d)≥F(c∨d)+F(c∧d)，且非减；当 c,d 为带输入位长的有理向量时，F 可由显式有理 LP 在总输入位长多项式时间精确求值。F可由显式有理LP总位多项式精确求值；F(c)=|R|恰为完整共同分数路由。
- Objects / Domain / Definitions：未允许边无变量；R可空、可有无light端任务；零时间、零容量允许。F只计分数任务质量，不把合法输出改成可拆调度。
- Assumptions / Scope：同一个R,E,p冻结；固定C_i≥a_i≥0时c_i(I)=C_i−a_i1_I给非增次模F(I)、非减超模D(I)=|R|−F(I)。每个有零light端任务可免费删除加回，但不保另一个物理关机模型的原子问题值。
- Conclusion / Mechanism：dual混合格封闭(u∧v,a∨b)/(u∨v,a∧b)与逐坐标费用重排；完整通过量须精确达到任务数，近似总量不强制逐任务完成。固定状态失败证书不排除其他H。
- Dependencies：UM-MODEL-v1；显式有理LP强对偶（正文自足证明）。相关continuous assignment/submodular GAP文献只作背景，未将共同job资源模型导入任意p_ij。
- Evidence：构造者与statement先行独立重构；冻结全文/代码攻击；不调用仓库核的独立primal/dual有理顶点、dual混合/重排及实际2x2原调度/4份残余LP核验。见本节Related Files。
- Counterevidence / Objections：H同时改变R和机器扣减、F只用固定交叉light资格时不继承次模：p=[[1,1/2],[1/2,1]],T1，四H的V为2,1,1,2，原OPT1/2；它只是继承推理反例。无joint恢复、统一ε或sound FAIL保证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified。一般容量性质可复用，不认证新颖性或一般算法。一般LP软件未集成，审计为有限指数oracle。
- Related Files：`research/current/unrelated_machines/residual_throughput_and_occupation_projection.md`；`research/reviews/unrelated_machines/residual_throughput_occupation_review.md`；`tests/audits/unrelated_machines/residual_throughput_lattice.py`；`evidence/runs/unrelated_machines/residual_throughput_lattice_release.json`；LITERATURE及manifest中的LRMV2005/KSSS2019准确取得记录。

## UM-OCCUPATION-INDUCED-EDGE-DEFICIT-v1：严格次二占位的诱导边缺口恒等式

- Exact Statement / Quantifiers：∀固定有理1≤α<2和固定有理δ>0，∃确定性算法，对每个非空显式有限simple图G，在图位长poly时间构造2N机、N个任机单位宏及同尺寸h≤δ的tiny实例，给显式 OPT=1 调度；∀I⊆V，α容量完整调度的图机宏占位投影恰所有独立集。固定全部tiny为R、图机残余c_i(I)=α−1_I时，精确D(I)=|R|−F_R(c(I))=|E(G[I])|。
- Objects / Domain / Definitions：α=A/B既约，Δ=maxdeg；q=2B max{1,ceil[1/(2Bδ)],ceil[Δ/(2B(2−α))]}，h=1/q，r=q(α−1)整数。每图机r件专属tiny，每图边一件双端tiny；N辅助机不接tiny，全部宏资格为所有2N机。α与δ不是原实例OPT输入承诺。
- Assumptions / Scope：固定α、δ时才声称输出规模poly(|G|)；不声称bit(α)+bit(δ)统一poly。N≥1；宏单位和α<2使每机至多一个宏。tiny允许全部等端同尺寸、每件至多两选。
- Conclusion / Mechanism：宏全辅助给OPT1；I专属+内部边只能用I，剩余容量恰专属任务总量，至少缺诱导边数；弃内部边、其余向未占位端定向达到。故Hall完成族可精确为任意图独立集族；星图排除固定p-extendibility，但不是调度路径能垒。
- Dependencies：UM-MODEL-v1；本页F定义/流容量计数；构造与完整原任务恢复。一般F格次模提供共同接口语境，不是该表示下界的计算证据。
- Evidence：构造与独立statement先行重构；显式P/全部任务实际σ/原OPT下上界回算；普通整数maxflow与独立边定向oracle核D=e(I)，冻结参数与输入hash见Related Files。有限图核验不承担一般证明。
- Counterevidence / Objections：每个生成的原实例都直接可最优解，不能把投影选择升级为UM困难性；改变宏必须进图或减少辅助机是新合同。αδ二进制极值会使显式tiny数大，未误报统一位poly。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified。只关闭免费拟阵/固定交换界的状态识别；一般主目标仍OPEN，新颖性/论文价值未认证。
- Related Files：`research/current/unrelated_machines/residual_throughput_and_occupation_projection.md`；`research/reviews/unrelated_machines/residual_throughput_occupation_review.md`；`tests/audits/unrelated_machines/occupation_induced_edge_deficit.py`；`evidence/runs/unrelated_machines/occupation_induced_edge_deficit_release.json`。


## UM-TWO-STATE-QUOTA-ORIENTATION-EQUIV-v1：两状态残余树的 two-rail quota orientation 表示

- **Exact Statement：** 固定 \(\delta\in(0,1]\) 时，状态内资源不交的两状态残余树满足 \(b(H)\ge\delta\) 当且仅当存在至少 \(\lceil\delta q_r\rceil\) 个变量的rail选择、每个标签至少 \(\lceil\delta K\rceil\) 个资源槽且所有资源像互不交。
- **Mathematical role：** 完整支付层是2-SAT禁冲突；部分支付层是带方向约束的quota packing，正是两状态近二soundness的最小对象。
- **Status：** complete stated-scope equivalence proof; external review and novelty unverified。
- **Related Files：** `research/current/unrelated_machines/two_state_quota_orientation_obligation.md`。

## UM-UNIT-READOUT-FIXED-HEIGHT-APPROX-v1：任意密度完整单位树的固定高度次二近似

- Exact Statement：任意clause密度的私有双k叉深h单位读出完整模型，可确定性按显式输入总位长poly输出全部原jobs的合法σ，C≤(1+2^(−1/h))OPT；h≤固定H时统一严格小于2，h1给3/2。算法不求未知OPT；b0分支证明OPT2并全parent达到；空变量先返0。
- Objects / Definitions：正文§1的全部mandatory双轨原任务、私有树、unit clauses、实际不可拆分σ；第二合同的完整YES和固定根如§3。
- Domain：全部显式单位双树、任意arity与binary A；h,k≥1；原资格无pins/额外jobs。
- Quantifiers：∀本结构类输入；固定H时∀h≤H给统一正常数；h无界不保统一ε。
- Assumptions：原资格恰声明成本与共同unit资格；全部叶路径显式；第二合同所有见证属于同一P/共同容量。
- Scope：限定结构类或给定真实完整见证，不是一般UM算法或近二NP-hardness；一般目标及其反面OPEN。
- Conclusion / Mechanism：最大共同真实叶流b→多数sign→r=k−floor((k^h−ceil(b/2))^(1/h))的真实祖先子树；只删同一flow叶保共同容量；最优r*给b≥r*^h，导数给因子。
- Dependencies：UM-MODEL-v1；UM-PRIVATE-KARY-DUAL-TREE-UNIT-READOUT-MODEL-v1；UM-UNIT-READOUT-GLOBAL-LEAF-FLOW-v1；UM-UNIT-READOUT-PRUNED-FOREST-IDENTITY-v1；UM-PRUNED-TREE-LEAF-HITTING-v1；经典流/Hall/ST工具明确扣除，不认证新颖性。
- Evidence：两合同分别先陈述独立重构，冻结正文425af66全文双审与root亲核；两个规范实际构造CLI、独立p1..4完整原P/σ及有限回算见Related Files。
- Counterevidence / Objections：h无界余量趋0；N<p有真实指定profileOPT2反例；旧64open不许免费补祖先；NO源可能无任何完整YES，不能越界应用重组；锐profile值非全局OPT。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实际构造已实现；外审、全球新颖性和独立论文价值未认证。
- Related Files：`research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md`；`research/reviews/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_review.md`；`evidence/runs/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_audit.json`；`examples/unrelated_machines/unit_readout_selector_mixing_sharp_profiles.json`；`tests/audits/unrelated_machines/unit_readout_leaf_flow.py`。

## UM-UNIT-READOUT-SELECTOR-MIXING-v1：完整YES支持的指定selector重组锐界

- Exact Statement：同一P给p≥1份完整实际C≤1调度，每变量指定一个至少在一见证采用过的selector sign；非空另需N=k^h≥p。可按P加全部见证位长poly输出满足全部指定根的完整σ，C≤2−1/(2p−1)。大k取r=floor(k/p)，小k取r1；p1直接原YES。对每p该指定profile保证精确锐，而原全局OPT1。
- Objects / Definitions：正文§1的全部mandatory双轨原任务、私有树、unit clauses、实际不可拆分σ；第二合同的完整YES和固定根如§3。
- Domain：同私有单位双树原模型；给定完整YES/指定根，不含额外pins；空变量0。
- Quantifiers：∀p及同一P的完整真实见证、∀covered坐标profile；非空需N≥p；不声称寻找见证。
- Assumptions：原资格恰声明成本与共同unit资格；全部叶路径显式；第二合同所有见证属于同一P/共同容量。
- Scope：限定结构类或给定真实完整见证，不是一般UM算法或近二NP-hardness；一般目标及其反面OPEN。
- Conclusion / Mechanism：完整YES强制所选轨全外送，指定轨arity d*≤pA；只指定轨建x0=1计数槽，另一轨固定parent；共同Hall保指定根和所有机器。
- Dependencies：UM-MODEL-v1；UM-PRIVATE-KARY-DUAL-TREE-UNIT-READOUT-MODEL-v1；UM-UNIT-READOUT-COMPLETE-YES-COVER-v1；UM-UNIT-READOUT-CALIBRATED-SLOT-v1；经典流/Hall/ST工具明确扣除，不认证新颖性。
- Evidence：两合同分别先陈述独立重构，冻结正文425af66全文双审与root亲核；两个规范实际构造CLI、独立p1..4完整原P/σ及有限回算见Related Files。
- Counterevidence / Objections：h无界余量趋0；N<p有真实指定profileOPT2反例；旧64open不许免费补祖先；NO源可能无任何完整YES，不能越界应用重组；锐profile值非全局OPT。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实际构造已实现；外审、全球新颖性和独立论文价值未认证。
- Related Files：`research/current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md`；`research/reviews/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_review.md`；`evidence/runs/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_audit.json`；`examples/unrelated_machines/unit_readout_selector_mixing_sharp_profiles.json`；`tests/audits/unrelated_machines/unit_readout_selector_mixing.py`；`tests/audits/unrelated_machines/unit_readout_selector_profile_independent.py`。

## UM-MEDIUM-CONFIG-TINY-BARRIER-v1：固定阈值中任务配置分解的近二边界

- Exact Statement / Quantifiers：对每个固定有理 (0<\alpha<1/5)，存在合法 (P,T) 使全部有限 (p_{ij}>\alpha T)、配置 LP 在 (T) 可行而 (\operatorname{OPT}/T=7/5>1+\alpha)。因此“仅凭配置 LP(T)可行性，再把 (p\le\alpha T) 的 tiny 末步独立支付 (\alpha T)”的合同在该范围不可能给统一小于2。
- Objects / Domain / Definitions：取经典两树族 (k=4)，(T=5/4)，有限时间仅 (1/4,1)，整数最优值 (7/4)。
- Assumptions / Scope：只否定固定阈值、配置 LP 与独立 tiny-ST 加性收费的接口；不排跨机器强化、直接联合舍入、改变阈值或 (\alpha\ge1/5)。
- Conclusion / Mechanism：tiny 集合为空，接口退化为配置间隙；配置列在固定 (alpha) 下可枚举不改变 LP 到共同整数选择的积分缺口。
- Dependencies：UM-CONF-GAP-v1 与 `model_and_classical_barriers.md` 的 (k=4) 证书；本页 Fraction 反算 (1/4>\alpha(5/4))、(7/5>1+\alpha)。
- Evidence：参数化直接证明；独立 Python Fraction 计算覆盖 (alpha=1/6,1/10,1/100) 的严格不等式。有限算术核对不替代配置族证明。
- Counterevidence / Objections：若外层能识别更强的共同容量状态或允许重开配置边，该反例不适用；(\alpha=1/5) 时严格 tiny 排除条件失效。
- Status：failed-route boundary; not a hardness result; external review and novelty unverified。
- Related Files：`research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md`；`research/current/unrelated_machines/model_and_classical_barriers.md`；`research/unrelated_machines/FAILED_ROUTES.md`。

## UM-FIXED-WORK-CONVEX-POTENTIAL-BARRIER-v1：固定工作量与分离凸势锁定近二

- Exact Statement / Quantifiers：对任意整数 (h\ge2,q\ge1)，令 (t=(h-1)/(hq))，用 (h) 个核心、(hq) 个私有叶、一个核心全可用的大任务 (B) 与每个 tiny 的 home/私有叶两条边 (t,1) 构造实例。则 OPT=1；给定 (T=1) 的最小总工作量分数支撑的任一 ST 槽匹配值为 (2-1/h)。对任意有限、非减、凸 (f:[0,3]\to\mathbb R)，若 (Delta=f(1)-f(0)>0)、(D=f(3)-f(2)) 且 (q>(1-1/h)D/\Delta)，则每个 (\sum_i f(L_i)) 全局最小调度仍有值至少 (2-1/h)。取 (q=h^2) 时任意固定相对工作量预算 (W\le\rho h) 的调度满足 (C_{\max}\ge2-1/h-(\rho-1)ht/(1-t))（\(\rho\ge1\)）。
- Objects / Domain / Definitions：(P_{C_i,B}=1)、(P_{C_i,S_{i,r}}=t)、(P_{L_{i,r},S_{i,r}}=1)，其余边不可用；(m=h(1+q))、(n=1+hq)。
- Assumptions / Scope：只排固定正支撑、固定总工作量放松和固定非减凸分离势；不排输入自适应 hinge/机器权重/非可加势/允许暂时增载的批量迁移。(f) 仅需在 ([0,3]) 有限。
- Conclusion / Mechanism：最小工作量支撑把 tiny 叶边质量置零；迁出 (B)-核心 tiny 的叶增量 (f(1)-f(0)) 大于核心节省，故任一固定势全局最小解保留近二坏态；真正 OPT 通过重开边并非不可达。
- Dependencies：本页 `fixed_work_and_medium_config_barriers.md` 的参数化证明；UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1 只作相邻背景，不替代本族证明。
- Evidence：独立 Fraction 全枚举 ((h,q)=(2,1),(2,2),(3,1),(3,2)) 核验 OPT、(W_{\min}) 与槽值；((2,4), f(L)=L^2) 全状态枚举的最小势值为 (3/2)。
- Counterevidence / Objections：昂贵叶边本身可被配置方法识别；hinge/自适应势可逐件迁移，因此不能升级为一般困难性或主目标反证。
- Status：failed-route boundary; not a hardness result; external review and novelty unverified。
- Related Files：`research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md`；`research/unrelated_machines/FAILED_ROUTES.md`；`research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md`。

## 槽包络、弱H2及强二阶合同的精确分离

### UM-ST-ENVELOPE-CONFIG-IDENTITY-v1：完整槽包络的精确调度表示与两种凸化身份

- Exact Statement / Quantifiers：任意非负有理行的E=ΣΔp ceil(prefix x)；固定B子水平凸包恰配置多面体、至多d+1有理原子。全局min max E=OPT，可ST实际恢复；先固定B逐行凸化恰CONFIG，先凸化上图仅线性负载。
- Objects / Domain / Definitions：UM-MODEL-v1；全部非负二进制有理/不可用输入，具体子域与合同见正文。槽包络量化所有合法P及x；H2下界只取正OPT/T>0，强校准为同一k≥3参数族。
- Assumptions / Scope：精确表示不等于可求非凸选择；CONFIG的二倍gap为既有结论复用；未给主目标近似算法。
- Conclusion：完整槽包络的精确调度表示与两种凸化身份，不改UM-TARGET-v1的OPEN状态。
- Dependencies：UM-MODEL-v1, UM-ST-ROUND-v1, UM-CONF-GAP-v1；正文自足推导所列各共同前提。
- Evidence：先陈述独立重构、冻结全文攻击、root亲自复核；最小精确运行见evidence/runs/unrelated_machines/slot_envelope_identity_audit.json。
- Counterevidence / Objections：精确表示不等于可求非凸选择；CONFIG的二倍gap为既有结论复用；未给主目标近似算法。 共享二阶的强系统与仅共享一阶的弱系统身份绝不互换。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。无一般求解器，未认证全球新颖性或外部评审。
- Related Files：`research/current/unrelated_machines/slot_envelope_and_configuration_identity.md`；`research/reviews/unrelated_machines/slot_envelope_identity_review.md`；`tests/audits/unrelated_machines/slot_envelope_identity.py`；`evidence/runs/unrelated_machines/slot_envelope_identity_audit.json`。

### UM-WEAK-H2-CONFIG-MOMENT-GAP-v1：同一一阶配置与全局四阶矩合取的锐利二间隙

- Exact Statement / Quantifiers：弱H2=C2-load(T)+共享一阶x的完整CONFIG(T)，一般正值sup OPT/T=2。k≥3,b=k²稀释资源星在T=1+(k−1)/(k²+1)有显式有理全局PSD/全localizer与同x CONFIG1，真实OPT=2−1/k。
- Objects / Domain / Definitions：UM-MODEL-v1；全部非负二进制有理/不可用输入，具体子域与合同见正文。槽包络量化所有合法P及x；H2下界只取正OPT/T>0，强校准为同一k≥3参数族。
- Assumptions / Scope：不共享行二阶且三阶仍可负；不含强二阶H2、完整SoS(CONFIG)或一般计算困难性；本族可直接最优解。
- Conclusion：同一一阶配置与全局四阶矩合取的锐利二间隙，不改UM-TARGET-v1的OPEN状态。
- Dependencies：UM-MODEL-v1, UM-C2-GENERAL-MULTISLICE-CONSTRUCTION-v1, UM-ST-ROUND-v1；正文自足推导所列各共同前提。
- Evidence：先陈述独立重构、冻结全文攻击、root亲自复核；最小精确运行见evidence/runs/unrelated_machines/weak_h2_configuration_moment_gap_audit.json。
- Counterevidence / Objections：不共享行二阶且三阶仍可负；不含强二阶H2、完整SoS(CONFIG)或一般计算困难性；本族可直接最优解。 共享二阶的强系统与仅共享一阶的弱系统身份绝不互换。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。无一般求解器，未认证全球新颖性或外部评审。
- Related Files：`research/current/unrelated_machines/weak_h2_configuration_moment_gap.md`；`research/reviews/unrelated_machines/weak_h2_configuration_moment_gap_review.md`；`tests/audits/unrelated_machines/weak_h2_configuration_moment_gap.py`；`evidence/runs/unrelated_machines/weak_h2_configuration_moment_gap_audit.json`。

### UM-STRONG-H2-ROW-PAIR-STAR-EXACT-v1：共享行二阶矩的条件单槽容量与资源星精确阈值

- Exact Statement / Quantifiers：若容量一行CONFIG同机pair与全局M2共享，则任意端f有Σ_row y_fe≤x_f；在同一k≥3,b=k²无z星族，共享每行二阶CONFIG的强H2阈值恰2−1/k=OPT，所有T<OPT均不可行，真实Dirac达到。
- Objects / Domain / Definitions：UM-MODEL-v1；全部非负二进制有理/不可用输入，具体子域与合同见正文。槽包络量化所有合法P及x；H2下界只取正OPT/T>0，强校准为同一k≥3参数族。
- Assumptions / Scope：仅此族的强合同精确校准，不含一般强H2间隙改善或求解复杂度；该条件容量证明不需要负载localizer。
- Conclusion：共享行二阶矩的条件单槽容量与资源星精确阈值，不改UM-TARGET-v1的OPEN状态。
- Dependencies：UM-MODEL-v1；正文自足推导所列各共同前提。
- Evidence：先陈述独立重构、冻结全文攻击、root亲自复核；最小精确运行见evidence/runs/unrelated_machines/weak_h2_configuration_moment_gap_audit.json。
- Counterevidence / Objections：仅此族的强合同精确校准，不含一般强H2间隙改善或求解复杂度；该条件容量证明不需要负载localizer。 共享二阶的强系统与仅共享一阶的弱系统身份绝不互换。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。无一般求解器，未认证全球新颖性或外部评审。
- Related Files：`research/current/unrelated_machines/weak_h2_configuration_moment_gap.md`；`research/reviews/unrelated_machines/weak_h2_configuration_moment_gap_review.md`；`tests/audits/unrelated_machines/weak_h2_configuration_moment_gap.py`；`evidence/runs/unrelated_machines/weak_h2_configuration_moment_gap_audit.json`。

## UM-CROSS-LAYER-CORE-PRIVATE-NEAR-TWO-v1：核心—私有资源的全层配额与真实近二整数障碍

- **Exact Statement：** 取 K>s≥1、c=K−s、q≥ceil(cK/s)。共同核心 C 大小 c，每变量私有 P_i 大小 s，A_i=C∪P_i。全层 t-matching 值为 ν_t=q（t≤s），ν_t=min(q,floor(c/(t−s)))（t>s），故 b*=s/K。需求树桥梁的实际不可拆矩阵满足 OPT=2−s/K；每个固定 δ>0 可取 s=1、K=ceil(2/δ) 得 OPT>2−δ 的显式族。
- **Objects / Domain：** 根需求 q、变量需求1、标签需求K、资源零需求；实际任务为根/变量/标签/资源边的二值有限处理矩阵，任务数1+2q+qK，机器数1+2q+c+qs。
- **Quantifiers / Scope：** 对所有上述整数参数和显式资源系统成立；只证明该接口的全层障碍，不声称源问题困难性、一般UM近二下界或新颖性。
- **Dependencies / Evidence：** `UM-SINGLE-LAYER-QUOTA-VALUE-v1`、`UM-DAG-DEGREE-TOKEN-IDENTITY-v1`；正文、独立审查、Fraction全枚举与4950组闭式检查见 Related Files。
- **Counterevidence / Objections：** 资源族显式可识别，YES对照显式可解；缺源相关接线和任意低调度 decoder，不能升级为P≠NP结论。
- **Status：** complete stated-scope obstruction; independently reconstructed and exactly audited; external review and novelty unverified；`UM-TARGET-v1`仍OPEN。
- **Related Files：** `research/current/unrelated_machines/cross_layer_quota_matching_near_two_obstruction.md`、`research/reviews/unrelated_machines/cross_layer_quota_matching_review.md`、`tests/audits/unrelated_machines/cross_layer_quota_matching.py`、`evidence/runs/unrelated_machines/cross_layer_quota_matching_candidate.json`。

## UM-INDEPENDENT-SET-BIG-RESIDUAL-INTERFACE-v1：共同大任务选择的独立集阈值障碍

- **Exact Statement：** 给最大度 Δ 图、k 件全图宏任务时间1、每顶点 r 件私有任务时间 h、每边一件两端任务时间 h，满足 rh=α−1、Δh≤1、1<α<2。则 Cmax≤α 当且仅当图有大小k独立集；NO下界为 min{2,α+h}。固定 Δ=3、h=1/3、r=0 给1对4/3，r=1给4/3对5/3。
- **Objects / Domain：** 一般不相关机矩阵，边外不可用；k≥1，r=0端点 α=1 单列；任务数与图显式规模多项式。
- **Scope / Conclusion：** 这是“先固定big位置、再残余流补齐”接口的精确NP障碍候选；不排同时重选、配置割或其他全局算法，不给统一(2−ε)硬度。
- **Dependencies / Evidence：** `UM-MODEL-v1`；双向负载证明、独立审查和1080个小图 Fraction实际枚举。
- **Status：** candidate exact-threshold interface obstruction; internally reconstructed and exactly audited; external review and novelty unverified；`UM-TARGET-v1`仍OPEN。
- **Related Files：** `research/questions/unrelated_machines/independent_set_big_residual_interface_obstruction.md`、`research/reviews/unrelated_machines/independent_set_big_residual_review.md`、`tests/audits/unrelated_machines/independent_set_big_residual_audit.py`、`evidence/runs/unrelated_machines/independent_set_big_residual_audit.json`。

## UM-FIXED-WORK-CONVEX-LOCAL-MINIMUM-v1：固定总工作量下凸势与排序势的近二局部极小

- **Exact Statement：** 对每个 m≥3 的完全相同机器族，两件unit和m²−1件1/m tiny使总工作量固定；给定初始分配的Cmax=2、OPT=1+2/m，二次负载势与非增排序负载词典序均对每一件单任务换机严格变差；任意Cmax≤2−ε需改变至少2+ceil(εm)件任务。
- **Objects / Domain：** 全有限正处理时间、无资格限制的R||Cmax子族；只声明单任务邻域和固定势合同。
- **Scope / Conclusion：** 只关闭该初态的单任务严格下降及证明最终总支持下界；固定批量多轮外推已由公屏467三件启动反驳撤回。保留非单调过渡、输入自适应势或全局重求解。两机精确全局二次势含PARTITION只是额外oracle义务。
- **Dependencies / Evidence：** `UM-MODEL-v1`；自足计数证明、独立审查、m=3全分配枚举及m=4,5,8,12 Fraction核验。
- **Status：** complete stated-scope obstruction; independently reconstructed and exactly audited; external review and novelty unverified；`UM-TARGET-v1`仍OPEN。
- **Related Files：** `research/current/unrelated_machines/fixed_work_convex_local_minimum_near_two.md`、`research/reviews/unrelated_machines/fixed_work_convex_local_minimum_review.md`、`tests/audits/unrelated_machines/fixed_work_convex_local_minimum.py`、`evidence/runs/unrelated_machines/fixed_work_convex_local_minimum_audit.json`。


## UM-TWO-STATE-QUOTA-HALL-CUT-v1：固定 rail 方向的 Hall 切分解

- **Exact Statement：** 固定变量子集 \(S\)、每个变量的一个 rail、选中标签集合 \(L\) 及整数需求 \(t_\ell\ge0\)。存在每个标签注入 \(t_\ell\) 个互不重复资源，当且仅当对所有 \(U\subseteq L\)，
  \[
  \sum_{\ell\in U}t_\ell\le\left|\bigcup_{\ell\in U}R(\ell)\right|.
  \]
  资源至多接两个标签时，邻域等于全局度一私有、两端都在 \(U\) 的共享和恰一端在 \(U\) 的边界资源三项之和。
- **Objects / Domain / Definitions：** 两状态残余 DAG；状态内资源不交；跨状态资源可共享；支付是不可重复资源的整数注入。固定方向，不量化 rail 选择。
- **Quantifiers：** 对每个满足上述条件的显式 \(L,R,t\)，Hall 条件与实际支付等价；证明不依赖有限枚举。
- **Assumptions / Scope：** 资源容量均为1，需求为整数；不声称方向选择或最大根比例的多项式算法，不声称一般 `FAIL⇒OPT>T` 或 UM-TARGET-v1 困难性。
- **Conclusion / Mechanism：** 二部匹配/Hall 定理给出精确切条件；固定方向可用下界流和整数最大流构造实际支付。完整支付层恢复跨变量共享资源的2-SAT禁冲突；部分支付层必须检查集合 Hall 切，不能只查成对冲突。
- **Dependencies：** `UM-TWO-STATE-QUOTA-ORIENTATION-EQUIV-v1`、二部匹配 Hall 定理与整数流。
- **Evidence：** 独立 Python 审计标签≤3、资源≤4、需求 \(0,1,2\) 的全部资源关联模式（含空标签子集）共 279,936 个固定方向实例，均与 Hall 判据一致；有限核验不替代一般证明。
- **Counterevidence / Objections：** 尚未得到对 rail 方向/变量子集联合选择的算法或全方向失败证书；单固定方向的 Hall 缺口不能拒绝原阈值 \(T\)。
- **Status：** complete stated-scope proof; internal blind review completed with wording repairs; external review and novelty unverified。
- **Related Files：** `research/current/unrelated_machines/two_state_quota_hall_cut_decomposition.md`、`tests/audits/unrelated_machines/two_state_quota_hall.py`、`evidence/runs/unrelated_machines/two_state_quota_hall_audit.json`。

## UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1：私有单位树的配置正部多面体

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions：对完整私有单位双树，T∈[1,2)、s=floor k(T−1)，CONFIG可行恰为共同边际满足Σ(q−t)+≤sq和clause容量；显式有理分解、多项式LP及精确阈值网格。 全部对象固定为正文§1，所有输入显式；退化、binary A和k1见正文。
- Scope / Conclusion：只给本单位树结构的配置描述、严格单位阈值gap或闭合族精确阈值；不是一般UM改善/困难性。
- Dependencies：UM-MODEL-v1, UM-PRIVATE-KARY-DUAL-TREE-UNIT-READOUT-MODEL-v1；全部共同前提及自足证明见[正文](../current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)。
- Evidence：一般证明、先陈述独立重构和冻结全文攻击；精确有限审计仅checks，见[审查](../reviews/unrelated_machines/unit_readout_configuration_threshold_review.md)。
- Counterevidence/Objections：无standing内部fatal；严格1不可外推1+1/k，一般LP软件未集成，外审/新颖性未认证。
- Status / Related Files：限定完整证明与内部独立核验；实际实现范围、原P见证和冻结输出由正文/审查互链。

## UM-UNIT-READOUT-STRICT-UNIT-GAP-v1：严格单位阈值的整轨LP五三间隙算法

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions：CONFIG1等价整轨literal LP；可行时多数轨active-only槽输出全部原jobs C≤5/3，偶k≤3/2，k1≤1；为(1,5/3) promise gap，不是任意OPT比例。 全部对象固定为正文§1，所有输入显式；退化、binary A和k1见正文。
- Scope / Conclusion：只给本单位树结构的配置描述、严格单位阈值gap或闭合族精确阈值；不是一般UM改善/困难性。
- Dependencies：UM-MODEL-v1, UM-PRIVATE-KARY-DUAL-TREE-UNIT-READOUT-MODEL-v1, UM-UNIT-READOUT-LITERAL-LP-WITNESS-v1, UM-UNIT-READOUT-CALIBRATED-SLOT-v1, UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1；全部共同前提及自足证明见[正文](../current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)。
- Evidence：一般证明、先陈述独立重构和冻结全文攻击；精确有限审计仅checks，见[审查](../reviews/unrelated_machines/unit_readout_configuration_threshold_review.md)。
- Counterevidence/Objections：无standing内部fatal；严格1不可外推1+1/k，一般LP软件未集成，外审/新颖性未认证。
- Status / Related Files：限定完整证明与内部独立核验；实际实现范围、原P见证和冻结输出由正文/审查互链。

## UM-UNIT-READOUT-CLOSED-TREES-EXACT-CONFIG-v1：闭合两树的精确配置阈值

- Exact Statement / Objects / Domain / Quantifiers / Assumptions / Definitions：每末父k叶共一私有unit的闭合两树，OPT=2−1/k，Tconf=1+s*/k，s*=min{s:(k−s)^h≤2k^(h−1)}；经典gap高度下精确1+1/k。 全部对象固定为正文§1，所有输入显式；退化、binary A和k1见正文。
- Scope / Conclusion：只给本单位树结构的配置描述、严格单位阈值gap或闭合族精确阈值；不是一般UM改善/困难性。
- Dependencies：UM-PRIVATE-KARY-DUAL-TREE-UNIT-READOUT-MODEL-v1, UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1, UM-UNIT-READOUT-PRUNED-FOREST-IDENTITY-v1；全部共同前提及自足证明见[正文](../current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)。
- Evidence：一般证明、先陈述独立重构和冻结全文攻击；精确有限审计仅checks，见[审查](../reviews/unrelated_machines/unit_readout_configuration_threshold_review.md)。
- Counterevidence/Objections：无standing内部fatal；严格1不可外推1+1/k，一般LP软件未集成，外审/新颖性未认证。
- Status / Related Files：限定完整证明与内部独立核验；实际实现范围、原P见证和冻结输出由正文/审查互链。

## UM-PRUNED-FIRST-MOVE-BOUND-v1：剪枝调度首步临时容量的全输入分段上界

- Exact Statement / Quantifiers：对任意合法P、有理T≥0与T≤C≤2T、使用p≤T端且Cmaxσ≤C的实际σ，若存在不同τ且Cmaxτ≤T，则某一件直接σ→τ迁移后的最大负载≤U=max(2T,C+T/2)。不给τ时可位多项式返回DONE、此类MOVE或可靠NO_T_SCHEDULE⇒OPT>T；MOVE不保证改善。
- Objects / Domain / Definitions：UM-MODEL-v1；二进制非负有理/∞，实际完整分配；E_T={p_ij≤T}；U与非空同步批量、指定目标路径按正文§1定义。
- Assumptions / Scope：首步上界承重σ使用边≤T；T0单独精确处理；锐族T>0、k由m=k+1显式体现。初态不声称来自ST/配置/真最优凸包。不是一般全程U上界、未知目标求解器或次二近似。
- Conclusion：确定性总位多项式实际单步及单向拒绝证书；不是进展保证。
- Dependencies：UM-MODEL-v1；正文自足端点入/出计数、非负性、环边界、逐件负载与最短时间总和平均下界。两项一般证明相互独立；不依赖外部定理或有限实验。
- Evidence：两名内部研究者先陈述独立重构、后冻结全文攻击；主研究者亲核。规范、完全不导入规范的独立状态oracle、完整原矩阵OPT集成审计及实际输入/路径证书均已冻结。
- Counterevidence / Objections：C=T零步到OPT与B<C不在状态图的原措辞已在首版冻结前修正；一步可超过2T，不能无证明迭代。公开结构能直接求τ，未导入调度困难性。声明范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实际首步实现、内审、外审和新颖性分轴，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/pruned_first_move_and_transient_peak.md](../current/unrelated_machines/pruned_first_move_and_transient_peak.md)、research/reviews/unrelated_machines/pruned_first_move_transient_peak_review.md；三份审计代码、evidence/runs/unrelated_machines/pruned_first_move_transient_peak_audit.json、examples/unrelated_machines/transient_peak_two_job_cycle.json与evidence/certificates/unrelated_machines/transient_peak_two_job_cycle.json。


## UM-BOUNDED-BATCH-TRANSIENT-PEAK-SHARP-v1：有界批量环族的逐参数锐临时峰值

- Exact Statement / Quantifiers：对每k≥1、每有理T>0及T≤C≤2T，显式m=k+1环族全部有限边≤T、每任务≤2端、OPT=T、初值C；任意非空≤k件同步变化新值≥U=max(2T,C+T/2)，到指定不同最优τ的最小路径峰恰U（单件路径达到）。孤立图范围C≤B<U；C=T不排零步到OPT集合。
- Objects / Domain / Definitions：UM-MODEL-v1；二进制非负有理/∞，实际完整分配；E_T={p_ij≤T}；U与非空同步批量、指定目标路径按正文§1定义。
- Assumptions / Scope：首步上界承重σ使用边≤T；T0单独精确处理；锐族T>0、k由m=k+1显式体现。初态不声称来自ST/配置/真最优凸包。不是一般全程U上界、未知目标求解器或次二近似。
- Conclusion：固定批量的首步临时预算与指定目标minimax逐参数锐；C>T才同时限制到整个最优集合。
- Dependencies：UM-MODEL-v1；正文自足端点入/出计数、非负性、环边界、逐件负载与最短时间总和平均下界。两项一般证明相互独立；不依赖外部定理或有限实验。
- Evidence：两名内部研究者先陈述独立重构、后冻结全文攻击；主研究者亲核。规范、完全不导入规范的独立状态oracle、完整原矩阵OPT集成审计及实际输入/路径证书均已冻结。
- Counterevidence / Objections：C=T零步到OPT与B<C不在状态图的原措辞已在首版冻结前修正；一步可超过2T，不能无证明迭代。公开结构能直接求τ，未导入调度困难性。声明范围无尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实际首步实现、内审、外审和新颖性分轴，UM-TARGET-v1仍OPEN。
- Related Files：[research/current/unrelated_machines/pruned_first_move_and_transient_peak.md](../current/unrelated_machines/pruned_first_move_and_transient_peak.md)、research/reviews/unrelated_machines/pruned_first_move_transient_peak_review.md；三份审计代码、evidence/runs/unrelated_machines/pruned_first_move_transient_peak_audit.json、examples/unrelated_machines/transient_peak_two_job_cycle.json与evidence/certificates/unrelated_machines/transient_peak_two_job_cycle.json。

## UM-FULL-DEGREE-MOMENT-DECODING-v1：全阶共同矩与负载局部化器的整数提取

- Exact Statement / Quantifiers：对任意合法二进制有理 `P`、`T≥0`，若给定次数至多 `2n+1` 的 Boolean/one-hot 泛函 `L`，满足次数 `n` 平方正性与每台机器次数 `n` 负载 localizer 正性，则存在真实 `T`-可行整数调度。
- Scope / Conclusion：`m_σ` 原子权重非负且总和1，超载原子权重为0；证书和原子族可指数大，不是位多项式算法或一般输入证书生成器。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; novelty/external review unverified；`UM-TARGET-v1`仍OPEN。
- Related Files：`research/current/unrelated_machines/full_degree_moment_localizer_decoding_bridge.md`、`research/reviews/unrelated_machines/full_degree_moment_localizer_review.md`、`tests/audits/unrelated_machines/full_degree_moment_and_saddle.py`。

## UM-HEAVY-LIGHT-SADDLE-CERTIFICATE-v1：重轻角色的自洽对偶证书与YES固定点边界

- Exact Statement / Quantifiers：固定 `T,β` 与 admissible heavy placement `H`。若 `λ*` 是残余 LP 的最优归一化对偶，且 `H` 全局最小化 `g(·,λ*)`，则 `H` 全局最小化所有 admissible placement 的残余 makespan；若 `R(H)≤T`，有序槽舍入输出 `(1+β)T`。
- Counterevidence / Objections：对任意 `β∈[1/2,1)` 存在 `OPT≤T` 的两机参数族，无 placement 满足该纯 saddle 条件；因此最佳响应循环不能当作一般选择器。
- Status：complete stated-scope conditional proof plus exact obstruction; independently attacked and audited; not a general hardness result；`UM-TARGET-v1`仍OPEN。
- Related Files：`research/current/unrelated_machines/heavy_light_saddle_certificate_and_cycle.md`、`research/reviews/unrelated_machines/heavy_light_saddle_certificate_review.md`、`tests/audits/unrelated_machines/full_degree_moment_and_saddle.py`。

## UM-INCIDENCE-FEEDBACK-EXACT-v1：机器—任务关联反馈边参数的精确阈值算法

- Exact Statement / Quantifiers：对任意合法 `P,T`，令有限关联图反馈边数 `b=|E|-|V|+c`。反馈边子集枚举、固定任务、删除未选反馈边后，剩余森林由叶交换精确求解；总时间 `2^b·poly(L)`，失败可靠蕴含 `OPT>T`。`b≤1` 时为总位多项式精确算法，任务支持度不受限。
- Scope / Conclusion：这是实际调度输出的 FPT 结构结果；一般 `b` 无界时不解决主目标，也不提供困难性。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; novelty/external review unverified；`UM-TARGET-v1`仍OPEN。
- Related Files：`research/current/unrelated_machines/incidence_cycle_rank_exact.md`、`research/reviews/unrelated_machines/incidence_cycle_rank_review.md`、`tests/audits/unrelated_machines/incidence_cycle_rank_exact.py`。

## UM-SUBLINEAR-CC-PROJECTION-GAP-v1：子线性联合投影的高围长近二边界

- Exact Statement：对任意 `r(s)=o(s)`（`s` 为机器数）及任意 `epsilon>0`，存在每任务恰两端、机器图简单且围长严格大于 `r(M)` 的实例 `P`，满足 `OPT(P)/T_CC_{r(M)}(P)>2-epsilon`。`CC_q` 采用长链正文的共同完整单机配置边际定义。
- Dependencies：`UM-LONG-PATH-GAP-v1` 的森林耦合、整数收缩和配置证书；机器数 `M_{k,ell}=A_k+B_k ell`，围长为 `2ell`。
- Scope / Limits：大小参数是机器数（或本族同阶关联边数），不是总二进制输入位长；这是固定 `r` 结果的对角量词加强，不是一般近二困难性。
- Status：自足 stated-scope proof；独立盲审待完成；外部优先权和新颖性未认证；`UM-TARGET-v1` 仍 OPEN。
- Related files：`research/current/unrelated_machines/sublinear_coalition_projection_high_girth_gap.md`、`tests/audits/unrelated_machines/sublinear_coalition_projection_gap.py`。

## UM-HEAVY-LIGHT-FOREST-INTEGRALITY-BARRIER-v1：重轻自洽 saddle 的森林整数补全边界

- Exact Statement：在 `T=1` 参数族中，中心任务在每台机器成本 `beta`、每机私有任务成本 `a=1-beta/m`；残余 LP 有 `R(H)=1` 及均匀价格的纯自洽 saddle，但任何整数分配的最大负载为 `a+beta=1+beta-beta/m`，可趋近 `2`。`T=3,beta=2/3,m=2` 是时间同时乘 `3` 的最小审计特例，且关联图为树、反馈秩为 `0`。
- Dependencies：`UM-HEAVY-LIGHT-SADDLE-CERTIFICATE-v1` 的残余对偶定义与 `UM-INCIDENCE-FEEDBACK-EXACT-v1` 的森林叶消元。
- Boundary：反例只否定“森林残余 + `R(H)≤T` 自动给整数补全”；森林阈值问题仍可由叶消元精确判定，不能升级为一般困难性。
- Status：自足 exact method boundary；独立盲审待完成；外部优先权未核查；`UM-TARGET-v1` 仍 OPEN。
- Related files：`research/current/unrelated_machines/heavy_light_forest_integrality_boundary.md`、`tests/audits/unrelated_machines/heavy_light_forest_integrality_boundary.py`。

## UM-ROW-UNIFORM-CORRELATED-GUARD-HALF-RETENTION-v2：相关单位请求的逐点半数共同匹配

- Exact Statement / Objects / Domain / Quantifiers：对任意显式二部simple图，每左非空有限标签、每右q=degree互异单位资源、每edge复合行全定义且均匀，同一左标签控制全部测试；确定性总位poly输出共同标签及合法F，逐点|F∩δ(u)|≥ceil(d_u/2)，含d0、d1与空图。
- Assumptions / Definitions：simple、资源按right分区、逐复合行均匀，详见正文；纯right标签列matching不推出uniform。
- Scope / Conclusion：只有该单位读出合同，不是一般UM困难性。原未登记scratch v1的floor结论由陈述先行审查加强，v2量词和ceil结论独立记录。
- Dependencies：显式合同、整数碰撞势和二部matching整数性；正文完整给出，不导入外部近似定理。
- Evidence / Counterevidence：361输入/943稳定profile Hall，删除simple或uniform有具体反例；有限运行不证明一般性。
- Status：完整限定证明、独立内部攻击通过、构造器已实现；外审、新颖性未认证。
- Related Files：`research/current/unrelated_machines/row_uniform_correlated_guard_rounding.md`、`research/reviews/unrelated_machines/row_uniform_correlated_guard_review.md`、`tests/audits/unrelated_machines/row_uniform_correlated_guard.py`、`evidence/runs/unrelated_machines/row_uniform_correlated_guard_audit.json`。

## UM-ROW-UNIFORM-FLAT-STATE-THREE-HALVES-v1：原平层状态矩阵的三二实际输出

- Exact Statement / Objects / Domain / Quantifiers：给定前项图表的显式flat编译，每state一parent、每左一unit selector、每state每incident edge一parent时间1/d及外端时间1的port，无其它任务。对全部这种原矩阵，确定性位poly输出全部sigma且Cmax≤3/2；非空selector给OPT≥1，空任务OPT0，故该子类三二近似。
- Assumptions / Definitions：保留retention-v2全部条件；显式结构随输入给出，不隐含任意P结构识别；空机器集添dummy。
- Scope / Conclusion：特殊完整原调度子类；不声称generalUM、零时间任意矩阵或该近似因子锐利。
- Dependencies：UM-MODEL-v1与UM-ROW-UNIFORM-CORRELATED-GUARD-HALF-RETENTION-v2，连同正文完整编译。
- Evidence / Counterevidence：6068原任务Fraction回算、三角32768合法调度枚举；去simple/uniform的原OPT分别7/4和2，只否定绝对上界延伸。
- Status：完整限定证明、陈述先行独立攻击通过、实际构造器实现；外审、新颖性未认证，UM-TARGET-v1正反面仍OPEN。
- Related Files：同上正文/审查/代码及`examples/unrelated_machines/row_uniform_correlated_guard_examples.json`。

## UM-PRIVATE-TREE-Q-VALUATION-v1：私有分叉估值的次可加性与精确signed需求

- Exact Statement / Conclusion：显式多state单射树的f=max q为次可加，任意有理signed价格可精确位poly输出真实demand集合与子树。
- Objects / Domain / Quantifiers：所有显式满k叉深h树，k,h≥1；全部有限非空state族与逐state单射叶资源像；仅第一项包括多state与任意signed有理价格，其余仅single-state；完整量词及全部约束见[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)。
- Assumptions / Definitions：同深真正r叉子树；minorant权重非负，f=max q；总位长支付显式树/全部叶地址，h0排除、k1链包括。
- Scope / Conclusion：树源表示与加性下包络工具，不是一般UM算法、近二计算困难性或配置gap。
- Dependencies：UM-PRUNED-TREE-LEAF-HITTING-v1与显式估值定义；第三项另用包络定义及标准精确有理LP可解性；共同前提见正文及超图。
- Evidence / Counterevidence or Objections：一般证明、陈述先行攻击及800子集等有限独立核验分开；generic LP优化未实现，单state LP不自动延伸max-state。
- Status：限定证明完整、内部独立重构与读后攻击通过；value/demand/分离实现，LP仅约束数据及给定支持扩展实现；外审、新颖性未认证。
- Related Files：[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)、[实际审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)、`tests/audits/unrelated_machines/private_tree_branching_valuation.py`、`evidence/runs/unrelated_machines/private_tree_branching_valuation_audit.json`、`examples/unrelated_machines/private_tree_branching_valuation_examples.json`。

## UM-TREE-Q-XOS-ENVELOPE-v1：全叶XOS包络与显式叶预算锐阶

- Exact Statement / Conclusion：单state E_q(L)=k^h/[k^h−(k−1)^h]；损失G在min(k,h)的1/2至1倍，叶预算B的最大损失阶logB/loglogB。
- Objects / Domain / Quantifiers：所有显式满k叉深h树，k,h≥1；全部有限非空state族与逐state单射叶资源像；仅第一项包括多state与任意signed有理价格，其余仅single-state；完整量词及全部约束见[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)。
- Assumptions / Definitions：同深真正r叉子树；minorant权重非负，f=max q；总位长支付显式树/全部叶地址，h0排除、k1链包括。
- Scope / Conclusion：树源表示与加性下包络工具，不是一般UM算法、近二计算困难性或配置gap。
- Dependencies：UM-PRUNED-TREE-LEAF-HITTING-v1与显式估值定义；第三项另用包络定义及标准精确有理LP可解性；共同前提见正文及超图。
- Evidence / Counterevidence or Objections：一般证明、陈述先行攻击及800子集等有限独立核验分开；generic LP优化未实现，单state LP不自动延伸max-state。
- Status：限定证明完整、内部独立重构与读后攻击通过；value/demand/分离实现，LP仅约束数据及给定支持扩展实现；外审、新颖性未认证。
- Related Files：[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)、[实际审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)、`tests/audits/unrelated_machines/private_tree_branching_valuation.py`、`evidence/runs/unrelated_machines/private_tree_branching_valuation_audit.json`、`examples/unrelated_machines/private_tree_branching_valuation_examples.json`。

## UM-TREE-Q-MINORANT-LP-v1：单状态加性minorant的分离与紧凑LP

- Exact Statement / Conclusion：补集最小blocking树给精确强分离；O(k|V|)紧凑LP投影恰为A(q)，指定集合可标准有理LP精确求E。
- Objects / Domain / Quantifiers：所有显式满k叉深h树，k,h≥1；全部有限非空state族与逐state单射叶资源像；仅第一项包括多state与任意signed有理价格，其余仅single-state；完整量词及全部约束见[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)。
- Assumptions / Definitions：同深真正r叉子树；minorant权重非负，f=max q；总位长支付显式树/全部叶地址，h0排除、k1链包括。
- Scope / Conclusion：树源表示与加性下包络工具，不是一般UM算法、近二计算困难性或配置gap。
- Dependencies：UM-PRUNED-TREE-LEAF-HITTING-v1与显式估值定义；第三项另用包络定义及标准精确有理LP可解性；共同前提见正文及超图。
- Evidence / Counterevidence or Objections：一般证明、陈述先行攻击及800子集等有限独立核验分开；generic LP优化未实现，单state LP不自动延伸max-state。
- Status：限定证明完整、内部独立重构与读后攻击通过；value/demand/分离实现，LP仅约束数据及给定支持扩展实现；外审、新颖性未认证。
- Related Files：[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)、[实际审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)、`tests/audits/unrelated_machines/private_tree_branching_valuation.py`、`evidence/runs/unrelated_machines/private_tree_branching_valuation_audit.json`、`examples/unrelated_machines/private_tree_branching_valuation_examples.json`。

## UM-PRIVATE-TREE-GLOBAL-XOS-LOSS-v1：任意目标集合的锐XOS损失与实际加性支持

- Exact Statement / Conclusion：对每个S构造全域有效w≤f，w(S)≥f(S)/G(k,h)，G=k[1−(1−1/k)^h]逐参数锐；不需精确minorant分离。
- Objects / Domain / Quantifiers：全部显式k,h≥1满树、多state单射叶资源、每个S⊆U，量化全部B的minorant有效性。
- Assumptions / Definitions：f=max_a q_a；A(f)与E_f按全部资源子集定义；signed demand、强分离、指定0/1集合优化分别处理。
- Scope：源估值到XOS下支持的锐定量桥，非资源分配算法。
- Dependencies：UM-PRIVATE-TREE-Q-VALUATION-v1、UM-TREE-Q-XOS-ENVELOPE-v1及共同显式输入。
- Evidence / Counterevidence or Objections：一般证明及实际陈述先行独立重构/读后攻击；没有新生产接口或有限运行。图类已explicit XOS，所以不能把分离困难性错称指定集合包络困难。
- Status：限定证明完整与内部攻击通过；外审、新颖性未认证；主目标正反面未变。
- Related Files：[完整正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)、[实际审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)。

## UM-MULTISTATE-Q-MINORANT-GRAPH-HARDNESS-v1：最浅多状态全minorant域的图计算困难性

- Exact Statement / Conclusion：k2h1图边states，即使uniform正权且总重<2，nonminorant NP完全、membership coNP完全；但E_f(S)=f(S)及value/demand均易解。
- Objects / Domain / Quantifiers：全部无孤立非空简单图G，每edge一k2h1双叶state，全部非负有理w；困难性子类w=uniformλ>0且|V|λ<2。
- Assumptions / Definitions：f=max_a q_a；A(f)与E_f按全部资源子集定义；signed demand、强分离、指定0/1集合优化分别处理。
- Scope：标准IS归约嵌入全minorant域；NP/coNP区别与全输入停机合同明确；不是UM近似hardness。
- Dependencies：显式k2h1图模型、Karp1972 CLIQUE/补图Independent Set Paper Fact、标准精确有理LP。
- Evidence / Counterevidence or Objections：一般证明及实际陈述先行独立重构/读后攻击；没有新生产接口或有限运行。图类已explicit XOS，所以不能把分离困难性错称指定集合包络困难。
- Status：限定证明完整与内部攻击通过；外审、新颖性未认证；主目标正反面未变。
- Related Files：[完整正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)、[实际审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)。

## UM-TREE-Q-ONE-THRESHOLD-MINORANT-v1：单位色类划分与单阈值支持域

- Exact Statement / Conclusion：任意A的q值等于q≤1最少划分数，输出实际色类；非负minorant只须检验最大单位色类权≤1，等价C_(k−1)≥W−1；O(V)变量/约束/非零系数扩展LP精确。
- Objects / Domain / Quantifiers：single-state全部显式k,h≥1满树、全部叶集合及非负权重；k1单叶另列，h0排除。
- Assumptions / Definitions / Scope：真正同深分叉、非负加性minorant；仅single-state，不延伸max-state域，不是调度hardness。
- Dependencies：显式q定义、UM-PRIVATE-TREE-Q-VALUATION-v1、UM-PRUNED-TREE-LEAF-HITTING-v1、minorant定义与标准精确有理LP；所有共同前提见[自足正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)。
- Evidence / Counterevidence or Objections：实际陈述先行独立重构和冻结证明读后攻击；消Z非负系数、F叶0及全部非零计数专核；旧代码未修改，无新generic LP运行。
- Status：限定证明完整，内部两阶段攻击通过；新增构造未实现，外审及新颖性未认证。
- Related Files：[正文](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)、[审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)。

## UM-COTRANSVERSAL-UNIFORM-CONFIG-SHARP-GAP-v1：每个配置均独立的余横截共同保留锐间隙

- Exact Statement / Conclusion：显式D≥3,m=D+1族，每C独立M且uniform边际属于P(M)，但最优min保留1/D；普通UM有Tconf1、真OPT2−1/D。
- Objects / Domain / Quantifiers：所有整数D≥3的显式g/A/B+mandatory L族，m=D+1。
- Assumptions / Definitions：配置C、vacancy M=N*、真实β*与完整原矩阵均在[正文](../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)精确定义；不得把fractional βLP当β*。
- Scope：限定配置/marginal舍入gap，不是计算困难性，实例OPT闭式易算。
- Dependencies：显式原P/集合对象、标准transversal dual/Hall；不调用未解oracle。
- Evidence / Counterevidence or Objections：陈述先行与后读冻结证明内部攻击；D3/D4全部原P/配置/匹配和81/7776模式有限checks；pure右列完整源不由此编译。
- Status：限定证明完整与独立攻击通过；显式家族实现与冻结有限证据。外审/新颖性未认证，主目标正反面不变。
- Related Files：[正文](../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)、[实际审查](../reviews/unrelated_machines/uniform_port_parking_matroid_review.md)、`tests/audits/unrelated_machines/cotransversal_uniform_configuration_gap.py`、`evidence/runs/unrelated_machines/cotransversal_uniform_configuration_gap_audit.json`。

## UM-UNIFORM-PORT-PARKING-PAPER-APPROX-v1：统一D端口加任意unit停车的真实次二推论

- Exact Statement / Conclusion：统一D、固定外资源ports、任意mandatory unit aux且parents/external分离时，由BLMRS Thm4得实际2−1/(4+η)近似；Baux≥2或U空分支精确。
- Objects / Domain / Quantifiers：任意显式共同D≥1 states/ports与任意外部unit aux，固定有理η>0；全输入含U空及aux B≥2。
- Assumptions / Definitions：配置C、vacancy M=N*、真实β*与完整原矩阵均在[正文](../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)精确定义；不得把fractional βLP当β*。
- Scope：published Theorem4的相对实际OPT推论，统一D和parent/external分离承重；不是一般UM算法。
- Dependencies：显式原P/集合对象、标准transversal dual/Hall；另用Rado lifting、标准matroid intersection及BLMRS v1 Def7/Thm4。
- Evidence / Counterevidence or Objections：陈述先行与后读冻结证明内部攻击；没有实现BLMRS通用算法；图族LPgap2不反驳相对OPT近似。
- Status：限定证明完整与独立攻击通过；数学归约与实际σ构造可算，source算法未集成。外审/新颖性未认证，主目标正反面不变。
- Related Files：[正文](../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)、[实际审查](../reviews/unrelated_machines/uniform_port_parking_matroid_review.md)、`tests/audits/unrelated_machines/cotransversal_uniform_configuration_gap.py`、`evidence/runs/unrelated_machines/cotransversal_uniform_configuration_gap_audit.json`。

## UM-NEAR-UNIT-PCSP-EXACT-MINION-v1：近单位蕴含promise的精确winning-set minion

- Exact Statement / Conclusion：固定k≥2、1≤r≤k−1时，Pol恰为非空单调相交winning族且全部minwinner大小≤k−r；同一minwinner双侧fixing，不保证bounded essential arity。
- Objects / Domain / Quantifiers：固定k≥2、1≤r≤k−1，底集0/1；全部正有限arity函数/全部一般PCSP实例；变量可任意重复，无physical次数/类型保证。
- Assumptions / Definitions：strict b0或≥k−1 out，weak b0或≥r out，加exact AMO2/ONE；单调winning族、minimal指inclusion-minimal。
- Scope：unrestricted source；不是实际UM gap，不是主目标反面。
- Dependencies：仅显式模板与正文自足有限矩阵证明。
- Evidence / Counterevidence or Objections：实际先陈述独立重构、原始定理相关页读取、后读canonical攻击；r1 purearc flow与一般hard不矛盾；ordinaryFeder投影的weak cube不能补物理编译。
- Status：限定证明完整、内部独立攻击通过；没有新实现/有限审计，外审/新颖性未认证，physical compiler OPEN。
- Related Files：[自足正文](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)、[实际审查](../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)、原始文献与manifest。

## UM-NEAR-UNIT-PCSP-UNRESTRICTED-HARDNESS-v1：强fixing导入的一般PCSP困难性

- Exact Statement / Conclusion：对每个固定k,r，A_k→B_k,r加exact AMO2/ONE的unrestricted PCSP NP-hard；没有保持physical two-occurrence/端口类型的归约。
- Objects / Domain / Quantifiers：固定k≥2、1≤r≤k−1，底集0/1；全部正有限arity函数/全部一般PCSP实例；变量可任意重复，无physical次数/类型保证。
- Assumptions / Definitions：strict b0或≥k−1 out，weak b0或≥r out，加exact AMO2/ONE；标准deterministic polynomial many-one promise hardness；P≠NP仅无poly求解器推论使用。
- Scope：unrestricted source；不是实际UM gap，不是主目标反面。
- Dependencies：UM-NEAR-UNIT-PCSP-EXACT-MINION-v1及BBKO v3 Def5.16/Prop5.17；identity homomorphism与固定C共同满足。
- Evidence / Counterevidence or Objections：实际先陈述独立重构、原始定理相关页读取、后读canonical攻击；r1 purearc flow与一般hard不矛盾；ordinaryFeder投影的weak cube不能补物理编译。
- Status：限定证明完整、内部独立攻击通过；没有新实现/有限审计，外审/新颖性未认证，physical compiler OPEN。
- Related Files：[自足正文](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)、[实际审查](../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)、原始文献与manifest。

## UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1：多小端关联度流的实际五三边界

- Exact Statement / Conclusion：全部P可实际输出C≤B+F/k≤B+maxceilrho/k；small行≤k且每非unit-only job至少D≥2个small端时为unknownOPT 1+ceil(k/D)/k≤5/3；d_j≥k时strict1+1/k iff unit-only可单匹配。
- Objects / Domain / Quantifiers：{1,1/k}、k≥2；B为unit-only最小计数瓶颈，F为其余仅small最小瓶颈，rho_i=sum1/d_j。 对全部满足域的显式输入，不由有限实验量化。
- Definitions / Assumptions：全部原任务恰一个合法端，实际负载按原机回算；共同b/k及见证条件不能略去；相关符号在正文完整定义。
- Scope：限定完整算法、阈值表示或给定两actual见证的局部接口；不解决一般UM主目标正反面。
- Dependencies：正文自足单位容量/整数二部流与逐机计数或配对证明；不导入一般PCSP困难性。
- Evidence / Counterevidence or Objections：真实先陈述独立重构、后读冻结全文；没有新通用生产实现；数学实际构造与实现状态分开。
- Status：限定证明完整、内部攻击无standing fatal；implementation=none，外审/全球新颖性未认证。
- Related Files：[自足正文](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)、[实际审查](../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。

## UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1：三端单位选择器的精确阈值正规形

- Exact Statement / Conclusion：二叉私有单位树使每newjob为一q<b端加unit端或unit-only至多3端；forward≤max(b,C)，任意newC<2b反投影逐原机不增；非空OPTnew=min(2b,max(b,OPTold))，两值small关联数保留。
- Objects / Domain / Quantifiers：任意合法P，给正有理b且每有限p≤b；允许zero/empty/单端，普通完整sigma。 对全部满足域的显式输入，不由有限实验量化。
- Definitions / Assumptions：全部原任务恰一个合法端，实际负载按原机回算；共同b/k及见证条件不能略去；相关符号在正文完整定义。
- Scope：限定完整算法、阈值表示或给定两actual见证的局部接口；不解决一般UM主目标正反面。
- Dependencies：正文自足单位容量/整数二部流与逐机计数或配对证明；不导入一般PCSP困难性。
- Evidence / Counterevidence or Objections：真实先陈述独立重构、后读冻结全文；规范transform/forward/project实现与9关键例13原σ/116新τ/29投影精确复跑；一般证明不依赖有限checks。
- Status：限定证明完整、内部攻击无standing fatal；implementation=implemented，外审/全球新颖性未认证。
- Related Files：[自足正文](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)、[实际审查](../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。

## UM-TARGET-TERNARY-SELECTOR-EQUIVALENCE-v1：一般UM与三端单位选择器的统一次二算法等价

- Exact Statement / Conclusion：UM-TARGET成立 iff 正规类有某统一确定性位poly actual次二算法；反向先zero处理，再L=max minp,U=sum minp≤nL的常数有理比率尺度，实际C<2b才投影，余量仍固定正。
- Objects / Domain / Quantifiers：一般UM全输入含OPT0；正规类随输入给定共同b>0，全部SU端q<b或unit-only arity≤3。 对全部满足域的显式输入，不由有限实验量化。
- Definitions / Assumptions：全部原任务恰一个合法端，实际负载按原机回算；共同b/k及见证条件不能略去；相关符号在正文完整定义。
- Scope：主目标的算法存在等价表示，未给任一边的求解器或hardness。
- Dependencies：UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1与正有理尺度搜索，缺少normal-class求解器。
- Evidence / Counterevidence or Objections：真实先陈述独立重构、后读冻结全文；没有新通用生产实现；数学实际构造与实现状态分开。
- Status：限定证明完整、内部攻击无standing fatal；implementation=none，外审/全球新颖性未认证。
- Related Files：[自足正文](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)、[实际审查](../reviews/unrelated_machines/near_unit_implication_pcsp_review.md)。

## UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1：两测量单位占位读出的逐k锐胶合界

- Exact Statement / Conclusion：任意两mixed真实sigma可位poly构造C≤B(k)=1+ceil((k+2)/2)/k；四机2k+6job族两mixed真OPT=B(k)。k2/3 B2，k≥4≤9/5，B≤3T/2。
- Objects / Domain / Quantifiers：任意{1,1/k}原P，k≥2，给两完整actualσ≤1+1/k；两不同原机presence00/11，资格arity/行关联数不限。 对全部满足域的显式输入，不由有限实验量化。
- Definitions / Assumptions：全部原任务恰一个合法端，实际负载按原机回算；共同b/k及见证条件不能略去；相关符号在正文完整定义。
- Scope：限定完整算法、阈值表示或给定两actual见证的局部接口；不解决一般UM主目标正反面。
- Dependencies：正文自足单位容量/整数二部流与逐机计数或配对证明；不导入一般PCSP困难性。
- Evidence / Counterevidence or Objections：真实先陈述独立重构、后读冻结全文；没有新通用生产实现；数学实际构造与实现状态分开。
- Status：限定证明完整、内部攻击无standing fatal；implementation=none，外审/全球新颖性未认证。
- Related Files：[自足正文](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)、[实际审查](../reviews/unrelated_machines/unit_presence_two_witness_gluing_review.md)。

## UM-TWO-MEASUREMENT-TINY-PRESENCE-GLUING-v1：任意tiny时间单位占位的三半系数胶合

- Exact Statement / Conclusion：任意两mixed actualσ可确定性总位poly构造≤3T/2；unit匹配+两选择加权半整化。a<1/3绝对<2；odd reciprocal a→0族恰3T/2，a1/3可恰2；不是每单独a逐参数锐。
- Objects / Domain / Quantifiers：有限p属于{1}∪[0,a]，给有理0≤a<1、两完整actualσ≤T1+a、两测量00/11；无arity/行数/time-consistency限制。 对全部满足域的显式输入，不由有限实验量化。
- Definitions / Assumptions：全部原任务恰一个合法端，实际负载按原机回算；共同b/k及见证条件不能略去；相关符号在正文完整定义。
- Scope：限定完整算法、阈值表示或给定两actual见证的局部接口；不解决一般UM主目标正反面。
- Dependencies：正文自足单位容量/整数二部流与逐机计数或配对证明；不导入一般PCSP困难性。
- Evidence / Counterevidence or Objections：真实先陈述独立重构、后读冻结全文；没有新通用生产实现；数学实际构造与实现状态分开。
- Status：限定证明完整、内部攻击无standing fatal；implementation=none，外审/全球新颖性未认证。
- Related Files：[自足正文](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)、[实际审查](../reviews/unrelated_machines/unit_presence_two_witness_gluing_review.md)。

## UM-LIST-AGREEMENT-DEGREE-BUDGET-v1：列表agreement的度数预算与逐图锐阈值

- Exact Statement / Conclusion：确定性actual lists agr≥L(D−1)/(2d+L(D−1))；L≥ceil2d/D可整数流全agree，且此通用整数阈值在每固定图上有多项式地图锐例；低soundness须d/L≥(D−1)(1−alpha)/(2alpha)。
- Objects / Domain / Quantifiers：显式simple (d,D)-biregular projection图，B非空、d≥1、D≥2、逐right公共像非空；binary L≥1，lists大小≤L。 对所有该输入；sharp地图一次排除全部低于阈值的L。
- Definitions / Assumptions：agreement必须两个不同左邻居的列表像相等；局部公共像不等于全局YES；不假设原像互异，不量化平行incidence图。
- Scope：源预算的确定性组合地板；全agreement整数阈值锐，不声称分数界锐；非LabelCover/UM困难性及非physical compiler。
- Dependencies：显式对象、饱和ticket计数、标准整数二部流；Moshkovitz final仅为对接源定义和局部预算背景，不承重证明本结论。
- Evidence / Counterevidence or Objections：true statement-first独立重构后全文读后攻击，无standing fatal；没有生产实现或有限实验代替证明；binary巨大L不按数值循环。
- Status：限定证明完整、内部审查完成；implementation=none；外审与新颖性未认证，UM-TARGET仍OPEN。
- Related Files：[自足正文](../current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)、[实际审查](../reviews/unrelated_machines/list_agreement_degree_budget_review.md)。

## UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2：部分MinRep线性度数源与真实费用桥

- Exact Statement / Conclusion：给定val≤rho³/(10^9g^8)，随机位poly删边使最大度Δ=1000ceil(1000gλ/(rho floorlog2g))；好NO非空且全部cost≤gN列表cover<rho，概率≥0.9；perfect YES每seed保留。固定参数PCP下Q=poly_rho(g)、Δ=O_rho(g)，同覆盖禁令必需Δmax>(2g−1)/rho。 同覆盖禁令必须M>(g−1/2)N/rho。固定rho、c下，若真实decoder另给cover≥rhoM、cost≤N+B/F、B≤cM，F≥cΔ/[2(g−1)]为一个充分固定费用。
- Objects / Domain / Quantifiers：显式平衡D-regular全投影游戏，平行约束逐条计；binary g≥2、0<rho≤1，N≥2，Q≥2；cost为全部顶点列表总大小。 对每个显式合法游戏及参数；NO同时量化全部廉价lists。PCP结论先固定g,rho再归约SAT，输出图不必regular。
- Definitions / Assumptions：YES val1每seed保留；NO val≤gamma按源值量化、成功概率至少0.9且非空。投影全映射、平衡、列表可空及独立采样不能略。
- Scope：源定理、度数阶必要性、条件物理费用代数；非实际UM归约或主目标反证。随机源判别器矛盾采用NP不包含BPP，未用仅P≠NP。
- Dependencies：自足heavy截长、列表生成函数、rare covered上尾和一次总边数事件、条件Markov删边；固定参数源另用Mosh final Thm2.1/2.3和DS Thm1.1、精确保value正规化。实际fee前提未提供。
- Evidence / Counterevidence or Objections：两份Exact-first独立重构后全文攻击无standing fatal；root实核primary前提。无生产实现、有限实验或新颖性认证；F1不由degree下界绝对排除。
- Status：限定source证明完整、内审完成；implementation=none，外审/全球新颖性未认证；UM-TARGET正反面OPEN。
- Related Files：[正文](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)、[实际审查](../reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md)。

## UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v4：坐标切片源编译的精确阈值与双射反例

- Exact Statement / Conclusion：strictP≤1 iff fullLC；linear-degree cheap-list NO显式家却OPT=1+1/D；proper-color private-output padding保NO仍低C；随机conditioned-bijection族至少1/2概率同NO，每seed Tconfig1/实际C≤1+1/D，好NO整数OPT精确。 完整定量参数、所有机器/任务及概率量词见正文；每seed与好NO事件区分。
- Objects / Domain / Quantifiers：simple平衡Dregular全投影源、D≥3、共同Q≥2；明确坐标slice叶/完整树port矩阵；显式展开。padding和随机双射族各按正文附加参数。 显式NO家全部g≥2、rho∈(0,1]、D>max(2,2g/rho)、t≥1；general padding要求rho0+2g/D≤rho；permutation族Dceil16g/rho,Q≥max(2D+1,ceil((100g²/rho)^4))。
- Assumptions / Definitions：每state叶单射，slice必须有完整Q−1坐标；active机器全部port负载、inactive所有states和资源机同算。CONFIG证书不是实际sigma；随机源仅存在非hardness。
- Scope：限定明确编译的source-to-weak-decoder反例；严格阈值与OPT/Tconfig的精确小gap，不是near2困难性或一般q算法。
- Dependencies：坐标模型、单位selector逐层传播、token计数、proper coloring、Bernoulli上尾/列表计数、双射配置计数和1/D网格；无外部PCP假设。
- Evidence / Counterevidence or Objections：真实Exact-first独立重构后冻结proof/完整canonical攻击无standing fatal；root读独立小审计并全复跑一致。有限数据不满足概率NO参数，不核NO或OPT。parallel和变参数树展开不在合同。
- Status：限定证明完成、内审完成；implementation=audit_only；外审/新颖性未认证；实际主目标hardness未得。
- Related Files：[正文](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)、[实际审查](../reviews/unrelated_machines/private_tree_branching_valuation_review.md)、代码和冻结输出互链。


## UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3：复制列表同时性的正规高围长部分MinRep源

- Exact Statement / Conclusion：随机硬位poly返回FAIL或simple平衡exact dregular/girth>G投影源；d=ceil(1000gλ/(rho floorlog2g))，N′=Nt,M′=dN′/2；FAIL<.1，val≤gamma时≥.8概率全部cheap copylists cover<rho；YES每nonFAIL保真。固定参数PCP下Q=poly_rho(g),d=O_rho(g)。 完整z,t、bounded rejection、same-type/layer repair和概率量词见正文；非FAIL每seed满足结构，NO同时量化所有lists。
- Objects / Domain / Quantifiers：固定G≥2；显式平衡Dregular无权全投影游戏可有parallel types；binary g≥2、0<rho≤1，Q≥2且Qrho³≥10^9g^8；copies可独立选lists，总cost≤gN′。 G预先固定；PCP链先固定g,rho,G，显式游戏变换另有统一binary位复杂度。
- Definitions / Assumptions：gamma=rho³/(10^9g^8)，每type继承原全投影；各copy lists可完全不同。FAIL是flag、可由调用者作YES分支，不伪装成合法girth源；非空val≤gamma蕴含Qgamma≥1。
- Scope：线性degree、simple、正则和固定高围长的随机部分覆盖源；不是实际UM reduction、任意cover保soundness或主目标反证。确定性promise判别器仅导出NP⊆BPP。
- Dependencies：显式regular投影模型；heavy-copy随机代表、生成函数、两侧permutation点态密度/factorial moments、shortcycle暴露、保类型交换；固定参数PCP另用已有Mosh/DS及精确保value正规化/padding。Kun/DKR只比较不承重。
- Evidence / Counterevidence or Objections：两份Exact-first独立witness重构，后读作者factorial-moment全文均无standingfatal；sampling保守多计与z不等号笔误在新读后记录纠正、旧字节冻结。
- Status：一般限定source证明完成、内审完成；implementation=none；外审、新颖性未认证；实际fee和weak decoder缺，UM-TARGET正反面OPEN。
- Related Files：[同专题正文](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)、[实际审查](../reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md)与六份保真来源。


## UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5：任意typed源的度数质量复制正规化

- Exact Statement / Conclusion：t_v=deg(v)z质量复制，N′=2M0z,M′=dN′/2；随机硬位poly输出FAIL或simple balanced exactdregular girth>G，保原typed表/equalfibers；FAIL<.1，val≤gamma时≥.8概率全cost≤gN′copylists cover<rho；perfect每nonFAIL保真。fixed-error PCP不需原regular/degree常数；Qpoly(g)才另得dO(g)。 d=ceil(1000gλ/(rho floorlog2g))，gamma=rho³/(10^9g^8)；完整z及bounded采样/repair见同专题正文。
- Objects / Domain / Quantifiers：固定G≥2；任意非空显式无权二部multigraph，原degree/两侧大小不限；非空typed ΣA,ΣB明确列举，全π:ΣA→ΣB；binaryg≥2,rho∈(0,1],Q=max域大小≥2且Qgamma≥1。 同时量化全部copies独立lists，成本不需按原degree加权；先删孤点，M0≥1。
- Assumptions / Definitions：G预先固定；FAIL明确flag；typed反向不伪造为函数。新source标签clone若用须逐符号计cost、Qλd按新域算，仅fixed-parameter PCP corollary可作域外padding。
- Scope：一般显式源的随机正规化，保exact kfibers；调用FMW新preprint Paper Fact给exact4源。不是UM reduction；随机判别器矛盾采用NP不包含BPP。
- Dependencies：任意typed投影模型、质量抵消heavycopy界、已证异长permutation density/factorialmoment和短cycle按起始v求和、same-type修复；固定PCP应用另用其精确外部定理，未免费导入regular。
- Evidence / Counterevidence or Objections：v4空alphabet使val未定义，保真原Exact记录失败；v5显式两域非空，两个先陈述独立推导后读冻结proof无standingfatal；root核原文指定页与proof，不声称全球新颖或全PCP重审。
- Status：限定证明完成、内审完成；implementation=none，外审/新颖性未认证；无真实UM费用或weak decoder。
- Related Files：[同专题正文](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)、[实际审查](../reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md)、来源及文献manifest。


## UM-Q-PRIVATE-INJECTIVE-TREE-CONFIGURATION-FLOOR-v2：私有注入树的全配置五三界

- Exact Statement / Conclusion：共同CONFIG(T)导出a=d−floor(d(T−1))叉树分布；若(a−r+1)^h≥2r^h−1则actualC≤2−r/d，故注入类配置gap≤5/3；一般原菜单过滤给严格(OPT≤1,OPT>5/3)确定性位poly判定，不输出σ。 A另给CONFIG1 iff共同full-state λ，按叶multiplicity计；T≥2由全父置C≤2补齐。完整定理及证明见[正文](../current/unrelated_machines/private_injective_tree_configuration_floor.md)。
- Objects / Domain：显式均匀d叉高h私有state树，任意非空有限菜单，selector与下端unit1、父端1/d；每leaf唯一外机；B要求每完整state叶map单射，C允许非注入。 U非空得Tconf≥1；空U单列OPT0/空σ。所有state/tree/jobs资格显式付费，不处理隐式巨大树。
- Quantifiers：∀d,h≥1、∀完整显式P、∀可行有理T与满足条件的r；∃针对全部原jobs的真实σ。C另∃确定性位poly判定器，∀其严格promise输入，非σ算法。
- Assumptions / Definitions：无额外任务/预载，不同state内部机器互异；Haxell超边每root加r^h个不同资源，资源transversal对全部root子集量化；共同分布与capacity不逐叶重选。
- Scope：限定结构配置界、严格promise decision及编译方法限制；非一般UM、非非注入配置gap、非近二困难性、非5/3锐界。
- Dependencies：UM-PRUNED-TREE-LEAF-HITTING-v1；显式模型；Haxell匹配PaperFact（AFS2008 Thm2/Annamalai2016 Thm1.1）；有理LP/均匀matroid分解；正文自足共同a树桥与原P回填。
- Evidence / Counterevidence：两个陈述先行独立重构后读作者proof无standingfatal；root亲核primary准确rank及所有原jobs。粗Σt≥aq不足，非注入叶打断阻断计数；共享internals/nonuniform等结构不在域。无有限测试代证明。
- Status：proof complete；internal review multiple audits；implementation none；external review/novelty unverified；UM-TARGET-v1OPEN。
- Related Files：[正文](../current/unrelated_machines/private_injective_tree_configuration_floor.md)、[实际审查](../reviews/unrelated_machines/private_injective_tree_configuration_floor_review.md)、assets中的冻结原字节及文献manifest。


## UM-PRIVATE-TERNARY-RAINBOW-BINARY-SUBTREE-NP-COMPLETE-v1：完整三叉树二叉彩虹的精确困难性

- Exact Statement / Conclusion：判定binary rainbow NP完全；确定性3SAT归约hO(logs)/完整sizepoly；原small1/3-unit1私有树加单端rootpin给YES actual≤4/3、NO OPT=5/3，任意<5/3σ可poly解码；比值仅5/4。 不是任意δ或near2困难性。
- Objects / Domain：显式完整三叉rooted树，h≥1随输入增长，所有叶深h、重复颜色允许；full binary rooted同深子树要求全部选中叶颜色单射。 颜色binaryID，输入含全部tree/leaf字节，q至少1。
- Quantifiers：∀显式3SAT输入Φ，∃确定性many-one输出完整tree，统一绝对C满足h≤Clog₂(s+2)、size≤(s+2)^C；SAT iff有rainbow2。∀原P低负载σ，完整提取真实binary子树。
- Assumptions / Definitions：导入Karp标准3SAT NP-completeness；树/颜色源结论无复杂度假设，NP-hardness排算法另用P≠NP。原P内部私有，重复color仅合外机，pin单端，其余job恰父small/唯一unit下端。
- Scope：noninjective且height变参的锚点，NP难可行性与小比值调度gap；非主目标、非固定height困难性、非5/3配置gap反例。
- Dependencies：Karp1972 MainTheorem/item11 PaperFact；自足coloredAND/OR、Rigid/Dead/Pad完整构造；原P逐机回填与<5/3提取。
- Evidence / Objections：作者Exact先冻，cover仅陈述重构另一完整归约后读作者proof无fatal，root亲核全部gate/位复杂度/原jobs；pin资格文字已在canonical修正、旧字节保留。leaf比例递减不推出分叉gap。
- Status：proof complete；internal review actual independent reconstruction/read-after；implementation none；external review/novelty unverified。
- Related Files：[正文](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)、[实际审查](../reviews/unrelated_machines/ternary_rainbow_subtree_exact_hardness_review.md)、assets/crosswalk冻结来源。


## UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3：有界重数的全配置离二界

- Exact Statement / Conclusion：所有CONFIG(T)整数gap≤2−1/(μ+2)；更精确r条件[a−μ(r−1)]^h≥2r^h−1给actual2−r/d。局部rainbow ceil(a/μ)与逆像blocker桥均证明；只σ存在，不是变参poly输出。
- Objects / Domain：完整私有uniform1/d-unit1树，每完整state每resource实际重数≤binaryμ≥1，任意d,h/menus显式。 所有原jobs和资格不删；空任务另0，不套selector下界。
- Quantifiers / Assumptions：完整数学量词、零/边界和外部依赖见[同专题正文](../current/unrelated_machines/private_injective_tree_configuration_floor.md)；复杂性仅调用准确标准3SAT PaperFact，配置存在性用既核Haxell，不能互换结论。
- Definitions / Scope：按actual multiplicity计共同预算；sharp G取同一完整类sup且未必达到；NP2是全局颜色重数，不偷换成逐state重数。结构类结果非UM一般正反面，implementation none。
- Dependencies：完整boundedμ模型、raw q子可加和叶blocker、共同CONFIG(T)非注入a树支配、准确Haxell资源侧rank。
- Evidence / Counterevidence：新Exact先冻结、仅陈述独立重构后全文读proof；root亲核实际记录。v3退化d1措辞已附可行前提；NP旧高重模板不能自动导入；G平星可直接解故非hardness。
- Status：proof complete；actual two-stage internal review；external review/novelty unverified；implementation none。
- Related Files：[正文](../current/unrelated_machines/private_injective_tree_configuration_floor.md)、[审查](../reviews/unrelated_machines/private_injective_tree_configuration_floor_review.md)、assets/crosswalk冻结原字节。


## UM-PRIVATE-TREE-MULTIPLICITY-GAP-ASYMPTOTIC-v1：重数参数的一阶锐渐近

- Exact Statement / Conclusion：2−1/μ≤G(μ)≤2−1/(μ+2)，误差≤2/[μ(μ+2)]，lim整数μ→∞ μ(2−G)=1；一层μ-state平星精确Tconf1/OPT2−1/μ。不是固定μ精确G或算法困难性。
- Objects / Domain：同boundedμ完整结构类Cμ，μ≥2；G(μ)对全部d,h/menus/输入长的OPT/Tconf取sup。 所有原jobs和资格不删；空任务另0，不套selector下界。
- Quantifiers / Assumptions：完整数学量词、零/边界和外部依赖见[同专题正文](../current/unrelated_machines/private_injective_tree_configuration_floor.md)；复杂性仅调用准确标准3SAT PaperFact，配置存在性用既核Haxell，不能互换结论。
- Definitions / Scope：按actual multiplicity计共同预算；sharp G取同一完整类sup且未必达到；NP2是全局颜色重数，不偷换成逐state重数。结构类结果非UM一般正反面，implementation none。
- Dependencies：同域G定义、v3全阈值上界、显式平星族的自足精确分析。
- Evidence / Counterevidence：新Exact先冻结、仅陈述独立重构后全文读proof；root亲核实际记录。v3退化d1措辞已附可行前提；NP旧高重模板不能自动导入；G平星可直接解故非hardness。
- Status：proof complete；actual two-stage internal review；external review/novelty unverified；implementation none。
- Related Files：[正文](../current/unrelated_machines/private_injective_tree_configuration_floor.md)、[审查](../reviews/unrelated_machines/private_injective_tree_configuration_floor_review.md)、assets/crosswalk冻结原字节。


## UM-PRIVATE-TERNARY-RAINBOW-MULTIPLICITY-THRESHOLD-v2：全局叶重数二三复杂性门槛

- Exact Statement / Conclusion：重数≤2全部存在binary rainbow；重数≤3仍NP完全，3SAT归约hO(logs)/全输出poly，原P资源资格≤3、YES≤4/3/NO5/3。精确门槛非near2。
- Objects / Domain：显式完整同深三叉树，整棵tree每叶色全局出现次数≤2或≤3；所有原/辅助色均计入。 所有原jobs和资格不删；空任务另0，不套selector下界。
- Quantifiers / Assumptions：完整数学量词、零/边界和外部依赖见[同专题正文](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)；复杂性仅调用准确标准3SAT PaperFact，配置存在性用既核Haxell，不能互换结论。
- Definitions / Scope：按actual multiplicity计共同预算；sharp G取同一完整类sup且未必达到；NP2是全局颜色重数，不偷换成逐state重数。结构类结果非UM一般正反面，implementation none。
- Dependencies：raw树q子可加、Karp3SAT源、低重数新Dead/Rigid/protected或独立Must/Fresh、原P阈值提取。
- Evidence / Counterevidence：新Exact先冻结、仅陈述独立重构后全文读proof；root亲核实际记录。v3退化d1措辞已附可行前提；NP旧高重模板不能自动导入；G平星可直接解故非hardness。
- Status：proof complete；actual two-stage internal review；external review/novelty unverified；implementation none。
- Related Files：[正文](../current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md)、[审查](../reviews/unrelated_machines/ternary_rainbow_subtree_exact_hardness_review.md)、assets/crosswalk冻结原字节。

## UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2：共同b双小边的实际三半锐界

- ID/version：UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2；旧row-spread身份不改。
- Exact Statement / Quantifiers：∀完整binary rational UM及显式b>0，finite p≤b且∀row正small数≤2，确定性位poly全σ C≤3OPT/2；∀T<b精确判定并解OPT<b；∀T=b+a<2b，OPT≤T必成功C≤3b/2+a、FAIL⇒OPT>T；∀固定ρ<3/2，同类ρ近似除非P=NP不存在。
- Objects / Domain / Definitions：unit恰b、small为0<p<b、zero无限；任意共享/多端，含n0/OPT0/单机/松b。
- Assumptions / Dependencies：UM-MODEL-v1、UM-ST-ROUND-v1、标准LP/流、Karp3DM及PSM2018已有机器方案。
- Scope / Conclusion：受限类sharp3/2实际算法及条件复杂性下界，非三small或任意不同big时间扩域。
- Evidence：双陈述先行重构/双读后攻击/root核全证明；有限精确flow审计16128local/300矩阵/7997阈值/256源子集。
- Counterevidence/Objections：无standing fatal；原文总资格≤3非本字面域，common-b适配自证；有限测试不代一般证明。
- Status：限定证明完成/已内审，synthesis；外审未记录，新颖性/论文价值未认证；audit_only。
- Related Files：research/current/unrelated_machines/joint_slot_prefix_rounding.md、research/reviews/unrelated_machines/joint_slot_prefix_review.md、tests/audits/unrelated_machines/two_small_incidence_flow_audit.py、evidence/runs/unrelated_machines/two_small_incidence_flow_audit.json及manifest/六冻结源。

## UM-SINGLE-PINNED-TREE-MULTIPLICITY-EXACT-CONFIGURATION-GAP-v1

- Exact Statement / Objects / Domain / Quantifiers：单强制根完整uniform树、整树每色≤µ的普通配置gap sup精确2−1/µ；det bitpoly全部σ≤2−ceil(d/µ)/d，显式底层重色+逐层衰减证书匹配；不改多state固定µ G。 完整量词/矩阵/域在research/current/unrelated_machines/private_injective_tree_configuration_floor.md。
- Assumptions / Definitions / Scope / Conclusion：无复杂度假设；只显式结构类/明确操作，全部原jobs与所有机器；不解决主目标正反面。
- Dependencies：UM-MODEL-v1、raw-q子可加/DP或旧三叉v1/v2实际构件；正文自足负载/完整LP，无finite前提。
- Evidence / Counterevidence / Status：实际Exact-first重构后读冻结proof；root亲核。域异议和讨论勘误已在canonical明修，原源保留；无standing fatal；限定证明完成/无新软件、外审或新颖性认证。
- Related Files：research/current/unrelated_machines/private_injective_tree_configuration_floor.md、research/reviews/unrelated_machines/private_injective_tree_configuration_floor_review.md及source_crosswalk新冻结材料。

## UM-TERNARY-PALETTE-TENSOR-AMPLIFICATION-OBSTRUCTION-v2

- Exact Statement / Objects / Domain / Quantifiers：末层两色的对齐Cartesian张量YES精确OPT2−(2/3)^k，gap上包络Gk≤5/4且严格下降趋1；纯k收缩连strong(d−1)也不可，非所有放大不可能。 完整量词/矩阵/域在research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md。
- Assumptions / Definitions / Scope / Conclusion：无复杂度假设；只显式结构类/明确操作，全部原jobs与所有机器；不解决主目标正反面。
- Dependencies：UM-MODEL-v1、raw-q子可加/DP或旧三叉v1/v2实际构件；正文自足负载/完整LP，无finite前提。
- Evidence / Counterevidence / Status：实际Exact-first重构后读冻结proof；root亲核。域异议和讨论勘误已在canonical明修，原源保留；无standing fatal；限定证明完成/无新软件、外审或新颖性认证。
- Related Files：research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md、research/reviews/unrelated_machines/ternary_rainbow_subtree_exact_hardness_review.md及source_crosswalk新冻结材料。


## UM-PREFIX-ATOMIC-DECODING-v1：前缀原子证书的确定性解码桥

- **Exact Statement / Quantifiers：** 对任意合法有理 `P,T`，若显式前缀oracle `π(S)` 对所有相容部分分配满足 `π(∅)=1`、非负性、未赋值任务的 one-hot 守恒，并对每个完整 `σ` 满足 `(T-load_i(σ))π(σ)≥0`，则逐任务正延伸贪心在至多 `O(|E|)` 次位多项式精确查询中输出 `load_i(σ)≤T` 的完整调度。该证书存在当且仅当 `OPT≤T`。
- **Scope / Value：** 全阶矩 `L(m_S)` 是一种指数表示；本Claim新增的是可查询压缩表示和确定性解码，不是一般算法。
- **Evidence / Objections：** Fraction核验覆盖Dirac/均匀可行证书、`T=0`、两机三件单位任务的全原子排除及异质Dirac例。一般 `P,T` 如何生成oracle或可靠 `FAIL` 未闭合；已有半单位选择NP障碍限制把它当免费oracle。
- **Status：** complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；`UM-TARGET-v1`仍OPEN。
- **Related Files：** `research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md`、`research/reviews/unrelated_machines/succinct_prefix_atomic_decoding_review.md`、`tests/audits/unrelated_machines/succinct_prefix_atomic_decoding.py`、`evidence/runs/unrelated_machines/succinct_prefix_atomic_decoding_audit.json`。

## UM-PREFIX-ATOMIC-FINITE-PRECISION-v1：前缀原子解码的锐有限精度与有理格点恢复

- ID / Version：`UM-PREFIX-ATOMIC-FINITE-PRECISION-v1`；新有限精度合同，不改精确查询 `UM-PREFIX-ATOMIC-DECODING-v1`。
- Exact Statement / Quantifiers：对每个合法P、T≥0、固定任务顺序及同一个非负归一化精确守恒前缀law π，令d_j为各任务有限端数，N=∏d_j。若每次前缀查询绝对误差≤a，则逐任务选最大近似值的det解码输出真实叶质量≥max(0,[1−2a(N−1)]/N)，该全参数最坏界锐。若全部完整叶逐机满足(T−L_i)π≥−τ_i且2a(N−1)<1，则输出逐机L_i≤T+Nτ_i/[1−2a(N−1)]。令Q为全部有限p及T的约分分母之积，a=1/(4N)、τ_i≤1/(4QN)时输出精确T可行调度。
- Objects / Domain：UM-MODEL-v1全部非负有理/∞输入、m≥1、n≥0；N数全部合法分配而非支撑数，Q为共同有理网格；只查询固定顺序的前缀。
- Assumptions / Definitions：π守恒和根归一化精确；localizer是真实全叶全机不等式的承诺。查询时间和输出位长按原输入及精度编码位数多项式，非按1/a多项式。近似查询值本身可以为负。
- Scope / Conclusion：至多|E|次查询的det-bit-poly条件解码；logN和logQ均受输入位长控制，指数小数值不构成指数位数障碍。绝对残差存在零选择任务稀释的锐N损失；相对残差−Δ_iπ直接给T+Δ_i且不随N损失。满行秩完整函数评价F时K_i≽−Δ_iM恰等价全部支撑原子容量界，低阶/缺秩F不可外推。
- Dependencies：UM-MODEL-v1；同一前缀law的守恒、全叶真实localizer、查询位复杂度合同；自足兄弟比较与望远镜、共同分母整数格点及满行秩线性代数。原精确桥和全阶矩只作相关表示，不是自动提供新承诺的生成器。
- Evidence：先只收精确陈述的独立重构，再实际读a17bde448cd58ab9b637a6050837153006423cf8097b078621bcb302031ff02b完整正文新增§1–6及原定义依赖；root复核证明并实际重跑三套Fraction审计。有限范围和SHA见冻结记录。
- Counterevidence / Objections：无尚成立的声明范围fatal。root/守恒误差未纳入；没有一般证书生成、全称承诺验证、低阶Gram提取或可靠FAIL程序。相对阈值(2−ε)T的promise-gap生成不能由精确阈值困难性直接否定。
- Status：complete scoped proof; independently reconstructed and exactly audited; external review and novelty unverified；软件为audit_only；UM-TARGET-v1仍OPEN。
- Related Files：`research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md`；`research/reviews/unrelated_machines/prefix_atomic_finite_precision_review.md`；`tests/audits/unrelated_machines/prefix_atomic_finite_precision.py`及两份独立审计；`evidence/runs/unrelated_machines/prefix_atomic_finite_precision_audit.json`及两份独立冻结记录。

## 近单位锚任务的缺额阈值与共同实际舍入

### UM-ANCHOR-DEFICIENCY-JOINT-ROUNDING-v1

- 中文数学名称：锚点分量缺额的全局联合舍入。
- Exact Statement / Quantifiers：对每个显式合法P、T>0、固定划分J=B⊔S、α∈[0,1/2)、β≥0、整数d0≥0，若anchor所有有限时间∈[(1−α)T,T]、tiny所有有限时间≤βT，且anchor资格图每个含anchor分量0≤m_c−k_c≤d0，则存在一个统一确定性位多项式阈值算法，输出全任务实际σ或FAIL，成功时Cmax≤[2−(1−α)/(d0+1)+β]T，FAIL⇒OPT>T。
- Objects / Domain：原UM非负有理/∞模型；机器/任务/分量数不固定，tiny可以跨全部分量、任意资格与异端时间；d0可随输入给出但改善可能退化。
- Assumptions / Definitions：固定任务身份；联合LP q满anchor分数匹配、q_i≤1、ℓ_i+(1−α)Tq_i≤T；结构前提失败只记OUT-OF-CLASS。
- Scope / Conclusion：同一LP后共同选anchor机器、一次全局tiny ST；β<(1−α)/(d0+1)时该结构类严格次二。抽象余秩d基点阈值1/(d+1)可同时删除其下全部坐标，且U_(1,d+1)均匀基点证明该阈值锐；不声称调度比例最优。
- Dependencies：UM-MODEL-v1、标准有理LP、Hall、UM-ST-ROUND-v1；完整证明见正文§1–9/11。
- Evidence：两条独立符号推导、实际全文攻击、root三个Fraction见证舍入及边界核对。
- Counterevidence / Objections：无standing fatal；一般混合身份与无界阻塞集未解决；不能把LP失败移用于域外。
- Status：限定类完整数学算法/位复杂度；软件仅给定LP见证舍入审计；外审/新颖性未认证。
- Related Files：current/unrelated_machines/anchor_deficiency_joint_rounding.md、reviews/unrelated_machines/anchor_deficiency_joint_rounding_review.md、tests/audits/unrelated_machines/anchor_deficiency_joint_rounding_audit.py、evidence/runs/unrelated_machines/anchor_deficiency_witness_audit.json（路径均从仓库根沿登记可达）。

### UM-ANCHOR-DEFICIENCY-PROMISE-APPROX-v1

- 中文数学名称：弱最优尺度承诺下的无损阈值搜索。
- Exact Statement / Quantifiers：对每个合法P与给定固定B/S、α∈[0,1/2)、β≥0、d0≥0，完整anchor资格图各含anchor分量亏缺≤d0；若OPT>0时存在一份最优σ*，anchor所用边≥(1−α)OPT且tiny所用边≤βOPT，则一个确定性总位多项式算法实际输出Cmax≤[2−(1−α)/(d0+1)+β]OPT。OPT0/空任务精确处理。
- Objects / Domain / Assumptions：固定身份但其他有限边可有任意尺度；仅要求一份最优见证具有所述性质，不要求输入能识别promise。
- Definitions / Scope：候选T只保anchor p≤T、tiny p≤βT；联合LP取c=1−α，不加anchor下截；完整图亏缺在保全顶点的可行删边分支中保持上界。
- Conclusion：接受性单调、原processing分母积Q的整数网格精确二分，最小接受T≤OPT，无η损失。固定αβd0且β<(1−α)/(d0+1)时整个承诺类统一次二；参数变化不保证统一epsilon。
- Dependencies：正文阈值舍入成功分支（其不需要anchor下界）、标准有理LP/整数二分、UM-ST-ROUND-v1；不把阈值定理的全边前提偷换成弱promise。
- Evidence：独立重构单调性、全部顶点亏缺求和、Q/QU位长及实际最终稿攻击；通用LP/端到端后端未实现。
- Counterevidence / Objections：没有一般输入的身份提取/亏缺控制；standing fatal无。
- Status：限定承诺类数学算法完整；外审/新颖性未认证。
- Related Files：与前一身份同正文/审查；正文§10。

## 任意固定阶强配置矩的共同匹配边界

### UM-FIXED-DEGREE-STRONG-CONFIG-MATCHING-LAW-OBSTRUCTION-v1

- 中文数学名称：强配置伪矩的共同匹配不可实现及锐修复距离。
- Exact Statement / Quantifiers：对每整数r≥2、每奇整数N≥4r−1，存在2N机2N任务、全有限时间1的N个K2,2块实例和显式有理degree2r证书：M_r PSD、one-hot到2r−1、逐机degree r−1负载localizer PSD（实际为0）、与每行完整CONFIG1的全部本行≤2r阶矩相容、全部≤2r原端literal事件非负；但无真实完整匹配分布保其一阶与二阶。实际OPT=T=1。
- Objects / Domain：SH(r)如自足正文定义；矩来自formal half-slice L(b_A)=(N/2)_|A|/(N)_|A|，不是声称真实分布。
- Assumptions / Definitions：每块两完美匹配由一个bit表示；代入bit后相容的短圆柱严格正，其余零。
- Scope / Conclusion：精确保给定二阶的law接口被否定；保持一阶的真实law对跨块pair的最小L∞改动精确1/[4N(N−1)]，floor/ceil均匀slice各半混合取等；不要求高阶同时修复。
- Dependencies：UM-MODEL-v1、Boolean商代数、自足up/down harmonic Gram证明及整数方差下界；经典knapsack伪矩机制不认领新颖性。
- Evidence：陈述先行独立重构、最终全文攻击、root三个小矩阵精确Schur/Gram/cylinder/variance/repair核验。
- Counterevidence / Objections：真实完美匹配很容易，改动二阶即可最优；修复半径趋零，不是常数鲁棒间隙。无standing fatal。
- Status：限定接口定理与锐二阶距离证明完整；固定r生成N^{O(r)}，不称r变参时联合多项式；外审/全球新颖性未认证。
- Related Files：current/unrelated_machines/strong_configuration_matching_moment_obstruction.md、reviews/unrelated_machines/strong_configuration_matching_moment_review.md、tests/audits/unrelated_machines/strong_configuration_matching_moment_audit.py、evidence/runs/unrelated_machines/strong_configuration_matching_moment_audit.json。

## UM-PERMANENT-BUFFER-ACTIVATION-v1：永久缓冲激活与统一分数选择的锐窗口

- Exact Statement / Quantifiers：对任意合法P、T≥0、T≤C≤2T、剪枝实际σ≤C和给定实际τ≤T，令S=f+A、Q为改变任务目标量、U=max(2T,C+T/2)、h=(S+Q−U)+。任意已迁子集R满足L=S+Q−D−B；D_i≥h_i当且仅当i在所有后续排列的全部前缀（含零步）局部负载≤U；h≤T/2且3h≤A。统一x_j=λ对全部此类输入满足源cover及原预算target packing的λ∈[0,1]恰[1/3,1/2]。
- Objects / Domain / Definitions：UM-MODEL-v1，二进制非负有理与不可用端；第1节定义S,f,A,Q,D,B,U,h及具体实际σ、τ；后续路径只直接迁往τ，每件至多一次，minimax下界另允许所有单件绕路。
- Assumptions / Scope：使用具体τ及改变任务；局部安全不以全局守容排列预筛。锐性T>0；T=0直接处理。
- Conclusion：以上准确范围的公式、反例或实际路径证书；UM-TARGET-v1及无条件全程路径保持OPEN。
- Dependencies：UM-MODEL-v1；正文自足非负负载、共同目标容量、端点/函数图计数及有理运算，不导入外部定理。
- Evidence：先陈述独立重构、实际冻结全文攻击及主研究者亲核；规范与不导入规范的独立有理核验仅作checks。
- Counterevidence / Objections：局部排列量词、零步、不可达集合闭合性、策略死锁与全局死锁及整数入口均已修正；无standing内部fatal。新颖性和外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实现轴为audit_only。
- Related Files：research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md；research/reviews/unrelated_machines/permanent_buffer_activation_review.md；evidence/runs/unrelated_machines/permanent_buffer_activation_audit.json；实际代码和输入/证书从上述文件进入。

## UM-STATIC-ACTIVATION-COVER-OBSTRUCTION-v1：原始接收预算的一次性整数激活障碍

- Exact Statement / Quantifiers：存在T=1,C=2、四机七任务且OPT=1的剪枝实际σ及具体τ≤1：统一分数窗口可行，但无子集同时移出每机至少h_i并使每目的接收量≤U−S_i。显式逐件目标路径峰23/10<5/2。
- Objects / Domain / Definitions：UM-MODEL-v1，二进制非负有理与不可用端；第1节定义S,f,A,Q,D,B,U,h及具体实际σ、τ；后续路径只直接迁往τ，每件至多一次，minimax下界另允许所有单件绕路。
- Assumptions / Scope：仅否定原始接收预算不变的一次性cover/packing；不是全程路径反例或一般困难性。
- Conclusion：以上准确范围的公式、反例或实际路径证书；UM-TARGET-v1及无条件全程路径保持OPEN。
- Dependencies：UM-MODEL-v1, UM-PERMANENT-BUFFER-ACTIVATION-v1；正文自足非负负载、共同目标容量、端点/函数图计数及有理运算，不导入外部定理。
- Evidence：先陈述独立重构、实际冻结全文攻击及主研究者亲核；规范与不导入规范的独立有理核验仅作checks。
- Counterevidence / Objections：局部排列量词、零步、不可达集合闭合性、策略死锁与全局死锁及整数入口均已修正；无standing内部fatal。新颖性和外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实现轴为audit_only。
- Related Files：research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md；research/reviews/unrelated_machines/permanent_buffer_activation_review.md；evidence/runs/unrelated_machines/permanent_buffer_activation_audit.json；实际代码和输入/证书从上述文件进入。

## UM-TRANSIENT-PRIORITY-DEADLOCK-v1：最大源端与源目标比率的无平局依赖死锁

- Exact Statement / Quantifiers：对每有理T>0、3/2<c<2、0<d<1/3、1/2<q≤1，四机八任务两端族OPT=T且初态全cT；在U=(c+1/2)T下从安全直接τ迁移选最大a或a/b，不论平局均停在未完成真死锁。仅未激活源规则亦失败但须区分允许动作耗尽。到指定τ的全部单件路径minimax恰(c+(1−d)/2)T<U，允许回退重复也不降低。
- Objects / Domain / Definitions：UM-MODEL-v1，二进制非负有理与不可用端；第1节定义S,f,A,Q,D,B,U,h及具体实际σ、τ；后续路径只直接迁往τ，每件至多一次，minimax下界另允许所有单件绕路。
- Assumptions / Scope：全部族端时间≤T且b>0；a/b实现仅该正端族。τ给定，初态不声明ST来源。只否定两种具体选序。
- Conclusion：以上准确范围的公式、反例或实际路径证书；UM-TARGET-v1及无条件全程路径保持OPEN。
- Dependencies：UM-MODEL-v1, UM-PERMANENT-BUFFER-ACTIVATION-v1；正文自足非负负载、共同目标容量、端点/函数图计数及有理运算，不导入外部定理。
- Evidence：先陈述独立重构、实际冻结全文攻击及主研究者亲核；规范与不导入规范的独立有理核验仅作checks。
- Counterevidence / Objections：局部排列量词、零步、不可达集合闭合性、策略死锁与全局死锁及整数入口均已修正；无standing内部fatal。新颖性和外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实现轴为audit_only。
- Related Files：research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md；research/reviews/unrelated_machines/permanent_buffer_activation_review.md；evidence/runs/unrelated_machines/permanent_buffer_activation_audit.json；实际代码和输入/证书从上述文件进入。

## UM-PERMANENT-BUFFER-UNLOCK-PATH-v1：单件解锁函数图的可检验全程路径

- Exact Statement / Quantifiers：在激活身份的全部输入下，H={h>0}、eligible为源在H且a≥h_source、G={有eligible到非H或b≤U−S_target}。每H点经H内eligible边可达G，等价每H源选一条eligible且每所选有向环含初态安全边。该条件下确定性位poly输出每件至多直迁一次的完整τ路径且峰≤U；每H源有至少两件不同eligible时条件自动成立。
- Objects / Domain / Definitions：UM-MODEL-v1，二进制非负有理与不可用端；第1节定义S,f,A,Q,D,B,U,h及具体实际σ、τ；后续路径只直接迁往τ，每件至多一次，minimax下界另允许所有单件绕路。
- Assumptions / Scope：具体τ给定；条件失败只表示该证书失败，不表示OPT>T或无路径。所有负载逐台保证，n步位poly仅指selector，不指审计枚举。
- Conclusion：以上准确范围的公式、反例或实际路径证书；UM-TARGET-v1及无条件全程路径保持OPEN。
- Dependencies：UM-MODEL-v1, UM-PERMANENT-BUFFER-ACTIVATION-v1；正文自足非负负载、共同目标容量、端点/函数图计数及有理运算，不导入外部定理。
- Evidence：先陈述独立重构、实际冻结全文攻击及主研究者亲核；规范与不导入规范的独立有理核验仅作checks。
- Counterevidence / Objections：局部排列量词、零步、不可达集合闭合性、策略死锁与全局死锁及整数入口均已修正；无standing内部fatal。新颖性和外审未认证。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；实现轴为implemented。
- Related Files：research/current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md；research/reviews/unrelated_machines/permanent_buffer_activation_review.md；evidence/runs/unrelated_machines/permanent_buffer_activation_audit.json；实际代码和输入/证书从上述文件进入。

## UM-SMALL-DENSITY-FLOW-BARRIER-v1：多小端柔性密度的整数流障碍

- **Exact Statement / Quantifiers：** 固定整数 `k≥2`，每条有限时间属于 `{1,1/k}`。令 `Q` 为无 `1/k` 端任务，`R` 为其余任务；`S_j` 为任务 `j∈R` 的 small 端集，`d_j=|S_j|`。若每机 small incidence 数 `t_i≤k`，且至少 `γ` 比例的 incidence 来自 `d_j≥2` 的任务（逐机 `b_i≥γt_i`），则均匀 small 分流的行质量 `ρ_i=Σ_{i∈S_j}1/d_j` 满足 `ρ_i≤(1−γ/2)k`。容量 `ceilρ_i` 的整数流给每个 `R` 任务一个 small 端。若 `Q` 有容量1匹配，则有实际调度 `C_max≤2−floor(γk/2)/k`；若 `Q=∅` 则删去前导1；若 `Q` 无容量1匹配，则 `OPT≥2`。若柔性端均满足 `d_j≥D`，把 `γ/2` 换成 `γ(1−1/D)`。
- **Objects / Domain / Assumptions：** 显式合法 UM，时间只取 `{1,1/k}`；`Q` 的所有有限端均为 unit 端；`d_j=1` 只约束 small 端，不排除同一任务另有 unit 端。柔性密度必须逐机成立，不能只用全局平均。
- **Conclusion / Scope：** 这是一个确定性位多项式的结构类算法和近二归约必要形状；它直接击穿每机多端小任务占固定比例的 `{1,1/k}` 物理编译。它不是一般 `UM-TARGET-v1` 算法，也不是一般不可近似性证明；`Q=∅` 分支给绝对负载界，不自动给相对 `OPT` 比率。
- **Dependencies：** 二部容量流积分性、容量1二分匹配、`ρ_i` 的逐机计数不等式、`ceil` 的整数恒等式。
- **Evidence / Counterevidence：** 一般证明已独立重构并经红队核对；无大规模枚举。仍未覆盖多尺度时间、跨机器 unit/medium 联合编码或 `γ→0` 的近二候选。
- **Status：** 限定结构类证明完成，内部攻击无尚成立的致命异议；外审/新颖性未认证；`UM-TARGET-v1` 仍 OPEN。
- **Related Files：** [多小端柔性密度正文](../current/unrelated_machines/mixed_small_endpoint_density_flow_barrier.md)、[近单位物理编译总页](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)。

## UM-FIXED-SA-ASSIGNMENT-GAP-v1：固定轮 assignment Sherali--Adams 趋二间隙

- **Exact Statement / Quantifiers：** 固定 `r≥1`，对每个 `m≥r` 取 `m` 台相同机器、`n=m+1` 个 unit 任务，令 `T_{m,r}=1+1/(m−r+1)`。按“至多 `r−1` 个 literal 乘子”的标准 SA 轮次约定，`SA_r(T_{m,r})` 可行；而真实 `OPT=2`，故 `OPT/T=2−2/(m−r+2)`，固定 `r` 时随 `m` 趋近2。
- **Objects / Domain / Definitions：** assignment/LST feasibility LP 的完整 literal SA 乘式（含 `1−x` 事件），伪点由至多 `r` 个任务的均匀局部注入分布定义；局部注入只是伪分布，不把原调度误改成每机至多一任务。
- **Conclusion / Scope：** 任何固定轮 SA assignment/load 证书的统一 `(2−ε)T` 舍入合同均失败。命题不限制 configuration-LP、随规模增长的层数、Lasserre/SOS 或直接利用原矩阵的算法；本族本身易解，故不是 `P≠NP` 困难性。
- **Dependencies：** 局部注入的扩展计数、assignment 等式、条件容量期望 `1+1/(m−q)`、鸽巢原理。
- **Evidence / Counterevidence：** 伪分布与 signed-literal 容量乘式已独立重构并红队核对；固定 `r` 的事件/证书位长为多项式级，未用枚举。标准 SA 的轮次编号可整体平移1，不能把此结果扩大到配置或所有算法。
- **Status：** 固定层松弛障碍证明完成，内部攻击无尚成立的致命异议；外审/新颖性未认证；`UM-TARGET-v1` 仍 OPEN。
- **Related Files：** [固定轮 SA 正文](../current/unrelated_machines/fixed_sa_assignment_gap.md)、[经典 LST/配置地基](../current/unrelated_machines/model_and_classical_barriers.md)。

## UM-WEIGHTED-SMALL-ST-BARRIER-v1：加权小端柔性密度与 ST 的次二障碍

- **Exact Statement / Quantifiers：** 固定 `β<1,γ≤1`，unit-only 任务所有有限边时间为1；其余任务至少有一条 `p≤β` 的 small 端。若逐机 small 总工作 `s_i≤1`，且多端任务 `d_j≥2` 的 small 工作 `u_i≥γs_i`，则等分支撑加 ST 给 `C≤2−γ/2+β`；unit-only 匹配失败则 `OPT≥2`。
- **Objects / Domain / Scope：** 任意有理 mixed small 时间和任意支持图；逐机条件不可替换成全局平均。`Q=∅` 只有绝对界，`Q≠∅` 且匹配成功时才有 `OPT≥1` 的相对解释。
- **Conclusion：** 若 `2−γ/2+β<ρ<2`，YES≤1/NO>ρ 的此类物理归约被 matching+ST 位多项式 decoder 直接击穿；不构成一般算法或 hardness。
- **Dependencies：** UM-ST-ROUND-v1、均匀 small 支撑的逐机工作不等式、容量1匹配。
- **Status：** 限定多尺度结构证明完成，独立攻击无尚成立的致命异议；外审/新颖性未认证；`UM-TARGET-v1` 仍 OPEN。
- **Related Files：** [加权正文](../current/unrelated_machines/weighted_small_st_barrier.md)、[独立攻击](../reviews/unrelated_machines/weighted_small_st_barrier_review.md)。

## UM-PERMANENT-BUFFER-HELD-CYCLE-PATH-v1：保留坏环与源补集的共同全程路径

- Exact Statement / Quantifiers：对任意UM-MODEL-v1的T≥0,T≤C≤2T、剪枝实际σ≤C和给定实际τ≤T，定义S=f+A,Q,U=max(2T,C+T/2),h=(S+Q−U)+。若每个h_i>0的源至少有一件改变任务a_j≥h_i，则确定性位poly输出每件至多一次直迁τ的完整路径，全程≤U。任意选一件eligible形成的坏环可保留，其他来流统一受S+Q−β<U控制，源补集A−a≥h后释放。
- Objects / Domain / Definitions：二进制非负有理/不可用边、实际完整σ与τ；不动任务f，改变源A/目标Q，正阈值H，所选坏环Z和暂留入边β按正文定义。
- Assumptions / Scope：具体τ给定；源端a≤T承重。没有eligible只是否定该充分条件，不是OPT>T或无路径。
- Conclusion：给定目标的全程实际路径与明确范围锐界；非一般近似/困难性。
- Dependencies：UM-MODEL-v1, UM-PERMANENT-BUFFER-ACTIVATION-v1；全部共同输入前提仍须满足。
- Evidence：先陈述独立重构、构造者复核、冻结全文/实现攻击、主研究者亲核；两独立有理实现仅作有限checks。
- Counterevidence / Objections：删除剪枝的两机反例明确保留；padding only-original条件已补；条件保护不冒充永久安全；无standing内部fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；规范给定目标构造implemented，外审与新颖性未认证，UM-TARGET-v1仍OPEN。
- Related Files：research/current/unrelated_machines/held_cycle_release_and_assigned_max_path.md；research/reviews/unrelated_machines/held_cycle_assigned_max_path_review.md；evidence/runs/unrelated_machines/held_cycle_assigned_max_path_audit.json；两审计实现沿上述文件进入。

## UM-MULTI-ACTIVATION-STATIC-COVER-v1：多件共同激活的静态 cover/packing 桥

- **Exact Statement / Quantifiers：** 给定任意合法 UM、`T≤C≤2T`、初态完整分配 `sigma` 且 `Cmax(sigma)≤C`、目标完整分配 `tau` 且 `Cmax(tau)≤T`。按正文定义不动负载 `f_i`、源量 `A_i`、目标量 `Q_i`、`S_i=f_i+A_i`、`U=max(2T,C+T/2)`、`h_i=(S_i+Q_i-U)_+`。若存在改变任务子集 `R` 同时满足 `D_i(R)≥h_i` 和 `P_k(R)≤U−S_k`，则先迁 `R` 后迁其余任务的确定性位多项式路径全程 `Cmax≤U`，最后到达 `tau`。
- **Objects / Domain / Scope：** 二进制非负有理/不可用边；所有机器和任务同时计入；`R` 是额外证书而非输入自动可得的 oracle。等源端/等目标端时间时，证书存在性可化为带上下界整数 circulation。
- **Conclusion / Boundary：** 这是给定 `sigma,tau` 的充分桥，不是必要条件；三机六任务例有路径峰 `23/10` 但无静态 `R`。失败不推出 `OPT>T`，未知目标和任意输入证书生成仍 OPEN。
- **Dependencies：** UM-MODEL-v1、负载恒等式、带下界整数流。
- **Evidence / Status：** 自足证明；Fraction 审计通过；独立审查无尚成立 fatal；外审/新颖性未认证，`UM-TARGET-v1` 仍 OPEN。
- **Related Files：** [正文](../current/unrelated_machines/multi_activation_cover_and_replication_barriers.md)、[审查](../reviews/unrelated_machines/multi_activation_cover_replication_review.md)、[审计](../../tests/audits/unrelated_machines/multi_activation_cover_replication.py)。

## UM-MULTI-ACTIVATION-HOLD-EDGE-RESTATEMENT-v1：保留目标边的静态证书重排

- **Exact Statement / Quantifiers：** 在同一给定 `sigma,tau` 输入中，若 `B⊆R` 满足正文的源 cover、无保留目标的原预算以及保留目标 `beta_k>h_k` 条件，则按 `R\\B`、其余任务、`B` 的顺序全程不超过 `U`。
- **Scope / Objection：** 令 `A=R\\B` 后，条件推出 `A` 本身满足静态 cover；因此该身份只是延迟执行的等价重写，不扩大可行证书集合，也不绕过静态 cover 失败。等号 `beta=h>0` 可放宽到非严格峰值，但正文采用严格版本。
- **Status / Related Files：** 限定证明及独立审查通过；不构成一般算法；正文、审查和审计同前一命题。

## UM-DISJOINT-BLOCK-NO-AMPLIFICATION-v1：不交机器块的近似 gap 不放大

- **Exact Statement / Quantifiers：** 对任意有限族不交机器/任务实例 `I_t` 及正缩放 `alpha_t`，不交并的最优值满足 `OPT(⊔_t alpha_t I_t)=max_t alpha_t OPT(I_t)`；分别求解各块时整体近似比不超过组件比值最大值。
- **Scope / Conclusion：** 只否定不交复制/块并的 gap 放大；不外推到共享机器、跨副本任务身份或 Kronecker gadget。
- **Status / Related Files：** 自足两边不等式；见 [多件激活与复制正文](../current/unrelated_machines/multi_activation_cover_and_replication_barriers.md) 与其审查；`UM-TARGET-v1` 仍 OPEN。

## UM-SHARED-CLONE-REPLICATION-COLLAPSE-v1：共享同机复制渐近回到 assignment-LP

- **Exact Statement / Quantifiers：** 对任意合法实例 `I`，令 `F` 为未删边 assignment-LP 的最优 makespan；令 `I^(k)` 把每个任务复制 `k` 次到同一机器集，`O_k=OPT(I^(k))`。则对每个整数 `k≥1`，`kF≤O_k≤kF+S`，其中 `S=max_i Σ_{j:p_ij<∞}p_ij`，故 `O_k/k→F`。
- **Proof Mechanism / Scope：** 下界由复制计数除以 `k`；上界由 LP 最优解逐任务 floor/ceil 取整，每个有限端至多增加一份。`k` 的显式展开有 `nk` 个任务，不能把二进制超大复制直接当作位多项式归约；不讨论阈值删边 configuration-LP，也不外推任意跨副本 gadget。
- **Status / Related Files：** 自足证明、Fraction 审计和独立审查通过；这是复制接口边界而非一般 hardness；见同一正文/审查/审计，`UM-TARGET-v1` 仍 OPEN。

## UM-ASSIGNED-MAX-TRANSIENT-PATH-SHARP-v1：实际最大件初态的全程容量锐界与槽输出推论

- Exact Statement / Quantifiers：在前项同一剪枝/具体τ输入上，若逐机S_i≤T+M_i，其中M_i为σ实际分配最大件（空0），则确定性位poly输出每件至多一次直迁τ的完整路径且峰≤U。对每有理T>0,C∈[T,2T]，这个局部promise类到指定不同τ的单件路径最坏minimax恰U。标准非增单位槽匹配从同一剪枝分数负载≤T产生的任何实际输出满足S−M≤T，故上界覆盖实际槽输出。
- Objects / Domain / Definitions：二进制非负有理/不可用边、实际完整σ与τ；不动任务f，改变源A/目标Q，正阈值H，所选坏环Z和暂留入边β按正文定义。
- Assumptions / Scope：锐性针对完整局部promise类，允许m=2，不声称每固定m,n或实际ST输出锐性；C=T仍为另一指定目标的非空路径。不给未知目标。
- Conclusion：给定目标的全程实际路径与明确范围锐界；非一般近似/困难性。
- Dependencies：UM-MODEL-v1, UM-PERMANENT-BUFFER-ACTIVATION-v1, UM-PERMANENT-BUFFER-HELD-CYCLE-PATH-v1, UM-ST-ROUND-v1, UM-BOUNDED-BATCH-TRANSIENT-PEAK-SHARP-v1；全部共同输入前提仍须满足。
- Evidence：先陈述独立重构、构造者复核、冻结全文/实现攻击、主研究者亲核；两独立有理实现仅作有限checks。
- Counterevidence / Objections：删除剪枝的两机反例明确保留；padding only-original条件已补；条件保护不冒充永久安全；无standing内部fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified；规范给定目标构造implemented，外审与新颖性未认证，UM-TARGET-v1仍OPEN。
- Related Files：research/current/unrelated_machines/held_cycle_release_and_assigned_max_path.md；research/reviews/unrelated_machines/held_cycle_assigned_max_path_review.md；evidence/runs/unrelated_machines/held_cycle_assigned_max_path_audit.json；两审计实现沿上述文件进入。

## 未知目标与冻结核心接口

| ID | 精确陈述 | 证据与范围 |
| --- | --- | --- |
| UM-COMMON-SIZE-UNKNOWN-B-EXACT-v1 | 冻结核心后公共尺寸 q 的重开任务可在候选阈值上用整数最大流精确搜索未知 B，并输出实际最优分配；机器侧不交的单尺寸分量可独立合并。 | [正文](../current/unrelated_machines/unknown_target_common_size_exact_repair.md)、[审计](../../tests/audits/unrelated_machines/unknown_target_common_size_exact_repair.py)；异尺寸共享机器为装箱/Partition边界，非一般算法。 |
| UM-COMMON-MULTIPLIER-UNKNOWN-B-EXACT-v1 | 冻结核心负载后，若每个资格连通分量的有限端都形如机器固定倍率 a_i 乘该分量公共尺寸 q_C，则未知最优峰值可由有限候选与整数最大流精确求出并输出实际重开；混合尺寸共享机器不在范围。 | [正文](unrelated_machines/unknown_target_common_multiplier_exact_repair.md)、[独立审查](../reviews/unrelated_machines/unknown_target_common_multiplier_review.md)、[Fraction审计](../../tests/audits/unrelated_machines/unknown_target_common_multiplier_exact_repair.py)；仅受限未知目标接口，非一般UM算法。 |
| UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1 | 去除给定目标 τ 后，承诺存在 T-可行目标的多项式目标生成已包含两机 Partition；p_1j=p_2j=w_j、Σw_j=2B、T=B 时存在目标 iff Partition。 | [正文](../current/unrelated_machines/unknown_target_partition_search_obstruction.md)、[审查](../reviews/unrelated_machines/held_cycle_unknown_target_obstruction.md)；只限制“免费删去 τ”，不推出一般UM不可近似性。 |
## UM-TWO-WITNESS-QUERY-SEPARATION-v2：一般双见证查询分离的锐3/2费用合同

- ID / Version：`UM-TWO-WITNESS-QUERY-SEPARATION-v2`；新域/锐结论按v2冻结，不改旧Claim。
- Exact Statement：det bitpoly两两不交Aq⊆D\Q，单q实际τq≤max(3T/2,T+δq)，Σfee≤W；tiny聚合Q时3T/2，且任意tinyη下3/2合同阈值sharp。不是OPT gap或UM算法。
- Objects / Domain / Quantifiers：任意一般P，同一P实际σ0/σ1均≤有理T≥0；非空Q⊆owner改变集D；δq为其它Q在σ0每机最大总负荷；任意非负非query改派权。 对每个完整输入成立；全部共同前提见[正文](../current/unrelated_machines/two_witness_query_separation.md)。
- Assumptions / Definitions / Scope：无复杂度假设；原对象显式，实际给定见证或准确slice结构不可略；不是一般UM正反面结论。
- Conclusion：上述构造/锐界按精确定义全量词成立，不以有限测试证明。
- Dependencies：正文列出的全部共同域及自足证明步骤，图derives同时列入；DGR源只作准确Paper Fact。
- Evidence：完整证明、实际陈述先行/读后审查及root核对；实现=audit_only。
- Counterevidence / Objections：无standing fatal；费用/背景退款、任意子集、显式输入和sharp非OPT gap限制见正文；cube组合措辞异议已实际修复并留记录。
- Status：证明完成，内部独立审查完成；外审、新颖性未认证，UM-TARGET-v1保持OPEN。
- Related Files：[正文](../current/unrelated_machines/two_witness_query_separation.md)；[实际审查](../reviews/unrelated_machines/two_witness_query_separation_review.md)；关联代码/证书和保真来源在审查互链。


## UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2：单正小端级联的完整查询立方体

- ID / Version：`UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2`；新域/锐结论按v2冻结，不改旧Claim。
- Exact Statement：同一批不交Aq对全部S⊆Q同时给完整实际τS，J-unit恰S加并Aq；C≤1+δ(S)，非query unit费精确模加；零端Z保持原零端。仅此normal form。
- Objects / Domain / Quantifiers：每J唯一正小home其它端0/1，U任意unit资格；同一P两actualσ≤1，σ0全J留home，σ1全Q走unit；D/Z按σ1定义。 对每个完整输入成立；全部共同前提见[正文](../current/unrelated_machines/single_home_cascade_query_separation.md)。
- Assumptions / Definitions / Scope：无复杂度假设；原对象显式，实际给定见证或准确slice结构不可略；不是一般UM正反面结论。
- Conclusion：上述构造/锐界按精确定义全量词成立，不以有限测试证明。
- Dependencies：正文列出的全部共同域及自足证明步骤，图derives同时列入；DGR源只作准确Paper Fact。
- Evidence：完整证明、实际陈述先行/读后审查及root核对；实现=audit_only。
- Counterevidence / Objections：无standing fatal；费用/背景退款、任意子集、显式输入和sharp非OPT gap限制见正文；cube组合措辞异议已实际修复并留记录。
- Status：证明完成，内部独立审查完成；外审、新颖性未认证，UM-TARGET-v1保持OPEN。
- Related Files：[正文](../current/unrelated_machines/single_home_cascade_query_separation.md)；[实际审查](../reviews/unrelated_machines/single_home_cascade_query_separation_review.md)；关联代码/证书和保真来源在审查互链。


## UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2：超立方分组菜单的Hall保留与锐3/2实际界

- ID / Version：`UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2`；新域/锐结论按v2冻结，不改旧Claim。
- Exact Statement：所有state选择/组子族union≥cdΣLg；整数Hall给ceil(Lg/2)资源，所有实际P≤3/2且有限例达OPT3/2；d1或Q1 OPT1；d5Q2三变量组每组11/15，实际≤19/15。非hardness。
- Objects / Domain / Quantifiers：d,Q≥1，显式带变量tag的[d]^Q；每variable至多d个groups，incidence索引单射，每state每变量一slice；非空菜单/组变量集。selector1、private incidence1/Lg、resource1。 对每个完整输入成立；全部共同前提见[正文](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)。
- Assumptions / Definitions / Scope：无复杂度假设；原对象显式，实际给定见证或准确slice结构不可略；不是一般UM正反面结论。
- Conclusion：上述构造/锐界按精确定义全量词成立，不以有限测试证明。
- Dependencies：正文列出的全部共同域及自足证明步骤，图derives同时列入；DGR源只作准确Paper Fact。
- Evidence：完整证明、实际陈述先行/读后审查及root核对；实现=none。
- Counterevidence / Objections：无standing fatal；费用/背景退款、任意子集、显式输入和sharp非OPT gap限制见正文；cube组合措辞异议已实际修复并留记录。
- Status：证明完成，内部独立审查完成；外审、新颖性未认证，UM-TARGET-v1保持OPEN。
- Related Files：[正文](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)；[实际审查](../reviews/unrelated_machines/grouped_hypercube_slice_scheduling_review.md)；关联代码/证书和保真来源在审查互链。


## UM-TWO-WITNESS-QUERY-COUNT-FEE-v3：单件查询计数与近单位固定费必要条件

- ID / Version：`UM-TWO-WITNESS-QUERY-COUNT-FEE-v3`；v1零η严格错误和v2修复保留，v3新增heavy必要条件。
- Exact Statement：同族good数≥d−Rβ，实际≤βT并有fee≤W/(d−Rβ)；单件≤ηT时有严格mass界（η0单列）和s=floor(c/η)+1整数分组界。若每singleton必费F且W≤κF，至少d−2floorκ枚query旧端>cT；非主反证。
- Objects / Domain / Quantifiers：任意P同一两actualσ≤有理T>0；D改变jobs、非空Q、d=Q数；使用分离v2同一I>T/2着色族，β∈[3/2,2)、cβ−1、Rβ为query旧端总量>cT的机器数；非负改派权W。 对所有满足共同域的完整输入成立。
- Assumptions：两个实际strict见证与指定非负费用；F>0和W≤κF只用于条件性heavy推论，不默认成立。
- Definitions：LQ_i、Rβ、同染色good族、η、s、heavy H和κ按[正文§5](../current/unrelated_machines/two_witness_query_separation.md)；T>0。
- Scope / Conclusion：给定见证读取费用的必要条件，非一般算法/困难性或任意子集族。
- Dependencies：UM-TWO-WITNESS-QUERY-SEPARATION-v2的同一阈值染色逐机唯一owner/局部负荷不变量，加全部本域与源query组不交计数。
- Evidence：两个真实Exact-first独立重构、原η0反例、修复与读后最终组合；implementation=none，无新有限核验代proof。
- Counterevidence / Objections：η0严格多于d原错已单列修复；old=cT非heavy、rich严格>、κ取floor、W0非严格费均核过；无standing fatal。
- Status：证明与内部审查完成；外审、新颖性未认证，UM-TARGET-v1正反面仍OPEN。
- Related Files：[正文](../current/unrelated_machines/two_witness_query_separation.md)、[审查](../reviews/unrelated_machines/two_witness_query_count_fee_review.md)及其十个原字节来源。


## UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1：严格见证下有gap的重中端占位

- ID / Version：`UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1`；与旧T=1+a、精确unit的域分开。
- Exact Statement / Conclusion：四模式完整actual≤[3/2+(ε+a)/2]T<2T；固定端点gapκ给2−κ/2；允许job跨heavy/medium角色和异端成本，仅测presence，不保指定任务身份或源标签。
- Objects / Domain / Quantifiers：任意P、给T>0及两实际σ0/σ1≤T；只用过端在[0,aT]或[(1−ε)T,T]，0≤ε<1/2、0≤a<1−ε，未用资格任意；两测量heavy-presence00/11。 对所有满足共同域的输入、两个mixed同时成立。
- Assumptions / Definitions：见证已给；仅用这两份实际用过端、heavy按下界分类，gap严格正。
- Scope：不保指定job身份或其它锁定边界，非源decoder/一般算法。
- Dependencies：两heavy匹配分量、非负两选择加权半整化（自足证明）、本严格T和gap共同域。
- Evidence：作者Exact、独立完整重构、Proof读后及canonical最终审查五来源；无新软件/有限核验。
- Counterevidence / Objections：flip需ε+a已真实计入；式(6)控制字符和T0旁称在推送前修正；无standing fatal，不声明全参数锐性。
- Status：证明/实际内审完成，外审、新颖性及主目标未解。
- Related Files：[正文](../current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md)、[审查](../reviews/unrelated_machines/heavy_medium_strict_witness_presence_gluing_review.md)及五个保留原字节来源。


## UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v2：私有身份读口接公共子句的具体失败

- ID / Version：`UM-PROTECTED-CYCLE-CIRCUIT-CLAUSE-OR-FAILURE-v2`；v1零机器退化另立v2补idle，原字节保留。
- Exact Statement / Conclusion：此确切OR接线对所有公式均有det bitpoly完整actual≤1，每非idle机恰一原job，每Rc真由clause qi占据；导出query与返回blocker索引可错配，不能保源NO。
- Objects / Domain / Quantifiers：显式CNF每clause≥2独立文字occurrences、允许重复；变量环/dummy/polarity按正文，q_i内部a/1、私有Ci1及clauseRc1，b_i私有Ci1/pin a，clause u_c可Ci1；a∈(0,1)，空Φ加idle。 对所有公式及其所列真实矩阵成立。
- Assumptions / Definitions：k_c≥2；每occurrence独立物理索引，pin/后继/全部合法端见正文；不假设免费OR或返回与读出同编号。
- Scope：只否定此OR接线，不否定private身份组件或其它medium/共享decoder。
- Dependencies：完整显式矩阵定义、共同job/machine分数匹配证书（x_i1/k_c≤1/2）和二部整数匹配；没有源hardness假设。
- Evidence：root与rank独立Exact-first构证、Proof读后及canonical最终审查；root十job实际端回算是有限校准，非一般证明。
- Counterevidence / Objections：v1空公式不合法已由v2修复；实际q@Rc与返回b可错配，正是失效步骤；无standing fatal。
- Status：限定失败机制证明/内审完成，外审/新颖性未认证，UM-TARGET-v1未解。
- Related Files：[正文§9](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)、[审查](../reviews/unrelated_machines/protected_cycle_shared_clause_or_failure_review.md)及七个保留来源。


## UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2：加权菜单的共同资源与相对OPT

- ID / Version：`UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2`；保留promise-only v1来源，不改旧域。
- Exact Statement / Conclusion：确定性位poly完整实际C≤2−(2−OPT)/(2K)≤(2−1/(2K))OPT，无OPT/witness输入；normalized OPT=2−XOS分配值，bonus精确保OPT；group平均接已知VW factor2，最后单state还原全部原jobs。
- Objects / Domain / Quantifiers：显式非空groups、非空indexed menus每组K_g≤K；每resource跨全部states最多2groups；state私有根互异，selector1只选本组state，每incidence根非负p/resource1，Wstate≤1，无其它jobs/约束。 对每个完整合法结构输入输出具体原σ。
- Assumptions / Definitions：K是显式最大菜单数；resource外端恰1，所有private总量≤1，group标签是输入；V、average、bonus按正文。
- Scope：固定K给该结构类统一改善；非一般UM、degree3、任意外端或succinct菜单。
- Dependencies：完整结构域、已发表VW2010v1 §5.1 Theorem12 degree2 additive factor2，加自足OPT2−V/平均/归一化/原jobs还原共同前提。
- Evidence：实际primary读取、root独立加强/核、general Exact-first完整重构、作者Proof读后及canonical最终审查；软件另记。
- Counterevidence / Objections：OPT2单独处理，未在2上假设资源独占；未先冻结heavy matching；phase success不是精确T可行；零权/empty states/不同Kg已核，无standing fatal。不声明factor锐性。
- Status：数学证明/内部审查完成；直接结构推论，不冒称新SC算法；外审/新颖性未认证，UM-TARGET-v1未解。
- Related Files：[正文](../current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md)、[审查](../reviews/unrelated_machines/degree_two_group_bounded_menu_joint_rounding_review.md)、原VW PDF及七份原字节数学来源。


## UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2：有限组交互的加权菜单实际次二匹配算法

- Objects / Domain / Definitions / Quantifiers：显式非空flat weighted-menu UM；state资源互异、selector1、private p≥0/resource1、state质量≤1；完整菜单资源跨组≤Δ、组交互≤M，Δ≥1/M≥0，无菜单大小界或其它jobs。 对每个所列完整输入成立，定义与退化见[自足正文](../current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md)。
- Exact Statement / Conclusion：不输入OPT/witness，det bitpoly输出全原jobs C≤[2−1/(M+2Δ−1)]OPT；成功绝对≤R，失败OPT≥1+β且输出≤2。所有state bonus精确保OPT；两次matching与精确full-block尾损失。
- Assumptions：恰上述真实原矩阵和结构标签，不输入OPT/未知见证，不隐藏其它资格或原jobs。
- Scope / Limits：固定M/Δ才统一ε；交互按全部菜单并集，state内resource不能重复。非general UM或近2hardness；未实现软件。
- Dependencies：一般ordinary UM模型、完整flat菜单域及本条相应度数假设；正文自足matching/构造证明，不借有限核验或未证源gap。
- Evidence：作者证明、先陈述独立重构、实际作者读后和最终稿全文读后；root亲读原件及独立核。
- Counterevidence / Objections：越域与非fatal措辞意见已在审查保留并关闭；无standing fatal。
- Status：证明完成/多份内部实际审查；外审、新颖性未认证；implementation none，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md)、[审查](../reviews/unrelated_machines/weighted_menu_bounded_group_interaction_rounding_review.md)及其逐SHA原来源。


## UM-DEGREE-THREE-WEIGHTED-MENU-CUBE-EMBEDDING-v1：资源跨组三的加权菜单精确嵌入零权三坐标

- Objects / Domain / Definitions / Quantifiers：显式非空flat weighted-menu UM，state资源互异、质量≤1、资源跨全部menus至多3groups，K/q/M任意；target d=Q=3允许零cell及相同labelvector异state cost。 对每个所列完整输入成立，定义与退化见[自足正文](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)。
- Exact Statement / Conclusion：原jobs含p0/所有selector资格逐身份保留；任意原σ精确同峰扩展、任意targetσ不增投影，actualOPT/K/state mass/group interaction graph精确保持；empty union独占dummy、unused资源仍保。
- Assumptions：恰上述真实原矩阵和结构标签，不输入OPT/未知见证，不隐藏其它资格或原jobs。
- Scope / Limits：仅允许zero与indexed state异cost的target；不保全cell正权或label唯一定价域，不制造源YES/NO gap；固定cube维数不界M。
- Dependencies：一般ordinary UM模型、完整flat菜单域及本条相应度数假设；正文自足matching/构造证明，不借有限核验或未证源gap。
- Evidence：作者证明、先陈述独立重构、实际作者读后和最终稿全文读后；root亲读原件及独立核。
- Counterevidence / Objections：越域与非fatal措辞意见已在审查保留并关闭；无standing fatal。
- Status：证明完成/多份内部实际审查；外审、新颖性未认证；implementation none，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)、[审查](../reviews/unrelated_machines/degree_three_weighted_menu_cube_embedding_review.md)及其逐SHA原来源。


## UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1：归一化菜单与加性Santa Claus的精确实际值桥

- Objects / Domain / Definitions / Quantifiers：显式非空flat weighted-menu UM、每state非负private总量恰1、distinct资源、selector1及resource端1、全部原jobs，无degree或K限制。 对全部所列显式对象/参数成立，完整定义及边界见[自足正文](../current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)。
- Exact Statement / Conclusion：每state一SC agent、每组K_g−1不可拆unitdummy，exact OPT_SC=V与actualOPT_UM=2−V；给定SC allocation与完整UM schedule双向poly解码含C2/t0/K1/V0端点，非优化算法。
- Assumptions：恰所列归一化/不可拆/全部subset量词；没有未述sourcegap、隐式小state表或OPT输入。
- Scope / Limits：只供normalized image源合同，非外部generalSC自动归约；W≤1先bonus再重定义V，full SC row总K_g，resource group degree非agent degree；不制造near2hardness。
- Dependencies：正文明确的完整flat norm1域或same-U norm1 XOS域；自足pigeonhole/原jobs转换或support覆盖计数，无有限审计/外部hardness前提。
- Evidence：作者证明、Exact-first独立重构、实际作者读后及限定章节最终稿审查；root亲读并独核。
- Counterevidence / Objections：§5“任意d项等号”措辞已修≤与support内达到，旧原件保留；无standing fatal，不能扩大为一般归约不可能。
- Status：完整精确结构证明；多份内部实际审查；implementation none、外审/全球新颖性未认证，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)、[实际范围审查](../reviews/unrelated_machines/normalized_weighted_menu_santa_value_bridge_review.md)及逐SHA原件。


## UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2：同宇宙归一化菜单的最小状态数与达到锐界

- Objects / Domain / Definitions / Quantifiers：固定有理η∈(0,1)，t≥1、同U有2t资源，显式非负norm1 indexed XOS clauses；全部t-subsets值1、全部≤floorηt-subsets值≤η；无辅助资源/玩家。 对全部所列显式对象/参数成立，完整定义及边界见[自足正文](../current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)。
- Exact Statement / Conclusion：k=max(1,ceil(floorηt/η))；K_min精确等于每t集含一个k集的最小family Θ；K≥C(2t,t)/C(2t−k,t−k)。d0精确t+1，ηt正整数精确中央二项式达到；固定η一般K≥4^t/[(2t+1)(2t)^(ceil(1/η)−1)]（d≥1）。
- Assumptions：恰所列归一化/不可拆/全部subset量词；没有未述sourcegap、隐式小state表或OPT输入。
- Scope / Limits：只否定同U逐玩家/全部unit-tiny保真/explicit norm1 shortcut；不排辅助全局归约或隐式表示，不供sourcegap；不是2^Ω(源总位长)或poly求Θ。
- Dependencies：正文明确的完整flat norm1域或same-U norm1 XOS域；自足pigeonhole/原jobs转换或support覆盖计数，无有限审计/外部hardness前提。
- Evidence：作者证明、Exact-first独立重构、实际作者读后及限定章节最终稿审查；root亲读并独核。
- Counterevidence / Objections：§5“任意d项等号”措辞已修≤与support内达到，旧原件保留；无standing fatal，不能扩大为一般归约不可能。
- Status：完整精确结构证明；多份内部实际审查；implementation none、外审/全球新颖性未认证，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md)、[实际范围审查](../reviews/unrelated_machines/normalized_xos_menu_threshold_size_review.md)及逐SHA原件。


## UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1：完整加权菜单的资源度三物理路径归约

- Objects / Domain / Definitions / Quantifiers：完整显式flat weighted-menu UM，非空groups/menus、state distinct资源、private非负质量≤1、selector1/resource1；资源跨组度与K/M不限制，zero/empty/unused均保留。 对全部所列输入，完整对象及精确计数见[正文](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)。
- Exact Statement / Conclusion：每旧资源按group分ports，d−1真实两态heavy-only helpers；target资源跨组≤3、K≤max(Kold,2)，任意actual C<2全旧jobs双向不增映射，actualOPT精确保含2；norm1 partial V含0精确保。
- Assumptions：全部辅助group/selector/incidence为真实jobs，完整矩阵无隐含资格，未选states也执行；没有源hardness或OPT输入。
- Scope / Limits：不是general UM到flat的转换；不保group数/M，不提供tiny-gap源；标准BCG2009路径装置非原创，无软件声明。
- Dependencies：完整flat域、ordinary UM；三态另需norm1及前述path实际合同，cube组合另调用原嵌入ID；正文自足，不以有限测试导一般结论。
- Evidence：作者Proof、Exact-first独立重构、作者读后、最终指定章节实读；root亲读并独核全原job和端点。BCG标准路径由root与rainbow实际核原件。
- Counterevidence / Objections：K1正向无singleton已明确特判；原§1–5字节保持，新增不同ID不替旧域；无standing fatal。
- Status：完整限定表示重构/多份实际内审；实现none、未外审、不主张既有装置原创，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)、[真实scope审查](../reviews/unrelated_machines/flat_menu_resource_degree_three_path_reduction_review.md)及逐SHA原始来源。


## UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1：归一化完整菜单的三态与资源度三精确正规形

- Objects / Domain / Definitions / Quantifiers：完整显式flat菜单且每state非负private质量恰1，非空groups/menus、distinct资源、全部原jobs；K/资源跨组度/M任意，原selector在target改为root资格是明示构造。 对全部所列输入，完整对象及精确计数见[正文](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)。
- Exact Statement / Conclusion：先满binary selector树（原states在leaf、真实own资源与unit singletons），后按真实中间memberships路径降度；actualOPT与one-state partial V精确保含2/0，最终K≤3/Δ≤3，任意C<2全原jobs双向poly不增；K1单叶原位。
- Assumptions：全部辅助group/selector/incidence为真实jobs，完整矩阵无隐含资格，未选states也执行；没有源hardness或OPT输入。
- Scope / Limits：source必须norm1 explicit flat，不能免费纳入SCΣp>1行或一般UM；M/原group数不保，不变成one-heavy/two-diffuse；不制造近2NO。
- Dependencies：完整flat域、ordinary UM；三态另需norm1及前述path实际合同，cube组合另调用原嵌入ID；正文自足，不以有限测试导一般结论。
- Evidence：作者Proof、Exact-first独立重构、作者读后、最终指定章节实读；root亲读并独核全原job和端点。BCG标准路径由root与rainbow实际核原件。
- Counterevidence / Objections：K1正向无singleton已明确特判；原§1–5字节保持，新增不同ID不替旧域；无standing fatal。
- Status：完整限定表示重构/多份实际内审；实现none、未外审、不主张既有装置原创，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)、[真实scope审查](../reviews/unrelated_machines/normalized_flat_menu_three_state_degree_three_normal_form_review.md)及逐SHA原始来源。


## UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1：裸笛卡尔菜单的精确反向放大

- Objects / Domain / Quantifiers / Definitions：t>=1，D=2^t，全部二元affine-line Cartesian groups/states/resources，private 1/D及unit selector/resource，全部原state jobs。 对全部所列参数成立；完整矩阵/额外语义及所用符号见[正文](../current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)。
- Exact Statement / Conclusion：任意partial与任意group state重选的精确V_t=1−2^-t，完整actualOPT(P_t)=1+2^-t；cyclic跨坐标labels构造达界，任意补组交一点给全调度下界。
- Assumptions：非空t>=1显式族、不可拆资源、全部原jobs；额外一致性仅第二ID，ordinary P未免费实现。
- Scope / Limits：只否定明示裸Cartesian菜单NO乘幂；不排其它产品/物理一致性/source image，不供hardness；degree随D增长，后接精确正规形不恢复NO。
- Dependencies：完整二元Cartesian菜单定义；第一ID用普通UM与cyclic方程，第二用额外f一致性和全子集Hall整数matching；常数修复后果共同用两ID。
- Evidence：完整作者Proof、Exact-first独立重构、实际作者读后/最终限定章节审查；root实际亲读。第一ID有限t1..4全原矩阵核验及t1完整1024枚举另列checks，非一般证明前提。
- Counterevidence / Objections：t0明确排除；C>=2不套unit独占；跨资源度D非3；无standing fatal。
- Status：完整限定结构结果；实际内部审查；第一ID仅audit_only、第二none；未外审或认证全球新颖性，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)、[实际审查](../reviews/unrelated_machines/cartesian_menu_reverse_amplification_review.md)及原字节来源。


## UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1：逐坐标状态一致性下的精确整数资源配额

- Objects / Domain / Quantifiers / Definitions：同二元t>=1族，额外强制全体group状态ell_i(g)=f_i(g_i)，各固定f_i任意；partial资源子集仍完全自由且全局不交。 对全部所列参数成立；完整矩阵/额外语义及所用符号见[正文](../current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)。
- Exact Statement / Conclusion：每一固定f族及优化f后的值均精确floor((3/2)^t)/2^t；全子集Hall给显式位多项式整数配额构造。与bare值共同排除同族统一常数保值的事后一致性修复。
- Assumptions：非空t>=1显式族、不可拆资源、全部原jobs；额外一致性仅第二ID，ordinary P未免费实现。
- Scope / Limits：一致性仅为额外语义，未用实际普通P实现，不能作为NO解码免费约束；无hardness源或一般UM反面。
- Dependencies：完整二元Cartesian菜单定义；第一ID用普通UM与cyclic方程，第二用额外f一致性和全子集Hall整数matching；常数修复后果共同用两ID。
- Evidence：完整作者Proof、Exact-first独立重构、实际作者读后/最终限定章节审查；root实际亲读。第一ID有限t1..4全原矩阵核验及t1完整1024枚举另列checks，非一般证明前提。
- Counterevidence / Objections：t0明确排除；C>=2不套unit独占；跨资源度D非3；无standing fatal。
- Status：完整限定结构结果；实际内部审查；第一ID仅audit_only、第二none；未外审或认证全球新颖性，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)、[实际审查](../reviews/unrelated_machines/coordinate_oblivious_cartesian_menu_quota_review.md)及原字节来源。


## UM-CARTESIAN-COORDINATE-CONSTANT-REPAIR-OBSTRUCTION-v1：两种精确值共同推出的修复限制

- Objects / Domain / Quantifiers / Definitions：上述同一二元完整Cartesian族所有t>=1，输入任意高值bare allocation，输出同groups/resources/states的coordinate-oblivious allocation；统一c>0不依赖t。
- Exact Statement / Conclusion：不存在此输出保证minvalue至少c乘输入minvalue的合同，即使不要求可计算。将其用于bare达界witness即迫c<=floor((3/2)^t)/(2^t−1)，右侧趋0。
- Assumptions / Dependencies：共同使用UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1与UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1的两种精确值，graph两前提均列。
- Scope：只排同族、受限输出的统一正乘法保值修复，不排改变实际任务/资源/状态的新归约；不提供物理一致性或hardness源。
- Evidence / Counterevidence / Status：正文§7证明；general实际canonical §6–7审查明确重证该比值矛盾；root独核，无standing fatal。是完整直接推论、非另一个发现过程；implementation none、外审/全球新颖性未认证。
- Related Files：同上两Claim的[正文](../current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md)及[一致性实际审查](../reviews/unrelated_machines/coordinate_oblivious_cartesian_menu_quota_review.md)。


## UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1：q元菜单线性重选与逐坐标一致性的精确差异

- Objects / Domain / Definitions / Quantifiers：primepower q>=2、t>=1的完整affine-line菜单；cyclic、全部affine A,c、任意coordinatewise f三域分别优化，partial subsets完全自由。 全部所列参数与具体原矩阵见[正文](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)。
- Exact Statement / Conclusion：V_cyc=V_aff=1−ceil((q−1)^t/q)/q^t，V_sep=floor((q−1+1/q)^t)/q^t；每域完整受限实际峰2−V，固定q分别趋1/0；固定A的quota由Σ_a q^rank(A−diag a)精确给出。
- Assumptions：显式有限域表示与完整ordinary P、不可拆资源、所有原jobs；额外选择语义只在相应受限ID中使用，非免费机器约束。
- Scope / Limits：q>2不将affine上界升级全nonlinear；C_sep不是原无约束OPT，一致性未物理实现，无near2源。
- Dependencies：完整q元菜单定义与ordinary任务规则；binary另需q2及block-fiber条件；正文直接给线性代数/网格计数/Hall或并发投影/遗漏双计数，有限计算不是推导前提。
- Evidence：作者完整Proof、独立Exact-first重构、实际作者读后、final指定章节重读；root亲核并实读来源，非投票认证。
- Counterevidence / Objections：共用空选择域措辞补非空，三位实际逆替换核字节；binary generic字母typing明确；旧v1/首写/final来源均保留，无standing fatal。
- Status：限定结构证明完整，多份实际内审；implementation none、外审/全球新颖性未认证。非近二源，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)、[指定scope审查](../reviews/unrelated_machines/qary_affine_menu_recoupling_consistency_review.md)及逐SHA原件。


## UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1：二元分块一致性精确配额与无环链逃逸

- Objects / Domain / Definitions / Quantifiers：q2、t>=1完整菜单，固定非空blocks partition，只限制每block的标签看同block输入，F任意非线性；全部任意partial仍全局不交。 全部所列参数与具体原矩阵见[正文](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)。
- Exact Statement / Conclusion：H=prod_j(2^b_j−1/2)，精确Q=floorH/2^t、union≤2^t H且达到；固定maxblock L指数衰减。另固定无环单输入链ell1=0,elli=g_(i−1)精确quota1/2，union N(N+1)/2。
- Assumptions：显式有限域表示与完整ordinary P、不可拆资源、所有原jobs；额外选择语义只在相应受限ID中使用，非免费机器约束。
- Scope / Limits：binary逻辑条件非physical guard；不称优化全部无环函数值恰1/2，不将2−Q冒称原OPT，不排其它compiler。
- Dependencies：完整q元菜单定义与ordinary任务规则；binary另需q2及block-fiber条件；正文直接给线性代数/网格计数/Hall或并发投影/遗漏双计数，有限计算不是推导前提。
- Evidence：作者完整Proof、独立Exact-first重构、实际作者读后、final指定章节重读；root亲核并实读来源，非投票认证。
- Counterevidence / Objections：共用空选择域措辞补非空，三位实际逆替换核字节；binary generic字母typing明确；旧v1/首写/final来源均保留，无standing fatal。
- Status：限定结构证明完整，多份实际内审；implementation none、外审/全球新颖性未认证。非近二源，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)、[指定scope审查](../reviews/unrelated_machines/binary_cartesian_block_fiber_quota_review.md)及逐SHA原件。


## UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v2：任意非线性选态的并发投影与全局缺项界

- Objects / Domain / Definitions / Quantifiers：全部q>=2 primepower、t>=1完整菜单，任意nonlinear ell/任意partial，整数每组缺d∈[0,N]；projection恒等式仅对真实concurrent fiber非空子family。 全部所列参数与具体原矩阵见[正文](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)。
- Exact Statement / Conclusion：并发union精确Σ_J(q−1)^|J| |π_JF|，遗漏预算推出h(k)≤kd，K(d)为合法最大k；全局必dK(d)≥(q−1)^t，仅必要非充分。q3t2无约束V7/9/actual11/9，新增q3t3精确V8/9/actual10/9。
- Assumptions：显式有限域表示与完整ordinary P、不可拆资源、所有原jobs；额外选择语义只在相应受限ID中使用，非免费机器约束。
- Scope / Limits：粗projection非全参数sharp，不闭合一般nonlinear最优；旧strict2d<q不加等号，无free coherence/no hardness。
- Dependencies：完整q元菜单定义与ordinary任务规则；binary另需q2及block-fiber条件；正文直接给线性代数/网格计数/Hall或并发投影/遗漏双计数，有限计算不是推导前提。
- Evidence：作者完整Proof、独立Exact-first重构、实际作者读后、final指定章节重读；root亲核并实读来源，非投票认证。
- Counterevidence / Objections：共用空选择域措辞补非空，三位实际逆替换核字节；binary generic字母typing明确；旧v1/首写/final来源均保留，无standing fatal。
- Status：限定结构证明完整，多份实际内审；implementation none、外审/全球新颖性未认证。非近二源，UM-TARGET-v1仍OPEN。
- Related Files：[正文](../current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md)、[指定scope审查](../reviews/unrelated_machines/qary_affine_menu_near_full_deficit_review.md)及逐SHA原件。


## UM-MACHINE-UNIFORM-QUERY-RETURN-INDEX-EXCHANGE-v2：逐机统一时间的查询返回严格索引交换

- Objects / Domain / Definitions / Quantifiers：任意固定辅助集A、k≥2不同q/b、内部每机finite时间统一s_h≥0或∞、T>0，任意资格；给两aligned strict见证。
- Exact Statement / Conclusion：inactive在T不可行则两方向mismatch均在T可行；给两实际见证可总位多项式输出inactive或指定mismatch，全辅助保留；容量截N处理0及tiny。
- Assumptions / Dependencies：完整原P与[正文](../current/unrelated_machines/machine_uniform_query_return_index_exchange.md)指定域，所有原jobs须执行；固定辅助/正权/半权ρ或tag-degree-intercept等分别承重，不跨ID相互借用。标准matching、容量计数或Hall在正文自足重构，外部hardness与finite checks非推导前提。
- Scope：仅内部/私有outside封装；不保证真实共享外部负载。单容量v1只模式matching化约，不称原矩阵包含；无端辅助使前件失败、不冒称非法UM合法。
- Evidence：rank分别仅读v1/v2 Exact独立重构，冻结后才实际读v2作者Proof；随后实际全文读current b930…认证完整v2。Root亲读所有原件、独核容量截断/增广，并明确封装合法性的aligned前件；旧原记录不回改，无单独v1作者Proof。标准matching技术已扣除。
- Counterevidence / Objections：实际审查所提边界精确化已在current闭合；全部源保原字节。 无standing fatal。
- Status：限定数学证明完整、实际独立重构及final范围审查；implementation none/audit_only分开，外审与全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/machine_uniform_query_return_index_exchange.md)、[实际审查](../reviews/unrelated_machines/machine_uniform_query_return_index_exchange_review.md)及逐SHA原件；证书/代码仅按登记的finite身份。


## UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1：异权直接共居严格SAT与全公式三半逃逸

- Objects / Domain / Definitions / Quantifiers：每clause≥2实际occ的显式CNF，环padding≥3；ρ∈(1/2,1)，逐occ正异权x+y≤1；全部q/b/u原jobs、dummy与空式idle单列。
- Exact Statement / Conclusion：strict≤1 iff SAT且同编号返回由实际容量推出；任意公式/异权均可不用源解输出全部原jobs实际≤3/2，baseline与active在一个共同匹配内恢复。
- Assumptions / Dependencies：完整原P与[正文](../current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)指定域，所有原jobs须执行；固定辅助/正权/半权ρ或tag-degree-intercept等分别承重，不跨ID相互借用。标准matching、容量计数或Hall在正文自足重构，外部hardness与finite checks非推导前提。
- Scope：只排此改动后的direct co-location矩阵；不同旧D/h及公共Rc输入不回改，不否一般medium复制或所有source-to-UM桥。
- Evidence：typed仅据Exact独立重构先冻6d853…，作者rainbow的策略摘要其后才到达；再授权实际读Proof、最终全文读3e6ac…但正式只B§1–3。root实际通读所有来源并独核fractional perfect matching、所有原任务恢复和每机异权负载。§4 C仅context，不由typed代审。
- Counterevidence / Objections：实际审查所提边界精确化已在current闭合；全部源保原字节。 无standing fatal。
- Status：限定数学证明完整、实际独立重构及final范围审查；implementation none/audit_only分开，外审与全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)、[实际审查](../reviews/unrelated_machines/weighted_direct_cohabiting_query_return_review.md)及逐SHA原件；证书/代码仅按登记的finite身份。


## UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1：半权直接共居SAT编译的精确三半阈值

- Objects / Domain / Definitions / Quantifiers：同明示全原矩阵但固定真实x=y=1/2、dummy x1、3/4<ρ<1；所有域内CNF，空式idle0。
- Exact Statement / Conclusion：非空SAT真实OPT1，非空UNSAT真实OPT3/2；任意完整C<3/2实际调度可det-bit-poly解码SAT，等号不能扩。
- Assumptions / Dependencies：完整原P与[正文](../current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)指定域，所有原jobs须执行；固定辅助/正权/半权ρ或tag-degree-intercept等分别承重，不跨ID相互借用。标准matching、容量计数或Hall在正文自足重构，外部hardness与finite checks非推导前提。
- Scope：固定3/2的锐界不是near2反面，不排所有统一小ε；可选unit端本身不是OPT下界，非空下界单独证明。
- Evidence：root新陈述先交general，仅给原P定义/既有结论，不交root Proof；general先冻独立初稿/final并自枚举5184分配，root实读后才解封作者statement/Proof，再最终通读3e6ac…正式只C§1/4。原初稿/final字节保留。C独立重证容量/环方向，不借B异权active匹配。root另自建固定审计比两份原矩阵并全枚举同hist；finite checks不是一般proof。
- Counterevidence / Objections：实际审查所提边界精确化已在current闭合；全部源保原字节。 无standing fatal。
- Status：限定数学证明完整、实际独立重构及final范围审查；implementation none/audit_only分开，外审与全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md)、[实际审查](../reviews/unrelated_machines/direct_cohabiting_sharp_three_halves_review.md)及逐SHA原件；证书/代码仅按登记的finite身份。


## UM-LST2025-AFFINE-LINE-SOURCE-UNIFORM-COMPILATION-OBSTRUCTION-v1：仿射线集合打包源的均匀菜单编译障碍

- Objects / Domain / Definitions / Quantifiers：prime R≥2、k≥1，每constraint k个不同变量，每变量indexed constraint-degree≤R、注入intercept、tag分离、所有显式allowed tuple菜单非空；uniform 1/(kR)。
- Exact Statement / Conclusion：任意local state选择都可对全部Hall子集分配每group ceil(kR/2)项，输出全部原jobs峰≤2−ceil(kR/2)/(kR)≤3/2；不求源assignment。
- Assumptions / Dependencies：完整原P与[正文](../current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)指定域，所有原jobs须执行；固定辅助/正权/半权ρ或tag-degree-intercept等分别承重，不跨ID相互借用。标准matching、容量计数或Hall在正文自足重构，外部hardness与finite checks非推导前提。
- Scope：constraint-as-group/tuple-as-state特定编译；不排tuple-as-group+dummy；空relation不合法且须另证promise。源仅near-perfect YES且NP⊆BPP例外，不能改成perfect或P≠NP。
- Evidence：fee仅据Exact独立完成所有Hall子集，实际核在线arxiv v1 §2–4，然后才实际读作者Proof。root另下载原14页PDF并亲读同位置，不冒认fee下载了root字节。fee实读c50…后提出tuple句过强，最终f740…改为不再自动保证，逆替换核旧hash；主数学未变。标准pair-overlap/Hall直接应用已从新颖性扣除。
- Counterevidence / Objections：实际审查所提边界精确化已在current闭合；全部源保原字节。 无standing fatal。
- Status：限定数学证明完整、实际独立重构及final范围审查；implementation none/audit_only分开，外审与全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)、[实际审查](../reviews/unrelated_machines/lst2025_affine_line_uniform_compilation_review.md)及逐SHA原件；证书/代码仅按登记的finite身份。


## UM-PARTIAL-SUM-TAKE-CONTINUE-FLAT-MENU-ACTUAL-ESCAPE-v1：累计take继续路径的实际八五逃逸反例

- Objects / Domain / Definitions / Quantifiers：明示3源agents/2不可拆items值3/5；目标每a为take1/off-take2/off-accept三组、五state，全26机30job57finite。
- Exact Statement / Conclusion：source SC OPT0，目标partial V2/5、完整ordinary UM OPT8/5；此明示additive take/continue规则不存在任意正常数全agents正值decoder，即使重排全部源items。
- Assumptions / Dependencies：完整原P与[正文](../current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)指定域，所有原jobs须执行；固定辅助/正权/半权ρ或tag-degree-intercept等分别承重，不跨ID相互借用。标准matching、容量计数或Hall在正文自足重构，外部hardness与finite checks非推导前提。
- Scope：只否所列AND拆分规则，不否所有DAG compiler/既有normalized leaf selector-tree；不认证最小性或一般sourcehardness。
- Evidence：必须保留路由纠正：原misnamed Exact本身含完整Proof，general先读后的原Exact-only标签不能充盲审，另冻scope correction撤回该身份；其实际Fraction证书保留。root另造真正statement-only，此前未读原Proof的fee独立给完整30-job证书/任意调度lower后才读作者源，满足真实陈述先行。fee随后实读canonical及E固定checker/output，未冒称自己运行或亲核其未读raw cert。root独建矩阵逐57条资格相等，全部30任务/26loads/9bundles Fraction核验；无E优化枚举。
- Counterevidence / Objections：旧误Exact-only审查已另冻scope correction，不能作blind；fee真正statement-first闭合。 无standing fatal。
- Status：限定数学证明完整、实际独立重构及final范围审查；implementation none/audit_only分开，外审与全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)、[实际审查](../reviews/unrelated_machines/partial_sum_take_continue_actual_escape_review.md)及逐SHA原件；证书/代码仅按登记的finite身份。


## UM-GENERAL-WEIGHTED-QUERY-RETURN-THREE-HALVES-EXCHANGE-v1：任意异权内部查询返回的三半二选一交换

- Objects / Domain / Definitions / Quantifiers：固定辅助A、k≥2不同q/b，任意非负异权内部H，边界各有自身私有outside:T，T>0；给同一完整P的两aligned实际T见证。
- Exact Statement / Conclusion：det-bit-poly输出inactive或指定cross(j,i)完整实际≤3T/2，所有A保内部、每原job一次、内部端仅取两见证已用端；inactive在1.5T被禁则每指定cross已可行。
- Assumptions / Dependencies：UM-MODEL-v1, UM-TWO-WITNESS-QUERY-SEPARATION-v2, UM-GENERAL-WEIGHTED-PRIVATE-OUTSIDE-INTERFACE-DOMAIN-v1；[正文](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)的完整原资格/原jobs和给定见证为承重，不跨域借用。
- Scope：外部私有封装不可免费替共享变量环；不给未知strict见证finder，多个boundary bundles或A外送未覆盖；不是一般UM算法/源hardness。
- Evidence：general仅据Exact及实际旧query-separation全文独立构证先冻，再读作者Proof，最后实读6074…全文正式仅§1。独立P0保全部jobs后移出q_i，与作者P*先删q_i再恢复是等价路线；都没有零端遗留或漏原任务。root实际读全部来源并亲核。该结论是旧v2不交支持合同的直接推论，标准分离算法新颖性明确扣除。
- Counterevidence / Objections：shared outside反例界定local外接边界；pool good最优不等于任意rho；所有zero/empty/unknown见证与实际环负载已单列，无standing fatal。
- Status：限定数学完整、真实独立重构/作者读后/final指定范围；implementation none，外审/全球新颖性未认证，主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)、[实际审查](../reviews/unrelated_machines/general_weighted_query_return_exchange_review.md)及逐SHA原件。


## UM-PRIVATE-CLAUSE-QUERY-RETURN-UNIVERSAL-THREE-HALVES-v1：任意私有异权子句网络与真实变量环的全公式三半上界

- Objects / Domain / Definitions / Quantifiers：显式CNF每clause≥2occ、变量环padding≥3；clause内部Hc/Ac私有，q外部恰两ring端、b恰polarity pin，外部time∈[0,T]；dummy固定，给每索引singleq/singleb局部strict证书。
- Exact Statement / Conclusion：任意SAT/UNSAT全原P实际≤3T/2，每原ring机恰一真实q/b负载≤T，所有Ac/dummy/边界原jobs一次；给全部局部见证det-bit-poly，没有见证只承诺存在OPT上界。
- Assumptions / Dependencies：UM-MODEL-v1, UM-GENERAL-WEIGHTED-QUERY-RETURN-THREE-HALVES-EXCHANGE-v1, UM-PRIVATE-CLAUSE-REAL-RING-INTERFACE-DOMAIN-v1；[正文](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)的完整原资格/原jobs和给定见证为承重，不跨域借用。
- Scope：不同clause共享真实机/jobs、Ac外送、非全索引strict可选、多q/b bundle或其它外部资格未覆盖；标准matching/分离组合不作为near2主反面。
- Evidence：fee先只读主Exact、local新Exact及旧分离正文，未把未审local当黑箱，而从染色机制独立重证，再用N+h实际ring matching给全模板。其原wrapper中δ=T未谎称0：query旧outside无入流不触发、H无旧query的更细位置不变量足够。冻结独立全证后才实读两个作者Proof：分析零端δ0及2N+h图是等价新路线，旧记录保留；最后实际读canonical正式§2–3。root实际亲核全部原jobs与共同负载。
- Counterevidence / Objections：shared outside反例界定local外接边界；pool good最优不等于任意rho；所有zero/empty/unknown见证与实际环负载已单列，无standing fatal。
- Status：限定数学完整、真实独立重构/作者读后/final指定范围；implementation none，外审/全球新颖性未认证，主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)、[实际审查](../reviews/unrelated_machines/private_clause_query_return_universal_review.md)及逐SHA原件。


## UM-SHARED-OUTSIDE-SMALL-QUERY-RETURN-POOL-EXACT-RELATION-v1：共享外端小查询返回池的全部模式精确关系

- Objects / Domain / Definitions / Quantifiers：k≥2、正有理a_i总≤1，q_i仅H:a_i/E_i:1，b_i仅任一k−1池P_r:1/E_i:1，2k机/2k原jobs；任意query内部集S/return外部集T，池分配自由优化。
- Exact Statement / Conclusion：pattern OPT恰1 iff 非空T⊆S，否则恰2；任意actual C<2本已≤1且解码非空containment；明确容许多queries/returns。§4标准4×4共享环说明internal交换不能免费外接。
- Assumptions / Dependencies：UM-MODEL-v1, UM-SHARED-OUTSIDE-SMALL-POOL-DOMAIN-v1；[正文](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)的完整原资格/原jobs和给定见证为承重，不跨域借用。
- Scope：孤立模块恒OPT1无sourceNO，新增q outside端/E同一化/实际额外jobs须重证；不保证S=T、singleton或变量一致性，不升级新颖性/困难性。
- Evidence：bicriteria分别仅据两Exact独立重构：四环全部16模式及任意k pool所有S/T/rho，冻结后才各读作者Proof，最终实际读canonical正式§4/§5。四环不新立Claim；pool当前新ID只是精确关系身份。其k2..4辅助4328分配检查仅归reviewer，未登记软件或root运行，一般证明为任意k计数。root实际读全部来源并独核数学。
- Counterevidence / Objections：shared outside反例界定local外接边界；pool good最优不等于任意rho；所有zero/empty/unknown见证与实际环负载已单列，无standing fatal。
- Status：限定数学完整、真实独立重构/作者读后/final指定范围；implementation none，外审/全球新颖性未认证，主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md)、[实际审查](../reviews/unrelated_machines/shared_outside_small_query_pool_review.md)及逐SHA原件。


## UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1：仿射线逐tuple分组加全局dummy的完整三半逃逸

- Objects / Domain / Quantifiers / Definitions：primeR≥2/k≥1/tagged affine lines，relation-degree≤R/intercept注入，A_g可空；n为tuples总数/m0非空表数，1≤q≤m0，d=n−q；每tuple group为原D=kR均匀state或任一globaldummy singleton，所有原jobs。
- Exact Statement / Conclusion：不求源解可det-bit-poly输出全部原jobs实际≤2−ceil(kR/2)/(kR)≤3/2；完整unit可行iff原full-set packing≥q。
- Assumptions / Dependencies：UM-MODEL-v1与明示完整矩阵，degree/intercept/tag/uniform及dummy计数承重；line几何与Hall自足重构，不调用primary hardness或有限实验。
- Scope：只排uniform原权/d=n−q个globaldummy及q≤m0的具体桥，空relation不偷换原sourcepromise；不排其它grouping、权重/guard/阈值或一般source-to-UM归约。
- Evidence：rank先仅据root精确消息及旧current前27行明示source定义独立全证，未读旧Hall证明或新作者Proof；root实际读e8eed…后才冻结正式statement与Proof，rank随后实际读后，不倒填当时已读正式文件。最终canonical初稿22c…的dense逗号排版错误经指出改为显式乘号，rank实读edc…后逆替换精确核回旧hash，原statement/Proof/独立记录均保原字节。root亲核全部Hall子族、全部states原任务及任意unit分配提取，当前无standing fatal。
- Counterevidence / Objections：dense公式逗号排版改显式乘号，final逆替换核old hash；source empty关系与q=n分开，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/final全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md)、[审查](../reviews/unrelated_machines/affine_line_tuple_groups_global_dummy_review.md)及逐SHA原件。


## UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v3：完整归一化菜单的配置证书保持与三行三度SC间隙

- Objects / Domain / Quantifiers / Definitions：非空显式normalized-flat、非空indexed menus、state非负有理总质量1、可有零incidence/unused/重复state；machine CONFIG阈值恰1；SC路径任意非空old agents/有限非负估值，前向正阈值≤1、逆向任意正阈值。
- Exact Statement / Conclusion：完整flat machine CONFIG(1) iff positive-support FSLP iff state-dummy SC CONFIG(1)；tree/menu-path双向保unit证书；SC path在old actual/CFG最高≤1时各精确保并降item度3，最终row3/degree3族CFG1而actual1/D。
- Assumptions / Dependencies：无复杂度假设；UM-MODEL-v1、明确有限证书域，实际V与state-dummy/normalform两旧Claim共同前提；fractional保持在正文自足重证。
- Scope：限定finite证书而非未知CONFIG oracle；不保一般UM或arbitrary machine阈值/全边际；SC路径不自动归一一般row。自足D族为actualNO，不排actualOPT≥1常数finder，不提供near2源hardness。
- Evidence：general先冻结独立pre-Exact，再仅v1 Exact独立全证；仅v3 Exact另重构新增machine CFG桥/SC层path，不读v2或作者Proof；root实读两份独立记录后才放v1/v3 Proof。general实际全文读后另冻记录，再实际全文审最终canonical header与§1–7；root全部实读，zero/empty/helper双copy/位长无standing fatal。
- Counterevidence / Objections：先前all-membership与最终positive LP分开；SC path forward仅≤1/reverse任意positive，helper可取双copy；actualNO不作YES反例，当前无standing fatal。
- Status：限定证明完整，真实独立先行/作者读后/最终全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md)、[审查](../reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md)及逐SHA原件。


## UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1：并行线性关系的任意状态重赋权仍可半保留

- Objects / Domain / Quantifiers / Definitions：primeR≥2/k≥2，R个groups共k变量且indices=j，完整A_j={a:Σa=j}、taggedR² lines；各state任意非负有理norm1权，允许zero，全表显式。
- Exact Statement / Conclusion：任意state-dependent norm1重赋权均有affine-in-j选态/真实partial≥1/2及全原jobs actual≤3/2；source value1/R，另singleton关系可V0/OPT2。
- Assumptions / Dependencies：UM-MODEL-v1与完整矩阵/prime/k≥2/全部sum关系/任意norm1权；有限域双射/条件平均/资源回填自足，不调用hardness或有限实验。
- Scope：只排保持该完整sum关系/groups/states/resources/eligibilities且仅改权、对整个包含本族NO域一概V<1/2的接口；不排避开本族的hard image、额外结构/预处理/其它gadget；非near2困难性。
- Evidence：root先听作者口头策略，核对不记盲审；rank仅Exact独立全证冻865ed…，root实读后才放Proof17bf…；rank实际读后6ac…再正式最终canonical header+§1–4全文审，root所有记录均实际读，conditional均匀/唯一例外回填/全部原job与可变k显式位poly闭合，无standing fatal。
- Counterevidence / Objections：k1/singleton关系给V0/actual2，主k≥2完整关系承重；不误套hard image，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/final全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md)、[审查](../reviews/unrelated_machines/weighted_affine_parallel_relation_reweighting_review.md)及逐SHA原件。


## UM-UNRELATED-AUX-HEAVY-READOUT-BULK-OR-COMMIT-SPLIT-v3：任意异权辅助与重读口的批量OR三半逃逸

- Objects / Domain / Quantifiers / Definitions：r≥2/偶k≥2/ρ∈(.5,1)完整block-ring双池；J只接任意unrelated非负I或正C，全部J在C端∈(.5,1]；给同P两份不同一真完整实际strict≤1调度。
- Exact Statement / Conclusion：det-bit-poly构造全部原jobs全False实际≤1.5，J各仅取自身两witness原端，I≤1.5/C,M≤1/正pool≤1.5；只承诺witness存在则仅存在结论，原OPT1非sourceNO。
- Assumptions / Dependencies：无复杂度假设；UM-MODEL-v1与明示完整backbone/J资格/两actual strict模式，自足排序配对与整数流；不调用未知见证finder。
- Scope：只排该独立committer已有两完整strict模式的weak抗split；不排缺两全局strict见证的跨子句NO，不覆盖J到ring/pool/负C或C≤.5小端/其它backbone；不提供一般算法/near2困难性。
- Evidence：root与fee共同推导，不记root盲审；general分别仅v1/v2/v3 statement独立重构并冻结b26…/ab4…/698…，root全文实读后才统一放三版作者Proof；general实际全文读后9de…，再正式canonical header+§1–5全文审，root每份实际读。固定同端/重复occurrence两路线与maxF/分段回填均合法，全部aux共用同一流，无standing fatal。
- Counterevidence / Objections：重C边界严格>.5，C输出≤1非恰1；I仅≤1.5，fixed C扣gate，原OPT1/conditionalFalse与sourceNO分开，无standing fatal。
- Status：限定证明完整，真实独立先行/作者读后/最终全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md)、[审查](../reviews/unrelated_machines/bulk_or_commit_two_witness_interpolation_review.md)及逐SHA原件。


## UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1：单标签边际均匀的仿射线菜单仍有趋二实际间隙

- Objects / Domain / Quantifiers / Definitions：primeR≥3、完整tagged F_R² line planes、各变量intercept单射、state-dependent非负有理norm1权含全部zero；显式main与R(R−1)helper，每group Rstates、各incidence label单边际uniform。
- Exact Statement / Conclusion：对每primeR≥3显式族，任意partial选择最优V=1/(R−1)，全原jobs普通UM实际OPT=2−1/(R−1)，显式达界assignment；fresh零权变量padding使共同arityR/R-partite并精确保值。
- Assumptions / Dependencies：UM-MODEL-v1与primeR≥3/完整norm1 tagged-LINE矩阵/main-helper显式族；资源挤占/完整调度/零权padding与有限域代数自足，不调用CONFIG、hardness或有限实验。
- Scope：仅反驳真tagged-LINE几何加uniform单标签边际足以保证任意state-dependent权正常数partial值；main/helper关系并非pairwise independent，不认证Chan/LST hard image、源value、CONFIG新值或near2计算困难性；UM-TARGET-v1仍OPEN。
- Evidence：root先听作者口头策略，核对不记盲审；rank仅Exact独立全证冻0d8a…，root实际全文读后才放作者Proof c502…；rank实际作者读后df172…再审canonical header+§1–4全文b661…，root全部实际读，任意helper选态、完整actual含zero/padding/counts/显式位poly均闭合，无standing fatal。
- Counterevidence / Objections：不是局部pairwise-independent关系；任意helper/全部未选和zero jobs均包含，R2不在域；source hard image未认证，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/final全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/tagged_affine_line_uniform_marginal_gap.md)、[审查](../reviews/unrelated_machines/tagged_affine_line_uniform_marginal_gap_review.md)及逐SHA原件。


## UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v2：宽标签矩形的仿射线重细资源共同避冲突

- Objects / Domain / Quantifiers / Definitions：primeR≥2/完整tagged-LINE norm1 states含zero、fixed injective intercepts；显式Cartesian标签矩形最小边长L、每line≤b marks、其余点权≤β，D变量度/M逐组共享数/q最大arity；L>b(D−1)。
- Exact Statement / Conclusion：det-bit-poly共同选真实indexed states与disjoint B，保全部selected marks及独占点，每组≥max(0,1−Mβ)，全部原UM jobs≤2−该值；sparse β0给actualOPT1，任意权L>2q(D−1)²给actual≤1.5，D1直接OPT1。
- Assumptions / Dependencies：UM-MODEL-v1与完整norm1 tagged-LINE域/宽Cartesian labels/固定截距/marked-unmarked界及严格slack；几何与共同分配自足，不调用CONFIG、hardness或有限实验。
- Scope：仅wide Cartesian rectangles加label slack的输入子域；不从pairwise independence或alphabet可增推全部LST/Chan hard images满足，所有固定intercepts量词明确，不提供source perfect completeness/hardness/NO decoder，UM-TARGET-v1仍OPEN。
- Evidence：bicriteria只据v2 Exact独立全证冻f2786…，root实际全文读后才放作者Proof e725…，再actual读后2c8a…，最终canonical header+全部§1–5实审b1cb…；root所有记录实际读，root先听口头策略不记盲审。v1仅历史Exact，root实际读，不冒reviewer读v1/无v1 Proof。
- Counterevidence / Objections：state-dependent marks查真实index后才用；不主张所有supports不交；R2等号有V0/actual2，所以严格slack承重；hard-image域未认证，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/final全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape.md)、[审查](../reviews/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape_review.md)及逐SHA原件。


## UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4：一般两完整见证插值与批量全False的实际池端义务

- Objects / Domain / Quantifiers / Definitions：一般显式P/T≥0/两完整actual≤T/F原任务指定legalν，含zero与空任务；bulk完整原ring双pool/r≥2/偶k/ρ>.5/两不同一真全actual1，任意非负unrelated J接全部非pool或全部原机。
- Exact Statement / Conclusion：det-bit-poly同一τ：非F仅自身两actual端，逐机件数≤ceil(N_i/2)、负载≤t_i+(L_i0+L_i1+d_i)/2；bulk nonpool J全False≤1.5，任意pool J≤1.5+d/2，near2排除要求两新正pool实际used近unit J且同job实际改派。
- Assumptions / Dependencies：UM-MODEL-v1与完整两actual/F合法ν/全部非F实际端数据；bulk原backbone定义及两一真witness；标准配对整数流自足，不依旧v3 quota强输出、hardness或有限实验。
- Scope：给定两完整actual witnesses，未知时只推出存在；不提供普通UM新ratio或源NO。只新§6–10，旧v3前缀8153bytes/限定强输出保原值；新M/C仅≤1.5。pool必要事件不是充分decoder，UM-TARGET-v1仍OPEN。
- Evidence：typed先冻非pool特化v1，root独立闭合/建议一般域，共同参与不记blind；rank仅v4 Exact独立全证81bd…，root实际读后才放作者Proof d5e…，actual读后2f3b…再正式§6 header+全部§6–10实审abe199…（实际读§1定义依赖，不冒旧v3全文重审）；root各记录实际全文读。原v3前缀SHA df8d61b09dcdce43f7b76d50c8c981e80d91cdcce5a3a28b063e4cd317004a48保持。
- Counterevidence / Objections：same-dest两occurrence不提前合并，zero任务保留，pool d计q/J已用边非unused；严格/非严格threshold分开；原OPT1/指定False不同，unknownwitness非免费finder，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/final全文审查；implementation none，外审/全球新颖性未认证；主目标OPEN。
- Related Files：[正文](../current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md)、[审查](../reviews/unrelated_machines/bulk_or_commit_two_witness_interpolation_review.md)及逐SHA原件。


## UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1：单primary与PI onehot共享辅助的完整unit逃逸

- Objects / Domain / Definitions / Quantifiers：primeR≥2/完整norm1 tagged-LINE菜单；main只含全部primary，各helper恰一primary+任意共享aux，所有helper states onehot；fixed injective截距；primary uniform与primary-aux pair uniform；任意指定main state。
- Exact Statement / Conclusion：det-bit-poly从原states直接建conditioned-state matching图，不需取出存在的λ；完整真实helper选态/每组质量1/V1/全部原UM jobs实际OPT1。
- Assumptions / Dependencies：无复杂度假设；UM-MODEL-v1与本ID完整对象域，几何/有限域/匹配或计数自足；不以前另一ID定理、CONFIG或有限实验为前提。
- Scope：只单primary/all-state onehot/main不接aux及指定条件边际；不覆盖多primary/diffuse/额外groups/预载，不输出source全局赋值，不是general PI或主hardness结论。
- Evidence：general仅Exact独立全证f535…；root实际全文读后才放作者Proof2b4…，actual读后30a…；final shared one-primary header+§1–2 d7bb…实审；root全部实际读。realλ只证Hall、直接状态图可含λ0 states，无standing fatal。
- Counterevidence / Objections：多primary会改变条件化分布；同页simplex不在此域，所有zero与λ0 indexed states仍保留，realλ前提非未知实际witness，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/最终指定scope审；无软件/外审/全球新颖性认证；主目标OPEN。
- Related Files：[合并正文](../current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md)、[分域审查](../reviews/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_review.md)及逐SHA原件。


## UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1：公共simplex陪集且全部标签两两独立的精确趋二族

- Objects / Domain / Definitions / Quantifiers：oddprimeR≥3、K=F_R² extension、q=(R²+1)(R+1)个parts/同4D full-projective simplex C；每组全部R⁴ states，main与B(R−1) onehot helpers，完整freshzero padding/common q/common cosets/variable degree≤R。
- Exact Statement / Conclusion：uniform local全部pair独立，精确V=2/(R+1)、完整actual UM OPT=2−2/(R+1)、CSP value B/[1+B(R−1)]；显式达界对象，finite表O(R11 polylogR)/dense O(R19 polylogR)。
- Assumptions / Dependencies：无复杂度假设；UM-MODEL-v1与本ID完整对象域，几何/有限域/匹配或计数自足；不以前另一ID定理、CONFIG或有限实验为前提。
- Scope：易显式计算族，不给NP-hard promise/source任意NO decoder；q约R³/C随R非既有LST固定arity大R参数域；仅删唯一diffuse main即其余全部unit，不提供robust删除/dummy-budget困难性。
- Evidence：bicriteria仅Exact独立全证db3…；root全文实际读后才放作者Proof4278…，actual读后1add…；final simplex shared-header+§3–8 a06…实审，§1.3定义依赖实际读，不冒one-primary全审；root各记录全部实际读，无standing fatal。
- Counterevidence / Objections：所有states含ζ0均norm1；未选state额外exports不能减lower bound；fresh权0但labels真PI不能删后冒同C；R2不在域，单main脆弱且非hard image，无standing fatal。
- Status：限定证明完整，真实独立重构/作者读后/最终指定scope审；无软件/外审/全球新颖性认证；主目标OPEN。
- Related Files：[合并正文](../current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md)、[分域审查](../reviews/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_review.md)及逐SHA原件。


## UM-LOCAL-BUNDLE-SHIELD-PATH-v1：二分任务包的逐机屏蔽与入流剥离

- ID/version / Exact Statement / Quantifiers：任意有限m≥1的非负二进制有理迁移弧、固定底载f，逐机U_i≥S_i，h_i=(S_i+Q_i−U_i)_+。若每h_i>0源给出出弧包P_i，满足h_i≤U_i−S_i及包、补集源量均≥h_i，则确定性总位poly构造每弧一次的完整直接目标路径，全部前缀逐机≤U_i。任意源二分另给U_i=max(S_i+Q_i/2,F_i+max(a(P_i),A_i−a(P_i)))，自动满足这些前提；两箱LPT可有效生成二分，M_i≤max(a_i^max,2A_i/3)。
- Objects / Domain / Definitions：源/目标为不同机器；a,b,f≥0有理；S=f+A,F=f+Q。完整迁移弧及包是输入，等价给定具体目标，不从分数边际免费产生它们；空源包只使相关h=0。
- Assumptions / Scope / Conclusion：五阶段共同入流剥离、逆删除激活、补集释放核心；逐机预算profile不声称最优，没有一般调度近似或阈值不可行判据。
- Dependencies：UM-MODEL-v1；正文§2自足永久安全与加权入度剥离，§5自足两箱贪心估计。旧单件路径不是本上界的承重前提。
- Evidence：精确陈述先行独立重构，最终正文/代码后读攻击；证明及实际审查、有限回放由Related Files进入。逐机profile是数学构造，尚未提供软件接口。
- Counterevidence / Objections：零值LPT证明的“末件至少第三”措辞已改为不依赖编号的X≤(A+x)/2、x≤X/2证明。未发现声明范围内尚成立fatal。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified。软件仅实现下项统一预算合同。
- Related Files：research/current/unrelated_machines/bundle_inflow_peeling_and_pruned_transient_sharpness.md；research/reviews/unrelated_machines/bundle_inflow_peeling_review.md。

## UM-PRUNED-BUNDLE-PEELING-PATH-v1：任意剪枝初态的完整直接目标路径与分段锐界

- ID/version / Exact Statement / Quantifiers：任意UM-MODEL-v1的有理0≤T≤C≤2T、实际σ≤C、给定具体实际τ≤T，σ所用端均≤T，则det-bit-poly输出每件改变任务仅一次直迁τ的完整顺序，所有前缀≤U=max(2T,C+T/2)。对每有理T>0、T≤C≤2T，整个剪枝输入类到指定不同τ的最坏最小路径峰恰U；不是逐实例最优，也不声称ST输出达到下界。
- Objects / Domain / Definitions：m≥1,n≥0，非负二进制有理/∞、零端、单可用机器、大分母皆包括。f为不变任务负载，A/Q为源/目标改变负载；h=(S+Q−U)_+。h>0源取h≤a(P)≤T的包，补集≥h。
- Assumptions / Scope / Conclusion：去掉旧eligible单件与assigned-max前提；直接实际全程构造，不产生未知目标。无τ或剪枝合同失败不提供FAIL⇒OPT>T。
- Dependencies：UM-MODEL-v1；UM-LOCAL-BUNDLE-SHIELD-PATH-v1；锐下界沿UM-BOUNDED-BATCH-TRANSIENT-PEAK-SHARP-v1的两机k=1族。本次没有新下界机制。
- Evidence：正文§1–4完整证明、陈述先行与最终稿后置攻击；Fraction独立前缀重算、小minimax及OPT oracle、全小件核心/剥离/出口分支、退化与长分母、锐族均有实际代码及冻结结果。
- Counterevidence / Objections：实现初稿漏所选核心出口，现补phase0并由三机全小件fixture回归；原proof有该步骤。旧贪心安全步死锁仍成立，与全局次序定理不冲突。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; external review and novelty unverified。规范完整路径构造implemented；UM-TARGET-v1仍OPEN。
- Related Files：同上正文/审查；tests/audits/unrelated_machines/bundle_peeling_buffer_path.py；tests/audits/unrelated_machines/bundle_peeling_path_audit.py；evidence/runs/unrelated_machines/bundle_peeling_path_audit.json；history/source/notes/unrelated_machines/bundle_inflow_peeling_frozen_proof.md。

## UM-KNAPSACK-MATROID-EXPONENTIAL-v1：固定次二原地拟阵外包的超多项式数量

- Exact Statement / Objects / Domain / Quantifiers：对所有整数k≥3及1≤r≤floor((k−1)/2)，k件tiny各1/k、一件b大小1−r/k。任意q个同一原地基集的拟阵各包含全部重量≤1集合；若共同独立集重量均严格小于w0=2−2r/k，则q≥ceil[binom(k,r)/binom(k−r−1,r)]≥exp(r(r+1)/k)。最少数精确为C(k,k−r−1,r)。
- Assumptions / Definitions / Scope：逐拟阵完整保留本地可行集；所有共同独立集均安全；静态交，原输入显式权重表。覆盖数定义见正文§9。
- Conclusion：每个固定1≤B<2的全类外包需要超多项式于原始位长L=Θ(k log k)的拟阵数；不是exp(Ω(L))声明，也不是调度困难性。
- Dependencies：UM-MODEL-v1的本地非负容量定义；自足唯一回路分类、坏集覆盖与对数估计。UM-KNAPSACK-MATROID-ENVELOPE-v1仅作旧线性数量边界的对照，不改其身份。
- Evidence：完整一般证明；声明先行独立重构、作者稿及canonical§9实际读后审查；精确回路/端点审计及冻结记录。
- Counterevidence / Objections：严格阈值不能删；不保证坏集延伸为共同基或全局调度。共享辅助/存在性投影/多元素块/只保选定profile/自适应或一般有符号电路均不由本定理排除。
- Status：限定范围证明完成；实际内部独立攻击，未外审；全球新颖性与论文价值未认证。UM-TARGET-v1仍OPEN。
- Related Files：research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md §9；research/reviews/unrelated_machines/knapsack_matroid_exponential_review.md；tests/audits/unrelated_machines/knapsack_matroid_exponential.py；evidence/runs/unrelated_machines/knapsack_matroid_exponential_audit.json。


## UM-BOUNDED-CONFIG-CARDINALITY-SLOT-v1：有界配置任务数的统一槽包络余量

- Exact Statement / Quantifiers：For every integer K>=1 and explicit rational equal-coverage CONFIG(T) point whose positive-weight configurations have at most K positive jobs after zero-edge preprocessing, every standard ST slot envelope and covering matching has load <=(2-K^{-(K-1)})T for K>=2, <=T for K1. K2/K3 sharp envelope bounds are3T/2,11T/6.
- Objects / Domain / Definitions：UM-MODEL-v1；精确定义、零值预处理、输入证书和输出合同见对应正文，不把目录或推送视作数学升级。
- Assumptions / Scope：K is fixed only for the algorithmic enumeration; the supplied-point theorem holds for each K. Full source configuration cardinality, not total eligible row degree or just large-job count. No generic CONFIG oracle or uniform epsilon for growing K.
- Conclusion：有界配置任务数的统一槽包络余量，仅在上述量词和条件内；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1, UM-ST-ROUND-v1；正文中自足的类型/计数/构造步骤。
- Evidence：一般证明；实际声明先行独立重构及证明知情最终读稿分别记录；有限Fraction核验仅为checks。
- Counterevidence / Objections：K is fixed only for the algorithmic enumeration; the supplied-point theorem holds for each K. Full source configuration cardinality, not total eligible row degree or just large-job count. No generic CONFIG oracle or uniform epsilon for growing K.
- Status：限定范围证明完成、内部独立攻击、未外审；全球新颖性和独立论文价值未认证。
- Related Files：research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md；research/reviews/unrelated_machines/bounded_configuration_cardinality_review.md；对应assets与catalog登记给出实际代码/冻结结果。


## UM-BOUNDED-CARDINALITY-PROMISE-APPROX-v1：有界最优任务数承诺的未知阈值构造

- Exact Statement / Quantifiers：For each fixed K, on ordinary UM instances promised to have some OPT schedule with at most K no-zero-edge jobs per machine, explicit <=K subset enumeration, rational CONFIG LP and threshold-sum search give a deterministic bit-polynomial actual assignment at the stated K-dependent ratio.
- Objects / Domain / Definitions：UM-MODEL-v1；精确定义、零值预处理、输入证书和输出合同见对应正文，不把目录或推送视作数学升级。
- Assumptions / Scope：Polynomial degree depends on fixed K. Infeasibility only excludes schedules with the K-cardinality promise and is not unrestricted OPT>T. General LP solver not integrated in audit software.
- Conclusion：有界最优任务数承诺的未知阈值构造，仅在上述量词和条件内；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1, UM-BOUNDED-CONFIG-CARDINALITY-SLOT-v1；正文中自足的类型/计数/构造步骤。
- Evidence：一般证明；实际声明先行独立重构及证明知情最终读稿分别记录；有限Fraction核验仅为checks。
- Counterevidence / Objections：Polynomial degree depends on fixed K. Infeasibility only excludes schedules with the K-cardinality promise and is not unrestricted OPT>T. General LP solver not integrated in audit software.
- Status：限定范围证明完成、内部独立攻击、未外审；全球新颖性和独立论文价值未认证。
- Related Files：research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md；research/reviews/unrelated_machines/bounded_configuration_cardinality_review.md；对应assets与catalog登记给出实际代码/冻结结果。


## UM-WEIGHTED-EXCESS-ZERO-DEFECT-TRAP-v1：加权余量消元的零缺陷满秩坏核心

- Exact Statement / Quantifiers：For every fixed rational eps in(0,1), integer m>=3,m>1/eps, an explicit 2m-machine,2m+1-job instance has OPT1 and a true-optimal-hull initial x. Exactly m legal maximal weighted-excess nullspace pivots preserve all protected row loads and reach a full-column-rank core with D0 but every frozen-assignment completion2-1/m>2-eps.
- Objects / Domain / Definitions：UM-MODEL-v1；精确定义、零值预处理、输入证书和输出合同见对应正文，不把目录或推送视作数学升级。
- Assumptions / Scope：One specified harmful direction history only. It violates the row big-count inequality immediately; no claim under maintaining full CONFIG, no failure of all direction choices or general approximation lower bound.
- Conclusion：加权余量消元的零缺陷满秩坏核心，仅在上述量词和条件内；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1；正文中自足的类型/计数/构造步骤。
- Evidence：一般证明；实际声明先行独立重构及证明知情最终读稿分别记录；有限Fraction核验仅为checks。
- Counterevidence / Objections：One specified harmful direction history only. It violates the row big-count inequality immediately; no claim under maintaining full CONFIG, no failure of all direction choices or general approximation lower bound.
- Status：限定范围证明完成、内部独立攻击、未外审；全球新颖性和独立论文价值未认证。
- Related Files：research/current/unrelated_machines/configuration_preserving_elimination_support_loss.md；research/reviews/unrelated_machines/configuration_elimination_support_loss_review.md；对应assets与catalog登记给出实际代码/冻结结果。


## UM-CONFIG-PRESERVING-ACTIVATION-SUPPORT-LOSS-v1：完整配置路径的一步激活支撑丢失

- Exact Statement / Quantifiers：Given explicit rational CONFIG1 witness on m>=2,n>=1, a polynomial-size activation lift has OPT1 and explicit true-optimal-hull initial x. One maximal legal row-load nullspace pivot preserves full CONFIG1 along the whole segment but deletes all original private alternatives; endpoint frozen-support optimum equals max(1,OPT(P positive marginal support)). The known CONFIG gap family gives any fixed sub-two bad history.
- Objects / Domain / Definitions：UM-MODEL-v1；精确定义、零值预处理、输入证书和输出合同见对应正文，不把目录或推送视作数学升级。
- Assumptions / Scope：Explicit y is part of input, not a free CONFIG oracle. No endpoint-rank or zero-D claim. Reverse or another direction and support reopening are not excluded; the full constructed instance is easy via its supplied optimal atoms.
- Conclusion：完整配置路径的一步激活支撑丢失，仅在上述量词和条件内；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1, UM-CONF-GAP-v1；正文中自足的类型/计数/构造步骤。
- Evidence：一般证明；实际声明先行独立重构及证明知情最终读稿分别记录；有限Fraction核验仅为checks。
- Counterevidence / Objections：Explicit y is part of input, not a free CONFIG oracle. No endpoint-rank or zero-D claim. Reverse or another direction and support reopening are not excluded; the full constructed instance is easy via its supplied optimal atoms.
- Status：限定范围证明完成、内部独立攻击、未外审；全球新颖性和独立论文价值未认证。
- Related Files：research/current/unrelated_machines/configuration_preserving_elimination_support_loss.md；research/reviews/unrelated_machines/configuration_elimination_support_loss_review.md；对应assets与catalog登记给出实际代码/冻结结果。


## UM-CONFIG-PRESERVING-TWO-SIGN-SUPPORT-LOSS-v1：保配置同一方向的双符号坏端点

- Exact Statement / Quantifiers：For the explicit bipartite <=2-core-end CONFIG source domain, half-color activation has polynomially many genuine OPT1 atoms. Two disjoint lifts admit one allowed nullspace direction with exact maximal steps +/-1/2, full CONFIG1 throughout, and both endpoint frozen-support optima max(1,OPT(P positive marginal support)). Initial rank J+P and nullity2|E+|+2m-P are exact.
- Objects / Domain / Definitions：UM-MODEL-v1；精确定义、零值预处理、输入证书和输出合同见对应正文，不把目录或推送视作数学升级。
- Assumptions / Scope：The direction is a direct sum, not support-minimal/circuit. Refutes arbitrary direction plus both-sign endpoint checking only; different directions, circuit rules, preserved common atoms or reopened edges remain open.
- Conclusion：保配置同一方向的双符号坏端点，仅在上述量词和条件内；UM-TARGET-v1仍OPEN。
- Dependencies：UM-MODEL-v1, UM-CONFIG-PRESERVING-ACTIVATION-SUPPORT-LOSS-v1, UM-CONF-GAP-v1；正文中自足的类型/计数/构造步骤。
- Evidence：一般证明；实际声明先行独立重构及证明知情最终读稿分别记录；有限Fraction核验仅为checks。
- Counterevidence / Objections：The direction is a direct sum, not support-minimal/circuit. Refutes arbitrary direction plus both-sign endpoint checking only; different directions, circuit rules, preserved common atoms or reopened edges remain open.
- Status：限定范围证明完成、内部独立攻击、未外审；全球新颖性和独立论文价值未认证。
- Related Files：research/current/unrelated_machines/configuration_preserving_elimination_support_loss.md；research/reviews/unrelated_machines/configuration_elimination_support_loss_review.md；对应assets与catalog登记给出实际代码/冻结结果。

## UM-OCCURRENCE-WEIGHTED-DIRECT-LITERAL-POOL-BUDGET-ESCAPE-v1：出现位置异权文字池的完整三半逃逸

- Objects / Domain / Definitions / Quantifiers：显式CNF每clause至少2个不同身份occurrences，允许重复literal/variable；per-occurrence b≥0为binary rational，每变量每polarity全部eligible b和≤1；仅完整private-root/query/clause-selector/两pool unit-f原矩阵，含zero/unused/empty-idle。
- Exact Statement / Conclusion：det-bit-poly无SAT/witness输入地为所有原jobs构造actual≤3/2；每clause恰一个原query导出，其余原root；含f池query-only≤1/2、另一池≤1、全部roots≤1。
- Assumptions / Dependencies：无复杂度假设；UM-MODEL-v1及本页完整域，标准整数匹配/排序自足。
- Scope：仅独立private-root/full-sign预算≤1编译；不排更大预算、额外资格或shared guards，不给主UM新ratio/near2hardness，不承诺sharpness。
- Evidence：typed作为candidate作者/熟悉标准工具者仅新Exact独立重构5aa…后root实际全文读才放作者Proof d882…，actual读后24cd…；新6.1sol reviewer另仅Exact独立全证c759…，root全文实读后解封同一已冻Proof，actual读后778…，最终header+全部§1–5实审601…；root全部实际读，不记blind。
- Counterevidence / Objections：预算是full eligible而非selected；unit/empty clause不在域；zero原job仍执行，未选root保留，旧cohabiting域认证/锐性不转移，无standing fatal。
- Status：证明完整，实际独立重构/读后/最终全文审；implementation none、外审与全球新颖性未认证；UM-TARGET-v1 OPEN。
- Related Files：[正文](../current/unrelated_machines/occurrence_weighted_direct_literal_pool_budget_escape.md)、[审查](../reviews/unrelated_machines/occurrence_weighted_direct_literal_pool_budget_escape_review.md)与原件。

## UM-HOME-UNIT-CYCLE-ELIMINATION-v1：任意负载下单home单位外端的逐机消环

- Exact Statement / Objects / Domain / Quantifiers：每H任务有指定home a∈[0,1]、其余有限端均1；U全unit；任意给定实际σ。反复取消简单有向转移环，至多|H|轮得完整σ′，保U位置、每H保原端或回home、外送DAG且∀i L_i(σ′)≤L_i(σ)。C<2时所得外送图为森林。
- Assumptions / Definitions / Scope：无home行预算限制；不要求原支持DAG；完整批次比较，不声明单件安全迁移。 全部对象、阈值及退化分支见[自足正文](../current/unrelated_machines/home_unit_cycle_elimination_and_directed_token_bridge.md)。
- Conclusion：严格限于上述合同；UM-TARGET-v1保持OPEN。
- Dependencies：UM-MODEL-v1；标准有限组合、有理数精确运算及正文逐条推导。不调用未知最优分配或免费共同选择oracle。
- Evidence：自足一般证明；已发生的陈述先行/读后攻击及两路精确回放见[实际审查](../reviews/unrelated_machines/home_unit_cycle_and_directed_token_review.md)；有限输出单独冻结。
- Counterevidence / Objections：已排除的越界推广及其反例见正文；无standing fatal限于当前版本。有限搜索不提升一般真值。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。Truth、实现、外审、新颖性与主目标分别管理。
- Related Files：正文、实际审查、tests/audits/unrelated_machines/home_unit_cycle_and_directed_token.py, tests/audits/unrelated_machines/home_unit_cycle_independent.py、evidence/runs/unrelated_machines/home_unit_cycle_and_directed_token_audit.json。

## UM-HOME-UNIT-ROOTED-FOREST-v1：小于二调度的保unit占位根森林

- Exact Statement / Objects / Domain / Quantifiers：同一home/unit模型，给实际σ、Cmax(σ)≤C<2。W为从U实际占位机沿实际外送弧可达集。保W发出弧，其他H回home，得完整τ：W上负载精确保原σ，外部负载精确home预算b_i；W上恰|U|棵互不交根树。若∀i∉W,b_i≤C，则Cmax(τ)≤C。
- Assumptions / Definitions / Scope：只使用给定实际调度；外部逐机不增不成立；阈值C=2的同容量森林推广有反例。 全部对象、阈值及退化分支见[自足正文](../current/unrelated_machines/home_unit_cycle_elimination_and_directed_token_bridge.md)。
- Conclusion：严格限于上述合同；UM-TARGET-v1保持OPEN。
- Dependencies：UM-MODEL-v1；标准有限组合、有理数精确运算及正文逐条推导。不调用未知最优分配或免费共同选择oracle。
- Evidence：自足一般证明；已发生的陈述先行/读后攻击及两路精确回放见[实际审查](../reviews/unrelated_machines/home_unit_cycle_and_directed_token_review.md)；有限输出单独冻结。
- Counterevidence / Objections：已排除的越界推广及其反例见正文；无standing fatal限于当前版本。有限搜索不提升一般真值。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。Truth、实现、外审、新颖性与主目标分别管理。
- Related Files：正文、实际审查、tests/audits/unrelated_machines/home_unit_cycle_and_directed_token.py, tests/audits/unrelated_machines/home_unit_cycle_independent.py、evidence/runs/unrelated_machines/home_unit_cycle_and_directed_token_audit.json。

## UM-DIRECTED-DEGREE-TOKEN-IDENTITY-v1：任意简单有向需求图的压缩任务值恒等式

- Exact Statement / Objects / Domain / Quantifiers：任意显式有限非空简单无自环有向图D、根r及二进制需求k≥0，k_v=0⇒outdegree0。b*为真实向外根树的截断最小度需比最优值。原token/filler构造P(D,k)仍满足OPT=2−b*；实际C<2调度可位poly解码b≥2−C根树，给树可位poly构全部任务≤2−b调度。
- Assumptions / Definitions / Scope：允许环境环、输入根入边、不可达环和巨大需求；不把旧DAG v1静默扩域；无未知树选择算法。 全部对象、阈值及退化分支见[自足正文](../current/unrelated_machines/home_unit_cycle_elimination_and_directed_token_bridge.md)。
- Conclusion：严格限于上述合同；UM-TARGET-v1保持OPEN。
- Dependencies：UM-MODEL-v1, UM-HOME-UNIT-ROOTED-FOREST-v1；标准有限组合、有理数精确运算及正文逐条推导。不调用未知最优分配或免费共同选择oracle。
- Evidence：自足一般证明；已发生的陈述先行/读后攻击及两路精确回放见[实际审查](../reviews/unrelated_machines/home_unit_cycle_and_directed_token_review.md)；有限输出单独冻结。
- Counterevidence / Objections：已排除的越界推广及其反例见正文；无standing fatal限于当前版本。有限搜索不提升一般真值。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。Truth、实现、外审、新颖性与主目标分别管理。
- Related Files：正文、实际审查、tests/audits/unrelated_machines/home_unit_cycle_and_directed_token.py, tests/audits/unrelated_machines/home_unit_cycle_independent.py、evidence/runs/unrelated_machines/home_unit_cycle_and_directed_token_audit.json。

## UM-SC-BLOCK-TYPE-PROFILE-RECONSTRUCTION-v1：单阈值Santa Claus的分块计数多项式配置

- Exact Statement / Objects / Domain / Quantifiers：固定任意有理ε>0，对任意显式非负有理m×n估值、m≥1,n≥0，可确定性位poly生成舍下v′≤v、Oε(log(n+1))正类型与每player显式poly count profiles。对每个原值≥1实际子集A都有A′⊆A完整match某profile且v′(A′)≥1/(1+ε)；因此不交YES见证仍保留。
- Assumptions / Definitions / Scope：只生成类型列表，不求共同选择；ε固定；n0输出空菜单；替代自足证明已知BLMRS单阈值合同，非原文逐字机制。 全部对象、阈值及退化分支见[自足正文](../current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md)。
- Conclusion：严格限于上述合同；UM-TARGET-v1保持OPEN。
- Dependencies：UM-MODEL-v1；标准有限组合、有理数精确运算及正文逐条推导。不调用未知最优分配或免费共同选择oracle。
- Evidence：自足一般证明；已发生的陈述先行/读后攻击及两路精确回放见[实际审查](../reviews/unrelated_machines/type_profile_compression_and_rank_bridge_review.md)；有限输出单独冻结。
- Counterevidence / Objections：已排除的越界推广及其反例见正文；无standing fatal限于当前版本。有限搜索不提升一般真值。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。Truth、实现、外审、新颖性与主目标分别管理。
- Related Files：正文、实际审查、tests/audits/unrelated_machines/santa_block_type_profiles.py, tests/audits/unrelated_machines/type_matching_rank_bridge.py、evidence/runs/unrelated_machines/type_profile_compression_and_rank_bridge_audit.json。

## UM-NORMALIZED-TYPE-MATCHING-RANK-VALUE-IDENTITY-v1：归一化partition-rank菜单的精确调度值

- Exact Statement / Objects / Domain / Quantifiers：任意显式非空player/resource集合、非空indexed正总值类型profiles、每profile≤n件，f_ic(B)=Σ_v(v/Wc)min(c(v),|B∩E_iv|)，F_i=max_c f_ic，V=max不交B_i min_iF_i。selector/token普通UM构造满足OPT=2−V；给bundles输出全部任务峰恰2−minF，给任意调度C输出每F_i≥max(0,2−C)的实际不交bundles。
- Assumptions / Definitions / Scope：含V0、重复profile、全部未选jobs及空菜单另外固定OPT2分支；max-profile一般非次模有四资源反例；不提供全局常数finder或新困难性源。 全部对象、阈值及退化分支见[自足正文](../current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md)。
- Conclusion：严格限于上述合同；UM-TARGET-v1保持OPEN。
- Dependencies：UM-MODEL-v1；标准有限组合、有理数精确运算及正文逐条推导。不调用未知最优分配或免费共同选择oracle。
- Evidence：自足一般证明；已发生的陈述先行/读后攻击及两路精确回放见[实际审查](../reviews/unrelated_machines/type_profile_compression_and_rank_bridge_review.md)；有限输出单独冻结。
- Counterevidence / Objections：已排除的越界推广及其反例见正文；无standing fatal限于当前版本。有限搜索不提升一般真值。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。Truth、实现、外审、新颖性与主目标分别管理。
- Related Files：正文、实际审查、tests/audits/unrelated_machines/santa_block_type_profiles.py, tests/audits/unrelated_machines/type_matching_rank_bridge.py、evidence/runs/unrelated_machines/type_profile_compression_and_rank_bridge_audit.json。

## UM-DIVISIBLE-TWO-SIZE-NEUTRAL-REPAIR-v1：整比双尺寸任意初态的防循环中性精确修复

- Exact Statement / Objects / Domain / Quantifiers：全资格同机m≥1、k件Qδ宏及N件δ tiny，Q≥1二进制整数、δ>0有理。任意初态可确定性位poly用≤floor(k²/2)宏批次及≤N单tiny步达OPT=δmax(Qceil(k/m),ceil((kQ+N)/m))；各批次新负载被旧majorize，组成势Σu_i²控制中性步不循环。
- Assumptions / Definitions / Scope：只限整比、完全同机和全资格；批次支持可随tiny数增长；不保证批内逐件同峰值，不解决一般UM。 全部对象、阈值及退化分支见[自足正文](../current/unrelated_machines/divisible_two_size_neutral_repair.md)。
- Conclusion：严格限于上述合同；UM-TARGET-v1保持OPEN。
- Dependencies：UM-MODEL-v1；标准有限组合、有理数精确运算及正文逐条推导。不调用未知最优分配或免费共同选择oracle。
- Evidence：自足一般证明；已发生的陈述先行/读后攻击及两路精确回放见[实际审查](../reviews/unrelated_machines/divisible_two_size_neutral_repair_review.md)；有限输出单独冻结。
- Counterevidence / Objections：已排除的越界推广及其反例见正文；无standing fatal限于当前版本。有限搜索不提升一般真值。
- Status：complete stated-scope proof; independently reconstructed and exactly audited; unrefereed; novelty unverified。Truth、实现、外审、新颖性与主目标分别管理。
- Related Files：正文、实际审查、tests/audits/unrelated_machines/divisible_two_size_neutral_repair.py, tests/audits/unrelated_machines/divisible_two_size_neutral_independent.py、evidence/runs/unrelated_machines/divisible_two_size_neutral_repair_audit.json。


## UM-FRACTIONAL-BENCHMARK-REMATCHING-v1：分数benchmark的真实H匹配

- Objects / Domain / Definitions / Quantifiers：n>=1有限单调次可加有理valuations；n个不同真实H、B=U\H、Vi>=0、inactive vi(B)=0、c>=1；对每个feasible fractional residual family总normalized utility<=cn，正finite配置benchmark行一列<=一。
- Exact Statement / Conclusion：不输入benchmark、不验证全局前提，仅真最大product匹配det-bit-poly给GM(Vi+singleton)>=每个正fractional benchmark/(c+1)。
- Assumptions：无复杂度假设；C的P=NP仅条件于另有明确promise-gap Karp reduction；E方法限制另用既有CONFIG gap。
- Dependencies：UM-FRACTIONAL-REMATCHING-SEMANTIC-DOMAIN-v1；页内完整定义、标准有理LP/匹配/路径分解。具体范围见正文。
- Scope：不适用weighted或oracle-only/general-SA后端；不提供all-group maxmin或general UM算法/困难性。normalized高端NO需以1−gamma_hi比较低质量计数；旧未覆盖判断撤回；未构造NP-hard源，算法数学规格未实现。
- Evidence：实际独立Exact-first、完整或明确模块作者读后及最终canonical全文审查；root实际读完相关记录，完整顺序/哈希见review。
- Counterevidence / Objections：旧generic-SA数值反驳保留，不回填旧v4完整作者Proof；当前v5任意显式XOS域另审。C–D精确低端定理保留；旧§F把gamma_hi/gamma_lo混用的解读已撤回，互补推论另ID；不把旧审查追认为已发现。
- Status：complete scoped deterministic fractional-XOS proof; actual Exact-first, author-read-after and whole canonical review; implementation none; novelty unverified；外审未记录；UM-TARGET-v1 OPEN。
- Related Files：[正文](../current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md)、[实际审查](../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md)与冻结原件。


## UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1：显式XOS的确定性分数NSW

- Objects / Domain / Definitions / Quantifiers：n>=1、m>=0，非空有限显式indexed XOS clauses，全部非负binary rational，允许zero/重复/未用，无global grid或normalization/utility floor，仅unweighted。
- Exact Statement / Conclusion：从任意显式原XOS表det-bit-poly输出真实不交allocation，对全部正finite fractional log-CONFIG benchmark同时NSW>=benchmark/1125000；无正singleton matching时actual optimum零。
- Assumptions：无复杂度假设；C的P=NP仅条件于另有明确promise-gap Karp reduction；E方法限制另用既有CONFIG gap。
- Dependencies：UM-FRACTIONAL-BENCHMARK-REMATCHING-v1, UM-EXPLICIT-BINARY-RATIONAL-XOS-DOMAIN-v1；页内完整定义、标准有理LP/匹配/路径分解。具体范围见正文。
- Scope：不适用weighted或oracle-only/general-SA后端；不提供all-group maxmin或general UM算法/困难性。normalized高端NO需以1−gamma_hi比较低质量计数；旧未覆盖判断撤回；未构造NP-hard源，算法数学规格未实现。
- Evidence：实际独立Exact-first、完整或明确模块作者读后及最终canonical全文审查；root实际读完相关记录，完整顺序/哈希见review。
- Counterevidence / Objections：旧generic-SA数值反驳保留，不回填旧v4完整作者Proof；当前v5任意显式XOS域另审。C–D精确低端定理保留；旧§F把gamma_hi/gamma_lo混用的解读已撤回，互补推论另ID；不把旧审查追认为已发现。
- Status：complete scoped deterministic fractional-XOS proof; actual Exact-first, author-read-after and whole canonical review; implementation none; novelty unverified；外审未记录；UM-TARGET-v1 OPEN。
- Related Files：[正文](../current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md)、[实际审查](../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md)与冻结原件。


## UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1：归一化菜单几乎所有组与同组修复LP边界

- Objects / Domain / Definitions / Quantifiers：原每state总量1、positive-support FSLP及明确同组singleton REPAIR；fixed eta/gamma/a/delta_q量词同正文。
- Exact Statement / Conclusion：原total-one FSLP可行给det实际NSW>=1/3000000；rho2^24、Kceil1/eta、q=rho^-K、c=q/2，少于eta*n组quality<q或<=c。同组D singleton REPAIR、D<=a*n、eta<gamma-a且delta_q<=c的promise由显式LP分离。原ordinary全jobs load<=2仅selected-root例外计数；§F旧高/低gamma比较已撤回；新高端互补推论另ID登记。
- Assumptions：无复杂度假设；C的P=NP仅条件于另有明确promise-gap Karp reduction；E方法限制另用既有CONFIG gap。
- Dependencies：UM-FRACTIONAL-BENCHMARK-REMATCHING-v1, UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1, UM-NORMALIZED-MENU-POSITIVE-SUPPORT-CERTIFICATE-DOMAIN-v1, UM-FLAT-MENU-EXACT-STATE-MASS-ONE；页内完整定义、标准有理LP/匹配/路径分解。具体范围见正文。
- Scope：不适用weighted或oracle-only/general-SA后端；不提供all-group maxmin或general UM算法/困难性。normalized高端NO需以1−gamma_hi比较低质量计数；旧未覆盖判断撤回；未构造NP-hard源，算法数学规格未实现。
- Evidence：实际独立Exact-first、完整或明确模块作者读后及最终canonical全文审查；root实际读完相关记录，完整顺序/哈希见review。
- Counterevidence / Objections：旧generic-SA数值反驳保留，不回填旧v4完整作者Proof；当前v5任意显式XOS域另审。C–D精确低端定理保留；旧§F把gamma_hi/gamma_lo混用的解读已撤回，互补推论另ID；不把旧审查追认为已发现。
- Status：complete scoped deterministic fractional-XOS proof; actual Exact-first, author-read-after and whole canonical review; implementation none; novelty unverified；外审未记录；UM-TARGET-v1 OPEN。
- Related Files：[正文](../current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md)、[实际审查](../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md)与冻结原件。


## UM-SHARED-LOAD-HISTOGRAM-CONFIG-PROJECTION-v1：弱共享负载递推等于配置投影

- Objects / Domain / Definitions / Quantifiers：m>=1,n>=0,K>=0整数；a_ij在0..K或infinity，可含无有限端任务；每步非负branch各行同质量theta、和一、aggregate在previous弱Hhat、own bad-load mass零；不要求branch perspective membership。
- Exact Statement / Conclusion：对每个前缀弱Hhat_j恰等于CONFIG_j(K)完整负载直方图投影；显式LP规模O(m(j+1)(K+1)+|E_[j]|(K+1))、目标另计位长。固定delta downround提供bit-poly可靠NO，非实际finder。
- Assumptions：无复杂度假设；C的P=NP仅条件于另有明确promise-gap Karp reduction；E方法限制另用既有CONFIG gap。
- Dependencies：UM-INTEGER-WEAK-SHARED-HISTOGRAM-RECURSION-DOMAIN-v1；页内完整定义、标准有理LP/匹配/路径分解。具体范围见正文。
- Scope：只否aggregate-only弱递推相对原CONFIG阈值的合同；不是相对OPT的算法下界。数值K伪多项式，downround可行不解码actual；不采用PHP/rank或假设真共同hull有poly oracle。
- Evidence：实际独立Exact-first、完整或明确模块作者读后及最终canonical全文审查；root实际读完相关记录，完整顺序/哈希见review。
- Counterevidence / Objections：旧full作者Proof将previous weak误写true-H，原字节与勘误保留；v2/当前修复。有限4机例不作一般证明；无standing fatal对当前合同。
- Status：complete scoped weak-histogram equals CONFIG projection; actual Exact-first, corrected author-read-after and whole canonical review; implementation none; novelty unverified；外审未记录；UM-TARGET-v1 OPEN。
- Related Files：[正文](../current/unrelated_machines/shared_load_histogram_recursion_equals_configuration_projection.md)、[实际审查](../reviews/unrelated_machines/shared_load_histogram_recursion_equals_configuration_projection_review.md)与冻结原件。


## UM-THRESHOLD-LEAF-HALL-CONSISTENT-MARGINALS-PATH-PROJECTION-GAP-v1：阈值叶、共同边际与精确路径投影

- Objects / Domain / Quantifiers / Definitions：显式normalized-flat，非空group/menu、非负binary rational每state质量1，可含零/重复/unused；0<epsilon<=1。投影指定全部旧组为C、仅新增D_+路径组为L；自动版另要求原组皆非threshold-UD；D_+只列positive邻居、保全部zero jobs。 对所有该域Q/epsilon、全部supplied basic点及每个整数t>=2。
- Exact Statement / Conclusion：全实际epsilon解必给R_cons必要有理LP；同一旧lambda,z的R_cons/R_leaf D_+投影都恰basic；每t>=2 diffuse Q_t在unit阈值两合同及FSLP可行而V=1/t、完整ordinary OPT=2-1/t。弱单matching与MC混合区分，转换确定性总位poly。
- Assumptions：无复杂度假设；标准有理LP/二部matching/有限运输，不用exact SDP或未知oracle。
- Dependencies：UM-MODEL-v1, UM-THRESHOLD-LEAF-HALL-DESIGNATED-PARTITION-DOMAIN-v1, UM-NORMALIZED-MENU-POSITIVE-SUPPORT-CERTIFICATE-DOMAIN-v1, UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1, UM-NORMALIZED-MENU-FULL-SUPPORT-LP-PRESERVATION-v3；BCG2009相邻路径思想，页内自足运输/完整gap证明。
- Scope：仅排所定义叶流relaxation相对unit证书的统一正质量提取，不排actual-OPT近似、actual-YES finder、joint-core/PSD、共同完整law或一般hardness；不是所有core系数微小，不认证global novelty。
- Evidence：新Exact-first、实际作者读后、最终338行独立实读；root实际读取记录与两套完整code并重放。
- Counterevidence / Objections：自动partition前提不可省；MC不保共同完整law；弱单matching不能升级；positive degree不含zero eligibility。无standing fatal对当前域。
- Status：complete scoped projection and sharp unit-threshold gap; independent reconstruction and actual final whole-text review; audit only; novelty unverified；UM-TARGET-v1及反面均OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md)、[新审查](../reviews/unrelated_machines/threshold_leaf_hall_consistent_marginals_path_projection_review.md)、所列代码/冻结原件。


## UM-NORMALIZED-ROBUST-HIGH-LOW-COMPLEMENT-v1：鲁棒高低比例互补纠错

- Objects / Domain / Quantifiers / Definitions：同一个非空原group集合、原norm1显式非负binary-rational indexed菜单、positive-support unit-FSLP；eta固定在(0,1]，delta_q/高端计数严格号按正文。不是一般非归一化或隐式菜单。
- Exact Statement / Conclusion：原norm1显式菜单unit-FSLP可行；固定eta，q_eta=(2^24)^(-ceil(1/eta))，0<delta_q<=q_eta及0<=gamma_hi<=1−eta时，C的同一实际allocation有计数 #{g:quality_g>=delta_q}>gamma_hi*n。因此all-allocation高端robust NO不可能；其互补低端比例是1−gamma_hi。
- Assumptions：无复杂度假设；依赖原C的实际输出和精确集合互补。
- Dependencies：UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1 与原norm1/positive-support域；不重证A/B。
- Scope：只修旧§F解释并给C直接推论；A/B与C–D原精确低端定理未被此反驳。无全组maxmin、一般UM次二算法/困难性或未来gated构造认证。
- Evidence：旧2365正文/header/F与新bfd9 header/C–F/全diff实际读后，冻结fc0f04记录，root实际全文读取。
- Counterevidence / Objections：旧§F未覆盖判断有实质错误，已撤回；严格/弱边界不能无条件互换；旧审查漏检事实保留。
- Status：complete elementary complement corollary; actual targeted correction review; old erroneous interpretation explicitly withdrawn; novelty not claimed；主目标OPEN。
- Related Files：[正文F](../current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md)、[实际纠错审查](../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md)。


## UM-NORMALIZED-GATED-MENU-VALUE-v1：归一化门控菜单与真实平衡值

- Objects / Domain / Definitions / Quantifiers：n>=1,m>=1；非空indexed states，distinct资源、非负binary rational系数每state总量1；pin/connector/gate/selector/全部incidence与零job恰按正文§1。 全部输入与所有参数按正文精确量词。
- Exact Statement / Conclusion：所有上述输入OPT(P_gate)=2−beta*；任意完整C<2解码不交原bundles，反向保全部jobs含零/未选states；双向det-bit-poly。
- Assumptions：结构结果无复杂度假设；排NP归约的结论以其实际P≠NP或随机归约假设为条件。
- Dependencies：UM-NORMALIZED-GATED-MENU-EXPLICIT-DOMAIN-v1, UM-MODEL-v1；正文自足内部推导及明确标准工具。
- Scope：仅完整显式norm1菜单和新gated普通矩阵；旧flat全组selector、多层/共享内部/非归一化/隐式表未覆盖。福利机制为DNS既有工具，13/8不称锐或新颖；generic rational LP仅数学规格，软件finite audit only。
- Evidence：Exact-first独立重构、实际完整作者读后和最终正文实读；源与新颖性分开。有限审计见review，不作一般证明。
- Counterevidence / Objections：旧NSW高低gamma解释错误已撤回，原A/B和C–D定理保留；近完美作者与独立审者身份互换并如实记录。
- Status：complete scoped proof; independently reconstructed and actually reviewed; external review unrecorded；外审及全球新颖性未认证；UM-TARGET-v1与其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md)、[实际审查](../reviews/unrelated_machines/normalized_gated_menu_welfare_review.md)及其来源/输入/代码/冻结结果。


## UM-NORMALIZED-GATED-MENU-WELFARE-APPROX-v1：归一化加权门控类的未知最优值十三八近似

- Objects / Domain / Definitions / Quantifiers：n>=1,m>=1；非空indexed states，distinct资源、非负binary rational系数每state总量1；pin/connector/gate/selector/全部incidence与零job恰按正文§1。 全部输入与所有参数按正文精确量词。
- Exact Statement / Conclusion：整个明确norm1 gated类有det-bit-poly真实13/8近似，无FSLP前提/未知OPT输入。联合使用明确福利LP x<=z、标准最大系数舍入的精确CDF确定性化、真实排序平衡与所有jobs映射；不是generalUM。
- Assumptions：结构结果无复杂度假设；排NP归约的结论以其实际P≠NP或随机归约假设为条件。
- Dependencies：UM-NORMALIZED-GATED-MENU-EXPLICIT-DOMAIN-v1, UM-NORMALIZED-GATED-MENU-VALUE-v1；正文自足内部推导及明确标准工具。
- Scope：仅完整显式norm1菜单和新gated普通矩阵；旧flat全组selector、多层/共享内部/非归一化/隐式表未覆盖。福利机制为DNS既有工具，13/8不称锐或新颖；generic rational LP仅数学规格，软件finite audit only。
- Evidence：Exact-first独立重构、实际完整作者读后和最终正文实读；源与新颖性分开。有限审计见review，不作一般证明。
- Counterevidence / Objections：旧NSW高低gamma解释错误已撤回，原A/B和C–D定理保留；近完美作者与独立审者身份互换并如实记录。
- Status：complete scoped proof; independently reconstructed and actually reviewed; external review unrecorded；外审及全球新颖性未认证；UM-TARGET-v1与其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md)、[实际审查](../reviews/unrelated_machines/normalized_gated_menu_welfare_review.md)及其来源/输入/代码/冻结结果。


## UM-NORMALIZED-ROBUST-PARTIAL-SOURCE-LP-BARRIER-v1：归一化部分束源的互补纠错与近完美LP判别

- Objects / Domain / Definitions / Quantifiers：n>=1,m>=1；非空indexed states，distinct资源、非负binary rational系数每state总量1；pin/connector/gate/selector/全部incidence与零job恰按正文§1。 全部输入与所有参数按正文精确量词。
- Exact Statement / Conclusion：high>=delta少于gamma_hi*n对应low<delta多于(1−gamma_hi)n；完整YES由positive-support FSLP在gamma_hi<=(5/8−delta)/(1−delta)判；近完美YES由福利LP在(5/8)(1−eta)>=gamma_hi+(1−gamma_hi)delta判，分别同样覆盖high>delta版本及等号；含gamma_hi<=delta<=3/8,eta<=1/40。
- Assumptions：结构结果无复杂度假设；排NP归约的结论以其实际P≠NP或随机归约假设为条件。
- Dependencies：UM-NORMALIZED-GATED-MENU-EXPLICIT-DOMAIN-v1；正文自足内部推导及明确标准工具。
- Scope：仅完整显式norm1菜单和新gated普通矩阵；旧flat全组selector、多层/共享内部/非归一化/隐式表未覆盖。福利机制为DNS既有工具，13/8不称锐或新颖；generic rational LP仅数学规格，软件finite audit only。
- Evidence：Exact-first独立重构、实际完整作者读后和最终正文实读；源与新颖性分开。有限审计见review，不作一般证明。
- Counterevidence / Objections：旧NSW高低gamma解释错误已撤回，原A/B和C–D定理保留；近完美作者与独立审者身份互换并如实记录。
- Status：complete scoped proof; independently reconstructed and actually reviewed; external review unrecorded；外审及全球新颖性未认证；UM-TARGET-v1与其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md)、[实际审查](../reviews/unrelated_machines/normalized_gated_menu_welfare_review.md)及其来源/输入/代码/冻结结果。


## UM-ACTUAL-KRONECKER-NO-TO-YES-v1：完整实际矩阵平方与全偶次幂的反放大

- Objects / Domain / Definitions / Quantifiers：m>=1,n>=0，合法非负有理有限边/∞；全部机器对/任务对保留，有限资格笛卡尔积，时间非负乘积；不剪枝。 全部输入与所有参数按正文精确量词。
- Exact Statement / Conclusion：显式8机10job seed真实OPT3/2，完整square64机100job400有限边可全机load1；所有完整偶次幂OPT1。含全部mixed jobs，关闭该通用平方保NO合同；不宣称首次发现现象或hard source。
- Assumptions：结构结果无复杂度假设；排NP归约的结论以其实际P≠NP或随机归约假设为条件。
- Dependencies：UM-ACTUAL-NONNEGATIVE-KRONECKER-DOMAIN-v1；正文自足内部推导及明确标准工具。
- Scope：只给本seed全矩阵反例与指定未剪枝LP恒等式；无NP源，不排特定hard image或物理一致性产品，不是UM主反证。
- Evidence：Exact-first独立重构、实际完整作者读后和最终正文实读；源与新颖性分开。有限审计见review，不作一般证明。
- Counterevidence / Objections：旧checker负编号/额外row语义缺口已修；v3严格finite记录另审，不把旧版本追认为已拒。先前boss7同现象报告保归属。
- Status：complete scoped proof; independently reconstructed and actually reviewed; external review unrecorded；外审及全球新颖性未认证；UM-TARGET-v1与其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/private_graft_and_resource_repetition.md)、[实际审查](../reviews/unrelated_machines/actual_kronecker_product_review.md)及其来源/输入/代码/冻结结果。


## UM-UNPRUNED-ASSIGNMENT-LP-KRONECKER-v1：未剪枝指派LP的精确可乘恒等式

- Objects / Domain / Definitions / Quantifiers：m>=1,n>=0，合法非负有理有限边/∞；全部机器对/任务对保留，有限资格笛卡尔积，时间非负乘积；不剪枝。 全部输入与所有参数按正文精确量词。
- Exact Statement / Conclusion：对所有合法非负有理矩阵含n0/zero/∞，未剪枝assignmentLP F(P⊗Q)=F(P)F(Q)，非负原初/对偶相乘；不是剪枝LST或CONFIG。
- Assumptions：结构结果无复杂度假设；排NP归约的结论以其实际P≠NP或随机归约假设为条件。
- Dependencies：UM-ACTUAL-NONNEGATIVE-KRONECKER-DOMAIN-v1；正文自足内部推导及明确标准工具。
- Scope：只给本seed全矩阵反例与指定未剪枝LP恒等式；无NP源，不排特定hard image或物理一致性产品，不是UM主反证。
- Evidence：Exact-first独立重构、实际完整作者读后和最终正文实读；源与新颖性分开。有限审计见review，不作一般证明。
- Counterevidence / Objections：旧checker负编号/额外row语义缺口已修；v3严格finite记录另审，不把旧版本追认为已拒。先前boss7同现象报告保归属。
- Status：complete scoped proof; independently reconstructed and actually reviewed; external review unrecorded；外审及全球新颖性未认证；UM-TARGET-v1与其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/private_graft_and_resource_repetition.md)、[实际审查](../reviews/unrelated_machines/actual_kronecker_product_review.md)及其来源/输入/代码/冻结结果。


## UM-MULTIWITNESS-SHARED-JOB-FEE-CAPACITY-v2：互斥查询多见证的阈值二收费与容量

- Objects / Domain / Definitions / Quantifiers：p>=1、0<a_r,b_r,c<=1有理，c+Σb>=1；q:H→A、x:A→R、f:R→S全部原任务，指定pattern、原f owner改派费。 全部输入与所有参数按正文精确量词。
- Exact Statement / Conclusion：OPT(P)=1；每pattern OPT_K=min(2,max(1,B_K))，闭beta<2最小fee按B_K>beta/ c+B_K<=beta/其余为∞/0/1。单queries各strict且阈值2共享同一f；无全开strict。非空K共同strict且每single收费迫|K|(beta−c)<B_K<=1，beta>=3/2时至多1；empty另0。
- Assumptions：结构结果无复杂度假设；排NP归约的结论以其实际P≠NP或随机归约假设为条件。
- Dependencies：UM-MULTIWITNESS-FEE-FIXED-MATRIX-DOMAIN-v2, UM-MODEL-v1；正文自足内部推导及明确标准工具。
- Scope：同一OPT1显式易解P的精确读取/费用合同；无共同全开strict、无源NO decoder或可复用fanout，不是OPT gap或UM主反证。
- Evidence：Exact-first独立重构、实际完整作者读后和最终正文实读；源与新颖性分开。有限审计见review，不作一般证明。
- Counterevidence / Objections：v1空K严格和式错误保留；v2明确非空K，empty另费0。
- Status：complete scoped proof; independently reconstructed and actually reviewed; external review unrecorded；外审及全球新颖性未认证；UM-TARGET-v1与其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/two_witness_query_separation.md)、[实际审查](../reviews/unrelated_machines/multiwitness_shared_job_fee_review.md)及其来源/输入/代码/冻结结果。


## UM-SINGLE-OUTER-PRIMITIVE-SA1-EPS2-4-v1

- ID/version：UM-SINGLE-OUTER-PRIMITIVE-SA1-EPS2-4-v1。
- Objects / Domain / Definitions：显式normalized-flat的typed单outer；跨全部outer-state索引的正homes互异、每home恰一own-singleton helper；fallback states normalized且只用与homes分离的任意共享B，可无fallback；无其他groups；全部selector/incidence/zero/unselected jobs保留。
- Quantifiers / Exact Statement / Conclusion：给定Q、0<epsilon<=1及同一完整primitive-SA1有理点，可det-bit-poly输出真实全组质量>=epsilon²/4及全部原job分配C<=2−epsilon²/4；成本按三项总编码。
- Assumptions：无复杂度假设；NP-source排除仅作为结构算法在P!=NP下的直接推论。
- Dependencies：UM-MODEL-v1, UM-SINGLE-OUTER-TYPED-PRIMITIVE-SA1-DOMAIN-v1, UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1；页内精确证明及已明确扣除的标准工具。
- Scope：特殊typed结构，不覆盖多个outer、无own-home辅助groups、一般UM；软件none、福利工具既有、全局新颖性未认证。
- Evidence：Exact-first独立重构、实际作者读后及最后规范正文的实读；root逐项实际读取；不登记未运行软件。
- Counterevidence / Objections：多个outer条件点不能免费合并；标准福利后端非本次原创；同名13/8门控矩阵是另一对象。 当前精确域无standing fatal。
- Status：complete scoped proof; independent Exact-first reconstruction and actual final reading; software none; novelty unverified；主目标及其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary.md)、[实际审查](../reviews/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary_review.md)及其保真来源。


## UM-SINGLE-OUTER-TYPED-13-8-v1

- ID/version：UM-SINGLE-OUTER-TYPED-13-8-v1。
- Objects / Domain / Definitions：显式normalized-flat的typed单outer；跨全部outer-state索引的正homes互异、每home恰一own-singleton helper；fallback states normalized且只用与homes分离的任意共享B，可无fallback；无其他groups；全部selector/incidence/zero/unselected jobs保留。
- Quantifiers / Exact Statement / Conclusion：只输入typed Q，恰11次普通有理LP查询、至多一次CDF舍入，det-bit-poly输出全部原jobs，C<=13/8 OPT；无OPT/点/oracle输入。
- Assumptions：无复杂度假设；NP-source排除仅作为结构算法在P!=NP下的直接推论。
- Dependencies：UM-MODEL-v1, UM-SINGLE-OUTER-TYPED-PRIMITIVE-SA1-DOMAIN-v1, UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1；页内精确证明及已明确扣除的标准工具。
- Scope：特殊typed结构，不覆盖多个outer、无own-home辅助groups、一般UM；软件none、福利工具既有、全局新颖性未认证。
- Evidence：Exact-first独立重构、实际作者读后及最后规范正文的实读；root逐项实际读取；不登记未运行软件。
- Counterevidence / Objections：多个outer条件点不能免费合并；标准福利后端非本次原创；同名13/8门控矩阵是另一对象。 当前精确域无standing fatal。
- Status：complete scoped proof; independent Exact-first reconstruction and actual final reading; software none; novelty unverified；主目标及其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary.md)、[实际审查](../reviews/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary_review.md)及其保真来源。


## UM-FLAT-UNIT-RESOURCE-PATH-K2-PRESERVATION-v1

- ID/version：UM-FLAT-UNIT-RESOURCE-PATH-K2-PRESERVATION-v1。
- Objects / Domain / Definitions：显式normalized-flat的全部finite-endpoint Boolean degree4共同functional，M2 PSD、job onehot所有允许乘子、每机器有限有理真实CONFIG的first/pair及全部global affine physical-load localizers；1<=T<2；证书完整提供而非免费finder。
- Quantifiers / Exact Statement / Conclusion：对每个Q及有理1<=T<2，raw K2(P(Q),T)可行 iff raw K2(P(D_+Q),T)可行；给定两方向任一有限有理证书可det-bit-poly转换，保原moments<=4与private CONFIG；同时省localizers版本亦同。
- Assumptions：无复杂度假设；NP-source排除仅作为结构算法在P!=NP下的直接推论。
- Dependencies：UM-MODEL-v1, UM-FLAT-RAW-K2-FINITE-RATIONAL-CERTIFICATE-DOMAIN-v1；页内精确证明及已明确扣除的标准工具。
- Scope：仅给定raw K2有限有理证书的双向转换；非exact SDP可行性后端、非canonical native C2、非弱R_cons的强gap升级，非一般算法或hardness。
- Evidence：Exact-first独立重构、实际作者读后及最后规范正文的实读；root逐项实际读取；不登记未运行软件。
- Counterevidence / Objections：弱R_cons点不证明强K2 gap；不能把canonical额外限制或任意quartic literal非负当raw合同。 当前精确域无standing fatal。
- Status：complete scoped proof; independent Exact-first reconstruction and actual final reading; software none; novelty unverified；主目标及其反面OPEN。
- Related Files：[正文](../current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md)、[实际审查](../reviews/unrelated_machines/normalized_menu_configuration_certificate_review.md)及其保真来源。


## UM-ANONYMOUS-TOKEN-M1-LIFT-M2-NONEXTENSION-v1：匿名原任务身份的矩障碍

- ID/version / Objects / Domain / Definitions：UM-ANONYMOUS-TOKEN-M1-LIFT-M2-NONEXTENSION-v1；共同degree4 Boolean functional/global M2；有限同菜单组k>=1,0<=r<=k，A/X满足XA=X、ΣX=rA的全允许乘子；原identity端onehot/Boolean至4；固定k4 d10 delta1/100点。全局affine-context容量块另允许任意显式原任务类别及非Boolean X。
- Quantifiers / Exact Statement / Conclusion：形式标签lift一般保共同M1含inactive/home与k1/r0/rk；给定67维aggregate M2(rank55)点有形式Q²=-1/150且无任何保全部<=4矩的原token M2 extension；必要整个head×context矩阵由原quadratic SOS给出，坏方向-1/25。 一般M1/必要块对所有该域共同functional成立；非扩展针对固定点。
- Assumptions：无复杂度假设；原onehot/Boolean/M2准确使用，signed beta非true law。
- Dependencies：UM-MODEL-v1, UM-ANONYMOUS-TOKEN-COMMON-MOMENT-DOMAIN-v1；页内Laplacian/Schur与原SOS。
- Scope：仅给定point非扩展，不是所有points不可行；13机context actualOPT1，非原任务K2 gap/hardness/一般算法或SDP finder；必要块未证充分，显式任务与binary需求不混。
- Evidence：Exact-first、实际作者读后及最终附录实读；root完整读两code、三个新目录重放。
- Counterevidence / Objections：M1不能升M2；异context块不可单独PSD；原input OPT1且可换point。当前范围无standing fatal。
- Status：complete scoped algebraic proof; Exact-first reconstruction and actual final appendix reading; finite exact audit only; novelty unverified；主目标/反面OPEN。
- Related Files：[正文§7](../current/unrelated_machines/home_unit_cycle_elimination_and_directed_token_bridge.md)、[新审查](../reviews/unrelated_machines/anonymous_token_label_lift_and_nonextension_review.md)及其原件/代码/证据。


## UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1

- ID/version / Objects / Domain / Definitions：UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1；固定18m17j34端normalized-flat族Qc，0<c<1有理、T1+c、epsilon1−c；完整共同Boolean/onehot degree4/M2、全部raw-affine物理localizers及每行完整legal CONFIG law共享全部本地矩；每行≤3端。
- Quantifiers / Exact Statement / Conclusion：对每个c可detbitpoly生成指定强物理证书，所有每机full-row laws仍不能保证direct A=a,Z=aE的同点plainSA1：负claim-state=-1/160、quality-state=-c/160；实际OPT1。
- Assumptions：所有共同表/全部原jobs按正文定义；无复杂度假设、真实global law或未知oracle。
- Dependencies：UM-MODEL-v1, UM-FLAT-RAW-K2-FULL-LOCAL-LAW-PULLBACK-DOMAIN-v1, UM-FLAT-RAW-K2-FINITE-RATIONAL-CERTIFICATE-DOMAIN-v1；页内自足PSD/SOS/有限矩或literal分解与标准rationalLP。
- Scope：只反对给定点指定map，非actualOPTgap/改点不可能/一般算法或hardness；全globaltriple positivity会切该点。
- Evidence：先独立Exact重构、root实际全文读后释放Proof、实际读后与最终新增两节实读；只一量词句后作定向核对。
- Counterevidence / Objections：原实例OPT1且有别的R点，旧14m同机triple缺口已透明保留。 当前精确范围无standing fatal。
- Status：complete scoped parametric counterexample; independent Exact-first and actual final reading; finite audit only; novelty unverified；主目标及反面OPEN。
- Related Files：[正文§13–14](../current/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary.md)、[实际审查](../reviews/unrelated_machines/raw_k2_canonical_pullback_and_sa3_repair_review.md)及其来源/证据。


## UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1

- ID/version / Objects / Domain / Definitions：UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1；任意显式normalized-flat Q，全部zero/inactive/indexed/unused finite endpoints；1<=T<2；共同完整有理degree4 L，全部原boxes/raw slack/unit resource cap1×≤3 raw literals及Boolean/onehot允许乘子。目标plain共同primitive-SA1精确定义。
- Quantifiers / Exact Statement / Conclusion：每真实T-schedule给S3 Dirac点；显式rationalLP infeasible=>OPT>T；每给定S3点的指定product pullback满足完整R_(2−T) plainSA1，若另给同点rawM2则另保canonicalM1；构建/求解/提取均totalbitpoly，无PSDfinder。
- Assumptions：所有共同表/全部原jobs按正文定义；无复杂度假设、真实global law或未知oracle。
- Dependencies：UM-MODEL-v1, UM-FLAT-RAW-SA3-POINT-DOMAIN-v1；页内自足PSD/SOS/有限矩或literal分解与标准rationalLP。
- Scope：仅necessary LP与充分point接口，非反向actual可行性/全部group rounding/一般UM；S3与K2无自动包含关系，optionalPSD不带exact SDPfinder；不称层数最小。
- Evidence：先独立Exact重构、root实际全文读后释放Proof、实际读后与最终新增两节实读；只一量词句后作定向核对。
- Counterevidence / Objections：Source cap1、所有三literal乘子、normalization与共同点不可省；未宣称S3已含PSD。 当前精确范围无standing fatal。
- Status：complete scoped same-point transfer proof; independent Exact-first and actual final reading; software none; novelty unverified；主目标及反面OPEN。
- Related Files：[正文§13–14](../current/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary.md)、[实际审查](../reviews/unrelated_machines/raw_k2_canonical_pullback_and_sa3_repair_review.md)及其来源/证据。


## UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1

- ID/version：UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1。
- Objects / Domain / Definitions：全部普通UM的positive binary-rational T与有限有理raw K2证书：全部finite端、共同degree4 Boolean/onehot商及M2、逐机完整legal CONFIG first/pair、全部global affine physical-load localizers；无共同CONFIG指标四次links、无canonical gates。
- Quantifiers / Exact Statement / Conclusion：所有k>=2，L2k²,M1+60Lk4的显式共享终端族实际OPT2−floor√k/k，raw K2在T1+1/k有det-bit-poly生成指定有理证书；缩放到T1实际OPT趋2，结合slot上界得此raw合同全类gap supremum2。
- Assumptions：无复杂度假设，全部原jobs不可分且每样本onehot；证书含全机CONFIG distribution但只共享first/pair。
- Scope：仅所列raw relaxation gap，非hardness/一般算法非存在性；row triple和跨行selector×incoming条件可切给定点，不声称canonical C2、joint-CONFIG M2、高阶load或全SoS(CONFIG)gap；一般输入证书finder未提供。
- Dependencies：UM-MODEL-v1、UM-RAW-K2-FINITE-RATIONAL-CERTIFICATE-DOMAIN-v1、UM-ST-ROUND-v1及正文§4–10自足定量证明。
- Evidence：独立Exact-first完整重构先冻，root实读后释放Proof；作者Proof读后和最终正文实际全文读；root实际读代码并两新目录精确重放。
- Counterevidence / Objections：当前raw合同无standing fatal；stronger two-event条件及same-row triple明确失败，不能扩为所有算法或高层级。
- Status：complete exact raw-system gap theorem; independently reconstructed and actual final read; finite local audit only; novelty unverified；外审、新颖性、独立论文价值未认证，主目标及反面OPEN。
- Related Files：[正文](../current/unrelated_machines/diluted_shared_terminal_raw_k2_gap.md)、[实际审查](../reviews/unrelated_machines/diluted_shared_terminal_raw_k2_gap_review.md)及所列原件/有限软件记录。


## UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1

- ID/version / Objects / Domain / Definitions：UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1；每固定整数d>=2、一般普通UM与目标T>0；共同degreeD=max(4,d) Boolean/onehot商、globalM2、每机legal CONFIG全部同机degree<=d矩一致及全部global-affine physical-load localizers；无joint CONFIG indicators或higher q。
- Quantifiers / Exact Statement / Conclusion：每固定d及所有k>=d，显式L2k²/M1+120Lk4+4kZAmax族真实OPT2−floor√k/k，T1+(d−1)/k有det-bit-poly指定证书；缩放target1实际值趋2，故此合同gap supremum2；指数可依固定d。
- Assumptions：无复杂度假设；全部原jobs不可拆/finite eligibility；每固定d分别量化，无binary d统一poly承诺。
- Dependencies：UM-MODEL-v1、UM-RAW-ROW-DEGREE-CONFIG-AFFINE-DOMAIN-v1、UM-ST-ROUND-v1及正文§13.1–13.6独立自足有限差分/定量概率证明。
- Scope：非uniform variable-d algorithm、非高阶负载/完整SoS(CONFIG)/canonical C2/jointCONFIG-M2 gap，非hardness或一般算法不存在；原degree3跨行条件切给定点；d+1>D仅自然延伸下一阶失败。
- Evidence：新Exact-first4294c…、作者Proof实际读后c3ac3…、最终新195行实读d4dcc…；旧前缀仅hash。root完整读source/code并一次规范CLI四例逐字重放。
- Counterevidence / Objections：degree3跨行条件始终负，下一阶仅自然extension；来源策略作者合作不计盲审，旧k2 audit不升级。当前精确合同无standing fatal。
- Status：complete fixed-d raw row-consistency gap proof; independent Exact-first, author read-after and actual new-section final read; finite four-case audit only; novelty unverified，主目标及一般反面OPEN。
- Related Files：[正文§13](../current/unrelated_machines/diluted_shared_terminal_raw_k2_gap.md)、[实际审查](../reviews/unrelated_machines/diluted_shared_terminal_row_degree_gap_review.md)及所列完整来源/有限记录。


## UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1

- ID/version / Objects / Domain / Definitions：UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1；任意输入k>=1个单indexed-state outers，所有positive homes跨outer互异，每home一个own-unit helper，shared B disjoint homes且任意显式normalized fallback，无其它groups；每outer Σw1,wmax<=1/(4096k⁴)，所有zero/duplicate/inactive原jobs保留。
- Quantifiers / Exact Statement / Conclusion：只输入完整typed Q，可det total-bit-poly输出全部ordinary P(Q)原jobs合法σ，Cmax<=19/10 OPT；内部plain共同SA1 LP infeas给actualOPT>17/16并用baseline，feasible用CDF/MW+globalvariance精确CE+q.1回填；无SDP/给定点oracle。
- Assumptions：algorithm无复杂度假设，标准rationalLP/有理算术/MW/ES/CE；source排除推论另假设P≠NP。
- Scope：仅此typed profile，非任意Q/多state outer/重home/一般UM，k²或高阶moment后续不混入；只有有限pair backend，无端到端软件。排近二hardness源仅所有输出本域、YESOPT1/NO>=2−γ fixedγ<.1且P≠NP。
- Dependencies：UM-MODEL-v1, UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-DOMAIN-v1, UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1及正文§3–9完整自足算法/概率/bit证明。
- Evidence：独立Exact-first用不同强凸势算法，后实际全文读作者MW算法，最终175行实读；root已实际全读source/code及一次新目录exact replay。
- Counterevidence / Objections：多state或large home不能免费归一；CE不能丢requestcoins；后续vector/moment候选不自动扩大此合同。当前精确范围无standing fatal。
- Status：complete scoped Q-alone deterministic bit-polynomial 19/10 algorithm specification; independent Exact-first and actual author/final read; backend audit only; novelty unverified，一般主目标及反面OPEN。
- Related Files：[正文](../current/unrelated_machines/multi_outer_single_state_tiny_home_rounding.md)、[实际审查](../reviews/unrelated_machines/multi_outer_single_state_tiny_home_rounding_review.md)及sources/finiteaudit。


## UM-RAW-SH3-CONDITIONAL-SUBTREE-FLOW-AND-INCLUSION-CUT-v2

- ID/version / Objects / Domain / Definitions：UM-RAW-SH3-CONDITIONAL-SUBTREE-FLOW-AND-INCLUSION-CUT-v2；完整显式native unique-home/unit-forward DAG加unit-only entry jobs；有理1<=T<2；同一个degree6原端Boolean/onehot/M3、各行合法CFG first/pair、全部global degq<=2物理负载平方；sink无自有jobs。
- Exact Statement / Quantifiers / Conclusion：每个正质量非home unit入口推出新的parent-bounded单根firstflow，real r=k(2−T)、k1可选不衰减；仅整数网格恢复辅助CFG first。集合包含原矩强制δd1(δd2−M)<=H，每固定多项式q缩放最终每固定T<2均sound FAIL，虽CFGopt1与actualOPT趋2。 逐点forall共同L及其positive入口；asymptotic先固定a,b,δ再forall允许整数scales。
- Assumptions / Dependencies：无复杂度假设；UM-MODEL-v1、UM-NATIVE-RAW-SH3-COMMON-ORIGINAL-ENDPOINT-DOMAIN-v1及正文自足PSD-null/条件流/普通LP/子集分解/原jobs计数。原paper包含机制扣除，不导入其hierarchy点。
- Scope：不是保原点矩的canonical扩展/原全实例新点/完整调度器/SH3gap/复杂性困难性；不ceil realquota、不将单entry失败等同整个OPT>T；多层同owner路径预算未免费继承。
- Evidence：inclusion Exact-first00c51…→实际Proof读后704bd…；general先行f7587…→作者v2实读0d2c4…；最终全文1e513…加唯一归一化差分d36fa…实读859cc…。root全部材料/code实际读并两fresh-output重放116d69…。
- Counterevidence / Objections：归一化记号歧义已统一a/p与f/a；rawpoint restriction保所有6次矩及bit增长已补。多层owner机制未解；无standingfatal于本精确范围。
- Status：complete scoped conditional-firstflow and inclusion sound-FAIL proof; independent statement-first and actual read-after/final diff; finite arithmetic audit only; novelty unverified；一般UM正反面OPEN。
- Related Files：[正文](../current/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity.md)、[实际审查](../reviews/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity_review.md)及所列原件/有限证据。
