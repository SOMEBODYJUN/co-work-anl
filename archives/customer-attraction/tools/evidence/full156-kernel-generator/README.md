# 完整156主题阈值生成器：证据边界

主源 `30ffd5d8405d7bc16953` 的完整语义在[正式程序对象](../../../state/程序/完整156主题的阈值物化收益矩生成器--程序.md)。

- `original/full156_tail2_kernel.py` 是clean show导出的7510B冻结原字节，未改。
- `source-manifest.json` 记录主源、两个输入和两个输出原件的SHA与共享路由；大JSON不在本包重复保存。
- `check_input_contract.py` / `input-contract.json` 是本轮新增的组域、隐含00、分段、R位/Z界、尺度和轨道审计。没有LP可行性或完整SPE认证。
- `run_original_once.py` 是本轮运行包装器：源码与输入复制到clone外临时目录，默认及`--with-welfare`各一次，assert开启；独占创建rerun目录防止误覆盖。
- `rerun/` 保存两次完整stdout/stderr、解释器/命令/源SHA、执行结果和逐字段比较。所有48828个F/G/U整数及24336个福利整数均等冻结数据，只有kernel的seconds及福利绑定kernel_sha不同。

临时新矩已删除。`comparison.json`对每份输出给冻结路径、冻结SHA、新输出SHA及changed_fields。对冻结JSON按原键序加载，把每个changed_fields的rerun值替换到相应顶层键，再以`json.dumps(obj,indent=2)+'\n'`编码，就能恢复新文件；原运行包装器已实际核恢复字节与输出完全相同。不要把“数学字段相同”写成原文件逐字节相同。

新增客户类型实现由[收益矩证据](../full156-payoff-kernel-data/)和[福利矩证据](../full156-welfare-kernel-data/)分别保存；本包实读其脚本及结果，不再次运行原入口或重复代领它们的来源。两份点的5108/10344行数仅为旧字段身份；本生成器从不重建那些LP行。
