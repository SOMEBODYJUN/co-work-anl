# 最优fresh费用的精确审计及有限浮点攻击

两份自足计算对象分别说明[精确支持枚举](../../../state/计算/最优覆盖查询费用的精确支持枚举--计算.md)与[严格最优支持策略锥攻击](../../../state/计算/严格最优覆盖支持的完整策略锥攻击--计算.md)。候选定义、正确静态式及未核实历史断言在已清洗[最优自留预算](../../../state/想法/最优覆盖查询的自留份额预算--想法.md)。本批不修改旧共享正文，不将比较源再登记完成。

## 正式五源及字节

Boss4确认正式claim pushed `6015570f6c0db3c8c3e52fbbabb8ee88976fb1ab`，synced。五主源合计19059B，正式确认后重新全文读并核inventory SHA；原始字节保留原路径，两个冻结来源逐字节核对相同。

|源ID|原文件|字节|
|---|---|---:|
|e34ee6479d87bca78052|audit_optimal_fresh_self_reserve.py|3681|
|c320561014ad69bbebf0|audit_optimal_fresh_self_reserve.json|7553|
|2abfdaad5623537eeb3a|attack_optimal_fresh_policy_cones.py|4546|
|7cfd730044a42f607965|attack_optimal_fresh_policy_cones.json|1950|
|4ff936ca40b885e9237f|README.md|1329|

共同原目录为 `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/geometry/`。每份的完整path、blob、SHA、双commit和阅读角色见 [source-manifest.json](source-manifest.json)。

## 完整冻结扫描域与真实依赖

原精确脚本扫描顶层 `evidence/certificates/customer_attraction/*.json`，仅读存在同名 `examples/customer_attraction/*.json` 的配对。为保全部scan/skip语义，保存完整冻结顶层29个证书及22个example，共51个JSON、2339418B，放入 `original/` 和独立 `replay-tree/` 的原路径。两个冻结提交 `git ls-tree` 得出的非递归JSON集合与保存集合准确相同，见[目录清单](frozen-directory-listing.json)。嵌套子目录不属于原glob，未偷偷扩大原入口范围。

29个证书里16个进入solve，3个配对被读取但选中层无terminal_counts，10个没有同名example而内容未被原程序读取；example里3个没有同名证书。逐项名字和原因在[补核记录](supplement/input-scan-and-multiset-check.json)。这51份全字节保全并由补核完整JSON解析，记录角色为依赖/目录证据，**不声称已独立完成其数学语义清洗**。

精确原程序实际使用example全部客户类型/整数多重数、m/p和证书所选层的terminal_counts，忽略actions。浮点原程序仅读四对JSON，使用example的m/p和证书全部actions，忽略旧重数与所存terminal_counts：worst_cce_welfare_failure、aggregate_theta_failure、individual_security_failure、prefix_balance_failure。所有字段使用差异在正文说明；没有仓库helper依赖。原代码、51文件与放置树的精确身份见[运行输入清单](runtime-input-manifest.json)。

## 两个原入口各一次

原程序未改写，ROOT仍由`__file__.parents[6]`计算，cwd为新隔离树，运行只禁写pyc。两入口顺序各执行一次，exit0、stderr均空，代码和全部目录输入前后SHA不变。

|入口|秒数|新JSON字节|与冻结报告|
|---|---:|---:|---|
|audit_optimal_fresh_self_reserve.py|0.0630037784576416|7553|逐字节相同，SHA0042a21501a17483c18361773a0e9f8f3cde25c093e237d764963e89c9ecbdba|
|attack_optimal_fresh_policy_cones.py|1.281893014907837|1950|逐字节相同，SHAee17a8e793e1fc2abe0965ad7106768b78a781cfa1d21243d8bd6042393ede96|

Python3.12.14、numpy2.3.5、SciPy1.17.0。精确入口只用标准库，浮点入口用SciPy HiGHS。两份原stdout/stderr、命令、次数、环境、时间和输出SHA记录于[execution.json](replay/execution.json)；[精确新报告](replay/audit_optimal_fresh_self_reserve.json)与[浮点新报告](replay/attack_optimal_fresh_policy_cones.json)和 `original/` 中旧报告分别保存。原stdout文件名为 `exact-fresh.stdout.txt`、`float-policy-cones.stdout.txt`，stderr相应保存。上一批仅全文比读而未执行的历史保持，不回填成以前已经跑过。

另有本批新写的静态补核：完整解析51个JSON，对16份使用中策略检查有序历史键集/合法动作、根重放计数一致；不核IC。随后不用原程序、不调用原solve，直接枚举2767个大小恰为m的主题多重集，得到同样的OPT/minK0/W/R0/余量。补核实际运行一次，代码在本批cleanup工作区 `inspect_inputs_and_multisets.py`，结果另在 `supplement/`。它是读原实现后的不同枚举方式，非盲实现、非SPE认证、非LP精确对偶。

## 数学与证据边界

精确16行全部候选余量正，有限输入中未见S?反例；真正m槽算法靠全目录cheapest补齐，支持小于m没有丢重复。浮点四锥共65目标，57个获求解器成功报告，8个无成功报告；非精确可行/不可行证书。固定归一化eps=1e−6还排除更小正间隔的严格唯一输入，最优平局、小支持和其他策略都未覆盖。中间两锥最佳点最小IC约−4.37e−8、覆盖gap略低于eps，容差不可抹掉；没有精确dual或一般锥定理。

没有负点也就没有精确恢复负点。本批没有把程序文件名、负候选余量的假设情形或无分离报告当half结论。若未来S?被精确否定，还需另算2W−OPT判half；原强minfresh-OPT断言未找到证书，不能由冻结Q反例或任意单query加强失败替代。

五份comparison-only原件全文对读：已清洗fresh工作稿、零损失门独立review、共享saddle几何checkpoint、13人36客户算术、旧13人安全最优query攻击状态。前两份与当前正式对象完整核同数学，saddle说明等价格/PSD/KKT与未付half-slot关系；原件不额外done。当前五人half另证、六人开放，不由这些有限程序提升状态。

工作区 `check_package.py` 只核字节、冻结目录集合、链接、receipt及已有执行记录，不运行原程序或补核。[verification.json](verification.json)是结构证据；人的数学判断、全仓比较和关系理由分别记录在该工作区self-review/relations，二者不可互代。原入口README的六项资源/状态全部由两计算正文承接，不另复制导航冒充数学对象。
