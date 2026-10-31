---
id: "unrelated-machines/qary-affine-menu-deficit-recoupling-two-source-review"
kind: "review"
type_tag: "审查"
title: "q 元仿射菜单缺项与重选两源精读"
status: "restricted-consistency-and-deficit-boundary"
summary: "两份 q-ary affine menu review 确认：任意非线性选态的粗投影有 near-full deficit/资源配额上界，coordinate-wise recoupling 在指定非空选择域内有精确差异与奇异层分析；这些结果只讨论菜单层的一致性与有限容量，不提供物理调度 decoder、一般 nonlinear 最优值或一般 UM 近二结论。"
source_refs:
  - "clean:ef47f56eb82860e83dc3"
  - "clean:c5bceece4104f6baf428"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/qary_affine_menu_near_full_deficit_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/qary_affine_menu_recoupling_consistency_review.md"
---

# 来源、读序与准确对象

`ef47f56eb82860e83dc3`（SHA `4821785cd24a141f790152752d3ca484ff78a1ac5d5d18f4741890795f84e1f2`）审 v2 `UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v2`；`c5bceece4104f6baf428`（SHA `f63a4e56fb17d2c564cdfb1cd4031eb44b658be07220479a8f3657066c081e1b`）审 v1 `UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1`。两源均 clean show 全文实读，导出与 manifest 在 `archives/unrelated-machines/tools/evidence/qary-affine-menu-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/qary-affine-menu-receipts-20261031.json`。review 记录明确先冻结 Exact、独立证明，再读作者 Proof；有限辅助矩阵/函数检查只属各审查者，不代签 root 运行。

# 1. v2 arbitrary nonlinear near-full deficit

v2 研究任意非线性 q-ary 选态菜单的粗 projection：给每 group 的若干 affine/Boolean state，研究资源度和可保留的 bundle/缺项。核心边界是 coarse projection 不自动提供逐坐标一致的物理菜单；q>2 的 affine 上界不应升级成所有 nonlinear projection 的 sharp optimum，更不应把 finite toy 矩阵当 near-two source。`strict 2d<q` 的限制是严格不等式，不能擅自加等号；选择域非空是修订后明确的量词条件。

审查确认：v2 使用新合同闭合旧 v1 q=3,t=3 未完成的缺口，但仍只证明受限 deficit/资源配额与状态计数；没有 free coherence、真实 shared-resource decoder、一般 nonlinear 最优值或 hardness。所有具体 Claim 的非空选择域此前已满足，修订只消除共用值恒等式的歧义，无数学方向变化。

# 2. v1 coordinate recoupling consistency

v1 `UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1` 分析 q-ary affine state 的 coordinate-wise 重选。bicriteria 精确读后保留：固定选项 A 下，rank/Hall、determinant 网格计数、cyclic 奇异层、所有 coordinate-f unions 可逐项核对；A−diag 与 `Π_a 1` 符号、characteristic 任意、`t=1`、全部未选 state jobs 均有明确边界。证明域要求选择族非空；不满足该前提的空选择域不能由该文静默覆盖。

重选/recoupling 的关键是逐坐标配额与全局一致性的差异：逐 coordinate 提供的资源支持不等于一个实际物理 menu 的共同 assignment。`C_sep` 是分离后上界/计数，不是原无约束实际 OPT；在没有一致性 decoder 时，不能把其数值写成普通 UM makespan 或近二 gap。

# 3. 与仓库其它 q-ary/菜单对象的关系

仓库已有 q-ary affine、笛卡尔菜单、coordinate quota 与 shared resource 的定理/反例；本批独有处置是把 v2 near-full deficit 与 v1 recoupling 的 exact scope、非空域修订和“粗 projection/逐坐标配额≠物理一致性”逐源记录。两源不替换 `q元仿射菜单重选的证明分工与受限域审查`，而是补充其 source IDs 和审读顺序。

与 unrelated-machines 的关系仅是菜单层接口：若未来能给出真实 assignment 的共同 resource decoder，有限配额可能成为条件 rounding 输入；当前两源没有该 decoder，不承担一般 UM-TARGET-v1 的正面或反面结论。它们也不接当前六人 SPE 客户覆盖目标，模型身份保持独立。

# 4. 软件、外部事实与缺口

本批没有生产实现、端到端调度运行或外部同行评审认证。源中提及的审查者有限矩阵/函数数量只作为其内部检查范围，不转写为本轮新证据。任何 Karp/菜单文献事实需按原始来源另核，不能由本 review 的有限检查承载。

未解决的数学义务包括：给定粗 projection 时的物理 shared-resource 一致性、非线性状态全局选择、跨坐标耦合的位多项式 decoder、以及若要用于 UM 的实际负载与所有原 jobs 回填。现阶段安全结论是受限 deficit/recoupling 边界和失败机制，不是一般 hardness 或近二算法。

处置为 `restricted-consistency-and-deficit-boundary`；引用时需同时保留 q、非空选择域、strict 约束、粗投影与 physical decoder 的区别，以及实现/新颖性/一般 UM 未认证。
