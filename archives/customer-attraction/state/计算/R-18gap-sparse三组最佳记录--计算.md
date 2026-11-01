---
id: "customer-attraction/R-18-gap-sparse-three-best-records"
kind: computation
type_tag: 计算
title: "R-18 gap-sparse 三组最佳记录"
status: "finite-sparse-best-records"
truth_status: "finite-exact-enumeration-at-recorded-instances; no-universal-result"
review_level: "full-225-346-1032-byte-read-and-reduced-replay"
scope: "R-18 literature_mechanism/gap_sparse_best_m3p4.json, m4p5.json, m5p7.json"
summary: "三份稀疏 probe 记录分别给 (m,p)=(3,4): OPT=15,W=9,min-pay=3,factor=2；(4,5): 21,12,3,factor=3；(5,7): 27,15,3,factor=4。每条 factor=m-1，低于 gap-floor 严格 violation 的 factor>m 门槛；这些是有限 best 记录，不是 Q-CAG-HALF 反例。"
source_refs:
  - "clean:fb2cdf5d1079b8c9e81b:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_sparse_best_m3p4.json"
  - "clean:b68d081acd3fe482e71c:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_sparse_best_m4p5.json"
  - "clean:9fc58a4018a8cde1b7ad:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/literature_mechanism/gap_sparse_best_m5p7.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_best_m3p4.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_best_m4p5.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_best_m5p7.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_sparse_results.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/comparisons/comparison-notes.md"
source_identity:
  records:
    - id: "fb2cdf5d1079b8c9e81b"
      blob: "cd5d1bd0d812fbdaf38cee0c3ab9536dcaea83c9"
      sha256: "da3badd3fabfbed1c0ba1c3f333bceedccc31e68a9ec15e0127469e8d227f477"
      size_bytes: 225
    - id: "b68d081acd3fe482e71c"
      blob: "97444d6199a985589bcb90293eaba17dd6ba0156"
      sha256: "67cc274f0ab3c2c11ad2ee1454d9bcae72b20b775af0afec5ef9d635eebbe271"
      size_bytes: 346
    - id: "9fc58a4018a8cde1b7ad"
      blob: "3269a00dc9293f8c1da6e46b0ea7899b439fbc70"
      sha256: "68a4913196e60ce8341ffd9d4bdf14e164510ba6f3aa626b87464135694d2e5b"
      size_bytes: 1032
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_best_m3p4.json"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_best_m4p5.json"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/original/gap_sparse_best_m5p7.json"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/replay/reduced/gap_sparse_results.json"
  - "archives/customer-attraction/tools/evidence/R-18-gap-probes-20261031/comparisons/comparison-notes.md"
---

# R-18 gap-sparse 三组最佳记录

## 精确字段

三份 JSON 均完整读取，并与 `gap_sparse_probe.py` 缩短重放的首轮输出相符。它们的非零类型都是单例主题：

| ID | m,p | 非零客户类型（mask:重数） | q | OPT | W | min pay | factor=(OPT-W)/min pay |
|---|---|---|---|---:|---:|---:|---:|
| `fb2cdf5d1079b8c9e81b` | 3,4 | 1:9, 2:3, 4:3 | [3,0,0,0] | 15 | 9 | 3 | 2 |
| `b68d081acd3fe482e71c` | 4,5 | 1:12, 2:3, 4:3, 8:3 | [4,0,0,0,0] | 21 | 12 | 3 | 3 |
| `9fc58a4018a8cde1b7ad` | 5,7 | 1:15, 2:3, 4:3, 8:3, 16:3 | [5,0,0,0,0,0,0] | 27 | 15 | 3 | 4 |

这里 `q` 是保存的终局计数向量；`opt` 是在脚本的主题组合域上计算的最大覆盖，`w` 是该终局福利。每条 factor 都是 (m-1)，因此 gap 为 3(m−1)，而指定终局最小玩家收益为 3。

## 脚本量词

`gap_sparse_probe.py` 对每个随机重数用 Fraction/LCM 计算所有终局的整数效用，`spe(q)` 递归保留达到子局 max-min 门槛的全部可信终局，随后在全部 `comps(m,p)` 主题计数组合上求 OPT，并选取该实例中最大的 factor。原程序设置每组 5,000 轮；本轮缩短回放各执行 10 轮，首轮立即得到上述三条同值 best，未把缩短轮数冒充原 5,000 轮完整结果。

## 与 gap-floor 条件的区别

`gap_floor_probe.py` 寻找的是 (m\min u < OPT-W)，即 factor (>m)。本批三条 sparse factor 为 2、3、4，分别严格小于 m=3、4、5；它们是稀疏最佳记录，不是 floor 违反。它们也没有给出 `OPT/W>2`：比率分别 15/9=5/3、21/12=7/4、27/15=9/5，均小于 2。

本对象处置为 integrated 的有限 exact-record 计算页；没有一般 factor 上界、全策略反例、Q-CAG-HALF 或 unrelated-machines 结论。
