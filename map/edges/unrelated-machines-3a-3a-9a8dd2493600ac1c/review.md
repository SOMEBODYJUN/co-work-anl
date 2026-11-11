# InfDegreeOne、InfDegreeTwo 与降度交域的实读比较

任务 unrelated-machines-3a-3a-9a8dd2493600ac1c；Boss5。核心 M-90610eea6c6447188c03208eaa549254 v3；共享 M-b126c4b3ff29400589f7f38abdca4d85 v3、M-7bc9eab74ecd475db7df33c3f4b75e61 v1。当前任务三项 input_pins 均与 research show 的 registration_pin 一致。

## 1. 实读和模型

完整读取三份登记合同、共同文献正文；从冻结 maxmin.pdf 重新 pdftotext -layout，读取印刷页4的物品侧 Degree/InfDegree 定义、页6–7的原始配置LP和M-LP定义、页12–13的值域边界及 Lemma4.1/脚注2；渲染并目视核印刷页13，确认平方根、人数指数与脚注对象。没有声称复审全文49页算法。完整读取《无限helper全阈值降度与三度二无限度配置间隙--定理》及必要独立复核的定义、链式容量和 §§6–7 具体族；同时查读现有 infinity-chain-to-exact-intersection-config-gap 关系，避免重复交付其已成立的迁移。

所有比较均为不可分物品、非负加性 MaxMin；每件物品至多一位受领者。InfDegree 是物品的符号∞端数，不是玩家的∞物品数。配置LP对每位玩家的所有达阈值配置给质量和1，对每物品给总边际≤1；它不要求各玩家配置分布有共同整数实现。不能把有限大端重估为∞后不再检查 InfDegree 条件。

## 2. 核心 InfDegreeOne 的完整配置见证

取整数 T≥4。每份 H_T 有 root a、辅助玩家 b_1,…,b_T，物品 u_1,…,u_T、w_1,…,w_T；a 对 u 值1，b_k 对 u_k 值∞、对全部 w 值1，其余值0。建立 K=T² 份 H_T；另加 K 件 B_r，B_r 对第 r 个 root 值∞；加一位中心玩家 c，对全部 B_r 值1。于是

n=K(T+1)+1=T³+T²+1，m=2TK+K=2T³+T²。

每件 u 只有一个∞端，每件 B 只有其 root 一个∞端，w没有∞端，故是 InfDegreeOne。这里 w 的总正度为T，不能调用 DegreeTwo 后端。

在阈值T，每个 root 给全u配置质量1/T、其 B singleton质量1−1/T；每个 b_k 给 u_k singleton质量1−1/T、全w配置质量1/T。对中心 c，给 K 个循环连续 T件B 的配置各质量1/K（指标模K）；每件B恰出现T次，所以其中心边际为T/K=1/T，且每个中心配置值T。每件u、w、B的总边际恰为1，所有玩家配置质量恰为1。故原始CONFIG(T)可行；这比“分数效用为T”更强，明确支付了全部配置合法性。

按原论文 M-LP 的阈值规范，把∞大端截记为T。root 的小物品使用z=1/T，各u边际1/T；b的小使用z=1/T，各w边际1/T；中心z=1，各B边际1/T。大singleton边际均1−1/T。逐项满足小边际≤z、有限值加权和≥Tz、大边际+z≥1、每物品容量≤1，所以同一家族也支付M-LP下界；没有使用一个一般的精确M-LP⇔CONFIG等价。

任何正最低值V的整数分配令中心至少取得一件B，故至少一个root没有其唯一外部∞物品。若该root拿s件u，则s≥V；对应s位b失去各自唯一∞物品，须共享T件单位w，故sV≤T，推出V²≤T。中心的值是有限整数，最低值也为有限整数，因此OPT≤q=floor√T。反向每个block给root q件u，失u的q位b各给q件互异w，其余b拿自己的∞u；q²≤T。再给中心q件B（q≤K），其余B任补。所有玩家至少q，故OPT=q。

还可直接核ConfigOPT=T：若s>T，每位b的合法配置都必须含自己的u，故u容量已被其对应b完全占满；各root只能用其B达到s，进一步把全部B容量占满；中心不可能获得正质量有效配置。因而该明确家族比值恰为T/floor√T=Θ(n^(1/6))。这只是核心既有存在性证明的精确补全，不新增一个为算术单独编号的节点，不声称全类tight上界或NP-hardness。

## 3. 与 InfDegreeTwo 的具体比较

原PDF对InfDegreeTwo的 Ω(n^(1/4)) 只有印刷页13脚注2的“类似论证”声明。其完整透明重构已在共享交域正文§8展开：用T个H_T和T−1件相邻root共享∞物品B_r，去掉中心c。对B_r给左右root的singleton质量(T−r)/T、r/T；每root的外部质量恰1−1/T。block内部配置沿用上节。每件物品边际均1。T个root面对T−1件B，整数分配必有root没有B，仍得V²≤T；q²≤T给达到q的分配。s>T时每root的合法配置必含B，总需求T超过容量T−1，故ConfigOPT=T、OPT=q、人数n₂=T²+T，给Θ(n₂^(1/4))。

这是一项明确的外层结构重设计：InfDegreeOne 用T²份block及单位值中心消耗某件B；InfDegreeTwo允许同一B在两个root上为∞，于是T份block和一条缺一物品的路径就能强制有root内部自足。它不是从两个对象的存在性陈述作代数推演，也不是同一输入的保持映射；本包只留 motivates/context，精确指示复用的H_T与容量证明。类包含 InfDegreeOne⊂InfDegreeTwo 至多把核心旧族带成Ω(n^(1/6))的较弱下界，不能支付目标Ω(n^(1/4))整句。反向从较宽类的存在性gap，也不能给∞度1的实例。

## 4. 与 DegreeThree 交域的比较

共享 M-7bc9eab… 的明确输入是上一节T-block的InfDegreeTwo族，不是InfDegreeOne核心族。对其中T²件正度T的w用∞helper链，各件新增T−1玩家，故全部新玩家N=T³+T，物品M=T³+T²+T−1。已登记的全阈值桥和现有canonical边给ConfigOPT=T、OPT=q；新比值Θ(N^(1/6))，不是Ω(N^(1/4))。

指数1/6与核心相同并不表示命题等价。交域有物品总正度≤3和∞度≤2；核心要求∞度≤1但不限制总正度。交域族的相邻root外B有两个∞端，链内部w副本有两个∞helper端，所以它不在InfDegreeOne中。核心族的w正度T，所以也不在DegreeThree中。新增helper必须计入人数和MaxMin目标；不能把它们删去以保旧指数。两个端点各自的存在性结论均不推出另一个完整结构命题。现有桥的已有迁移不重复写为本包资产，也不把其宽泛源存在性强称指定实例的来源。

## 5. 交付范围与剩余义务

本包给核心准确 isolated-after-review 覆盖，保一条有完整具体结构说明的语境边。对三个已指明族的比较已完成；没有需要新队列承接的未付对象对，没有把一般缺少 InfDegreeOne↔交域桥描述成已证明不可能。若后续要把交域族改成∞度1，必须另给新构造并同时支付配置合法性、整数上界和全部新增人数；当前三个对象没有这一保证。
