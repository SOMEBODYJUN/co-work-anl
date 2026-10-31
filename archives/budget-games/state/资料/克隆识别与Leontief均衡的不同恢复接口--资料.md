---
id: budget-games/cloning-recognition-and-leontief-fisher-ledger-contracts
kind: resource
type_tag: 资料
title: 克隆识别与Leontief均衡的不同恢复接口
summary: "逐来源保留克隆识别与Leontief均衡的不同恢复接口的精确模型、量词、关键论证和证据/版本边界，不升级外审或新颖性。"
status: cloning-internal-proof; fisher-known-tool-reconstruction; no-novelty-certification
legacy_ids: [BN-CLONE-v1, BN-CLONE-v2, NE-FISHER-TRANSFER-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/CLAIMS.md
---

# 克隆识别与Leontief均衡的不同恢复接口

对应三Claim的几何稿、coNP稿、版本审计及Fisher重构全文实读，root复核全文比较。它们共享预算聚合背景，却不是同一效用或复杂性问题。以下保源内部证明及已知工具的身份；文献版本和覆盖是原2026-10-20审计记录，本批没有重新联网认证当前文献或新颖性。原件见[证据](../../../../tools/evidence/retired-topic-claims/README.md)。

## min-of-linear克隆识别的全部量词

输入非负二进制有理$R\times m$矩阵$A$，效用$u_A(\delta)=\min_{r\le R}a_r\cdot\delta$，总预算一，$\delta\ge0,\sum_j\delta_j=1$。玩家按自己预算在$m$项目间贡献，效用看总贡献。CLONE-INVARIANT要求：**每个**整数$D\ge1$、$1\le k\le D$、任意有限外部玩家及其正有理预算（总和$1-k/D$）、任意外部效用，$k$个效用均$u_A$且各预算$1/D$的clones的**每个NE**，在合并这些clones、预算和策略取和后仍NE。不只是存在可合并NE；外部效用不需凹。

固定$\delta$，active行$I$给凹超微分$P_I=\operatorname{conv}\{a_r:r\in I\}$。正支出支持$S$最优，当且仅当有$g\in P_I$使$S\subseteq\arg\max_j g_j$。定义$U_\delta$为$\delta_j>0$且可由某个超梯度把$j$列为最大值的坐标。点态合并保持当且仅当存在**同一个**$g$令全部$U_\delta$最大。不同clones各自有一个$g$不够。

**BN-CLONE-v1**的有效识别为$2^R\operatorname{poly}(m,R,L)$。枚举非空active集合$I$；以正margin LP找各可正坐标$J_I$，平均各坐标见证可在同一active cell内让全部$J_I$同时正，同时保持外行严格间隔，因此无需枚举$2^m$支出支持。对每个$j\in J_I$用凸组合LP查能否成为最大坐标，得$U_I$；再查有无共同$g$令全部$U_I$最大。不可行时，同一有理$\delta$上给每个$j\in U_I$一个足够小等预算纯投clone，余量由全一线性效用outsider提供，得到真实NE而合并后非NE。$D$二进制压缩，不能声称显式打印指数多玩家仍多项式。浮点六手例不是精确有理算法实现。

**BN-CLONE-v2**只证明语言在coNP，不是hardness或complete。失败证书为active$I$、非空支持$S$、有理$\delta,z$、逐$j\in S$的凸组合超梯度$\xi^{(j)}$，以及共同LP不可行的Farkas向量。令$M_{(j,s),r}=a_{rs}-a_{rj}$，共同LP为$\xi\ge0,\mathbf1^T\xi=1,M\xi\le0$；证书$y\ge0,M^Ty\ge\mathbf1$方向不能反。正margin LP的BFS及Cramer/Hadamard界给所有有理数总位长$\operatorname{poly}(L)$，含把无理失败点替换为有理点。它不消去$2^R$或证明一般识别多项式。

## 精确反例与版本纠错

三项目效用$u=\min(2\delta_1+\frac32\delta_3,2\delta_2+\frac32\delta_3)$。两相同clone各预算$1/4$，分别纯投项目1、2，outsider预算$1/2$纯投3且只在乎3；总$\delta=(1/4,1/4,1/2)$。各clone效用$5/4$，自己的一个active线性分支给单方上界$5/4$，故为NE；合并预算$1/2$全投3使效用$3/2$，严格改善。Farkas toy取$I=S=\{1,2\}$、两单位行凸组合、$y_{(1,3)}=y_{(2,3)}=1$，精确得到$M^Ty=(1,1)$。

原版本审计指出该例反驳2509.08767v1 Lemma8.2的广凹性范围：总$L_1$小移动不保证由单clone的支出支持执行。其已审v3改为若干特定效用类并留一般分类；**本例不反驳已修v3**，也不否定Leontief类。可微凹效用的共同梯度使合并保持，是标准KKT推论；不可微的coordinatewise/global差异及active-face工具已有成熟优化背景。两项目时凹超微分的坐标差可插值到零，给本polyhedral类合并保持，但三项目反例不自动证明全部模型最小性。一般效用分类、tight complexity、禁形和新均衡算法后果仍未闭合。

## NE-FISHER-TRANSFER-v1：另一效用下的已知工具

给非负有理$v_{ij}$与正预算$b_i$、$\sum_i b_i=1$，每行至少一正项。public Leontief效用为$U_i(\delta)=\min_{j:v_{ij}>0}\delta_j/v_{ij}$。贡献矩阵$X$行和$b_i$，列和$\delta_j$。零预算行及对所有正预算玩家全零列可删后补零。

精确NE恰为正贡献仅在critical坐标$\arg\min\delta_j/v_{ij}$：若投非critical，可挪小量按$v_i$比例同时改善全部critical；反之全部预算投critical时无法同时增加它们。每人可保证$U_i\ge b_i/\sum_jv_{ij}>0$，故保留列在NE的$\delta_j>0$。

构造同矩阵$v$、同预算的private **linear** Fisher市场，goods供给一；价格$p$、数量$y$、spending$X_{ij}=p_jy_{ij}$。市场行支出$b_i$、列支出$p_j$、正支出走$\arg\max v_{ij}/p_j$，恰与public条件相同。两向映射是$\delta=p$、public策略$X=p\odot y$，反向$y_{ij}=X_{ij}/\delta_j$。不能把private数量直接当public贡献，也不能误接private Leontief。private效用$A_i$与public满足$U_i=b_i/A_i$。

原例$b=(1/3,2/3)$、$v_1=(1,0),v_2=(1,1)$，$p=(1/2,1/2)$，public两行为$(1/3,0),(1/6,1/2)$；private效用$(2/3,4/3)$而public均$1/2$。原说明按Brandt的NE/Lindahl、Tao–Zheng的同预算dual及Orlin精确linear Fisher接口记录为**已知工具重构**，因此NA02“首次weighted exact bit-poly算法”题淘汰，不因另一原文仍写open而升级成团队新解。

原备线weighted-log强凹恢复的分母、内球、oracle与坐标有理恢复合同仍保在完整原件，但不用它制造第二新算法。源审计还指出有理$u,\delta$不使几何平均目标有理：两效用$1/2,1/4$的几何平均$1/(2\sqrt2)$，不能用有限有理目标二分论证精确终止。此处只是局部证明步骤边界，不否定可由Fisher工具得到的结果。

这三ID分别是识别算法、失败证书复杂性包含、另一效用类的已知两向转移；没有从cloning识别推出Fisher算法、一般NE或新复杂性下界的已知边。内部重构、参与几何构建和原文覆盖审计各保历史独立性，不把本批阅读称新盲审或外审。
