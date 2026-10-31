---
id: "unrelated-machines/five-machine-tree-markov-independent-original-audit"
kind: "computation"
type_tag: "计算"
title: "五机树Markov独立原程序的逐态最优补全"
status: "complete-primary-read-and-original-cli-retained"
summary: "独立从真实两调度构造树pair条件扩展，32原分配及四态两补全；只否定冻结树任务的逐态严格次二合同。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/independent_tree_markov_completion.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/independent_tree_markov_completion.py"]
source_ids: ["550029ae0b7866d1f937"]
truth_status: "exact finite checks with separately reconstructed proof and version scope"
review_status: "informed internal reread, no new blind or external review"
---

# 原任务与可见信息

3592B `independent_tree_markov_completion.py` 全文已读，源SHA `e00e21918e3e5aee4729525fb4eb7409d6c97f3ed8cb6f59581533804225d9e2`。它不导入作者实现或其它数学模块；无随机数。实际原CLI一次exit0，自己构造全部单机与树pair边际、逐条件扩展、重新回算原调度负载。[原件/执行资源](../../tools/evidence/um-tree-matching-and-configuration-primary/README.md)。

机器1,…,5，任务有限端点为

| 任务 | 有限端点与时间 |
|---|---|
| a | 1:1，2:1/2 |
| b | 2:1/2，3:1 |
| d | 3:1，4:1/2 |
| e | 4:1/2，5:1 |
| c | 1:1，5:1 |

T=1，选生成树路径1–2–3–4–5（任务a,b,d,e）。真实全局分布D以各1/2取 A：c→1、a,b→2、d→4、e→5；B：a→1、b→2、d,e→4、c→5。两份峰1，c的两端都时间1给OPT≥1，故OPT=1。代码另枚举全部2^5=32个合法原分配，独立求得同一个OPT。不是仅配置LP、伪矩或彼此不相容的pair数据。

# 条件扩展保持什么，坏态怎样产生

程序从D取得完整单机配置概率与四条树边上的完整配置pair分布，先按机器1边际取状态；沿u→v将当前状态质量乘 pair(S_u,S_v)/singleton_u(S_u)。正状态的分母为正。每次扩展后得到完整5机配置元组，最后独立核全部单机和四pair概率与D精确相同，归一质量1。

机器3在D中恒空，使左A/B分支与右A/B分支在Markov再耦合中独立；四态各1/4。**只冻结树任务**，丢掉元组中c的暂时选择，再在c的两个合法端各试一次，真实最优补全为

| 左/右分支 | 冻结树负载(1,…,5) | 最佳补c峰 |
|---|---|---:|
| A/A | (0,1,0,1/2,1) | 1 |
| A/B | (0,1,0,1,0) | 1 |
| B/A | (1,1/2,0,1/2,1) | 2 |
| B/B | (1,1/2,0,1,0) | 1 |

坏态冻结a→1、b→2、d→4、e→5，c两端都已有1，任意补全都峰2，故坏质量恰1/4。全局D本来有峰1调度，失败来自舍掉非树相关性并冻结再耦合的树任务；不能把原c边际1/2、1/2直接当成坏态余量LP的可行点。

本原程序核四态权重、所有边际、每树任务恰由一端选择、每态两种c补全，输出全部四态的局部配置、冻结分配和负载。没有只输出一个抽象失败标签。[完整新stdout](../../tools/evidence/um-tree-matching-and-configuration-primary/runs/tree-markov-independent.stdout)、[运行记录](../../tools/evidence/um-tree-matching-and-configuration-primary/runs/tree-markov-independent.execution.json)。

# 一般合同、四机正面边界与有限范围

完整5545B canonical、2966B实际review及4173B作者源码本批全读；作者源码有顶层主审计，但本程序不导入它，**本轮没有运行作者主审计**。review的内部statement-first构造/重建再读冻结稿仍属历史，本轮知情复跑不是新blind。

反驳的量词是：给定真实全局T分布、固定连通生成树、每任务两端且每机器对至多一任务，对**每个正概率树Markov态**冻结树任务后，非树任务均可补成严格<2T。换树、择好态、移动树任务或保留更多相关性都不受否定。本坏态把a从1移到2再把c给1，就恢复峰1；原程序没有自动执行这个修复，正文解析指出它。

至多4台机器的同合同有正面边界：连通树是星或双星，一个顶点或中央边端点覆盖全部树边。正Markov态的这个完整单机/中央pair状态在原D某支持态中出现，并决定所有树任务方向，所以那份原支持态提供T补全。它不是本程序枚举所有4机输入得来的结论；断开森林、多任务同机器对、非真实D数据不在这个证明内。

新输出与旧独立JSON `4793fd8514c206c37797` 全字段相等；作者旧JSON `72369…` 的完整输入/pair数据另作比较，不能转记本轮作者运行。[既有最终审查](../审查/五机树Markov再耦合补全反例最终审查--审查.md)与[旧独立有限审查](../审查/独立稀释残余与树Markov完成审计--审查.md)承载原数学身份，不重复done。该有限接口反例不是一般调度困难性、所有树法失败或UM主目标的否定。
