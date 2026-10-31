---
id: "unrelated-machines/davies-rothvoss-zhang-matroid-santa-claus-v4"
kind: "resource"
type_tag: "资源"
title: "Davies–Rothvoss–Zhang 拟阵 Santa Claus 与超图匹配"
status: "retained-literature-source-read"
summary: "完整读取 arXiv:1807.07189v4（2026-01-04）冻结 PDF。文献定义 Matroid Max-Min Allocation，以拟阵基和资源分配为目标；给出紧凑 LP Q(T) 的 (1/5-ε)T-(1/5)max p_w 整数化结果，并由可匹配集拟阵得到 Santa Claus 的 (6+ε)-近似。算法是带拟阵交换的 Haxell 型增广树；第4节明确修正早期误称的 4+ε。"
truth_status: "published-source theorem statements and proofs read; literature comparisons and correction note retained as source claims"
review_level: "full-PDF-text-read; repository-cross-comparison; no external novelty certification"
scope: "Matroid Max-Min Allocation, compact LP Q(T), Haxell-style augmenting tree, restricted Santa Claus application"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/davies_rothvoss_zhang_2026_santa_hypergraphs_matroids_v4.pdf#pp1-18"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/davies_rothvoss_zhang_2026_santa_hypergraphs_matroids_v4.pdf#pp1-18"
source_inventory_id: "d1def15ac71c3fd998c8"
source_blob: "618606a42fbeba1a9c27c11777b4a9cc0fcbde40"
source_sha256: "a95a66ce64fbaf6c49086f6891a19909d271df2fd784e0da530424afd9c91081"
source_size_bytes: 186948
source_pdf_pages: 18
arxiv_identifier: "1807.07189v4"
legacy_ids:
  - "DRZ-MMATROID-SANTA-2026-V4"
  - "UM-LITERATURE-MATROID-MAXMIN-DRZ"
---

# 1. 实读范围与身份

冻结源 `d1def15ac71c3fd998c8` 的两个来源提交字节相同，PDF 导出后用 `pdftotext -layout` 读取全部正文、证明、图注、致谢和参考文献（18 个物理页）。题名为 *A Tale of Santa Claus, Hypergraphs and Matroids*，作者 Sami Davies、Thomas Rothvoss、Yihao Zhang，arXiv:1807.07189v4，文献标注日期 2026-01-04。本文不把摘要、仓库旧摘要或引用当作全文证明；以下按源文献的量词和模型记录。

全仓检索显示既有 `resource_distortion_flat_menu_rounding.md` 已引用该版本纠正“早期 4+ε”说法，并把 restricted Santa Claus 作为一个独立后端。此对象补足来源自身的拟阵模型、LP、增广树和参数边界。它与仓库的六人共同目录纯 SPE 题没有共同策略或支付定义，也不能直接转成一般 `R||C_max` 的新近似或困难性。

# 2. Matroid Max-Min Allocation 定义和紧凑 LP

给有限地面集 (X)、拟阵 (M=(X,mathcal I)) 和资源集 (W)。每个资源 (w) 有非负值 (p_w)，二部可用边 (Esubseteq X\times W)。要选一个拟阵基 (Sinmathcal B(M))，再把每个资源分给一个相邻的基元素，最大化
\[
  \min_{iin S}\sum_{w:\sigma(w)=i}p_w.
\]
资源不可拆分；未选入基的地面元素不需要收益。拟阵只通过基多面体、独立性测试和交换性质进入算法，文献不假设拟阵具有图、均匀或可显式列举的特殊结构。

给目标阈值 (T\ge0)，定义 (Q(T)) 为非负变量 ((x,y))，其中 (xin P_B(M))，并满足
\[
 \sum_{win N(i)}p_wy_{iw}\ge T x_i \quad(iin X),\qquad
 \sum_{i:(i,w)in E}y_{iw}\le1 \quad(win W),\qquad
 y_{iw}\le x_i \quad((i,w)in E).
\]
(x_i) 表示元素是否被选入基的分数质量，(y_{iw}) 表示资源分数分配。约束 (xin P_B(M)) 已经编码所有基的凸组合；Q(T) 的变量/约束规模为二次量级（给定边集）且不需要配置 LP 的指数配置枚举。

**Theorem 2（源文献主技术定理）。** 假设 (Q(T)\ne\varnothing)，给任意常数 (\varepsilon>0)，在拟阵成员资格可多项式测试时，可在 (n^{O_\varepsilon(1)}) 时间找到积分 (x,y)，使
\[
  (x,y)\in Q\!\left((1/5-\varepsilon)T - (1/5)\max_{w\in W}p_w\right).
\]
这里 (n=|X|+|W|)，积分 (x) 是某个基的特征向量，积分 (y) 是该基上的资源分配。定理是从 LP 可行性到降低目标的实际分配保证；它不声称 Q(T) 的积分间隙恰为 5，也不提供一般不相关机的目标解。

# 3. Haxell 型增广树与证明承重结构

对 (0<\beta<\alpha<1) 和 \(\delta=\max_wp_w/T)，把一个以元素 (i\) 为左端、资源子集为右端的最小超边称为 \(\nu\)-edge，当资源总值至少 \(\nu T)。最小性给出超边总值小于 \((\nu+\delta)T)。算法维护：

* 当前独立集 (S\in\mathcal I)，其中一个元素 (i_0\) 暴露；
* 覆盖 (S\setminus\{i_0\}) 的 \(\beta\)-超匹配 \(M\)；
* 增广树的 adding 层 (A_0,A_1,\ldots)（\(\alpha\)-edges）和 blocking 层 (B_1,B_2,\ldots)（当前匹配中的 \(\beta\)-edges）；
* 已发现元素集合 (C=\{i_0\}\cup B_X)。

一轮先用 Expansion Lemma 找到相互不交、避开当前已占资源的 \(\alpha\)-edges，覆盖 \(D\subseteq(X\setminus S)\cup C)，满足 \((S\setminus C)\cup D\in\mathcal I) 且 \(|D|\ge\mu|C|\)。若其相当比例与当前匹配相交，就新增 blocking 层；否则相当比例仍有至少 \(\beta T\) 的可用值，交给 Swap 子程序，把一层匹配边替换进来。

证明的关键数学环节是：

1. **交换引理。** 两个独立集的拟阵交换图有左完美匹配；由此得到 Weak/Strong Swapping Lemma。若 (C\subseteq S) 可被 (D) 替换而保持独立性，基多面体中所有可继续交换的元素总分数至少为 \(|C|-|D|\)。
2. **Expansion Lemma。** 用 Q(T) 的 (y)-质量与前述总分数下界双重计数。若贪心扩张在 \(|D|<\mu|C|\) 时卡住，则所有可交换元素的邻域在已占资源外价值小于 \(\alpha T\)，其 LP 质量必须集中到已占资源；与当前 adding/blocking 资源值上界矛盾。
3. **二分情形。** Lemma 9 证明，给定匹配 (M) 和新增超匹配 (H)，要么至少 \(\phi|H|\) 的边在去掉 (M) 后仍有 \(\beta T\) 可用值，要么至少 \(\phi|H|\) 条 (M)-边被相交；\(\phi=(\alpha-\beta)/(\delta+\alpha)\)。
4. **几何增长与终止。** Blocking 层满足 \(|B_{i+1}|\ge c|B_{\le i}|)。每次 collapse 令某层 blocking 数量按固定比例下降；用 \(s_j=\lfloor\log_b|B_{\le j}|\rfloor\) 的签名向量作字典序势，保证迭代严格下降。层数为 (O(\log |X|))，签名向量数量为多项式量级，故总时间 (n^{O_\varepsilon(1)})。

源文献取
\[
 \alpha=\tfrac25(1-\delta)-\tfrac\varepsilon2,\quad
 \beta=\tfrac25(1-\delta)-\varepsilon,
\]
并设置 \(\kappa=\varepsilon/2\) 及由 \(\alpha,\beta,\delta\) 定义的 \(\mu,c,\gamma\)。定理要求 (0<\varepsilon\le(1-\delta)/5)，且算法中的成员资格、交换和最小超边选择均必须能在多项式时间完成。不能删去 \(\delta\) 项而把结论改写成无最大资源惩罚的 \(T/5\)。

# 4. Santa Claus 应用：6+ε 的准确量词

Santa Claus 输入儿童集 (M)、礼物集 (J)，每礼物 (j) 有固有值 (p_j)，儿童 (i) 对该礼物要么价值 (p_j)，要么价值 0（restricted max-min fair allocation）。给定最优阈值 (T)，先将礼物分为大礼物 (J_L) 与小礼物 (J_S)，满足
\[
 p_j\le\delta_1T\quad(j\in J_S),\qquad p_j>\delta_2T\quad(j\in J_L),
\]
中间区间为空，且 (0<\delta_1\le\delta_2<1)。文献构造一个二次规模的 LP (P(T,\delta_1,\delta_2))，令大礼物的分数覆盖诱导 matchable-set matroid；其余儿童构成该拟阵的 co-matroid。用拟阵多面体整数性把大礼物分数 (x) 扩为 base-polytope 点 (x'\ge x)，再取余向量 (x^*=1-x') 和小礼物分配 (y^*)，得到 (Q(T)\ne\varnothing)。

Theorem 2 产生一个 co-matroid 基，所有其中儿童得到小礼物总值至少
\[
 (1/5-\delta_1/5-\varepsilon)T.
\]
补集儿童可由 matchable-set matroid 的定义各得一个大礼物，价值至少 \(\delta_2T\)。因此每名儿童至少得到
\[
 \min\{(1/5-\delta_1/5-\varepsilon)T,\,\delta_2T\}.
\]
取 \(\delta_1=\delta_2=1/6\) 得 \((1/6-\varepsilon)T\)，即相对最优值的 \((6+O(\varepsilon))\)-近似。源文献将其记作 **(6+ε)-approximation**，具体常数依参数重命名；这里保留其定理量词，不把公式机械地改成另一篇论文的 (4+ε) 结论。

文献还指出若礼物值分布让 \(\delta_2\) 明显大于 (1/6) 且 \(\delta_1\) 很小（例如礼物值为 (T) 或 1），同一公式给出接近 5 的比值。这是该实例域的参数性改善，不是统一 5-近似定理。

# 5. 与相关文献及本仓库范围比较

* Haxell 条件、AKS 的 restricted Santa 算法、Cheng–Mao 的后续常数和 Jansen–Rohwedder 的配置 LP 结果在本文引言中作为外部背景；本对象只把 DRZ 文献自身的 Theorem 2/3 与证明读入，不替这些外部结果重新认证。
* 本文的 Matroid Max-Min Allocation 与 Santa Claus 的 restricted 值结构相容，但一般 max-min allocation 允许每个儿童对同一礼物有任意非负值，不能用本定理直接覆盖。
* 本文不是一般 (R\|C_{\max}) 的 2 近似、低于 2 的硬度或配置 LP 的完整间隙定理。Santa 应用只使用礼物固有值和 matchable-set matroid；普通 unrelated-machines 的 (p_{ij}) 依赖机器。
* 与六人共同目录纯 SPE 模型无策略、最佳反应或覆盖均分语义；不应作为六人半覆盖结论的证明、反例或先验假设。

# 6. 版本纠错、证据等级与接续

源文献致谢明确说明早期版本曾声称 (4+\varepsilon)，经 Stephen Arndt 指出分析错误后，本版本改为 (6+\varepsilon)。修正点是：旧算法在层 collapse 后不保 blocking 层几何增长；当前版本令 adding edges 约为 blocking edges 两倍，并在每轮检查拥有足够可用资源的层，牺牲常数换取签名势终止。不得从旧摘要或旧正文保留 4+ε。

应保留的独有对象是：拟阵基上的资源分配定义、紧凑 (Q(T))、Strong Swapping Lemma、Expansion Lemma、层增长和签名向量、matchable-set/co-matroid 的 Santa 归约，以及最大礼物惩罚项。后续第三阶段可建立“来源→受限超图匹配”“来源→拟阵增广算法”“纠错→早期常数失效”关系；若要接到一般不相关机，必须另给逐边机器值的真实转换并证明不会破坏固有礼物值结构。

**处置建议：** `integrated` 或 `retained` 均需以本文写入 `archives/unrelated-machines/state/资源/` 的正式对象后再登记；本草稿作为完整阅读证据保留。由于当前会话的 GitHub 写端点未认证，本批不执行 `clean done`，不把本地文件称为已推送。
