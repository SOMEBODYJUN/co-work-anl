# 索引回复的真尾利润子集投影证据

主源 `72c498d7803e037d9c4b`，[原程序5730B](../continuous-query-refinement-program/related/tail_reply_subset.py)，SHA-256 `9f812b0381186aa8546a038416b6335424673cbf1f895e8da40f7b6f4baadfdc`。正式说明见[程序对象](../../../state/程序/索引回复的真尾利润子集投影程序--程序.md)。原件、默认816661B点和已有5075全图事件均复用共享保存位置，不重复持久复制大数据。

## 原搜索没有在本次重跑

源码只有发现入口，没有verify：main固定枚举4位置×2会员×3轨道×4比较=96个结构，每个调用浮点LP找alpha/gamma。冻结报告仅534B，`selected=[]`、`best_float=[0,null]`，且没有每个LP的成功状态或精确对偶。这里不把初始化哨兵当精确最小值0，不把空列表当所有参数已认证无分离。

本次原main、discover、linprog调用均为0。没有重跑默认点的5075图、已保存的原发现搜索或其它完整策略审计。当前新增的是下面明确有限范围的原helper对照。

## 两次有限helper尝试

实际第1次运行在完成所有结构与系数比较后，于末尾**错误的计数期望**触发AssertionError：4×2×3×4实际为96，脚本误写192；三价格向量实际288，误写576。失败代码原字节保在[attempt1.py](attempt1.py)，其SHA、原工具traceback和退出1保在[failed-attempt.json](failed-attempt.json)。没有生成成功报告，不隐去这次失败。

仅修正计数及相应说明字符串后第2次有限核通过，脚本为[audit_helpers.py](audit_helpers.py)，SHA `fcf4770fdeb1ea9d062f49c591b4e26479636937a3fd183bea117d44c603c52a`。实际调用：

```sh
python /workspace/scratch/c0ab78c47566/tail-reply-subset-helper-audit.py /workspace/scratch/c0ab78c47566/round12-tail-reply-subset.py /workspace/scratch/c0ab78c47566/boss7-cleaner/archives/customer-attraction/tools/evidence/continuous-query-refinement-program/related/continuous_refinement_exact.json /workspace/scratch/c0ab78c47566/tail-reply-subset-helper-report.json
```

Python3.12.14，退出0，成功核的数学部分用时3.932秒，输入与原程序前后字节不变。脚本以非main模块名导入原件，显式只调用comp_rc、states、coefficient_rows；它不是原发现入口复跑，也未修改原函数。全部结果保[helper-audit.json](helper-audit.json)，包括288条具体参数、slack与非零系数数。

| 精确检查 | 成功核的实际范围 |
| --- | ---: |
| 原超几何值与显式r元组平均 |14336次，3584个不同输入状态|
| 源码存在但未被发现器搜索的重复主题分支 |520次|
| 原states与显式有序索引对质量 |96结构，全部质量和1|
| 完整系数数组 |96结构×3固定价格=288数组|
| 逐列精确相等 |288×1905=548640项，含零权列|
| 原系数点积与直接状态包络 |288项，全部精确相等|

三个非负价格为(alpha,gamma)=(0,0)、(1/3,2/5)、(7/5,3/2)。288个slack在此点均正；这些选定参数只是实现合同回归，绝不证明整个连续参数族非负。程序的一般行合法性来自真后继背景利润定理、实际源IC及同一个实际末位报价，见正文自足推导。

显式比较枚举保留对角 `opt_include_ij` 的两次同一T，以及r=1时只含首索引的退化。独立系数实现按全部具体有序索引对展开，不使用原组重数公式；共同元数据仍是同一冻结1905列。检查不证明该松弛点全部旧交叠坐标有共同客户实现。

## 身份、自查及复用

[source-manifest.json](source-manifest.json)绑定主源、534B空报告、816661B点及已有5075事件；[self-check.json](self-check.json)只保存包内哈希、JSON/代码语法、完整报告统计、链接及回执一致性检查，不再次调用数学helper。数据源由配套[空报告对象](../../../state/计算/回复子菜单查询的空切面报告--计算.md)处置；它复用这次helper事件，不再另跑96结构。

未来要独立复现有限helper核，可从仓库根显式调用保存脚本，并给一个不存在的新输出文件：

```sh
python archives/customer-attraction/tools/evidence/tail-reply-subset-program/audit_helpers.py archives/customer-attraction/tools/evidence/continuous-query-refinement-program/related/tail_reply_subset.py archives/customer-attraction/tools/evidence/continuous-query-refinement-program/related/continuous_refinement_exact.json /absolute/new-helper-audit.json
```

该命令只复现有限函数检查。不要给原main添加不存在的 `--verify` 并误认为它会跳过发现；也不要在冻结原件目录直接运行会覆盖输出的main。改变点或参数域需要新记录身份与范围。
