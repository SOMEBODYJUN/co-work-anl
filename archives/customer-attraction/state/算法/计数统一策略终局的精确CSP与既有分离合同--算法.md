---
id: customer-attraction/count-uniform-terminal-target-csp-and-known-separation-record
kind: algorithm
type_tag: 算法
title: 计数统一策略终局的精确CSP与既有分离合同
status: 6164B原算法与720B已知例记录全读；有限CSP必要充分性重构；不重复既有分离穷尽
truth_status: exact-fixed-input-count-policy-realization-decision-not-general-purification
review_level: full-code-and-canonical-dependency-reading-existing-exact-obstruction-reused
scope: 固定有限单位客户实例、正人数与共同标签目录、指定完整SPE终局计数；只决定计数统一动作SPE的可实现性
summary: 每计数态选择一个全局终局目标，父子关系存在最佳动作；GAC仅逐关系精确，DFS解决共享孩子依赖。已知三人五题023不可实现及最差22428/22429分离复用成熟证明，不据本记录伪造默认80案例运行。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/count_policy_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/known_markov_obstruction_replay.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/count_policy_probe.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/parent/known_markov_obstruction_replay.json
---

# 计数统一策略终局的精确CSP与既有分离合同

6164B原代码及720B记录均完整保全，[证据包](../../tools/evidence/d398-parent-diagnostics-primary/README.md)绑定原件和规范model/exact依赖。它是指定实例的有限决策算法；不假定所有完整历史SPE都可净化成计数策略。已有[严格分离反例](../反例/完整历史与计数统一策略的严格分离--反例.md)已经否定一般净化，本代码提供不同于特定三人末层穷尽的通用CSP实现。

## 两类策略与变量域

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)的单位客户均分收益，p个共同标签、m≥1位单位玩家。程序接口保同覆盖标签、空题、重复和离轨弱平局。计数统一策略要求动作φ(s)只依先前标签计数s；一般完整策略可在同计数不同有序历史选不同动作。

先用规范ExactSPESolver算每个 \(|s|\le m\) 的**完整历史SPE终局集合**R(s)。这一步缓存整个集合，允许一般历史依赖；不是先求一份Markov策略。为每个s设终局目标变量

\[
 Q_s\in R(s),\qquad |s|=m\Rightarrow Q_s=s.
\]

对指定根目标t再固定Q₀=t。若t不在R(0)，realize直接返回None；主CLI只遍历R(0)中的t，因此其分离分支有完整历史可实现性前提。

每个非终端s和所有孩子s+e_b之间施加一条有限关系：

\[
 \exists a:\quad Q_s=Q_{s+e_a},\qquad
 U_a(Q_s)\ge U_b(Q_{s+e_b})\quad\forall b. \tag{C}
\]

U_b是固定终局一名选b玩家的真实均分收益，相关孩子中b一定已经选择，分母正。

## 必要充分性及为何要全局搜索

若φ是计数统一完整SPE，把每个s按φ继续的终局记Q_s；它属于R(s)，规定行动使父目标等于该孩子目标，全部真实偏离恰给(C)。故任一实现都会给此CSP全局赋值。

反向，给满足全部(C)的全局赋值，为每个s任选其见证a。按剩余深度归纳：末层Q_s=s；若更深φ均实现各自Q，父所选孩子目标等Q_s，故父真实终局也Q_s。关系中的收益比较因此是每个计数s的真实IC。提升到所有有序历史h，令σ(h)=φ(count(h))，得到完整纯SPE并实现根t。此证明保每个离轨历史，不只实际路径。于是算法精确决定该固定输入/目标的计数统一实现；有限并不意味着一般净化成立。

propagate做广义弧一致性。给各变量当前域D_s，对每个可能父目标q和可选a，先要求q∈D_(s+e_a)，再检查

\[
 U_a(q)\ge\max_b\min_{t\in D_{s+e_b}}U_b(t). \tag{P}
\]

对单条关系，各非规定孩子的目标可分别选择，因此(P)恰等价于存在相容孩子赋值。父q和规定孩子q得到支持；其他孩子b保全部满足 \(U_b(t)\le U_a(q)\) 的目标。遍历所有q/a并取支持并集，删无支持值；各域单调缩小，至固定点或空域。

不同父关系会共享同一个孩子变量，单条关系各有支持并不保证全局能同时选取。DFS因此选择域大小>1最小的变量（再按深度、计数破平局），枚举其目标并递归传播；不能把GAC尚非空当作可实现。有限域保证完整DFS终止且不漏赋值。若全域单例，(C)给每个s至少一个真实见证动作。

成功后源码还从**每个计数态**正向沿φ走到m，重算终局并检查全部行动的真实IC，确认根目标。它不调用规范完整证书验证器代替这个检查。visited/rejected在同一实例对象多次realize之间累计，不是每个目标自动重置；历史统计需有具体驱动才能解释。

## CLI与真正保存的已知例不同

CLI默认cases80、players4、topics4、seed20261023。每次所有非空兴趣型质量从[0,0,1,1,2,3,4]抽取，整数重数仍是不同单位客户。对每个输入遍历全部完整SPE根终局，逐目标决定count实现。若失败，输出EXACT_SEPARATION及完整实例、目标和规范full_certificate；若全部通过，输出finite_no_separation、所请求参数、目标数、累计DFS及耗时。前者只在完整DFS未被中断时有穷尽意义；后者只限实际有限输入，不证明任何全称等价。

只有指定output才写JSON；代码有main guard。导入规范model/exact及Fraction，无NumPy/SciPy或LP依赖。它使用solver的私有_outcomes枚举全部计数态，故版本须绑定，不能只按类名认为兼容。

known_markov_obstruction_replay.json**不是**上述main的输出schema：没有CLI参数、完整实例或full_certificate，却有source、exact_unsat、all_markov_roots、两福利值及DFS100/rejections2。它自称已知例的独立实现重放，未提供该驱动/argv，不能回填成默认80例m4/p4运行，也不把100节点/2拒绝当本轮复现数。

## 已知精确分离的来源去向

记录指向R-18旧markov_obstruction_report，目标
\(t=(1,0,1,1,0)\)，即三主题023。其六个计数统一根支持为014、024、034、124、134、234；完整历史另可达023。完整最低福利22428，计数统一最低22429，strict差1。

这些数值/全部六向量与成熟[三人五主题24831客户反例](../反例/完整历史与计数统一策略的严格分离--反例.md)逐项相同。那里已给完整31动作、严格fresh/repeat界、648末层映射和130776第二层穷尽，足以证明目标确不可计数统一实现和最差福利严格分离。720B新记录不含这份全部输入/穷尽表，故复用现有自足证明，不另造同反例或以100节点计数替代严格排除。

本轮检查仅完整消费known JSON全部字段、将六向量/目标/福利与该已证对象比较；原CSP main、随机80例和已知DFS重放均0次。源码关系的必要充分性由上述证明重构，不以未给的历史驱动证明普遍算法正确，也不新增外审/盲审/新颖性身份。

后续可用这个精确CSP测试一个明确新整数输入/目标，成功时提升并直接核完整树，失败时保实例、完整SPE目标证书及可重放DFS参数。它不支持把计数子类的优化阴性当所有完整SPE阴性，也没有给一般六人half或固定p的效率常数。
