---
id: customer-attraction/pay-original-implementation-full-input-and-ordered-path-replay
kind: computation
type_tag: 计算
title: PAY原实现的完整输入与有序路径复现
status: 三原入口各一次成功；7相关原件不额外primarydone，旧冻结0run历史不改
summary: 正常取回原PAY7件后核完整依赖/实际输入，在三新source-root各运行作者审计、三真实输入全路径及父方显式路径；报告/781树与原证据精确一致，有限量词与一般证明分开。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/pay/audit_pay.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/pay/all_path_pay.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/parent/audit_pay_dag.py
---

# PAY原实现的完整输入与有序路径复现

## 补取版本及严格分开的处置

Root用正常授权clean show实际取回7项共111551B，size/SHA256/Git blob SHA1逐件核对；完整正常show capture及source原路径双冻结commit都保于[获取与依赖清单](../../tools/evidence/pay-original-implementation-comparison/source-and-dependency-manifest.json)。三py（6325/6590/2897B）、两JSON报告（563/596B）、2215B三行JSONL、92365B完整m5树全部实读/解析。JSON全部字段及781 action行被消费，原树不是只有metadata的断言。

此前JE/JQ包在当时确仅本地blob缺并记录0run，保持冻结；本补充新记录实际补取、完整依赖和三次原入口。**这7项只是已清洗数学的必要相关原件，不额外认领或primarydone**，也不重写旧semantic receipt、原报告/树字节或原数学一般性。

## 真实导入链与输入域

三个入口都靠路径parents定位原repo根，故每次保留research/workspaces/customer-attraction/R7…/pay或parent层级。原__init__.py导model/exact/certificate四文件（691/8640/9943/6201B），分别完整实读并核SHA；它们都只用Python标准库。原all_path_pay再用importlib从R-7e9…/background_induction/search_background.py加载4073B BackgroundSolver；该文件也全文核读。它的默认随机1000轮main有守卫，本次仅导入类，**没有执行其随机main**。无pip、LP、MIP或网络。

BackgroundSolver用lcm(1,…,m)整数缩放，保存全部终局composition、pay/coverage和位集SPE菜单，阈值max_a min_child，count缓存只集合，不共用一个平局选择器。inspect_instance使用零前缀，全m静态终局的利润正好是覆盖。其pay矩阵可能给未占用主题代数值，路径选择先以终局次数过滤，实际阈值孩子均含当前动作，未将ghost值当不存在玩家收入。输入由Instance验证单位客户正整数重数/合法标签及玩家数；重复兴趣条目由inspect_instance显式合并，不丢同mask条目。没有声称BackgroundSolver本身是任意外部非法输入的健壮验证器。

真实三输入均完整保留examples原字节：root_tax_failure（4人/6题/61客户，1133B）、individual_security_failure（3人/6题/34客户，1465B）、dynamic_iid_local（5人/7题/60客户，1930B）。这不是从新counterexample异schema重造的输入。作者audit与父audit其余夹具内嵌原py，均全读；它们的schema/真实客户组另在[输入及源码清单](../../tools/evidence/pay-original-implementation-comparison/source-and-dependency-manifest.json)。

## 三个不同原入口，各一次

每次从不存在的独立run目录建立source-root，仅复制核过字节的代码/所需输入；不预放audit将写的两个输出。记录原argv/cwd、时间、exit、stdout/stderr SHA、运行前所有文件SHA与新增输出。原代码和输入运行后均未变。完整[事件](../../tools/evidence/pay-original-implementation-comparison/execution-summary.json)保三记录，不把模块导入或内部函数调用另计原CLI。

| 原入口 | 当前实际执行 | 作用与责任 |
|---|---:|---|
| pay/audit_pay.py | 一次exit0 | 180分位/全断点对照、128完整有序策略显式核、两无限族有限点和参数左跳有限点，内嵌m5完整树定义级核；写新报告和树。 |
| pay/all_path_pay.py + 三原examples参数 | 一次exit0 | 三真实输入上每SPE终局/全部可实现有序路径/全部真OPT计数/全部允许前缀参数的max–min；不使用原某一策略作为全部路径。 |
| parent/audit_pay_dag.py | 一次exit0 | 三内嵌小输入直接枚举全部可实现有序paths/OPT/断点，对DAG值；独立于DAG优化递推，但仍共享canonical Instance/ExactSPESolver。 |

当前三入口各一次，未重复；不是一个原入口跑三次。PYTHONDONTWRITEBYTECODE阻pyc噪声，PYTHONHASHSEED0只固定集合遍历，原源码没有改。audit默认write_text会覆盖输出，故不在冻结目录执行；两个新输出从不存在状态生成，旧原树/报告只在original只读保存。

## 作者审计的全部实际有限域

180条分位检查是m2…9、k2…m、五种r、每行七个(w,b,d)类型，与独立枚举0/4及全部精确断点比较同一(score,t)，还核空types及全d0返回(F0,F0)。这不是实例SPE扫描，也不认证任意实背景/有权玩家。

两主题/三玩家、不交各一客户的全部7个有序决策节点策略共有2⁷=128份，原定义级verifier逐份核，14份为完整SPE，直接路径min PAY再取max得−1，与count-DAG同值。这里是完整policies枚举，和下一节81/6/2的路径枚举不是同一种计数。Verifier只从给定完整动作树计算每条真实偏离，不调用SPE求解器；payoff模型仍共享canonical代码，不能称完全独立模型实现。

有限族检查为：大题族m3…40共38点，负首步族n4…40共37点，参数左跳m5…40共36点；它们用直接断点评价核精确t/余量及两个移位正多项式。无界人数的证明仍来自[两近二族](../引理/两个近二完整策略族的末对参数支付--引理.md)和[左跳证明](../反例/真实前缀支付未成立时的最优参数左跳--反例.md)，不从这些点外推。

m5内嵌输入B有12名客户、四个不交singleton各1，共16单位客户，所有781决策历史行动0。原入口生成新StrategyCertificate并定义级核781历史/3124**非自身**偏离（每节点4替代），验证后写新树。新92365B树与冻结原树**逐字节相同**，新563B报告亦同SHA；所以原树全部字段/完整action表与已核新构造吻合，而非声称原入口先读取旧tree作验证。两前缀best_t40/13和20/7，最小PAY余量1056/325、176/525，完整证据同样保留“非PAY/half反例”scope。

## 三真实输入的全路径结果

原三行JSONL全部字段实际解析；新stdout除各行seconds外所有字段逐项相同，连原input相对路径、选择的实际path/收益、每k收费参数/真OPT计数组合都一致。两组seconds均原样保于[比较结果](../../tools/evidence/pay-original-implementation-comparison/comparison-results.json)，不抹计时差或伪称JSONL逐字节一致。

| 输入 | 真OPT | 真OPT计数组合数 | SPE终局数 | 终局/前缀状态对 | max_path min_prefix,OPT,t |
|---|---:|---:|---:|---:|---:|
| root_tax_failure | 61 | 1 | 12 | 120 | −39/5 |
| individual_security_failure | 34 | 4 | 20 | 82 | −70/3 |
| dynamic_iid_local | 60 | 14 | 20 | 154 | −136/3 |

这是各固定输入全部可实现SPE路径上的有限阴性，没有找到PAY反例。并不只重放一条原策略，也不证明一般输入的PAY。三个max_suffix2_margin也保存为相同负值，只属这些有限输入。

重要的路径区别：root报告最坏PAY路径是AAFA=(0,0,5,0)，收益(9,9,11,9)、W38；[旧根税策略](../反例/四人实际根总税--反例.md)是AAAF、收益(9,9,9,11)。它们同终局计数，但不同策略的末位平局可以使第三人的真后继改变。JQ纸面三收费只核旧AAAF一path，不能代替本次全path认证；其前两A使三个允许prefix数值恰相同，并非输入/原σ相同。

individual报告取(2,4,3)，收益(29/3,35/3,35/3)、W33；不要替换成该输入另一份原individual-security反例策略的W32。dynamic报告取(6,6,2,5,4)，收益(12,12,10,12,12)、W58。负值下代码不会额外构造这三path的完整证书；可实现性来自完整集合值菜单合同。正值才执行canonical certificate(on_path)并定义级核的分支已全文读，但这三输入及其余本次小例**未触发**，不能声称正反例证书分支已跑过。

## 父方显式路径三例

父入口用ExactSPESolver.ordered_outcomes逐path，与逐OPT/断点最小值直接比较subject.inspect_instance；并非枚举所有完整策略映射，尽管每path均可独立补全。三case分别：四人三空题（零客户），三人覆盖{0,1,2}/{1,3}/{2,3,4}，四人覆盖{0,1}/{1,2}/{0,2,3}。

| m/题数 | 可实现有序paths | 真OPT计数数 | 直接值及DAG值 |
|---|---:|---:|---:|
| 4/3 | 81 | 15 | 0 |
| 3/3 | 6 | 3 | −3 |
| 4/3 | 2 | 9 | −59/15 |

这些数学字段与原596B report完全一致；原report另附command元数据，当前stdout没有该字段，比较时只排它，不声称report原始JSON字节相同。零case保全同覆盖空标签与全部平局，81是3⁴条paths，不是3^40份完整策略。

## 状态与复用

完整源码、三原输入、全部标准库导入链、三事件/完整新旧stdout/两个新输出和比较脚本记录都自足保存。当前新增的是有限实现证据，原一般[PAY算法合同](../算法/真实前缀支付的加权分位与完整路径切断--算法.md)仍需其解析证明；没有新一般half、PAY存在前缀或正完整SPE反例。

本补充只增加相关资源，不给7source写primarydone。JE/JQ原件和0run处置保持原字节，后续读者由本页看到真实补取/新运行时态；其它谱/奖励尾尚未补到的代码不能借这三次成功自动视已运行。
