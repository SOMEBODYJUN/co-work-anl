---
id: "unrelated-machines/multiwitness-shared-job-fee-v2-suffix-review-20261031"
kind: "review"
type_tag: "审查"
title: "多见证共享收费 v2 精确稿与 canonical 后缀三源接续审查"
status: "complete-source-read-version-chain-integrated"
truth_status: "v2-empty-set-fix-and-canonical-suffix-scope-confirmed"
review_level: "clean-show-full-read-cross-version-and-canonical-hash-audit"
scope: "multiwitness_shared_job_fee_exact_v2.md、final_section_review.md、proof_read_after_review.md 三份后缀来源"
summary: "v2 Exact 仅修复 v1 第7项 K=∅ 严格式缺口；canonical 后缀审查确认第6节同一多见证参数族的 OPT/费用/容量边界与 v2 Proof 无冲突；proof read-after 记录 v2 Exact/Proof 全文核验。三源强化版本 provenance，不创建第二个多见证定理。"
source_refs:
  - "source:0d3452ca55f205aa6a7e:history/source/notes/unrelated_machines/multiwitness_shared_job_fee_exact_v2.md"
  - "source:17808d1982b908b5713a:history/source/notes/unrelated_machines/multiwitness_shared_job_fee_final_section_review.md"
  - "source:a7b3b41f0c16e5f04794:history/source/notes/unrelated_machines/multiwitness_shared_job_fee_proof_read_after_review.md"
related_objects:
  - "../审查/多见证共享作业费用三源精读与空集边界版本审查--审查.md"
  - "../审查/多见证共享作业费用与共同容量精确合同--审查.md"
  - "../审查/双见证查询分离的染色证明与冻结审查边界--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/multiwitness-shared-fee-suffix-20261031/"
---

# 1. 来源身份与版本链

三源均由 `clean claim` 后完整 `clean show` 读取，双冻结提交内容一致。原始指纹：

| ID | 路径 | 字节 | SHA-256 |
|---|---|---:|---|
| `0d3452ca55f205aa6a7e` | `multiwitness_shared_job_fee_exact_v2.md` | 5,139 | `b3b3f2d98a6b81d5ee525bcdfa0fb26d1021994db58419f11f4862b321e6a607` |
| `17808d1982b908b5713a` | `multiwitness_shared_job_fee_final_section_review.md` | 2,794 | `a657ddaa05ff7dbd5cb0b9778256cd6ef4e68dd2b798dff0662894f2028fd950` |
| `a7b3b41f0c16e5f04794` | `multiwitness_shared_job_fee_proof_read_after_review.md` | 2,120 | `a106c640f48154a7dfaebf418fc43ba9c44380e432e47da49002b7f0962157d7` |

本批证据目录保留三份后缀源。canonical `two_witness_query_separation.md` 的最终 SHA 为 `bf942037e600967fa86b76c2b1f0db41673a2bae71411e1afb6527d6f332c709`；后缀 review 对该 canonical 第1–6节做全文审读，但不是新的 canonical 文件副本。

# 2. v2 Exact 的唯一修改：K=∅ 量词修复

v2 Exact 完整列出同一 P：(p\ge1)、正有理 (a_r,b_r,c\le1)、(c+\sum b_r\ge1)、互异 (H_r,A_r,R,S) 机器和 (q_r,x_r,f) 任务。它保留：

\[
\operatorname{OPT}(P)=1,
\quad
\operatorname{OPT}_K=\min\{2,\max(1,B_K)\},
\quad B_K=\sum_{r\in K}b_r,
\]

以及 (1\le\beta<2) 闭阈值费用

\[
F_\beta(K)=
\begin{cases}
\infty,&B_K>\beta,\\
0,&c+B_K\le\beta,\\
1,&B_K\le\beta<c+B_K.
\end{cases}
\]

v1 第7项若允许 (K=\varnothing)，会把真空前件与 (0<B_\varnothing=0) 矛盾地拼起来。v2 明确改为“若 (K) 非空 strict1 可行，而每个 singleton 在同一 (eta) 上都收费”，则

\[
|K|(\beta-c)<B_K\le1.
\]

因此 (eta\ge3/2,c\le1) 时 (K) 至多一个元素。空 K 单独保持 strict1、fee0，不进入严格求和。Proof read-after 和 canonical final-section review 均确认这一修复，没有倒改 v1 冻结文件。

# 3. Canonical 第6节与 v2 Proof 的一致范围

`final_section_review.md` 对 canonical `two_witness_query_separation.md` 新第6节逐项核验：

- 原矩阵仍为 (2p+2) 台互异机器、(2p+1) 枚任务和 (4p+2) 条 finite 资格；
- (sigma_0) 与每个 (sigma_r) 都是完整实际峰1见证；
- (operatorname{OPT}=1) 下界使用 (c+\sum b_r\ge1)，不是“存在 unit 任务”捷径；
- (operatorname{OPT}_K) 两份实际上界与 (C<2) 强迫 (x_K\to R) 的下界覆盖空 K、B=1、B=2 和 B>2；
- (B_K=\beta) 仍可行，(c+B_K=\beta) 归 fee0，(eta=2) 所有 pattern fee0；
- 容量 (s)、异权非空 K 严格和式、(p=1)、(c=1) owner fee 边界均保持。

`proof_read_after_review.md` 记录先读 v1 Exact/独立 Fraction 枚举，再读 v2 Exact 与 Proof 全文；确认 v2 Proof 的第1–6节与 Exact-first 重构一致，未把 owner fee 统一冒称新增 unit 费用，也未将 OPT1 族冒称 OPT gap 或 source reduction。

# 4. 与前一批多见证三源的关系

前一批 `多见证共享费用三源精读与空集边界版本审查--审查.md` 已整合 author Proof v2、code review 和 Exact-first review；本批后缀新增：

| 源 | 独有内容 | 处置 |
|---|---|---|
| `0d3452ca55f205aa6a7e` | v2 Exact 正式对象/7项结论及 K 非空修复 | integrated-exact-v2 |
| `17808d1982b908b5713a` | canonical 第6节最终全文审读、SHA、边界和无新增 fatal 判定 | integrated-canonical-final-section-review |
| `a7b3b41f0c16e5f04794` | v2 Exact/Proof read-after 的实际顺序、空集修复和量词确认 | integrated-proof-read-after |

这些来源都是同一多见证参数族的版本链，不建立第二个 theorem。它们共同保留“多个互斥 singleton strict 见证不等于共同全开 strict 见证”的核心边界。

# 5. 不应推出的结论

该族仍是 OPT=1 的显式可解参数族，没有 OPT gap、源 decoder、标签复制、跨测试预算或一般 UM 近似。它不反驳旧双见证查询分离，因为旧定理需要同一完整 (sigma_1)，而本族只有 (sigma_0) 与每个 singleton 自己的 (sigma_r)。它也不提供 CAG 六人完整历史 SPE 覆盖结论。

本批三源均已完整阅读、比较和保全；未执行 clean done、commit 或 push，父 Boss 在 checkpoint/pushed 后逐源 done。
