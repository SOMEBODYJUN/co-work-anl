---
id: "evidence/unrelated-machines/tiny-work-vector-label-review"
kind: "evidence"
type_tag: "审查证据"
title: "小任务、压缩向量与两层标签三源审查证据索引"
status: "source-read-and-reconstructed"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/tiny_work_stability_and_selection_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/tiny_work_stability_and_selection_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/truncated_vector_greedy_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/truncated_vector_greedy_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/two_level_label_fee_escape_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/two_level_label_fee_escape_review.md"
---

# 冻结源指纹

| 来源 ID | 路径 | SHA-256 | 大小 | 处置 |
|---|---|---|---:|---|
| `8934c135f1ec0a4c68d9` | `research/reviews/unrelated_machines/tiny_work_stability_and_selection_review.md` | `3097ebf2d896e815ae1038bb5f205bbb9f8f31d309d2b9f0aaa7916451fb7c9d` | 54274 | 已整合到联合槽稳定性对象 |
| `cff5b6b52101bc54d9c1` | `research/reviews/unrelated_machines/truncated_vector_greedy_review.md` | `f44814c28e337ff312506d6caf6c5c34ce6c6aa78b3c10f5e8f2ae34b5383369` | 16295 | 已整合到固定阶真实源反例对象 |
| `91d907ecfa2f31c5aa82` | `research/reviews/unrelated_machines/two_level_label_fee_escape_review.md` | `8727c124eff0c31cf4c03720765ee046d4124850dddf4c2c3d23a96446d1e5e6` | 38609 | 已整合到第二重数恒等式对象 |

两个冻结提交的同路径字节均按库存视为同一源版本；没有把 legacy-cleanup 与 main 重复计算成两个证明。

## 实际读取与复核范围

* 小任务源逐节读取独立陈述先行稿、作者/最终 canonical 读后记录和有限审计范围。解析合同包含零端预处理、同一全局 big/tiny Hall 匹配、严格前缀计数、Hadamard/Cramer 余量以及三值 selector 的绝对阈值。有限证据是 9 个联合槽成功、15 个拒绝、5 个 capped 算术检查，奇偶 `ell=2,3` 全部分配和 6 个三值矩阵共 816208 个分配；这些数字只作为审查记录，不替代全称证明。
* 压缩向量源逐节读取真实有限源、全 (V_r) 投影、future-feature 正交、位复杂度和独立 Fraction 审查。固定 (r) 的解析族给 `OPT=B` 与普通机峰 `q`；有限运行完整枚举 (r=1,q=7,11,13) 和 (r=2,q=11,13)，其中 (r=2) 未形成完整 (V_2) 矩阵，故仅作支持证据。
* 两层标签源逐节读取独立重构、作者 canonical/read-after、generic 构造审计和 actual-option DFS。承重恒等式是 `OPT=1+L*/D`，严格阈值为 `C<1+1/D`；循环移位族的有限重放覆盖空图、孤点、非单射投影和 `D=2,3`。没有把有限程序升级为求 (L^*) 的算法或一般近二困难性。

## 复现边界

上述源正文和审查记录是冻结证据；本目录没有复制临时 scratch 代码或输出。任何未来改动需以新来源指纹重新 clean show、读取和登记；旧审计的 `passed`/退出码不能替代数学量词检查。
