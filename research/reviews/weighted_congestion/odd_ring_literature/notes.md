# Odd cyclic hubs 文献核对（R3 内部文献任务）

核对时间：2026-10-14 UTC。任务范围是 WC-TARGET v1 的 degree-dependent 存在/非存在因子及 odd cyclic hubs、unequal cohorts 的机制参照。本文是有限检索审计，不是新颖性证明；未修改正式 claim 状态。

## 可比较的基线

### L1：Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann

- 一手全文：[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3)，arXiv 版本日期 2022-03-27；初稿 2020-02-18。另有 [ICALP 2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32)、[MOR DOI](https://pubsonline.informs.org/doi/10.1287/moor.2022.1272)（卷 48(1), 2023）。这里核对的是固定 v3 全文。
- Paper fact，§2：固定正玩家权；各资源费用为非负系数 degree≤d 多项式；玩家成本为所用资源费用之和；近似条件是 ≤α 倍偏离成本。与 MODEL.md 的核心模型一致。
- Paper fact，§3 Theorem 1 / (3)：对 d≥2，其可认证非存在包络为

\[
 F_d=\sup_{n,k,w,\beta}\min\left\{
 \frac{1+n\beta(1+w)^d}{(1+nw)^k+n\beta},
 \frac{(1+w)^k+\beta w^d}{(nw)^k+\beta(1+w)^d}
 \right\},
\]

其中 `n∈N, k∈{1,…,d}, w,β∈[0,1]`。对每个 `α<F_d` 有该族的非存在实例；不是说每个参数实例的精确阈值就是两比值最小值，也不是全类 `a_*(d)=F_d`。
- Paper fact：论文给出的可增长下界是 `Ω(√d/ln d)`，且足够大 d 有 `F_d≥√d/(2ln d)`。其拓扑为一位 weight-1 heavy player、n 位等权 light players、两组 hub/spoke 资源。
- Paper fact，§6：general nondecreasing costs 下 n-PNE 存在，另有 `α<Φ_{n−1}` 的非存在族，`Φ_m∼m/ln m`。该后者用 step costs 和几何递减玩家权，不能把 n 改写为 polynomial degree d。
- 适用性说明：正式正权实例要求 w>0。w=0 是公式边界，第一比值为 1；不提高增长下界。sup 解释仅需对每个严格小于 F_d 的 α 选合适参数，不需端点 attainment。

本仓库 `sharp_source_review/proof.md` 对 F_d 的内部精细渐近分析属于独立项目资产；这里不把它当作已发表文献事实。

### U1：Caragiannis–Fanelli

- 一手全文：[arXiv:1902.07173v5](https://arxiv.org/html/1902.07173v5)，2020-11-06；初稿 2019-02-19。会议：[ICALP 2019](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.133)。
- Paper fact，Theorem 2(a)：取其 `Φ_1` 势，得到 finite-degree 保证

\[
 \rho_d=\max_{1\le k\le d}\sup_{x\ge0}
 \frac{(k+1)(1+x)^k}{(1+x)^{k+1}+k-x^{k+1}}\le d.
\]

Theorem 2(b) 给另一参数族；Theorem 7 的 existence/PoS tradeoff 是 `(d+δ, (d+1)/(d+δ))`, `δ∈[0,1]`。
- Paper fact：正文的基本资源形式是 `a_e x^{k_e}`、`a_e>0`、`k_e≥1`；策略可不同，权为任意正实数。其 finite-d 保证从 d 下方逼近，低 degree 保证并非新发现。
- 本任务的适用性重构：一般 polynomial 的非零单项可复制成始终共同选择的资源。常数项加入精确势 `Σ_i w_i a_{e,0} 1[e∈s_i]`，其 local marginal/cost ratio 是 1；零项省略。空策略与零成本直接使用未除法势差不等式。因此同一 `max{1,ρ_d}` 保证覆盖 MODEL.md 边界。
- 本任务独立推断：`ρ_d/d→1`。取 k=d、`x=2ln d/d`，上式比值为
  `(d+1)/(1+x+d(1+x)^(−d)−x^(d+1)/(1+x)^d)∼d`；结合 `ρ_d≤d`。故只改善 finite-d 的线性保证不是 WC-TARGET 的 o(d) 上界。

### U2：Giannakopoulos–Poças

- 一手全文：[arXiv:2005.10101v3](https://arxiv.org/html/2005.10101v3)，2022-03-30；初稿 2020-05-20。出版：[TOCS 67, 855–876](https://link.springer.com/article/10.1007/s00224-023-10133-z)，version of record 2023-07-10。
- Paper fact，Table 1 / Theorem 2：polynomial 这一行恢复 `(λ,(d+1)/λ)`、`λ∈[d,d+1]`，不是新的 sublinear-degree existence 保证。其他新界针对 concave/fair sharing/mixed cost families。
- 检查提醒：其 introduction 的一处对 CF19 的 PoS 概述写 `(d+1)/(δ+1)`，而本论文 Table 1 与 Theorem 2，以及 CF v5 Theorem 7 写 `(d+1)/(d+δ)`。不能只依据那句概述提取效率常数。本任务不使用效率常数证明 growth 下界。

### U3：Ren–Wu–Xu–Yang，bounded weight ratio 算法

- 可读一手固定稿：[arXiv:2208.11309v1 PDF](https://arxiv.org/pdf/2208.11309)，2022-08-24。新标题/作者扩充的 publisher 条目：[Computing approximate pure Nash equilibria for weighted congestion games](https://www.sciencedirect.com/science/article/pii/S2667325825006338)，检索显示 2025；其完整 journal 文本本次读取失败，不声称已逐项核对 final version。
- Paper fact，v1 §1/§2：对固定常数 d、`w_i∈[1,W]`（W 固定），报告 `ρ/(1−ε)` 算法，第二算法 `ρ=2W(d+1)/(2W+d+1)`；runtime 还参数依赖 coefficient ratio A、W、d。这里核定 preprint statement，不认证其所有算法证明。
- 模型边界：W 是经正比例缩放后的 `w_max/w_min` 上界，不是只给原始权重上界即可统一适用。WC-TARGET 允许该比值随 d、实例任意增大，故不能由此得全类 constant 或 o(d) 保证。

## 最接近的机制参照（不是优先权认证）

| 一手论文及版本 | 已核机制事实 | 与候选的关系和范围边界 |
| --- | --- | --- |
| [Hansknecht–Klimm–Skopalik, APPROX/RANDOM 2014 PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol028-approx-random2014/LIPIcs.APPROX-RANDOM.2014.242/LIPIcs.APPROX-RANDOM.2014.242.pdf)，2014-09 | §7：两玩家、四资源、2×2 行列交错策略；Theorem 16 给两玩家 sharp envelope。Table 1 的 universal 小 d 上界含 4/3、约1.785、约2.326。 | 双玩家 matching-pennies 型全 profile 改善循环；不是增长人数 odd hub cohort 机制。 |
| [Harks–Klimm, MOR2012 作者 PDF](https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/harks/HK-MOR-2012.pdf)，2012-08 issue | §3 Lemma3.4：两位 active 玩家与固定策略的 offset players；四 resource blocks 的行列交错策略构成涵盖所有 active profiles 的 4-cycle。 | prior art 已有 offset players 和 resource cloning。结论针对 exact PNE 一般函数类结构分类；未给 degree-growing approximate lower。 |
| [Goemans–Mirrokni–Vetta, FOCS2005 作者出版 PDF](https://math.mit.edu/~goemans/PAPERS/GoemansMirrokniVetta-2005-SinkEquilibriaAndConvergence.pdf)，2005-10 | §4.1 / Fig1：两位玩家、权1和2、四顶点六弧、四路径；去掉 strictly dominated 路径后，四个 profiles 形成严格改善环。 | 是无 PSNE 实例，理由包含全部非循环策略的排除；不是只凭一个局部改善环。只有两玩家，不含 odd movable cohort 放大。 |
| [Kleinberg–Ligett–Piliouras–Tardos, ICS2011](https://conference.iiis.tsinghua.edu.cn/ICS2011/content/paper/15.pdf) pp125–140 | p126 asymmetric cyclic matching pennies；p128 Lemma2.3：前驱的纯动作触发唯一反色 best response，odd cycle 无 pure NE。 | odd anti-coordination 的组合逻辑已有 general-game 一手参照。本文未给 WC-TARGET degree-controlled positive polynomial realization。 |
| [Milchtaich, Representation of Finite Games as Network Congestion Games 作者 PDF](https://econ.biu.ac.il/sites/econ/files/shared/staff/u36/papers/representation.pdf)，IJGT42(2013)1085–1096 | Theorem1：一般 finite game 可表示为 weighted network congestion game；§4.2 经统一常数平移可让 costs nonnegative/nondecreasing。 | 无 nonnegative polynomial coefficient/degree 限制。本任务推断：平移保 exact preference，不保 multiplicative improvement ratios；不能直接运输候选的 α(d)。 |

## 检索过程和证据等级

所有下面 query 在 2026-10-14 UTC 执行。搜索返回的 aggregator、ResearchGate、百科结果只作定位线索；数学陈述最终只依上面的 author/arXiv/publisher/proceedings 一手全文。搜索工具的 “Published/Crawled” 相对日期不是论文版本日期，版本以正文或 arXiv history 为准。OCR 有把 `√d` 丢成 `d` 的结果，尤其 RePEc/EBSCO；不可据其摘要认定 linear lower。

本任务的 degree-dependent 检索 query（保留原字符串；S1/S2 是两个引擎）：

```text
S1: "weighted congestion games" "approximate" "existence" lower bound polynomial 2025 2026
S1: "weighted congestion games" "pure Nash" "d" "lower bound" "log"
S1: "On approximate pure Nash equilibria in weighted congestion games with polynomial latencies" d delta
S2: "weighted congestion games" "existence" "2024" approximate
S2: "weighted congestion games" "existence" "2025" approximate
S2: "weighted congestion games" "nonexistence" "2023"
S2: "weighted congestion games" "approximate" "lower bound" "linear"
S1: "weighted congestion games" "approximate pure" "2024"
S1: "weighted congestion games" "approximate pure" "2025"
S1: "weighted congestion games" "approximate pure" "d/log"
S2: "Computing approximate pure Nash equilibria for weighted congestion games" Ren
S2: "weighted congestion games" "lower" "log d" "nonexistence"
S2: "weighted congestion games" "approximation" "degree" "2026"
S2: "weighted congestion games" "d" "existence" "improved" "2023"
S1: "2208.11309"
S1: "weighted congestion" "rho" "2W"
S1: "weighted congestion games" "pure" "sublinear"
S1: "weighted congestion games" "nonexistence" "-PNE"
S1: "S2667325825006338"
S1: "Computing approximate pure Nash equilibria for weighted congestion games" "2025" "rho"
S1: "Existence and Complexity of Approximate Equilibria in Weighted Congestion Games" "cited" "2026"
S2: "weighted congestion games" "nonexistence" 2024 2025 2026
S2: "weighted congestion games" "approximate" "Ω" "log"
S2: "weighted congestion games" "equilibria" "sqrt" 2025
S2: "weighted congestion games" "lower bound" "linear" equilibrium
S1 (recency 730d): "weighted congestion games" "non-existence" approximate polynomial
S1 (recency 730d): "weighted congestion games" "nonexistence" polynomial
S1 (recency 730d): "weighted congestion games" "approximate equilibria" "existence" degree
S1: "weighted congestion games" "lower bound" "d/log d"
S1 (recency 365d): "weighted congestion games" "nonexistence" "polynomial" "lower bound"
S1 (recency 730d): "weighted congestion games" "existence" "approximation factor" "2026"
S1: "weighted congestion games" "cyclic" "polynomial"
S1: "weighted congestion games" "odd cycle"
```

检索结果：在已读的一手资料和上述 query 返回条目中，未发现 WC-TARGET 同模型的已发表 `Ω(d/log d)` 或 linear-in-d 非存在定理。这是“本次未发现”，不是“全世界不存在”。

## 尚未消除的漏查风险及措辞

1. 本轮不是系统引用图穷尽：未把 CGG+20/2023 的全部 citing papers、学位论文、非英语稿、未索引 preprints 逐篇审计。
2. 2025 Ren 等 journal full text 未读到；只能核定 publisher 条目和其可读 v1 的限定模型。
3. odd anti-coordination 可出现在 broader graphical/general games；应把 degree-controlled weighted polynomial 实现与 odd-cycle 组合论本身分开。
4. 成本 rule 改成 Shapley allocation、player-specific costs、resource-specific weights、bottleneck aggregation、混合均衡、step functions、PoA/PoS、强制部分玩家选择指定策略，都不是同一个 a_*(d) 问题。
5. 若候选一般证明通过，可说“相对已核 CGG+ v3 的增长下界获得改善；本轮检索未找到同模型更强已发表下界”。不能说“全球首次”“已确定最新最优阈值”或仅凭 proof gadget 新形状认定新颖。

## 并行机制任务的补充检索日志

子任务也在 2026-10-14 UTC 完成，读取 HK2012 作者 publication PDF、HKS2014 publication PDF、GMV2005 author publication PDF、ICS2011 proceedings PDF、Milchtaich author全文。主文献任务再次打开这些一手来源并核对了 relevant section / theorem 定位。

两项全文缺口保留：Fotakis–Kontogiannis–Spirakis *Selfish unsplittable flows* [TCS2005 publisher](https://www.sciencedirect.com/science/article/pii/S0304397505005347)（DOI10.1016/j.tcs.2005.09.024）journal PDF 未成功读取；Academia 转录不作为最终 primary 数学证据。Libman–Orda *Atomic Resource Sharing in Noncooperative Networks* [2001 publisher](https://link.springer.com/article/10.1023/A:1016770831869) 完整 PDF 403，仅见 primary manuscript 的检索缓存与 HK2012 的回顾，仍应标为进一步核查入口。这里不依两项缺口认定机制优先权。

```text
S2: weighted congestion games odd cycle polynomial non existence approximate pure Nash equilibria Harks Klimm 2012
S2: Hansknecht Klimm Skopalik 2014 approximate pure Nash equilibria weighted congestion games
S1: "weighted congestion" "odd" "cycle"
S1: "weighted congestion games" "representation"
S1: "Harks" "Klimm" "2012" "pdf" existence
S2: "On the existence" "Harks" "Klimm" pdf site:math.tu-berlin.de
S2: "weighted congestion" "odd cycle"
S2: "weighted congestion" "cycle" "1.153"
S2: "Beyond the Nash Equilibrium Barrier" pdf
S2: "Sink equilibria and convergence" weighted congestion cycle pdf
S1: "HarksKlimm2012.pdf"
S1: "On the Existence of Pure Nash Equilibria" "three-player" "game"
S1: "weighted congestion" "cyclic" "polynomial"
S2: "congestion games" "odd cycle" equilibrium
S2: "weighted congestion games" "heterogeneous" "nonexistence"
S2: "weighted congestion games" "non-existence" "cycle"
S2: "On the Existence of Pure Nash Equilibria" "Fig" "3" Harks
S1: "congestion games" "odd cycle"
S1: "weighted congestion" "heterogeneous" nonexistence
S1: "HarksKlimm2012" "three"
S2: Harks Klimm 2012 moor 1120 0543 pdf
S2: "HarksKlimm2012.pdf" OR "HK12.pdf" congestion
S2: "On the Existence of Pure Nash Equilibria" Harks filetype:pdf -jstor -researchgate -math.tu-berlin.de
S2: "Cyclic Matching Pennies" "odd cycle"
S2: Fotakis Kontogiannis Spirakis Selfish unsplittable flows 2005 pdf
S2: Libman Orda Atomic Resource Sharing Noncooperative Networks 2001 pdf
S1: "Selfish Unsplittable Flows" pdf Fotakis Kontogiannis Spirakis
S1: "Atomic Resource Sharing" "pdf" "Libman" "Orda"
S2: "Libman" "Orda" "Atomic Resource Sharing" filetype:pdf -citeseerx -researchgate -proquest
S2: "Selfish Unsplittable Flows" site:cs.ntua.gr
S2: "Selfish Unsplittable Flows" "no pure" "Fig"
S2: "Atomic Resource Sharing" site:webee.technion.ac.il
S2: "Atomic Resource Sharing" site:libman.org
S2: "Atomic Resource Sharing" "no" "equilibrium" "1" "2"
S2: "Atomic Resource Sharing in Noncooperative Networks" "5."
S1: "Atomic Resource Sharing in Noncooperative Networks" "no" equilibrium "general"
S1: "Selfish unsplittable flows" "3." "Nash"
S1: "Selfish unsplittable flows" "Fig. 1"
S1: "Atomic Resource Sharing" "7."
S2: "Selfish unsplittable flows" "Figure" "2" "no"
S2: "Atomic Resource Sharing" "equilibrium" "counterexample"
S2: "Selfish unsplittable flows" "two players" "cycle"
S2: "Atomic Resource Sharing" "no NEP"
S2: "Atomic Resource Sharing in Noncooperative Networks" "general topologies"
S2: "Atomic Resource Sharing" "Figure" "equilibrium"
S2: "Atomic Resource Sharing" "Nash" "does not"
S2: "Atomic Resource Sharing" "Example" "delay"
S2: "Atomic Resource Sharing" "Cost-Sum"
S2: "Atomic Resource Sharing" "counterexample" "2"
S2: "Atomic Resource Sharing" "Fig. 3"
S2: "Atomic Resource Sharing" "no equilibrium"
S2: "Atomic Resource Sharing" "Cost-Sum" "Hence" "path 3"
S2: "Atomic Resource Sharing" "loop" "paths"
S2: "Atomic Resource Sharing" "users alternate"
S2: "Atomic Resource Sharing" "does not possess"
```


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
