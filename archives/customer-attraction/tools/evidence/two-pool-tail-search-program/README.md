# 双客户池的可信三人尾搜索：证据合同

主源 `9178a319461f5fdf746b` 是3726B `two_pool_tail_search.py`。本包保全原字节、数学解释和一次原main的完整实际证据；[程序正文](../../../state/程序/双客户池的可信尾局搜索程序--程序.md)定义客户块、全部收益、可信过滤的充要证明、实现安全界、预滤及结论边界。

## 文件与入口身份

| 文件 | 角色 |
|---|---|
|[original/two_pool_tail_search.py](original/two_pool_tail_search.py)|两冻结提交相同的原件；SHA f268d9322c947d4bf805397b2c489f7f310b81966c9f4d8b8378bfb93376746e。|
|[run_original_once.py](run_original_once.py)|透明runpy/profile记录器，仅观察未改原main及批返回；不改数组或参数。|
|[rerun/execution.json](rerun/execution.json)|真实环境、时间、路径、前后SHA、调用数及输出字节比较。|
|[rerun/captured-batches.json](rerun/captured-batches.json)|同次运行的809批摘要和完整门槛直方图；非第二次搜索。|
|[rerun/two_pool_tail_search.json](rerun/two_pool_tail_search.json)|隔离运行生成的429B结果，逐字节同[冻结报告](../two-pool-tail-search-data/original/two_pool_tail_search.json)。|
|[rerun/stdout.txt](rerun/stdout.txt)、[stderr.txt](rerun/stderr.txt)|原stdout425B，包括末行 `survivors 0 []`；stderr0B。stdout整体不是单个JSON。|
|[related/research_README.md](related/research_README.md)|全文比较的1744B工作区README；其鲁棒前缀无界松弛族是另一数学对象。|
|[manifest.json](manifest.json)、[self-check.json](self-check.json)|来源、共享输入与交付指纹，静态解析和范围核对；不调用数学入口。|

唯一原执行发生于2026-11-01，Python3.12.14、NumPy2.3.5，耗时16.869292686秒。命令为：

```text
python -B /workspace/scratch/c0ab78c47566/round13-two-pool-work/run_original_once.py /workspace/scratch/c0ab78c47566/round13-two-pool-work/runtime/two_pool_tail_search.py /workspace/scratch/c0ab78c47566/boss7-round13-two_pool_tail_search.json /workspace/scratch/c0ab78c47566/round13-two-pool-work/rerun
```

上述保留的是实际执行路径，落盘后不改写为从本证据目录运行。原main调用1次、coefficient_tables1次、test_parameters809次；未先跑测试批，没有第二轮全网格，也未重跑历史canonical crosscheck。记录器拒绝覆盖已有execution或相邻输出。将来复现应另建目录并复制未改原件，避免原main覆盖源码旁同名JSON。

## 有限域与结果

主搜索固定旧三C、新一组、18标签、x6、a4，四个池在整数0…18，初始19⁴=130321点。末位D₂对两类B的必要BR条件留下103474点，完整按808批128点加最后50点检查。每点保全部18³有序叶和全部末BR平局，以max–min和弱收益过滤求精确三人尾可支持性。

38130点可支持指定末两步D₁,D₂，65344点不支持；整条C₃,D₁,D₂无通过点。被动捕获同时给所有检查点的12倍根门槛最小84，末两步支持点也最小84、最大420；80个支持点达到84，首个为 `(6,4,0,7,4,3)`。目标首收益为6，因此最小门槛7已严格排除。这些额外门槛来自本次原返回，不冒称429B历史JSON已有此字段。

这精确排除本有限参数域的指定三人尾及指定六行动路径，不排除其他路径、不同参数或一般模型。即使忽略IC只看候选终局，其W/OPT₆=(24+S)/(40+S)≥3/5；源码“5/3”目标不是已获六人SPE比值。

## 独立核验与相关比较

配套数据任务保存历史[2686B交叉程序](../two-pool-tail-search-data/related/crosscheck_tail_oracle.py)、[3839B十二例报告](../two-pool-tail-search-data/related/tail_oracle_crosscheck.json)。历史12例的canonical threshold相同只是有限对照，不是全网格的另一证明。

本轮共享[定义级脚本](../two-pool-tail-search-data/independent_client_audit.py)新增12历史参数加全零退化参数，13×5832=75816叶；[单例脚本](../two-pool-tail-search-data/audit_minimum_case.py)再核被动观察的最小点，5832叶。两入口均不调用原函数或规范求解器，结果见[unit-client-audit.json](../two-pool-tail-search-data/unit-client-audit.json)及[minimum-supported-tail-case.json](../two-pool-tail-search-data/minimum-supported-tail-case.json)。本包只实读并解析这些已执行证据，没有重复数学运行。全零例全部18×324可信对子保留；最小点A₀孩子有20可信对子、最低首收益7。

完整历史终局递推给本文两层可信过滤的数学依据；九客户两池构造只有g0/p6/m3及43有序动作，不能搬至本g3/p18背景；另一公共锚点族使用不同交叠结构，不能因同有门槛7而合并；产品门槛的Cartesian假设在本18标签目录不成立。正文保这些比较与可接续缺口，manifest绑定实际所读材料。

本源完整处理；原冻结输出及相关crosscheck源码/报告由数据对象负责，本receipt不代其它源完成登记。阶段三关系由父方处理。
