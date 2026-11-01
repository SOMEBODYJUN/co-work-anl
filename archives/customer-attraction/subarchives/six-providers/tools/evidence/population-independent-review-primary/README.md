# 十二客户人口独审：精确原件与比较

[计算对象](../../../state/计算/十二客户人口反例的独立全历史证书--计算.md)保存完整模型、代码生成/认证合同、全部证书字段、与旧版差异和当前执行边界。

三份primary按实际正常 `work.py clean show ID --out` 导出，size/SHA逐件与冻结inventory相合；[source-manifest.json](source-manifest.json)列两个完整来源commit、blob、ID、size/SHA及准确副本。

- [原审查](original/population_review.md)：4416B，f7f5a4f7cf4f5ce57c8c。
- [原标准库程序](original/population_audit.py)：5837B，b353df096f453d0cfdce；输入嵌入BASE，不需外部数学依赖。
- [原完整报告](original/population_audit.json)：56827B，1579392412b3df65bd7d；12份完整策略/276动作、所有根路径/数值/压缩表全文读完。
- [完整读取与来源比较](complete-semantic-read-and-comparison.json)：无损A/B/C动作读本及两版相等/差异。其[脚本](inspect_records_and_compare.py)只查schema、动作域和两个已有报告的一致性，**不计算效用/IC/SPE**；[唯一执行事件](current-comparison-event.json)明确原审计入口0运行。

comparison/保已有发现者原稿、原程序、原JSON及已有stdout，前三件也逐项核冻结size/SHA。它们是同一12客户实例的旧版，包含n5与all-theme边界；不能混入本独审n1…4/scale2/zero接口。没有重跑旧或新原入口，没有覆盖原冻结数据，没有凭据或Git变更。所有独立性均按原历史源作者合同保存，本轮同时阅读两版不自称盲审。
