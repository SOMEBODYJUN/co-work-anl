# v6 准备状态更新

原准备阶段为866 raw且0优化器。Main随后正式释放新增ROOT30第二尾容量反馈，最终合同为867 raw、257列：冻结546旧行+320 P25+1 ROOT30_B2_CAPACITY_FEEDBACK。全部旧31及ROOT30原行保留，不覆写。

当前`main_release.json`记录本会话收到的明确释放及准确SHA，`preparation_config.json`已更新。`ingest_rows.py`只准确装配、不调用优化器。独立来源预检通过后，方可执行本轮唯一LP。源族数值正除数25，根行1，精确输入一直未缩放。

已pin此前163个冻结文件。v5的原始/对偶、proof及其31/25诊断全部保持冻结。来源详情将在`source_review.md`中于LP前写入。
