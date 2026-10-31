---
id: "customer-attraction/true-deviation-optimal-matching-harmonic-lower-bound"
kind: "lemma"
type_tag: "引理"
title: "真实偏离最优匹配的调和下界"
status: "proved-fixed-strategy-bound; conditional-weak-matching-corollary-only"
summary: "任意固定完整策略零根背景下真实query匹配M≥[Q+(H−1)D]/m及实载加强；条件W/Q阈值与小人数应用分开，不借辅助harmonic收费或冻结尾。"
source_refs:
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-7eb35cf5aa0f402c892d23bc658a0639/weak_matching/harmonic_matching_floor.md"
---

# 对象与量词：主引理不使用SPE

`47b0b012b74895569094` 3904B/78行全文。有限单位客户、共同有限非空目录、m≥1名单位提供者，固定任意依全部有序历史的完整纯策略σ，**根无额外外生背景**。actual终局S_1,…,S_m、覆盖C、W=|C|。位置i的actual历史h_i与past负载b_i(x)固定，尚有r_i=m−i+1位。

V_i(T)是位置i在h_i强制合法T、后继继续原σ所得的真实最终收益，包括own-action query。不是冻结actual尾，不把σ按主题重新命名。比较m槽元组T_1,…,T_m允许重复/空主题，O为并集、Q=|O|，D=|O\C|、A=|C\O|，H_m=Σ_(r=1)^m1/r。定义
\[
 M=\max_{\pi\in Sym(m)}\sum_i V_i(T_{\pi(i)}).
\]
重复主题仍有不同槽索引参与排列。若σ为SPE，每行V_i(T)≤u_i，故M≤W；这个上界才用IC，下述下界不需均衡。

# 通用调和下界及完整证明

不管真实后继怎样响应，x∈T的最终负载≤b_i(x)+r_i，因此
\[
 V_i(T)\ge g_i(T):=\sum_{x\in T}\frac1{b_i(x)+r_i}.
\]
对带标签比较槽均匀随机排列，任一槽被配到i概率1/m，故
\[
 M\ge\frac1m\sum_{i,j}\sum_{x\in T_j}\frac1{b_i(x)+r_i}.
\]
对每个x∈O任选一个包含它的槽j(x)，只保留这槽贡献、其余非负；没有把比较重叠偷计为不同客户。于是
\[
 M\ge\frac1m\sum_{x\in O}\sum_i\frac1{b_i(x)+r_i}.
\]
总有b_i(x)≤i−1，所以分母≤m，内和≥1。若x∈O\C，全部actual前缀均不覆盖它，b_i(x)=0，内和恰H_m。因此
\[
 \boxed{M\ge[Q+(H_m-1)D]/m.}\tag{HM}
\]
固定外生背景若非零，逐行g仍可写，但b_i≤i−1及(HM)的这一基线不直接成立；不能把原零根引理无声用于任意带背景子局。

# 到净缺口的条件转换，及小人数的正确用途

Q−W=D−A，(HM)减去净缺口给
\[
 M-(Q-W)\ge Q/m-(m-H_m+1)D/m+A.
\]
Q>0时令q=W/Q，代D=(1−q)Q+A，精确得
\[
 \boxed{M-(Q-W)\ge\frac{1-(m-H_m+1)(1-q)}mQ
 +\frac{H_m-1}mA.}\tag{GAP}
\]
所以只要
\[
 q\ge1-1/(m-H_m+1),
\]
便有弱匹配M≥Q−W。右端为负只说明这个充分界不够，不能当真实M失败的反例。Q0时净缺口≤0而M≥0；m1时V_1(T_1)=|T_1|，不用比值，阈值0。

|m|H_m|足够W/Q|
|---:|---:|---:|
|1|1|0|
|2|3/2|1/3|
|3|11/6|7/13|
|4|25/12|23/35|
|5|137/60|163/223|
|6|49/20|71/91|

若T达到OPT，结合另外的m2福利比≥2/3、m3锐比≥3/5，可推出这些小人数的弱匹配助手；此是依那些已证结论的推论，不是主引理对任意σ也有相同比率。原稿用当时四人界750/1499说明未达23/35；本文只保这份工具自身未给四人一般应用，不把旧文引用当今日所有其它定理的唯一进度。五人half已独立另证，也不让本工具的163/223条件自动满足；恰六人一般弱匹配/half未由(HM)闭合。

# 保留actual客户负载的加强

令c_x为actual总覆盖次数，H_0=0。对固定x，考虑Σ_i1/[b_i(x)+m−i+1]。若相邻覆盖指示为0,1，交换成1,0只让b_(i+1)增加1，其余前缀不变；因此这个和只会减小。反复交换把c_x次覆盖放到最早位置。在前c_x项分母恒m，之后依次m,…,c_x+1，故最小和为
\[
 c_x/m+H_m-H_{c_x}.
\]
代前述逐客户单槽下界得到
\[
 \boxed{M\ge\frac1m\sum_{x\in O}
 [c_x/m+H_m-H_{c_x}].}\tag{LOAD}
\]
c0给H_m，c=m给1，包含所有边界。交换的是用于**下界比较的actual覆盖指示**，不是声称可交换真实SPE历史且仍均衡，也没有把每客户不同交换拼成一个新策略。

# 与其它调和对象、匹配和证据的分离

本对象的H_m来自真实query的剩余最多角色数；它不同于[静态调和收费](../资源/实际覆盖与重叠最优目录的静态调和边界--资源.md)中的Σ_x(H_(c+d)−H_c)，后者额外计比较元组重数。也不是[比较池随机保留](最优比较池的净交换与随机保留恒等式--引理.md)的L_i、辅助删玩家收益核、或旧FOMA冻结尾价格。它们的恒等式不替本真实V矩阵或其IC来源。

原同目录`harmonic_weak_matching_audit.py`被源报告用Fraction核m1..12阈值/代换及m≤8覆盖位置；本批未读/未跑那段代码，不能把MD的链接变成新程序实读、扫描或另一条一般证明。这里的任意m证明由均匀索引排列、非负单槽保留和相邻交换承担，不需数值实验或BI。只说明一个可复用下界，不声称新颖性、外审、一般弱匹配或half已经成立。
