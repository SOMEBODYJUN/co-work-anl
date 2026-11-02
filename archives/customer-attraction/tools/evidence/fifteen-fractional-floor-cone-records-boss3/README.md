# 十五份自由分数地板锥记录的证据范围

主源仅 `9dc18dac0787b3042451`，原5494570B JSON保在[original](original/fractional_floor_cones_n4k6.json)，SHA256 `7d3755c796965db4fb5c8e9217570a2a9e3c3b3b06d9f2109636cd3044451723`。两个完整冻结提交、source path/blob/size和保存位置见[source-manifest.json](source-manifest.json)。没有用重构账替代原文件，没有删15记录的重复项。

[正式正文](../../../state/计算/十五份自由分数地板锥记录的完整矩阵身份与单客户零债--计算.md)自足写明模型、15记录/14字段的两组身份、完整初值、共同策略、矩阵来源、单客户自由值和精确数值误差。既有生产程序和静态定理仅同SHA复用，见[依赖及比较](dependency-and-comparison-reading.json)。根负责Git/claim/done；本stage不修改共享正文或原字节。

## 全量实读及新执行的必要性

原文件根状态NUMERIC_EXPLORATION_ONLY，15条均NUMERIC_CANDIDATE_ONLY、n4/k6/floor。全部字段逐值分组，只有initial和trace有两组，另12字段同。全部1260项保存policy和4590行/289170系数均遍历；共同policy84项、共同矩阵306×63。原同SHA仅见inventory身份，无充分的原policy/target/rows与保存点精确成功，因此新增一次针对固定原数据的标准库审计，补这个具体绑定缺口。

[audit_fifteen_records.py](audit_fifteen_records.py)不导入任何原producer、Search、canonical BI、NumPy或SciPy。它确认本特殊policy完整覆盖84个计数前缀且各唯一动作，再独立展开259有序历史；检查全部target索引与真实完成叶，重建306条有理真实IC，所有15份原浮点系数逐项核原转换身份，最后核单单位客户下1554真实收益比较。它没有重求初值的BI、原策略选择、完整锥优化或其它实例。

唯一真实[execution-record](replay/execution-record.json)开始UTC2026-11-02T14:38:33.601371+00:00，elapsed0.9154928940006357秒、returncode0、stderr空、断言开。新驱动12475B，SHA256 `bdbb5fa55c05803c703bbe6aff58fad7bfdba69428ac29baf5cd995eb2534d79`；stdout383B，SHA256 `f50d2aeeb7b745c5cd5c748b520cbeb0f5ddd9cf9ff040fc133d97dc8d5467a9`。原main/LP/SLSQP/BI/RNG全0次。

## 完整账、分组和原误差

[exact-review.json](replay/exact-review.json)保存各字段的比较组与SHA、15记录各自的初值总量/47与63坐标、原30条trace、原负零位置、矩阵/有序域计数、原p/q/z的精确二进制值和另立的新有理背景。source SHA及全部14字段关系一起保，不只留“最终单客户”的摘要。

[complete-exact-ledger.json.gz](replay/complete-exact-ledger.json.gz)解压117001B，SHA256 `4667f6aa2b34c18efbde8c16eb71f76234cff3d9d3b27ee30bc327333b26a2a9`。其内容是全部126终局索引、84 target绑定、259有序历史所有偏离利润/slack、306×63整数12Γ及每行所有计数来源位置。该账是新独立重构，不冒原JSON字节或原发现者的完整运行日志。

实际共同最终权重mask47=1，其余±0，五个同覆盖标签A/B/C/D/F和空E全部保留。真实BCCC路径利润各1/4，W=OPT1，单客户静态双边证明t4=1/4，因此真实地板差0。原30条trace的debt−2^-53只来自返回value=1/4+2^-53，不是严格反例。一般FF早已被另一个完整银行族反驳；本保存点不是那个族，也不改变其证明。

原p恰是δ_A且精确可行，原q虽各坐标非负，其精确二进制和超1，保持原值不修复为通过。原z47=1/4+2^-54，以原p/z仍可独立算Fenchel下界1/4−2^-106，给地板差的正上界2^-106；没有负的有理上界证书。新q*=(1/5,1/5,1/5,1/5,0,1/5)及其63个逆分母单独标为新见证，不回写原q/z。

策略count展开可行仅因本文件每计数前缀唯一且域完整，不能用来删别的(q,target) DAG的target。矩阵身份与一个点可行不提供整个锥的地板下界，也不提供一般逐人或六人half结论。[关系证据](relationship-review.json)和逐源收据保这些边界；关联四代码不额外done。
