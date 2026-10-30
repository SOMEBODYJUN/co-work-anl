---
id: "customer-attraction/actual-extra-query-and-last-probe-scope"
kind: "computation"
type_tag: "计算"
title: "实际终局查询与LAST探针的核验范围"
status: "one-positive-exact-replay-and-two-numerical-probes-preserved"
summary: "原终局查询程序只对明确十一客户输入重放一次，完整报告字节相同；两份LAST探针全文核接口并保全依赖，不把浮点值、固定锥搜索或阴性输出当普遍证据。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/actual_extra_candidate_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/actual_extra_candidate_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security/probe_last.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/security/last_cone_attack.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/exchange/README.md"
---

# 实际终局查询与LAST探针的核验范围

## 三个程序针对不同对象

| 程序及源ID | 实际对象 | 本轮处置 |
|---|---|---|
| actual_extra_candidate_probe.py，a9288235052e5e03c122 | 固定完整SPE终局负载c的m max_T F_c(T)−W；规范精确求解器枚举可实现终局计数 | 全文读取；只对明确的十一客户正例运行一次原代码，重建并核完整证书 |
| probe_last.py，4f7f0b7c5113d769a72f | 已存策略的实际末前背景b，计算单阻挡minimax M_b的数值LP | 全文读取并保全；未重新扫描旧输入，没有把打印的数值当精确证书 |
| last_cone_attack.py，8b75653bc03d252658e6 | 固定完整动作图的精确激励锥中，交替优化查询分布与客户重数，尝试mM_b>W | 全文读取并核数学接口及恢复边界；未重跑旧阴性搜索 |

前一候选已被[三人十一客户例](../反例/实际终局额外查询的三人反例--反例.md)否定；后两程序针对的[LAST](../候选/实际末前背景的聚合安全值--候选.md)仍须按其自身定义判断，不能因三个文件在相邻工作区就合并其真值。

## 额外查询程序的精确流程

程序按文件名排序读取`examples/customer_attraction/*.json`，允许一层`instance`包装，调用规范Instance解析；跳过解析时的TypeError/ValueError/KeyError，以及玩家数大于5或主题数大于7的输入。JSON读取本身在这段异常处理外，缺失、损坏或非预期目录不是“检查通过”的输入。

对每个保留下的固定输入，ExactSPESolver.outcomes()返回全部可实现的**终局主题计数**。程序逐个用Fraction计算五类或一般k类查询F_c(T)，并计算gap=m max_T F_c(T)−W。若当前输入存在正gap，取`max(violations)`对应的元组，重构一份完整策略，调用verify_certificate并要求其有效，写出完整JSON后立即返回。

因此“首个失败”指排序后第一个有失败终局的输入；在该输入内不是遇到首个终局就停止，而是计算全部终局后选最大正差，平局继续按Python元组顺序比较。它没有枚举全部完整策略，亦没有保证所得证书就是原examples同名的旧证书。

程序没有随机扫描、数值LP或外部参数搜索。若所有读取输入都没正差，只打印已检查终局数和“无一般证明”的说明；没有完整输入清单或全阴性结果文件，因而不能从一条旧stdout重建所有实际扫描范围。

## 本轮一次明确正例重放

原失败报告3cdcdaf1fa0e22cc5859为4134字节，完整保存七行客户、31个有序历史动作、终局计数、31历史/124非自身偏离审计、实际AAB路径、W=8、五个查询分数和gap=1。本轮全文读取所有字段和每条动作，不只读取audit.valid。

按原字节保存程序及四个规范模块`customer_attraction/{__init__,model,exact,certificate}.py`；这四依赖已经有[完整求解器对象](完整历史求解器的精确复现--计算.md)，本批不重复为其提交done。恢复一个只含`coverage_opportunity_failure.json`的明确输入目录，运行原程序一次，得到

\[
\text{可实现终局计数}=8,\qquad
\text{正差终局计数}=2,
\]

所选AAB完整报告与冻结原JSON**全部字段和原始字节一致**，SHA256均为

`1acd1404ec8d7f3d594b1bc0525dbb98ea64cd9734ea74d539b624a5fc47a568`。

实际Python3.12.14，退出0，stderr为空；命令、cwd、运行次数、完整stdout和比较记录见[重建与运行清单](../../tools/evidence/terminal-query-probes/replay/stage_manifest.json)。这次不是原历史整个examples目录的重建，也不重复此前已妥善处置的阴性样本。8是计数向量数，2是其中违反当前候选的向量数，都不是完整策略棵数。

该报告与既有规范证书有四处末位动作不同。新[固定查询比较](../../tools/evidence/terminal-query-probes/audit_fixed_query_values.py)逐条对账，并从单位客户定义计算查询核；它不再执行完整SPE搜索。其新增有理分布p=q=(0,1/3,1/3,1/6,1/6)认证同路径的M_b=7/3，精确说明此例没有同时否定LAST。这个值和证书差异是本轮补充，未写回旧报告。

## probe_last：静态核精确，优化值仍为浮点

对给定背景主题计数b，`matrix`逐客户类型以Fraction建立

\[
K_b(T,A)=\sum_{x\in T}\frac1{1+b_x+\mathbf1_{x\in A}}.
\]

`value`随后把整矩阵转换为NumPy浮点数组，调用SciPy/HiGHS求

\[
\min v:\quad K_bq\le v\mathbf1,\quad q\ge0,\quad\sum_Aq_A=1.
\]

数学LP准确对应有限minimax的列问题；实现返回的res.fun只是数值结果，函数没有检查res.success、恢复有理q或提供精确上下界。只因输入矩阵最初是Fraction，不能称整个计算精确。

主程序遍历所选根目录的examples文件，要求同名certificate存在。`action_map`递归字典，找到某个actions列表后转为历史到动作的字典；它不递归列表，重复历史会被字典覆盖，也不在此验证完整域、所有离轨激励或证书终局声明。主程序只跟随实际路径取得b和W，再打印mM_b与差值；部分异常被标为skip。因此单独运行它不是完整SPE认证。

该程序可作已认证种子上的定位诊断。若输出提示正差，仍需保全明确输入和完整有序策略、重验全部真实偏离，并给足够精确的查询分布下界证书，才能认证LAST失败。

## last_cone_attack：固定完整策略中的交替候选生成

它导入已经整理的[完整策略客户重数锥](../定理/固定完整策略的客户重数锥--定理.md)实现。固定动作图后，实际路径、末前主题计数b及根终局计数都固定；客户重数改变时，必须保持该图的全部激励行非负。

按k个主题的非空兴趣掩码M建立列，记w_M≥0为客户重数。对每个查询t、阻挡a，张量K_{t,a,M}是该类型一名客户在背景b下的查询收益。于是查询收益对w线性。程序交替做：

1. 固定w，解查询行LP，最大化z，使每个阻挡列的期望收益至少z。
2. 固定p，在完整策略锥、w≥0及根福利W(w)=1下，最大化v，使每个阻挡a都有mΣ_{t,M}p_tK_{t,a,M}w_M≥v。

第二步使用全部已建立的真实历史激励行，不是只约束实际路径；但“固定完整策略”仍只是全部策略集合中的一个锥。它没有搜索任意完整动作图，也没有把交替优化变成联合全局最优性证明。

实现使用一个seed=942137的NumPy随机生成器，每个种子最多9个起点，每起点最多12次交替；首起点取原重数的数值最优查询，其余用Dirichlet。达到数值停滞容差1e−9便提前停止。输入glob未排序，所以多文件目录的枚举顺序还会影响同一随机流的使用；只写seed不足以复现未知旧目录的全部运行顺序。

归一化要求原实际福利非零，代码直接除以它，没有专门处理零福利；这个搜索范围不能因此改变原模型允许零客户、空主题的定义。零兴趣掩码不参与收益及福利，程序的列空间也不把它作为一个有影响的重数变量。

### 正候选的恢复仍不是完整安全值证书

若浮点mM超过1+1e−7，程序将每个浮点w近似为分母至多10⁸的Fraction，精确核锥和归一化；不满足时尝试恢复有理顶点。接着放大为整数客户，重建实例，并用既有定义级函数检查完整策略。

这些步骤可把**实例与SPE**部分恢复为精确对象。但最后的M_b仍由`probe_last.value`数值LP给出，正差阈值仍是1e−7。输出JSON虽含完整actions、整数clones和一个p向量，p来自先前浮点重数上的查询优化，未对最终整数实例形成独立的精确下界认证。因此原输出名`last_candidate.json`准确；不能把它直接改称LAST反例证书。

`row_opt`没有核res.success便读取res.x；`weights_opt`不成功时返回None并停止当前迭代。这些实现失败、恢复失败和最终“NO CANDIDATE”都不是一般数学上界。原注释也明确浮点LP只提候选、阴性结果不作一般推断。本轮没有执行这两个主扫描函数，也没有新增一个正或负LAST搜索结论。

## 原目录、写行为和可用复现依赖

两个security脚本按自身`parents[5]`定位旧仓库根，last_cone还从同目录导入probe_last，并从`tests/audits`导入策略锥。平移单个脚本会破坏路径。全部三个原程序、四个规范模块、策略锥模块、明确的十一客户输入及同名旧证书，均按原相对路径保全。

[stage_probes.py](../../tools/evidence/terminal-query-probes/stage_probes.py)逐文件验SHA并复制到必须尚不存在的新目录，形成10文件的可用小工作树。它不自动运行两份LAST扫描；只有显式`--run-extra`才执行本轮已经重放的精确查询程序。完整用法见[README](../../tools/evidence/terminal-query-probes/README.md)。NumPy、SciPy仅为两份数值程序及策略锥导入所需；原额外查询重放只需标准库。

actual_extra和last_cone的成功分支都会在自身目录覆盖同名输出，没有拒覆盖保护；probe_last只打印。因而原件只供读取，运行使用新目录，旧JSON与新输出分别保留。新辅助程序明确记录单输入范围，不伪装成丢失的历史扫描驱动或完整旧目录。

## 与恢复点README的数学衔接

源737470ce81258b7fcdf2同时记录Bernoulli生成表示、有限组合核验、终局查询候选失败、遗漏阈值纠错和动态返还池缺口。本轮把这些分别接入[生成表示](../引理/最优索引交换的生成表示与查询税--引理.md)、[有限二项/Beta核验](最优交换二项矩与Beta核的精确核验--计算.md)、[候选反例](../反例/实际终局额外查询的三人反例--反例.md)与[净遗漏勘误](../障碍/遗漏份额支付的半因子勘误--障碍.md)。

其正面停点保留：真实外部覆盖E=L_out+R_out，积分税只给L_out；即使逐枝补出R_out，互斥强制最优主题子树仍未获得可无重复使用的原路径W共同预算。清洗和复现这些来源没有解除这个动态义务，也没有把有限失败、阴性探索或代数修正登记成一般half新进展。
