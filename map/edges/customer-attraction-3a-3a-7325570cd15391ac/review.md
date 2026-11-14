# ZZ 阈值必要系统：固定点、会员实现与策略边界

## 任务与读取范围

本包沿 Boss1 身份处理任务 `customer-attraction-3a-3a-7325570cd15391ac`，核心对象为 `customer-attraction/zz-threshold-necessary-system-rational-point`，任务声明 pin 为 `ac10a798aeb36ec28d960c0e244f61431da8a4383a5fa314d7fc47ee118d28f0`。读取声明没有 `read_object_ids`、`overlap_comparisons` 或 `comparison_groups`；没有新增只读依赖，也没有把 deferred candidates 当作已付证据。

12 份 declared refs 全部逐文件读取并核对 SHA：6 份状态正文（模型、计算、程序、资源、拆分诊断、双格式审查）、5 份证据 JSON/执行记录（原 321 点、42 原子、3949 verify、接口审计、格式绑定）以及 1 份阶段账本，共 12 份。大 JSON 不是只看摘要：`zz_threshold_exact.json` 的 321 条变量、`membership-realization.json` 的 16 hist/25 slabs/321 重建/194 组/42 atoms/60 ZZ rows、`saved-format-binding.json` 的 25 modes/321 coordinates/42×156 位/42+18 ZZ 映射均解析到顶层和逐项计数；未执行原程序。

## 模型、量词和核心数学

共同模型是有限单位客户、有限非空共同标签目录和六名单位提供者。策略为 `sigma_i:S^(i-1)->S`，对所有有序历史、每个玩家和每个合法单方偏离，沿偏离历史按同一完整策略真实续局比较收益；允许空主题、重复行动、同覆盖异标签、零客户和任意离轨平局。目标对象不是六人 half 定理，而是固定旧 `cc48d8` 输入的有限必要系统点。

对象固定 16 个 hist、194 个 R 边缘、25 个共同 R 阈值层中的 321 个 Z 质量，重验 3889 个旧仿射行并加入 60 个 Z→Z 类。原点证据精确给 `rows=3949`、`variables_count=321`、`minimum_slack=0`、`O=1`、

`W=2590607258266118042503848518699183/5430547020889608346592960056661140<1/2`，134 个正变量（17 个严格内部）和 187 个零变量。它保存的是一份有限 necessary-condition 点：旧 Z/RZ 被释放并重选，不能称旧 1905 坐标原样保持，更不能称完整历史纯 SPE、顶点最优或一般目录结果。

## 共同会员与格式绑定

`membership-realization.json` 证明 42 个正质量代表原子可共同嵌套实现全部 321 个 Z 质量；194 个 R 边缘保持，1306 个 R-R 交叠取 `min`，56 个 Z 边缘和 257 个 1905 坐标发生改变（93 joint-reply、164 overlap），60 个 ZZ 余量为 29 正、31 零。它明确 `original_program_calls=0`、`LP_calls=0`、`old_3889_rows_regenerated=false`，所以这是静态点的会员实现，不是新一轮图求解。

C37 双格式绑定 `saved-format-binding.json` 把两份不同字节表示的全部 25 模式、321 坐标、42 个 156 位原子、42 个非空 ZZ 槽和 18 个空参考槽逐项绑定，`all_equal=true`。这只支持复用已有成熟事件的身份与坐标，不产生新的 LP、SPE 或 108900 边对重放。

`zz-threshold-closure` 历史执行一次 `--verify`：40.329713 秒、exit 0、stderr 0、冻结输入未变；其责任是旧 3889 + 60 ZZ 的 3949 行精确检查。接口审计和格式绑定是独立静态合同，程序 PASS 不能替代全历史 IC。

## 后续真实语义障碍与开放义务

同点对角拆分诊断的 56 行出现 5 负、2 零、49 正；其中 R 异索引 source 与 price 两行只依 hist、实际/比较会员和真 `R_ij=sigma_6(h,T_i,C_j)` 语义，不依 K、Z 或 R-R 联合，严格负值因而排除保这些统计和真实 R 身份的指定完整 SPE 骨架。该事实与有限 3949 行通过同时成立：合行可抵消，真实行拆分揭示缺失的预算条件；它不排除改变 hist/R 的后续重优化点，也不推出所有同支持点或一般六人 half 失败。

未付义务包括：强制实际第五位改 Z 后的新末位 Y、早期真实中间节点、全目录合法查询和容量、所有有序历史 IC、完整策略存在性及 `OPT_6<=2W`。低 W 与 42 原子不构成完整 SPE 反例；阶段账本列出的其它行数/点改变变量或约束，不能自动迁移。

本包因此交付一个 context-only self-check 边；没有正式 overlap 对，也没有后续任务需要发布。
