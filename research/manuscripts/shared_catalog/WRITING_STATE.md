# 第一篇写作状态：双设施共同目录

## 当前版本与锁定范围

- 源资产恢复提交：`69e6012bd585e1e1b53b7535a1cff661fe35a855`。
- 本稿身份：SC-PHI-E / SC-PHI-A 的英文成文；不新增或提升数学Claim。
- 主人指定的叙事已落实：前人模型和未解问题 → 本文共同目录双设施φ存在与构造；Introduction含精确定义 → 核心菜单与实质引理 → 短主定理证明。四类菜单不拆成多篇结果。
- 正实权重用于存在性；正二进制有理权重和显式覆盖表用于位多项式构造；设施共用同一目录、允许同址、客户强制参与、独立混合、全部有标签布局上的精确续局选择，均保留原量词。
- 不包括实例最优倍率、NP困难性、稀疏目录阶梯或EPTAS候选；不把局部纯修复势函数作为设施存在性的新发明。
- 不填写未经授权的姓名、单位、邮箱或署名。

## 数学来源及正文映射

| 来源 | 本稿中的作用 |
| --- | --- |
| `research/current/shared/model.md` | Definition 1.1、条件费用、精确客户NE及完整续局量词 |
| `research/current/shared/theorems.md` | SC-PHI-E/A 的存在和复杂度分离 |
| `research/current/shared/proof.md` | 固定菜单、完整目录d值、坏回应环、全局依赖链 |
| `research/current/shared/heavy_pairs.md` | 附录A中重原子容量、同对禁边、三角排除；参考现行逐式重写而不只保留旧节号 |
| `research/current/shared/star_anchors.md` | 附录A中共同重客户、唯一运输、双锚覆盖、星形和空/单对的全部分支 |
| `research/current/shared/local_chord_full.md` | Lemma 2.2 及附录B/C；保留任意多人独立混合、坏正差和坏负差、端点交换与位长 |
| `research/current/shared/algorithm.md` | P/E/T/C菜单在d之前固定、全目录搜索、最终证书及复杂度 |
| `history/source/manuscripts/shared_phi/main.tex` | 完整英文数学论证的直接改写底稿；保留其全部主定理必要证明，改正硬编码节号，删除重复流程语言 |

## 归属核对

已打开一手原文核对：

- Krogmann、Lenzner、Skopalik、Uetz、Vos，IJCAI 2024，`https://arxiv.org/html/2403.03114v2`，§1.1、Theorem 5、§6：原子模型、黄金比下界及开放猜想。下界归原作者；本稿不复刻其构造。
- Vos，2023年硕士论文，`https://essay.utwente.nl/96484/1/Vos_MA_EEMCS.pdf`，Lemma 29、§8.3：受保护纯修复和相关双锚重叠思路。不能将该论文称为博士论文。
- 主定理不是“新势函数直接证明存在性”：平方负载势用于客户纯修复；全局结果来自固定有限菜单与闭环/双锚排除。多项式时间另外依赖端点交换的移动数界。

本轮没有进行穷尽新颖性核查，也不以历史评审代替新稿独立审读。

## 作者自查与实际构建

- 已完整阅读数学写作skill的SKILL、exposition standard、workflow及paper-writing guide；采用写作者流程，没有启动要求额外审批的多模型relay。
- 自查了完整目录d值与环内归一化的区别、有限菜单最小值与全部NE最小值的区别、P修复守卫、C的实际覆盖条件、全部NE唯一性的严格支配论证、离轨续局的有标签不冲突。
- 主定理只调用菜单覆盖引理和已证的局部默认续局；菜单覆盖在附录A独立完成反证。局部强弦只依赖客户模型与附录B/C，不依赖全局φ结论。首边计算可供任意大对族使用；后面的空对/单对选择不被用来证明首边，因此没有该方向的循环依赖。
- 摘要120个空白分隔英文词；LaTeX交叉引用无未定义项、无重复label。删除了全部旧硬编码内部节号。
- 已实际构建25页PDF。最终日志没有LaTeX错误、未定义引用、overfull/underfull或其他warning。初次失败是本机缺失format和TeX文件数据库；复用第二篇目录的本地pdflatex格式并显式设置TeX输入/字体/BST搜索路径后构建成功。此环境恢复不涉及论文数学结论。
- 最终TeX SHA256：`6aaa893eeab3f818fdfee71819830e4880bee66365a077a4d66c092190ec4c3e`。
- 最终PDF SHA256：`65e383808a3184bbd8dc76a9c25c1003a9073353ab949ed0f45d3166afffe984`。

## 未决事项与接续

1. 目标期刊未确定，当前使用`amsart`通用数学稿；不得声称已经采用某刊最终投稿模板。
2. 已完成下述公开样本的局部英文校准；它不意味着已完成隔离全文审读或目标期刊的版式转换。
3. 当前检查是作者源稿核对和自查，尚不是对这个新排版版本的隔离连续阅读或独立数学审查。下一步应冻结本稿后给独立读者检查，并保持数学身份不变。
4. 主agent负责同轮统一索引、研究资产登记、commit与push；本agent未提交或推送。


## 有实际范文依据的英文校准

已实际打开并阅读 Tobias Harks、Max Klimm，*On the Existence of Pure Nash Equilibria in Weighted Congestion Games*，*Mathematics of Operations Research* 37(3) (2012), 419–436，作者公开PDF：
`https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/harks/HK-MOR-2012.pdf`。

具体样本是印刷p.419的Abstract、p.420的§§1.1–1.2，以及pp.422–423的Lemma 3.1及其完整证明。标定只取这些段落可观察的组织方式：先给精确对象和结论；技巧按两个实际数学机制展开；反证中先交代所选对象存在、极值及正性何以成立，再用明确连接词推进。不复制其独特句子或导入其数学结果；没有为纯文风参照增加正文数学引用。

本次实际改动位置：摘要（120词）；Introduction的研究对象和既有结果段；§1.2的两机制与归属段；§2开头；Lemma 2.2之前；Construction 2.3之前；Lemma 2.4前后；Theorem 2.5证明。核心覆盖引理后的说明现在明确交代有限映射保证有环、零最大值已经给见证，因此坏环的最大d值可正归一化。只是把附录已有理由提前解释，没有改变证明义务。

润色前版本保留在本地`.build/pre-style-main.tex`供差分审计，SHA256为`c712665b5136b472f5dac525494ef50a8d9206fc7cbcfbf1a5acf72f4a58d8bd`。已机械逐字比较：所有display数学、Definition/Lemma/Theorem/Construction完整正式陈述、label顺序及section/subsection结构均保持原样。附录证明未改。复编译仍25页、零error/undefined/warning/overfull/underfull；这只是锁内英文改写与构建证据，独立数学audit由主agent另行安排。


## 主agent最终接续记录

Round-1 isolated referee findings were repaired in REVISION-NOTES.md:
the false equal-reach quota sentence was removed, the large-pair chord now
states its no-witness scope, the common-\(h\) reach-order implication and
fixed-largest-client invariant are explicit, and the polynomial constructor
has an ordered branch table. The revised source is not yet independently
passed; a targeted re-review and clean build are required before delivery.

最终交付以[三稿核验汇总](../MANUSCRIPT_REVIEW.md)中的版本和真实覆盖为准。统一构建脚本已实际成功运行；PDF总页数保持25/8/26，已渲染检查全部页面的排版概览。
独立数学检查者已完整读冻结初稿并发回无已确认致命异议的阶段报告，但最终审查回执未完成。隔离editorial审读因工作区额度错误中断，未产生可验收报告。不得登记独立全文审查通过。
当前源码SHA-256：`6aaa893eeab3f818fdfee71819830e4880bee66365a077a4d66c092190ec4c3e`。当前PDF SHA-256：`c9b1deb3bd400142626c12e6cba0aa8665226f058d06c89506e99125763c19c5`。最终期刊未定，当前为成文稿而非某刊最终提交包。
