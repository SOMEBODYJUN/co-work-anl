# R-428：五人根续接与尾部 LP 停界

## 稳定身份与来源

本页处置七个来源版本：`e5f0500e497d4ef77a6f`（README）、`affb51b29415737dc725`（`five_c/root_cg.json`）、`374c9ffa5ddd91f85166`（`five_c/root_pricing.py`）、`43029622360f8045a351`（`five_e/search_last_deduction.py`）、`31e9da2667907884436c`（`parent/root_tail_lp.py`）、`745517e0827a7fc9c75e`（`parent/root_tail_lp_result.json`）和 `8146c21161122fb5070a`（workspace 元数据）。每项均以 `clean show` 导出、全文或逐字段读取；README 与元数据中的旧 Boss/旧 clone 身份不覆盖当前 Boss3、`repository-cleanup` 与 `rebuild/research-v2`。

这是 **审查/计算停界**，不是五人 HALF 证明。来源目标是五名提供者、全部有序历史纯 SPE、有限单位客户和共同目录下的 `OPT_5\le2W`；该限制目标仍 OPEN。所有 LP 和搜索都只给必要不等式的松弛、有限实验或候选筛查，不能替代客户级可实现性、完整历史动作表和 SPE 最优回应。

## 模型路径和真正新增对象

本批把旧的四人尾部比例界接到根最优主题的四位真实后继，并考虑根改实际末位 `E` 的完整真实路径。四条路径是

\[
ABCDE,\qquad EFGHI,\qquad AEUVW,\qquad ABEXY.
\]

`root_tail_lp.py` 对 14 个主题的全部 (2^{14}=16384) 个客户成员类型建立分母保底、最优五主题聚合、尾二税、尾三/四利润 lift 以及三条真实 `E` 偏离 IC；它明确把变量 (O) 当作由有效聚合比较约束的松弛变量，而不是某个实际最优菜单。`root_pricing.py` 把根后继 `T,X,Y,Z,K` 的必要回复行加入旧 `full_pricing` Universe，并用列生成/定价寻找违反列；它依赖旧 `full_pricing` 输入和 SciPy，源文件没有给出精确对偶恢复。

## 实读和复现结果

### 尾部 LP

对 `root_tail_lp.py` 逐行读取并在导出副本上直接运行。HiGHS 返回 `status=0`、`Optimization terminated successfully`，支持集空间为 16384 个成员类型，约束行数为 222，浮点发现目标为

\[
2.209867046461754,
\]

且最小浮点 slack 为 \(-2.42861286636753\times10^{-16})，这是数值舍入量级的零。报告明确写 `discovery relaxation only, never an SPE certificate`。该值与 README 所说的旧无索引上界约 2.0616947857 不同，原因是本批把根/真实后继行纳入了另一套必要松弛；它既没有给出 (2) 的普遍上界，也没有证明该松弛不可加强。

### 根列生成发现

`root_cg.json` 的报告逐字段读取：包含 720 条根扩展行、1890 个当前列（初始 1570 列，五轮每轮加入 80 列），浮点 dual beta 从 1.9744176489、1.9980650983、2.0045198189、2.0118859711 增至 2.0166955106；五轮定价最小值仍为负（最后约 (-10.0227)），所以这不是已闭合的列生成证书。报告的 `scope` 是 `Numerical discovery necessary-condition relaxation only`，其 support atom、histogram 和 dual multipliers 只是发现记录；没有精确 primal/dual 恢复、没有整数客户重数实现，也没有全历史 SPE 证明。

`root_pricing.py` 的数学边界必须保留：每一行是必要 SPE 不等式的候选编码；根后继份额、四人/三人利润函数和真实偏离行都在固定路径标签下计算。代码在 `root_score`/`root_price` 中以有限成员类型和直方图取价，不能由此推出所有目录、任意平局或任意完整历史的共同支付。

### 有限最后扣除筛查

`search_last_deduction.py` 逐行读取并直接运行默认参数：(q=5,k=3,	ext{prefix}=0)，1000 个固定种子 `117` 的随机有限试验，输出 `status=no_hit`。源码先枚举有限终局组合、递归计算可行后继的 floor/最佳回应集合，再筛查 `F > 2R_actual - u_last` 的路径。无命中只能说明该参数和样本的有限筛查没有找到候选，不能外推为一般不存在反例或定理。

### 版本元数据

`workspace.json` 只有 schema、旧 save、旧 actor 和 instance UUID，不含定义或计算证据；作为 provenance 保存，不生成新的数学对象。

## 结论等级、失败机制和用途

**条件/计算结论。** 在这套 14 主题、四条路径、必要行和有限成员类型的松弛中，尾部 LP 的可发现值为 2.20986704646，根列生成的当前 dual beta 为 2.01669551062 且仍可被负定价列改进；二者都没有达到 HALF(5) 所需的 2，也没有精确证书。

**有限实验。** 1000 次最后扣除随机筛查无命中；尾部 LP 的 16384 类型 HiGHS 运行可复现，最小 slack 为浮点零。实验保留脚本和报告在 `archives/customer-attraction/tools/evidence/r428-root-continuation/`，没有把运行结果写成一般性证明。

**主要障碍。** 松弛变量 (O) 没有被识别为实际可实现的最优菜单；根列生成尚未停止，旧 `full_pricing` 依赖不能从当前冻结来源自动补造；根改分支的真实后继动作、所有偏离后的完整策略和客户整数重数尚未同时构造。README 提醒“根最优主题四人真实回复”仍需覆盖全部客户类型的非负精确恢复，不能用旧尾四人比例界代替。

**接续用途。** 后续若继续此方向，应先补齐旧 `full_pricing` 输入并对负定价列做精确 Fraction 恢复，再给出每个新根分支的完整真实 IC 和整数客户实现。若仍只有必要松弛或有限无反例，应继续归入计算/审查，不能升级为五人 HALF 证明、SPE 反例或任意人数结论。空主题、重复、零客户和任意平局的主模型量词仍不因本批而改变。

## 处置结论

七个来源均 **integrated**：README 保留五人目标与 OPEN 状态；`root_tail_lp.py`/结果保留 16384 类型、222 行和 2.20986704646 的可复现实验；`root_cg.json`/`root_pricing.py` 保留 720 行、1890 列、beta 轨迹及未闭合定价；`search_last_deduction.py` 保留 1000 次无命中筛查；workspace 元数据仅作版本追踪。没有将任何有限松弛误报为完整 SPE 或 HALF 结论。
