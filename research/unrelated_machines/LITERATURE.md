# 不相关并行机的原文、定理与模型边界

这是首批核心来源的核查账本，不是全领域综述。逐条下载状态、版本、页数、SHA256和限制在 [JSON清单](literature_manifest.json)。PDF取得不代表全部证明已独立复现。

| 来源 | 本次核对的结果及范围 | 原文与定位 |
| --- | --- | --- |
| LST1990 | Polynomial 2-approximation; PTAS for fixed number of machines; NP-hard to approximate within any constant rho < 3/2 unless P=NP. General offline integral unrelated-machine makespan; fixed-m PTAS separately. | [Approximation Algorithms for Scheduling Unrelated Parallel Machines](https://ir.cwi.nl/pub/6083/6083D.pdf)；[本地原文](../../history/source/literature/unrelated_machines/lenstra_shmoys_tardos_1987_unrelated_scheduling_report.pdf)；CWI report Theorems 1–3 (printed pp. 3–6); Theorem 5 and Corollary 2 (printed pp. 7–8)。版本：CWI report R8714 (1987), NOT the 1990 journal typesetting |
| ST1993 | A feasible LP with load target T, edge-size cutoff t, and cost bound C can be rounded to load <= T+t and cost <= C. In particular cutoff t=T gives load <= 2T with no cost increase. Cost-preserving bicriteria rounding; does not improve general makespan approximation constant. | [An Approximation Algorithm for the Generalized Assignment Problem](https://www.cs.cornell.edu/~eva/Approx.Algorithm.Generalized.Assignment.Prob.pdf)；[本地原文](../../history/source/literature/unrelated_machines/shmoys_tardos_1993_generalized_assignment.pdf)；Theorem 2.1, journal p. 463 (PDF p. 3); Corollary 2.3, journal p. 466 (PDF p. 6)。版本：Mathematical Programming 62 (1993), pp. 461–474 |
| SV2005 | Polynomial (2-1/m)-approximation, using consolidation of an acyclic fractional distribution with additive increase <= (1-1/m) times maximum processing time in support. Improvement depends on m and is not a uniform fixed-epsilon breakthrough. | [An Optimal Rounding Gives a Better Approximation for Scheduling Unrelated Machines](https://www.researchgate.net/profile/Nodari-Vakhania/publication/220060026_Optimal_rounding_gives_a_better_approximation_for_scheduling_unrelated_machines/links/5b391be50f7e9b0df5e454bd/Optimal-rounding-gives-a-better-approximation-for-scheduling-unrelated-machines.pdf)；全文已通过网页核对，未取得可落地PDF；Manuscript Theorem 1 (PDF p. 5); Theorem 2 (PDF p. 9); last paragraph of Section 4 (PDF pp. 9–10)。版本：Author-uploaded 10-page manuscript; published ORL 33(2), pp. 127–133 |
| EKS2008_2014 | Polynomial 7/4 approximation for graph balancing, where each job has at most two eligible machines and the same size at either machine. Restricted graph balancing; do not transfer to unrelated graph balancing with unequal endpoint sizes. | [Graph Balancing: A Special Case of Scheduling Unrelated Parallel Machines](https://iuuk.mff.cuni.cz/~sgall/ps/grbal.ps)；[本地原文](../../history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.pdf)；Theorem 3, author manuscript p. 14 (PDF p. 14); approximation setup in Section 2。版本：20-page accepted author manuscript linked by author; downloaded as PostScript, locally converted to PDF; not journal typesetting or SODA2008 8-page proceedings |
| VW2014 | Configuration LP has supremum integrality gap 2 even if each job is allowed on at most two machines with machine-dependent sizes. Unrelated graph balancing; not equal-edge-size graph balancing. A family approaches 2; no finite instance with exactly ratio 2 is asserted. Section 4, Theorem 7 additionally gives a $2-g/p_{\max}$ LST-style guarantee for finite processing-time alphabets, so any fixed finite alphabet has a strict sub-2 algorithm; the theorem is an algorithmic barrier, not a hardness result. | [On the Configuration-LP for Scheduling on Unrelated Machines](https://arxiv.org/pdf/1011.4957v1)；[本地原文](../../history/source/literature/unrelated_machines/verschae_wiese_2010_configuration_lp_v1.pdf)；Theorem 2, manuscript printed p. 4 statement and p. 7 proof (PDF pp. 5,8); Theorem 7, printed p. 8 / PDF p. 8; Lemmas 4–6 in Section 3。版本：arXiv v1 submitted 2010-11-22; ESA2011 conference; Journal of Scheduling 17(4), 2014 |
| Svensson2011 | Restricted assignment configuration-LP gap <= 33/17; polynomial-time (33/17+epsilon) estimation of optimum. Local search constructs schedule eventually, with no proved polynomial convergence. p_ij in {p_j,infinity}. Estimation is not polynomial-time constructive approximation. | [Santa Claus Schedules Jobs on Unrelated Machines](https://arxiv.org/pdf/1011.1168v2)；[本地原文](../../history/source/literature/unrelated_machines/svensson_2011_santa_claus_schedules_v2.pdf)；Theorem 1.1 printed p. 2 (PDF p. 2); Theorem 4.1 printed p. 11 (PDF p. 11)。版本：arXiv v2 submitted 2011-03-21; PDF internal date 2018-10-23 differs and must not silently override version metadata |
| JR2016 | Restricted-assignment configuration-LP gap <= 2-1/6 = 11/6; yields polynomial (11/6+epsilon) estimation, not a polynomial constructive schedule. Restricted assignment only. | [On the Configuration-LP of the Restricted Assignment Problem](https://arxiv.org/pdf/1611.01934v2)；[本地原文](../../history/source/literature/unrelated_machines/jansen_rohwedder_2017_configuration_lp_v2.pdf)；Theorem 1.1, PDF p. 2。版本：v1 2016-11-07; v2 2017-01-13 (downloaded); SODA2017 conference; later incorporated into JR2019 extended manuscript |
| JR2019 | Configuration-LP gap <= 11/6; constructive (11/6+epsilon)-approximation in time n^(O((1/epsilon) log n)), n=|J|+|M|. Restricted assignment only; quasi-polynomial running time is not polynomial. | [A Quasi-Polynomial Approximation for the Restricted Assignment Problem](https://arxiv.org/pdf/1701.07208v2)；[本地原文](../../history/source/literature/unrelated_machines/jansen_rohwedder_2019_quasi_polynomial_v2.pdf)；Theorem 5, printed p. 13 (PDF p. 13); Theorem 16, printed p. 29 (PDF p. 29)。版本：v1 2017-01-25; v2 2019-08-20 is joint extension of SODA2017 and IPCO2017 papers; SIAM J. Comput. 49(5), 2020 |
| Li2023 | For every epsilon>0, (2+epsilon)-approximation for R||Cmax in nearly-linear time in number of eligible machine-job edges, suppressing polylog and polynomial 1/epsilon factors. Makespan result improves running time. Its (1.45+epsilon) result is weighted completion time, a different objective. | [Nearly-Linear Time LP Solvers and Rounding Algorithms for Scheduling Problems](https://arxiv.org/pdf/2111.04897v2)；[本地原文](../../history/source/literature/unrelated_machines/li_2023_nearly_linear_scheduling_v2.pdf)；Theorem 1.1, manuscript printed p. 3 (PDF p. 3)。版本：v1 2021-11-09; v2 2023-06-05; ICALP2023 published 2023-07-05 |
| Baba2026 | Prediction of heavy job assignments enables 1+epsilon with sufficiently accurate prediction; guarantee smoothly degrades and is capped by 2 OPT. Search budget K gives running time (mn)^K poly(m,n,log P,1/epsilon). K must remain constant for stated polynomial search; arbitrary prediction does not yield uniform <2 ratio. | [Learning-Augmented Approximation for Unrelated-Machines Makespan Scheduling](https://arxiv.org/pdf/2606.13133v1)；[本地原文](../../history/source/literature/unrelated_machines/baba_bampis_mitropoulos_2026_learning_augmented_v1.pdf)；Theorem 5.2 and Corollaries 5.3–5.4, Section 5.3; full HTML https://arxiv.org/html/2606.13133v1。版本：v1 submitted 2026-06-11; 22 pages; unreviewed preprint |
| BGW2026 | Polylog-round CONGEST algorithm with 2+epsilon integral guarantee or 1+epsilon fractional guarantee. Distributed communication model; better-than-2 round lower bound is not NP-hardness or a central-polynomial-time lower bound. | [Distributed Load Balancing on Unrelated Machines](https://arxiv.org/pdf/2607.10075v1)；[本地原文](../../history/source/literature/unrelated_machines/bernstein_gupta_wang_2026_distributed_load_v1.pdf)；Theorem 1.2 (PDF p. 4), formal Theorem 4.3; Remark 1.3 fractional alternative。版本：v1 submitted 2026-07-11; preprint |

| BCG2009 | Bateni–Charikar–Guruswami, *New Approximation Algorithms for Degree Lower-bounded Arborescences and Max-Min Allocation*: Theorems 3.1/4.2 give factor-2 hardness for additive DegreeTwo/InfDegreeOne Max-Min Allocation; Definition 4.3/Lemma 4.6 use a forest M-pyramid containing all sources. §7's duplication gadget only records a barrier below factor 2. These statements do not yield the rooted single-tree (b^*=1) versus (b^*\le\delta) gap. | [作者PDF](https://mhbateni.com/academic/pubs/maxmin-tech09.pdf)；[本地原文](../../history/source/literature/unrelated_machines/bateni_charikar_guruswami_2009_maxmin.pdf)；Theorems 3.1/4.2, Definition 4.3/Lemma 4.6, §7 Definition 7.1/Lemma 7.2。版本：TR-848-09 author PDF; targeted theorem locations read, full proof not independently reconstructed |

## 可以沿用什么、还缺什么

- LST的通用2近似与低于3/2的困难性分开引用；不把ρ=3/2也写成排除。已保存的LST公开全文是1987报告，未假装成1990期刊排版。
- Shchepin–Vakhania的2−1/m没有统一ε；作者稿的strict consolidation记号疑点另记在清单，不扩大“最优舍入”的否定范围。
- 等边长Graph Balancing与两端异长Unrelated Graph Balancing分开。图平衡的作者accepted稿和2008会议页码不混用。
- Svensson以及JR的多项式估值，不等于多项式输出调度；JR扩展稿的构造时间仍是准多项式。
- Shi Li的2021预印本/2023版本改进makespan运行时间，不能把另一目标的1.45类结果套到C_max。
- Baba等的预测辅助、BGW的分布式界限是相关机制，不改主目标的模型。
- 2026-10-16定向检索未找到一般确定性位多项式统一(2−ε)构造结果；这是有日期的检索观察，不是不存在定理或穷尽检索保证。

## 内化程度与下一步

已逐步重构的核心是[有序槽舍入与两树配置间隙](../current/unrelated_machines/model_and_classical_barriers.md)。可复现实验在tests/audits/unrelated_machines，证据范围逐项冻结。困难性归约、2005完整舍入和受限指派局部搜索仍待按承重需要复原。

教材Vazirani第17章、Schuurman–Woeginger综述及其他附件中提到的外围论文尚未构成已审原文库；清单中没有的原始25项JSON和构建说明没有被假称找回。继续沿种子文献的参考文献/后续引用扩展、去重并记录版本。

## 共同匹配接口新增的明确外部依赖

Karp1972的完美3DM为NP完全，Main Theorem原p94及第17项p95。本次实际取得[2010重印中的原稿扫描](../../history/source/literature/unrelated_machines/karp_1972_reprinted_2010_reducibility.pdf)，PDF第14/15页已渲染并图像核对；它不是1972原排版的单独PDF。真实URL、重印DOI、23页、字节及SHA256见manifest的Karp1972_reprint2010。这里只导入NP完全性Paper Fact，未独立重证Karp的完整源归约。其用于[共同大边选择的精确接口](../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)；不是UM-TARGET-v1或任何近似比例的困难性证明。

## 新路线实际承重的归约来源

BLMRS2024：[Santa Claus meets Makespan and Matroids](https://ir.cwi.nl/pub/36041/36041.pdf)，arXiv:2307.08453v1，37页，原字节与hash已取得。Theorem1印页2是一般近似归约的Paper Fact；Section2.1.2印页9–11的Lemmas12–14已直接重构selector/configuration/resource及调度转换。Lemma11/AppendixB仍未完整独立内化。印页6回顾标准Santa Claus间隙；本题[容量一紧凑星](../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)是机制简化的自足推导，不冒充新近似或新困难性。Corollary6的two-value改善依赖输入规模，不关闭UM-TARGET-v1。

## 联合槽前缀的针对性机制重构

VW2010 arXiv v1第4节Theorem8（PDF9/印刷8）及紧随证明的计数LP说明已针对性复核；原文是共同区间[γ,3γ]的11/6结果。新[逐机跨度2正文](../current/unrelated_machines/joint_slot_prefix_rounding.md)是相同机制的自行重构推论，γ_i可不同；不把它登记为Paper Fact或新颖性认证。Theorem9的已知机器type信息仍有额外假设，本阶段未宣称完整重建其全部技术报告证明。

## MMDA相关性机制的新定位来源

Bamas, *Lift-and-Project Integrality Gaps for Santa Claus*, [arXiv:2406.18273v2](https://arxiv.org/html/2406.18273v2)，2024-10-17，SODA2025作者版56页。[原始PDF字节](../../history/source/literature/unrelated_machines/bamas_2025_lift_project_santa_claus_v2.pdf)的SHA256/版本/取得状态见manifest。印/PDF页12 §2.1定义异需求分层MMDA；页3脚注1明确MMDA→Santa Claus近似保持关系，结合BLMRS2024的一般必要方向已经存在。

[本仓库直接token桥梁](../current/unrelated_machines/rooted_dag_degree_token_bridge.md)独立重构真实整数转换，给一般DAG及二进制需求填充的准确合同。源页5 Theorem1只核对一轮SA陈述，未独立重构全文证明，也未建立调度SA保真；不能把它当调度困难性。Theorem2深度比值记号与上下文有倒置疑点，本阶段不导入。下载/定位/机制重构/SA完整证明各自分开记录。

## 森林边界接口的结构算法背景与经典舍入祖先

Jansen–Maack–Solis-Oba, [Structural Parameters for Scheduling with Assignment Restrictions](https://arxiv.org/abs/1701.07242)，arXiv1701.07242v1，Theorem3（印页/PDF3）和§3末Results（印页/PDF11）给一般R∥Cmax在常数dual/incidence treewidth时的FPTAS。原始19页PDF已取得；投稿2017-01-25与PDF内部2018-10-08分开，hash见manifest的JMS2017_structural。只核相关陈述/机制，不声称全部证明已内化。[森林边界正文](../current/unrelated_machines/forest_boundary_contraction.md)自行证明根负载支配和恢复，未认证新颖性。

固定最优边际的舍入边界另核ST1993图1、印页464–465经典tight例；与私有sink新scope比较见[正文§9](../current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md)。SV2005单任务加性sharpness不升级为所有算法不可能。

## 原任务拟阵容量外包的标准背景

Goemans, [MIT18.433拟阵讲义](https://math.mit.edu/~goemans/18433S11/matroid-notes.pdf)，2011-03-16 Handout9，第1页定义/partition例及第4页Theorem4.1唯一回路性质已核。15页原始PDF字节与hash见manifest；当前star正文第7节由augmentation自行证明所需特例及锐容量权衡，不认证新颖性或一般调度结论。

## 对称共同条件矩的原始定义

Lovász–Schrijver, *Cones of Matrices and Setfunctions, and 0-1 Optimization*, CWI BS-R8925（1989-10），[原始38页报告](https://ir.cwi.nl/pub/5815/5815D.pdf)。实际字节已保存，hash见manifest的LS1989_matrix_cones；PDF8/印5 §1(a)(i)要求对称，PDF10/印7 (iii″)给列/补列，PDF11/印8式(3)区分非对称投影。此处印刷页码来自PDF页面底部，与公屏207曾少一页的定位不同；正文数学无冲突。只核这些定义，不宣称全文证明内化。[任务聚合与重置正文](../current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)自足证明特定运输规则的2T门槛，同时在同一边际上给T重新耦合；不是源定理或LS间隙。

## 平坦矩提取的经典来源

Laurent–Mourrain, *A Sparse Flat Extension Theorem for Moment Matrices* (arXiv:0812.2563v1, 2008)，实际[CWI原始PDF](../../history/source/literature/unrelated_machines/laurent_mourrain_2008_flat_extension.pdf)已取得，12页、154865字节，SHA见manifest的LM2008_flat_extension。核读Theorem1.2/Corollary1.3（页2–3）及§2 Lemma2.1（页6–7）的交换乘法构造；不宣称全部应用证明重构。[本题四阶矩正文](../current/unrelated_machines/global_assignment_moment_rounding.md)自足证明使用的布尔特例和近平坦定量接口，经典flat结论不计为原创算法，定量扩展的全球新颖性未认证。

反面路线的新增定位阅读：Bamas2025 arXiv:2406.18273v2 PDF/印刷p44开放问题4明确询问MMDA的ETH困难性，并指出直观转换会指数规模；不把SA gap当近2调度hardness。BLMRS arXiv:2307.08453v1 Theorem1为PDF3/印刷2页的算法归约方向。只新增定位核对，原PDF字节及完整证明重构状态未变；见[私有组合正文§1](../current/unrelated_machines/private_graft_and_resource_repetition.md)。

## 有限覆盖与配置点实现的标准祖先

Vontobel–Koetter，[arXiv:cs/0512078v1](https://arxiv.org/pdf/cs/0512078v1)，2005-12-20，67页。Proposition10（PDF/印18）及AppendixA.1的Lemmas55–56（PDF/印50–52）给二元线性码局部多面体有理点的有限覆盖解释。原始字节/hash见manifest的VK2005_graph_cover。这里只核该机制，不声称源论文证明了调度困难性；[调度专门重构](../current/unrelated_machines/configuration_finite_cover_obstruction.md)自行证明配置阈值覆盖不变、任意高围长可实现与输出尺寸限制。不是原创性或全篇内化认证。

## 仙人掌精确算法的最近祖先

Asahiro–Miyano–Ono，*Graph classes and the complexity of the graph orientation minimizing the maximum weighted outdegree*，[作者稿](https://kyutech.repo.nii.ac.jp/record/2000093/files/10347755.pdf)，DAM2011。§3（PDF/印5–11）及Theorem9（PDF/印11）给对称端点边权cactus精确算法；§3.1另含顶点固定权。原始字节/hash见manifest的AMO2011_cactus_orientation。本文不能把cactus精确求解笼统称新；[块参数与配置锐界正文](../current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md)自行重构非对称端点权/最大块环秩扩展及伪森林边界，不将其标为AMO的原文定理，也未认证全球优先权。


## 标签一致性接口的已知困难性方法边界

Bateni–Charikar–Guruswami，TR-848-09，[49页作者PDF](https://mhbateni.com/academic/pubs/maxmin-tech09.pdf)，Theorems 3.1/4.2 给 additive DegreeTwo/InfDegreeOne Max-Min Allocation 的因子<2困难；Definition4.3/Lemma4.6 的 M-pyramid 是含全部源点的 forest。§7 Definition7.1/Lemma7.2 只把 duplication gadget 路线限制到低于2，未给 α≥2。已下载原字节并做目标位置文本核读；当前树模型的非可导入性见 [两份完整复制地板](../current/unrelated_machines/duplication_two_copy_floor.md)。


## 整束缺陷着色的标准势函数来源

Fuchs–Kuhn，*List Defective Colorings: Distributed Algorithms and Applications*，[DISC2023正式PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol281-disc2023/LIPIcs.DISC.2023.22/LIPIcs.DISC.2023.22.pdf)，PDF4/印22:4，在Definition1后明确将缺陷着色存在性和势函数机制追溯Lovász1966。只联网核这一定义/机制归属，未保存原字节或宣称分布式算法全文内化；manifest的FK2023_defective_coloring_background明确取得状态。[大需求束正文](../current/unrelated_machines/large_bundle_collision_square_root_floor.md)自行证明整数势+Cauchy+容量Hall，未把该组合公式冒充源定理或认证新颖性。

## 现行裸C2接口的针对性对照

Verdugo–Verschae–Wiese，[arXiv:1811.08539v3](https://arxiv.org/abs/1811.08539v3)，2020-05-16，34页；PDF/印3 Theorem1及AppendixB（33–34）已联网核读其陈述/定义。它研究CONFIG上高轮SoS的小常数间隙；本文 `UM-C2-LOAD-UNIT-GAP-v1` 的[单位伪矩证明](../current/unrelated_machines/c2_unit_multislice_gap.md)只是对仓库裸degree-four负载合同的精确自足判定，不能将后者包装成更强CONFIG层级下界。该源仅web读取，未落地原始字节或重构全文；全球新颖性未认证。

## 有符号阈值 PCSP 的源困难性及出现次数缺口

Brakensiek–Guruswami，[ECCC TR16-183 原始PDF](https://eccc.weizmann.ac.il/report/2016/183/download)，35页，Theorem1.3 PDF6/印4已实际核读。对arity2A−1、严格重量0..A、弱重量0..B且A≤B≤2A−2，允许否定和常量的一般PCSP为NP-hard；固定ρ<2可取A>1/(2−ρ)、B=floorρA。这只是原分类的直接代入，不是调度困难性。原定理不限制变量双出现、相反符号；每机等权的调度端口合同则可容量匹配精确解。[单任务投影正文](../current/unrelated_machines/signed_one_job_port_downset.md)定位普通复制缺口。仅web核原陈述，原字节未落地、全部源归约未重构，取得状态及限制见manifest。

## 三特殊物品复制接口的针对性扣除

BCG2009 的已登记 TR-848-09 §7 Definition7.1/Lemma7.2（原作者PDF/印47–48）已经提出三特殊item a vsbc的完整分配复制合同和两完整分配剪度。本次[三host/半值正文](../current/unrelated_machines/three_host_selector_sharp_three_halves.md)不把该接口或剪度冒充原创；规范proof独立用非负二色阈值闭包，给无条件half实际allocation及含全部预载的锐3/2完整调度，未导入该文困难性或配置算法。本组初核仅web读取§7/准确范围；本次合并保留同行随后取得的原始PDF字节及manifest哈希，全球新颖性仍未认证。

CCK2009，[arXiv:0901.0205v1](https://arxiv.org/abs/0901.0205v1)，35页，§6.1 PDF28–31的Claim3/Theorem6及逆向环证明已针对性核读；已给精确配置证书时可精确减半。它只出现在第二名审查者的独立K4重构中；规范二色proof不依赖该定理。近似pricing的ε不能置零；web-only取得状态及完整前提见manifest和审查，未取得原字节。


Magniez等，[递归多数原始PDF](https://arxiv.org/pdf/1309.7565)，§2.2 PDF4–5定义完整三叉多数树。仅作为[叶命中递推](../current/unrelated_machines/unit_readout_pruned_forest_boundary.md)的经典模型背景，不将query复杂度结果当通用横截定理或调度困难性；全(k,r,h)命中式由自足递推证明，未认证新颖性。仅web实读、未落地原字节，已准确登记manifest。

## 连续残余通过量与次模背景

Lok–Romero Morales–Vermeulen (2005)，[大学原PDF](https://cris.maastrichtuniversity.nl/ws/files/1037187/guid-9485980d-bc86-4240-b008-d8fb2096cc3d-ASSET1.0.pdf)，§3.2印p5/PDF6为job-only资源消耗；§6.3 Theorem6.2/Cor6.3印pp17–18/PDF18–19为机集合次模。Kulik等ESA2019，[正式PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol144-esa2019/LIPIcs.ESA.2019.69/LIPIcs.ESA.2019.69.pdf)，§2.1.1/Theorem1及§3为共同job大小下的item子集LP值次模。两者仅为相关祖先，不当作任意异端p容量格定理；[本阶段自足证明](../current/unrelated_machines/residual_throughput_and_occupation_projection.md)自行处理对偶格封闭。仅web定位读原PDF，未物化字节/填写hash或宣称完整内化；Topkis原件没有被本阶段读取，全球新颖性未认证。

既有Karp1972再版原文新增用途：[树估值minorant域](../current/unrelated_machines/private_tree_branching_valuation_and_minorants.md)的标准Independent Set源。root重新渲染PDF14/原印94核Main Theorem与item3 CLIQUE，补图保阈值；只导入标准NP完全性，不称本轮重构Karp全证明，不复制另一份扫描。该计算障碍不属于makespan近似困难性。

## 近单位promise源的原始定理与普通扇出边界

新增原件：BBKO arXiv1811.00970v3，73页，Def5.16/Prop5.17在PDF33/印33给strong C-fixing minion criterion；KKR arXiv1602.03124v6，33页，Thm7/8 PDF5/印0:5仅普通edge-CSP；Feder作者原PS12页，Theorems3–4印8–11的clauses/minimal-support/三坐标机制。root及独立审查实际读取相关范围，原字节/hash见manifest；未宣称重构所有外部证明。当前[自足PCSP正文](../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)导入BBKO，另外两源只核ordinary→promise迁移不能免费成立。Feder期刊2001元数据与未注明日期的作者PS版本分开；不把转制PDF冒原件。

## Moshkovitz2015最终版：短列表与逐右局部费用

官方最终PDF已保真取得，SHA/bytes/pages见manifest，非会议版PGC条件稿。root及内部研究者实际核印227–229的Def4.5–4.6/Lem4.7、Cor4.8、Claim4.10。Cor给polylog左列表、固定素数幂右度的agreement源；Claim的局部s_b包含各incident左点全部已选标签，不能替换成一个组件一次收费。对应[源预算正文](../current/unrelated_machines/list_agreement_degree_budget_and_decoder.md)独立证明线性地板及ceil2d/D全agreement锐阈值，未把文献定位当新hardness。

## 部分MinRep度数取舍的primary核查

新增DS作者2014 PDF及Manurangsi arXiv原字节，SHA/版本/bytes与实际读取范围见manifest。Mosh final另实际读印223–224的完美完备PCP定义与Thm2.1/2.3，固定误差重复即可，不用PGC。Manurangsi Lem7已有采样/trimming、O(glogg) degree框架；[现行源证明](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)以更低原soundness与rare covered上尾、一次共同总边数事件给较粗polynomial alphabet下O(g) degree，并未宣称同时最佳字母表或全球首创。

Minzer–Zheng ECCC TR24-027的2026 revision1 §7.4/Lem7.12/Thm7.13显示定理仍给O(glogg) degree和O(g^{2+epsilon}) alphabet。root及作者实际读相关primary段；初web-only比较冻结后实际取得2026原字节并核hash/106页，manifest记录获取顺序，原比较不倒改。此处不认证其整个应用证明、新颖性或连通性应用改进，实际UM compiler仍缺。


v3源比较新增Kun arXiv0706.1701v2（已核12页原字节，Thm1/9）及DKR TALG2015 final §3（web实际读，下载403不伪称本地原件）。高girth CSP和同纤维换位修短环是已有技术；[正文](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)只把复制列表同时性/degree/regular固定girth组合列为本次已证增量，未认证新颖性。


FMW TR26-179 Revision2的Definition1.1/Theorem1.6及AppendixB已实际核读，119页原PDF、版本/SHA/bytes见manifest。它给perfect exact4-to1固定误差Paper Fact；不自动给regular/degree/girth、Qpoly(g)或UM反证。[v5源](../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)以度数比例copies补正规化，仍为随机归约。


AFS2008作者稿Thm2/3与Annamalai2016v2 Thm1.1/1.3已实际核读并存原PDF，manifest区分经典匹配框架与本文[私有树配置桥](../current/unrelated_machines/private_injective_tree_configuration_floor.md)，未导入不适用的变rank构造算法。

PSM2018作者稿§6/Fig5/Thm2已实际核读，总资格≤2/3/4及big-buffer框架；原PDF版本/hash见manifest。common-b双small合同见[正文](../current/unrelated_machines/joint_slot_prefix_rounding.md)，明确直接框架推广，非原文字面无限unit域。

## 非整数背包伪矩的经典机制边界

Potechin, *Sum of Squares Lower Bounds from Symmetry and a Good Story*, ITCS2019，[正式页面](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2019.61)摘要已核：明确恢复Grigoriev的knapsack下界。已保存20页正式原始PDF，hash/字节见manifest；实际核摘要与§1.1 Theorem1（PDF3/印61:3），未独立内化全篇。[匹配矩正文](../current/unrelated_machines/strong_configuration_matching_moment_obstruction.md)自行给出所需harmonic PSD和K22编译，不认领背包伪矩的新颖性；精确调度接口与锐修复距离亦无全球优先权认证。

DGR2025/2026 constrained rejections全arXiv v1原PDF已取得并parse（18页，SHA/bytes见manifest），实际核§5印13–14的degree5/binary/7states/15sets参数，§3由内部构造者定位。其Theorem4是固定常数的高保留率ungrouped硬度；不提供near-zero grouped源。本文另定义的cube普通UM桥有[Hall与全类锐3/2，DGR19/15](../current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md)；这些是独立结构推论，不归给原论文或认证新颖性。


## VW2010v1 的degree2 additive后端：本次实际读取

沿用既有VW2014登记的arXiv v1原PDF（不替换字节）。root及两内部独立审查实际读§5.1、Lemma11、Theorem12，PDF10–11/印9–10，含preassignment和两匹配二着色；原件按binary input给纯组合2approx，允许item两端异值、degree1及省去zero edges。仅用于[两组资源加权菜单](../current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md)：每group一aux agent，item正支撑≤2，条件真实满足。新部分是group平均、原UM/XOS恒等式和保OPT bonus的直接结构推论；不把此旧SC算法或原论文CONFIG2gap当新增成果。

已登记BCG2009原件本次另核§2.2 Theorem2.4/Fig2（PDF/印8–9）：d copies、d−1相邻dummy玩家的item路径降度是已知机制，MinMax脚注亦有提及。[flat菜单路径重构](../current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md)§6不主张装置原创，只给具体ordinary UM helper矩阵、全部原jobs/partial导出、OPT2/V0与位复杂度的可复用自足合同；后续三态selector树也不因此成为新hardness源。原PDF字节与既有理论身份保留。

[Lee–Svensson–Thiery arXiv2409.17831v1](https://arxiv.org/abs/2409.17831v1)的[14页原PDF](../../history/source/literature/unrelated_machines/lee_svensson_thiery_2024_affine_line_set_packing_v1.pdf)已实际定位§2/3/4：prime R、变量degree≤R、slope/intercept整set一致性；stated YES≥1−ε/NO≤k(1+ε)/((k−3)R)、k≥4、NP⊆BPP例外。不是perfect YES或tiny partial-set hardness。constraint作group、allowedtuple作state的uniform普通UM桥对所有local choices都有Hall半保留/actual≤3/2，见[自足桥审计](../current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md)；tuple作独立group+dummy未排。原论文数学、target桥分析与新颖性分开；未核DOI排版不冒作本地版本。

## BLMRS 单阈值配置合同的完整替代重构

[分块计数与真实匹配后端](../current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md)完整给出Lemma11同一单阈值列表合同的自足替代证明及总位复杂度，不宣称逐字复现AppendixB的原record机制。v1 AppendixB印20–21的tiny cutoff与乘法删除断言有精确反例，正文记录原字样、Fraction反例和局部修复；原PDF字节不改，不以此否定原主定理。Lemmas12–14机制另提取为normalized type matching的真实OPT=2−V接口；全局选择仍OPEN。


## DLRV2023v1：NSW框架与本次显式分数替换

[arXiv:2309.04656v1](https://arxiv.org/abs/2309.04656v1)原23页PDF保真存储，SHA/bytes及版本边界见manifest。root针对性实际读§2.1–§2.5、AppendixB及相关solver/Thm17/19/20，渲染阅读PDF12/13；不是root整篇全文认证。新作者读所供v1完整提取文本，审者只读指定相关段，具体范围见[实际来源审查](../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md)。原作matching/splitting/iteration/rematching是继承模板；[当前自足证明](../current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md)的任意显式有理XOS确定性fractional NSW、local-grid及同组修复后果不能当原文逐字结论。未认证全球新颖性，非2024正式排版，源字节不改。

## 显式菜单福利舍入的既有机制归属

Feige, [On Maximizing Welfare When Utility Functions Are Subadditive](https://epubs.siam.org/doi/10.1137/070680977)，SIAM J. Comput. 39(1), 122–142：原刊摘要明确记录 fractionally subadditive 的 1−1/e 福利舍入。此轮只实读原刊摘要，未下载原PDF或重构全文。新增 [F2部分激活计数](../current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md) 给自足证明及 W−δA 确定化；是标准工具在精确源合同上的直接推论，不认领该福利机制新颖性。

## DNS作者稿：本次福利机制的明确既有来源

[作者PDF](https://www.cs.yale.edu/homes/schapira/cfjournal.pdf)15页版，metadata 2009-10-30且刊头有placeholder，不称2010正式排版。§3.2 PDF8–9 Theorem3.2/Lemma3.3已给独立配置、attaining clause与逐资源最大系数舍入，有限n因子更强；Prop2.1 PDF5给显式XOS查询。原字节/哈希在manifest，内部源审者实际文本与四页渲染、root primary相关文本的范围见[新审查](../reviews/unrelated_machines/normalized_gated_menu_welfare_review.md)。本文使用该既有机制，不认领新福利算法；门控桥与特定源后果另证。


[原端SH3条件子树流与包含容量切](../current/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity.md)的本次定位：root核既有Bamas v2原PDF字节SHA e1120098…并实际读本地文本560–716、908–990、1815–1868，区分原assignment-LP/polylog-congestion/包含计数与新原job共同SH3合同。原图、rare-terminal机制不认领新颖；rho1/100是新自足数值范围而非原paper所有估计的认证。未重审全文SA证明，也不把新soundFAIL误作paper定理反例或复杂性困难性。

## 任意资格价格覆盖的单侧舍入祖先

`BBMV2019_degree_multiplicities_v2`：[Bérczi–Berger–Mnich–Vincze arXiv1911.09890v2](https://arxiv.org/pdf/1911.09890v2)，Theorem2印2/PDF3及upper-only证明印11/PDF12，给整数multiplicities的单侧Delta−1，Delta是最大列总量。按二进制有理共同分母缩放直接得到本文+b界；因此[任意汇点正文](../current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md)的舍入引理是旧工具重构，不认领新一般方法。root实际读取primary PDF/HTML，未落地PDF、未假填SHA。

`BLRT2026_weighted_equitability_v1`：[Bérczi–Liu–Reis–Tarnawski arXiv2608.13983v1](https://arxiv.org/html/2608.13983v1) §5 Theorem10给相关双侧weighted-discrepancy背景。本轮仅针对性读primary HTML，不把该结果倒记为本结构算法或全部论文内化。覆盖背包、匹配、MW同样是标准工具；新结构组合的全球新颖性/独立论文价值仍未认证。
