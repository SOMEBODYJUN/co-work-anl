---
id: customer-attraction/padding-blind-driver-terminal-count-and-ordered-path-boundary
kind: program
type_tag: 程序
title: P填充独立重建驱动的计数终局与顺序边界
status: complete-source-and-import-semantics-review; original-output-not-supplied
truth_status: exact-count-question-defined; no-new-existence-result-or-ordered-strategy-certificate
review_level: full-983-byte-driver-and-25475-byte-actual-import-closure-read
scope: 六共同标签ABTDEP、整数k≥1、k+3名单位提供者；规范集合值逆向归纳的终局计数存在性
summary: 完整还原八兴趣型、目标计数与五个首动作孩子最小值；明确不强制P^k AAB、不输出全树证书或安全值，且blind名称不认证独立实现或读序。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/independent_attack/padding_blind.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/independent_attack/padding_blind.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/independent_attack/README.md
---

## 全部输入与单位客户解释

原`padding_blind.py`共983B，全文只有导入、game(k)、run(k)和main guard。它构造共同标签顺序(A,B,T,D,E,P)，人数m=k+3，每个兴趣型的整数重数是这么多名**不同单位客户**，不是一名可加权客户：

|位掩码|兴趣标签|单位客户数|
|---:|---|---:|
|1|A|4|
|2|B|4|
|4|T|2|
|12|T,D|2|
|20|T,E|2|
|25|A,D,E|6|
|26|B,D,E|2|
|32|P|5k|

前七型共22人，P独立5k人。规范CustomerType要求重数为正整数，故此构造对整数k≥1合法；k=0保留P重数0而会在构造时拒绝，负k同样不合法。不能以主问题允许零客户为由把这段固定非零输入代码扩成零客户实例。命令行仅`run(int(sys.argv[1]))`，没有默认k、范围检查、超时、批量循环、argparse或结果输出参数；缺argv/非整数字符串会在进入求解前报错。

固定目标终局计数

\[
q=(2,1,0,0,0,k),\qquad \sum_aq_a=k+3.
\]

从输入可直接算出：若实现q，则两名A各得4/2+6/2=5，一名B得4+2=6，k名P各得5；覆盖W=5k+16。所有客户共5k+22且四个合法主题A,B,T,P已覆盖全部，m≥4允许填重复，故OPTₘ=5k+22。因此这个**条件终局**有2W−OPTₘ=5k+10>0。上述代数不需要求解器，不证明q真能实现；也没有从文件名推断它是half反例。

## 规范求解器的真实语义

驱动导入Instance、CustomerType、ExactSPESolver。已逐字全文阅读实际规范包`__init__.py`691B、`model.py`8640B、`exact.py`9943B和`certificate.py`6201B，共25475B，并核原PROVENANCE的源ID/SHA。全部实际导入依赖保[证据](../../tools/evidence/independent-padding-attack-entry-and-driver-two-primary/README.md)；没有用不同版本或只读函数摘要代源码。`Fraction`、`json`虽在驱动导入，但其名称未被使用；精确有理算术来自规范model/exact本身。

对历史计数c、每个行动a，令R(c+eₐ)为该孩子可由某完整历史纯SPE实现的终局计数全集，并置

\[
\ell_a(c)=\min_{z\in R(c+e_a)}U_a(z),\qquad
L(c)=\max_a\ell_a(c),
\]
\[
R(c)=\bigcup_a\{z\in R(c+e_a):U_a(z)\ge L(c)\}.
\]

终端R(c)={c}。当前节点可选择实现保留目标的孩子，其他有序孩子分别选使当前行动者收益最小的子SPE；不同孩子后代互不相交，可同时拼接。逆向归纳必要性来自当前行动必须压住所有离轨孩子的实际收益。完整证明和展开算法已有[终局全集对象](../算法/完整历史纯SPE终局全集--算法.md)，本处只明确驱动实际消费哪项接口。计数缓存相同的是**可实现终局集合**，不要求同计数的不同有序历史采用相同策略。

因此`q in s.outcomes()`若完成返回True，确切含义是：存在某份完整历史纯SPE，根终局计数为q。它既不是只检查末位均衡，也不是认证某个给定作者控制器。若返回False，否定的是这个精确输入下的该终局计数存在性；不得扩成任意padding方案或一般half失败。

## 终局计数没有固定P^k AAB顺序

q不记录各玩家的行动顺序。程序未向`certificate(..., on_path=...)`传入P^k AAB，也未调用`ordered_outcomes()`、生成完整动作映射或调用定义级verify_certificate。故即使有True，也只能认证**某个顺序**可实现；不能单凭计数存在性说前k人全P、随后AAB，不能把两名A、一名B的5,5,6支付依此分给指定时点玩家。

如果要另认证指定完整在轨序列，规范接口还须在每个该序列前缀强制下一指定行动，并确认该目标属于对应孩子且其收益达到L(c)，再逐有序孩子展开策略、定义级核全部真实后继。父目录名“独立”或代码docstring的blind有限重建不是这几步已经发生的证据。本清洗没有补运行来制造缺失结果。

## 五个首动作孩子打印了什么

run(k)建立g、s和q后先打印`k ... start`。完成根`outcomes()`后打印k、target布尔值及`s.stats`（计数状态、终局状态、累计保留终局项）；这些是缓存求解器统计，不是完整有序历史数、SPE策略总数或激励检查总数。根求解已递归消费所有行动孩子，随后读取孩子通常使用已有缓存。

接着a=0,…,4，即A/B/T/D/E，分别做：

1. b=eₐ，把该首动作已选一次作为合法过去；`r=s.outcomes(b)`返回该子博弈的全部可实现终局计数。
2. 对每个t∈r求`s._utility(t,a)`，即首位选择a者在该终局的最终收益；取v为最小值。因为t含已选a，收益分母为正；它不是这个子博弈新行动者的保证值。
3. 收集所有达到v的终局，再只打印`choices[:12]`及`str(v)`。r为frozenset，未排序，前12不是规范的有序见证表，片段不能恢复全部极小值实现；整数元组哈希的迭代顺序也没有跨环境的输出顺序合同。

这五个v是在**五个不同首动作孩子**中分别可实现的惩罚值。该循环没有打印首P孩子、没有固定其后P^(k−1)AAB、没有显式比较目标P利润5与这五个v，也没有交付所有孩子的一份共同完整动作证书。独立孩子的最小值可以用于规范递推的拼接充分性，但数值片段本身不提供指定目标首P分支的实现。根目标计数查询与这些诊断是两个真实不同的问题。

所有打印均flush=True，只有stdout而无写JSON结果文件。run最终返回feasible布尔值，但main直接调用且不将返回值传给sys.exit；正常结束时无论True或False都不会据此返回非零退出状态。因此即使另有一次进程exit0，也不能从退出码推出target=True，必须读该次真实输出。

## 作者全k构造、旧桥和独立性身份

必要related的10930B`all_k_padding.md`已正常全文读，其相同八型和q却进一步给全k的**指定P^k AAB完整策略**：有限激活模式处理非饱和核心，饱和核心全部未来查询即时≤5后全P，其他受上界保护节点用默认集合值BI。驱动没有实现这些模式，不认证作者默认分支守卫；“规范求解器有相同终局”也不等于该特定模式正确。作者另述k1/5/10有限成功属其报告时态，当前两primary没有那些输出或证书，不冒本驱动已在这些k跑过或通过。

该全k作者稿针对实际分数负载的辅助桥取α=(m−1)/m、M=max_TΣₓ∈T1/(1+αcₓ)、G=Σcₓ>0 1/(1+αcₓ)，此族M=6，声称mM≤W+G恰从k≥10失败；逐人更强式从k≥9失败。它同时有真正静态vₘ≤5，W−mvₘ≥1。因此不是入口所攻击强安全聚合桥的反例。驱动根本不计算α、M、G、vₘ、安全原始/对偶证书、福利或OPT；本正文的条件计数代数没有变成其实际输出字段。

已比较[既有实际负载税桥反例](../反例/实际均匀缩放负载的弱付款桥--反例.md)：其旧十三人36客户、W33/OPT36与本输入k10的W66/OPT72数值不同。即使有成比例客户族，也不能挪旧27243节点/18675决策/112050激励数作为本983B驱动的输出或把不同作者控制器的18669决策/112014比较视为同一运行。1697B复制遗漏失败related则是另一扩张族：形式低覆盖路径在真实末两位置有Dⱼ偏离7>5，不能靠换平局认证目标。两related primary由Boss7处置，本包不代其done。

## 原布局、执行合同和清洗处置

`ROOT=Path(__file__).resolve().parents[5]`仅在原research/workspaces/customer-attraction/R731/independent_attack的嵌套布局指向仓库根，随后`sys.path.insert(0,...)`导入根包。原字节移入tools/evidence后不会自动成为自包含可执行文件；不能原地import来探测，main guard只阻止run，不阻止路径修改和规范包导入。欲重建旧布局应另用隔离目录放原driver与配套包，未在本轮执行。

当前两原件没有stdout冻结文件、JSON结果、退出码记录、k扫描范围、完整策略或失败证书。0新数学运行、0原代码import；AST解析/JSON解析/源SHA和链接检查仅为包验证。本源retained为程序资源与完整原件，入口见[独立工作台资源](../资源/独立全局攻击入口的安全桥均匀接口与文献范围--资源.md)；不创建第二份规范求解器算法或虚构新均衡结果。第三阶段可据真实消费关系建立驱动→规范集合递推、终局计数问题→原族输入、缺失指定顺序认证等关系，本阶段不机械造边。
