# Unit-home 外层的精确保值：learning 确认

本记录只确认一个直接重构，未登记新 Claim，不主张全球新颖性，也不提供一般 UM 算法或困难源。2026-10-18 的选择性检索覆盖 `research/current/unrelated_machines` 内 home/outer/helper/unit 关键词、`research/unrelated_machines/CLAIMS.md` 的身份/保值关键词，并实际核对既有 normalized-flat→state-dummy SC 值桥及 normalized 菜单树/资源路径的相关正文。未在这些检索结果中找到下述完整 unit-home 恒等桥；这不是对全库每一字节或外部文献的否定性认证。既有标准 selector 思想和 `OPT=2−V` 均为已知依赖。

## 输入、构造与值

令 Q 为任意完整显式 normalized-flat 菜单：有 m≥1 个 groups，每组至少一个 indexed state，每个 state 的非负二进制有理系数总和一。旧资源宇宙记 B。零 incidence、重复 indexed states、inactive states 和 unused resources 均保留。同一 state 不重复列同一 resource。记旧总 states、listed incidences、resources 数为 S、I、U。

为每旧 group g 建立一个新资源 h_g，彼此不同且不在 B 中。旧 group 改名为 helper H_g：原 indexed states 完整保留，另添 own indexed state，其唯一 incidence 是在 h_g 上的系数一。再加 outer O_g，只有一个 indexed state，唯一 incidence 同样是 h_g 上系数一。无其它 groups。记新菜单 Q⁺。因此 k=m，每 outer 只有一个 home，w_g=1，ν=1；helper fallback 恰是任意原 normalized 菜单。

对不交资源 bundles 的最大最小 normalized 菜单质量，严格有

\[
V(Q^+)=V(Q),\qquad \operatorname{OPT}_{UM}(P(Q^+))=\operatorname{OPT}_{UM}(P(Q)).
\]

原 allocation 直接给各 helper，全部新 homes 分给对应 outers，故新 minquality 不小于原值。反向，任意新 allocation 若 minquality b>0，每个 unit outer 都必须取得自己的 h_g；helper 无法使用 own state，故其在旧 B 上某个 fallback state 的质量至少 b，直接删去 outers/homes 得原 allocation。若 b=0，所需相反不等式由原 V≥0 成立。这涵盖 V=0 与 V=1，无正值 promise。

## 完整原任务的双向转换

普通矩阵 P(Q) 的定义是每 state 一 private machine、每资源一 resource machine；每 group 一 selector，只在本组任一 private machine 时间一；每 listed incidence 一独立 job，在其 private machine 时间 p、在其资源机时间一，其他端点为∞。未选 states 和零任务仍是原任务。

原矩阵的全部旧 machine/job 子矩阵逐项不变。但旧 selector 多获得一个新的 helper-own private endpoint；因此本构造不应描述成单纯添加互不相交的固定任务。

给任意旧合法调度 σ，保全部旧 assignments；新 helper-own incidence 留在其新 private machine，新 outer selector 留在 outer private machine，新 outer incidence 送 h_g。所有新机器负载恰一。旧 selector 给 C(σ)≥1，故 C(σ⁺)=C(σ)。

给任意新合法调度 σ⁺，若 C(σ⁺)<2，outer selector 固定其唯一 private machine，迫 outer incidence 送 h_g；h_g 已收一枚 unit，迫 helper-own incidence 留其 own private machine；该 private 已有 unit，迫 helper selector 在某个原 fallback private machine。直接限制到全部旧 jobs/machines 即是合法旧调度，且负载不增。若 C(σ⁺)≥2，则输出原全-private baseline：各 incidence 留原 private、selector 任取一个原 state，峰至多二。两种情况均给 C(σ)≤C(σ⁺)。这独立证明完整矩阵 OPT 相同，包括 OPT=2，不在 C=2 时使用 unit 独占。

## 显式规模与边界

Q⁺ 的 groups、states、incidences、resources 分别为 2m、S+2m、I+2m、U+m。因此普通矩阵有 S+U+3m 台机器、I+4m 枚 jobs、S+2I+6m 个 finite endpoints；稠密矩阵规模亦为输入位长的多项式。只复制原有理数并添加 0/1/∞，所有转换均确定性总位多项式，不调用 OPT、allocation oracle 或未知目标。原零 jobs 和 unused resources 原样保留。

m=0 的空实例不在此非空 normalized-flat 值定义内；其 UM 全 jobs 为空时单独输出空调度、OPT=0，不能套 `2−V`。本记录也未把任意外部 UM 矩阵变为 normalized-flat Q。

因此，把多 single-state outer 的 tiny 条件完全删去，即使只允许每 outer 一个 unit home、一个 own-unit helper，也已包含完整任意 normalized-flat 菜单的精确值问题。它阻止把 ν=1 扩域视为免费相邻特例；未证明一般 normalized-flat 或一般 UM 的新算法/困难性。
