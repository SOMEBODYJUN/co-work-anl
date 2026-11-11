# 最大裸大小 C 真根分支的内部钱包：精确新根界

Boss1；RUN `six-boss1-20261111`。本轮只写本摘要与 `maximal_root_tail_wallet/`，此前 `universal_true_x_tail/` 不变。一轮小型 LP 发现后，精确原始/对偶与独立字面核验均完成。

## 可直接使用的新必要行

对原有限单位客户、共同合法标签目录、完整有序历史纯 SPE，actual 根收益 u、真实全目录最大裸大小 K、最优六标签并 O 满足

\[
\boxed{112944305160u-11595684007K-2178783435O\ge0.}
\]

该证书不使用 OPT 分支覆盖帽，故 O 更一般可取任意六个合法查询标签的覆盖并。没有选择或假设任何 f_P 最大 X；唯一被强制的根标签 C 是裸大小最大标签。

在指定 K0=`24376964954228547006/142891298915142483961`、O=1，本轮 71 行有限必要锥的精确最优值为

\[
u_* =\frac{197998925913631121419767306359}
{5379586156460209884457196512920}
=0.03680560551592973\ldots.
\]

Main NEW 在该点给 `0.03368410087708602…`；本轮精确提高
`341445530563148400742229293643/109384918514690934317296329096040`
≈`0.0031215046388437047`。新根线优于 Main NEW 恰在
`K/O < 8701782449/37000646641 ≈ 0.2351791992564166`。

## 为什么提高

强制 C 后，完整保留其真有序分支 `(C,B2,B3,B4,B5,B6)`。10 个正对偶预算是根 IC、全部五个尾标签大小帽、真 source 3/4/6 的 Omean SAFE，以及同一真末两位的 **PAIR(Omean,Omean) 全 36 配对**。所有收益属于这同一根 C 分支。第五位没有单独正 SAFE 权，其真实收益通过最后两位 PAIR 承重。

两条自由质量乘子保留为
`πp=18687762431/56472152580` 和 `πo=145252229/7529620344`；五个 CAP 的 K 右端全部回收到根线系数。全 128 原子余项非负，13 零、115 正，u 列余项为零；因此该行对所有原类型普遍有效，不是固定 K 数值关系。

## 完整有限系统和证据

全部 128 Boolean 型 `(p,y2,y3,y4,y5,z,o)` 加 u 共 129 列，保 o=0、全零型及两个质量式。71 原始行包括 1 根 IC、5 CAP、1 branch-union OPT 帽、1 K/6 地板、35 internal SAFE、28 final PAIR。零行和重复行均保留。分支覆盖帽及 K/6 地板对偶权为零。

匹配精确原始点有 10 个正原子，不构成 SPE 实现。独立标准库 checker 重建 9159 个矩阵项，核全部 71 原始行、129 对偶列及 K/O 两个参数列，精确目标完全一致；28 个旧来源文件不变。仅一次 LP 已消耗；不再优化。

| 文件 | 内容 |
|---|---|
| [proof.md](maximal_root_tail_wallet/proof.md) | 根线证明、十个整数预算、两自由乘子、精确点和与 Main NEW 的比较 |
| [derivation.md](maximal_root_tail_wallet/derivation.md) | 优化前全部真实钱包及 full36 来源 |
| [exact_input.json](maximal_root_tail_wallet/exact_input.json) | 完整 129 列 71 原始行；SHA `3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65` |
| [exact_certificate.json](maximal_root_tail_wallet/exact_certificate.json) | 精确匹配原始/对偶；SHA `80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771` |
| [all_129_column_checks.tsv](maximal_root_tail_wallet/all_129_column_checks.tsv) | 全 128 型及 u 的原始值、对偶余项 |
| [check_literal.py](maximal_root_tail_wallet/check_literal.py) | 不导入 builder、不调优化器的确定性字面检查 |
| [literal_certificate_check.json](maximal_root_tail_wallet/literal_certificate_check.json) | 独立 PASS、原始/对偶精确目标与全列核验 |
| [freeze_manifest.json](maximal_root_tail_wallet/freeze_manifest.json) | 最终冻结与新包哈希 |

结论是新全域必要根线和指定有限锥在 K0 的精确最优值，不是所有 K 上最优根界、half 证明或完整 SPE 反例。未重优化旧 217 行点，未进行大系统合账；后续装配由 Main 单独授权。
