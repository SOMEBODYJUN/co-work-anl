# 逐机两倍跨度的前缀计数、实际槽舍入与位多项式搜索审查

审查结论：冻结版本的 `UM-ROW-SPREAD-TWO-ROUND-v1` 有完整的显式必要LP、联合舍入和目标搜索证明，未发现仍成立的 fatal objection。它给出受限矩阵类上的确定性位多项式3/2近似实际调度，不需先选大边匹配H，不需全局粗gcd。这是已知前缀计数机制的直接推论；不解决 `UM-TARGET-v1`，不认证全球新颖性、独立论文价值或外部同行评审状态。

## 冻结对象、独立程度与来源

实际首次审读正文为 `research/current/unrelated_machines/joint_slot_prefix_rounding.md`，SHA256 `e2f0d96ac49e6f269ef13dfe27d8a29002b1ba5bb9eea4d2f1165697d1b28b74`。最终正文SHA256为 `8b1abf7a149759cb2f9c7424c380181442990e0f7ee913273a1c1091526f3e00`；审查者已核对最终文件，并将唯一独立程度措辞替换回原句后精确恢复首次hash，确认数学部分未变。最终版本仍无fatal objection。

审查者在读正文前按Exact Claim及任务消息中给定的前缀计数机制，独立重构了目标LP、四段逐机估计、任意全局槽匹配同时保持前缀计数，以及固定γ下的单调目标搜索。中途任务消息已提示“两条前缀计数及T<4γ时的总数floor”，因此本审查不声称在完全没有候选机制提示的条件下独立发明该LP。完成证明重构后才全文读取冻结稿并读、运行两份实际审计。

另读取本地原始VW arXiv v1 PDF第9页/印刷第8页，SHA256 `2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a`。Theorem8确为全局共同区间[γ,3γ]的11/6配置间隙界，紧随说明确实将三个计数行加入LST-LP形成算法。冻结稿将本页逐机不同尺度、跨度2的结论明确标为机制推论，没有冒称原文Theorem8本身就是本页定理。

## 删零与固定行尺度

将每个有零边任务分到任一零端并删除保持OPT精确不变：限制原调度到剩余任务不增负载，反向加回零任务也不增负载。该操作在同时处理所有机器时仍然正确，因为所有新增负载都是0。

对每个剩余非空行，存在γ使所有有限时间在[γ,2γ]等价于最大值≤2倍最小值，故可将γ_i固定为该行最小有限处理时间。固定发生在目标搜索之前；空行跳过γ定义，全部零/空任务在计算正gcd之前直接返回零调度。若仍有任务，每个任务至少一条正有限边，故上界U有限且为正。

删零后跨度条件是明确的额外矩阵假设。各行γ可以相差任意倍数，证明没有把它们替换为一个共同下界。

## 必要LP与前缀计数的同时保持

给T>0，只使用p≤T边，设置非负x、每任务列和1与每机分数负载≤T。对每机器加入

`Σ_{p>T/2}x≤1`，`Σ_{p>T/3}x≤2`；

若T<4γ_i，再加 `Σ_j x_ij≤floor(T/γ_i)`。

这些均对每个makespan≤T整数调度必要：不能容纳两个严格大于T/2的任务、三个严格大于T/3的任务，总任务数由每项至少γ控制。等于阈值的任务不应被放入严格前缀，冻结稿处理正确。

对某行按p非增序连续排列x质量。如果前缀质量≤整数k，该前缀内每个正质量任务的整个行区间都在[0,k]中。只按正交长连槽边，所以它只能连该行前k个单位槽；当区间端点恰等于k时，不会误连第k+1槽。任意覆盖任务的槽匹配因每槽至多一任务，均在该行至多选择k个此前缀任务。总质量≤整数k同理限制总槽数和总任务数。

每任务总质量1和每槽容量1给分数匹配，故Hall保证存在覆盖所有任务的整数匹配。前缀性质对每个覆盖匹配、每一行都成立，因而一次全局匹配同时保留全部行约束。这里没有逐行分别选择互不相容的匹配，也没有先固定big任务。

## 四段估计及边界攻击

写t=T/γ_i，缺失的第二、第三任务按0处理。

- 0<t<2：floor(t)≤1，因此最多一任务，且保留边p≤T，负载≤T。t<1时实际上无保留边，表中的弱界仍成立。
- 2≤t<3：最多两任务，且严格>T/2的任务至多一条。因此较大者≤T、另一条≤T/2，和≤3T/2。
- 3≤t<4：最多三任务。γ_i≤T/3及行跨度给第一大≤2γ_i≤2T/3；第一条前缀计数给第二大≤T/2；第二条给第三大≤T/3。和为3T/2。
- t≥4：全行最大时间≤2γ_i≤T/2，普通ST加性界给舍入负载≤分数负载+最大时间≤3T/2。

t=2、3分别进入允许两条、三条的分支；t=4时删除总数行并使用普通ST，仍恰有最大时间≤T/2。所有端点都正确，不需要额外严格余量。该推导对全部机器同时成立。γ_i很小或分母很大不影响不等式。

## 目标单调性、极小有理数与位复杂度

固定删零后γ_i，再增大T：可用边只增加，负载容量只增加，两个严格前缀只缩小，floor(T/γ_i)不减，在T=4γ_i时仅删除总数约束。因此已有x扩零后仍可行。目标LP的可行性单调性没有被分段合同破坏。

用全体剩余正有限处理时间的有理gcd d仅建立搜索格点。取分母积D，再计算整数Dp的gcd并除D，D及全部中间整数的位长均为输入位长多项式。d可以极小；算法不会逐一扫描U/d，也没有把d/最大时间作为近似余量。每个机器负载和OPT都是d的整数倍。

U=Σ_j min_i p_ij由逐任务最短端分配给实际上界，U/d为正整数且二进制位长多项式。目标0在仍有正任务时不可行，目标U由实际调度给LP证书。对整数k∈[0,U/d]二分，调用次数O(log(U/d+1))。OPT对应格点且其整数调度满足必要LP，所以最小可行格点T_*≤OPT。无需LP真正连续阈值恰好落在格点上。

每次LP只有O(mn)变量、O(m+n)约束，系数、阈值比较、floor及目标均为多项式位长。标准有理LP的确定性位多项式求解是明示导入的工具，审计没有冒称实现通用LP求解器。非空LP可取多项式位长基本可行解。

列和1使每个正x≤1，其区间至多正交两个单位槽；每行槽数≤n，总数≤mn。累加有理端点的分母积位长受所选x总位长控制，排序、正交长判定、增广匹配与输出n个机器编号均为总位多项式。最终负载≤3T_*/2≤3OPT/2。不存在依赖γ大小、固定m或指数配置枚举的隐藏循环。

## 实际审计与parity证书

审读和重跑的局部审计：`tests/audits/unrelated_machines/row_spread_prefix.py`，SHA256 `1d15f1515ff3bc1b63ab857e7e2ace44b4cf766fe9f72cf21ba5fbac1380c195`。

它对γ=1、0至4个任务、处理时间{1,3/2,2}、x∈{0,1/2,1}、半整数目标1/2至5的全部局部候选，以及seed 271828的10000个大分母边界样本，验证满足行LP约束后所有槽最大值之和≤3T/2。真实输出为83810个候选、39673个可行候选、38279个正支撑可行候选，全部通过。它是单行包络检查，不是所有全局LP求解，也没有穷举任意γ或任意有理分母；一般性来自上述缩放及位复杂度证明。

实际parity审计：`tests/audits/unrelated_machines/half_unit_joint_slot.py`，最终加强版SHA256 `c07f31788f7aad244a781468a439e1cbcb565f839a8e5695bb9fa9d73ce0c763`。初读时版本仅显式检查分数负载，审查者另外用只读计算逐条检查了LP前缀、总数floor与输出计数；root随后将LP前缀和floor断言加入脚本。审查者读取并重新运行了该最终hash，结果通过。

该例10机14任务，四个三元组任取两项都共享某一坐标，故没有完美3DM。每激活列的2/3+1/6+1/6=1，每关联列1/2+1/2=1。源行γ=1/2、总质量2、两个前缀质量为0及2；三元组行γ=1/2、总质量3/2、两个前缀质量1/2及3/2；元素行γ=1、总质量1、两个前缀质量都为1。每行分数负载确为1，全部LP约束成立。

实际覆盖槽匹配的负载按脚本机器顺序为 `(1,1,1,3/2,3/2,1,1,1,0,0)`。通用合法端容量回溯拒绝makespan1并接受3/2，结合半整数负载得到OPT=3/2。该回溯没有把3DM判断当调度oracle。例中部分三元组机器同时容纳时间1与1/2任务，正好说明实际联合舍入可以不提供δ<1/2的(Aδ)见证，与前篇承诺构造障碍相容。

## 异议状态与未认证范围

没有未解决的致命异议。必要LP、一次全局匹配的逐机同时性、T/γ端点、正有理小尺度、目标搜索单调性及全部删零边界均已检查。审查中仅作了parity脚本断言加强及独立过程表述精确化，未修改数学定理。

本审查不证明行跨度可任意大时仍有3/2或统一低于2算法，也不证明简单删除tiny任务保持目标。通用LP求解器及其有限实现工程不在两份审计实现范围；正确性与多项式存在性调用标准有理LP工具。最终资产登记、后续全文措辞变化及新的正面机制须按实际版本另行核对。

## 双small行v2的实际顺序、实现和近邻扣除

绑定UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2。此前row-spread hash是旧冻结版本的历史记录，不是本追加后整页hash。root据hardness_route阈值合同自行重构CONFIG/slots、所有OPT分支及3DM下界，不是零信息盲审；冻结时已知PSM2018摘要，未收到本次两个审查者推导。literal/shared先只读Exact，分别独立重构直接flow/一般ell容量表及不同3DM归约，冻结后才收到root证明作实际读后攻击。literal先核Karp原文重印PDF MainTheorem/3DM定义，PSM比较后加。四份记录无standing fatal。shared最终显式范围稿替代较早读后稿，限制common-b而不扩至任意不同big时间。

root已全文读四份审查，亲核zero/低阈值精确流、显式CONFIG规模、Q>2与Q≤2逐机同时界、真实unit身份、所有OPT分支及3DM原P提取。root全文读191行独立Fraction/整数流代码并真实重跑，16128 local、300随机矩阵、7997阈值、q2全部256源子集PASS；实际观察JSON精确等于作者冻结结果。代码源hash f0e534a880bf072cde15126c4db3b8f417fe234e087ffa31a8d57af349dd989b。root新输出单独存放不覆盖原结果。

代码provenance的Exact-only指创建者建模时顺序；root运行在读后审查后，不倒称盲审。实现是另一份一般ell流合同，仅有限b1网格/m≤4/n≤5样本及q2；不作为完整CONFIG-LP生产工具或普遍证明。代码3DM helper的q0不作为生产合同，数学源q≥1并有常量退化分支。root实际核PSM2018原PDF摘要/§6/Fig5/Thm2 PDF8–11；原文字面域不同，common-b适配在正文明确写全。状态为published-framework synthesis，非新算法或一般UM突破。

冻结源及SHA256：
- history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_exact_statement_source.md：051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065。
- history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_root_frozen_proof_source.md：63da068c732421f76efa84cac37ad15d3e6fd24cc86af605403a344eadaf809a。
- history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_independent_literal_source.md：ee6ce66d47247d16dac6cf2a71be92ea5894f8feccafbe0195e81ce989a57437。
- history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_independent_shared_source.md：d2fbd514316482e7a0c40a035ed65bcc1a909bda584fcb17da29d95b03e67705。
- history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_read_after_literal_source.md：2be403fa4c1976a22ddf8ef1e3d8c7c4444404da6834eaf7d1731ed9243a75b8。
- history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_read_after_shared_scope_source.md：bb1dab81d8f0208e7eb4bf683573d72d3020093d1ccadadc9db2741c10ca8b9f。

最终组合actual read：literal实际全文核正文SHA ab1a6cd8c7c3b5cceabc7a4a103d77180ee0465f722dddbeb277400cc2533be4；三类非fatal导航/来源词句修正后的byte已核。旧v1前缀仍精确恢复8b1abf7a149759cb2f9c7424c380181442990e0f7ee913273a1c1091526f3e00，数学无改；root也全文实际读取本节。冻结最终回执：history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_final_canonical_receipt_source.md，SHA b48ef90d2b8c1153dc2c8831872172dee853a94a15cf8b10edfc51360eddd376。本段追加不改变所绑定canonical；没有声称审查者读跑新code。
