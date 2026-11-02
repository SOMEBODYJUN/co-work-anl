# 私有核与两标签路径的冻结原件及精确核验

主数学见[两标签实际路径的全目录有理覆盖证书](../../../state/计算/两标签实际路径的全目录有理覆盖证书--计算.md)；根入口的历史版本和旁引状态见[工作区版本入口](../../../state/资源/静态CCE间隙与私有核障碍工作区的版本入口--资源.md)。本目录保存六份冻结原字节，不用结构摘要代替448236字节的大JSON。完整commit、blob、SHA-256、原路径及大小在 [manifest.json](manifest.json)。两来源提交为 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，六文件两提交内容分别相同。

| 源ID | 原件 | 字节 | 内容及处置 |
|---|---|---:|---|
| 183bd96eea2a1aaa8c39 | [根README](original/README.md) | 3550 | 全文保入口的CCE、分数覆盖、收益图三阶段、六目录及未付义务；与当前正式结论分列 |
| ec060c4b3e27cb295502 | [private_guard.md](original/private_guard.md) | 4705 | 全历史cap1及局部保留菜单、m≥7不可补全族、同质多诱饵障碍和严格前提；已有容量资源含主证明，本批补primary证据和必要行接口 |
| db1489fe344348e1a916 | [private_guard_audit.json](original/private_guard_audit.json) | 24662 | 顶层全部字段、m7..50共44案例及m7约分数值全部读回和精确重建 |
| 4a135a131769d88f4cd2 | [private_guard_audit.py](original/private_guard_audit.py) | 2091 | 全文理解；导入原coeffs的依赖、44案例必要行及断言、实际写出位置均核实 |
| 2761d1fa1de684caadaa | [two_support_obstruction.json](original/two_support_obstruction.json) | 448236 | m2..10全部1022词及各有理乘子/余项字段完整精确检查，非只读取最坏值 |
| 85672653e9eb9e9717ae | [two_support_obstruction.py](original/two_support_obstruction.py) | 3837 | 全文理解；有限原子、真实保底/末两人税行、浮点候选恢复及精确余项检查，未输出完整SPE策略 |

## 两个不同层次的真实运行

原程序在clone外独立目录执行，未改冻结原件。Python3.12.14、NumPy2.3.5、SciPy1.17.0。两进程exit0：

```sh
python3 private_guard_audit.py
python3 two_support_obstruction.py
```

两份生成JSON与冻结输出逐字节相同（SHA同manifest）。[replay-metadata.json](replay-metadata.json)保存程序、依赖版本及原/新SHA比较。原运行目录、输入副本和stdout是临时运行材料；因重放输出与冻结JSON字节相同，本目录仅保一份JSON，避免制造两份相同证据。

原private程序的stdout为：

```json
{"cases":44,"m7_impossible_path_ratio":"97/48","minimum_guard_gap":2,"all_necessary_rows_nonnegative":true}
```

另一层核验是[verify_frozen_certificates.py](verify_frozen_certificates.py)。它只用Python标准库，**不导入**原 `coeffs` 或任何生成器，不调用LP/SPE求解器，从正式对象展示的逐原子公式重建所有行。可在复制此目录后的任意可写位置运行：

```sh
python3 verify_frozen_certificates.py original verification.json
```

该命令完整读取两JSON的每条记录和每个字段，检查集合/词顺序/所有汇总标志；重新计算有理乘子、每原子余项、每份最小余项及44个私有族案例的所有值。其 [verification.json](verification.json)保留：

- 全1022个有序词、2396个非零有理乘子、39930个原子对偶余项，负余项0；重建1670050个两支持行系数。
- 私有族44个案例、5236个必要行求值、726132个原子行系数；m7约分、全部零行和每个数值字段一致。
- 每个人数的精确最大证书值、首个对应词、对应稀疏对偶；小数proposal只作与该有理值的容差一致性检查，不承担证明。

它认证所给完整词集合的有理证书与必要行算术。它没有枚举所有SPE、产生七人反例、认证原作者外审或证明所有人数half。原生成器只归一化实际W、优化必要行；七人以上必要行可行的显式客户点还需真实离轨最优性，而本批guard解析证明恰将其全部排除。

## 实际比较与版本缺口

本批实际读取了现有共同目录模型、固定背景两人税界、末AB严格二倍定理、私有容量资源、整数污染守卫、CCE反例及其最新锐值、分数覆盖真实前缀引理、真实收益比较图定理与菜单/Markov后续边界。另以 `clean search private_guard` 和 `clean search two_support_obstruction` 检索冻结MD，并全文读取相关counterexample/README（源 `7cd7873a588332fd1884`，同提交同工作区路径）；它明确列五人15/8、六人137/70及七人后必要行不闭合2。相关阅读只用于比较，不额外办理其primary处置。

现有私有容量资源已经完整陈述4705字节早期cap1主源及反族，并明确其当时未办理primary done；本批补上原件、原程序/报告、完整证书范围及运行核验，不重复造同一guard定理。两标签有限人数结果与末AB全人数定理的假设不同，不能仅用后者吞掉前者的全部32词及末BB证书。根入口42客户发现版仅有源述，本批不以README独立认证其未取得的客户/策略/对偶；八客户当前正式锐值另有完整对象。

逐源收据在 `cleanup/workspaces/Boss6/private-guard-receipts.json`，仅声明本批实际阅读、比较和独有去向；其内容不替代数学核验，也不预称已经推送或done。
