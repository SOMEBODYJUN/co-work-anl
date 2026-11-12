# visible_maximum_joint_v6_solve_v2：严格来源接口修复，等待Main复核

状态：`WAITING_V2_MAIN_REVIEW_AND_NEW_EXPLICIT_RELEASE`。实际agentID仍为 `/root/visible_joint_v6_solve`；Boss1 / six-boss1-20261111 / full。累计优化调用0，原消费标记不存在，原release已撤回；本包不含Main release。

原preflight发现冻结 `source_pins.json` 的实际schema为 `v6_exact_read_set_pins_v1`、files列表44项，而旧gate要求sources字典。原代码及失败回执已独立冻结，新包从原9core复制并保留逐行patch，只做明确接口适配和必要的更严格边界。

适配器固定44个唯一规范repo路径及完整SHA/bytes，只接受精确schema与字段；缺失/重复/未知/错SHA/错大小/多余字段拒绝。全清单通过后逐文件核内容SHA与大小，在内存重建sources映射；后续source_route检查完整保留。不改冻结输入、source_pins、metadata、数学来源、尺度或行序。

完整输入保持4177=3056+230+160+550+180+1，513非负列、2自由等式、30条rhs=-1；父3056对象与尺度字符串literal保留，新1120行除数25、ROOT270最后行除数1。原objective、K、零行、重复、弱尾均不动；不加入新cap3。

Main明确允许的 `preflight.py --repair-read-only --write-report` 可读取实际完整输入与全部44来源进行零优化校验。旧release只作为已撤回且SHA固定的input/evidence字段来源，其原优化许可不传播；solver入口仍只认新的solver-v2 Main gate。此修复阶段确已接触实际source_pins与输入，不能将其描述成从未读取来源的最初静态准备。

准确X模型：给定完整纯SPE的actual A1,…,A6，P_y是前四负载，一次选择X∈argmax_Q f_P(Q)，f_P(Q)=Σ_{y∈cov(Q)}1/(P_y+1)，最大范围为全共同合法目录，所有会员位/查询/强制分支用同一个X。不对其他背景声称最大性。C为最大裸覆盖标签，O为OPT6六标签覆盖并；只在OPT6>0归一化。新增局部任意合法T可特化为该X，不能取消旧行X最大性。旁挂更正和semantic release内容SHA会直接纳入加载pins。

最终静态检查要求全部9core解析编译、唯一优化调用及固定highs-ds/60秒/presolve=False/双tol1e-9、gate→exclusive+fsync marker→call顺序、checker独立性和14个拒绝案例通过；完整repair报告另外核全部44源内容、4177行/513列/2等式/原metadata。freeze仅在代码与两报告SHA一致后执行。

交Mainreview文件包括 `core_interface_patch.diff`、`source_reference_pins.json`、`predecessor_obstacle_pins.json`、`repair_read_plan.json`、`repair_preflight_result.json`、`scaffold_static_check.json`、`scaffold_manifest.json`及`SCAFFOLD_SHA256SUMS`。本轮不执行LP，不生成任何primal/dual/face；冻结后停止写入等新明确release。

## 本次实际零优化加载结果

`repair_preflight_result.json` 返回 `PASS_ZERO_OPTIMIZER_REPAIR_FULL4177_SOURCE_PIN_INTERFACE`。全部44文件内容SHA及bytes验证通过；全4177原行、513非负列、2自由等式、3056字面父行、30条rhs=-1、4177条catalog和新来源路由通过。零系数行索引[45]以及全部560类精确重复约束保留在报告中。全读入pins共83项，包含独立X更正、语义释放、输入资产和全部来源；未递归展开旧来源metadata。原/新消费标记均不存在、新Main release不存在、累计优化调用0。
