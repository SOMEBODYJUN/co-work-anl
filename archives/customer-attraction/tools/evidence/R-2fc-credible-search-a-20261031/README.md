# R-2fc credible_search 十源清洗证据

本证据包对应 Boss2 认领的十个冻结 source version。十次 `work.py clean show <id>` 均实际调用并退出 1：当前 partial clone 的 promisor remote 试图连接 `browser-proxy:8889`，随后无法取得对应 blob。每次 stdout 为空，stderr 逐源保存在 `clean-show/<id>.stderr`。为完成逐源实读，我按冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 的原始路径打开 raw 页面，逐字读取四个 Python、三个审计 JSON 和两个完整策略 JSON，并把冻结 inventory 的 blob、大小、SHA-256 对入 `source-manifest.json`。同一路径在 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 是相同 source version，不计作第二次独立数学证据。

## 源文件承担的实际义务

* `audit_dag_candidate.py` 是不导入 customer_attraction 求解器的标准库 `Fraction` 验证器。给定 `instance/strategy` 或 `exact_candidate/milp` 报告后，它恢复每个客户类型的整数重数，枚举 `m` 人的全部有序历史，检查每个节点的所有非自身偏离、终局计数、福利和静态 OPT；只在没有 violation 时写 `full_history_SPE=true`。它是验证实现，不是搜索或全局定理。
* `audit_old_largest_incumbent.py` 同样用单位客户和 `Fraction` 审计旧 R-18 三人六主题候选。其实际结果是根规定 0 的五个替代动作全部盈利，故 `verified:true` 不能作为完整 SPE；独立本地重核见 `run/old_largest_incumbent_recheck.*`。
* `dag_individual_probe.py` 复用 unrestricted outcome-witness DAG，目标为 `coverage(J)-(2m-1)u_a(q)`。浮点 MIP 只生成候选；随后调用 exact recovery，输出仍标 `universal_claim_proved=false`。冻结有限运行的三个超时 incumbent（m4/p5 两例、m5/p5 一例）和完整历史规模写入 `run/dag_individual_historical_summary.json`。
* `dag_restricted_half.py` 在相同 DAG 上加入合法必要行 `|T| <= m*u_a(q)`，并在发现阶段限制每个客户至多关联一个未使用根主题（`outside-order=1`）。m5/p7、J=23456、floor 1.8 的两个 25 秒运行均无 incumbent；变量数 42345、二元变量 41888。限制是实验开关，超时不能解释为不可行。
* `cyclic_construct.py` 先用旧浮点 oracle 提议一个前缀 0 的后缀，再按 p=7 的 19 个循环客户轨道做有理 LP、旋转到全部首动作分支，最后恢复整数客户并做完整有序历史核验。它的目标可以是 individual 或 half；19 个种子是有限搜索队列，不穷尽循环实例。
* `cyclic_m3p7_individual.json` 是 m=3,p=7 的一个完整有限 pure SPE：14 单位客户、57 历史、342 非自身比较、路径 0-5-2、收益 (3,4,4)、W=11、OPT=13、`OPT/u_0=13/3<2m-1=5`，故不是个体桥反例。
* `cyclic_m5p7_half.json` 是 m=5,p=7 的一个完整有限 pure SPE：7 单位客户、2801 历史、16806 非自身比较、路径 0-4-1-3-6、五人收益均 7/5、W=OPT=7，`OPT/W=1`。它支持一个合法点，但不构成六人 half 的全称结论。
* `cyclic_candidate_audit.json` 独立 `Fraction` 审计上述两份 cyclic JSON，逐历史没有 violation，minimum slack 为 0。
* `extra_candidate_audit.json` 审计七个 m=3 的固定候选（m3p6 三项、m3p5 两项、m3p6 mid 两项）；全部完整历史 SPE，但 W=3 或 4、OPT=5，均有正 half 余量。
* `individual_candidate_audit.json` 审计三个 DAG individual 候选：m4/p5 的 W=19/OPT=19、W=5/OPT=6，以及 m5/p5 的 W=1/OPT=1；全部完整历史 SPE，均没有 half 反例。

## 独立重核和输出

`run/independent_summary_validator.py` 对三个审计 JSON 的 12 条记录重算：

* 历史数为 `sum(p^d for d=0..m-1)`；非自身比较数为历史数乘 `(p-1)`；
* `half_gap = 2W-OPT`；
* `minimum_weak_individual_gap = (2m-1) min_i u_i - OPT`；
* 所有记录 `full_history_SPE=true`、`violations=[]`、`minimum_slack=0`。

运行 exit=0、stderr 为空；12 条记录的 `max(OPT-2W)=-1`，即本批所有完整点都严格满足 `2W>OPT`。这只是已保存点的定义级一致性检查；不把有限点提升为任意输入的 `OPT/W<=2` 证明。

`run/exact_audit_old_largest.stdout` 是原 `audit_old_largest_incumbent.py` 在临时依赖布局中的一次原字节重放（`source/audit_old_largest_incumbent.py` 的 3344B SHA-256 与冻结 inventory 完全相同）；`run/old_largest_incumbent_recheck.py` 另作同逻辑本地重核。两次均读取已归档的 R-18 5707B JSON，展开 963 个单位客户、43 个历史和 215 个非自身比较。它复算出五个且仅五个根盈利偏离：替代 1、2、3、4、5 的偏离收益分别 303、303、357、190、303，而规定根 0 的收益为 375/2；实际路径 0-2-3、W=750、OPT=963。运行 exit=0、stderr 为空，源 SHA 与冻结值 `7dcd445b...fcbbd` 一致。

这两次本地运行复核的是已经读取并保存的审计结果/归档原 JSON，未伪装成重新执行缺失依赖的 DAG MILP。DAG 的超时/无 incumbent 状态按冻结运行实况保留，未重新解释为数学不可行。

## 处置边界

本批归档 12 个有限完整策略证书和一个旧候选根遗漏障碍；不形成完整证书、普遍上界或六人 half 反例。`cyclic_m5p7_half.json` 和 `dag_restricted_half.py` 保留为有限候选/有限实验；旧 `largest_incumbent` 通过现有审查对象撤回“完整 SPE/个体桥反例”标签。所有源身份、clean-show 失败和本地运行的 stdout/stderr/status 均保存在本目录。
