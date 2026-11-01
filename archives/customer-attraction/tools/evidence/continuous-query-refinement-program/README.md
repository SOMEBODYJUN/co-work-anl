# 连续旧查询迭代精化证据

正式对象：[连续旧查询切面的迭代精化程序](../../../state/程序/连续旧查询切面的迭代精化程序--程序.md)。主源 `4a76f48dc6135747f165`，3324B，SHA `9af39d9eecc13ff203713ed60e2058b9d8faa2a6cd8836a76b952201b4da5e19`。

本轮唯一原入口是 `refine_continuous_queries.py --verify`；5075行（5043+32）、1905列，精确最小slack=0，退出0、stderr空。没有运行自适应发现模式，没有重跑已交付的5108入口。原始事件在 `rerun/execution.json`，147B stdout SHA为 `807f019d2fb8c5eb70c760563bbb120d600d565112bfe816e9f2a17e9875b6e2`。

| 文件 | 作用 |
|---|---|
|`original/refine_continuous_queries.py`|主冻结原件，未修正代码或参数边界|
|`related/continuous_refinement_exact.json`|816661B精确点原件，其他本轮数据对象共享此件|
|`related/refine_terminal_portfolio.py`、`tail_reply_subset.py`、`HANDOFF.md`|完整实读的后继消费者与历史交接；静态比较，不属于本次运行依赖|
|`source-manifest.json`|37份运行源的共享位置、3份静态比较源、全部源ID/冻结SHA及来源|
|`rerun/`|原verify事件、原stdout/stderr、实际组织脚本和37源清单|
|`audit_point_interface.py`、`point-interface-audit.json`|当前独立检查完整点接口和与5108点的124坐标差异，不重建图或求LP|
|`materialize_runtime.py`|仅按清单复制原字节到新目录，不自动运行原程序|
|`package-check.json`|打包自查结果|

基础依赖复用 `combined-branch-master-program/dependencies/` 中已核原字节，32条数据复用 `continuous-old-query-cut-data/related/continuous_refinement_cuts.json`，没有重复持久大依赖树。37源清单不含早期64表、实际B投影器或联合master入口；这些均不是本原verify所需输入。

实际运行先在clone外原相对路径布局完成，随后保留日志字节。`rerun/replay_verify_once.py` 是当时组织脚本，要求其邻接 `frozen-input-manifest.json` 及完整原路径；归档位置不冒作实际执行cwd。根 `work.py` 只是注释标记，供旧模块上溯定位，未导入/执行控制器。

将来要复现另一个独立事件，可在仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/continuous-query-refinement-program/materialize_runtime.py /absolute/new-empty-runtime
python3 -B /absolute/new-empty-runtime/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/refine_continuous_queries.py --verify
```

需要NumPy和SciPy，assert须启用。第一条仅恢复路径，不执行历史代码。本轮没有因测试材料化工具而执行第二次入口。不要在冻结证据目录运行发现模式；它会覆盖cuts/trace/exact，且前两件写完之后精确恢复可能失败。

独立输入审计的复现命令为：

```sh
python3 -I archives/customer-attraction/tools/evidence/continuous-query-refinement-program/audit_point_interface.py --point archives/customer-attraction/tools/evidence/continuous-query-refinement-program/related/continuous_refinement_exact.json --reference archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json --source archives/customer-attraction/tools/evidence/continuous-query-refinement-program/original/refine_continuous_queries.py --cuts archives/customer-attraction/tools/evidence/continuous-old-query-cut-data/related/continuous_refinement_cuts.json --output /absolute/new-point-interface-audit.json
```

它完整解析1905列，核179正列、16hist、194隐含00、O/W/坏差及布局；保存所有124处坐标差异。它不独立生成1306交叠界或其余5075行，也没有重新认证所有连续价格。原5075与5108点同K、hist和W，但10组R及45组Z边际不同。

冻结inventory没有该程序输出的同名trace，因此不能从32条cut反推历史轮数。原程序默认最多7次主LP和6×180次结构LP，有限截断后无fresh不等于精确闭包。必要系统可行点、共同客户实现及完整历史SPE分开解释；本包不声明half结论。
