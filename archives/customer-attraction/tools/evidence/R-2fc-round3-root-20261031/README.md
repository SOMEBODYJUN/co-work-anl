# R-2fc round3_root exact-tax 三源清洗

三个源均在认领后执行 `clean show` 返回 0，并以冻结原文、blob、SHA、大小保存于 `source/` 与 `source-manifest.json`。源代码与报告属于 `round3_root` 的辅助桥探针：它们研究完整纯 SPE 锥上的更强实际分数负载预算

\[
m\max_T g(T)\le W+G,\qquad
g(T)=\sum_{x\in T}\frac1{1+((m-1)/m)c_x},
\quad G=\sum_{c_x>0}\frac1{1+((m-1)/m)c_x}.
\]

## 逐源处置

| ID | 文件 | 处置 | 实读和复放 |
|---|---|---|---|
| `115b42a116e15b821e19` | `exact_tax_probe.py` | integrated | 完整读取随机实例、`ExactSPESolver` 证书、全有序历史/偏离矩阵、LP 目标、理性重构与 `verify_certificate` 分支；`py_compile` 和短 m=4/m=5 smoke run 通过。|
| `c0c1973365884e5cbf7e` | `exact_tax_scan_m4p6.json` | retained | 读完 40 次 m=4,p=6 扫描；每次 1295 个偏离行，`best=-0.25`，状态 `finite_probe_only`。|
| `a3fa866a17aaafa76def` | `exact_tax_scan_m5p6.json` | retained | 读完 50 次 m=5,p=6 扫描；每次 7775 个偏离行，trial 35 有 2 个完整 SPE outcome，其余 1 个，`best=-0.2`，状态 `finite_probe_only`。|

## 数学范围

`exact_tax_probe.py` 不是对所有完整 SPE 的枚举。每次试验随机抽掩码客户权重，调用 `ExactSPESolver` 取一个 outcome（奇数 trial 取 welfare 最小 outcome，偶数 trial 随机取），再随机选择证书动作和续局平局。随后对全部长度 `<m` 有序历史、所有非规定主题构造 SPE 锥的 IC 行，用浮点 `scipy.optimize.linprog` 检查指定查询主题的辅助桥目标；只有正值候选才用有理逼近、整数缩放和 `verify_certificate` 做精确源模型核验。代码没有产生 `exact_tax_failure_m4p6.json`/`m5p6.json`，因此当前两份 JSON 只说明有限随机扫描中未找到正候选。

m=4 的冻结报告含 40 个 trial（虽然探针默认 `--trials=50`），m=5 含 50 个 trial；两者均只在 `p=6` 固定主题数、固定种子下运行。m=4 每 trial 的历史数为 `1+6+36+216=259`，非自身偏离行 `259*5=1295`；m=5 为 `1+6+36+216+1296=1555`，行数 `7775`。短复放在 `run-manifest.json` 指明的 `tmp/varying_baselines/customer_attraction` 依赖下退出 0，stderr 为空，未生成失败 JSON。

这三源没有证明预算桥、半覆盖或六人目标。它们保留的用途是：若未来同一桥在某个完整 SPE 锥上出现正候选，沿代码已有的 Fraction 重构和 `verify_certificate` 路径形成可审计精确证书；当前负 best 只是一组有限 no-hit 记录。空主题、重复目录、零客户、任意平局和离轨历史没有被这组随机扫描的量词覆盖。
