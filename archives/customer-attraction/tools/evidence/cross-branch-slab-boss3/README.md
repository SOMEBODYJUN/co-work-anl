# 固定R阈值的B枝条件cube：原源码、两份float报告与输入几何

三primary共13285B，原字节在`original/`；完整指纹/双冻结定位见[source-manifest.json](source-manifest.json)。正式对象：[固定回复阈值的实际末主题跨枝条件抬升](../../../state/程序/固定回复阈值的实际末主题跨枝条件抬升--程序.md)。它完整保存build/solve/三种入口、未触发的精确恢复资产及两报告范围，不把原float infeasible升级为全域结论。

代码输入是已保存的R5 5277点，SHA `303291e7ec19437d226bb8d33d3e689beaf54f52103fde53a12e28f1058f806a`。固定K/hist/R边缘并选共同阈值R联合，旧Z/RZ和新B条件态重新分配；普通Yi的actual报价仍未加入。code以alpha/beta共同sector来支持cross查询和强PAIR，不能把前批旧B状态或其一条漏价直接冻结到这里。

本次只执行标准库[audit_input_geometry.py](audit_input_geometry.py)一次，exit0、stderr空，约.049秒；[执行记录](replay/geometry.execution.json)、[stdout](replay/geometry.stdout.json)、[完整结果](replay/input-geometry.json)保全部24slab和R位。原程序module import/build/main/ablate/verify/solve/QR/精确恢复、float LP及SPE求解全为0。未重造41649矩阵，未重跑历史消融。

精确输入计数：11正hist、24slab、192sector，alpha192+beta2416=2608 core，overlap16816，总19424变量。5277+180终局+24cross+72B-PAIR+2416 beta界+48 slab等号行+33632 overlap界=41649。三删行范围41553/41577/41625与报告全相容；这是输入及循环合同核，不是当前不可行证书。

两历史报告仅有float状态：full41649不可行；no-new-cross41553可行；quotes-only41577不可行；branch-pairs-only41625可行。可行没有有理点，不可行没有有理Farkas；报告未附source/code SHA、命令或原完整日志。正文解释CN的条件诊断、W固定而非优化、真SPE/完整域边界。

`--verify`需要本冻结批次未提供的cross_branch_slab_exact.json；不能因为源代码包含此分支便执行出一个虚构PASS。`--ablate`在verify之前分支，两个旗标同时出现仍会运行三次float LP。默认入口和消融会覆盖源码目录输出，因此本包不直接运行`original/`。

若未来另建执行树，可先在仓库根只恢复依赖，目的目录必须尚不存在：

```sh
python3 archives/customer-attraction/tools/evidence/cross-branch-slab-boss3/materialize_runtime.py /absolute/new-cross-runtime
```

材料化程序按47母依赖、5耦合源、4 latest源和本批3源的既有清单核SHA并恢复59文件，不执行数学、网络或凭据；需要的NumPy/SciPy/原current build链由原路径保留。之后是否进行新的float发现或有理恢复应按实际研究目标另定，不把材料化计成原入口事件。

[comparison-manifest.json](comparison-manifest.json)保全文比较及前批同字节复用身份；[relation-review.json](relation-review.json)分开条件会员构造、真实行推导、输入限制、原float消融、当前几何核和未交付exact路径。前批5277全行/价格证据与父方5692 pending核验归各自对象，本批未重复执行。第三阶段图未改。逐源receipt为`cleanup/workspaces/Boss3/receipts-20261101-cross-branch-slab.json`，由Boss3在正文推送后串行done。
