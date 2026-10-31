---
id: "unrelated-machines/shared-ud-tiny-state-potential-and-19-over-10-completion"
kind: "candidate-proof"
type_tag: "证明"
title: "共享 UD tiny 状态势与 19 比 10 回填"
status: "scoped-candidate; independent-review-and-end-to-end-implementation-pending"
truth_status: "author-proof-chain-with-versioned-conditional-domains"
review_level: "author-proof-self-audit-and-informed-version-read; no-fresh-blind-audit"
summary: "在单态 outer、互异 home、shared-B fallback 与 B-only exact-threshold-UD 叶的显式结构域中，作者候选用 profile 势、稳定 matroid 交换、Frank–Wolfe 和 prefix-flow 回填声称 19/10；各 k⁴、k² 与 v5 版本保持独立量词，尚未升级为一般 unrelated-machines 定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_author_self_audit_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_canonical_append_v4b.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_O1k_v5_final_actual_read_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_k2_refinement_informed_audit_v1.md"
evidence_manifest: "../../tools/evidence/shared-ud-tiny-potential-20261031/manifest.json"
legacy_ids:
  - "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1"
  - "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4b"
  - "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v5"
---

# 1. 共同 typed 域与版本身份

共同输入是有限 unrelated-machines 矩阵的显式 typed 子类：每个 outer 只有一个 indexed state；每个 home 是物理互异的 unit helper；fallback 状态只使用公共资源集 (B)；额外叶的正支持也只在 (B)，并满足 (arepsilon=15/16) 的 exact-threshold unit-demand 条件。所有 selectors、未选 state payload、zero/incidence、duplicate 和 unused 项都保留在完整 (P(Q))，没有 actual target、OPT 或 profile oracle。

版本量词不能合并：Exact/author Proof v1 的 home 最大正权重为 (
ule1/(4096k^4))；k² 扩域稿在 (kge2) 使用 (
ule1/(16384k^2))，并对 (k=1) 单独处理；v4 解除 (k=1) 的 tiny 上界；v5 后置读后版本使用不同的 (kge2) 上界 (
ule1/(1024k))，并为 (k=1) 保留 actual-I 分支。这些是不同候选对象的输入域，不能将某一版本的曲率或方差常数静默迁移到另一版本。

# 2. 规范化值桥

给 fallback bundle 定义每组的 normalized value (V)。在完整保留原 jobs 的 typed 矩阵中，作者链给出
[
\operatorname{OPT}(P(Q))=2-V,qquad 0le Vle1.
]
正向把每组达到 (V) 的 state 的正 incidence 外送到不交的 (B) 资源，其余 payload 留在 private machine；反向当 (C<2) 时，resource unit job 的独占性把 selector 所在 state 读成不交 bundle，值至少 (2-C)。这一步是完整 jobs 的值桥，不是把分数 profile 当作实际调度。

# 3. v1 作者候选的 profile 势机制

v1 取固定 (arepsilon=15/16)、(c=5/16)、(	heta=1/32)，在每个 helper 的 fallback state/empty profile 上定义可行 (B)-资源流和 outer payoff (W_i)。对 profile (S) 定义
[
\Phi(W)=\frac{\theta}{k}\sum_iW_i-sum_i(c-W_i)_+^2,qquad
P(S)=\max_W\Phi(W).
]
梯度权重 (lambda_i=	heta/k+2(c-W_i)_+) 严格为正。weighted matroid/matching oracle 给出每个固定 profile 的线性最优点；稳定的 helper-state 交换估计以被替换 helper 的 (w_j) 控制 weighted (L^\infty) 与 (L^1) 变化，二次 smoothness 给出
[
P(S')-P(S)geDelta_j-2(\lambda_i(j)/\lambda_{\min})^2w_j^2.
]

若真实 (Vgearepsilon)，某 target profile 对所有正权 (lambda) 提供 (arepsilon^2sum_ilambda_i) 的 benchmark。次模 option-sum 加上曲率界，说明只要 deficit (D=sum_i(c-W_i)_+) 尚未低于 (9/80)，至少一个单 helper state 替换带来固定 (ho>0) 的 profile 进展。用固定步长 (	au=1/(2048H)) 的近似 profile 搜索，势值域有限，故 move 次数为多项式；无进展时可 sound 地判定 (V<15/16)，而全 private baseline 的比率严格小于 (19/10)。

profile 评价以有理 Frank–Wolfe 近似 (P(S))，只调用显式 matching/matroid greedy 和有理算术；候选数是显式 state 数，不枚举指数 joint profile。此处的算法合同仍是作者候选，尚无 end-to-end 软件认证。

# 4. Prefix-flow 与完整回填

成功 profile 达到 (W_ige25/128) 后，把同 outer 的资源 claims 聚合为按资源权重排序的 nested prefixes，再将 outer lower bounds、叶 matching 和资源容量合在整数 circulation。原有 fraction flow 给出可行性，integrality 恢复不交的 B 资源 claims；每组损失至多 (
u)。取 (q=1/10)，由 (W_ile z_i+q(1-z_i)) 得每个 outer 的 good home mass (z_i>q)。Good helpers 送出 fallback bundle，其余 helpers 回 own-home，额外 UD 叶保留匹配；全部原 jobs 逐 selector 回填，得到 (C_{\max}le2-q=19/10)，并保持未选 state、zero 和 duplicate payload。

# 5. k 依赖修订与证据等级

k² informed audit 重新推导
[
\sum_jB_jle2\nu k+\left(\frac{8\nu k}{\theta}+\frac{8c\nu k^2}{\theta^2}\right)D,
]
并在 (kge2) 的 (
ule1/(16384k^2)) 下得到 (1/16384+(21/128)D)，(k=1) 另用实际 (lambda_{min})；它只做有限 Fraction 参数核查，不是 fresh independent 或完整运行。v5 后置读后同样区分 actual-I、相对 reciprocal 势和旧版本，不把后置作者票当 blind 审查。

本批六源没有提供 end-to-end scheduler、完整 profile/FW/prefix-flow 运行、外部 referee 或一般 UM hardness。它们支持的是版本化、条件性的作者证明链和精确范围记录；multi-state outer、home overlap、非 UD extra groups、一般 unrelated-machines、六人 SPE 与 Q-CAG-HALF 均未由此解决。
