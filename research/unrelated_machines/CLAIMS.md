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
