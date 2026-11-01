# 五份笛卡尔资源来源的实质清洗与确定性重放

本目录配套两页独立新正文：

- [不交资源笛卡尔目录的精确边缘计数递推](../../../state/程序/不交资源笛卡尔目录的精确边缘计数递推--程序.md)：整数收益、集合递推、全部有序历史拼接、输入及输出边界。
- [两层笛卡尔补偿族的完整策略与分量极值精确核验](../../../state/计算/两层笛卡尔补偿族的完整策略与分量极值精确核验--计算.md)：十二完整策略例、十二全SPE边缘最小例、旧新版本与安全端点字段。

## 原件与版本

`original/` 内五文件均逐字节保留，合计52058字节；`source-manifest.json` 保原ID、双冻结commit、Git blob、SHA256、大小及正式保存路径。两个程序只有标准库依赖，无规范solver。主源JSON全部字段和子对象都已读取、比较；不是只核文件名或统计摘要。

`related-context-manifest.json` 保相关正式数学对象及原构造全文的读取身份和用途。它们是比较来源，不在本批新增primary或done；历史缺blob页的“0原运行”保其当时状态，不由本轮覆盖。

## 本轮实际运行

均在clone外独立stage完成；本轮执行恰为以下两项，没有随机CLI、LP/MIP、网络或第三种数值检查：

1. `python replay_complete_policy.py`：内部以当前解释器调用冻结 `original/verify_coupled_cartesian.py --max-n 9 --output replayed_coupled_cartesian_padding_audit.json` **一次**。原CLI输出文件采用`x`模式，禁止覆盖。输出与冻结padding JSON逐字节相同；仅删除每例两新增字段，生成 `replayed_pre_padding_projection.json`，与旧audit逐字节相同。这项JSON投影不是第二次策略审计。原CLI stdout/stderr为空，wrapper另保存结果摘要。用时3.452秒，12例、80803DAG键、439866全局比较、10557分量比较。
2. `python replay_finite_components.py`：以`runpy`导入冻结scout的`solve`，固定$n=2\ldots13,b=3n,s=2n,d=3$，12次联合加24次单分量，共36次函数调用。检查指定根目标成员，完整比对原报告字段及组合状态数；`replayed_finite_component_diagnostics.json`与原件逐字节一致。用时5.572秒；stdout记录每例时间，stderr为空。未调用scout的随机`main`。

`complete-policy-event.json`、`finite-components-event.json`保实际命令/耗时/计数/输出SHA等；stdout/stderr及wrapper原码全保留。既有历史JSON没有自己的event或程序SHA，本轮新事件不倒填历史。

## 范围

完整策略DAG认证给定原九主题策略的全历史最佳回复；全集递推在十二输入上求全部完整纯SPE的终局边缘及最差福利。计数缓存不强制一般SPE匿名。安全padding字段只算旧最优覆盖与最大安全端点的卷积，不添加新主题或认证扩充后的完整策略；存在性另引已证同人数扩充定理，分数端点须全实例同倍单位化。两类计算与全参数证明、全SPE福利闭式、六人half开放问题都不混同。

`self-check.json`是最后一次不调用数学程序的静态交付核对，检查保存字节、receipt目标、相对链接和两个event；没有增加数值运行次数。
