---
source_id: "09654b68c8ce88dfbc5a"
source_path: "history/source/notes/unrelated_machines/sol_general_repair_shared_ud_k2_refinement_informed_audit_v1.md"
source_sha256: "ea0ea155880899462b298ff6e9c092ec8201237203bd1dd6684783a03f7084ac"
source_size: 3806
kind: "informed-author-audit"
status: "integrated-candidate; not-fresh-independent"
disposition: "integrated"
target_suggestion:
  - "archives/unrelated-machines/state/审查/Boss11共享UD叶tiny-home-k二次扩域三源审查--审查.md"
  - "archives/unrelated-machines/tools/evidence/retired-boss11-tiny-home-k2-20261031/manifest.json"
---

# 来源身份与证据等级

`clean show 09654b68c8ce88dfbc5a` 已完整读取 3,806 字节冻结源。它是 `/root/sol_general_repair` 在已读取 `boss11_shared_ud_tiny_home_k2_refinement_exact_v3.md`、旧 Exact、作者 Proof §1–9 及 append-v1 后写的 **知情作者核查**；源文件明确说它不是新的 Exact-first 独立票，也没有打开 truehardness 的新重构。因此本稿不能把它计为 fresh independent proof 或外部审查，只能作为对现有 v3/v4/proof 版本审查的补充审计。

来源声明旧 v3 Exact 为 2,124 bytes，SHA `cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39`；这些字节及 v3/v4/proof 三源已有证据 manifest。当前源自身的 SHA 为 `ea0ea155880899462b298ff6e9c092ec8201237203bd1dd6684783a03f7084ac`，原件应在本批 evidence 中另存并与既有三源分开。

# 扩域合同与重算结论

源所核的域是 typed normalized-flat、single-state outer、每 outer 正 home 权重和为一、homes 物理互异、每 home 一个 own-unit helper、shared B fallback 与 B-only exact-threshold-UD leaves；完整 ordinary jobs、zero/incidence/duplicate/unused payload 均保留。tiny-home 上界为：(k=1) 时 (
ule1/4096)，(kge2) 时 (
ule1/(16384k^2))。源没有把 multi-state outer、重 home、non-UD leaf、home 额外叶或一般 unrelated-machines 纳入域。

审计重新固定 profile 的精确 Φ-optimal 点，令 (	heta=1/32)、(c=5/16)、
(lambda_i=	heta/k+2d_i)、(D=sum_i d_i)。stable weighted-matroid coupling 给出

[
B_j=2(\lambda_{i(j)}/\lambda_{\min})^2w_j^2,
\qquad
\sum_jB_jle2\nu k+\left(\frac{8\nu k}{\theta}+\frac{8c\nu k^2}{\theta^2}\right)D.
]

这是对旧 (k^{-4}) 粗化估计的直接重推，ν 只在曲率项中承重。对 (kge2) 代入新域得到

[
2\nu k\le1/8192k\le1/16384,
\qquad
\frac{8\nu k}{\theta}+\frac{8c\nu k^2}{\theta^2}le21/128,
]

故 (sum B_jle1/16384+(21/128)D)。与既有次模交换下界 (sumDelta_jge(65/128)D-287/8192) 合并，当 (Dge9/80) 时，增量至少为 (293/81920>0)。

(k=1) 不可机械套用 (lambda_{\min}ge	heta/k) 的粗界；源保留实际 (lambda_1)，用 (sum_jw_j^2le
u) 得 (sum B_jle2
ule1/2048)，相应余量 (177/8192) 仍足以推进原比较。这一分支正是 v4 解除 (k=1) 上界时需单独检查的承重步骤。

# 其余依赖和有限检查

源逐项重查 ν 的其他用途：target-profile benchmark 只用 actual (V\ge\varepsilon)、home 独占与 normalized sums；weighted-rank 次模性、fractional optimum 的稳定性和 Φ deficit stability 不用 tiny bound；prefix-flow 损失只需 ν\le1/4096；FW 的 profile 次数 (N=\lceil4k/\xi\rceil)、ξ 与 τ 只用 (H\ge1) 和有理公共分母；actual FAIL、baseline (32/17) 和 zero/inactive jobs 也不依赖新的 ν 代数。

本源报告用 `Fraction` 对 (k=2,3,4,8,64) 的新常数、Dsum 系数、prefix margin 做有限计算，确认常数 ≤1/16384、系数 ≤21/128、margin ≥799/4096，并直接复算 (293/81920)。这只是局部代数/参数回归，没有运行新域完整算法、profile 搜索、FW、prefix-flow 或全部原 jobs；不能把它当端到端软件认证。

# 与既有对象的关系和边界

现有《Boss11共享UD叶tiny-home-k二次扩域三源审查》已整理 v3 Exact、v4 Exact 和 proof_v3，并给出同一 k² 曲率式、k=1 分支、19/10 目标和一般 UM/open 边界。本源的独有内容是知情作者对所有 ν 使用点的逐项回核、k=2/3/4/8/64 的 Fraction 参数检查，以及明确声明“未读 truehardness 新重构、不是 fresh independent”。它应 integrated 到该审查页与同一 evidence manifest，保留独立 source ID，不能覆盖或重写已有三源身份。

源不证明一般 `UM-TARGET-v1`、source hardness、P≠NP、外部新颖性、六人 SPE 或 Q-CAG-HALF；也不把 root 的新 Exact-first 审查或 NSW k⁴ 报告冒称为本轮实际读取。旧 k⁴ 域包含于新 k² 域（(k=1) 相同、(k=2) 等号、(k>2) 严格扩宽），因此扩域必须按版本单独保存。

# 处置建议

`integrated`。将本稿和原件导出纳入 Boss11 k² evidence manifest，更新现有审查的 source_refs/版本段；receipt 应说明完整读取、知情作者角色、局部 Fraction 检查和未运行端到端算法。不要把本源记作第二份独立证明，也不要把有限常数检查升级成一般 19/10 定理。
