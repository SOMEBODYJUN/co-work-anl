---
id: "facility-games/common-many/restricted-identical-link-range-preserving-nashification-import"
kind: "lemma"
type_tag: "引理"
title: "受限同链Nash化的双端负载保持导入"
status: "primary-source-UBF-and-stage-flow-checked-range-derived-no-canonical-implementation"
summary: "实际读取STOC2004 Cor4.3与完整§4阶段流，联合Th4.7由子实例双端保持归纳推出RANGE；正有理缩放与分量版明确。外部算法导入不等于本仓软件交付。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:learning/08_reading_list.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:learning/08_reading_list.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:learning/reviews/20261010.json#reports.blind_core"
external_refs:
  - "https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf"
  - "https://cgi.csc.liv.ac.uk/~gairing/publications/2009-tocs.pdf"
---

# 受限同链Nash化的双端负载保持导入

## 输入与准确结论

有限m≥1家有标签的相同单位容量机器，逐名正二进制有理不可拆任务w_i，每人有非空允许集A_i；给一份可行纯初态s。任务成本为所选机器的实际总负载L_f，改去g的成本为L_g+w_i。则已有受限同链Nashification算法可在联合输入位长多项式时间输出原完整允许游戏的精确纯NE t，且

\[
\min_fL_f(t)\ge\min_fL_f(s),\qquad
\max_fL_f(t)\le\max_fL_f(s).
\tag{RANGE}
\]

可分别在客户—允许机器二部图的每个连通分量运行，使每个分量分别保持这两个端点；孤立空机器仍计入其负载0，空任务游戏直接返回。这里机器数m是显式标签设施数，不能把物理站点q家合并为速度q而不改客户自重成本。

本页导入的是Gairing–Lücking–Mavronicolas–Monien已发表算法的正确性与运行定理，并从实际阶段赋值流程和单次UBF不变量补出双端保持。它不是本项目新发明的调度算法，也没有交付其规范源码或运行该算法。

## 原文定位与双端保持的归纳

本批已实际读取[作者STOC2004会议稿](https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf)§4的Corollary4.3、Theorem4.5、完整Nashification阶段/递归/扫掠描述和Theorem4.7；并读[作者期刊稿](https://cgi.csc.liv.ac.uk/~gairing/publications/2009-tocs.pdf)§2模型及§6/Theorem6.5。后者明确从任意给定分配输出NE、最大负载不增及O(rmS(logW+m²))，但单看该定理的makespan结论不能推出最小值保持。

会议稿Cor4.3（工具PDF第6页；Nashification描述和Th4.7接PDF第7–8页）对一次Unsplittable-Blocking-Flow调用，直接给调用链接集上的最大负载不增、最小负载不减。其原式为max_j δ_j(β)≤max_j δ_j(α)及min_j δ_j(β)≥min_j δ_j(α)。完整算法的赋值改变来自这些UBF调用：首阶段对当前实例作阈值二分，必要时按互补链接/任务集合递归；后续阶段在活动块上扫掠、调用UBF或递归二分。更新Low/Up、块的分割/合并、排列及重新拼接本身不搬动任务。算法中没有另一种不受Cor4.3控制的赋值重置。

设某一次真正改赋值的调用作用于链接子集B，调用前全局最小/最大为a,b。B内所有当前负载已处于[a,b]；Cor4.3使调用后B内每个负载仍介于调用前B内的最小、最大，故仍在[a,b]。B外赋值不变。因此全局最小不低于a、最大不高于b。二分若从同一输入测试多个调用，每个被接受或返回的赋值均有同一端点保障；递归对子块同样归纳，重组只拼接已有赋值而不改变负载。

以上对子实例调用及重组的双端归纳是本批根据实际算法流程作出的推断，不是将Th4.7的文字改成它未单列的MIN结论。由所有有限阶段归纳，从初态到最终NE始终保持原端点。NE正确性和多项式调用/运行界由会议稿Th4.7（r种整数权、总允许关联A，O(rmA(logW+m²))）导入，不在此重证其blocking-flow数据结构。期刊版把允许关联总大小写S，Th6.5的对应输入输出一致。由此得到(RANGE)，而非从“最大值不增”单句猜最小值。

## 有理位长与分量版

对正有理输入乘全部输入分母积D。logD不超过分母位长总和，所有新整数权及总W的对数由原输入位长多项式控制；r≤n，允许关联总大小显式计入。调用整数算法的算术数位、二分深度和运行定理因此给位多项式合同，输出只是任务机器标签；除回D不改变纯NE比较和两个端点不等式。这里没有按D或W的数值枚举任务。

客户—允许机器关联图分量之间没有合法任务偏离，各分量初态仍可行。逐分量调用上述算法，保持各分量最小/最大并得到各自完整NE；拼接即全局NE。空机器分量无需调用。故冻结普通游戏的初始分量最小负载μ_C可以作为最终下界，与独立强制池η取max。

## 在现行设施接口中的作用及限制

已有MAX合同足以做普通设施受帽离轨和冻结η基本版。本页双端导入另支持：AD首轮LPT所有负载≥γ后保持该在轨收益下界；冻结残余组件μ_C下界强化。其余前提仍须实际验证：每名残余客户有原初普通机器，冻结客户全部外部比较，偏离者普通，重新放回冻结设施后核全原动作。RANGE不生成成功LPT/装箱证书，也不从任意坏在轨NE造因子二续局。

原审查页记录此前作者PDF不可读，RANGE未核，是当时的准确证据边界。本批新增可读主源和上述数据流归纳来接续，未修改旧页或将其旧失败描述为错误。当前canonical pure_improve仍是有限严格改善，不是该文献算法；一般盒在轨选择的总位多项式时间仍开放。本文没有据此升级SC-PHI-E/A、一般异构2、EPTAS、外审或优先权状态。
