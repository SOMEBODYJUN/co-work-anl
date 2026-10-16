# 加权拥塞线性门槛主稿的贡献、证明重构与成稿核查

## 对象、版本与证据层级

本记录审查[自足英文主稿](../../current/weighted_congestion/linear_threshold_article.tex)、[实际PDF](../../current/weighted_congestion/linear_threshold_article.pdf)及[参考文献](../../current/weighted_congestion/linear_threshold_references.bib)。最终TeX SHA256为 `f06b65a42ee6c69a69b0e8fd00295da92532b4e4ac8458124ecf2f7b507523e7`；PDF SHA256为 `29e4daf4cfa57b26037a238afb330acba1925f6d20904b7ef5b050fe68b36647`。

主稿是既有内部已审数学结果的面向读者重构，不新增或改写Claim。数学源为 `6fea2ee6b5117033eb3b522853f18a31cf396c6f` 的 [完整否定证明](../../current/weighted_congestion/linear_degree_allstate_lower_bound.md)，SHA256 `04181c4d5c09fb85ac84270e06743571e156a8334611943aa5f6b865f9409c33`；整数次数证明来自 `365425de2fb53e38c62e31b950ca2f43ee86dc3c` 的[独立审查补节](ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)。原规范正文的字节及四个Claim身份均不变。

两名此前参与数学审查的内部研究者首次通读本TeX。一人从本稿自身重建资源和前沿证明，检查是否必须依赖仓库中未写出的段落；另一人逐式对照规范证明、整数预算及文献定理适用条件。另一路独立审查贡献定位与直接文献。主研究者汇集并核查所有修改，编译、逐页检查最终产物。本记录不是外部匿名同行评审，也不是全球优先权或期刊录用判断。

## 贡献与证明落点

| 稿内对象 | 精确作用与来源 | 审查结论 |
| --- | --- | --- |
| Theorem 1.1 | `WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`：每整数d≥2^20，正有理权、正有理纯d次费用、二个非空不交动作、全部状态真实margin≥(2^d−d/10)/8 | 构造与全部状态证明自足；未以环代替非存在 |
| Lemma 3.1 | `WC-CLASS-FRONT-ALLSTATE-COMPILER-v1` 的同类宽N≥3特例；全前沿出口加全态成本cap，经同权三元资源扩成全态出口 | 真实单人修复及原费用保留均写出；没有泛化到所有改善环 |
| Lemmas 4.1–4.2 | 健康输入的标量闭环和全态费用cap | 这是规范辅助构造中主证明所需的部分；主稿未宣称重证整个双扫环Claim |
| Proposition 5.1、Lemmas 5.2–5.4 | `WC-HEALTHY-FRONT-COVERAGE-v1`：全部异步相位的保前沿出口 | 基体扭转、backward r+1、短差累计和return parity完整；新增时钟未被错误地要求扭转对称 |
| Lemma 6.1 | 同次数CLOCK预算的整数分层证明 | 归纳恒等式及严格号保持；实际新增费用取p次 |
| Corollary 6.2 | `WC-MATCHING-LOG-UPPER-NEGATIVE-v1`及其直接o(d)推论 | 否定量词、零偏离成本和strict/weak号正确 |
| Corollary 6.3 | 新下界结合CF既有d近似势定理得a_*(d)=Theta(d) | 明确列作文献上界的应用，未把上界归为本文贡献；非精确常数 |

文章的主要论证是显式线性全状态下界及其原次数实现。增长阶和对数保证否定是推论。稿件没有为增加篇幅并入旧势障碍、有限小反例或尚未建立的新复杂性机制。

## 已处理的问题

1. 原稿末尾的 `large strategy sets` 易与每人恰二策略混淆，改为 `strategies containing many resources`。
2. 在首次预算估计之前明确heavy为区分用户、light为窗口用户；类在不同测试中可有不同角色。
3. 标量证明先由Y≤2^(−p)X确立L>0，再使用H/L，不再让读者等待后文补正分母符号。
4. CF的正费用单项式表述与本模型空策略/零项/常数项的衔接已明确：先固定具有恒零费用策略的玩家；这些玩家仅用恒零资源，不影响剩余正费用负载。然后拆正次数项，常数a0改成每玩家私有费用(a0/w_i)x，使用时负载恰w_i；合并同像动作。保留全部真实成本及偏离，次数≤d。全零情形直接有精确均衡。
5. 删除末尾重复的机制总结，保留真正影响范围的权类、权比、资源束大小、常数和构造规模问题。PDF没有孤立的单条参考文献页。

最终修订后的完整重构复核绑定上述最终TeX hash：未发现数学漂移、缺失的承重证明或尚成立的fatal objection。审核者没有将稿件页数当作贡献证据。

## 文献与计算核查

两条引用均已按一手来源人工核对作者、标题、卷期、页码、年份与DOI。CF为JCSS 117:40–48 (2021)，DOI `10.1016/j.jcss.2020.10.007`，v5 Theorem 2给d近似势；CGGPW为MOR 48(1):583–602 (2023)，DOI `10.1287/moor.2022.1272`，在线发表于2022年，v3 Theorem 1和第7节提供正文引用的旧下界及gap。主稿没有宣称穷尽文献或世界首次。

实际运行 `check_references.py linear_threshold_references.bib --strict`，两个条目均通过、无warning/error。在线Crossref检查的CF条目成功，MOR请求返回HTTP 429；因此未把在线检查记为全部通过。MOR条目另由出版商正式页面直接核验。服务限流没有元数据真值含义。

[独立多项式费用拆项审计](../../../tests/audits/weighted_congestion/linear_threshold_article_cost_split.py)及[冻结结果](../../../evidence/runs/weighted_congestion/linear_threshold_article_cost_split.json)检查全零、常数和混合多项式三类小输入，包括空动作、不同策略族、零项删除和同像动作合并。使用Fraction，枚举所有所列状态和真实偏离，验证所有玩家费用逐项保真；没有用有限计算证明一般上界。结果记录的是当时工作稿hash `fb2592ce1246be14b5d66af4d991f4a1e79ac7a8732fbe6a061238fc682528da`，不是最终TeX hash；核验对象仅为拆项与私有常数资源的费用恒等式。稿内恒零策略预处理另由直接论证与最终全文审读核查，不归入这份有限计算的覆盖。

一般费用保真由私有资源占用时成本恒为a0的代数以及正次数拆项的逐资源加和承担。引用CF一般定理的全部证明不在本稿重证，也不被有限拆项测试替代。

## 实际编译、阅读与版面覆盖

实际编译环境为pdfTeX/TeX Live，BibTeX生成参考文献，最终两次编译无未定义引用、缺失字形、overfull或underfull诊断。系统提供TeX源树但没有预生成format/font map，本轮仅在临时目录重建格式与字体映射。全部实际命令、环境、源/产物hash以及普通完整TeX Live下的复现命令均见[冻结编译记录](../../../evidence/runs/weighted_congestion/linear_threshold_article_build.json)。

最终PDF共10页。使用系统Poppler以105dpi渲染，逐页视觉检查1–10页；另对全部页面的文本边界、页码、交叉引用及字体诊断做程序检查。主定理完整置于第2页，核心前沿覆盖在第7–8页，同次数主证明在第9页，推论、范围及两条参考文献在第10页。无裁切、叠字、未解析引用或孤立参考文献页。

这份产物已经是可以连续阅读的自足主论文草稿，区别于一页贡献计划或仅有推论的摘要。发表价值仍需外部新颖性核查与专家评审；本记录不保证具体期刊档次、录用或最优常数。
