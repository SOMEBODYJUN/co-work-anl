---
id: "unrelated-machines/support-safe-load-directions-versus-config-point-regeneration"
kind: "review"
type_tag: "审查"
title: "支撑安全负载方向与CONFIG点再生的不同义务"
status: "local-obstruction-and-one-step-candidate; no-iterative-algorithm"
summary: "保conformal支撑论证、全正三任务例、可计算非circuit泛型一步候选及位复杂度；不把支撑存在当成保持CONFIG或提取原子。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-56ef7110b0a749ac8b85029bd8c6dd61/support_safe_motion_and_point_regeneration_questions.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/unrelated-machines/R-56ef7110b0a749ac8b85029bd8c6dd61/support_safe_motion_and_point_regeneration_questions.md"]
---

# 状态与问题身份

源是“不进入可靠Claim账本”的探索桌面：给定普通UM的真实T调度凸包点，怎样安全删端、保持CONFIG、再生下一点，是三个不同义务。本页保存局部conformal论证、三任务障碍和非circuit一步候选；[单环给定点及未来扩域](真单环给定点分解拒绝与低停车扩域候选--审查.md)、[整数前缀证书](整数前缀槽预算的共同证书与搜索缺口--审查.md)分别保存同源其余数学，不能将48行原稿只归为一种失败模型。

用完整指派坐标x，固定0/1端保持，正端图指xₑ>0的原有限资格。真实原子σ是每件任务恰一次的实际峰≤T整数分配，不能用行内CONFIG配置代替共同原子。

# Conformal只给支撑，不负责下一点

假设x确在同一当前支撑的真实T调度凸包。每台分数负载恰T的机器，所有正权真实原子都恰负载T：其各原子负载≤T，平均等于T。令A保护任务守恒行及这些紧负载行，则σ−x∈ker A。标准同符号分解可逐次选核中支撑极小方向并消去至少一个非零坐标，写成与σ−x conformal的circuits之和；此处方向不必计算到未知σ。

任一这样的非零conformal方向d取最大箱步，若σₑ=1而0<xₑ<1，则σₑ−xₑ>0，conformality迫dₑ≥0，故这个实际原子的正端不会被删为零；固定坐标也相容。于是某个目标原子仍在新正支撑内。

这不提供未知σ、向它的方向选择、松负载行的分数可行性、CONFIG保持、原子提取或迭代点再生。仅去掉松Q/Z行也不能修复已核坏单环：那个方向的动端全在G，子矩阵未改变。存在保好支撑的方向与任意circuit安全不是一个命题。

# 全正时间三任务：所有负载circuits都离开CONFIG

两机相同，任务h耗1、a与b各耗1/2，T=1。总工作2，实际T调度只有h|ab及交换。等权平均每任务去机1概率x=(1/2,1/2,1/2)。CONFIG也必须每台满载，正配置只可能{h}或{a,b}；列守恒迫整个CONFIG投影恰为
\[
(t,1-t,1-t),\quad0\le t\le1.
\]
消去任务行后，保护两紧负载行的核为
\[
u_h+(u_a+u_b)/2=0.
\]
其非零支撑极小circuits只动两件任务，而CONFIG线段非零切向(1,−1,−1)动三件。因此任何非零负载circuit步都会立即离开CONFIG。

例如d=(1,−2,0)，最大正步1/4到(3/4,0,1/2)，两行分数工作仍1；机1支持h，机2支持a,b，仍有实际h|ab，但点不在CONFIG线。源特别保这个最小正时间例，不把其他powers族或别人的机制整类认成新定理。

# 非circuit泛型方向的一步候选

仍假设x确在真实T凸包。A只保护所有正权真实原子共同满足的行，并限制当前固定0/1坐标。取活坐标q个，0<xₑ<1，核基N，维数k>0；d=Nu。两种边界形式是
\[
\ell_e(u)=-\frac{(Nu)_e}{x_e},\qquad
r_e(u)=\frac{(Nu)_e}{1-x_e}.
\]
按**整个线性系数向量恒等**分组，选择u使非恒等形式取值互不相同。沿d的正向最大步由所有形式的正最大值决定，只命中一个恒等组；负向等价看−u，也命中一个组。

对正端某个命中边界，x的真实分解中存在原子σ在该活bit取那一边的0或1，否则其平均不能严格在(0,1)。写σ−x=Nv；该边界形式在v上为1。组内形式作为线性函数恒等，故在同一个v上都为1，迫同一个σ达到全组边界。新点除了这组没有其他活端碰边，故其支撑保留这个σ。负端同理，两个端可以保不同原子。该论证不要求知道σ，也不输出它。

可确定性选u(t)=(1,t,…,t^(k−1))。任意非恒等差给一个非零次数≤k−1的多项式，至多k−1根。2q个形式的差至多binom(2q,2)，扫描
\[
1\le t\le\binom{2q}{2}(k-1)+1
\]
必找到避碰值。精确有理核消元、幂的位长O(k log t)、组判等和端点运算均按显式输入总位长多项式。k=1无非零差多项式的根；若无活坐标或核零，则没有此非零移动义务。真实分解且有活bit时，各活bit的核行不恒零。

在三任务例取d=(1,−19/10,−1/10)，最大步分别±5/19，两个端点是
\[
(29/38,0,9/19),\qquad(9/38,1,10/19).
\]
各保一个实际T原子的支撑，却都不在CONFIG线。该例真实凸包方向(1,−1,−1)恰使非恒等边界取值碰撞，泛型方向会离开它。所以可计算的一步支撑安全远不等于可重复舍入。

# 证据、原先验与接续缺口

本批一次新Fraction审计枚举这个三任务例的全部8份分配、核仅两T原子、三个端点的逐机负载/实际支撑和精确CONFIG线排斥。它没有验证一般方向算法、CONFIG oracle或完整迭代。原稿的circuit_safety/global_representation是不同内部研究来源；root已读作者短稿、反算分数，但泛型候选没有声明先行独立完整审查，不进入current。本轮已读这里列入比较清单的相关正文，不重演盲审身份。

一般输入如何产生共同点、方向/批更新如何选、下一轮如何保持或再生真实输出意义的点、实际全机负载如何控、FAIL怎样sound及统一位复杂度，都仍开放。局部菜单、每模式流、价格或负载核不能自动闭合。原文见[48行探索桌面](../../../../tools/evidence/um-missing-one-pin-kernel-primary/original/61a03c090144ca4e8673.md)。
