# 五名提供者的半覆盖：完整历史纯 SPE 的精确证书证明

## 精确身份

**Claim `CA-FIVE-HALF-EXACT-v1`，已证明（精确计算机辅助证明；内部复核，未记录外审）。**

对每个有限单位客户集 N、每个有限非空共同目录 S⊆2^N，以及恰五名单位权提供者的每份完整有序历史依赖纯 SPE σ，实际终局满足 `2W≥OPT_5`。客户价值在最终覆盖者间均分。空主题、重复主题、重复比较索引、零客户与全部历史上的任意平局均保留。依赖 [CAG-MODEL](model.md)。不声称任意背景五人剩余利润定理、六人定理、一般人数定理或锐性。

## 唯一完整证明与精确数据

用户本轮上传的原包已按原字节保存在 [证明包目录](../../../customer_attraction/proofs/half5_exact_v1/README.md)：

| 资产 | 内容与读取条件 |
| --- | --- |
| [中文主证明](../../../customer_attraction/proofs/half5_exact_v1/PROOF_ZH.md) | 固定同一份完整 σ、定义所有实际和离轨主题、全类型覆盖、整数恒等式及全部乘子；引用本定理必读。 |
| [活跃行语义](../../../customer_attraction/proofs/half5_exact_v1/ACTIVE_ROWS_ZH.md) | 逐条对应最终使用的真实节点、偏离、菜单和投影；审查强制者与真正后继的最优性时读取。 |
| [局部引理](../../../customer_attraction/proofs/half5_exact_v1/LOCAL_LEMMAS_ZH.md) / [最大根引理](../../../customer_attraction/proofs/half5_exact_v1/MAXROOT_LEMMA_ZH.md) | 明确局部非负组合、隐藏回复消元及共同 K 的来源；推广人数时先检查适用条件。 |
| [证书](../../../customer_attraction/proofs/half5_exact_v1/certificate.json) / [行清单](../../../customer_attraction/proofs/half5_exact_v1/row_manifest.json) | 最终整数乘子、公共分母、冻结局部表及来源哈希；核验器的输入。 |
| [本轮复跑证据](../../../evidence/customer_attraction/half5_exact_v1/import_verification.json) | 原包全部哈希核对，以及原包之外保存的局部和主域复跑记录。 |
| [入库审查](../../reviews/customer_attraction/five_player_half_import.md) | 本轮数学读取、精确复跑、独立检查与未覆盖事项；不把历史日志冒充新实现。 |

证书 SHA-256：`395e056b218d237abe8b85db894f0b1c37d2e14d55c74b1dca723abeceb6a44e`。

## 闭合机制

固定任意五个合法比较主题，O 为其并集大小，K 为共同目录最大主题大小。每条合法行写成 `S_j=Σ_x a_j(ω_x)+k_j K≥0`。原包给出正整数 L_j 和全类型非负整数余项 R，使

\[
120\cdot10^{22}(2W-O)
=120\sum_{j=1}^{53}L_j S_j+\sum_x R(\omega_x)+271784400K.
\]

右端逐项非负，故对任意比较五元组都成立；取最优五元组得到结论。没有除以 W。

承重信息是：实际末位的完整目录最佳回复，给所有真实离轨主题同一个价格上界；局部投影保留其价格成本，最终主证书统一支付这些成本。末两人关系同时保留比较主题重叠。隐藏回复的逐客户消元与索引直方图使任意客户数、目录大小归入完整有限系数域。

**本证明的有限性是系数类型域的有限性，不是对有限客户数或有限目录规模的抽样实验。** 各回复族独立取最大只扩大类型域；没有假定原策略可独立选择回复，也没有把同计数历史强制合并。

## 重放与审查边界

从包目录运行局部核验器会写入其本地报告；如需保留冻结包字节，应在副本中运行，并将新结果另存 evidence。主核验可直接指定独立输出路径：

```sh
python customer_attraction/proofs/half5_exact_v1/components/verify_local_components.py
python customer_attraction/proofs/half5_exact_v1/verify_certificate.py --manifest customer_attraction/proofs/half5_exact_v1/row_manifest.json --output /tmp/half5_exact_check.json
```

本轮复跑得到：局部 36 组件、47,872 系数状态通过；主域 6,144 条件全部通过，最小清分母客户余项 0，K 列余项 2,264,870。判号使用 Fraction 或 Python 任意精度整数；NumPy 只承载整数表。

原包交付一个主域核验器和一个局部核验器。`checks/primary_full_domain.json` 是随包历史输出；本轮没有取得对应的第二个可运行主域核验源程序，不以该日志声称双主实现复跑。完整数学审查、程序复跑、外审和新颖性分别记录。

## 对一般人数的作用

一般 `Q-CAG-HALF` 仍 OPEN。五人结论不能直接用于有背景的五人后缀，也不能把源代码常数 5 机械换成 6。下一步提取任意人数的共同末位价格与隐藏回复投影，明确跨分支行和共同预算，再在六人完整类型域上检验；五人整数乘子仅作为机制来源。
