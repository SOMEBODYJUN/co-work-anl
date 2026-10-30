# 构造与布局障碍的冻结记录清点

本目录保留[逐项证据口径对象](../../../state/计算/构造与布局障碍记录的逐项证据口径--计算.md)的完整源数据与本批数据检查入口。

| 文件 | 冻结来源ID | 原字节数 |
| --- | --- | ---: |
| frozen_exact.json | 2cdff156aaa9614bb607 | 372123 |
| frozen_lexmax_barrier.json | 754b7f16d578df1fd751 | 527820 |

两份原文件固定于提交68fad804ec5946cb296f77dc5b336308a66abf12，分别对应 evidence/runs/kfac_two_exact.json 和 evidence/runs/kfac_lexmax_barrier.json；均原字节保留，SHA-256在 [record_inventory.json](record_inventory.json) 中。没有修改原Python字段或改写旧字段名称。

[inspect_records.py](inspect_records.py) 是本次清洗新增的数据清点器，仅使用Python标准库。它先核两份文件的固定长度和hash，再完整解析563条构造记录及20组布局障碍记录的1552条偏离见证。

本次已实际运行并保存record_inventory.json。它重建全部输入生成顺序及固定随机输入，核对每条构造记录的布局、负载质量和计数；对布局障碍记录核完整偏离键、策略覆盖可行性及偏离者负载。它没有执行构造器、均衡搜索、最佳反应检查、全局最优枚举或默认续局求值。报告中的历史聚合数仍保持其证据层级，没有从缺失轨迹重建装箱或改善过程。

重做清点时使用一个新输出文件：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-record-inventory/inspect_records.py --output /tmp/facility_record_inventory_new.json
~~~

需要Python3.10或更高版本，普通模式运行，不用 -O 关闭断言。程序拒绝覆盖已有输出；既有输入只读。脚本没有网络或Git操作。

布局障碍全部均衡见证的真实复跑是此前完成的[20实例审计](../factor-two-audit-suite/README.md)，其输出除Python版本外与本目录原barrier JSON全内容相等。本批沿用该实测，没有重复执行。完整exact审计仍未在此次清洗运行；此处的563记录清点不能称为一次新构造审计通过。

若需执行原审计程序，使用另存的[固定19文件重建入口](../factor-two-audit-suite/reconstruct_snapshot.py)，范围与命令见其README。它支持8程序、4历史lexmax证书、4示例和3冻结输出的明确核心快照；不代表整个当前冻结源树。
