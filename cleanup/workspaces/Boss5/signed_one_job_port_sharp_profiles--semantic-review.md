---
source_id: 30e9fd683b78907f45f5
source_path: examples/unrelated_machines/signed_one_job_port_sharp_profiles.json
source_sha256: 850f6d8451d56918c34de05a21a92d37d90dc197d63bbd63d2ba76089048bbe0
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/三外接选择器与单任务端口向下投影双源审查--审查.md
---

# signed one-job port sharp profiles 语义清洗

## 来源合同

冻结输入 `30e9fd683b78907f45f5` 位于
`examples/unrelated_machines/signed_one_job_port_sharp_profiles.json`，内容 SHA-256 为
`850f6d8451d56918c34de05a21a92d37d90dc197d63bbd63d2ba76089048bbe0`，两个冻结提交的路径和字节相同。JSON 只保存一个受限端口接口的输入/预测 profile，不含调度策略、求解器输出或一般性证明。

`claim` 是 `UM-SIGNED-ONE-JOB-PORT-DOWNSET-v1`，阈值 `T=1`。sharp fixture 有两个内部机器、四台外部机器和一枚只在两个内部端点上可行的单位任务。四个端口的内部时间均为 `1/2`；两个端口从内部 0 的 incoming bit 0 延伸到外部机器 2、3，另两个从内部 1 的 incoming bit 1 延伸到外部机器 4、5。输入预测 7 个严格 profile，并说明 projected relation 是“两个 A 端口同时外送或两个 B 端口同时外送”；这是端口向下闭集/状态数障碍的一个输入见证。

## 与已有单端口对象的对应

现有[三外接选择器与单任务端口向下投影双源审查](../../../archives/unrelated-machines/state/审查/三外接选择器与单任务端口向下投影双源审查--审查.md)与[单端口向下闭集与单home级联双源审查](../../../archives/unrelated-machines/state/审查/单端口向下闭集与单home级联双源审查--审查.md)已经承载该 claim 的数学接口：

* 单端口投影在外部容量不计、每端口只有一个内部端点时向下闭；两一致状态同时可行时，若有 (a) 个符号 0、(b) 个符号 1 的正时间端口，状态数至少为 (2^a+2^b-1)，零时间端口再给 (2^z) 因子。两台内部机器的构造达到该下界。
* 因此只用这种单端口 gadget 不能把严格阈值关系限制为全零/全一两个等值状态；翻转一个入向端口只删除非负内部负载，立即产生混合状态。
* 当两个端点都在内部，或把外部共同容量重新放回约束，向下闭结论不再适用；JSON 的 `negative_control` 正是这种被排除的两内部端点控制：矩阵全为 1，严格 relation 只保留 `(0,0)` 与 `(1,1)`，但它不属于单内部端口接口。

本输入的 `sharp` 字段与已有正文的参数化下界/达到例对应；`negative_control` 只用于说明模型合同的承重假设，不能被读成单端口结论的反例。

## 证据层级和边界

该 JSON 是精确输入夹具。它不单独证明 7 个 profile 的穷尽性，也不提供构造器或全部随机审计。既有审查中保存的 Fraction 审计、随机实例和 sharp fixtures 才承担有限验证；本源独有的是该 balanced (k=4) sharp profile 与明确的双内部端点排除控制。

建议将源标为 `integrated`，把源引用和 SHA 接入既有双源审查及其 evidence manifest；不新建第三个单端口对象。该结果只约束 unrelated-machines 的受限端口投影接口，不改变一般 UM hardness、近二近似、`UM-TARGET-v1` 或 customer-attraction 六人 SPE 覆盖目标的状态。

验证边界：`clean show` 导出后对 JSON 字段和有理字符串做结构读取；没有把输入 JSON 冒称为重新运行的构造器输出，也没有外推“有限 profiles = 全部 profiles”。
