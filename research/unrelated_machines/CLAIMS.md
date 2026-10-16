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
