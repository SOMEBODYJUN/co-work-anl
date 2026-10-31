---
id: "customer-attraction/R-171-fixed-population-pair-error"
kind: computation
type_tag: 引理
title: "R-171 固定人口 pair 误差与 ghost-rent 系数"
status: "finite-exact-definition-audit"
truth_status: "exact-local-algebra-and-finite-path-checks; no-full-SPE-transport"
review_level: "full-3160-byte-read-and-Fraction-replay"
scope: "R-171 coupling/audit_fixed_population_pair_error.py; h in {0..32,64,127,1000}, 2<=r<=16, 1<=s<r, binary memberships; m<=11 path checks"
summary: "独立脚本从收益定义以 Fraction 计算 r>s pair-circuit error，核对四种二值会员表、(r-s)(r-1) ghost-rent 支配系数及 r=2,s=1 等号；再对 m<=11 的全部二值路径和两种 s 模式检查归一化误差不超过 ghost budget。它是局部代数和有限实际路径审计，没有构造完整 SPE 运输。"
source_refs:
  - "clean:78ded6e12066708990fc:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/audit_fixed_population_pair_error.py"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/audit_fixed_population_pair_error.py"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/README.md"
  - "local:archives/customer-attraction/state/引理/R-171稀疏槽clock租金与skip-premium分解--引理.md"
  - "local:archives/customer-attraction/state/反例/R-171完整SPE稀疏槽租金障碍--反例.md"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "dd305dd277ad25b1b82c6449e01d15354909e909"
  source_sha256: "027c0d1e7d1f7f891b77732fd0282d7c1f0cdced7143889172d07c9cfc9b0443"
  source_size_bytes: 3160
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/audit_fixed_population_pair_error.py"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/replay/audit_fixed_population_pair_error.stdout.json"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/comparisons/comparison-notes.md"
---

# R-171 固定人口 pair 误差与 ghost-rent 系数

## 1. 局部误差对象

源脚本完整实读 3,160 B，SHA-256 `027c0d1e7d1f7f891b77732fd0282d7c1f0cdced7143889172d07c9cfc9b0443`，稳定 ID `78ded6e12066708990fc`，blob `dd305dd277ad25b1b82c6449e01d15354909e909`。它不导入作者其他模块，只使用标准库 `Fraction`、`itertools.product` 和 JSON 输出。

设 (h\ge0) 是某客户在 pair-circuit 前的背景命中数，(a,b\in\{0,1\}) 表示该客户是否属于两类查询主题 (A,B)，且 (r>s\ge1) 是两个固定人口参数。脚本直接按收益定义计算

[
\begin{aligned}
E_H^{r,s}(A,B)= {}&rs\,\frac{a}{h+ra+sb}
+r(r-s)\,\frac{b}{h+sa+rb}\\
&-s^2\,\frac{a}{h+sa+rb}
-(r-s)\frac{b}{h+1},
\end{aligned}
]

其中分子为零的项由 `own` 定义为零。对应宽二基准 ghost rent 是

[
G_H(A,B)=h\left(\frac1{h+1}-\frac1{h+1+a+b}\right).
]

将 (a,b) 的四种值化简，脚本要求精确等式：

| (a,b) | 精确 (E_H^{r,s}(A,B)) |
|---|---|
| (0,0) | (0) |
| (1,0) | (dfrac{(r-s)hs}{(h+r)(h+s)}) |
| (0,1) | (dfrac{(r-s)h(r-1)}{(h+r)(h+1)}) |
| (1,1) | (dfrac{(r-s)h(r+s-1)}{(h+r+s)(h+1)}) |

在这些二值类型上，脚本还精确检查

[
0\le E_H^{r,s}(A,B)
\le (r-s)(r-1)G_H(A,B),
]

并在 (r=2,s=1) 时检查 (E_H^{2,1}=G_H)。因此 ((r-s)(r-1)) 是脚本核对的统一比较因子；README/CLAIMS 进一步把它解释为一般 pair-circuit 的逐客户支配系数。

## 2. 固定人数路径预算检查

第二段循环对 (m=1,ldots,11) 的每个二值实际路径 `bits`（共 (2^m) 条）和两种模式执行：

- mode 0：(s=1)；
- mode 1：(s=\lfloor(n-1)/2\rfloor)，其中 (n=m-j)。

对每个 (j=1,ldots,m-3)，令 (b) 为前缀命中数，(n=m-j)，(r=n-s)，故 (r>s\ge1) 且 (j+r+s=m)。脚本把

[
\frac{E_H^{r,s}(A,B)}{j(r-s)(r-1)}
]

累加为 `weighted`，把 (G_H(A,B)/j) 累加为 `dominating_ghost`。若实际路径总命中数为 (c)，则比较

[
\text{weighted}\le\text{dominating\_ghost}
\le 1-\frac2{c+1}quad(c>0),
]

空路径 (c=0) 的上界取 0，并另外核对上界不超过 1。该式是对有限二值路径和两种选择模式的直接审计；它没有枚举任意主题目录、客户重数、离轨后继策略或完整 SPE 约束。

## 3. 实际执行结果

我直接执行原脚本，stdout 与源 JSON 完全一致：

```json
{
  "status": "all direct-payoff and fixed-population path checks passed",
  "scope": "algebraic errors and arbitrary actual paths; no SPE transport constructed",
  "local_membership_cases": 17280,
  "fixed_population_path_cases": 8188,
  "all_primary_pair_profiles_have_exactly_m_players": true,
  "uniform_comparison_factor": "(r-s)*(r-1)"
}
```

`local_membership_cases=17280` 等于 (36\times120\times4)：(h\in\{0,\ldots,32,64,127,1000}) 共 36 个值，(r=2,\ldots,16)，所有 (s<r) 和四种 (a,b)。`fixed_population_path_cases=8188=2\sum_{m=1}^{11}2^m`，对应全部二值路径和两个 mode。JSON 是该脚本的冻结原输出；replay 文件是本次执行的同字节结果。

## 4. 证据边界

这份审计支持：局部收益公式的精确化简、二值会员域内的非负性、((r-s)(r-1)) 支配因子，以及有限 (m\le11) 二值路径的归一化 ghost 预算检查。它不单独证明 README 所述任意主题/任意完整路径的根支付，也不证明每个 pair-circuit 是真实 SPE 的偏离收益。特别是 `R-171稀疏槽clock租金与skip-premium分解` 已显示，稀疏槽收费会产生不能自动删除的 skip-premium；`R-171完整SPE稀疏槽租金障碍` 则给出完整 SPE 族中的调和发散但 half 取等。

因此本对象处置为 integrated 的有限精确审计和待接入引理接口，不升级为 Q-CAG-HALF、一般付款算法、完整 SPE 运输、hardness 或 unrelated-machines 结论。
