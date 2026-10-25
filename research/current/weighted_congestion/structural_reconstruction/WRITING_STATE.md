# 加权拥塞结构论文：成稿状态

本轮任务是按主人已给定的叙事与章节安排整理现有结果。基线提交为 `69e6012bd585e1e1b53b7535a1cff661fe35a855`；现行正文为 `structural_methods_article.tex`，参考文献为同名 `.bib`，PDF 为同名 `.pdf`。本轮没有改变既有命题的对象、假设、量词或结论，也未新立数学成果身份。

## 已锁定的写作安排

1. **Introduction**：先介绍局部费用与全局稳定性的结构问题及工具用途，再交代它与原文公开问题的关系；模型与记号留在本节。
2. **Structural tools for approximate stability**：共同玩家尺度、端点与面积、双排序与环一致性、权深度、稳定核实现。每个接口有用途与必要解释，不仅排列正式命题。
3. **All-state counterexamples from finite windows**：实际参数、玩家和资源集合放入正文；短主证明调用第二节工具及附录估计。给出 `n=2, d=2^21` 的一个明确成员，再给近次数族及通用门槛的渐近结论。不称该成员最小。
4. **Applications to stable states and social optimization**：实际小份额的正向存在、势与社会费用正则化、社会外部性预算、稳定集上的精确选择。详细相位计算、同次数修复和统一尾部检查放附录。

摘要132词，遵循“结构理解与工具→正向用途→反例应用及原问题”的顺序。章数是四个主节；附录承载完整技术证明。

## 已实际采用的 skill 与文风样本

读取开源仓库 `haruhisa-enomoto/math-paper-skills` 的 `write-research-paper/SKILL.md`、`references/exposition-standard.md`、`references/workflow.md`、完整 `references/paper-writing.md`；润色时另读 `polish-math-prose/SKILL.md` 与 `references/anti-patterns.md`。

实际读过的一手英文样本：

- Christodoulou--Gairing--Giannakopoulos--Poças--Waldmann, *Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*, arXiv:2002.07466v3：Abstract、Introduction、§1.2、Theorem 3 proof（作者稿PDF页15–16）、§7。采用的特点是先精确说明结果相对已知界的位置，再说明工具的独立用途；证明由对象和需证义务起步。
- Giannakopoulos--Noarov--Schulz, *Computing Approximate Equilibria in Weighted Congestion Games via Best-Responses*, arXiv:1810.12806v6：Abstract、Introduction、Lemma 3 proof（PDF页9）、Theorem 4 proof（PDF页18–19）。采用的特点是先将论证缩成明确不等式，再顺序给出代入、单调性和有界性理由。

上述是对所读具体段落的节奏、解释密度和连接方式的学习。没有复制其独特句子，没有声称由原作者撰写，也没有将其他模型的数学结论移入本文。

## 真实数学来源与归属

- 本轮成文以基线完整 `.tex` 为直接可复用来源，核对本专题八份正文的对应结构与数学身份：`endpoint_area_principle.md`、`shared_scale_gluing.md`、`instance_interval_calibration.md`、`repair_and_core_transfer.md`、`socially_descending_repair.md`、`parameterized_allstate_family.md`、`additive_near_degree_lower_bound.md`、`weight_depth_threshold.md`。原有详细审查记录的适用版本与范围不被本轮整理改写。
- 一般 `d` 存在上界归于 Caragiannis--Fanelli，未冒称本文原创。
- CGGPW 的下界及 §7 的差距问题已从其作者稿核对；本文只声称给出该差距的渐近解答，没有声称所有有限 `d` 的精确门槛均已确定。
- `n=2,d=2^21` 是现有统一族的明示代入，不是寻找最少玩家/资源后的最优反例。

## 已完成的检查

- 原稿24个正式 theorem/lemma/proposition/corollary 的陈述逐字保留。
- 原稿120个 label 全部保留；无重复 label；正文引用均有目标。
- 原稿22个 proof 环境中21个逐字保留；仅共同尺度引理的证明改写为连贯英文，公式与理由保持不变。另给统一族和近次数定理补上显式短 proof。
- `latexmk` 实际编译成功，26页；最终 LaTeX log 无错误、未定义引用/文献、重号、Overfull 或 Underfull 提示。BibTeX 正常。
- 作者自查覆盖摘要、叙事、首次出现、章节衔接与证明依赖；它不是新的独立盲审或外部同行评审。

## 未决项

主人尚未在本轮为该篇指定唯一投稿期刊，故保留现有 `article` 类与暂用参考文献格式，不能称为目标期刊最终版式。作者、单位、通讯信息未获指定，未擅自填入。完整独立新稿审读、外部审稿与新颖性认证仍各自独立；本次编译与编辑检查不替代它们。

下一步：统一三稿的目标期刊/文风记录，再对本次变动做独立数学diff核验和完整新稿审读；修改时保持四章结构及全部既有数学范围。


## 主agent最终接续记录

最终交付以[三稿核验汇总](../../../manuscripts/MANUSCRIPT_REVIEW.md)中的版本和真实覆盖为准。统一构建脚本已实际成功运行；PDF总页数保持25/8/26，已渲染检查全部页面的排版概览。
独立diff检查已确认24个正式命题不变、21/22旧proof逐字不变，验证显式参数例；最终回执未完成。依已确认观察澄清base-game相位对称性、subsection范围及构造的位置引用。新稿隔离editorial没有完成报告，不能登记通过。
当前源码SHA-256：`f6f65fd53db59261933663ca08cbf042e2cc0eb8d93cfe66b2138b0212d9af0f`。当前PDF SHA-256：`ee30c135b9825353328ed1ff3ad5f9757bfe9fce8065982b9b99e1121f29c7d8`。最终期刊未定，当前为成文稿而非某刊最终提交包。

## 2026-10-25 第三篇完整成稿闭环（进行中）

已按第一轮五项 S4 修订正文并重编译；`REVISION-NOTES.md` 记录逐项范围。以上旧哈希是上一冻结版本的历史快照，不代表本节修订版。独立证明、整篇编辑及期刊/模板复核正在进行；本轮审查报告和最终构建核验形成后才可将状态改为完成。没有改变二十四项正式命题的数学身份。作者信息仍待真实提供。

本轮当前冻结 TeX SHA-256 `cae8ff1b075640c0c5f5baed35f04585246b6319e11adb0c5c7da2d38505f461`，TEAC 单栏审稿版 PDF SHA-256 `24a28ad9d27a4e6903375a487c2e8d480384885c1c94b616ebd378b43e51687a`，27页。独立数学攻击及修订差分无 S0–S3，具体范围见 `REFEREE_REPORT_round2.md`；最终严格冻结的整篇表述读者尚在审读。`acmart` 测试类不等于ACM/CTAN生产包，官方模板复编译、TEAC门户特殊规定与作者元数据仍是投稿前项目。研究结论身份不变。

整篇非冻结反馈后的局部修订现为 TeX SHA-256 `38ea3d15412a71edee62b21363c157d3d863ef5528e2a4fd0b83a54cba70456c`、PDF SHA-256 `a832f998f06f625ee806e8e4439d291f3932b5a15206fc7bbd815e3ff03e9429`，27页；上段哈希标识的是其修复前的严格冻结读本。类名、线性证书记号和三句重复/未定义术语修复已通过独立定向数学回归。严格冻结编辑审读的完整意见尚待归档。

## 本轮闭环结果

最终 TeX SHA-256 `3ee2db7cadce655e4534d27a0aa1b923ad2a05be383fe82ab8a7f781908cd847`；TEAC单栏审稿 PDF SHA-256 `33727a90d83c2300658d1bcf89355c998f435af9ba6bdc4a8ef2d0c052407256`，27页。冻结全文编辑初审的 necessity / referential-precision 原判均为 FAIL；八项局部修复均经原读者 bounded delta 验收，**本批修复簇**两项均 PASS。独立数学攻击无 S0–S3，末轮定向数学差分无新增 S0–S3。审查证据与严格边界见 `REFEREE_REPORT_round2.md`，选刊及模板限制见 `VENUE_TEMPLATE_REVIEW_round2.md`。

构建、proof-sanity、标签与文献引用检查和27页视觉概览通过。稿件仍缺真实作者资料；编译所用 v2.20 tag 为ACM模板开发仓库的测试版，正式生产类文件与TEAC门户细则要在真正投稿前再核对。外部同行评审、穷尽优先权调查及技能所述逐命题两遍tracker均未发生，不能把此次内部闭环称为已获投稿接受保证。
