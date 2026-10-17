# 不相关并行机的原文、定理与模型边界

这是首批核心来源的核查账本，不是全领域综述。逐条下载状态、版本、页数、SHA256和限制在 [JSON清单](literature_manifest.json)。PDF取得不代表全部证明已独立复现。

| 来源 | 本次核对的结果及范围 | 原文与定位 |
| --- | --- | --- |
| LST1990 | Polynomial 2-approximation; PTAS for fixed number of machines; NP-hard to approximate within any constant rho < 3/2 unless P=NP. General offline integral unrelated-machine makespan; fixed-m PTAS separately. | [Approximation Algorithms for Scheduling Unrelated Parallel Machines](https://ir.cwi.nl/pub/6083/6083D.pdf)；[本地原文](../../history/source/literature/unrelated_machines/lenstra_shmoys_tardos_1987_unrelated_scheduling_report.pdf)；CWI report Theorems 1–3 (printed pp. 3–6); Theorem 5 and Corollary 2 (printed pp. 7–8)。版本：CWI report R8714 (1987), NOT the 1990 journal typesetting |
| ST1993 | A feasible LP with load target T, edge-size cutoff t, and cost bound C can be rounded to load <= T+t and cost <= C. In particular cutoff t=T gives load <= 2T with no cost increase. Cost-preserving bicriteria rounding; does not improve general makespan approximation constant. | [An Approximation Algorithm for the Generalized Assignment Problem](https://www.cs.cornell.edu/~eva/Approx.Algorithm.Generalized.Assignment.Prob.pdf)；[本地原文](../../history/source/literature/unrelated_machines/shmoys_tardos_1993_generalized_assignment.pdf)；Theorem 2.1, journal p. 463 (PDF p. 3); Corollary 2.3, journal p. 466 (PDF p. 6)。版本：Mathematical Programming 62 (1993), pp. 461–474 |
| SV2005 | Polynomial (2-1/m)-approximation, using consolidation of an acyclic fractional distribution with additive increase <= (1-1/m) times maximum processing time in support. Improvement depends on m and is not a uniform fixed-epsilon breakthrough. | [An Optimal Rounding Gives a Better Approximation for Scheduling Unrelated Machines](https://www.researchgate.net/profile/Nodari-Vakhania/publication/220060026_Optimal_rounding_gives_a_better_approximation_for_scheduling_unrelated_machines/links/5b391be50f7e9b0df5e454bd/Optimal-rounding-gives-a-better-approximation-for-scheduling-unrelated-machines.pdf)；全文已通过网页核对，未取得可落地PDF；Manuscript Theorem 1 (PDF p. 5); Theorem 2 (PDF p. 9); last paragraph of Section 4 (PDF pp. 9–10)。版本：Author-uploaded 10-page manuscript; published ORL 33(2), pp. 127–133 |
| EKS2008_2014 | Polynomial 7/4 approximation for graph balancing, where each job has at most two eligible machines and the same size at either machine. Restricted graph balancing; do not transfer to unrelated graph balancing with unequal endpoint sizes. | [Graph Balancing: A Special Case of Scheduling Unrelated Parallel Machines](https://iuuk.mff.cuni.cz/~sgall/ps/grbal.ps)；[本地原文](../../history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.pdf)；Theorem 3, author manuscript p. 14 (PDF p. 14); approximation setup in Section 2。版本：20-page accepted author manuscript linked by author; downloaded as PostScript, locally converted to PDF; not journal typesetting or SODA2008 8-page proceedings |
| VW2014 | Configuration LP has supremum integrality gap 2 even if each job is allowed on at most two machines with machine-dependent sizes. Unrelated graph balancing; not equal-edge-size graph balancing. A family approaches 2; no finite instance with exactly ratio 2 is asserted. | [On the Configuration-LP for Scheduling on Unrelated Machines](https://arxiv.org/pdf/1011.4957v1)；[本地原文](../../history/source/literature/unrelated_machines/verschae_wiese_2010_configuration_lp_v1.pdf)；Theorem 2, manuscript printed p. 4 statement and p. 7 proof (PDF pp. 5,8); Lemmas 4–6 in Section 3。版本：arXiv v1 submitted 2010-11-22; ESA2011 conference; Journal of Scheduling 17(4), 2014 |
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
