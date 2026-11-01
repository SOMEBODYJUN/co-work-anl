# R-2fc global_proof C：根势独立复放与截断势探针

本批处理四个已认领源，四次 `clean show` 均返回 0。原始 stdout/stderr 在 `clean-show/`，源字节及冻结 blob、大小、SHA 在 `source-manifest.json`；运行清单和独立验证在 `run-manifest.json` 与 `run/validation.json`。四个源均来自 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）及 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）同一路径版本。

## 逐源阅读与复放

- `831052265f6603650b50` `root_potential_independent_audit.json`：全文读取 78 个整数单位客户的固定策略报告。根终局 `(1,5,5)`，`W=54`、`OPT=75`、`Phi=Psi=141/2`，258 项含自身比较、215 项非自身比较、最小 slack 0，`2W-OPT=33`。
- `aad3b319edcc95b5d6d7` `root_potential_independent_audit.py`：逐行读取 `Fraction` 单位客户展开、完整有序历史、根/次根/末位策略、所有 6 个动作偏离和普通/截断势。独立副本运行默认模式与 `--minimized` 均退出 0；默认输出与 JSON 的核心字段一致，`--minimized` 恢复同策略的 11 客户点：`W=8, OPT=11, Phi=21/2`，仍有 `2W-OPT=5`。
- `d7389f400d38f77ec31d` `truncated_potential_audit.json`：全文读取固定候选的 43 个有序历史/258 项比较结果。其 78 客户、实际 `(1,5,5)`、`W=54`、`OPT=75`、普通/截断势 `141/2` 与根独立脚本一致；它是固定候选精确审计输出，不是搜索空间全称。
- `900e8c0df5857ce636c5` `truncated_potential_probe.py`：逐行读取 q=6、r=3 的随机权重生成、Markov 逆向策略、所有单步 SPE 约束、截断势目标和 scipy `linprog` 输出。副本以 `--trials 3 --seed 29393` smoke run 退出 0、stderr 为空、best=0；这是浮点发现探针，不能把无命中解释为不存在性。

## 数学去向

四源共同固定一个 3 人、6 主题、78 客户候选。独立 Fraction 复放确认它是完整历史纯 SPE 证书，并确认调和势与截断势都低于 `OPT`：`141/2 < 75`。程序的 `--minimized` 分支同时提供 11 客户精确障碍：`Phi=21/2 < 11`，与既有十一客户反例对象数值一致。两项都满足 `2W>OPT`，所以不能作为 Q-CAG-HALF 反例，也不能证明一般的调和势支配失败以外的命题。

`truncated_potential_probe.py` 搜索的是固定 Markov 策略锥和有限 q/r 的线性规划；`root_potential_independent_audit.py` 才承担给定候选的精确全历史核验。两者量词分开记录，不能把随机 LP 无命中升级为一般定理。
