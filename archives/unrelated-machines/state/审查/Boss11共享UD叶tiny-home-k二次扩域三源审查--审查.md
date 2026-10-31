---
id: unrelated-machines/boss11-shared-ud-tiny-home-k2-refinement-review
kind: review
type_tag: 审查
title: Boss11共享UD叶 tiny-home k²扩域三源审查
status: exact-scope-v3-v4-and-proof-revision-read; restricted-candidate-only
truth_status: proof-scope-reconstructed; no-general-UM-theorem
review_level: full-source-read-version-comparison
summary: "完整读取 k² tiny-home Exact v3、解除 k1 上界的 Exact v4 与 proof_v3；确认 19/10 只对显式 shared-UD-leaf 结构的完整量词，保留 k1/k≥2 曲率分支和无全叶匹配处理，不扩为一般 unrelated-machines。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/boss11_shared_ud_tiny_home_k2_refinement_exact_v3.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/boss11_shared_ud_tiny_home_k2_refinement_exact_v4.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/boss11_shared_ud_tiny_home_k2_refinement_proof_v3.md
source_ids: [95c635ea4087e884e26e, 3001ace70a0b1621eb88, 008523f50a31a6025502]
source_sha256:
  - cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39
  - 8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d
  - ba7556c84d8ce5759c66fd840448085e94c435a94723573d76d73f9f5530b877
source_sizes: [2124, 2486, 3235]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/boss11-shared-ud-tiny-home-k2-20261031/manifest.json
---

# 1. Exact v3 量词与对象

`boss11_shared_ud_tiny_home_k2_refinement_exact_v3.md`（ID `95c635ea4087e884e26e`，2,124B，SHA `cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39`）定义一个显式 typed normalized-flat 输入域。输入保留旧 Exact 的全部 ordinary \(P(Q)\)，但 home 最大正权重条件改为：

- \(k=1\)：每个 home 的最大正权重 \(\le 1/4096\)；
- \(k\ge2\)：最大正权重 \(\le 1/(16384k^2)\)。

每个 outer 的正 home 权重和为 1，homes 物理互异、每 home 一个 own-unit helper；shared B fallback 状态彼此 disjoint。允许任意多个 B-only exact-threshold-UD extra leaves，但要满足固定 \(\epsilon=15/16\) 的 \(H_l\) 条件：叶可达最高 \(p_{lsu}\) 至少 \(\epsilon\) 的 outer 集合之外的总值小于 \(\epsilon\)。所有菜单必须非空且显式，zero/incidence/duplicate/unused 均保留，不能偷删。

目标是固定确定性、总位多项式算法：对每个合法 \(Q\) 输出全部原 jobs 的合法调度，满足

\[
C_{\max}\le \frac{19}{10}\,\mathrm{OPT}(P(Q)).
\]

无 OPT 输入、joint law、可行 LP/PSD 点、profile 或精度 oracle；不允许随机运行时间或指数 profile 枚举。此 Claim 只覆盖 typed normalized-flat、shared UD leaves、tiny-home 与 B-only leaf 结构；multi-state outer、重 homes、non-UD leaves、home 额外叶和一般 UM 均不在域内。

## 2. Exact v4 的版本差异

`boss11_shared_ud_tiny_home_k2_refinement_exact_v4.md`（ID `3001ace70a0b1621eb88e`，2,486B，SHA `8948b47cc8b2f303f7f1446ecb0137da163d0b65e906ec4169c5f85294ef877d`）保留 v3 的所有对象和目标，但解除 \(k=1\) 的最大权重上界；\(k\ge2\) 仍为 \(1/(16384k^2)\)。它明确 v4 不回写 v3 草稿、没有一般 UM 结论，也不包含完整证明机制。

因此 v3 域严格包含于 v4：k=1 放宽，k=2 相同，k>2 的 k²约束仍比旧 k⁴ 域宽。版本差异只改变输入量词，不自动证明放宽后的 k=1 分支仍满足旧常数；这一义务由 proof_v3 的分支说明承担，必须单独核对。

## 3. proof_v3 的承重推导

`boss11_shared_ud_tiny_home_k2_refinement_proof_v3.md`（ID `008523f50a31a6025502`，3,235B，SHA `ba7556c84d8ce5759c66fd840448085e94c435a94723573d76d73f9f5530b877`）在 fresh Exact-only 期间冻结。它沿用旧作者 primal smooth-deficit/profile-exchange/FW 算法，常数为 \(c=5/16\)、\(\theta=1/32\)、\(\xi=1/(2^{20}H^2)\)、\(\tau=1/(2048H)\)、停止阈值 25/128，质量参数 q=1/10。

令 \(D=\sum_i d_i\)，\(d_i=(c-W_i^*)_+\)，\(\lambda_i=\theta/k+2d_i\)。稳定交换给出

\[
\sum_j B_j\le \frac{2\nu}{\lambda_{\min}^2}\sum_i\lambda_i^2,
\qquad
\lambda_{\min}\ge \theta/k,
\qquad
\sum_i\lambda_i^2\le \theta^2/k+4\theta D/k+4cD.
\]

从而

\[
\sum_jB_j\le 2\nu k+\left(\frac{8\nu k}{\theta}+\frac{8c\nu k^2}{\theta^2}\right)D. \tag{1}
\]

### k≥2 分支

代入 \(\nu\le1/(16384k^2)\)、\(\theta=1/32\)、\(c=5/16\)，得到

\[
\sum_jB_j\le 1/16384+(21/128)D. \tag{2}
\]

旧次模比较给出 \(\sum_j\Delta_j\ge(65/128)D-287/8192\)。当 \(D\ge9/80\) 时，

\[
\sum_j[P(A_j)-P(A)]\ge(11/32)D-575/16384
\ge293/81920>0. \tag{3}
\]

这条严格正增量是 proof_v3 对 k² 域的关键承重式；它不依赖旧稿粗化的 k⁻³ 估计。

### k=1 分支

proof_v3 不把 (2) 机械套到 k=1，而是用 \(\lambda_{\min}=\lambda_1\) 和 \(\sum_jw_j^2\le\nu\) 得 \(\sum B_j\le2\nu\le1/2048\)。对应剩余常数为 177/8192，仍足以完成正增量比较。这个独立分支是 v4 解除 k=1 tiny 上界时必须重新检查的接口；Exact v4 本身只是量词，不是证明。

## 4. 算法输出与边界

proof_v3 说明精确 P deficit 稳定性、近似 FW 误差、观察到的 \(\tau\) 进展及 soundFAIL 继续沿用旧证明；每个 profile 的匹配调用数为 \(N=\lceil4k/\xi\rceil\)，普通有理 LP/matching/min-cost flow 可用。所有原 selectors/incidences、inactive/zero/duplicate indexed payload 和无全叶匹配输入都需保留；不能以排除坏输入换取比率。

最后 prefix/叶 circulation 损失仍由 \(\nu\le1/4096\) 控制，给出 \(W\ge25/128-\nu\ge799/4096>19/100\)；基线失败分支保留 `actualOPT>17/16`，ratio<32/17。这里的输出保证只属于该显式结构类，不是一般 unrelated-machines 的 19/10 算法。

## 5. 结论分层与后续

**候选精确陈述：** v3/v4 的输入量词、全 job 输出、19/10 目标和结构排除条件；v4 的唯一新增量词是 k=1 无 tiny 上界。

**内部证明修订：** proof_v3 给 k≥2 曲率统一式、k=1 独立常数和 bit/匹配接口；它明确是根推导，未提供端到端软件、外审或新颖性证明。

**未建立：** 没有一般 UM 算法、没有未知 k² 域的完整独立实现、没有把 v4 放宽自动当作已验证定理。第三阶段应把 v3 exact、v4 exact、proof_v3 分开标注，并继续核对旧作者 proof、无全叶匹配、prefix 损失和位复杂度依赖。
