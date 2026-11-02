---
id: customer-attraction/static-optimal-matching-random-complete-policy-cone-probe
kind: program
type_tag: 程序
title: 静态最优匹配随机完整策略锥探针
status: full-source-read-and-default-run-complete; auxiliary-static-bridge-refuted-elsewhere
truth_status: finite-search-only; no-new-counterexample; no-universal-bound
review_level: exact-source-execution-with-preserved-dependencies; current-formal-counterexamples-compared
scope: seed 87129; 420 sparse integer-customer seeds at p,m equal to 3,3 or 4,4 or 5,4 or 6,4; only deduplicated non-PNE roots enter the LP attack
summary: 随机驱动先用精确整数缩放的完整历史倒推生成纯SPE，再按策略字典去重并筛选非静态PNE的实际叶，调用既有固定锥静态最优匹配攻击。默认原字节执行仅送入两个锥且未输出精确反例，不能证明一般桥；同一静态桥已由另一三人1953客户和四人52客户完整证书否定。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/cone/probe_static_matching_random.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/cone/probe_static_matching_random.py
source_ids:
  - d2ec05dffb737730fbee
---

# 被测桥及准确量词

有限单位客户有共同目录标签 `0,...,p-1`；客户兴趣类型由非空标签掩码 A 表示，重数为非负整数。m 名单位提供者按全部有序历史选标签，终局每个客户在覆盖者中均分。本源只测试下面的**辅助静态桥**，不直接测试六人半覆盖。

固定一份完整纯SPE及其实际终局 z，记 W 为实际福利。删去实际玩家 i、冻结其余实际行动后，标签 a 的静态替代收益为

$$F_i(a;z)=\sum_{x:a\ni x}\frac1{1+c_x(z)-\mathbf1_{z_i\ni x}}.$$

旧候选希望存在一个最优 m 主题元组 T 和一个索引排列 π，使 `sum_i F_i(T_{π(i)};z) <= W`。若该条件成立，则实际未覆盖但 T 覆盖的每个客户至少在一项静态查询中贡献 1，所以遗漏覆盖不超过 W，进而 `OPT_m <= 2W`。这只是充分推导；SPE 的真实偏离会改变后缀，不能用 SPE 激励直接压冻结 F。

原程序调用的 `try_cone` 实际只枚举 **m 个互异标签**的 supports `combinations(range(p),m)` 及其全部排列。由于本源总有 p>=m，福利单调性保证某个 m 元互异 support 达到最优福利；但若某个最优覆盖已可用少于 m 个标签达到，重复 padding 的静态匹配成本是否更低仍需另核，不能把“所有 m 元互异支持”自动称为“所有重复索引元组”。本次无候选输出，故没有需要扩域认证的反例；将来若 `try_cone` 返回候选，必须补上重复最优元组检查，或证明其最优覆盖确实需要 m 个不同标签。

# 精确种子策略与两层筛选

3723 字节原程序的 `random_spe(p,m,w,rng)` 接收整数兴趣类型重数。置 `s=lcm(1,...,m)`；它把每个终局收益乘 s，在所有客户负载为 1,...,m 的分母上变成整数。因此倒推比较和值相等的平局选择是精确整数计算。

程序先为全部 `p^m` 个有序终局保存计数向量，然后从深度 m-1 倒推到根。在每个有序历史 h，对所有标签 a 读取已经固定的子终局收益，随机选一个收益最大动作。每个孩子已由同样规则构成纯SPE，当前动作又是最佳回复，故递归得到该**种子输入**的一份完整纯SPE，覆盖离轨历史与任意随机平局。这里没有把计数状态相同的不同有序历史强制合并。

主循环固定随机种子 87129，依次测试 `(p,m,trials)=(3,3,100),(4,4,100),(5,4,120),(6,4,100)`，共 420 个抽样种子。每个种子从非空掩码中有放回抽取 2 至 9 次，每次加权 1、1、2 或 3，因而实际输入是稀疏整数客户类型。由生成动作字典的完整签名去重后，再用 `StrategyCone.verify(w)` 的 Fraction 行核验种子权重满足所有有序历史 IC。

第二层只保留实际终局不是静态PNE的策略锥。这个限制有数学理由：如果 z 是静态PNE，则每个 F_i(a;z)<=u_i(z)，从而对**任何**排列都有总和不超过 W，因此它不可能是本静态桥反例。筛选代码用普通浮点直接收益及 `1e-8` 阈值，不应把该筛选本身另称通用精确PNE认证。

# 固定策略锥的后续攻击

每个保留锥会调用另源 `probe_static_opt_matching.py` 的 `try_cone`。其共同固定策略 Γ 行全部保留，对一个指定最优互异 support J 加覆盖最优性行，归一化 W=1，并最大化该 J 的所有排列静态成本高于 W 的共同余量。发现正浮点余量后，以 Fraction 重建并检查 Γ、非负客户重数、福利归一、全部最优互异 support 和所有排列；返回值还带可清分母的 `integer_clones`。接受端的有限精确条件与浮点候选生成分开。

本源独有内容是**随机完整有序BI生成、整份策略去重、非PNE实际叶筛选与攻击编排**；LP、精确恢复和静态成本定义属于导入源的内容，不能把两个驱动说成两个独立数学实现。初始种子是真实整数客户SPE；后续LP变量则是该固定策略内的连续非负兴趣权重，只有被精确恢复并清分母后才可能成为新的单位客户证书。

# 本次真实执行

原字节脚本与原字节 `probe_static_opt_matching.py` 放回隔离 runtime 中的原相对深度，满足后者 `parents[5]` 定位；没有修改任一源码。`customer_attraction_strategy_lp.py` 及四个 `customer_attraction` 文件从已归档 `strategy-cones/original` 复制，SHA和来源见 runtime manifest。执行命令：

```text
PYTHONDONTWRITEBYTECODE=1 python3 runtime/research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/cone/probe_static_matching_random.py
```

进程 exit 0、stderr 为空；420 种子循环中只有以下两个去重后的非PNE锥被送入攻击：

| cone | p | m | trial（本组索引） | 实际有序路径 |
|---|---:|---:|---:|---|
| 1 | 4 | 4 | 19 | `(0,0,2,1)` |
| 2 | 6 | 4 | 62 | `(1,0,4,2)` |

末行是 `no_exact_counterexample_in_processed_cones`、`processed_nonPNE_cones=2`。本次 wall-clock 字段约39.23秒；elapsed 依环境变化，不是数学字段。没有生成 `static_opt_matching_counterexample.json`。这是本次原字节执行结果；冻结清单没有给本脚本配套的历史 stdout，不能声称与历史运行逐字节重现。

该结果只表示这两个筛后策略锥没有被当前有限发现/恢复器接受的反例；没有精确对偶最优证书，也没有穷尽其所有可行权重，更没有枚举所有策略或目录。420 个种子也不能写成“420 次完整锥攻击”。

# 后续纠错与可接续用途

已全文比较[正锥与均匀真实组合安全接口的历史分层](../资源/正锥与均匀真实组合安全接口的历史分层--资源.md)、[冻结终局后缀的最优主题排列预算反例](../反例/静态最优主题排列的冻结后缀失败--反例.md)和[真实最优组合的净差匹配与共同付款](../候选/真实最优组合的净差匹配与共同付款--候选.md)。

同一冻结静态存在桥已由另一三人1953单位客户完整SPE反驳：W=1735，唯一最优支持 `{1,2,5}`，所有排列最小静态成本1736>W，且最优覆盖确需三个标签；四人52客户证书也提供同类反例。因此本源原时点“未找到/运行中”只保留为有限发现历史，不能恢复该桥当前为OPEN，更不能用本次阴性推翻已发表反例。

真实净差匹配使用改变后缀后的真实收益，并只支付 `OPT-W`；它与冻结 F 不同。上述1953客户例最好真实匹配1734远高于净差5，故静态桥失败没有否定那个更弱候选。恰六人半覆盖也未被本源解决或反驳；代码只有 m=3,4，p=6 只表示六标签。

本源建议 integrated 为程序/有限计算对象，保留原字节、必要依赖、stdout、stderr与manifest。后续若复用生成器，应把“找新静态桥反例”改为当前未决的准确数学目标；保留完整历史与重复标签量词，另行认证新目标而不重新给已否桥授OPEN状态。与固定锥LP是实现依赖，与1953/52反例是后续真值纠错，与真实净差候选仅是范围对比；本次不建立第三阶段超边。
