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
