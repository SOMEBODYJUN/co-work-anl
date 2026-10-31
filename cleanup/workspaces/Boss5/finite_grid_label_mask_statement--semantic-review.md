---
source_id: "aee57c40a59da7343ff1"
source_path: "history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md"
source_sha256: "b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165"
source_blob: "12e1dccb8762e9e6d2baf010af542138b5781311"
status: "statement-only; independently reconstructed and author proof read-after passed"
disposition: "integrated"
target:
  - "archives/unrelated-machines/state/资料/显式XOS与福利舍入三源边界--资料.md"
  - "archives/unrelated-machines/tools/evidence/retired-xos-nsw-boundary-20261031/source-manifest.json"
---

# 有限格点 label-mask 对数势：语义清洗稿

## 来源与实际阅读

该冻结源是 1,982 字节的英文 statement-only 合同，提交路径为
`history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md`。
`clean show aee57c40a59da7343ff1` 已完整读取正文；冻结 inventory 给出的 SHA-256 是
`b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165`，
blob 为 `12e1dccb8762e9e6d2baf010af542138b5781311`，同一字节版本同时出现在
`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和
`main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

来源只给出精确命题和边界，没有作者证明、代码、运行输出、外部文献或 NSW 归约。因此它不能单独登记为“已证明算法实现”。同目录的
`c7285e5c3cc4ad1716ec` 独立 Exact-only 重构在同一模型上给出 PASS；
`c05060b2330f0a8d6978` 的作者 Proof v1 给出条件期望/格点 DP 证明；
`dfc2aa730b7a1fc9a905` 的作者 Proof 实际读后审查给出 PASS。三份相邻源均保持自己的来源身份，不能把 statement-only 源冒充作者 Proof 或独立实现。

## 精确数学合同

有限显式输入由以下部分组成：

- 显式的 (m)-件物品集 (U)，有限 agent 集 ([a])，标签 (0,1,ldots,L)，其中 (L\ge1)；
- 每件物品 (j) 的有理概率 (pi_{j,t}\ge0)，对所有标签求和为 1，且物品标签 (r_j) 相互独立；
- 每个 agent 的目标标签 (t_i\in[L])、子集 (S_i\subseteq U)、正二进制有理数 (V_i,
u_i)，以及 (j\in S_i) 上的非负权 (w_{i,j})；
- 一个正整数 (Q)，所有权是 (1/Q) 的整数倍，且每个 agent 的权重和不超过 1；集合外权重视为 0。允许空 (S_i)、零权和重复/无效标签概率。

给完整标签赋值 (r) 定义
[
W_i(r)=sum_{jin S_i}w_{i,j}mathbf 1[r_j=t_i],
qquad
Phi(r)=sum_{iin[a]}ln!rac{V_i}{
u_i+W_i(r)}.
]
因为 (V_i,
u_i>0)，所有对数都有语义定义。合同声称：给定正有理 (epsilon)，存在确定性算法，返回一个完整赋值 (r)，每个选中的标签满足原输入概率 (pi_{j,r_j}>0)，并有
[
Phi(r)\le mathbb E[Phi(r)]+epsilon .
]
算法复杂度按显式输入长度、(a,m,L,Q) 的**数值**及
(log(1+1/epsilon)) 计多项式。它不要求表示一般无理的 (mathbb EPhi) 或 (Phi)。在预期应用中 (Q=4m)（(m\ge1)），这时 Q 的数值收费转成显式输入的多项式；合同没有声称任意巨大二进制 Q 下的统一 bit-polynomial 复杂度。

空分支是合同的一部分：(m=0) 返回空标签；(a=0) 为每件物品选第一个正概率标签；两者都使势等于其期望。不能在这些分支里把 (epsilon/(2am)) 当作合法计算参数。

## 证明/审计内容的正确分层

statement-only 源本身不含证明。关联的 Exact-only 独立重构指出：

1. 将 (h_{i,j}=Qw_{i,j}) 取为整数后，每个 agent 的保留质量只有 (0,ldots,Q) 共 (Q+1) 个格点；
2. 固定一个正概率前缀后，剩余物品仍独立，生成多项式
   (prod_j((1-pi_{j,t_i})+pi_{j,t_i}z^{h_{i,j}}))
   可用精确有理 DP 求分布；
3. 用有理近似的 (-ln(
u_i+k/Q))，逐步只在正概率标签中选择条件期望估计最小者；误差尺度为
   (alpha=epsilon/(2am))，累计增量不超过 (epsilon)；
4. 用 (x=2^hy)、(z=(y-1)/(y+1)) 的对数幂级数以输入位长和
   (log(1+1/alpha)) 控制精度；
5. 这只认证有限表示的条件期望/DP 机制，且 Q 按数值计费。不同 agents 的 (W_i) 可以相关；需要的是物品标签独立，而不是 agent 独立；
6. 若额外假设同一目标标签类中的 (S_i) 两两不交，则
   (T_i={j\in S_i:r_j=t_i}) 跨所有 agents 两两不交。没有该假设，势不等式本身不推出物理资源不交。

`c7285...` 的独立重构和 `dfc2...` 的 read-after 都明确 PASS，但它们是数学读后审查，不是可执行实现或软件审计。因而安全分类是“statement-only 合同；由两份独立数学读后支持其推导可行性”，不是无条件的已交付程序。

## 与现有归档及后续工作的关系

该源与
`archives/unrelated-machines/state/资料/显式XOS与福利舍入三源边界--资料.md`
同属“显式有理 XOS / NSW 福利舍入”边界资料，但它比该资料中的内部 XOS backend 更窄：它只提供一个有限标签 mask 的对数势工具，不给分数 benchmark、XOS clause lift、welfare rounding、repair LP、makespan 或 NSW 常数。建议把它作为该资料的独立方法接口，更新
`retired-xos-nsw-boundary-20261031/source-manifest.json`，并与作者 Proof、独立 Exact-only、read-after 审查逐一列出。

历史来源解释账本已将它定位到 G148（显式 XOS fractional NSW / normalized robust gap boundary），但该映射是来源导航，不是定理继承。第三阶段可建立“有限 label-mask 对数势 → 显式 XOS 候选 backend”的方法/实现边，不能建立“该工具 → 六人 SPE 半覆盖”或“该工具 → 一般 unrelated-machines 常数”的无条件边。

## 不能升级的结论

- 不能把 (Q=4m) 的应用备注改写成任意 Q 的统一 bit-polynomial 算法；
- 不能把 (mathbb EPhi) 的加性势保证改写成 NSW、福利、makespan 或六人 Q-CAG-HALF 保证；
- 不能省略“每件物品只有一个全局标签”的物理身份，或把 agents 各自重抽标签；
- 不能删除同目标标签类的 (S_i) 两两不交前提后仍宣称 (T_i) 全局不交；
- 不能以 statement-only 文本替代作者 Proof、独立审查、实现或运行证据；
- 不能把相邻 DLRV/Feng–Li 文献范围审计当作该合同的外部已发表算法定理。

## 处置

该源的独有内容是一个边界清楚的有限格点 label-mask 对数势接口、Q 数值收费规则、空分支以及带固定标签类不交前提的物理后果。它不是纯重复：现有 XOS 资料没有逐字保留这一精确 (Phi) 合同及其 Q/空分支边界。建议处置为 `integrated`，目标为现有显式 XOS 福利舍入资料和退休 XOS evidence manifest；不新建六人 SPE 对象。原字节与 SHA 需在 checkpoint 中保留，之后才可提交本源的逐源 `done`。
