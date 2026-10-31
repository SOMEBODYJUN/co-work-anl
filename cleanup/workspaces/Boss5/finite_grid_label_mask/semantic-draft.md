---
id: "unrelated-machines/finite-grid-label-mask-log-potential-derandomization-author-proof-v1"
kind: "proof-review-draft"
type_tag: "证明审查草稿"
title: "有限格点标签掩码对数势去随机：作者 Proof 的范围与证据"
status: "author-proof-read-after; not-implemented"
truth_status: "finite-representation-proof-contract-passed-by-related-independent-review"
source_refs:
  - "source:c05060b2330f0a8d6978:history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_author_proof_v1.md"
  - "source-sha256:b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165"
related_sources:
  - "finite_grid_label_mask_log_potential_derandomization_statement_only_v1 (SHA256 b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165)"
  - "finite_grid_label_mask_log_potential_derandomization_v1_independent_review (SHA256 25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633)"
  - "author-proof read-after (SHA256 8a20ac9d1d0a9381621ff7560e1c3f985db072dba4aafae8125c4c846d54fbad)"
---

## 清洗结论

该冻结来源是 root/boss11 在实际读过独立 Exact-only 记录后写出的作者 Proof v1。它给出一个有限格点、显式有理输入的确定性 \(\epsilon\)-加性条件期望构造；相关 read-after 审查报告 PASS，未发现数学、误差、位复杂度或物理不交性证明的 fatal。这里的 PASS 只覆盖该工具的明确表示范围和额外不交前提，不覆盖下游 NSW 常数、源归约、一般 unrelated-machines 算法或当前六人 SPE。

该来源不应标成“软件已实现”或“外部发表定理”：文档没有实现、运行日志、数值实验或外部新颖性认证。正确分类是“作者完整证明稿；与先行独立 Exact-only 重构一致；实现仍缺失”。

## 对象与精确量词

- 有限显式 item 集 \(U\)（\(m\) 个）、agent 集 \([a]\) 和 labels \(\{0,1,\ldots,L\}\)，每个 item 有非负有理概率表 \(\pi_{j,t}\)，和为 1；item labels 相互独立。
- 每个 agent 有目标 label \(t_i\in[L]\)、显式子集 \(S_i\subseteq U\)、正有理 \(V_i,\nu_i\)，以及在 \(S_i\) 上的非负权 \(w_{i,j}\)。给定正整数 \(Q\)，每个权是 \(1/Q\) 的整数倍且行和不超过 1；空集、零权合法。
- 完整 assignment \(r\) 的 \(W_i=\sum_{j\in S_i}w_{i,j}{\bf1}[r_j=t_i]\)，目标势
  \[
  \Phi(r)=\sum_i\ln\frac{V_i}{\nu_i+W_i(r)}.
  \]
  结论是确定性输出一个每项都取正输入概率 label 的 assignment，使 \(\Phi(r)\le E\Phi(r)+\epsilon\)。
- 运行界按显式输入位长、\(a,m,L,Q\) 的**数值**以及 \(\log(1+1/\epsilon)\) 多项式计费。任意仅以二进制位长给出的巨大 \(Q\) 只有伪多项式保证；目标应用的 \(Q=4m\)（\(m\ge1\)）才落入真正位多项式范围。
- \(m=0\)、\(a=0\)、零权、空 \(S_i\)、概率 0/1 与 label 0 均在声明分支中处理，不从 \(1/\nu\)、\(1/\pi\) 或 \(1/\epsilon\) 的数值制造循环。

## 作者证明的关键链条

1. 写 \(h_{i,j}=Qw_{i,j}\) 并去掉 label-independent 的 \(\sum_i\ln V_i\)。剩余函数是 \(f_i(k)=-\ln(\nu_i+k/Q)\)，其中 \(k=0,\ldots,Q\)。
2. 对每个正概率 prefix，未决 item 仍独立且保留原概率。每个 agent 的剩余整数质量由
   \[
   \prod_{j\ {保留}}((1-\pi_{j,t_i})+\pi_{j,t_i}z^{h_{i,j}})
   \]
   给出，次数不超过 \(Q\)。用长度 \(Q+1\) 的有理 DP 精确求分布。若 \(\pi=P/D\)，整数系数递推
   \(N'_k=(D-P)N_k+PN_{k-h}\)，公共分母为各实际分母乘积，位长按输入分母位长控制。
3. 对每个候选正概率 label，加入该 item 对各 agent 的真实 base，再对剩余 item 做 DP；对表值 \(-\ln(\nu_i+k/Q)\) 预计算绝对误差 \(\alpha=\epsilon/(2am)\) 的有理近似。每个候选 child 的估计误差至多 \(a\alpha\)。
4. 选择估计势最小的候选。全期望保证存在真实 child 不超过 parent；近似比较带来至多 \(2a\alpha\) 的增加。逐 item 递推 \(m\) 次后得到 \(\Psi(r)\le E\Psi+\epsilon\)，再加回常数得到原势结论。整个 argmin 只在输入概率严格为正的 labels 上进行，无需概率下界或除以 prefix 概率。
5. 对任意正有理 \(x\) 用 \(x=2^hy,1\le y<2\)，\(z=(y-1)/(y+1)<1/3\) 的幂级数近似 \(\ln x\)；截断尾界 \(9^{-N}\)，\(N\) 只随输入位长和 \(\log(1+1/\alpha)\) 增长。没有按数值大小展开。
6. 若额外假设固定 target label 类内的 \(S_i\) 两两不交，则实际集合 \(T_i=\{j\in S_i:r_j=t_i\}\) 在**全部 agents** 间两两不交：不同 target 由单个 item 的唯一 label 排除，同 target 由该额外集合假设排除。没有这个额外假设，势条件期望本身不推出物理 allocation 不交。

## 相关来源、差异与证据边界

- 先行 statement-only Exact 与该 Proof 共享同一数学合同。独立 Exact-only 重构逐项核对空分支、概率 DP、误差递推、对数近似、\(Q\) 收费与全局不交条件；作者 Proof 的 read-after 审查结论为 PASS。作者 Proof 不是另一份 blind-independent proof，不能把作者与同一 root 的后写审查重复计数为两份独立证明。
- 现有 `archives/unrelated-machines/state/资料/显式XOS与福利舍入三源边界--资料.md` 已把该技术路线放在 DLRV 随机 NSW 框架和 additive NSW 对数势/DP 先例旁：本工具可作为**表示特定的 deterministic derandomization 接口**，不能自动推出一般显式 weighted-XOS、demand-oracle、subadditive、source-hardness 或 NSW 常数。
- `归一化门菜单福利与对数调色板 padding 有限审查` 的 exact JSON 审计与本工具不同：它是有限样例/有限 LP 与 padding 统计，不是本 DP 证明的实现，也不能把本证明的 \(Q\)-grid 条件倒写成普遍菜单舍入算法。
- 本来源没有代码、软件运行、有限数值回归或完整下游归约；任何后续 ordinary schedule、welfare ratio 或 SPE 主线对象必须另给输入保持、任务不交和逐偏离证据。

## 建议归档去向

建议将正式正文（由 Boss 审阅后入库）放入
`archives/unrelated-machines/state/证明/有限格点标签掩码对数势去随机--证明.md`，并把该冻结原件、相关 Exact-only 与 read-after 文档的 SHA/来源映射保存至
`archives/unrelated-machines/tools/evidence/finite-grid-label-mask/`。第三阶段只建立以下解释边：

- statement-only Exact → 作者 Proof：同一有限表示合同的证明展开；
- 独立 Exact-only → read-after：范围核验与误差/位复杂度交叉检查；
- 该工具 → 显式 XOS/NSW 资料：方法接口（需保留“未实现、非一般定理”标签）。

不要把它连成当前六人共同目录纯 SPE 半覆盖结论，也不要把有限 DP 的 PASS 写成已经有可执行程序。
