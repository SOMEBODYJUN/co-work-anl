# 第二篇：任意设施数因子二存在性成文状态

当前工作：将已有 SC-K-2-E 结果检查并整理为完整英文论文。只写本目录；不修改精确 Claim、原始证明、冻结证据或其他研究线。版本基线来自本轮恢复的 main。

## 已固定的主人要求

- 独立第二篇，聚焦任意设施数的一个存在性命题，不把大量后续条件算法与选择器障碍拼成杂稿。
- 摘要先交代前人模型、已知结果及缺口，再写本文结果与方法。
- 简短 Introduction；核心引理按数学本质组织；主定理的证明调用引理而保持简短。
- 正确性先于成文包装，不把有限计算当作一般证明。
- 英文自然、清楚；本稿采用明确主语与连贯的 theorem--proof 叙事，未复制任何作者的独特句子。

## 读者、主张和结构

读者：算法博弈论、拥塞博弈与组合优化研究者；假定熟悉 Nash equilibrium、独立混合策略、lexicographic order，不假定读过内部研究记录。

确切主张：任意 k≥2、有限非空共同地点目录、正实权原子客户、强制覆盖服务、线性实际负载成本和独立随机化模型中，存在纯设施布局和一整套精确客户 NE 续局，任意设施的单方换址收益不超过原来的两倍。在轨可用选地点后同址均匀随机，全部离轨可选纯续局。

结构：第一节 Introduction/模型；第二节依次给字典序选择、客户最优性、全部转移预算、允许独立重原子的装箱、严格纯改善保持上界、全部偏离构造和短主定理证明。末尾有限证书命题只说明显式有理输入可有限构造、显示策略短且可核验；没有多项式时间搜索主张。

## 来源与归属

主证明来源：`research/current/multi_facility/model.md`、`uniform_two.md`。逐项边界和独立内部攻击来源：`reverse_review.md`、`research/reviews/facility/arbitrary_facility_factor_two.md`、分支 `claims.md`。这些源文件未修改。

一手文献：实际打开并核对 Krogmann--Lenzner--Skopalik--Uetz--Vos，arXiv:2403.03114v2，§1.1 模型、§3 等权存在、Theorem 5 黄金比下界、Observation 4 的 k 保证、§6 猜想。正文只精确转述这些结果，不复刻前人证明，也不把已发表社会福利 PoA=2 当作稳定性因子二。

平方负载势是本客户子博弈的标准有限改善机制，不单独宣称其原创。新增结果主体是已有仓库 SC-K-2-E 的共同目录转移预算、装箱和精确续局组合；本轮仅成文，不提升数学状态。

## 未决事项

- 主人尚未指定这篇的最终期刊。`amsart` 为可编译成文稿，最终 publisher class、参考文献格式及字数需随期刊决定再落地。
- 作者名单、单位、邮箱未提供，全部留空。
- 文献优先权与外部同行审查未完成；本轮公开版本检查不等于全面新颖性确认。
- 正文的独立连续阅读及全篇审稿本轮尚未由本写作者执行；自查不能代替独立审查。

## 自查与产物

初稿自查重点：原子自己的完整权重；字典序优化域不限于客户 NE；源地点消失时的 J∩C_t 和 J∩C_r；客户端重原子隔离；所有完整带标签续局兼容性；真实零覆盖与空集合；证书紧凑与搜索复杂度的区别。自查未发现存活的致命异议。

实际编译：已生成 `main.pdf`，8页。最终 `main.log` 无 LaTeX error、warning、undefined reference/citation 或 overfull box；labels无重复、所有 ref/eqref均有定义。摘要138词。

环境原有 `pdflatex` 命令但默认format/字体映射不可发现；在本目录被git忽略的 `.build/` 用已安装的TeX源码生成本地format、组合既有CM/AMS映射后编译，未改变数学公式、页边距或分页。长标题的 `amsart` 页眉最初溢出，已提供相同题意的短页眉标题并重新编译，最终日志干净。

自查版本 `main.tex` SHA-256：`ceb6cb53b7bcb18fcce4bc7c7fbdea4f7cb85890c0215e81f0b6707a3c9f0dbe`；PDF SHA-256：`5f6b0ee953d803f4d6ad7e23c3e5a9c629d00099d6fe4a965afcab426bd10d13`。这是写作者自查及构建证据，不等于独立全文审查。主agent统一进行仓库入口维护、最终独立检查、commit/push。

## 本轮实际范文校准与审查修正

实际读过 Harks--Klimm，*On the Existence of Pure Nash Equilibria in Weighted Congestion Games*，MOR 37(3), 419--436 (2012)，作者公开PDF `https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/harks/HK-MOR-2012.pdf`：摘要p.419、§1.1--1.2 p.420、Lemma 3.1完整证明pp.422--423。采用这些段落中明确对象、先主结论后机制、先交代所需义务再推导的写法，不复刻独特句子，也不声称模拟整个作者风格。详细范围见 [REVISION-NOTES](REVISION-NOTES.md)。

校准仅改摘要/Introduction/定理引理前后叙述；结构、显示公式、编号与关键证明不变。另按主agent转来的两项非致命审查意见，明确在轨仅“every covered client”随机选择，以及编码证明中每个负载分母的额外至多k因子和 `O(log k)` 位长。七段proof只有最后编码proof的上述分母说明变动，其他六段逐字保留。审查原报告及后续delta由主agent保存；这里不是新的独立PASS。

当前最终稿实际编译为8页，摘要132词；最终日志无warning/error/undefined reference或citation/overfull。默认latexmk的outdir与BibTeX路径在本环境发生混读，最终改为独立 `.build/final/` 中按 pdflatex--BibTeX--pdflatex--pdflatex 顺序完成，检查成功后原子替换阅读PDF。

当前 `main.tex` SHA-256：`c8bfa0d94aaf22a732338fba5b1cc9216ba878329c62ddca04f485858240172a`；当前PDF SHA-256：`f96440de8ba4ebfefcee5c7aa5bc8bb1d073e826a2d383732eebb03e73adf65c`。本轮没有改任何精确Claim的身份或状态。


## 主agent最终接续记录

最终交付以[三稿核验汇总](../MANUSCRIPT_REVIEW.md)中的版本和真实覆盖为准。统一构建脚本已实际成功运行；PDF总页数保持25/8/26，已渲染检查全部页面的排版概览。
独立数学检查及两项精度修正的bounded delta已通过。隔离editorial原判必要性PASS、指称精度FAIL；3项发现均已逐项修正：Case2明确打包原客户与新增客户之并，默认规则固定客户枚举，依赖引用改为具体引理编号。主agent复核修复，不冒称另一次隔离审读已PASS。
当前源码SHA-256：`04190ddf297500eb24af37280b1dc61f9f6ce5d06f88065f755a85c93deb2e10`。当前PDF SHA-256：`22a9be2ddbcff76b8c03f2209cf3a7c2e51316e45b27b0df9c256006cf4a23de`。最终期刊未定，当前为成文稿而非某刊最终提交包。
