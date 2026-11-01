# R-18 gap probes 五源比较记录

## 来源与重放

| ID | 文件 | 大小 / SHA-256 | 处置 | 重放 |
|---|---|---:|---|---|
| `25a41ee07de97123bfb6` | `literature_mechanism/gap_floor_probe.py` | 1066 B / `957f93496d1b0509b119b048bc10d3e058c3f0bebaa04df6bfb8de581161ff7a` | integrated | 缩短 rounds 10/5/2，三组均 completed，无 floor candidate |
| `fb2cdf5d1079b8c9e81b` | `gap_sparse_best_m3p4.json` | 225 B / `da3badd3fabfbed1c0ba1c3f333bceedccc31e68a9ec15e0127469e8d227f477` | retained | factor=2、m=3、OPT=15、W=9 |
| `b68d081acd3fe482e71c` | `gap_sparse_best_m4p5.json` | 346 B / `67cc274f0ab3c2c11ad2ee1454d9bcae72b20b775af0afec5ef9d635eebbe271` | retained | factor=3、m=4、OPT=21、W=12 |
| `9fc58a4018a8cde1b7ad` | `gap_sparse_best_m5p7.json` | 1032 B / `68a4913196e60ce8341ffd9d4bdf14e164510ba6f3aa626b87464135694d2e5b` | retained | factor=4、m=5、OPT=27、W=15 |
| `01be6b7ef76d2362b2db` | `literature_mechanism/gap_sparse_probe.py` | 2515 B / `9845ae5847a1a43921e8ee180b36deddbbed4f996a0d37c2df60b9738fa55bf4` | integrated | 缩短每组 10 轮；首轮得到三份同值 best，无 FAIL |

## 数学对象和关键区分

`gap_floor_probe.py` 的严格目标是 `m * min_pay < OPT - W`，即 `factor=(OPT-W)/min_pay > m`。三份 sparse JSON 的 factor 为 2、3、4，而对应 m 为 3、4、5，均未达到 floor violation；不能把它们按文件邻近误归类成 floor 反例。

`gap_sparse_probe.py` 则在完整可信终局递归 `spe(q)` 中最大化同一 factor。每组最佳记录具有简单 singleton 结构：

| m,p | 非零 mask:重数 | q | OPT | W | min pay | factor | OPT/W |
|---|---|---|---:|---:|---:|---:|---:|
| 3,4 | 1:9,2:3,4:3 | [3,0,0,0] | 15 | 9 | 3 | 2 | 5/3 |
| 4,5 | 1:12,2:3,4:3,8:3 | [4,0,0,0,0] | 21 | 12 | 3 | 3 | 7/4 |
| 5,7 | 1:15,2:3,4:3,8:3,16:3 | [5,0,0,0,0,0,0] | 27 | 15 | 3 | 4 | 9/5 |

这些结果说明 sparse factor 至少达到 m−1 的有限构造；它们没有达到 m，也没有达到 `OPT/W>2`。

## 与全仓相关对象对照

- 与已有完整树/策略锥对象：本批 `spe(q)` 对给定客户质量递归保留可信终局集合，证明的是该有限实例内的终局选择，不是所有完整策略树或所有客户质量的量词。
- 与 R-18 aggregate-security：前一批随机安全预算脚本求的是静态 minimax 预算 `W-C`/`W-nv`；本批求的是终局 gap factor `(OPT-W)/min_pay`，目标和量词不同，不能拼成预算或 half 反例。
- 与现有 `静态安全值与聚合保底`、`固定安全预算锥障碍`：那些对象有固定输入的 Fraction/策略证书或指定查询预算；本批 JSON/探针主要是随机 sparse search，证据层级更弱。
- 与 `gap_floor_probe.py`：严格门槛是 factor>m；本批 sparse best 的 factor=m−1，故应记录为接近障碍的有限候选而非反例。

## 结论边界

五源支持的只有：三组有限 sparse best 记录、缩短回放的可执行性、以及 floor 条件在所测轮数内未触发。没有证明：

1. factor≤m 的普遍上界；
2. 任意完整 SPE 的 gap floor；
3. `2W<OPT`、Q-CAG-HALF 反例或一般福利比率；
4. 任意人数/目录的算法、hardness 或 unrelated-machines 结论。

三份 JSON retained，两个脚本 integrated；所有回放都明确缩短轮数，避免把有限实验冒称穷尽搜索。
