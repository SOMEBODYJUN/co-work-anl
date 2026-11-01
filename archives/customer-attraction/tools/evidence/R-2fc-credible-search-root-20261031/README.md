# R-2fc credible-search root tail — Boss2 cleaner

本目录保存六个已认领来源的实际 `clean show` 原件、JSON/脚本副本、独立字段复核和运行日志。六次 `clean show` 均退出 0、stderr 为空；stdout 的字节与 `source-manifest.json` 记录一致。凭据没有写入任何证据文件。

## 来源分组

- `m5p7_2210000.json`（`9dd325f6b652dc4cc0f1`）和 `m5p7_3200000.json`（`998df8512cbe0c0bbafc`）：五人七主题、受限支持但允许完整有序历史的 half 探针。两次 HiGHS 均 `status=1`、25 秒时限、没有 incumbent，`exact_candidate=null`；这只能是未决有限搜索，不能当作不可行性或 half 反例。
- `tight_markov_00011.json`（`4b182703448445426eaa`）和 `tight_markov_00112.json`（`3ccd633444ddd50af4b5`）：以 `valid_conditional_big_M=1` 收紧的 count-Markov 发现子类。两次 MILP 都时限到达且浮点 bound 不是证书，但脚本输出各有一个 objective/ratio 为 1 的 exact candidate；这保留为有限候选，不能升格为一般完整策略或六人 half 结论。
- `tight_markov_probe.py`（`0694ab24765066a3e411`）：脚本逐字保存；它只把 W=1 上界用于发现阶段，并在候选后展开/检查完整有序历史。该“发现子类”和完整历史验证必须分开陈述。
- `largest_incumbent_n3p6_best.json`（`7d8c67861a5d1cd5fdf1`）：与既有 R-18 证据同 SHA 的 963 单位客户 JSON。现有对象已经记录其五个根盈利偏离；本批只做同字节保全和字段复核，不重新声称 SPE。

## 独立复核

`replay/validate_root_batch.py` 解析六源，确认两个 restricted-half timeout、两个 tight-Markov finite candidates、旧 incumbent 的五个根坏行及 `full_history_SPE=false`，并检查探针脚本语法和 scope 标记。运行结果在 `replay/validate_root_batch.stdout`，退出 0、stderr 空。

## 数学边界

- `floating_value`、`status=1` 或 `floating_bound_not_a_certificate=true` 不是 infeasibility、最优性或全称结论。
- 计数 Markov 的发现约束不代表一般完整有序历史策略；原模型允许相同计数的不同历史选择不同续局。
- tight-Markov 的 exact candidate 是一个有限候选输出；由于 MILP 发现阶段时限且无 dual support，不能把 ratio 1 解释为全局最优或通用界。
- `verified:true` 只是旧生成 JSON 字段，实际完整历史检查在根处发现五个严格盈利偏离，故不能恢复 SPE 认证。
- 当前六人 Q-CAG-HALF 全称目标仍 OPEN。
