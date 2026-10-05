# 选题价值与正式发表对标：2026-10-05

本次评估以同步后的 `main@1683437` 为研究基线，核对根 README、RESEARCH_STATE、CLAIMS、FAILED_ROUTES、现行模型与分支主定理，并查阅下列一手文献。它是**有证据的编辑判断**，不是新数学定理、全面优先权认证或录用预测。本轮没有重新完整审查仓库所有证明，也没有改变任何命题的状态。

## 结论与投入判断

现有主成果有形成强专业理论论文的潜力。共同目录双设施的黄金比上界与位多项式构造最适合先形成一篇完整论文；任意设施数的统一因子 2 存在性是另一项有独立价值的主线，不能因为一般算法尚未完成而将其视为没有研究价值。最近增加的条件性离轨接口、特殊图类算法及指定优先规则反例，主要适合支撑主线，尚不足以仅靠积累数量形成同等分量的论文。

**当前主要目标期刊：Algorithmica、ACM Transactions on Economics and Computation (TEAC)、SIAM Journal on Discrete Mathematics (SIDMA)。Mathematics of Operations Research (MOR) 可作为有理由的冲刺目标。** 若完成全输入、任意设施数的位多项式构造，而且关键选择机制有独立的可复用内容，MOR 的竞争力会提高；SIAM Journal on Computing (SICOMP) 才值得更认真考虑，仍应视为高风险目标。

以上是领域声誉、主题匹配和贡献结构的判断，不是 JCR 或中科院分区，也不是接受概率。它以核心证明成立、贡献归属核定和一篇清晰完整的稿件为条件。

## Paper Fact：相近论文实际发表在哪里

每行都将相似性和不可直接类比之处列明。不同模型的数字 2、3、φ 不能直接比较优劣；社会福利 PoA 与设施偏离倍率也是不同指标。

| 论文、作者与正式发表 | 已核对的贡献 | 与本项目相近的维度及差别 |
| --- | --- | --- |
| Krogmann, Lenzner, Skopalik, Uetz, Vos, **Equilibria in Two-Stage Facility Location with Atomic Clients**, IJCAI 2024, 2842–2850 [P1] | 等权客户 SPE 存在性；不等权的 φ 以下不存在例及 NP 完全性；均衡社会福利 PoA=2。Theorems 5–6、Observation 4、结论见 pp.2848–2849。 | 最接近的模型与开放问题。原文给出的加权存在上界随设施数增长；它没有给出本项目共同目录双设施的 φ 上界算法或全 k 常数 2 构造。它是会议论文，不能当成期刊版本。 |
| Krogmann, Lenzner, Skopalik, **Strategic Facility Location with Clients That Minimize Total Waiting Time**, AAAI 2023, 37(5), 5714–5721 [P2] | 客户均衡存在、唯一、可高效计算；设施 SPE 可能不存在且存在性 NP 难；高效构造 3 近似 SPE。 | 同为两阶段设施—客户博弈，结合均衡、算法与困难性；但客户可拆分，我们的客户为不可拆分原子并允许独立混合。 |
| Caragiannis, Fanelli, Gravin, Skopalik, **Approximate Pure Nash Equilibria in Weighted Congestion Games: Existence, Efficient Computation, and Structure**, TEAC 2015, 3(1), article 2 [P3] | 用 Ψ-games 将原加权拥塞博弈联系到势博弈，得到存在性和输入位长多项式的常数近似算法，以及短改善序列结构。 | 与“存在但难选 → 新机制 → 高效近似均衡”非常相近；它处理更一般的一阶段策略与多项式成本，且近似的是玩家自身 NE，我们保持客户 NE 精确、仅近似设施稳定性。 |
| Christodoulou, Koutsoupias, Spirakis, **On the Performance of Approximate Equilibria in Congestion Games**, Algorithmica 2011, 61, 116–140 [P4] | 原子/非原子拥塞博弈的近似均衡效率界，包含尖锐 PoA 和部分 PoS 刻画及统一分析。 | 对标尖锐常数、原子与连续对照和组合分析的论文形态；不是本项目的 SPE 选取算法。 |
| Lücking, Mavronicolas, Monien, Spirakis, Vrto, **Which is the Worst-Case Nash Equilibrium?**, SIDMA 2024, 38(2), 1701–1732 [P5] | 通过组合分析，在“两玩家、相关并行链”和“任意多玩家、两条相同链”两个基本范围证明 fully mixed NE conjecture。 | 对标受限模型中的完整结构定理与混合均衡分析。它说明两资源/两玩家范围不自动排除强专业期刊，但所处理的是具体已有猜想，不能以对象数量判断我们的贡献等价。 |
| Giannakopoulos, Noarov, Schulz, **Computing Approximate Equilibria in Weighted Congestion Games via Best-Responses**, MOR 2022, 47(1), 643–664 [P6] | 确定性多项式算法，显著改善随成本次数变化的近似保证；直接在原博弈做改善，并给出独立的精确近似 PoA 刻画。 | 对标全输入算法、新势机制和附带结构定理。一般性和可复用工具比本项目目前的多数条件接口更强。 |
| Christodoulou, Gairing, Giannakopoulos, Poças, Waldmann, **Existence and Complexity of Approximate Equilibria in Weighted Congestion Games**, MOR 2023, 48(1), 583–602 [P7] | 超常数不存在下界；将不存在结果转成决策 NP 完全性的通用 gap/circuit 机制；一般非降成本的近乎匹配规模界。 | 对标存在阈值与复杂度边界。它说明不提供一般高效构造也可能形成高水平论文；关键在定理力度和可复用机制，不能仅比较是否含算法。 |
| Giannakopoulos, Poças, **A Unifying Approximate Potential for Weighted Congestion Games**, Theory of Computing Systems 2023, 67, 855–876 [P8] | 用统一近似势函数处理一般成本、混合成本族及 PoS，恢复和改善多类已知界。 | 对标工具论文。通用框架并不自动决定更高期刊层级；本项目若写工具论文，也必须展示真实的新适用范围和改进。 |
| Christodoulou, Gairing, Giannakopoulos, Spirakis, **The Price of Stability of Weighted Congestion Games**, SICOMP 2019, 48(5), 1544–1582 [P9] | 几乎闭合巨大 PoS 缺口的指数下界、多个博弈类扩展，以及一般近似势与上界。 | 上限对标：主题和工具相关，但结论覆盖和机制通用性较大。不能从“同为加权均衡与尖锐常数”推断本项目现稿已达到同等贡献。 |

## Interpretation：我们现有贡献与合理投稿档位

| 本项目结果包 | 实际贡献身份 | 编辑判断 |
| --- | --- | --- |
| `SC-PHI-E/A`，配合已知下界与五地点复杂度细化 | 两设施、共同目录的普遍 φ 上界；精确独立客户均衡续局与位多项式算法。φ 下界属于早期文献，不能列为我们的首次发现。五地点困难性细化固定目录规模，不能将早已存在的“φ 以下 NP 难”重命名为首次结果。 | 最完整、最适合先写稿。Algorithmica/TEAC/SIDMA 是严肃目标；MOR 是有理由的冲刺；当前不能据此称 SICOMP 录用希望大。 |
| `HC-2` 与 `SPARSE-RHO-ALL` | 异构双目录的因子 2 和单交叠条件下的尖锐 ρ=2cos(π/7)，形成不同限制下的结构边界；`HC-2` 当前仍为内部候选。 | 完成候选的作者级复核并统一机制后，可考虑同一组强专业期刊。不要把几个限制下的常数表自动当成一般理论。 |
| `SC-K-2-E` | 任意显式设施数、共同目录的常数 2 存在性；在轨站内均匀、离轨纯精确客户 NE。没有一般位多项式构造，也没有全模型的尖锐 2 下界。 | 比近期局部修补更有独立论文核心价值。TEAC/MOR/SIDMA 值得考虑；投 Algorithmica 时需突出构造机制并诚实解释复杂度边界。它与 φ 算法谁“更强”，取决于一般性、机制和稿件，不能只按设施数排序。 |
| 近期条件接口、星形/路径/固定参数子类、特定优先规则反例 | 扩充可算子类或排除指定路线；全输入的在轨选择仍未提供。 | 可作论文支撑材料。目前不足以可靠给出独立的同层级投稿建议；需要汇成清楚的新结构定理或参数化算法贡献。 |
| 尚未完成的全输入位多项式因子 2 算法 | 任意 k 与正有理权，联合选布局、精确客户 NE、兼容所有设施偏离的完整续局；证明输出表示、步数及位长。 | 一旦完成，MOR/TEAC/Algorithmica 会成为更强的目标；若选择机制可迁移到其他多阶段博弈，SICOMP 可认真冲刺。算法还未得到，不能计入当前成果价值。 |

## 2025 博士论文：本轮新增的具体优先权核查

**Paper Fact。** 本轮获取 Simon Krogmann 的 *Two-sided facility location games* (2025)，官方 DOI `10.25932/publishup-69272` [P10]。阅读范围是模型/贡献表、原子客户 Chapter 4（重点 §§4.3、4.5）、§6.2 的开放问题，并定向检索全文近似上界关键词；对印刷 pp.49、52（PDF pp.57、60）做了图像核对。没有全面重新审查其所有定理或全文所有引用。

- 印刷 p.48，Theorem 4.14 保留 φ 以下不存在的下界。
- 印刷 p.49，Observation 4.15 仍陈述 k 倍上界；Theorem 4.16 是 α∈[1,φ) 的 NP 完全性。
- 印刷 p.52，§4.5 仍把加权 φ 近似 SPE 存在性列为开放；它也指出等权构造的迭代多项式界未知。
- 印刷 p.71，§6.2 继续列出两阶段字典序势的收敛复杂度等开放问题。

**Interpretation。** 此次核查没有发现该论文相关章节已经给出我们的共同目录双设施 φ 上界算法、全 k 共同目录常数 2 定理或全输入位多项式因子 2 算法。该事实消除了此前“未能获取这份具体后续文献”的检索障碍，但不是全面优先权认证，也不能用作者的开放问题直接证明我们的成果新颖或正确。共同目录只是原文一般异构限制模型的一个范围；本项目两项结果没有解决原文全范围的 φ 猜想。

可复核检索记录：官方 PDF 共 98 页，2026-10-05 获取，SHA256 `150e907413e6be6a6842cfbd17679aa53d6608b102c7047f2b442968730e1613`。PDF 作为公开外部阅读材料，不重新分发进本仓库。

## 两周研讨会的价值门槛

两周投入值得用于把两项主证明学透、由人类独立重构关键机制，并决定先形成哪一篇稿件。最接近的论文在两阶段势函数、均衡选取、锐性或困难性之间形成完整故事；人类团队应检验我们是否也有这样一条可以清楚讲出来的主线。

近期反例和条件接口的学习只需覆盖会影响主定理或研究决策的几项。研讨之后应能区分：可以进入投稿打磨的已完成结果，仍需核心算法突破的目标，以及尚无足够独立价值的技术附属。理论发表潜力和企业落地价值分开评价；本轮文献对标没有提供现实部署、数据验证或使用者需求的证据。

## 一手来源与阅读精度

- **[P1]** [IJCAI 2024 正式论文](https://www.ijcai.org/proceedings/2024/0315.pdf)，以及 [arXiv 作者全文](https://arxiv.org/abs/2403.03114)。核对正式版模型、Theorems 5–6、Observation 4 与结论；arXiv 元数据仍指向 IJCAI 2024，不能由未列期刊版本推断不存在期刊版本。
- **[P2]** [AAAI 2023 官方文章页](https://ojs.aaai.org/index.php/AAAI/article/view/25709)，DOI `10.1609/aaai.v37i5.25709`。核对官方摘要与发表信息。
- **[P3]** [TEAC DOI](https://doi.org/10.1145/2614687)；[作者论文表与摘要](https://ngravin.github.io/) 的 2015 TEAC 条目；[作者提供的论文稿](https://ngravin.github.io/assets/pdf/TEAC/teac_weighted-full_15.pdf)。正式 DOI 页面本轮工具未能打开，发表身份以作者论文表及 P6 的正式参考文献交叉核对。作者所挂稿的题名和文件日期与发表元数据不同，不能把它当成出版社排版版本。
- **[P4]** [Algorithmica 官方文章页](https://link.springer.com/article/10.1007/s00453-010-9449-2)，DOI `10.1007/s00453-010-9449-2`。核对摘要与正式卷页，未阅读全文重构证明。
- **[P5]** [SIDMA 官方文章页](https://epubs.siam.org/doi/abs/10.1137/22M1542635)，DOI `10.1137/22M1542635`。核对摘要、范围与正式卷页。
- **[P6]** [MOR 官方文章页](https://pubsonline.informs.org/doi/10.1287/moor.2021.1144)，DOI `10.1287/moor.2021.1144`。2021 在线发表，2022 卷期；核对摘要和卷页。
- **[P7]** [MOR 官方文章页](https://pubsonline.informs.org/doi/10.1287/moor.2022.1272)，DOI `10.1287/moor.2022.1272`。2022 在线发表，2023 卷期；核对摘要、卷页与 ICALP 2020 前身。
- **[P8]** [Theory of Computing Systems 官方文章页](https://link.springer.com/article/10.1007/s00224-023-10133-z)，DOI `10.1007/s00224-023-10133-z`。核对摘要与卷页。
- **[P9]** [SICOMP 官方文章页](https://epubs.siam.org/doi/10.1137/18M1207880)，DOI `10.1137/18M1207880`。核对摘要、卷页与贡献范围。
- **[P10]** [Krogmann 博士论文官方落地页](https://publishup.uni-potsdam.de/69272)、[官方 PDF](https://publishup.uni-potsdam.de/files/69272/krogmann_diss.pdf)、[DOI](https://doi.org/10.25932/publishup-69272)。前端网页工具失败后，经官方站点直接获取并做上述范围核查；另用 [作者所在组的官方个人页](https://hpi.de/en/friedrich26/team/phd-students/simon-krogmann/) 核对博士论文身份与 2025 后续论文目录。2025 Bakers and Millers 论文讨论同时行动和不同效用，不能当成本项目序贯原子客户算法。

本评估只将查到的具体发表记录作为证据，未检查最新 JCR/中科院分区、投稿接收率、所有前向引用或所有潜在先行结果。正式稿的优先权检索仍需按精确定理逐项完成。
