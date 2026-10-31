---
id: fair-allocation/personalized-bivalued-efx-completion-exact-report-and-controls
kind: computation-resource
type_tag: 计算
title: 个性化双值EFX补全报告的全分配与边界
status: finite-exact-frozen-report; monotone-route-obstruction-only; no-new-generator-run
summary: 全字段保存243分配基例、八族点、三个边界及三个退化控制；utility/strict dominance/每件删除EFX和普通整数PO分别解释，不把completion_failure改写为无EFX+PO。
legacy_ids: [SEL-PB-EFX-MONOTONE-COMPLETION-OBSTRUCTION-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/personalized_efx_completion_independent_20261020.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/personalized_efx_completion_independent_20261020.json
---

# 个性化双值EFX补全报告的全分配与边界

## 模型和每个布尔字段的含义

三名代理、五件不可分goods，全分配，无charity。可加估值行

$$v_0=(1,1,1,a,a),\quad v_1=(1,1,b,1,1),\quad v_2=(1,1,c,c,c).$$

目标assignment为$(1,1,2,0,0)$：每个位置表示该物品的接收代理，均**零基索引**。故目标包是$X_0=\{3,4\},X_1=\{0,1\},X_2=\{2\}$，效用$(2a,2,c)$。

EFX逐个observer $i$、recipient $j$和每件$g\in X_j$检查$u_i(X_i)\ge v_i(X_j\setminus\{g\})$；删的是比较包的每一件，不是任选一件。程序也包括零值物品，不自动改成只删正值的另一约定。普通PO的比较域为**所有整数全分配**，不是fractional PO或仅与EFX分配相比。

严格支配为所有人效用不降且至少一人升。报告completion_failure精确表示：
目标有至少一个严格Pareto支配者，且**所有**这些支配者都非EFX。若无支配者（目标本身PO）则为false；若有一个EFX支配者亦false。这不是实例中不存在EFX+PO。

报告identity为SEL-PB-EFX-MONOTONE-COMPLETION-OBSTRUCTION-v1，python=3.12.14，arithmetic为fractions.Fraction/full assignments，scope明确独立有限核验，解析参数族证明另立。这些是冻结报告属性，本批没有重跑生成器或声称当前运行环境。

## 基例：全部顶层/支配者字段

$(a,b,c)=(2,3,4)$，agents=3、goods=5、all_allocations=$3^5=243$，efx_allocations=21、efx_po_allocations=13。目标效用$(4,2,4)$且target_is_efx=true。

全部严格支配者只有以下两份，均utility=$(4,3,4)$、efx=false：

$$Y^{(1)}=(0,0,1,0,2),\qquad Y^{(2)}=(0,0,1,2,0).$$

两者violations都恰为$(2,0,0,\text{“5”})$与$(2,0,1,\text{“5”})$。四元组依次是observer、recipient、removed-good、观察者对剩余包的价值；“5”不是效用差或recipient自己的效用。代理2自身四，而删对方低值物品0或1后仍看见$4+1=5$，故违反EFX。于是completion_failure=true。

全域13份EFX+普通PO分配是报告同时保存的正存在证据，直接防止把本方法障碍升级成EFX+PO不相容。

## 解析参数族为何只有两支配者

[既有完整参数笔记](../审查/个性化双值EFX效用单调补全障碍--审查.md)在$3/2<a\le2,b\ge2,c>2$且$a<2$或$b>2$给路线反例。目标EFX因比较包至多两件，删除一件后高值至多$c$，代理2自身恰$c$，其余约束亦直接成立。

任何弱支配且至少一人严格改善的全分配中，每人非空，代理0最多三件且至少值$2a$。若其只有两件，唯一达到者是$\{3,4\}$；剩$\{0,1,2\}$中代理2为达$c>2$必须拿2，代理1为达二必须拿0、1，恰原目标，不能严格改善。因此代理0拿三件（全低值三件价值三小于$2a$），其他各一件；代理1唯一单件达到二的是2，代理2必须拿3或4，所以仅上述两候选，效用均$(a+2,b,c)$。

$a\le2,b\ge2$保证不降，$a<2$或$b>2$保证严格；代理2删去对方低值物仍见$c+1>c$。这解释参数族结果，不靠八个格点外推。任何逐人不降路径的EFX+PO终点都须弱支配目标；同效用终点也因目标有支配者而非PO，所以这条单调补全路线失败。允许改变起点或效用回退的存在/算法问题未被否定。

## 八个family_checks完整记录

这里只报告每点的obstruction、dominators个数及efx_po；这些行没有保存各点全部EFX数或所有分配，不能补称它们都含21个EFX。

| a | b | c | obstruction | dominators | efx_po |
|---|---|---|---|---:|---:|
| 7/4 | 2 | 5/2 | true | 2 | 13 |
| 7/4 | 2 | 4 | true | 2 | 13 |
| 7/4 | 3 | 5/2 | true | 2 | 13 |
| 7/4 | 3 | 4 | true | 2 | 13 |
| 2 | 2 | 5/2 | false | 0 | 16 |
| 2 | 2 | 4 | false | 0 | 16 |
| 2 | 3 | 5/2 | true | 2 | 13 |
| 2 | 3 | 4 | true | 2 | 13 |

对应原代码仅对这个格点集assert obstruction iff($a<2$ or $b>2$)。两个false行是目标本身PO，不能解释成“存在改进但改进可EFX”。

## 三个boundary_checks的全部嵌套结果

每行agents=3、goods=5、all_allocations=243、target_is_efx=true。

| 参数(a,b,c) | 目标效用 | efx_allocations | efx_po_allocations | dominators | completion_failure |
|---|---|---:|---:|---:|---|
| (3/2,3,4) | (3,2,4) | 21 | 13 | 2 | true |
| (2,3,2) | (4,2,2) | 24 | 14 | 3 | false |
| (2,2,4) | (4,2,4) | 33 | 16 | 0 | false |

第一行的两支配assignment仍为$Y^{(1)},Y^{(2)}$，utility均$(7/2,3,4)$、efx=false，violations均$(2,0,0,\text{“5”}),(2,0,1,\text{“5”})$。该特定$a=3/2$点仍障碍，不足把严格参数族范围整体扩张。

第二行前两份assignment仍为$Y^{(1)},Y^{(2)}$、utility=$(4,3,2)$、efx=false，violations中的剩余值改为“3”。第三份为$(2,2,1,0,0)$、utility=$(4,3,2)$、efx=true且violations为空；它让代理2拿两个低值物0、1达到$c=2$，正是$c>2$承重条件松开后出现的新支配者。故failure=false。

第三行dominators为空，无嵌套utility/violations被省略：原目标已PO，所以failure=false。这与family重复的(2,2,4)记录相容。

## 三个degenerate控制

报告三行均没有target字段、dominators或completion_failure；它们只检查通用audit计数。输入由对应代码补足，不冒称JSON本身写了矩阵。

| 代码输入 | agents/goods | all_allocations | efx_allocations | efx_po_allocations |
|---|---:|---:|---:|---:|
| 一人、空goods：$[[]]$ | 1/0 | 1 | 1 | 1 |
| 两人两件、全零：$((0,0),(0,0))$ | 2/2 | 4 | 4 | 4 |
| 一人两件：$(1/1000003,0)$ | 1/2 | 1 | 1 | 1 |

一人只有一份全分配，空比较真空；全零任何分配同效用、无严格支配，故全部普通PO。Fraction保证小正有理值不被舍为零。

## 生成器、独立性和读取边界

4034B已清洗生成器本批全文比较：标准库Fraction/itertools/json/platform/pathlib，无scout导入；逐全assignment造包/效用，逐每件删除找所有violations，再对所有整数assignment做严格支配检测，所以EFX+PO是在全部分配域求PO。main调用base1、family8、boundary3和degenerate3，共15次audit；三人五物12次中仅10个不同参数点（base和一个边界与family重复），按调用累计$12\cdot243+1+4+1=2922$分配记录，不能当2922个不同实例。

本批未重复运行该已清洗generator。报告全部6620B/字段已实际读，目标/所列支配者及violations与代码和解析族逐项比较；243/21/13等穷举总计按**冻结有限报告**保留，不虚称本批重新枚举全部分配或重跑其已完成源。原JSON不含源hash/命令/输出时刻，本批[来源manifest](../../../../tools/evidence/retired-final-independent-reports/source-manifest.json)及支持manifest绑定实际冻结版本，scope独立不等外部审稿或形式化。

旧[三模型程序处置](../审查/三值探针输出与公平效率边界三源处置--审查.md)还含两代理WEFX/fPO和三值chores，三者不合并。这里仅补主报告全部数值/嵌套数组、边界意义与同一模型的自足数学；原一般EFX+普通PO问题、新颖性、任意参数区间的计算分类仍独立。[原件与逐字段去向](../../../../tools/evidence/retired-final-independent-reports/README.md)。
