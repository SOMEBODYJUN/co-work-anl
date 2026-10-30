---
id: "unrelated-machines/complete-clone-dual-oracle-periodicity-audit"
kind: "computation"
type_tag: "计算"
title: "完整克隆的双Oracle与周期族有限核验"
status: "finite-exact-audit-replayed"
summary: "保留带标签分配DFS、类型计数瓶颈DP及周期族构造的原程序和报告；一次重放逐字节一致，并澄清2290是全部177次DFS调用的累计节点数。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/complete_clone_multiset_periodicity.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/complete_clone_multiset_periodicity.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/complete_clone_multiset_periodicity.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/complete_clone_multiset_periodicity.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/complete_clone_multiset_periodicity_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/private_graft_and_resource_repetition.md"
---

# 完整克隆的双Oracle与周期族有限核验

本对象保存[完整机器任务克隆定理](../定理/完整机器任务克隆的多重集与最终周期--定理.md)配套原程序、原冻结报告及本轮一次重放。程序以两种不相互调用的有限方法求小实例最优值，另构造奇偶、任意周期及Sylvester实例族的实际带标签调度。它没有通用多重集LP、半群周期计算或多项式调度后端。

本轮用Python 3.12.14读懂并重放原程序一次，stdout与16138字节冻结报告逐字节一致。源码实读同时澄清一个计数口径：labeled_search_nodes=2290累计全部177次带标签DFS调用的递归节点，既不只是奇偶种子的5次，也不是穷举全部分配的数量。原报告没有改写。

## 原资源、依赖与使用

- [原程序](../../../../tools/evidence/private-tree/complete-clone/complete_clone_multiset_periodicity.py)：10337字节，原字节保持。
- [原冻结报告](../../../../tools/evidence/private-tree/complete-clone/frozen_report.json)：16138字节，原字节保持。
- [本轮重放输出](../../../../tools/evidence/private-tree/complete-clone/replay_report.json)。
- [本轮重放比对记录](../../../../tools/evidence/private-tree/complete-clone/replay_verification.json)：命令、解释器版本、hash、字节及JSON比较、177次调用的范围解释。

从仓库根运行：

~~~bash
python3 tools/evidence/private-tree/complete-clone/complete_clone_multiset_periodicity.py
~~~

原程序无CLI参数和外部输入文件，只使用fractions、itertools、hashlib、json、pathlib、platform、random等Python标准库。它读取自己的源码计算hash，打印JSON，不修改冻结报告。核验使用assert，采用普通python3执行。程序所说“两种独立oracle”仅表示两份不同实现不相互调用；它们仍共用Fraction类型、dimensions输入检查和同一测试集合，本轮也不是另写一份新的独立实现。

内部矩阵p按机器为行、任务类型为列，有限值须为非负Fraction，None表示不可用端。dimensions要求至少一行、矩形矩阵、每列至少一个可用端，允许零费用和零列。正整数q表示每台原机器和每种原任务都复制q份，每条原有限incidence放入全部q²个克隆端。内部函数面向合法Python对象，不是已经建立任意外部JSON schema及拒绝行为的输入服务。

## 两个有限最优值oracle的不同含义

### 带标签任务DFS

labeled_oracle(p,q)显式创建全部(j,r)任务标签，按原合法机器类型数量及标签排序。它递归选择原机器类型i和具体副本s，精确累加每个机器副本的负载。

同一机器类型内，当前负载相同的副本对未来任务完全对称，故每个负载只探索一个代表。另以

\[
U=\sum_j\min_{i:p_{ij}<\infty}p_{ij}
\]

作为初始已知可行上界：把每个原任务放最短端，再在每个克隆编号复制该原调度，得到负载≤U。若新增负载已经≥best，非负费用使该分支不可能严格改善best，可以剪去。因此程序可能没有访问达到当前上界的某个叶子，仍能正确保留这个已知可行值；零最优值及空任务均包含。

函数返回最优值和实际访问递归节点数，不返回一份最优分配。节点数受到这两类剪枝影响，不能解释为全部合法分配的枚举数量。对大输入，这是有限指数搜索，没有多项式复杂度承诺。

### 类型计数瓶颈DP

count_oracle(p,q)枚举每种原任务在单台机器副本上出现0,…,q次的计数向量a。对原机器类型i，删除在不可用端使用非零数量的模式，计算模式负载

\[
L_i(a)=\sum_j a_jp_{ij}.
\]

然后逐一处理每种机器的q个副本。状态done记录已安排的各类型数量；转移加入a且不超过每类型总量q，将瓶颈值更新为max(旧瓶颈,L_i(a))，同一新状态取最小值。目标状态是每类型均q。

这个DP没有调用DFS，也不枚举每个job副本的标签。对完整克隆，单类型所有副本具有完全相同资格；计数达到q后，可将q个带标签job一一填入对应槽位，因此计数模型与真实分配一致。其状态及模式数量可达(q+1)^n，仍是有限指数oracle。这里的单类型上限q来自本次实际克隆的q件任务，不是通用无限多重集LP求解。

## 实际输入集合及比较范围

固定6个矩阵为：

1. 单机一件零任务；
2. 两机两任务，分别具有唯一零端和唯一单位端；
3. 两台机器、零件任务；
4. 含分母10^40+7及不可用端的两机两任务；
5. 两机三任务奇偶种子：big两端时间2，左右各一件私有时间1任务；
6. 两机三件全可用单位任务。

随后以random.Random(24019)生成80例：机器数选1或2，任务数为0,…,3；费用字母表为0、1/3、1、2、None。若某列全不可用，随机选一个机器把该端改为1/3。总计86个固定或确定性采样矩阵；这不是遍历全部矩阵。

每例对q=1,2分别调用两oracle并比较，产生报告字段cross_oracle_checks=172。每例还检O_2≤O_1，这是整除倍数的单调性，不是相邻q单调性。之后对奇偶种子q=1,…,5另作5次双oracle比较，输出3、2、3、2、3。故实际总共有177对oracle调用；报告的172字段只计第一部分。

源码visited先累加前172次DFS，再累加后5次DFS，最终labeled_search_nodes=2290。旧审查表将这一数放在奇偶种子行附近，可能造成范围误读；本轮已据实际累加位置在定理对象中明确其全177次含义。报告本身的2290数值正确，原程序和原报告均未改动。

## 构造证书与容量检查

### 奇偶三任务种子

parity_schedule(q)在运行时创建全部3q件带标签任务的sigma。

- q为奇数时，每个左副本放一件big和一件左private，负载3；每个右副本放一件右private，负载1。
- q为偶数时，每行前q/2副本各放一件big，后q/2副本各放两件相应private，全体负载2。

程序对q=1,…,24逐次构造并核合法端、任务数量与机器负载。它返回makespan及每机器负载字典，不返回sigma。因此冻结报告的actual_allocations保存24张逐机负载表，不能把该字段称为序列化完整job→machine分配；完整分配的确定性公式及构造代码仍可复现。

另核T=2下每行半质量big单件、半质量两件private的多重集配置，三种job类型覆盖恰1。对q=1,…,50检查容量条件

\[
2(q-x)\ge q,\qquad2x\ge q,
\]

可行x在偶q时恰q/2，奇q时为空。一般奇偶最优值仍由整数负载及上述容量证明解释；程序只在所列有限范围重算。

### 任意周期族

对m=1,…,9和q=1,…,40，共360组，arbitrary_period_schedule构造一件全可用unit和每机m−1件私有1/m任务的完整q克隆。它按原定理余数式计算d，把q件big分配到各机器类型，并把每种私有任务的q个标签填入该行剩余整数槽位。负载以1/m为单位使用整数计数。

函数核全部job标签数量、有限端、每机器容量和实际值1+d/m；另在t=0,…,m−1上独立最小化行容量条件

\[
m\left\lfloor q(t+1)/m\right\rfloor\ge q
\]

确认最小值为d。这不是为360组分别运行完整DFS或DP；所谓独立最小容量检查，是对证明给出的整数行条件另行枚举。m=1时只有big任务，代码短路处理资格判断，不对不存在的private类型做除以m−1的运算。

报告仅保存参数范围、360计数及按固定顺序生成的(m,q,value)列表hash，不保存360份完整sigma，也不逐项打印该列表。

### Sylvester首次达到族

程序生成前5族，分母及理论首次最佳q如下：

| k | 分母列表 | 报告first_optimal_q |
|---|---|---:|
| 1 | 2，2 | 2 |
| 2 | 2，3，6 | 6 |
| 3 | 2，3，7，42 | 42 |
| 4 | 2，3，7，43，1806 | 1806 |
| 5 | 2，3，7，43，1807，3263442 | 3263442 |

每族先用Fraction核倒数和为1，再对q=1,…,100核ceil容量条件等价于q为分母乘积的倍数，共500次。仅k=1,2,3实际展开首次最佳q上的全部带标签任务，并检查所有机器负载1。k=4、5没有实际展开1806或3263442份副本；报告first_optimal_q由该族的理论公式计算，不是程序穷举到该数后才发现最优。其所有q范围的正确性须结合[一般容量证明](../定理/完整机器任务克隆的多重集与最终周期--定理.md)，不能由q≤100有限检查单独推出。

## 原报告及本轮重放

原报告完整保存Python版本、seed、source hash、全部上述计数、5项奇偶最优值、24张负载表、任意周期列表hash、5族分母及3条limits。它不保存86个矩阵、360份完整分配或全部一般LP证书；原程序中的固定定义及确定性生成规则提供复现路径。

本轮代码SHA256为ff27143a75627f1e6d7bd0f21afccb1ab21aa6119b5a9ed18778c992177bd9de；原冻结报告和新stdout的SHA256同为229ffdcf1a54afd756012957457258e70b2f07a0c33ccf4cc11ad9242a72301a。实际Python与旧报告同为3.12.14，连版本字段在内逐字节一致。重放比对记录另写出172+5=177的口径，不改原报告。

这批证据支持有限实例的完整克隆身份、实际构造和两种精确求值实现的一致性。一般MC阈值等于min O_q、最终周期与最小gcd、所有输入上的指数首次达到结论仍须依赖数学正文。若接续一般MC求解、周期识别或多项式调度算法，必须另外定义接口及复杂度，不能把这里的有限oracle直接充任后端。
