# 三篇英文论文：成文入口与写作依据

第三篇 2026-10-25 的新接续以 MOR 为投稿排版目标：已从本仓库 TEAC 源稿生成官方 INFORMS 模板的私有匿名审稿包，32 页，正文与附录合一；本仓库继续保存可审查的 TEAC 源稿/PDF 及精确数学资产。先读加权拥塞专题的 WRITING_STATE.md 与 VENUE_TEMPLATE_REVIEW_round2.md；下文的 TEAC 主投决定是上一轮历史快照。稿件仍待人类作者核验与真实投稿操作。

可复现的转换程序为 [prepare_mor.py](prepare_mor.py)：给它官方 INFORMS MOR zip 解压目录和仓库外输出目录，会生成匿名 TeX、BibTeX 及编译所需样式文件；不把 INFORMS 模板资产推入公共仓库。该程序本轮重放的 TeX SHA-256 与私有交付版完全相同。因当前本机 TeX 字体包不完整，已交付的 PDF 另按 WRITING_STATE.md 所记环境构建并逐项核验。此程序不自动完成作者核验或投稿。

本轮按主人指定结构整理既有证明，不改变各 Claim 的数学身份，也不把成文或内部审查当作新颖性与外审认证。两阶段设施客户的负载博弈与加权拥塞博弈分别定义，不能与当前顺序客户吸引主攻混用。

| 论文 | 连续稿与源码 | 固定结构、范围与证明来源 |
| --- | --- | --- |
| 共同目录双设施黄金比 | [PDF](shared_catalog/main.pdf)、[LaTeX](shared_catalog/main.tex)、[写作状态](shared_catalog/WRITING_STATE.md) | 第一节引言及模型；第二节四类精确均衡菜单、核心引理和短主定理证明。坏回应环、双锚及局部多混合证明在附录完整展开。对应 SC-PHI-E/A；[现行数学地图](../current/shared/README.md)。势修复与已有黄金比下界分别归前人。 |
| 任意设施数因子二 | [PDF](multiple_facilities/main.pdf)、[LaTeX](multiple_facilities/main.tex)、[写作状态](multiple_facilities/WRITING_STATE.md) | 第一节引言及模型；第二节字典序选择、全部转移预算、原子装箱、离轨修复与短主定理证明。对应 SC-K-2-E；[现行数学地图](../current/multi_facility/README.md)。有限构造、短显示证书与一般多项式搜索严格区分。 |
| 加权拥塞结构工具及反例族 | [TEAC审稿版PDF](../current/weighted_congestion/structural_reconstruction/structural_methods_article.pdf)、[LaTeX](../current/weighted_congestion/structural_reconstruction/structural_methods_article.tex)、[写作状态](../current/weighted_congestion/structural_reconstruction/WRITING_STATE.md)、[选刊和模板核验](../current/weighted_congestion/structural_reconstruction/VENUE_TEMPLATE_REVIEW_round2.md) | 四节：引言/模型，结构工具，全状态反例族，正向稳定及社会成本应用。先说明工具解释了什么，再由工具解决存在性增长阶问题。参数尾部和全部非法态证明保留；简单参数例不宣称数学最小。对应各独立 WC Claim；[专题地图](../current/weighted_congestion/structural_reconstruction/README.md)。 |

作者、单位及邮箱未由主人提供，正文不虚构署名。第二篇已由团队定为 **SIDMA** 主投，采用 SIAM `siamart251216` 宏包作为目标提交模板；当前可编译稿仍是通用 `amsart` 版本。第三篇经本轮讨论定为 **TEAC** 主投、SIDMA 备选，已转换 ACM `acmart` 单栏匿名审稿版；正式 production class 与真实作者元数据仍须投稿前核验。第一篇仍按自身写作状态的目标推进。没有稿件被登记为已经投稿。

## 实际拉取的开源写作 skill

来源：[haruhisa-enomoto/math-paper-skills](https://github.com/haruhisa-enomoto/math-paper-skills)，MIT；本轮使用提交 `37d0bb7d3f987b0e75e0ca108ecb0daa719f52fa`。已完整读取 `write-research-paper` 及其 exposition standard、workflow、paper-writing guide；独立表述审查使用 `read-research-paper`，英文润色遵守 `polish-math-prose` 的数学不变量。

恢复时在仓库外检出同一版本，保留四个 sibling skill 的相对目录，不把第三方 skill 或它的 Git 历史混进研究正文：

```sh
git clone https://github.com/haruhisa-enomoto/math-paper-skills.git ../math-paper-skills
git -C ../math-paper-skills checkout --detach 37d0bb7d3f987b0e75e0ca108ecb0daa719f52fa
```

当前使用 writer/reviser 工作流：主人给定的篇章安排是写作约束，不重复套用 coordinator 的初稿审批门。数学核验、独立表述审读、编译、文献核验和新颖性核验分别记录真实范围。

本轮重新拉取并固定了证明审查、整篇论文审稿和学术文字编辑工具；仓库外克隆的 URL、commit、使用范围和重建命令登记在[审查工具清单](SKILLS_AND_REVIEW_PROTOCOLS.md)。这些工具的报告只改变成文质量记录，不提升任何数学 Claim 或期刊接收概率。

## 英文范文与校准方式

采用实际论文的叙述节奏、逻辑衔接和解释密度，不复制句子，不在正文宣称由范文作者写作。

| 一手范文 | 实际阅读位置 | 在本轮成文中的用途 |
| --- | --- | --- |
| [Harks–Klimm，On the Existence of Pure Nash Equilibria in Weighted Congestion Games，MOR 2012](https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/harks/HK-MOR-2012.pdf) | 摘要p419，§§1.1–1.2 p420，Lemma 3.1证明pp422–423 | 前两篇采用先对象与精确贡献、再必要机制的叙述；反证中明确所选对象的存在性和极值条件。 |
| [Christodoulou等，Existence and Complexity of Approximate Equilibria in Weighted Congestion Games，作者稿](https://arxiv.org/pdf/2002.07466) | 摘要，§1.2，Theorem 3证明PDF pp15–16 | 第三篇先组织结构理解，再说明工具怎样导出反例及其他结论；逐项区分已有结果与新应用。 |
| [Giannakopoulos–Noarov–Schulz，Computing Approximate Equilibria in Weighted Congestion Games via Best-Responses，作者稿](https://arxiv.org/pdf/1810.12806) | 摘要及引言，Lemma 3证明PDF p9，Theorem 4证明PDF p18 | 结构定理与应用分层；证明先给足够完成任务的局部义务，再展开公式推导。 |

2026-10-23实际核对的[MOR编委页](https://pubsonline.informs.org/page/moor/editorial-board)将 Tobias Harks 列于 Game Theory。该事实只说明范文作者与期刊的关系，不表示主人已经选定MOR，也不表示编委认可本稿。

## 构建、检查与接续

从仓库根运行：

```sh
python3 research/manuscripts/build.py shared multiple congestion
python3 research/build_catalog.py --check
python3 research/check_active_research.py
python3 research/check_assets.py
```

构建依赖已有 TeX Live、latexmk、BibTeX；第三篇还依赖 ACM `acmart` class 和 `ACM-Reference-Format.bst`（生产版应由 ACM/CTAN 获取）。脚本将中间文件置于各稿 `.build/`，可从已安装文件重建缺失的 format；PDF仅在编译和未定义引用检查通过后更新。第三篇本次排版预览使用仓库外固定 v2.20 tag 的测试 class，真实限制和来源见本稿选刊核验。

各稿 `WRITING_STATE.md` 保存实际版本、正文/附录边界、已发生的检查及未决项。当前审查汇总见[成文核验](MANUSCRIPT_REVIEW.md)。下一轮应先读这些精确记录，再读论文；不要把旧审查当作覆盖新版本，也不要为成文目的擅自增加数学结果。
