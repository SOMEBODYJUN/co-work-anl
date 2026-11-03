# 可信惩罚、净缺口与真实查询行的冻结证据

本包对应Boss7本次13个已指定来源版本，全部原件按原`research/...`路径保存在[original](original/)，双冻结commit/path、blob、size和SHA见[source-manifest.json](source-manifest.json)。同字节双定位记一次来源，不是两次独立验证。

本包支撑三个自足正文：

- [可信惩罚的共同目录闭包与影子租金账](../../../state/审查/可信惩罚的共同目录闭包与影子租金账--审查.md)：构造所需BANK、共同目录闭包、同共享鞍点SIGNED/RENT和首次离轨拼合；跨枝付款未证。
- [最小净缺口与冻结指派的单策略锥压力](../../../state/程序/最小净缺口与冻结指派的单策略锥压力--程序.md)：完整MIN-NET39型负原始点和WEAK-Q浮点−0.2；没有精确最优上界或普遍结论。
- [真实查询行的完整树与根自由有限探针](../../../state/程序/真实查询行的完整树与根自由有限探针--程序.md)：精确全树BI、两锥的理性范围/恢复非负缺口，以及三named原分数报告。

## 实际核读范围

| 组 | 主源ID | 全读内容 |
|---|---|---|
| credible三稿 | c06e1bf0c264f222eb43、bed77faef0327047183d、8e4636756822195dc0cf | 入口1982B、构造6583B、影子账6699B全部段落/公式/停止点 |
| MIN-NET | 8b272cbf7ebb2571c473、ba927fc3db4af6fae727 | 4717B全部代码分支；559092B全部26根字段、39型、完整4681动作和全部附带字段 |
| direct四源 | 9c59647d5a2498c278b5、dfef5084cabecf00ee33、25c5ccc85c3313a9e4ca、593fe1df578b0bc6300c | 1225B入口、3093/3255/3278B全部源码/主入口、全根与根自由差异 |
| weak assignment | 0bb34a3d989e693aac4d、9823e13a1816e6297535 | 3278B全部源码和889B全部JSON字段，含重复比较调用coverage_row的实际合同 |
| named tree | 3f432dba3584132d7a90、649e5c0cf63cf4d1d607 | 4917B全部源码及3398B三报告每字段/完整根向量/最坏比较 |

大JSON以逐项语义解析完整消费，未只读大小/名称或实际路径。[pressure-complete-field-index.json](pressure-complete-field-index.json)保全部非策略字段和39型，并以完整有序层无损编码全部动作，能按深度与lex索引还原原数组；[source-inspection.json](source-inspection.json)逐JSON遍历所有标量、记录完整类型化叶流摘要及源码AST函数/导入清单。原JSON完整保留，是最终可复用证据，索引不是其数学替代。

当前静态核检查13份原字节size/SHA、Python可解析性、全部4681历史键域/动作范围/数组顺序、与旧repeated完整strategy逐值同；新endpoint与旧endpoint不同。named三输入也逐SHA匹配，并消费客户和全部有序动作键域。详[named-input-bindings.json](named-input-bindings.json)。这些检查不计算新收益、IC或最优值，不把它们称为独立数学认证。

## 运行及依赖的真实边界

本轮原源码import、main/CLI、LP/MILP、BI、SPE/oracle、收益/IC重放、原600/861扫描均为0。仅新增标准库[inspect_sources.py](inspect_sources.py)执行一次完成静态源/数据盘点；它显式不导入任何冻结模块。该次检查的临时输入根按代码原样保存，未来复核应依manifest指定实际根重新定位，不把它当数学求解器。无网络、Git、认证、认领、提交或发布动作。

原报告中的4681/32767、80/37440/55980比较、精确利润与秒数是冻结源报告及源码接受链的历史内容，不是本轮新事件。MIN-NET具有`cone.verify`非负/全Γ检查及canonical/direct精确验收路径，但没有带符号目标的精确对偶；WEAK-Q只有float−0.2和`exact_primal=false`，原件没有任何positive candidate。两ROW cone的分数接受只检查Γw≥0及正gap，遗漏显式w≥0；当前没有阳性文件，不制造失效证书。named脚本没有main guard，**导入会执行并覆盖报告**；本轮只读/AST，从未导入。

[dependency-manifest.json](dependency-manifest.json)绑定既有规范四模块、20567B helper与四个旧实际输入。它们已在仓库其它证据包保存，原字节不重复复制或代done；当前只读取相关helper函数、旧输入消费字段，未冒四规范模块本轮全读。若以后明确重放，应在一个隔离根中按各项`original_path`复建依赖，再把本包原`research/...`树放到同一根。只拷平单个脚本不满足其`parents[5]`、旧输入相对路径和规范导入布局。

helper的`coverage_row`用求和位mask、未对重复槽取set，且WEAK-Q传全部有重复比较；例(0,0,0,0,0)会产生mask5而非mask1。互异目标01256本身正确，重复alternative的每条最优性行则不可直接当真实覆盖。[dependency-helper-binding.json](dependency-helper-binding.json)保精确函数AST和SHA。这是软件范围核对，不是新搜索/原正证书纠错。

原件README的两个跨本批导航不改字节：[direct原主稿](../direct-general-and-terminal-interface-two-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/direct/direct_general_working.md)和[前缀核原审查](../terminal-wallet-fresh-reserve-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/credible/prefix_kernel_review_and_dedup.md)已在其它包精确保存，依赖清单给hash。旧原文的局部相对链接不因选择性保存13源自动在本`original/`子树内闭合；正式三正文和本说明的链接均指实际目标。这两条是导航寻址，不冒本批新primary或对导航原件的全文重读。

## 当前数学状态与关系证据

完整银行原族已否精确逐人门槛/EI/Mfull等过强合同；它不否MIN-NET、净ROW或本WEAK-Q。另一个UV最优前缀变分/固定链乘子障碍有不同量词，不移作这13源的反证。五人half当前已有别证，六人及各共同付款接口分别保留状态。

[comparison-bindings.json](comparison-bindings.json)绑定本次实际全文比较的12篇正式数学及其SHA/范围；[relation-evidence.json](relation-evidence.json)按同控制器必要IC、同账改写、旧拼合、同策略不同点、程序实现、不同接受合同分别解释联系。没有把链接列表自动升为推导，正式超图留第三阶段逐边审读。

逐源13条receipt和copy-plan由父方串行发布；这份stage不表示已checkpoint、pushed或done。正文完整保留原独有数学、候选与具体缺口，不以原来源自报或结构字段代替实质整理。
