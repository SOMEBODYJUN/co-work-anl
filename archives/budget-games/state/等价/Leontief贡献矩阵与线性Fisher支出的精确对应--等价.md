---
id: budget-games/leontief-public-profile-linear-fisher-spending-equivalence
kind: equivalence
type_tag: 等价
title: Leontief贡献矩阵与线性Fisher支出的精确对应
status: proved-equivalence; exact-algorithm-import; known-interface
summary: 同估值同预算的public Leontief NE与private linear Fisher支出逐矩阵对应；完整处理退化、有理缩放与实际策略输出，不以既有接口重构主张新算法。
legacy_ids: [NE-FISHER-TRANSFER-v1, NA02]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/leontief_fisher_known_interface.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/leontief_fisher_known_interface.md
---

# Leontief贡献矩阵与线性Fisher支出的精确对应

## 输入与要输出的对象

有限$n,m\ge1$。估值$v_{ij}\ge0$、预算$b_i\ge0$均二进制有理，$\sum_i b_i=1$；每个正预算者的估值行至少有一正项。玩家$i$选择$X_{ij}\ge0,\sum_jX_{ij}=b_i$，总量$\delta_j=\sum_iX_{ij}$，public效用

$$U_i(\delta)=\min_{j:v_{ij}>0}\frac{\delta_j}{v_{ij}}.$$

每个人只改变自己一行，效用取决于共同总量。目标是**精确有理NE贡献矩阵$X$**，不是仅$\delta$、极限点或近似NE。

先删零预算行，最终补零。再删所有正预算者都零估值的列，最终补零列。保留的每行/列各有一正项且$b_i>0$；$n=1$或$m=1$无须另排除。删列至少保持一个所需NE：在剩余问题构造NE、补零后，原玩家投向无价值列不能改善。事实上任一NE中正预算者不会支出到这种列，见下引理。总预算$B>0$未归一时，先将预算除$B$，最终把$\delta,X$乘$B$；总预算零时唯一贡献矩阵全零，无需市场调用。

## 临界支持引理

令$T_i(\delta)=\arg\min_{j:v_{ij}>0}\delta_j/v_{ij}$。**$X$是NE，当且仅当每行的正支出都在$T_i(\delta)$。**

必要性：若$i$在非临界$z$上正支出，取足够小$\varepsilon>0$从$z$挪出，按$v_{ij}$比例分给全部临界$j$。全部临界比值严格提高；有限个非临界正估值项在旧效用之上有严格间隔，故可取$\varepsilon$小到它们仍严格在旧效用之上。若$v_{iz}=0$，该减少本就不影响效用。因此严格改善，矛盾。

充分性：严格提高效用必须增加每个临界项目总量，亦即增加自己的每个临界坐标。她已把全预算放在这些坐标上，不能同时增加其和。

此外任一NE满足$U_i(\delta)\ge b_i/\sum_jv_{ij}>0$：将自己预算按估值比例分配即可保证该值，其他行非负。如果某保留列$j$有$v_{ij}>0$，则$\delta_j\ge v_{ij}U_i>0$。这正是逆映射所需的分母正性。引理不使用克隆，不限等预算。

## 同矩阵linear Fisher合同

构造private市场：同样的买家、货物、预算和矩阵$v$，每种货物供给一，买家$i$的private效用为$\sum_jv_{ij}y_{ij}$。保留列的均衡价格$p_j>0$；一列有正估值且其买家预算正时，零价使线性需求无有限最大值，故不能为均衡。令$X_{ij}=p_jy_{ij}$为**货币支出**。市场均衡恰满足

$$X\ge0,\qquad \sum_jX_{ij}=b_i,\qquad \sum_iX_{ij}=p_j,$$
$$X_{ij}>0\Longrightarrow j\in\arg\max_k\frac{v_{ik}}{p_k}.\tag{F}$$

花完预算来自非饱和线性偏好，列和表示货物恰好售完。正估值项上最大bang-per-buck等于最小$p_j/v_{ij}$；零估值项不可能最大。

**Fisher到public。** 输出原支出矩阵$X$，置$\delta=p$。两项守恒保证原预算、总量；(F)正是临界支持引理，所以是NE，且$\sum_j\delta_j=1$。

**public到Fisher。** 对任一NE，上一节保证所有保留$\delta_j>0$。令$p_j=\delta_j$、$y_{ij}=X_{ij}/\delta_j$。每列$\sum_i y_{ij}=1$，每行支出为$b_i$，临界支持就是(F)。线性买家在最高bang-per-buck上花完钱，故最优，市场清算。

所以这是**spending-matrix层面的双向等价**。保留人数、项目数、估值零模式、原预算；无克隆或分母人数膨胀。private效用$A_i=\sum_jv_{ij}y_{ij}=b_i\max_jv_{ij}/p_j$，因此public效用为$U_i(p)=b_i/A_i$；两者不能直接相等。

## 精确加权例子

取$b=(1/3,2/3)$，$v_1=(1,0),v_2=(1,1)$。Fisher价格$p=(1/2,1/2)$，货物分配$y_1=(2/3,0),y_2=(1/3,1)$。两列各和一，两行支出分别为原预算，第二人对两列bang-per-buck相同。

public贡献应为逐列乘价格：

$$X_1=(1/3,0),\qquad X_2=(1/6,1/2),\qquad\delta=(1/2,1/2).$$

临界支持逐行成立。private效用$A=(2/3,4/3)$，public效用$U=(1/2,1/2)$，满足$U_i=b_i/A_i$。直接把$y$当$X$会违反预算，不能省略这一步。

## 精确求解器的导入与位复杂度

数学对应本身已证明。算法结论另明确导入合同：一个对整数非负线性估值、正整数预算、每行/列非空的Fisher市场，返回精确均衡价格及支出，算术次数与中间有理位长均受多项式控制的求解器。主源指向Orlin2010的强多项式版本；本页没有重证或重新实现该外部算法。

有理输入令$Q_b$为预算分母乘积，$e_i=Q_bb_i$；令$Q_v$为估值分母乘积，$V_{ij}=Q_vv_{ij}$。也可逐行清估值分母。估值的全局或逐行正缩放不改变(F)；预算同乘$Q_b$只使价格、支出同乘$Q_b$。整数市场输出$(P,Z)$后返回

$$\delta=P/Q_b,\qquad X=Z/Q_b.$$

$\log Q_b,\log Q_v$至多输入各分母位长之和，整数化总位长仍多项式。导入求解器的强多项式算术保证加受控有理位长，给普通二进制多项式算法。不能只数实数运算、调用早期依赖$e_{\max}$数值的弱版本、或展开$Q_b$名玩家后声称位多项式。输出实际矩阵并补零行列，输入模型才完整闭合。

## 已知身份及接续

主源全文同时给出了直接推导、弱优化备线和文献核查。本页重构直接接口；[坐标恢复证明](../证明/Leontief对数规划的有理坐标恢复接口--证明.md)保留较长备线，[文献页](../文献/Leontief精确接口的Fisher覆盖与凸优化来源--文献.md)逐版本说明Brandt、Tao–Zheng和Orlin的既有覆盖以及实际阅读边界。这里不把母论文仍写open或内部独立重推当成新颖性。

NA02“首次weighted Leontief exact bit-poly新算法”按该历史核查已退休；完整模型与恢复接口仍可作学习/查重资产。若要新研究，须另给未被该同矩阵市场合同覆盖的任务与证据。本批未访问外部论文或核验最新版本，文学事实是2026-10-20主源报告，数学对应则在此自足重证。原件及处置见[证据](../../../../tools/evidence/cloning-leontief-potential/README.md)。
