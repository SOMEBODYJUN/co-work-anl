# v5 冻结结果摘要

Boss1；RUN `six-boss1-20261111`。保留全部 v4 的 225 原始行，加 Main 释放的 320 条全 source31 行与 1 条 BG 投影；共 546 raw、533 unique、全 256 类型加 K 共 257 列。只运行一次已授权 LP，随后准确恢复及独立 Fraction 检查全部通过。

普遍下界和该指定必要系统的精确最优值为

\[
\frac{W}{\operatorname{OPT}_6}\ge
\frac{2474258697351416114163812246401701803}
{5634528256756333986258798947915358765}
=0.4391243746776041\ldots.
\]

11 个正客户型、11 条正付款；全部 546 原始行和 257 列余项非负，互补、零原对偶差。K 约 .18677361051859434。244 列余项正、13 列为零，K 余项为零。全部原始付款与精确值在 [proof.md](proof.md) 和 [exact_certificate.json](exact_certificate.json)。不认领优于其他既有最佳下界，也没有证明 half。

新增正 family 行只有源2的 `(T,Q)=(A4,X),(A5,A6),(A6,A5)`。BG 行保留完整小负 K 系数，当前 slack 约 .005194972810286275，付款为 0。

独立的 0 优化器诊断还得到整个必要系统最优面

\[
z=z^*+s e_0,\qquad s\ge0.
\]

同一真实第二源的31预算取等，强制其前三个真实尾包含于 T 且各大小 K，从而必须 |T|=K。但该整面上的 K−|A4|、K−|A5|、K−|A6| 分别约 .00895831510100、.01876487812478、.01698095901517，均严格正。因此**整个 v5 最优面不能实现为 SPE**。这没有改动 546 行输入或增加优化；等号诊断与全257 signed identities 已另存本包。

| 文件 | SHA256 |
|---|---|
| exact_input.json | `3b2065e702c5590d50ebc8acd5ea30337e82db2a84585f87040acd36e91db553` |
| exact_certificate.json | `5e5a2377ed780f4a9c9f58ca8703fc5a473d41ea1945a654aa0ee6c0efa0deda` |

重放命令：

```bash
python research/workspaces/six-boss1-20261111/universal_union_wallet_v5/check_source_and_certificate.py
python research/workspaces/six-boss1-20261111/universal_union_wallet_v5/check_equality_diagnostic.py
```

两者均不运行优化器。Main 收尾提出的25倍同源付款亦经本包独立456态及320×257列分解预检，通过；结果另存 `source25_diagnostic.json`，不进入546行输入，可运行 `check_source25_diagnostic.py` 重放。所有131旧冻结文件保持原字节；本包在证明、精确证书与可复用等号缺口处停止。
