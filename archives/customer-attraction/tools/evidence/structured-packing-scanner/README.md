# 结构化相对私有块扫描器证据

正式完整合同见[程序对象](../../../state/程序/结构化相对私有块策略锥扫描器--程序.md)。状态为`local-prepared`，待Boss串行推送；此证据包不执行claim、done、checkpoint或Git写入。

`original/structured_packing_scan.py`是源ID `df0869a6fbef9062a300` 的原2000字节，`original/`另两程序只供全文比较，没有执行。原入口的硬编码相对输出路径仅在`rerun/`内创建。

从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/structured-packing-scanner/replay_original.py
python3 archives/customer-attraction/tools/evidence/structured-packing-scanner/build_manifest_and_check.py
```

第一条执行未改原入口n=4、5、6，用返回帧观察器记录全部moves/rowids，并以Fraction核整数种子的精确IC和末位优先动作。第二条只检查保全SHA、三份原格式复跑报告与冻结报告逐字节一致、JSON、frontmatter、相对链接及receipt targets。

主要记录为[manifest](manifest.json)、[全文比较](comparison.json)、[运行元数据](rerun/run-metadata.json)、[stdout](rerun/stdout.txt)和[交付自查](self-check.json)。`observed_n.json`保留源程序实际产生的完整策略与行标签，原JSON仍按原样输出在其硬编码相对目录中。

原最终LP浮点点仍可能有微小负IC及归一化误差；本包不将HiGHS成功或SHA相同当作精确证明。三份报告对象分别独立重建有理primal/dual并认证其有限锥最优值。目标始终为相对A、n叶的最小私有块除根收益，不是half或首步损失目标。
