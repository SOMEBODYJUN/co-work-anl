# 五人根付款与第三位查询松弛的来源和复核

本批10个正式来源均全文读取；[source-manifest.json](source-manifest.json)逐项记源ID、完整双冻结commit/path、SHA256及已存在原字节位置。它们与分配给本组的冻结local_source逐字节相同，没有改写原文件或从旧receipt推断完成。

对应正式正文：

- [五行付款引理](../../../state/引理/五人根到末回复的五行付款包络--引理.md)：真实根D分支、两个同策略索引族、五行合法证明、8态包络和固定旧点的精确分离。
- [根程序合同](../../../state/程序/五人根付款的原程序与必要条件发现记录--程序.md)：标准库精确审计、181行及simple发现、两段根末回复链。
- [第三位松弛合同](../../../state/程序/五人第三位查询松弛的原程序与可信性边界--程序.md)：19008型78行完整语义、浮点报告及77行后续诊断的版本边界。

`replay.py --all-discovery`在新建且拒绝覆盖的输出目录复制所需**原字节Python文件和旧点输入**，不复制任何待生成JSON。五次实际原入口事件保在[replay-001/runs.json](replay-001/runs.json)：全部exit0、stderr空、输出逐字节同相应冻结JSON。每次包含精确argv、cwd、脚本/报告SHA、开始时间及运行前输出不存在的断言。此处是本轮原CLI复跑；既有`five-prefix-interface-and-root-D-primary/replay-exact-001`的旧事件没有冒称本轮执行。

`inspect_reports.py`独立使用标准库重核10源指纹、三个报告的精确质量加权负gap、所有发现权非负，以及simple的64个最大值。它还逐64×8×8=4096态核depth2报告正权退化为simple地板的原因。完整结果见[report-inspection.json](report-inspection.json)。它不重新独立构建181行全部系数，不证明ROW3浮点点的精确可行性或最优值；报告明确将这两项标为false。

六份全文读过的相关来源位于[related-source-manifest.json](related-source-manifest.json)，只是比较证据，不在本批新增done：77行旧支持、其精确材料化报告及说明、浮点材料化源码、内部peer审查、父方ROW3工作稿。它们说明1.5084908438192186的当前78行点与1.51707147的旧77行点不能混作同一输入。

这些结果分别是普遍必要行、指定松弛点分离、浮点发现和某旧拟定回复的可信性诊断。没有创建完整五人/六人反例，没有将加强命题失败转成半覆盖失败，也没有建立阶段三超图。
