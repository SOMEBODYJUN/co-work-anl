# 共同 X 的 OPT6 交换：零新增必要行

Boss1；RUN `six-boss1-20261111`。**已独立核验并冻结完成；不追加矩阵，不派优化。**

正式模型的 `OPT6` 确为全目录六标签元组最大覆盖。当前原 16 hist 的 `d` 全为 1，
归一恰为全部 `H_h` 之和，因此表示范围内不存在最优并集外客户。

任意 `k≤6` 个合法标签并集 `V` 的交换计数式为

\[
\binom6k|V\setminus U|\le
\sum_{d=1}^k\binom{6-d}{k-d}|\{j:d_j=d,\ j\notin V\}|.
\]

对 `V=X∪⋃_{i∈S}A_i`、`k=1+|S|≤6`，当前支持上的行严格等于

\[
\binom5{|S|}\sum_{h:\,a_h\cap S=\varnothing}(H_h-x_h),
\]

由旧 20910–20925 行 `H_h−x_h≥0` 的非负组合支付。

- 64 子集检查中，63 条合法交换式；唯一 `k=7` 子集明确排除。
- 交换族 39 个不同向量、29 个正比例类。
- 加上七个“从 `A1,…,A6,X` 中选六个”的并集 cap，共 70 候选、40 不同向量、30 正比例类。
- 单条旧 22297／final 23676 行相等或正比例命中均为零，但全部 70 行有精确旧约束非负组合证书，故不能认领新 cut。
- 六个含 X cap 即 k=6 交换式；actual-only cap 是五个 `actual_bits=000000` 的 H 非负列之和。
- 独立审计通过 516096 个完整 `d/actual/X/S` 案、57344 个六选七 cap 案，及全部 70 行的 21021 坐标核验。
- 原 16 hist、所有 21021 描述符、六个历史零 hist 均保留；新列 0、追加行 0、优化器 0、点文件读取 0、冻结输入写入 0。

完整证明、边界和精确索引见 [report.md](opt6_shared_x_exchange/report.md)；
全部候选及旧行证书见
[candidate_rows_and_certificates.json](opt6_shared_x_exchange/candidate_rows_and_certificates.json)；
独立审计见 [literal_audit.json](opt6_shared_x_exchange/literal_audit.json)；
输入和输出 SHA 由 [freeze_manifest.json](opt6_shared_x_exchange/freeze_manifest.json) 绑定。

该有限路线已闭合，无需等待当前 23676 云点。原六人 `2W≥OPT6` 仍 OPEN。
