---
id: "unrelated-machines/bamas-lift-project-mmda-santa-claus-v2"
kind: "resource"
type_tag: "资料"
title: "Bamas 升投影 MMDA 与 Santa Claus 文献"
status: "retained-literature-source-read"
summary: "完整读取 Bamas 2024 arXiv v2（冻结 PDF 导出后全文抽取）：深度 3 一轮 Sherali–Adams 的 n^{Omega(1)} 间隙、任意深度 path hierarchy 间隙与 locally-good 构造、restricted-assignment 附录结果；保留证明量词、模型条件、失败机制和开放猜想，不把文献结果转成一般 unrelated-machines 近二困难性。"
truth_status: "published-source theorem statements and proofs read; conjectural higher-round SA claim and literature implications remain open"
review_level: "full-PDF-export-and-text-read; repository-cross-comparison; no external peer-review or novelty certification"
scope: "MaxMinDegree Arborescence on layered directed graphs, Santa Claus lift-and-project relaxations, restricted-assignment appendix"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/bamas_2025_lift_project_santa_claus_v2.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/bamas_2025_lift_project_santa_claus_v2.pdf"
source_inventory_id: "80209b36a2ca6ee50b17"
source_blob: "e4f54c317b218f400c1899b51bcc63b12b7d5288"
source_sha256: "e1120098a847eb10689c529579af5d44b93ee5f6e655eae7621a2333bf76e8de"
source_size_bytes: 825616
source_pdf_pages: 5
arxiv_identifier: "2406.18273v2"
legacy_ids:
  - "BAMAS-MMDA-LIFT-PROJECT-2024-V2"
  - "UM-LITERATURE-MMDA-SA-GAP-BAMAS-V2"
---

# 1. 实读范围、文献身份和仓库比较

冻结源 `80209b36a2ca6ee50b17` 的路径是 `history/source/literature/unrelated_machines/bamas_2025_lift_project_santa_claus_v2.pdf`，两冻结提交内容相同，blob 与 SHA-256 见 frontmatter。用 `clean show --out` 导出 PDF，确认其为 PDF 1.5、5 个 PDF 页，再用 Poppler `pdftotext -layout` 读出全部 3324 行；没有只依赖摘要、文件名或旧图。本文题名为 *Lift-and-Project Integrality Gaps for Santa Claus*，作者 Etienne Bamas，arXiv:2406.18273v2，文中版本日期 2024-10-17。

全仓比较发现已有 unrelated-machines 正文曾只把 Bamas 作为 MMDA/assignment-LP/subtree 的文献定位（例如“原作业 SH3 子树流与包含容量双源续审查”及“有向需求与调度的压缩双向任务桥”）；那些页面明确没有重构该 PDF 的完整 SA/path hierarchy 证明。本页补上文献源的独有完整结论，同时保留现有正文的边界：它没有给一般 `UM-TARGET-v1` 的实际调度编译器、近二算法不可能性、NP/ETH 困难性，也与当前六人共同目录 SPE 的量词无交集。

# 2. MMDA 模型和松弛

文献研究分层有向图 (G=(V,E))，层 (L_0\dot\cup\cdots\dot\cup L_\ell)，边只从 (L_i) 到 (L_{i+1})，源 (s\in L_0)，汇点为 (L_\ell)，图大小为 (n)，深度满足 (\ell\le O(\log n/\log\log n))。每个非汇点有整数需求 (k_u)，构造中 (k_u\ge n^{\Omega(1/\ell)})。目标是选一个以 (s) 为根的有向树/子图 (T)，每个顶点入度至多 1，源出度至少 (k_s/\alpha)，每个被选非汇点出度至少 (k_v/\alpha)；最大化可行的 (\alpha\)（文献把它称为近似率，越大越好）。

朴素 assignment LP 使用边变量 (x_e\in[0,1])：源覆盖、每个非源非汇点的出流至少 (k_v) 倍入流、每点入流至多 1。文献说明 packing 或 covering 约束若统一损失因子 (\alpha)，可通过两次缩放转成标准 LP/整数解，需求损失约为 (\alpha^2)。

Sherali–Adams (SA) 的分布判据（文中 Theorem 6）是：若对每个至多 (r) 个变量的 0/1 条件事件，都存在同一分布使每条原 LP 不等式在条件期望下满足，则得到 (r) 轮 SA 可行解。path hierarchy 则只保留长度至多 (t+1) 的有向路径变量；已知 (\ell-1) 层足以给分层深度 \ell 的 polylog 近似。文献还定义 (t)-locally-good：路径树满足局部出度覆盖，并且在距离 (t) 内同一顶点的多重到达仅有 \(\operatorname{polylog}(n)\) 拥塞；既有结果把 \(\Theta(\ell)\)-locally-good 方案稀疏成整数解，损失 (n^{\Theta(1/t)})。

# 3. 深度 3 的一轮 SA 间隙

固定小常数 (\rho>0)、地面集 (U=[m])。四层 (L_0,L_1,L_2,L_3) 的顶点分别标记为空集、大小 (\rho m) 的子集、大小 (2\rho m) 的子集、大小 (\rho m) 的子集；相邻层只有包含关系的边（扩张段为 (S_u\subseteq S_v)，收缩段为 (S_v\subseteq S_u)）。需求 (k_s,k_1,k_2) 选成二项式比值，使整数解在三层分别需要
\[
|T\cap L_1|=\binom{m}{\rho m}/\binom{(1-\rho)m}{\rho m},\quad
|T\cap L_2|=\binom{m}{2\rho m}/\binom{\rho m}{\rho m},\quad
|T\cap L_3|=\binom{m}{\rho m}.
\]
图规模 (n=2^{\Theta(m)})，所有需求为 (n^{\Omega(1)})。

**Theorem 1（作者主结果）。** 对充分大 (n)，存在深度 3、规模 \(\Theta(n)\) 的 MMDA 图，所有 (k_u=n^{\Omega(1)})，其 assignment LP 的一轮 SA 仍有至少 (n^{\Omega(1)}) 的 integrality gap。该轮数下界对一般 SA 也成立，且作者指出深度 3 上两轮已知把 gap 降到 polylog，因此在轮数意义上是紧的（此处“已知”来自论文引用，本批没有外部复核）。

SA 可行性的核心不是独立边抽样，也不是直接复现已有 rounding：

1. 为每条边 (e) 构造以其终点为源的 subtree assignment-LP 解 (x^{(e)})，保留真实边身份和包含关系。
2. 先独立以 (x_e) 选 shadow edges (S)。每个 shadow edge 再独立触发一个按 (x^{(e)}) 抽样的 subtree，最后取所有触发子树的并集 (A)。
3. 证明任意边的出现概率满足 (x_e\le s_e:=\Pr[e\in A]\le6x_e)。这个常数比例是条件期望分析的关键：若条件事件是 (e_1\in A)，则以常数概率 (e_1) 本身是 shadow，从而触发足够出流；若条件为 (e_1\notin A)，出流/入流只单向减少。
4. 通过 multiplicity 计数、Chernoff/尾界和二项式熵估计，在任意单边正/负条件下同时满足 covering（损失至多 \(\operatorname{polylog}(n)\)）与 packing（常数因子）约束。独立分布的问题是无相关性；逐层 rounding 的问题是两层相关性造成 sink packing 的多项式拥塞；shadow distribution 位于两者之间。

积分侧的 gap 由 Section 4 的 Lemma 15 承担：任意整数 (\alpha)-approximate 解都满足 \(\alpha\ge n^{\Omega(1/\ell)}\)，深度 3 时即 (n^{\Omega(1)}\)。因此本结果是 assignment-LP/SA 的松弛间隙，不是调度问题的直接 hardness 结论。

# 4. 任意深度的 lift、path hierarchy 和局部好解

取参数 (\varepsilon=3/\ell)，令 (\ell=3/\varepsilon=o(\log n/\log\log n))，并要求 \(\varepsilon m=\omega(\log m))。扩张阶段 (i<2/\varepsilon) 的标签集大小为 (i\varepsilon\rho m)，收缩阶段 (2/\varepsilon\le i\le3/\varepsilon) 的标签集大小为 (4\rho m-i\varepsilon\rho m)。相邻标签仍以包含关系连边；分层需求 (k_i) 通过三段常数 \(\gamma'_1,\gamma'_2,\gamma'_3) 校准，使整数解在 (L_{1/\varepsilon},L_{2/\varepsilon},L_{3/\varepsilon}) 的规模分别等于上述三项二项式比值。

文中 Theorem 2：存在绝对常数 (c>0)，对充分大 (n) 与 (\ell\in\Omega(1)\cap o(\log n/\log\log n))，有规模 \(\Theta(n)\)、深度 \ell 的图，其 path hierarchy 在至少 \(\ell/c\) 轮后仍有 (n^{\Omega(1/\ell)}) 的 integrality gap。该结论基于路径变量
\[
y(p)=x_{e_1}\prod_{j=i}^{i+|p|-1}\gamma_j
\]
（(e_1) 位于层 (L_i)），并用 Lemma 17 控制短距离路径数，使 lifted packing 约束抵消额外的 \(\gamma\) 因子。作者**只证明 path hierarchy 的此量词**；他们在 Future directions 中把“同一构造是否在深度 \(\Omega(\ell)\) 的一般 SA 轮数下仍有 gap”列为猜想，不能把猜想改写成 Theorem 2。

Theorem 5 的四项性质是同一 lifted instance 的结构性后果：

1. 所有非汇点需求 (k_u=n^{\Theta(1/\ell)})。
2. 每个顶点属于至少 (n^{\Omega(\log\ell)}) 条有向路径。
3. 任意整数解损失至少 (n^{\Omega(1/\ell)})。
4. 存在 (\ell/c\)-locally-good 的整数路径集合。

这说明当前 path/round-and-condition、递归 greedy 和基于局部好解的稀疏化方法在该族上同时承受超多项式路径数与 (n^{\Omega(1/\ell)}) 损失；这是对算法技术的障碍解释，不是所有分层 Santa Claus 实例的下界定理。

# 5. restricted-assignment 附录的独立结果

附录 A 的 restricted assignment 是 Santa Claus 特例：资源 (j) 的值 (v_j) 与玩家无关，不可用边价值 0。Theorem 3：对任意 (n) 和 (\Omega(1/n)\le\varepsilon\le1/3)，存在规模 (n) 的实例，使得 SA 的 \(\lfloor\varepsilon n\rfloor\) 轮仍有至少 \(\Omega(1/\varepsilon)\) 的 integrality gap。构造为 (k+1) 个玩家、每人一个价值 (3\varepsilon) 的小资源、(k) 个价值 1 的大资源；随机把大资源匹配给 (k) 个玩家并确定性给对应小资源，任意至多 \(\varepsilon k\) 个变量条件下每个玩家期望价值仍至少 1，而整数最优仅 (3\varepsilon)。

Theorem 4：存在多项式算法，把 restricted-assignment 实例变成 canonical 实例（每玩家要么只可接大资源，要么至多一个大资源且其余为小资源，所有大资源价值归一为阈值 (T)），且保持近似意义；在该 canonical 域，**一轮 SA 的强度至少达到 Davies–Rothvoss–Zhang LP**，该 LP 已知 integrality gap 至多 4。此处是 restricted-assignment 的结构性正面结果，不适用于一般 unrelated-machines。

附录 B 给一个与 Bansal–Srividenko configuration-LP gap 类似的深度 3 MMDA 图：configuration LP 可行但整数出度仅 (O(\sqrt{k})) 量级；作者强调该构造能骗 configuration LP，却不能骗一轮 SA。附录 C 给出反例：即使每条边都有 subtree solution，若出现概率不满足 (x_e\le s_e\le O(x_e))，一轮 SA 仍可能只有 (O(\operatorname{polylog} n)) gap。该反例解释了为什么“每边有子树证书”不能替代 shadow distribution 的全局比例性质。

# 6. 结论等级、与仓库对象的关系和未闭问题

- **完整来源定理/证明：** Theorem 1 的深度 3 一轮 SA 间隙；Theorem 2 的任意深度 path-hierarchy 间隙；Theorem 5 的需求、路径数、整数 gap 和 locally-good 四项性质；附录 A Theorem 3/4 的 restricted-assignment 结果。
- **条件/引用性结论：** “深度 3 两轮 SA 已知 polylog”“局部好解的稀疏化损失”“MMDA 与 Santa Claus 的近似保持关系”均在文献中作为既有工作引用，本批没有独立复证相关论文。
- **猜想/开放：** 一般 SA 是否在深度 \(\Omega(\ell)\) 仍保留 gap；更强 Lasserre 层数；MMDA 与 Directed Steiner Tree 的正式关系；ETH 困难性；准多项式常数近似。
- **失败机制：** 独立产品分布条件后没有足够相关性；直接模拟 rounding 的两层相关性在 sink packing 处产生多项式拥塞；仅有 subtree solutions 但无 (x_e\le s_e\le O(x_e)) 也不够。
- **不迁移范围：** 本对象不声明一般 (R\|C_{\max}) 近二 gap、不声明 `UM-TARGET-v1` 困难性，不改变仓库中已存在的 MMDA-to-UM 条件桥；它只是可供第三阶段建立“来源/启发/障碍”关系的独立文献对象。

后续如要复用，应保留：分层深度量词、标签集大小、需求阈值、SA/path hierarchy 层数、局部好解定义及 (x_e\le s_e\le6x_e) 的 shadow 关键不等式；不能删去 restricted-assignment 的特例域，也不能把作者 Future directions 的 conjecture 当已证结论。
