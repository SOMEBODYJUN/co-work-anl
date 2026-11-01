# 全部实际前缀保底行的无界松弛族

正式对象：[全部实际前缀最坏分母保底的无界松弛族](../../../state/障碍/全部实际前缀最坏分母保底的无界松弛族--障碍.md)。保稳定旧Claim `B7-ROBUST-PREFIX-FLOOR-UNBOUNDED-v1` 和新对象ID；类型为障碍，未把低覆盖指定路径当作SPE。

四primary原件全文实读：5275B发现稿、4678B独立重构稿、3086B标准库审计、6424B结果。全部来源的双冻结提交、ID、blob、SHA及保存路径在 `source-manifest.json`。另保存1744B同工作区README与3187B旧next_security README，仅作相关比较、不额外done。

## 数学内容

每个m≥2构造2m个真实共同目录主题、正整数单位客户类型，实际路径无拥挤，比较m主题覆盖全部客户。全部2m²实际前缀/全目录最坏分母行通过，实际末位是唯一BR，OPT/W=m/H_m无界。倒二改A_m后所有末位BR恰T_j，偏离统一严格获利，所以该指定路径不属于任何完整历史纯SPE。正文给一般证明、m=2端点、m≥5严格低于half和m=6的完整整数特例。

`six-player-formula-instance.json` 是本轮由公式直接代m=6写出的42类客户输入，含全部整数重数及12主题；不是历史原件，也不是完整策略或另一次SPE求解。2160名客户、actual覆盖882、OPT6=2160，倒二获利180→330。

## 本次运行及历史报告差异

只在clone外新目录执行原3086B程序一次，约0.251秒、exit0、stderr空，19个m=2…20结果全部精确相同，共5738条RF行。原程序还核实际末位所有目录动作以及倒二离轨节点的全部末位动作，保任意平局。没有LP、完整根BI、SPE求解器或第二套数值实现。

冻结报告根字段为claim/parameters/arithmetic/results/universal_basis，原main stdout为claim/status/results，所以完整输出字节不同；所有results、claim及参数列表精确相同。旧报告没有源码SHA/argv/UTC，当前事件不能倒填历史绑定。一般结论由解析证明承担，有限重放只核这份实现。独立review自述依据构造说明独立重建且未读发现稿；当前是知情数学比较，不另称盲审或外审。

## 复现

复制 `original/8893e23807e2ef69051b/audit_robust_prefix_floor.py` 到仓库外的新目录，保持assert开启，执行 `python3 -B /absolute/new-runtime/audit_robust_prefix_floor.py`，将stdout保存为新JSON。仅需Python标准库，无输入、网络、依赖目录或认证。原码main只输出stdout，不写文件；导入只定义函数。新事件耗时/路径可不同，勿覆盖归档输出。

|文件|作用|
|---|---|
|`original/<source-id>/`|四primary冻结原件，未改字节|
|`related/<source-id>/`|两个完整相关README，仅作比较|
|`source-manifest.json`|六源身份、冻结版本、SHA及实际保存路由|
|`replay/execution.json`|当前一次真实运行的源码SHA、argv/UTC/耗时与退出码|
|`replay/stdout.json`、`stderr.txt`|真实输出字节；stderr为空|
|`replay/comparison.json`|19结果逐字段全等、5738行数、元数据不同及六人结果|
|`six-player-formula-instance.json`|本轮从一般公式直接实例化的可重用有限输入|
|`related-mathematical-comparison.json`|已全文对照的正式对象及关系边界|

原四人LP约2.195只有未冻结的发现叙述；本m4家族为48/25，不能替它补精确证书。全历史限制字母表障碍、静态证书表示障碍、本全目录实际前缀分母障碍分别保存。分数覆盖前缀引理仍有效；本族Y私有块迫使全集分数覆盖数恰m，且非SPE，不用它声称真实SPE锐性。
