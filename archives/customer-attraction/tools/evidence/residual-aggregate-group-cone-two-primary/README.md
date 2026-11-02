# 固定三人两组残余聚合锥：两主源与一次最小重放

两主源是R642 `security_aggregate/cone_probe.py`（405e84b2e7073aa41e92，2817B）和`cone_probe_output.json`（e71802a0f07bfa587554，1096B）。父方串行`clean show`导出后全文读；两份原字节与元数据size/SHA256匹配，保存在`original/`。同目录`probe.py`（65bccd3aa2af649ab6c1，4708B）是相关helper，全文读取，只为`multisets`依赖，不记本批done。完整来源提交、blob、路径、SHA及19份全文比较记录见[source-manifest.json](source-manifest.json)。

正式正文：

- [程序合同](../../../state/程序/三人两组完整策略的残余聚合安全锥探针--程序.md)：43有序节点、215真实非自身激励行、21全部静态背景、64变量的3t−P分离目标，以及固定p/固定σ/背景采样的范围。
- [原保存点与另名归一校准](../../../state/计算/残余聚合安全锥的全兴趣保存点与概率归一--计算.md)：mask63单客户、旧五人加残余三人、P3/8与v1/8等号；原p在十进制及binary解释下均略超概率总和1，不能直接成为精确查询证书。

证据保全和运行：

- `original/cone_probe.py`与`original/cone_probe_output.json`保持源身份。`related/probe.py`是只相关依赖；`related/security_aggregate-README.md`是已归档旧入口的相关副本。
- `replay/cone_probe.py`、`replay/probe.py`是同字节运行副本。原main仅运行一次：`python cone_probe.py --samples 1 --seed 172912 --output one-sample-new.json`，退出0。新JSON的best与历史best按普通float解析后相等；请求数1与旧1500明确分开。工具合并stdout/stderr的原样输出转录在`replay/one-sample.stdout.txt`，没有单独stderr捕获，不冒空stderr证据。
- [audit_saved_point.py](audit_saved_point.py)独立以Fraction重构完整策略和全部系数，并加载原函数作21546项数值系数对照；不调用其main、不用LP、不扩样。它只执行一次，退出0；[完整新报告](exact-saved-point-audit.json)、[stdout](exact-audit.stdout.txt)、[stderr](exact-audit.stderr.txt)及[运行说明](execution.json)分别保存。审计stderr为空是本次subprocess实际捕获结果，与原main未独立捕获stderr有别。
- 精确报告还给两种另名归一p的全部分数、43个动作、m0,…,6全兴趣边界各258比较及零客户边界。概率域的原始不合法性仍在报告内，没有把PASS解释为原p已认证。

旧1500阴性没有重跑，不给全p、全背景或全策略安全性；旧负零不是严格负数，归一前约10^-17假正也不是真聚合反例。程序中变量质量截面不是删零客户模型，残余P不是根覆盖W。恰六人全历史half仍未由这些文件闭合。

[comparison-and-relations.md](comparison-and-relations.md)逐条解释本批对象与现行正式正文的作用和限制，不直接复制旧图。此包没有Git写、claim/done/checkpoint或公屏操作；正式保存状态由父方实际发布回执决定。
