---
id: "unrelated-machines/svensson-2011-restricted-assignment-configuration-gap"
kind: "resource"
type_tag: "资源"
title: "Santa Claus 调度与受限指派配置界"
status: "retained-literature-read-directly"
truth_status: "literature-source-proof; finite-local-search-and-polynomial-estimation-distinguished"
review_level: "full-22-page-text-read; critical-formula-pages-rendered"
summary: "Svensson arXiv:1011.1168v2 的受限指派配置LP间隙33/17、两尺寸5/3+δ、阻塞树与对偶摊还证明；多项式估值不等于多项式输出实际调度。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/svensson_2011_santa_claus_schedules_v2.pdf#pp.1-22"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/svensson_2011_santa_claus_schedules_v2.pdf#pp.1-22"
source_id: "b5f626d440f2f30bf0b3"
source_sha256: "e80d2b787fd0d594361e3eaedc1272a418c02d81b5c1e1fa06a81a688fab43c3"
source_blob: "00dd4e299080de27ad2cb379a72d40e5b16a03e2"
source_size_bytes: 471434
---

# Santa Claus 调度与受限指派配置界

## 来源身份和读取范围

冻结PDF为 Ola Svensson 的 *Santa Claus Schedules Jobs on Unrelated Machines*，共22页，没有另附未读附录。首页侧栏标注 arXiv:1011.1168v2、2011-03-21，而标题下内部日期为2018-10-23；这两个可见标记如实并存，不据文件名抹平版本差异。两冻结提交共享上述blob与SHA-256。

本批读取了全文1203行文本，包括Section 2配置LP/对偶、Section 3两尺寸算法与全部证明、Section 4一般尺寸算法与Claims 4.7–4.8、Lemmas 4.6/4.9、结论和参考文献；对PDF第1、9、12、15、17–19、21页另外渲染核对公式、分类端点和版本标记。下文是可接续的文献资源说明，来源内证明、来源引用的外部定理和本批独立核验范围分开。

## 模型、配置LP及量词

有限机器集合 \(M\)、作业集合 \(J\)。作业 \(j\) 有非负公共尺寸 \(p_j\)，以及可用机器集合 \(\Gamma(j)\)；在可用机器上处理时间均为 \(p_j\)，其它端为 \(\infty\)。每作业完整分配给一台可用机器，最小化最大机器总负载。这是 **restricted assignment**，不是任意有限端具有不同 \(p_{ij}\) 的一般不相关机器。

给定阈值 \(T\)，机器 \(i\) 的配置族为

\[
 \mathcal C(i,T)=\{C\subseteq J: i\in\Gamma(j)\ (j\in C),\ \sum_{j\in C}p_j\le T\}.
\]

原文[C-LP]采用“每机器至多一个配置、每作业至少覆盖一次”的非负变量形式：

\[
 \sum_{C\in\mathcal C(i,T)}x_{iC}\le1,
 \qquad
 \sum_i\sum_{C\ni j}x_{iC}\ge1,
 \qquad x\ge0.
\]

空配置补足机器总权、向下封闭配置删去作业多余覆盖后，与[现有定义](../定义/不相关机器与两个调度松弛--定义.md)的恰等式形式等价。令 \(T_{\rm conf}\) 为最小可行阈值，整数调度直接给LP可行点，故 \(T_{\rm conf}\le\mathrm{OPT}\)。原文对正阈值按 \(T_{\rm conf}=1\) 归一化；零尺寸作业可先任取可用端安排，空作业或全部尺寸零返回零峰，不用除以零。若某作业无可用端，则是不可行输入，不能套用有限最优值保证。

归一化后的对偶可写为

\[
 \min\Big(\sum_i y_i-\sum_j z_j\Big),\qquad
 y_i\ge\sum_{j\in C}z_j\quad(C\in\mathcal C(i,1)),\qquad y,z\ge0.
\]

若存在对偶可行点满足 \(\sum_i y_i<\sum_j z_j\)，沿正射线缩放即无界，反证原始可行性。文中把对偶分离联系到每机器一个背包问题，并调用已有的尺寸舍入/近似求解获得任意精度；这里**没有**把精确背包分离当成免费多项式oracle，也未独立重证该外部LP算法。

## 可引用的结论与真实输出合同

- **Theorem 4.1，PDF第11页：** 对所有上述restricted-assignment实例，配置LP整数间隙至多 \(33/17\)，即正阈值下 \(\mathrm{OPT}\le(33/17)T_{\rm conf}\)。这是整数调度的存在性上界，不是一个间隙达到该数的下界实例。
- **Theorem 1.1，PDF第2页：** 对每个固定精度 \(\eta>0\)，可在多项式时间估计最优makespan，因子 \(33/17+\eta\)。这结合近似求LP值与上述间隙；\(\eta\) 不是作业尺寸，也不是机器数相关余量。
- **Theorem 3.1，PDF第4页：** 尺寸只取 \(\{\delta,1\}\)、\(\delta\ge0\) 时，配置LP间隙至多 \(5/3+\delta\)。其中非平凡次二范围是 \(\delta<1/3\)；不要把尺寸参数 \(\delta\) 与任意精度 \(\eta\) 混用。

原文给出最终能找到相应实际调度的局部搜索，但只证明有限终止，**未证明其多项式收敛**。因此这份来源不能承担一般输入的多项式 \(33/17\)-近似输出算法，更不能承担本存档一般矩阵、确定性总位多项式、实际分配的 \(2-\varepsilon\) 主目标。文中关于历史最佳算法/硬度的比较是该版本背景，不作为本批已经穷尽当前文献的结论。

## 两尺寸证明：阻塞树、对偶和有限签名

Section 3先令 \(R=2/3+\delta\)，目标负载为 \(1+R\)。正尺寸的非平凡范围保持每机器至多一件size-1大作业；每次从一个合法部分调度开始，尝试安排新作业 \(j_{\rm new}\)。阻塞树 \(\mathcal T\) 同时有父子关系及按加入时间排序的线性次序，根只记新作业、不附机器。

小阻塞机器集合 \(M_S\) 禁止所有新入作业，大阻塞机器集合 \(M_B\) 只禁止新入大作业。令 \(S_i\) 为机器 \(i\) 上所有除当前机器之外的可用端都已在 \(M_S\) 中的小作业。潜在小移动只要求目标不在 \(M_S\)；潜在大移动还要求目标未入树且 \(p(S_i)\le R\)，并按目标是否已有大作业区分big-to-small/big-to-big。

立即合法移动优先，其后依序为小移动、大到小、大到大，同类用目标负载作为必要的字典序次坐标。不能立即完成的小/大到小移动添加小阻塞点，记目标上待移作业；大到大移动只把目标上大作业记入大阻塞点。执行合法移动后，删除包含被移动作业的阻塞点及所有较晚点，以释放过时禁止条件。每作业只属一个阻塞点、每机器至多小/大各一阻塞点。

若没有潜在移动，定义大阻塞作业 \(z_j=2/3\)，树内或被困小作业 \(z_j=p_j=\delta\)，其余0；小阻塞机器 \(y_i=1\)，其它机器取当前已排作业的 \(z\) 总和。对偶可行性的关键是：小阻塞机器容量1直接控制任意配置；其它机器没有未被计入的小作业能移入，大作业在单位配置中单独出现；无树标记的机器若拒绝大移动，则其被困小负载已大于 \(R\)。

负目标值并非逐机器一律 \(z\)-负载至少1：由小移动产生的小阻塞机器负载至少 \(4/3\)，由大到小产生者可能仅大于 \(2/3\)。后者因存在可逃逸小作业，按优先级必紧接前者，可两两摊还至至少2。于是所有小阻塞机器的总 \(z\)-负载至少其机器数；再加新作业有正 \(z\) 而尚未安排，得到 \(\sum_i y_i<\sum_j z_j\)，反证LP可行。这是Lemma 3.7/Claims 3.8–3.9的承重步骤。

终止性用阻塞点加入时移动值串成的signature，末项为 \(\infty\)。添加点严格减小字典序；删除一段后，下一个非立即合法移动的值比原首个被删点更小：负载下降，或大作业已移走使移动类型降级。至多 \(2|M|\) 个点、每点只有有限取值，所以终止（Lemma 3.10）。**有限**取值数未被证明多项式；不能从字典序下降直接写出多项式步数。

## 一般尺寸证明：三个阻塞种类和33/17摊还

Section 4令 \(R=16/17\)，始终维持负载不超过 \(1+R=33/17\)，并额外要求每机器至多一件big作业。后者不是负载界自动蕴含的条件：两件 \(11/17\) 能小于 \(33/17\)，所以这个不变量不可省。

按原文Definition 4.2的端点分类：

| 作业类别 | 尺寸范围（\(T_{\rm conf}=1\)） |
|---|---|
| small | \(p_j\le9/17\) |
| medium | \(9/17<p_j<11/17\) |
| big中的large | \(11/17\le p_j<14/17\) |
| big中的huge | \(p_j\ge14/17\) |

可行归一化实例的正作业都不大于1。除了small/big阻塞，新增medium阻塞：记目标上的medium作业，禁止medium/huge进入，但容许large进入；这是原文看似不对称而对证明必要的设计。small只不能进 \(M_S\)，medium/huge只能进未标记机器，large可进未标记或仅medium标记的机器。

令 \(S_i\) 为被困small作业，\(M_i\) 为目标上全部medium作业。huge移动分为：

- 若 \(p_j+p(S_i\cup M_i)\le1+R\)，按是否有big作业区分huge-to-small/huge-to-big。
- 若 \(p_j+p(S_i)\le1+R<p_j+p(S_i\cup M_i)\)，则huge-to-medium；这保证至少有一件medium作业可作为新阻塞。

medium/large到无big目标属于“small move”，到已有big目标则添加big阻塞。移动优先级按原文Definition 4.5为：合法 \((0,0)\)；small move \((p_j,p(L_i))\)；medium/large-to-big \((2,0)\)；huge-to-small \((3,p(L_i))\)；huge-to-big \((4,0)\)；huge-to-medium \((5,|L_i\cap J_M|)\)。这使存在small移动时优先挑尺寸最小者，为下一段定量摊还所需。

### 对偶可行性（Lemma 4.6、Claim 4.7）

若无潜在移动，树内big赋 \(z_j=11/17\)，树内medium赋 \(9/17\)，树内或被困small赋 \(p_j\)，其它0。仍令small阻塞机器 \(y_i=1\)，其它机器为当前 \(z\)-负载。

small阻塞机器因 \(z_j\le p_j\) 自动可行。其它机器按未标记、big标记、仅medium标记分三类：

1. 未标记机器不可能有树内small/medium/large作业能移入。若有huge可用却非潜在移动，\(p(S_i)>R\)；包含huge的单位配置最多有 \(11/17+(1-14/17)=14/17\) 对偶价值，比其 \(y_i\) 小。
2. big标记机器已有对偶值 \(11/17\) 的big作业；配置至多包含一件medium/big，所有正值small若能用此机器均已在该机，故可行。
3. 仅medium标记机器同理无新的正值small/large能移入。若配置含medium，由已占medium覆盖；若含huge，需证 \(y_i\ge14/17\)。有两件medium时直接成立；只有一件时，添加medium阻塞的条件给被困small与该medium真实总负载大于 \(R\)，把medium从小于 \(11/17\) 降到 \(9/17\) 最多损失 \(2/17\)，所以 \(y_i\ge R-2/17=14/17\)。

### 负目标值（Claim 4.8）

由small作业的小移动建立的small阻塞机器，其 \(z\)-负载满足

\[
 Z_i\ge\min\{27/17-p_{j_0},20/17\}\ge18/17.
\]

由medium/large的小移动建立者无big作业，至多一件medium时最多折损 \(2/17\)，又 \(p_{j_0}<14/17\)，故 \(Z_i\ge1\)；两件medium时直接 \(Z_i\ge18/17\)。

剩下huge-to-small建立者可能小于1，但其不能立即移动且 \(p_{j_0}+p(S_i\cup M_i)\le1+R\)，说明存在可逃逸small作业 \(j'\)。下一阻塞点必由尺寸不大于 \(p_{j'}\) 的small移动建立；其负载至少 \(\min\{27/17-p_{j'},20/17\}\)。与前一机器配对：两件medium时前者至少 \(18/17\)；一件medium时若 \(p_{j'}\ge7/17\) 前者至少 \(16/17\)，否则前者至少 \(14/17\)、后者至少 \(20/17\)；无medium时前者大于 \(16/17\)、后者至少 \(18/17\)。各情况配对总和至少2。

于是 \(|M_S|\le\sum_{i\in M_S}Z_i\)，而新作业尚未分配但有正 \(z\)，给出严格的 \(\sum_i y_i<\sum_j z_j\)，与配置LP可行性冲突。配对按时间相邻且第二点是small移动产生，不会把同一机器反复作为前项重用。

### 有限终止（Lemma 4.9）

仍用字典序signature。small/huge-to-small阻塞释放后目标负载严格下降；big阻塞释放后移动类型降为small/huge-to-small；medium阻塞释放后目标medium件数严格下降，因为其存续期间不能有新medium移入。每机器至多small、medium、big各一标记，故至多 \(3|M|\) 个阻塞点。有限signature严格下降，反复扩展直至全部作业安排，证明 \(33/17\) 间隙。来源没有将这些signature数量控制成多项式。

## 比较、版本区别及接续用途

已实读比较[不相关机器与两个调度松弛](../定义/不相关机器与两个调度松弛--定义.md)、[AFS五分之一文献](Santa-Claus超图匹配与配置LP五分之一界--资源.md)、[BLMRS资源](圣诞老人遇到Makespan与拟阵--资源.md)、[私有菜单树配置界](../定理/私有菜单树有界叶重数配置界--定理.md)的注入合同和Haxell证明，以及[入口与文献状态](../资料/不相关机研究入口与文献状态--资料.md)。

- 本文把AFS的交替搜索/签名思路用于**最小化**受限调度，增加负载敏感的阻塞类型和对偶摊还；这是来源明确的方法启发关系，不能把max-min配置阈值方向照搬到makespan。
- 第2页及参考文献[1]（PDF第21页）说AFS作者页面有 \(1/4\) 改进，而仓库本批冻结AFS作者稿实际写 \(1/5\)。本页仅记录Svensson引用的另一个版本说明，没有取得其 \(1/4\) 原稿，不能覆盖AFS冻结源的 \(1/5\) 数学正文或宣称独立核验 \(1/4\)。
- 私有菜单树对象的 \(5/3\) 界依赖叶单射/私有树结构，本文的 \(5/3+\delta\) 依赖受限指派的两种作业尺寸。相同数值不构成两者的推导边，也不使两模型等价。
- BLMRS给一般Santa Claus与Makespan之间的条件归约及两值/拟阵域结果；本文只给restricted assignment的配置间隙。引用两者必须逐一核对域、方向、求值和实际输出，不把文献拼接成一般UM严格次二算法。
- 原文结论提醒：取消公共尺寸限制时，配置LP即使每作业至多两可用机器也可有趋二间隙（其引用[19]）。这是本文中的外部文献陈述；精确构造应到Verschae–Wiese冻结源逐读，本文不冒称重证。

本源处置为 retained：独有的 \(33/17\) 与两尺寸 \(5/3+\delta\) 结果、完整阻塞类别、对偶价格、关键配对不等式、有限签名终止和估值/输出差别都保存在这里。开放的多项式舍入和版本背景保持开放/引用身份。本页不提供六人共同目录完整历史纯SPE的证明或反例，也不将经典文献的未定问题状态当成2026年的最新结论。
