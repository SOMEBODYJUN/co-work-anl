# 本地数学草稿选择性补录

本轮用户明确授权：审查这49份、约342MiB本地文件后，只补数学有用内容。本批没有推送先前包含全部载荷的本地提交，也没有删除本地原件。

原49份共358,389,000字节；接收19份原样Python草稿，共34,269字节。27份临时数据/网页逐字节证实为既有完整源的严格前缀；2份模板/身份文件无数学增量；1份缺陷派生脚本吸收纠错后不复制。逐项指纹、完整源定位、理由见[review.json](review.json)。

这些是待清洗来源，不是正式知识正文；不把浮点LP、条件证书、有限随机搜索或不完整列域当作普遍六人证明或原模型反例。

## 数学内容与限制

|原编号|原路径|可接续内容及限制|
|---|---|---|
|1|[diagnose_mixed.py](raw/diagnose_mixed.py)|固定路径的混合单例LP余量诊断；依赖test_mixed_singleton_lp3.py，只是所设行族/列域的数值探索。|
|2|[lp_all_R.py](raw/lp_all_R.py)|七标签六人行族的数值可行性探针；末尾名义R行只有正incidence项，不能当作已证明的真实偏离不等式。|
|3|[lp_private_domain.py](raw/lp_private_domain.py)|比较全部、前四位单例覆盖、非遗漏单例已覆盖三个限制域；float LP，不是一般结论。|
|4|[mixed_search.py](raw/mixed_search.py)|七主题单例与双重incidence随机搜索；调用既有全SPE结局递推，有限样本不证定理。|
|5|[private_search.py](raw/private_search.py)|七个不相交主题客户块的随机搜索；单位客户重数编码，有限样本。|
|10|[research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/m6_direct_lp.py](raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/m6_direct_lp.py)|混合系数、末位/尾二人/直接偏离行和省略标签排序行的探索；route只检查覆盖位蕴含标签，未编码完整策略树。|
|11|[research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/m6_private_lp.py](raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/m6_private_lp.py)|private/shared弱行与排序约束的浮点余量探索；正/负数值均需精确和语义核验。|
|12|[research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/m6_requery_lp.py](raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/m6_requery_lp.py)|带多层重查询phi枚举的候选行族；phi合法性未在本次证明，不能从优化器结果推出原模型结论。|
|13|[research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/mixed_private_probe.py](raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/mixed_private_probe.py)|给定路径、允许单例标签域的条件探针；共享行及路径一致性必须后续核对。|
|14|[research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/s6_private_early/lp_extend.py](raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/s6_private_early/lp_extend.py)|单例只在早期/倒数第二位/未覆盖等列域的对照；mode 1/2/4/5在此实现相同，不能算四份独立证据。|
|15|[research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/symmetric_private_lp.py](raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/symmetric_private_lp.py)|重查询行按部分对称组限制乘子的探索；硬编码原工作区绝对路径，移植时须显式修复，不是可直接运行的独立工具。|
|33|[resid_singletons.py](raw/resid_singletons.py)|既有dense乘子在单例列的精确余项诊断；与既有mixed_singleton_condition正文常数对应，保留短诊断实现便于复核。|
|34|[search5_tmp.py](raw/search5_tmp.py)|五主题六人随机搜索驱动；依赖既有全SPE递推，有限随机实验，不是完备搜索。|
|35|[search_disjoint_tmp.py](raw/search_disjoint_tmp.py)|不相交主题的全有序历史结局递推与有限整数域搜索；独立短实现，有复核价值；终局结局集本身不等于完整策略证书。|
|36|[test_mixed_singleton_lp.py](raw/test_mixed_singleton_lp.py)|七标签混合单例、末位/尾二人行的数值与有理重构检查；只检其列域，行的模型适用性仍须独立论证。|
|37|[test_mixed_singleton_lp2.py](raw/test_mixed_singleton_lp2.py)|固定route限制域下U/OPT6两个目标的探针；目标分支使用(cov-1)/2，须核对与预期W-OPT/2是否一致，不能照名称引用。|
|38|[test_mixed_singleton_lp3.py](raw/test_mixed_singleton_lp3.py)|在前项基础上排除部分未覆盖单例列；同有目标系数审查义务，是额外条件下的探索。|
|40|[verify_candidate.py](raw/verify_candidate.py)|已覆盖单例限制域上的LP解有理重构；检查多个分母，未固化求解器输出，不单独成立为精确证书。|
|41|[verify_simple.py](raw/verify_simple.py)|固定有理乘子逐列核验；本次4059列最小余项54012438388289/984516162149520，负列0。条件包含被选最优中相应单例已覆盖，原模型行合法性和归约条件另审，非普遍六人证明。|

## 发现的具体错误与精确检查

`tmp_k.py`不是通过的证书：代码`0b11011`与“前四位”注释不一致；原样运行在`(I,E,J)=(2,16,16)`得到`-1/30`并抛断言。没有将其报为新结论。正确前四位版本已在原冻结来源：`research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/s6_private_early/audit_private_early.py`及`private_early_condition.md`。

`verify_simple.py`原样精确检查4059列，无负余项，最小余项`54012438388289/984516162149520`。这是其指定条件列域内的系数检查，合法行来源、主题归约和可适用子类还需第二阶段整理。`resid_singletons.py`得到的负单例余项与既有`mixed_singleton_condition.md`的常数相符。实际输出见[checks.json](checks.json)。

## 依赖与复现

原文件保留原字节及原相对层次，不默改数学。NumPy/SciPy用于多数LP；`diagnose_mixed.py`读取同层`test_mixed_singleton_lp3.py`；三个随机搜索驱动导入原仓库`tests/audits/customer_attraction_search.py`。该既有依赖在原冻结来源，可用原源clone根目录作为PYTHONPATH后接续。`symmetric_private_lp.py`有原工作区绝对路径，需另作记录清楚的移植，不能声称本批已修复。

本批只运行checks.json记录的三个短小精确枚举，没有启动大规模随机搜索、LP全扫描或将未留输出的实验算为已验证。19份均经AST解析；未见网络/消息发送代码或凭据模式。
