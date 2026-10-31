---
id: bottleneck-knapsack/two-capacity-candidate-modules-and-fixed-k-target
kind: resource
type_tag: 资料
title: 双容量BMKP候选的三模块与完整目标
summary: "逐来源保留双容量BMKP候选的三模块与完整目标的精确模型、量词、关键论证和证据/版本边界，不升级外审或新颖性。"
status: whole-algorithm-candidate; three-conditional-modules-internally-checked; fixed-k-target-open
legacy_ids: [TS-BMKP-2CAP-APPROX-v1, GA-03-L1, GA-03-L2, GA-03-L3, SEL-BMKP-CONST-K-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/CLAIMS.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/CLAIMS.md
---

# 双容量BMKP候选的三模块与完整目标

物品有公共正有理重量$w_e$、非负有理利润$p_e$，有限非空背包容量属于$\{B_1,B_2\}$，$0<B_1\le B_2$；每物品至多一次、允许unused，所有背包容量硬满足，最大化$\min_jp(S_j)$。两容量值不等于两个背包，容量比无限制。它是中央优化，没有玩家偏离、延迟或NE；不能从旧拥塞存在界自动移来算法。

**TS-BMKP-2CAP-APPROX-v1**目标是每个固定$\varepsilon>0$的确定性总位多项式$(2/3-\varepsilon)$近似。完整候选和独立反方稿（含最终版本对齐）、VERIFICATION全文实读；模块内部完整推导不升级为总定理，软件未交付、导入结构引理与联合覆盖仍有审阅义务。本批没有执行旧玩具审计。原件见[总证据](../../../../tools/evidence/retired-topic-claims/README.md)。

## 三个分开验收的条件模块

**GA-03-L1：联合类型critical恢复。** 固定有限全局标签$\tau$，同标签在每容量有相同上舍入重量$u_t$和适用状态、利润同宽$\delta$桶$g\le p<g+\delta$、全局cheap/expensive标志一致。long的**全部昂贵物品**为critical，每long至多$K$件；short至多两件。已给互不交见证，long以$u_t,g$连同原cheap集合满足容量/利润式。每类型按所有long的总需求取全局最重$N_\tau$物品，替换critical后long标签式保持，short重量不增、利润损失$<2\delta$。

证明逐同类型配对旧critical中被换出者与较重换入者；后者只能在short或unused，不能藏在long的“非critical expensive”。放入long同型槽；若来自short，把更轻旧物放回，桶内每槽利润损失$<\delta$。两容量各自选最重可能重复同一物，只有全局联合需求的交换成立。模块不负责免费生成合法标签或初始结构。

**GA-03-L2：嵌套short matching。** 给未占critical的昂贵池、数量$m_1,m_2$和共同$Q>0$，加入$m_1+m_2$个零dummy。两物品若重量和$\le B_2$、利润和$\ge Q$则连边，小容量也可行者边权一，其他零。存在全部short的至多两物品分配，当且仅当存在大小$m_1+m_2$且至少$m_1$条权一边的matching。singleton补不同dummy；反向把任意$m_1$条small边给小包。固定基数最大权matching可解，**不是一般精确颜色Exact Matching**。$Q>0$排除dummy-dummy。

**GA-03-L3：允许discard的$4p_{max}$舍入。** 公共非负重/利、各包非负容量与目标，若LP满足$\sum_jx_{ej}\le1$、逐包重量$\le B_j$和利润$\ge t_j$，则可总位多项式输出互不交部分整数sets，容量不增、利润$\ge t_j-4p_{max}$，$p_{max}=\max(\{0\}\cup\{p_e\})$。

取残LP极点，固定所有一边并移除相应物品，删零。正真分数边数$E$、未完成包数$M$、紧物品行数$N$，每紧物品至少两分数边，所以$N\le E/2$，极点秩给$E\le N+2M$，故$E\le4M$。某包至多四分数边，结束该包仅保已固定整件，损失至多$4p_{max}$；删其分数边只放松其他物品约束，继续。每步固定物品或结束包，次数多项式，有理LP位复杂度另计。要求所有物品恰分一次会失败：一物重量二、两包容量一、各分数半可行而无完整整数分配。此例只反驳字面全覆盖子合同，不反驳母BMKP主定理；当前候选已自立L3，不依该歧义。

## 最终冻结的参数与已修异议

对阈值$T$用单向gap oracle：$OPT\ge T$必有枚举轮成功；成功仅保证输出利润$\ge qT$，不保证$T\le OPT$。归一到$T=1$并cap利润$\min(p,1)$。最终稿

$$\zeta=1/\lceil\max(100,20/\varepsilon)\rceil,\quad U=1-\zeta,\quad\gamma=U\zeta,\quad\delta=U\zeta^2,\quad K=1/\zeta,$$
$$q_{pre}=2/3-8\zeta,\qquad Q=2/3-11\zeta.$$

未知最优见证先把高利润包缩singleton，移除每包至多一heavy-cheap物品，损失小于$\gamma<\zeta$；余利润至少$U$，再以容量$B_t$、利润$U$缩放导入母Lemma8，逐项满足individual-profit及no-heavy-cheap前提。两容量子实例原物品互不交。重组后昂贵数超$K$可保任意$K$件，其利润至少$K\gamma=U$，并须检查profile/slack保持。

全局联合标签记录两容量各自状态/上舍入重与共同利润桶，类型数只依$\zeta$，不依容量比或包数。long的profile slack吸收至多$K$昂贵轻物舍入；同型槽交换用L1，noncritical expensive池用L2，严格$p<\gamma$池才可用cheap LP和L3，两池不抢物。正确猜测最终long$\ge Q-4\zeta=2/3-15\zeta$，short$\ge Q$；几何网格公比$1+\zeta$再损至多$\zeta$，得到$2/3-16\zeta\ge2/3-\varepsilon$的候选预算。

反方稿正文还保旧$q_{pre}=2/3-6\zeta$、$2/3-13\zeta$等，**末节已明确撤回为历史数值**，不能重新列作当前参数。profit cap、允许unused、cheap/expensive分池、昂贵数规范化、重cheap删除记账及单向oracle/几何网格旧异议已修；没有在最终对齐中重新逐行验完整新稿，不等于总证明通过。仍需母Lemma8输入/归一化/short/profile逐式核对、全部枚举轮联合覆盖、零OPT/空类别/无效标签/边界的完整审阅及通用实现与中间不变量核验。3000个L1、8192个toy pair等原局部证据不能替代它。

## 更大而未解的完整目标

**SEL-BMKP-CONST-K-v1**为proposed/open research target：每个固定整数$K\ge1$、固定$0<\varepsilon<2/3$，容量至多$K$种、各类包数任意、容量比无限制，公共正有理重/非负有理利；求输入位长多项式的硬容量$(2/3-\varepsilon)$近似，多项式次数可依$K,\varepsilon$，不暗加FPT要求。两容量候选不解$K\ge3$；固定某$K$的真正更低近似困难性是另一可能否定方向，单算法失败不够。

源母问题、自然两容量切片、三条件模块和总候选四层分别保留。原“内部独立重构”指谁核过哪个模块，不是外审或本批新盲审；新颖性与全文献开放性未认证。只有在同一标签/供给/利润/位长前提下才能拼接模块，第三阶段再写解释性关系，不从ledger摘要直接造总算法边。
