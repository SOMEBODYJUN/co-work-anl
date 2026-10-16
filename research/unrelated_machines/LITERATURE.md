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
