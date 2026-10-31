---
id: unrelated-machines/finite-grid-label-mask-log-potential-independent-review
kind: review
type_tag: 审查
title: 有限格点标签势去随机化的独立精确核验
status: independent-exact-reconstruction; finite-grid-and-scope-bounded
truth_status: PASS-for-stated-Exact-contract; no-downstream-NSW-certification
review_level: full-source-read-and-cross-archive-comparison
summary: "完整读取独立 Exact-only 审查及其声明的 statement-only 输入；重构条件期望、Q 格点 DP、对数近似与跨代理不交证明，确认其在明确量词下自洽，同时保留 Q 按数值收费、未读作者 Proof、未实现软件和不外推 NSW/UM 的边界。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_v1_independent_review.md
source_ids:
  - c7285e5c3cc4ad1716ec
source_sha256:
  - 25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633
source_sizes:
  - 11379
declared_input:
  source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md
  source_id: aee57c40a59da7343ff1
  source_sha256: b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165
related_objects:
  - ../资料/显式XOS与福利舍入三源边界--资料.md
  - ../tools/evidence/retired-xos-nsw-boundary-20261031/explicit_xos_deterministic_nsw_primary_scope_audit_rainbow_v1.md
  - ../tools/evidence/one-outer-v1-v2-sources-20261031/normalized_flat_proof_v2.md
evidence_paths:
  - ../../tools/evidence/finite-grid-label-mask-derandomization-20261031/
---

# 来源身份与读取范围

来源 `c7285e5c3cc4ad1716ec` 是 2026-10-18 的独立 Exact-only 重构，冻结于 legacy-cleanup 提交。原文长度 11,379 字节，SHA-256 为 `25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633`。本次通过 `clean show` 完整导出并逐节阅读；正文明确说明 reviewer 只读了 statement-only 源 `aee57c40a59da7343ff1`，没有读作者 Proof、其它新推导或 root 策略，也没有执行数值实验、实现或软件测试。这个“未读材料”是来源自身的证据边界，不能由本页抹掉。

本页同时将该独立记录与结果分支的三个相邻对象比较：显式 XOS/福利舍入资料、DLRV/Feng–Li 范围审查以及一个只覆盖特殊 normalized-flat UM 接口的确定性证明规格。比较只用于模型分流和量词核对，不把相邻对象的内部候选证明当成该源的独立验证。

# 精确合同

显式输入为有限 item 集 \\(U\\)，`a` 个 agents，labels \\(0,\\ldots,L\\)，每个 item 的非负有理 label 概率和为一且 items 独立。agent \\(i\\) 有 target \\(t_i\\in[L]\\)、集合 \\(S_i\\subseteq U\\)、正有理 \\(V_i,\\nu_i\\)，以及非负权 \\(w_{i,j}\\)，满足每个权是 \\(1/Q\\) 的整数倍且 \\(\\sum_jw_{i,j}\\le1\\)，其中 \\(Q\\) 是正整数。记 \\(h_{i,j}=Qw_{i,j}\\)，则所有质量索引在 \\(0,\\ldots,Q\\) 内。输入允许空 agent、空集合、零权、概率 0/1 和 label 0；`m=0` 与 `a=0` 都有显式早退，避免空分支除以 `m` 或 `a`。

目标势的 agent 项是
\\[
  \\ln V_i-\\ln(\\nu_i+W_i(r)),
  \\qquad
  W_i(r)=\\sum_j w_{i,j}{\\bf1}[r_j=t_i].
\\]
由于 \\(V_i\\) 与标签选择无关，记录先去掉常数 \\(\\sum_i\\ln V_i\\)，只需对
\\[
 f_i(k)=-\\ln(\\nu_i+k/Q),\\qquad
 \\Psi(r)=\\sum_i f_i(\\sum_jh_{i,j}{\\bf1}[r_j=t_i])
\\]
构造 \\(\\Psi(r)\\le E\\Psi+\\epsilon\\)，再加回常数。\`nu_i>0\` 保证每个对数有定义。

# 独立重构的承重论证

## 1. Q 格点条件期望 DP

按 item 顺序固定正概率 prefix。由于 items 独立，给定 prefix 后的未决 items 保持原概率；不需要除以 prefix 概率，也不需要 agents 间独立。对 agent \\(i\\)，剩余整数质量 \\(Z_i\\) 的生成多项式为
\\[
  \\prod_{j\\in J}((1-\\pi_{j,t_i})+\\pi_{j,t_i}z^{h_{i,j}}),
\\]
次数不超过 \\(Q\\)。长度 \\(Q+1\\) 的数组按 0/\\(h\\) 平移即可得到全部条件概率。以 \\(\\pi=P/D\\) 的共同分母整数递推
\\[
  N'_k=(D-P)N_k+PN_{k-h},\\qquad D'=DD_j
\\]
维护 bit length；每步系数和为分母，因此不会因极小正概率按 \\(1/\\pi\\) 次数展开。不同 agent 的 (Z_i) 可以相关，因为势只是 agent 项的线性和。

尝试下一 item 的每个正概率 label，更新对应 \\(b_i\\) 并用同一 DP 计算子前缀条件期望。零概率 label 不参与 argmin；这保证实际输出的每个 label 都有正输入概率，child 条件期望语义成立。

## 2. 近似 log 与全局误差

取 \\(\\alpha=\\epsilon/(2am)\\)。预计算 \\(\\widehat f_i(k)\\) 满足绝对误差至多 \\(\\alpha\\)，得到子前缀误差至多 \\(a\\alpha\\)。加权平均恒等式保证 parent 条件期望至少不小于某个正概率 child；选取近似最小 child 后
\\[
 F_{\\widehat t}\\le F+2a\\alpha.
\\]
经过 \\(m\\) 个 item 的 telescoping，输出满足 \\(\\Psi(r)\\le E\\Psi+\\epsilon\\)。

对正有理 \\(x\\) 的 log，记录使用 range reduction \\(x=2^hy\\)、\\(1\\le y<2\\)，令 \\(z=(y-1)/(y+1)<1/3\\)，以
\\[
 \\ln y=2\\sum_{n\\ge0}z^{2n+1}/(2n+1)
\\]
截断；\\(\\ln2\\) 同样处理。前 \\(N\\) 项的误差由 \\(9^{-N}\\) 控制，\\(N\\) 只随输入 bit length、`log(1+1/alpha)` 多项式增长，不按 \\(1/\\nu\\)、\\(1/\\epsilon\\) 的数值循环。近似值全是 rational，比较可精确完成，近似 ties 不需要判定 irrational log 相等。

## 3. 复杂度边界

总成本是输入长度、\\(a,m,L,Q\\) 与 \\(\\log(1+1/\\epsilon)\\) 的固定多项式，但 **Q 按数值收费**：数组大小为 \\(Q+1\\)，所以任意仅以 \\(\\log Q\\) 编码的巨大 Q 只得到 pseudo-polynomial grid DP。只有在应用合同 \\(Q=4m\\)（且 \\(m\\ge1\\)）时，Q 随显式 item 数线性，才能把该 DP 读成总输入位多项式。该边界是本记录最关键的范围限制，不能简化为“统一 bit-polynomial derandomization”。

## 4. 全局物理不交附加结论

源记录另外证明：若每个固定 target label \\(t\\) 下的 \\(S_i\\) 两两不交，则 \\(T_i=\\{j\\in S_i:r_j=t_i\\}\\) 跨所有 agents 两两不交。若某 item 同时属于 \\(T_i,T_h\\)，则 \\(r_j\\) 同时等于两个 target，迫使 target 相同；随后违反同 target 类的 \\(S_i\\cap S_h=\\varnothing\\)。不同 target 由 item 单标签排除冲突；相同 target 依赖额外 set-disjoint 前提。零权 item、空集合、label 0 和 \`m=0/a=0\` 都在论证范围内。没有复制 item 或为每个 agent 生成独立 assignment。若删掉该 set-disjoint 假设，纯势保证本身不推出 physical disjoint。

# 与相邻 XOS/UM 材料的比较

结果分支已有的 XOS/NSW 资料把 DLRV 的随机 geometric filtering、Feng–Li 的 additive log-potential/DP 和显式 XOS 的内部候选规格分开；它们明确不把 conditional-expectation 实现自动升级为 general weighted-XOS 或 demand-oracle 算法。本源的 finite-grid Exact 合同可以作为“显式有理输入上的一个 derandomization backend”接口，但：

- 它处理的是独立 item-label 概率和一个加性 log potential，不是 XOS clause 的一般 NSW 舍入；
- 它没有证明 DLRV 的 candidate/filter 语义能由该 DP 直接满足；
- 它没有给出 NSW、UM-TARGET、general subadditive 或六人 SPE 结论；
- 相邻 normalized-flat UM 证明只覆盖其专门的 supplied-CONFIG 表示，不能替本源的 Q-格点合同，也不能反向扩大本源量词。

因此，本页不创建与 XOS 定理合并的新对象；第三阶段若需要关系，可登记“方法接口/实现启发”边，而非“推出”或“证明”。

# 证据等级、独有内容与去向

本源独有的数学内容是：Q-格点生成多项式 DP、正概率 prefix 语义、`nu`/概率极小值不导致数值倒数循环、range-reduced log 的 bit-length 证明、以及固定 target 类 set-disjoint 才能推出全局物理不交。上述内容应进入正式审查对象；原文全文副本、statement-only 原件及 SHA/manifest 应放入 `archives/unrelated-machines/tools/evidence/finite-grid-label-mask-derandomization-20261031/`。

证据强度分层如下：

1. **Exact 合同内的完整推导（来源自称 PASS）**：条件期望误差 telescoping、Q 格点 DP、正有理 log 截断和附加不交推论。
2. **有限/伪多项式边界**：复杂度只对 Q 数值多项式；应用 \\(Q=4m\\) 才有 bit-polynomial 读法。
3. **未认证内容**：作者 Proof、root 策略、软件实现、运行回归、NSW/UM 下游、文献新颖性和任意巨大 binary Q。
4. **与现行六人 SPE 主线的关系**：仅是算法/证据接口；不涉及有序历史纯 SPE、终局客户均分或半最大主题覆盖。

处置建议为 `integrated` 到本对象、原件与 manifest 入 evidence；不把相邻源重复登记为本源的新颖性或独立实验。来源 `c728...` 的 `done` 回执应列出已完整读取、跨档比较、独有内容的目标路径和上述边界。
